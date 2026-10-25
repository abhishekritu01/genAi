# Chapter 10 — Security and Production Readiness

> **Goal:** Harden the API against common attacks, keep secrets and sensitive data safe, add health checks and graceful shutdown, tune performance, and ship with Docker, the right worker setup, cloud platforms and CI/CD, including how to deploy database migrations.

---

## 10.1 OWASP API Security Top 10 (2023) → FastAPI Defenses

| # | Risk | What it means | FastAPI defense |
|---|---|---|---|
| API1 | Broken Object Level Authorization (BOLA/IDOR) | Access other users' objects by changing IDs | Ownership checks in deps/queries (`WHERE owner_id = :uid`) |
| API2 | Broken Authentication | Weak login/tokens | Argon2, short JWTs, rotation, rate-limit login, MFA |
| API3 | Broken Object Property Level Authorization | Mass assignment / excessive data exposure | Separate `Create/Update/Out` schemas, `response_model`, `extra="forbid"` |
| API4 | Unrestricted Resource Consumption | No limits → DoS, cost | Pagination caps (`le=100`), body/file size limits, rate limits, timeouts |
| API5 | Broken Function Level Authorization | Users calling admin endpoints | Role/permission dependencies on routers |
| API6 | Unrestricted Access to Sensitive Business Flows | Bots abusing signup/checkout | Rate limits, CAPTCHA, anomaly detection |
| API7 | Server-Side Request Forgery (SSRF) | Server fetches attacker URL (e.g., cloud metadata) | Allow-list hosts, block private IP ranges, no redirects |
| API8 | Security Misconfiguration | Debug on, open CORS, default creds, verbose errors | Prod settings, strict CORS, generic 500s, security headers |
| API9 | Improper Inventory Management | Forgotten old versions/endpoints | Version lifecycle, disable docs in prod, API catalog |
| API10 | Unsafe Consumption of APIs | Trusting third-party responses | Validate upstream data with Pydantic, timeouts, TLS |

---

## 10.2 Input Validation & Common Attacks

- **Validate everything with Pydantic**: lengths, ranges, patterns, enums. Reject unknown fields on sensitive inputs:
  ```python
  class UserUpdate(BaseModel):
      model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
      full_name: str | None = Field(None, max_length=120)
  ```
