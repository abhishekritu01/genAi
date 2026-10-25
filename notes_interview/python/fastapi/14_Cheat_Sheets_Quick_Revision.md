# Chapter 14 — Cheat Sheets & Quick Revision

> One place for last-minute revision: commands, code snippets, decision tables and the key takeaways of every chapter.

---

## 14.1 Command Reference

### Environment
| Task | Windows PowerShell | macOS / Linux |
|---|---|---|
| Python version | `python --version` / `py --list` | `python3 --version` |
| Create venv | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Allow scripts (once) | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` | — |
| Install FastAPI | `pip install "fastapi[standard]"` | same |
| Freeze deps | `pip freeze > requirements.txt` | same |
| Install deps | `pip install -r requirements.txt` | same |
| Set env var (session) | `$env:DATABASE_URL = "..."` | `export DATABASE_URL=...` |
| Free port 8000 | `netstat -ano \| findstr :8000` → `taskkill /PID <pid> /F` | `lsof -i :8000` → `kill <pid>` |
| Generate secret | `python -c "import secrets; print(secrets.token_hex(32))"` | same / `openssl rand -hex 32` |

### Run
```bash
fastapi dev app/main.py                         # dev + reload
fastapi run app/main.py --workers 4             # prod-style
uvicorn app.main:app --reload --port 8000       # classic
uvicorn app.main:app --host 0.0.0.0 --proxy-headers --forwarded-allow-ips="*"
gunicorn app.main:app -k uvicorn_worker.UvicornWorker -w 4 -b 0.0.0.0:8000
```

### uv
```bash
uv init · uv add fastapi[standard] · uv add --dev pytest · uv run fastapi dev · uv sync · uv lock
```

### Alembic
```bash
alembic init alembic                         alembic current
alembic revision --autogenerate -m "msg"     alembic history --verbose
alembic revision -m "data fix"               alembic heads
alembic upgrade head | +1 | <rev>            alembic merge heads -m "merge"
alembic downgrade -1 | <rev> | base          alembic stamp head
alembic upgrade head --sql > out.sql         alembic check
```

### Testing & quality
```bash
pytest -q · pytest -k name -x --lf · pytest -n auto
pytest --cov=app --cov-report=term-missing --cov-fail-under=85
ruff check . --fix · ruff format . · mypy app · pip-audit · bandit -r app
pre-commit install · pre-commit run --all-files
```

### Docker
```bash
docker build -t api:dev .                docker compose up --build -d
docker run -p 8000:8000 --env-file .env api:dev
docker compose logs -f api               docker compose run --rm migrate
docker compose exec db psql -U app       docker compose down -v
```

### curl / PowerShell requests
```bash
curl localhost:8000/items
curl -X POST localhost:8000/items -H "Content-Type: application/json" -d '{"name":"x"}'
curl -X POST localhost:8000/auth/token -d "username=a@b.com&password=secret"
curl localhost:8000/me -H "Authorization: Bearer $TOKEN"
curl -F "file=@photo.png" localhost:8000/upload
```
```powershell
Invoke-RestMethod localhost:8000/items
Invoke-RestMethod -Method Post localhost:8000/items -ContentType "application/json" -Body '{"name":"x"}'
Invoke-RestMethod localhost:8000/me -Headers @{ Authorization = "Bearer $token" }
curl.exe -F "file=@photo.png" localhost:8000/upload
```

---

## 14.2 FastAPI Syntax Cheat Sheet

```python
from typing import Annotated
from fastapi import (FastAPI, APIRouter, Depends, HTTPException, status, Path, Query, Body,
                     Header, Cookie, Form, File, UploadFile, Request, Response, BackgroundTasks)

app = FastAPI(title="API", lifespan=lifespan)
router = APIRouter(prefix="/items", tags=["items"], dependencies=[Depends(auth)])

@router.get("/{item_id}", response_model=ItemOut, status_code=200, summary="Get item")
def get_item(
    item_id: Annotated[int, Path(ge=1)],                      # path
    q: Annotated[str | None, Query(max_length=50)] = None,     # optional query
    tags: Annotated[list[str], Query()] = [],                  # ?tags=a&tags=b
    x_token: Annotated[str | None, Header()] = None,           # X-Token header
    session: Annotated[str | None, Cookie()] = None,           # cookie
    db: DbSession = ...,                                       # (use Annotated alias, no default)
): ...

