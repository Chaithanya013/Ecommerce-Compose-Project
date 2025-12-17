# Docker Compose E-Commerce Backend

A real-world **E-Commerce Backend System** built using **Docker Compose** to demonstrate multi-container orchestration with Docker.
This project showcases how different services (API, Database, Cache, Worker, Reverse Proxy) work together in a clean and understandable way.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Architecture](#architecture)
* [Project Structure](#project-structure)
* [Technologies Used](#technologies-used)
* [How the Project Works](#how-the-project-works)
* [Configuration Files Explained](#configuration-files-explained)
* [Step-by-Step Setup & Commands](#step-by-step-setup--commands)
* [Understanding Redis in This Project](#understanding-redis-in-this-project)
* [Docker Hub: Build, Push & Pull](#docker-hub-build-push--pull)
* [Learning Outcomes](#learning-outcomes)
* [Conclusion](#conclusion)
* [Developer Details](#developer-details)

---

## Project Overview

This project implements a **containerized e-commerce backend** that manages:

* Product listings
* Vendor information
* Customer orders
* Payment records

The entire application is orchestrated using **Docker Compose**, making it easy to run, manage, and scale multiple services together.

---

## Architecture

```
Client (Browser / API Client)
        │
        ▼
     NGINX (Reverse Proxy)
        │
        ▼
   FastAPI Application
        │
        ├──► Redis (Cache & Message Broker)
        │
        └──► PostgreSQL Database
                    │
                    ▼
                 pgAdmin UI
```

---

##  Project Structure

```
ecommerce-compose-project/
│
├── app/
│   ├── main.py              # FastAPI application
│   ├── worker.py            # Celery background worker
│   ├── requirements.txt     # Python dependencies
│
├── db_init/
│   └── schema.sql           # Database schema & seed data
│
├── Dockerfile               # API image build file
├── docker-compose.yml       # Multi-container orchestration
├── nginx.conf               # Reverse proxy configuration
└── README.md
└── ScreenShots              
```
![Project Structure](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/cbfbda22c23c04a15c18df08c5de2e42bf15a5f6/ScreenShots/Project%20Structure.png)

---

## Technologies Used

* **FastAPI** – Python backend API
* **PostgreSQL** – Relational database
* **Redis** – Caching & background task broker
* **Celery** – Asynchronous task worker
* **Nginx** – Reverse proxy
* **Docker & Docker Compose** – Containerization & orchestration

---

## How the Project Works

1. User sends a request from browser or API client
2. Request hits **Nginx**, which acts as a reverse proxy
3. Nginx forwards the request to the **FastAPI application**
4. FastAPI:
   * First checks **Redis cache** for data
   * If not found, fetches from **PostgreSQL**
5. Data fetched from PostgreSQL is cached in Redis
6. Background tasks (if any) are handled by **Celery worker**
7. PostgreSQL stores all transactional data

---

## Configuration Files Explained

### requirements.txt

```txt
fastapi
uvicorn[standard]
psycopg2-binary
redis
celery
```

---

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### nginx.conf

```nginx
events {}

http {
    server {
        listen 80;

        location /api/ {
            proxy_pass http://ecommerce_api:8000/;
        }
    }
}
```

---

### schema.sql

```sql
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price NUMERIC,
    vendor_id INT REFERENCES vendors(id)
);
```

---

## Step-by-Step Setup & Commands

### 1.Build and start all services

```bash
docker compose up --build
```

![Build1](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/cbfbda22c23c04a15c18df08c5de2e42bf15a5f6/ScreenShots/Build%201.png)

![Build2](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Build%202.png)

![Build3](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Build%203.png)

![Build4](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Build%204.png)

![Build5](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Build%205.png)

![Build6](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Build%206.png)


---

### 2.Verify running containers

```bash
docker ps
```

![Docker ps](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Docker%20PS.png)

---

### 3.Access Services

* FastAPI root: [http://localhost:8000](http://localhost:8000)
* Products API: [http://localhost:8000/products](http://localhost:8000/products)

![LocalHost8000](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/localhost%208000.png)

![LocalHost8000/Product](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/local%20host8000prod.png)

---

### 4.Access pgAdmin UI

* URL: [http://localhost:5050](http://localhost:5050)

![LocalHost5050 Login](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/localhost5050login.png)

![LocalHost5050 DashBoard](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/localhost5050Dashboard.png)

---

### 5.Redis Container Verification

Enter Redis container:

```bash
docker exec -it redis_cache redis-cli
```

Test Redis:

```bash
ping
```

Expected output:

```
PONG
```

![RedisCache](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/rediscache.png)

---

## Understanding Redis in This Project

Redis is used as a **cache and message broker**:

* Stores frequently accessed product data
* Reduces database load
* Improves API response time

Flow:

* API checks Redis first
* If data exists → returns cached data
* If not → fetches from PostgreSQL and stores in Redis

This is why repeated `/products` API calls become faster.

---

## Docker Hub: Build, Push & Pull

### Build Images

```bash
docker compose build
```

### Tag Images

```bash
docker tag ecommerce-compose-project-app:latest <dockerhub-username>/ecommerce-api:latest
docker tag ecommerce-compose-project-worker:latest <dockerhub-username>/ecommerce-worker:latest
```

### Push Images

```bash
docker push <dockerhub-username>/ecommerce-api:latest
docker push <dockerhub-username>/ecommerce-worker:latest
```

![DockerPush1](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Docker%20Push1.png)

![DockerPush2](https://github.com/Chaithanya013/Ecommerce-Compose-Project/blob/4bff074ee00de3715b3c4279fa5b7d8415eda3ae/ScreenShots/Docker%20Push%202.png)

### Pull Images

```bash
docker pull <dockerhub-username>/ecommerce-api:latest
docker pull <dockerhub-username>/ecommerce-worker:latest
```

---

## Learning Outcomes

- After completing this project, you will be able to:

- Understand how Docker Compose manages multi-container applications

- Design and run a real-world backend system using containers

- Use PostgreSQL safely for transactional data

- Implement Redis for caching and performance optimization

- Understand service-to-service communication using Docker networks

- Build, tag, push, and pull Docker images from Docker Hub

- Debug common Docker Compose and networking issues

---

## Conclusion

This project demonstrates how Docker Compose can be used to build and manage a scalable, real-world e-commerce backend system. By combining multiple services such as FastAPI, PostgreSQL, Redis, Celery, and Nginx, the project highlights best practices in container orchestration, networking, and service isolation. It provides a strong foundation for deploying modern backend applications in development and production environments.

---

### Developer 

**Name:** Venuthurla Siva Chaithanya  
**Email:**  chaithanyav.0203@gmail.com
**GitHub:** [@Chaithanya013](https://github.com/Chaithanya013)
**Dockerhub:** https://hub.docker.com/u/chaithanya013