- **Limit sizes**: request body (proxy `client_max_body_size`, or middleware checking `Content-Length`), list lengths (`Field(max_length=100)` on lists), page size.
- **XSS**: APIs return JSON (browsers don't execute it), but if you render user content as HTML, escape it (Jinja2 autoescape) and set `Content-Security-Policy`.
- **Path traversal**: never join user input into file paths without `resolve()` + parent check (chapter 3).
- **SSRF**: if users supply URLs (webhooks, image fetch), resolve DNS and block `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`, IPv6 local; disable redirects.
- **Deserialization**: never `pickle.loads` / `yaml.load` (use `yaml.safe_load`) on untrusted data.
- **ReDoS**: avoid catastrophic regex on user input (Pydantic v2's Rust regex engine is linear-time for `pattern`, but your own `re` usage isn't).
- **Command injection**: never `subprocess` with `shell=True` + user input.

---

## 10.3 SQL Injection Prevention

```python
# ❌ VULNERABLE — string formatting
db.execute(text(f"SELECT * FROM users WHERE email = '{email}'"))
# email = "' OR '1'='1"  → returns every user

# ✅ ORM / Core (always parameterized)
db.scalars(select(User).where(User.email == email))

# ✅ Raw SQL with bound parameters
db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})

# ⚠️ Identifiers (column/table names) CAN'T be parameters → whitelist them
SORT_COLUMNS = {"created_at": Project.created_at, "name": Project.name}
col = SORT_COLUMNS.get(sort_by) or abort(400)
stmt = select(Project).order_by(col.desc() if desc else col)
```
Defense in depth: app DB user with **least privilege** (no `DROP`, no superuser), separate migration user.

---

## 10.4 Secure CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,          # exact origins from config, per environment
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "X-Request-ID"],
)
```
- ❌ `["*"]` + credentials; ❌ reflecting any `Origin`; ❌ overly broad regex like `.*example.com` (matches `evil-example.com`) → use `r"https://([a-z0-9-]+\.)?example\.com"`.
- Remember: CORS doesn't protect the API from curl/bots — auth does.

---

## 10.5 Rate Limiting and Abuse Prevention
- Layered: **edge** (CDN/WAF/API gateway) + **app** (Redis per user/IP/API key) + **business** (e.g., 3 password resets/hour).
- Different limits per endpoint class: login (strict), search (medium), reads (generous).
- Return `429` + `Retry-After`; expose `RateLimit-*` headers for clients.
- Cap expensive operations: max page size, query complexity, export size, file size, concurrent jobs per user.
- Bot defenses for sensitive flows: CAPTCHA, email verification, device fingerprinting.

---

## 10.6 Secrets and Environment Variables

- 12-factor: config via **environment**; code identical across environments.
- Never hardcode secrets; never commit `.env`; commit `.env.example`.
- Prod: secret manager → injected at runtime (K8s Secret / ECS task secrets / Cloud Run secrets).
- `SecretStr` in settings; required secrets have **no default** → app refuses to start without them.
- Rotate periodically and on staff departure/leak; support **two active keys** during rotation (JWT `kid`).
- Separate secrets per environment; least privilege for each credential.
- Don't bake secrets into Docker images (`ARG`/`ENV` end up in image layers) — use runtime env or BuildKit secrets.

---

## 10.7 HTTPS, Trusted Hosts, Secure Cookies, Security Headers

- **TLS terminates** at the load balancer / reverse proxy (Nginx, Traefik, ALB, Cloudflare). App speaks HTTP inside the private network.
- Tell Uvicorn to trust proxy headers so `request.url.scheme` is `https` and client IP is correct:
  ```bash
  uvicorn app.main:app --proxy-headers --forwarded-allow-ips="10.0.0.0/8"
  ```
- `TrustedHostMiddleware(allowed_hosts=["api.example.com", "*.example.com"])` — blocks Host-header attacks.
- `HTTPSRedirectMiddleware` only if the app itself sees plain HTTP from clients (usually the proxy handles redirects).
- **Cookies:** `httponly=True, secure=True, samesite="lax"|"strict"`, narrow `path`/`domain`, `__Host-` prefix for session cookies.
- **Security headers middleware:**
  ```python
  @app.middleware("http")
  async def security_headers(request, call_next):
      resp = await call_next(request)
      resp.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
      resp.headers.setdefault("X-Content-Type-Options", "nosniff")
      resp.headers.setdefault("X-Frame-Options", "DENY")
      resp.headers.setdefault("Referrer-Policy", "no-referrer")
      resp.headers.setdefault("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
      return resp
  ```
  (Swagger UI needs a looser CSP — apply strict CSP only to API routes or disable docs in prod.)

---

## 10.8 Preventing Sensitive Data Leaks (responses & logs)

| Leak | Fix |
|---|---|
| ORM object with `hashed_password` returned | Always `response_model` / return type with an `Out` schema |
| Stack traces in 500 responses | Generic handler; `debug=False` in prod |
| Different errors reveal existence ("user not found" vs "wrong password") | Uniform messages |
| Tokens/passwords in logs | Redact processor; never log request bodies of auth routes; filter `Authorization`, `Cookie`, `Set-Cookie` |
| PII in URLs (`?email=`) | Use body/POST; URLs land in access logs & proxies |
| Verbose validation echoing secrets (`input` field in 422) | Custom 422 handler that drops `input` for sensitive routes |
| Swagger exposing internal endpoints | `include_in_schema=False`, docs disabled/protected in prod |
| Error tracking (Sentry) capturing PII | `send_default_pii=False`, scrubbing rules |

Redaction processor (structlog):
```python
SENSITIVE = {"password", "token", "access_token", "refresh_token", "authorization", "secret", "api_key"}
def redact(_, __, event_dict):
    for k in list(event_dict):
        if k.lower() in SENSITIVE:
            event_dict[k] = "***"
    return event_dict
```

---

## 10.9 Database Transaction Safety

- One transaction per business operation; commit once at the end of the service method.
- Always `rollback()` on exceptions (or use `with session.begin()`), always `close()` sessions.
- Keep transactions **short**: no external HTTP calls, no sleeping, no user waits inside.
- Use DB constraints as the final guard (UNIQUE, FK, CHECK) — application checks race; constraints don't.
- Choose isolation consciously (Postgres default READ COMMITTED); use `SELECT … FOR UPDATE`, optimistic versioning, or SERIALIZABLE + retry for critical invariants.
- Set `statement_timeout` / `idle_in_transaction_session_timeout` on the DB role.
- Side effects after commit (send email *after* commit succeeded, or via outbox).

---

## 10.10 Health Check and Readiness Endpoints

| Probe | Question | Should check | Failure action |
|---|---|---|---|
| **Liveness** `/health/live` | Is the process alive (not deadlocked)? | Nothing external — just return 200 | Restart container |
| **Readiness** `/health/ready` | Can it serve traffic now? | DB, Redis, critical deps (with short timeout) | Remove from load balancer (no restart) |
| **Startup** | Has it finished booting? | Lifespan done / model loaded | Delay other probes |

```python
from sqlalchemy import text

router = APIRouter(prefix="/health", tags=["ops"])

@router.get("/live")
def live():
    return {"status": "alive"}

@router.get("/ready")
async def ready(request: Request, response: Response):
    checks = {}
    try:
        async with async_engine.connect() as conn:
            await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout=1)
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "fail"
    try:
        await asyncio.wait_for(request.app.state.redis.ping(), timeout=0.5)
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "fail"
    healthy = all(v == "ok" for v in checks.values())
    response.status_code = 200 if healthy else 503
    return {"status": "ready" if healthy else "degraded", "checks": checks}