@router.post("", status_code=status.HTTP_201_CREATED)
def create(item: ItemCreate, tasks: BackgroundTasks) -> ItemOut: ...   # body + return-type schema

@router.post("/upload")
async def upload(file: UploadFile, note: Annotated[str, Form()]): ...

raise HTTPException(status_code=404, detail="Not found", headers={"X-Error": "1"})
app.include_router(router, prefix="/api/v1")
app.dependency_overrides[get_db] = override
```

### Pydantic v2 essentials
```python
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator, model_validator, computed_field

class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    tags: list[str] = []

class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

m.model_dump(exclude_unset=True)   m.model_dump_json()   Model.model_validate(obj)
m.model_copy(update={...})         Model.model_json_schema()
```

### SQLAlchemy 2.x essentials
```python
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    bio: Mapped[str | None]
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

engine = create_engine(URL, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

db.get(User, 1)
db.scalars(select(User).where(User.email == e)).first()
db.scalar(select(func.count(User.id)))
db.execute(update(User).where(...).values(active=False))
select(Post).options(joinedload(Post.author), selectinload(Post.tags))
db.add(x); db.commit(); db.refresh(x); db.rollback()
```

### Auth essentials
```python
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")
def current_user(token: Annotated[str, Depends(oauth2)], db: DbSession) -> User: ...
CurrentUser = Annotated[User, Depends(current_user)]
jwt.encode(payload, key, algorithm="HS256")
jwt.decode(token, key, algorithms=["HS256"], options={"require": ["exp", "sub"]})
PasswordHash.recommended().hash(pw) / .verify(pw, hashed)
```

### Lifespan
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=5)
    yield
    await app.state.http.aclose()
```

---

## 14.3 Decision Tables

**`def` or `async def`?**
| Inside the function | Use |
|---|---|
| `await` on async libraries only | `async def` |
| Any blocking library (requests, sync DB, file I/O, boto3) | `def` |
| Heavy CPU | worker / process pool |

**Status codes**
| Situation | Code |
|---|---|
| Read OK / update OK | 200 |
| Created | 201 + Location |
| Accepted async job | 202 |
| Deleted | 204 |
| Bad input (business rule) | 400 |
| Not logged in | 401 |
| Not allowed | 403 |
| Not found / hidden | 404 |
| Duplicate / version conflict | 409 |
| Schema validation | 422 |
| Rate-limited | 429 |
| Upstream failure / timeout | 502 / 504 |
| Overloaded / not ready | 503 |

**Loading strategy**
| Relationship | Strategy |
|---|---|
| many-to-one / one-to-one | `joinedload` |
| one-to-many / many-to-many | `selectinload` |
| guard against accidents | `raiseload("*")` |

**Background work**
| Need | Tool |
|---|---|
| Tiny, OK to lose | `BackgroundTasks` |
| Must happen / retries / heavy / scheduled | Celery, ARQ, Dramatiq, RQ, cloud queue |
| Long workflows with compensation | Temporal / saga orchestration |

**Pagination**
| Data size / need | Type |
|---|---|
| Small, "page N" UI | offset |
| Large, infinite scroll, feeds | cursor/keyset |

**Real-time**
| Need | Use |
|---|---|
| Two-way, low latency | WebSocket |
| Server → client stream | SSE |
| Rare updates, simple | Polling |

---

## 14.4 ⚠️ Deprecated → Modern Map

| Outdated | Modern |
|---|---|
| `@app.on_event("startup")` | `lifespan` context manager |
| `q: str = Query(None)` | `q: Annotated[str \| None, Query()] = None` |
| Pydantic v1 `.dict()`, `orm_mode`, `@validator` | `.model_dump()`, `from_attributes`, `@field_validator` |
| `from pydantic import BaseSettings` | `from pydantic_settings import BaseSettings` |
| `declarative_base()` + `Column(Integer)` | `class Base(DeclarativeBase)` + `Mapped[...]`/`mapped_column` |
| `session.query(User).filter(...)` | `session.scalars(select(User).where(...))` |
| `passlib` | `pwdlib` (Argon2) |
| `python-jose` | `PyJWT` |
| `uvicorn.workers.UvicornWorker` | `uvicorn_worker.UvicornWorker` (separate package) or `uvicorn --workers` |
| `httpx.AsyncClient(app=app)` | `AsyncClient(transport=ASGITransport(app=app), base_url=...)` |
| `requests` in async code | `httpx.AsyncClient` |
| `Base.metadata.create_all()` in prod | Alembic migrations |
| flake8 + isort + black | Ruff |

---

## 14.5 Chapter Takeaways (one line each)

| Ch | Takeaway |
|---|---|
| 1 | One project = one venv = one pinned dependency file; run with `fastapi dev`. |
| 2 | Type hints are the contract: they drive validation, serialization and docs; never block in `async def`. |
| 3 | Predictable REST: nouns, correct verbs/status codes, separate in/out schemas, pagination, one error format, versioning. |
| 4 | Engine per app, session per request; `select()` style; eager-load to kill N+1; constraints + transactions for integrity. |
| 5 | Alembic: autogenerate, review, upgrade; expand/contract and concurrent indexes for zero downtime. |
| 6 | Thin routers → services → repositories; everything injected via `Depends`; typed settings; lifespan. |
| 7 | Argon2 hashes, short JWT access + rotating refresh, RBAC + ownership checks (no IDOR). |
| 8 | Durable queues for important work, shared clients, timeouts/retries/breakers, caching, rate limits, structured logs, idempotency. |
| 9 | TestClient + dependency_overrides + real test DB with rollback; mock at boundaries; lint/type/coverage gates. |
| 10 | OWASP API Top 10, secrets hygiene, health probes, graceful shutdown, Docker non-root, CI/CD with migration jobs. |
| 11 | Modular monolith first; stateless horizontal scale; cache, pool, observe (RED + traces + SLOs); make trade-offs explicit. |
| 12 | Build the four projects — they're your portfolio and interview stories. |

---

## 14.6 Production Readiness Checklist

- [ ] Settings from env; required secrets have no defaults; `.env` git-ignored
- [ ] All endpoints have input + output schemas; `extra="forbid"` on writes
- [ ] AuthN on non-public routes; ownership checks; admin routes guarded
- [ ] Pagination max limits; body/file size limits; rate limits on auth
- [ ] Consistent error format; generic 500 handler; no stack traces to clients
- [ ] Alembic migrations reviewed; naming convention; expand/contract for breaking changes
- [ ] DB pool sized vs workers × replicas; PgBouncer if needed; `statement_timeout`
- [ ] Shared HTTP/Redis clients created in lifespan; timeouts on every external call
- [ ] Structured JSON logs with request IDs; secrets redacted
- [ ] `/health/live`, `/health/ready`, `/metrics`; tracing enabled
- [ ] CORS explicit origins; TrustedHost; security headers; HTTPS at the edge; proxy headers trusted only from proxy
- [ ] Docker: slim, multi-stage, non-root, exec-form CMD, healthcheck
- [ ] CI: ruff, mypy, pytest + coverage, `alembic check`, pip-audit, image by SHA
- [ ] Deploy: migration job → rolling/canary → smoke test → monitor/rollback
- [ ] Backups + tested restore; runbooks; alerts on SLO burn

---

## 14.7 30-Second Elevator Answers

- **FastAPI:** "ASGI framework on Starlette + Pydantic; type hints give validation, serialization and OpenAPI docs for free."
- **Depends:** "Per-request dependency graph, cached per request, overridable in tests."
- **async:** "Only await non-blocking I/O in `async def`; blocking code goes in `def` (threadpool)."
- **Session:** "Engine per app, session per request via a yield dependency, always closed."
- **N+1:** "Eager-load: joinedload for to-one, selectinload for collections."
- **Alembic:** "Versioned migrations; review autogenerate; expand/contract in prod."
- **JWT:** "Signed claims; verify alg, exp, type; short access + revocable rotating refresh."
- **IDOR:** "Scope every object query by owner/tenant; 404 for others."
- **Testing:** "TestClient + dependency_overrides + transactional test DB."
- **Scaling:** "Stateless pods behind LB, pooler, cache, queues, replicas; measure with RED metrics and traces."
- **Idempotency:** "Idempotency-Key with stored response + unique constraint."
