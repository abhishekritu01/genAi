# 🚀 n8n Setup with Docker Compose (DevOps Ready)

## 📦 Overview

This guide helps you run **n8n** using Docker Compose with:

* Persistent storage
* Auto-restart
* Timezone config
* Easy logging

---

## 🧱 Prerequisites

* Docker installed
* Docker Compose installed

---

## 📁 Project Structure

```
n8n/
├── docker-compose.yml
└── .env (optional)
```

---

## ⚙️ Docker Compose Setup

Create a `docker-compose.yml` file:

```yaml
version: "3.8"

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    ports:
      - "5678:5678"
    environment:
      GENERIC_TIMEZONE: Asia/Kolkata
      TZ: Asia/Kolkata
      N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS: "true"
      N8N_RUNNERS_ENABLED: "true"
    volumes:
      - n8n_data:/home/node/.n8n
    restart: always

volumes:
  n8n_data:
```

---

## 🚀 Start n8n

```bash
docker compose up -d
```

Access:

```
http://localhost:5678
```

---

## 🛑 Stop n8n

```bash
docker compose down
```

---

## 📡 Logs

### View logs

```bash
docker compose logs
```

### Live logs

```bash
docker compose logs -f n8n
```

### Last 50 lines

```bash
docker compose logs --tail=50
```

---

## 💾 Data Persistence

* Data is stored in Docker volume: `n8n_data`
* Safe across container restarts

---

## 🔐 Basic Security (Recommended)

Add authentication:

```yaml
environment:
  - N8N_BASIC_AUTH_ACTIVE=true
  - N8N_BASIC_AUTH_USER=admin
  - N8N_BASIC_AUTH_PASSWORD=strongpassword
```

---

## 🏗️ Production Setup (Recommended Upgrade)

### 1. Use PostgreSQL instead of SQLite

Add DB service:

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

  n8n:
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: n8n
    depends_on:
      - postgres

volumes:
  postgres_data:
```

---

### 2. Add Reverse Proxy (Nginx + SSL)

Use:

* Nginx
* Or Traefik (recommended for auto SSL)

---

### 3. Environment Variables (.env)

Create `.env` file:

```
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=strongpassword
```

Then use:

```yaml
env_file:
  - .env
```

---

## ☁️ Deployment Ideas

* AWS EC2 (simple setup)
* AWS ECS (scalable)
* Docker Swarm / Kubernetes
* VPS (DigitalOcean, Linode)

---

## 📈 Monitoring & Logs

* Use:

  * Docker logs
  * Grafana + Loki
  * Prometheus

---

## ⚡ Useful Commands

### Restart service

```bash
docker compose restart
```

### Rebuild

```bash
docker compose up -d --build
```

### Remove volumes (⚠️ deletes data)

```bash
docker compose down -v
```

---

## 🧠 Pro Tips

* Always use `.env` for secrets
* Backup Docker volumes regularly
* Use HTTPS in production
* Enable queue mode (Redis) for scaling

---

## 🔥 Next Steps

* Add Redis (queue mode)
* Connect AI agents
* Automate workflows (n8n + APIs)
* Deploy with domain + SSL

---

## ✅ Done!

Your n8n setup is now:

* Persistent
* Scalable-ready
* DevOps-friendly