```
⚠️ Don't make **liveness** depend on the DB — a DB outage would restart every pod in a loop and make recovery worse. Exclude health endpoints from auth, rate limits and noisy logs.

---

## 10.11 Graceful Shutdown and Error Handling

On deploy/scale-down, the orchestrator sends **SIGTERM**:
1. Load balancer stops routing new requests (readiness fails / endpoint removed).
2. Uvicorn stops accepting connections, finishes in-flight requests (`--timeout-graceful-shutdown 30`).
3. Lifespan shutdown closes pools/clients.
4. After the grace period (K8s `terminationGracePeriodSeconds`, default 30s), SIGKILL.

Tips:
- Use **exec form** in Docker (`CMD ["uvicorn", ...]`) so the server is PID 1 and receives SIGTERM.
- K8s: `preStop: sleep 5` to let endpoints de-register before shutdown begins.
- Long jobs belong in workers that checkpoint, not in requests.
- Global exception handler: log with request ID → generic 500 JSON; report to Sentry.

---

## 10.12 Performance Optimization and Profiling

**Measure first:**
| Tool | Use |
|---|---|
| `py-spy top --pid <pid>` / `py-spy record -o flame.svg` | Sampling profiler on live process (no code change) |
| `pyinstrument` middleware | Per-request call tree in dev |
| SQLAlchemy `echo=True`, `pg_stat_statements` | Slow/repeated queries |
| `locust`, `k6`, `wrk`, `oha` | Load tests (p50/p95/p99, RPS) |
| APM (OpenTelemetry → Grafana/Datadog/New Relic) | Prod latency breakdown |

**Common wins (biggest first):**
1. Fix N+1 queries; add indexes; paginate.
2. Don't block the event loop; right `def`/`async def` choice.
3. Reuse connections (DB pool, shared `httpx` client, Redis).
4. Cache hot reads (Redis, HTTP caching, CDN).
5. Move slow work to background workers.
6. Reduce payload size (field selection, GZip, pagination).
7. Return typed Pydantic models (fast Rust serialization); avoid `jsonable_encoder` on huge payloads.
8. Run multiple worker processes per container/host (CPU cores).
9. `uvloop` + `httptools` (installed with `uvicorn[standard]`).
10. Scale horizontally.

---

## 10.13 Production Deployment with Docker

### Dockerfile (multi-stage, non-root, small)
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv && /opt/venv/bin/pip install -r requirements.txt

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/opt/venv/bin:$PATH"
RUN useradd --create-home --uid 10001 appuser
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser alembic ./alembic
COPY --chown=appuser:appuser alembic.ini .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*", "--timeout-graceful-shutdown", "30"]
```
(`--forwarded-allow-ips=*` is acceptable only when the container is reachable solely through your proxy; otherwise list the proxy IPs.)

**`.dockerignore`**
```
.venv
.git
__pycache__
*.pyc
.env
tests
htmlcov
.pytest_cache
```

### docker-compose for local full stack
```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    environment:
      DATABASE_URL: postgresql+psycopg://app:app@db:5432/app
      REDIS_URL: redis://redis:6379/0
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_started }
  migrate:
    build: .
    command: ["alembic", "upgrade", "head"]
    environment:
      DATABASE_URL: postgresql+psycopg://app:app@db:5432/app
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:17
    environment: { POSTGRES_USER: app, POSTGRES_PASSWORD: app, POSTGRES_DB: app }
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      retries: 10
  redis:
    image: redis:7-alpine
volumes:
  pgdata:
```
```bash
$ docker compose up --build -d
$ docker compose logs -f api
$ docker compose run --rm migrate
$ docker compose down            # add -v to delete volumes
```

### Workers: Uvicorn vs Gunicorn + Uvicorn workers

