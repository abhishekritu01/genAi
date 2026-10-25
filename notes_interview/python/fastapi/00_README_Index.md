# FastAPI — Zero to Senior: Complete Guide

> A step-by-step FastAPI learning guide for **building, testing, securing, deploying and architecting** production REST APIs — and for **interviews**.
> Targets **Python 3.12+**, **FastAPI 0.115+**, **Pydantic v2**, **SQLAlchemy 2.x**, **Alembic 1.13+**. Deprecated approaches are explicitly flagged with ⚠️.

---

## How the Guide Is Organized

| # | File | What you learn | Level |
|---|---|---|---|
| 01 | [01_Environment_Setup.md](01_Environment_Setup.md) | Python, venv, installing FastAPI, running the server, dependencies, troubleshooting | 🟢 Beginner |
| 02 | [02_FastAPI_Fundamentals.md](02_FastAPI_Fundamentals.md) | ASGI, Starlette, Pydantic, routes, params, bodies, responses, docs, sync vs async | 🟢 Beginner |
| 03 | [03_Building_REST_APIs.md](03_Building_REST_APIs.md) | REST design, CRUD, schemas, pagination, errors, versioning, files, CORS | 🟢→🟡 |
| 04 | [04_Database_SQLAlchemy.md](04_Database_SQLAlchemy.md) | SQL basics, SQLAlchemy 2.x ORM, sessions, relationships, loading, async, SQLModel | 🟡 Intermediate |
| 05 | [05_Alembic_Migrations.md](05_Alembic_Migrations.md) | Alembic setup, autogenerate, upgrade/downgrade, renames, safe production migrations | 🟡 Intermediate |
| 06 | [06_Project_Structure_Architecture.md](06_Project_Structure_Architecture.md) | Folder layouts, router/service/repository, `Depends`, settings, lifespan | 🟡→🔴 |
| 07 | [07_Authentication_Authorization.md](07_Authentication_Authorization.md) | Hashing, OAuth2 + JWT, refresh tokens, RBAC, API keys, reset flows | 🟡→🔴 |
| 08 | [08_Advanced_Concepts.md](08_Advanced_Concepts.md) | Middleware, background tasks, WebSockets, streaming, caching, rate limits, logging, httpx, retries, webhooks | 🔴 Advanced |
| 09 | [09_Testing_Code_Quality.md](09_Testing_Code_Quality.md) | pytest, TestClient, test DBs, overrides, mocking, async tests, ruff, mypy, coverage | 🟡→🔴 |
| 10 | [10_Security_Production.md](10_Security_Production.md) | OWASP risks, secrets, HTTPS, health checks, Docker, workers, CI/CD, migration deploys | 🔴 Advanced |
| 11 | [11_Senior_System_Design.md](11_Senior_System_Design.md) | Scaling, microservices, gateways, caching, observability, idempotency, trade-offs | 🟣 Senior |
| 12 | [12_Practical_Projects.md](12_Practical_Projects.md) | 4 progressive projects with full code | 🟢→🟣 |
| 13 | [13_Interview_Preparation.md](13_Interview_Preparation.md) | 80+ Q&A, 12 debugging scenarios, mistakes table, 10 coding/design exercises | All |
| 14 | [14_Cheat_Sheets_Quick_Revision.md](14_Cheat_Sheets_Quick_Revision.md) | One-page cheat sheets, command reference, last-day revision | All |

---

## Legend Used Throughout

| Symbol | Meaning |
|---|---|
| 🟢 | Beginner approach / must-know basics |
| 🟡 | Professional approach (what real teams do) |
| 🔴 / 🟣 | Advanced / senior-level thinking |
| ⚠️ | Deprecated, outdated, or dangerous — avoid |
| 💡 | Tip / insight |
| 🐞 | Common mistake + debugging |
| 🎤 | "Say this in the interview" — a ready answer |
| `PS>` | Windows PowerShell command |
| `$` | macOS / Linux (bash/zsh) command |

---

## Suggested Study Plan (4 weeks, ~1.5 h/day)

| Week | Days | Chapters | Hands-on |
|---|---|---|---|
| 1 | 1–2 | 01, 02 | Install, run hello-world, play with Swagger UI |
| 1 | 3–5 | 03 | **Project 1** – in-memory task API |
| 2 | 1–3 | 04, 05 | **Project 2** – Postgres + SQLAlchemy + Alembic |
| 2 | 4–5 | 06 | Refactor Project 2 into router/service/repository |
| 3 | 1–3 | 07, 09 | **Project 3** – auth + RBAC + tests |
| 3 | 4–5 | 08 | Add background tasks, logging, httpx client, rate limit |
| 4 | 1–3 | 10, 11 | **Project 4** – Docker, CI/CD, caching, observability |
| 4 | 4–5 | 13, 14 | Interview drills, cheat-sheet revision |

**Day before an interview:** read every chapter's *Quick Revision* box + chapter 14 + chapter 13 "Top 30".

---

## The Big Picture (one diagram)

```
                 ┌──────────── Client (browser / mobile / service) ─────────────┐
                 │                         HTTPS                                 │
                 ▼                                                               │
        ┌─────────────────┐   Load balancer / API gateway (TLS, auth, rate limit)
        └────────┬────────┘
                 ▼
   ┌──────────────────────────── Uvicorn (ASGI server) ────────────────────────┐
   │  Starlette: routing, middleware, requests/responses, WebSockets            │
   │  FastAPI:   dependency injection, validation (Pydantic), OpenAPI docs      │
   │     Router ──► Service (business rules) ──► Repository ──► SQLAlchemy      │
   └───────────────────────────────────────────────────────┬──────────────────┘
                                                           ▼
                                   PostgreSQL  ·  Redis (cache / rate limit)  ·  Queue (Celery / ARQ)
```

Keep this picture in mind — every chapter zooms into one box.
