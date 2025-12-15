from fastapi import FastAPI
import psycopg2
import os
import redis

app = FastAPI()

# PostgreSQL Configuration
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "ecommerce")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "admin")

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def get_connection():
    """Connect to PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


@app.get("/")
def home():
    return {"message": "E-Commerce Backend Running"}


@app.get("/products")
def get_products():
    """Return products, using Redis cache when available."""

    # 1️⃣ Check Redis cache
    cached_products = cache.get("products")

    if cached_products:
        return {
            "source": "cache",
            "products": eval(cached_products)   # convert string back to list
        }

    # 2️⃣ Fetch from PostgreSQL
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products")
    data = cur.fetchall()

    # 3️⃣ Save in Redis with 30 sec expiry
    cache.set("products", str(data), ex=30)

    cur.close()
    conn.close()

    return {
        "source": "database",
        "products": data
    }