| Setup | When |
|---|---|
| **1 Uvicorn process per container**, scale with replicas (K8s/ECS/Cloud Run) | ✅ Containers/orchestrators — let the platform manage processes |
| `uvicorn app.main:app --workers 4` or `fastapi run --workers 4` | VM / single host; Uvicorn now has its own process manager |
| `gunicorn app.main:app -k uvicorn_worker.UvicornWorker -w 4` | Classic VM deployments wanting Gunicorn's mature process management (`max_requests`, graceful reloads) |

⚠️ `uvicorn.workers.UvicornWorker` is deprecated → use the separate **`uvicorn-worker`** package (`uvicorn_worker.UvicornWorker`).
Rule of thumb for workers per host: start with number of CPU cores (I/O-heavy async apps rarely need `2×cores+1`), then load test. Remember DB pool math × workers.

### Cloud platforms (pick by ops budget)

| Platform | Type | Notes |
|---|---|---|
| Render, Railway, Fly.io | PaaS | Easiest, Dockerfile or buildpack |
| Google Cloud Run / AWS App Runner / Azure Container Apps | Serverless containers | Autoscale to zero, pay per use; watch DB connections (use pooler) |
| AWS ECS Fargate | Managed containers | ALB + RDS + Secrets Manager |
| Kubernetes (EKS/GKE/AKS) | Orchestrator | Max control; probes, HPA, ingress |
| AWS Lambda + Mangum adapter | FaaS | Spiky low traffic; cold starts; no WebSockets |
| VM + Nginx + systemd | DIY | Full control; more ops |

---

## 10.14 CI/CD Basics

**`.github/workflows/ci.yml`**
```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:17
        env: { POSTGRES_USER: app, POSTGRES_PASSWORD: app, POSTGRES_DB: app_test }
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U app" --health-interval 5s --health-retries 10
    env:
      DATABASE_URL: postgresql+psycopg://app:app@localhost:5432/app_test
      TEST_DATABASE_URL: postgresql+psycopg://app:app@localhost:5432/app_test
      JWT_SECRET_KEY: ci-only-secret
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.13", cache: pip }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check . && ruff format --check .
      - run: mypy app
      - run: alembic upgrade head && alembic check
      - run: pytest --cov=app --cov-fail-under=85
      - run: pip-audit

  build-and-deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build & push image
        run: |
          docker build -t $REGISTRY/api:${{ github.sha }} .
          docker push $REGISTRY/api:${{ github.sha }}
      - name: Run migrations (one-off job)
        run: ./deploy/run-migration-job.sh ${{ github.sha }}
      - name: Rolling deploy
        run: ./deploy/deploy.sh ${{ github.sha }}
```

Pipeline stages: **lint → type-check → test → security scan → build image (tag = git SHA) → push → migrate → deploy staging → smoke tests → (approval) → deploy prod → monitor/auto-rollback**.

### Migration deployment strategies

| Strategy | How | Notes |
|---|---|---|
| **Pre-deploy migration job** ✅ | CI/CD runs `alembic upgrade head` once (K8s Job, ECS one-off task, Helm pre-upgrade hook) then rolls out app | Migrations must be backward compatible with the *old* code still running |
| Run on container start | `alembic upgrade head && uvicorn ...` in entrypoint | ⚠️ Simple for 1 instance; races with many replicas (Postgres advisory lock can serialize, but still couples deploy & migrate) |
| Manual / DBA-applied | `alembic upgrade head --sql` reviewed and applied | Regulated environments |

Combine with **expand/contract** (chapter 5). Rollback the app freely; the schema stays compatible. Destructive "contract" migrations ship only after all old versions are gone.

Deployment strategies: **rolling** (default), **blue-green** (switch traffic between two full environments), **canary** (small % first, watch metrics), plus **feature flags** to decouple deploy from release.

---

## ✅ Quick Revision — Chapter 10

- OWASP API Top 10: BOLA #1 → ownership checks everywhere.
- Pydantic validation + `extra="forbid"` + size limits; whitelist identifiers; parameterized SQL.
- CORS explicit origins; TLS at proxy + `--proxy-headers`; `TrustedHostMiddleware`; secure cookies; security headers.
- Secrets: env + secret manager, `SecretStr`, rotate, never in images or git.
- No sensitive data in responses/logs/URLs; generic 500s.
- Liveness = no deps; readiness = checks deps with timeouts.
- Graceful shutdown: SIGTERM → drain → lifespan cleanup; exec-form CMD.
- Performance: measure (py-spy, load tests) → fix queries → async correctness → caching → workers → scale out.
- Docker multi-stage, non-root, healthcheck; 1 process/container in K8s; `uvicorn-worker` for Gunicorn (⚠️ `uvicorn.workers` deprecated).
- CI: ruff, mypy, pytest+cov, alembic check, pip-audit → image by SHA → migration job → rolling/canary deploy.
