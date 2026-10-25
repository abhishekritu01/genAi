# Chapter 6 — Project Structure and Architecture

> **Goal:** Grow from a single `main.py` to a clean, modular, testable codebase: routers → services → repositories, dependency injection, typed settings, lifespan, and clean architecture.

---

## 6.1 Small Project Layout (1–10 endpoints)

```
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI() + routes
│   ├── db.py            # engine, SessionLocal, Base, get_db
│   ├── models.py        # SQLAlchemy models
│   └── schemas.py       # Pydantic models
├── tests/
├── alembic/
├── requirements.txt
└── .env
```
Fine for prototypes and small services. Pain starts when `main.py` exceeds a few hundred lines.

---

## 6.2 Scalable Production Layout

Two common styles:

### A) Layer-based (by technical role) — good for small/medium teams
```
app/
├── main.py                    # create_app(), include routers, middleware, handlers
├── core/
│   ├── config.py              # Settings (pydantic-settings)
│   ├── security.py            # hashing, JWT
│   ├── logging.py
│   └── exceptions.py          # domain errors + handlers
├── db/
│   ├── base.py                # DeclarativeBase + naming convention
│   └── session.py             # engine, sessionmaker, get_db
├── models/                    # SQLAlchemy models
│   ├── __init__.py            # import all models (for Alembic)
│   ├── user.py
│   └── project.py
├── schemas/                   # Pydantic DTOs
│   ├── user.py
│   └── project.py
├── repositories/              # data access only
│   ├── base.py
│   ├── user_repo.py
│   └── project_repo.py
├── services/                  # business logic
│   ├── user_service.py
│   └── project_service.py
├── api/
│   ├── deps.py                # shared dependencies (db, current_user, pagination)
│   └── v1/
│       ├── __init__.py        # api_router = APIRouter(prefix="/api/v1")
│       ├── users.py
│       └── projects.py
└── workers/                   # Celery/ARQ tasks (optional)
tests/
├── conftest.py
├── unit/
└── integration/
alembic/
docker/
.env.example
pyproject.toml
```

### B) Feature/domain-based (by business module) — scales to large codebases
```
app/
├── main.py
├── core/ ...
├── users/
│   ├── router.py
│   ├── schemas.py
│   ├── models.py
│   ├── service.py
│   ├── repository.py
│   └── dependencies.py
├── projects/
│   ├── router.py ... (same files)
└── billing/ ...
```
✅ Everything about "projects" lives together → easier ownership, easier to extract into a microservice later.

| | Layer-based | Feature-based |
|---|---|---|
| Navigation for small apps | ✅ easy | more folders |
| Ownership by team/domain | ❌ spread across folders | ✅ one folder per domain |
| Extracting a microservice | harder | ✅ easier |
| Recommended for | < ~15 resources | larger / multi-team apps |

---

## 6.3 Controller → Service → Repository Pattern

```
HTTP request
   │
   ▼
┌──────────────────────┐  Router / "controller"
│ api/v1/projects.py   │  - parse & validate input (Pydantic)
│                      │  - auth dependencies
│                      │  - call service, map result → response model
└──────────┬───────────┘  ✗ no SQL, ✗ no business rules
           ▼
┌──────────────────────┐  Service
│ services/project_... │  - business rules ("max 10 projects on free plan")
│                      │  - orchestrates repositories, transactions, external APIs
│                      │  - raises domain exceptions (NotFound, Forbidden, Conflict)
└──────────┬───────────┘  ✗ no HTTP objects (Request, HTTPException)
           ▼
┌──────────────────────┐  Repository
│ repositories/...     │  - only data access (select/insert/update)
│                      │  - returns models / primitives
└──────────┬───────────┘  ✗ no business rules
           ▼
        Database
```

**Why bother?**
- **Testability:** unit-test services with a fake repository — no DB, no HTTP.
- **Reuse:** the same service is called by API, CLI, background worker.
- **Change isolation:** switch Postgres → another store by changing repositories only.

### Example implementation

**`app/repositories/project_repo.py`**
```python
from collections.abc import Sequence
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def list_for_owner(self, owner_id: int, skip: int, limit: int) -> tuple[Sequence[Project], int]:
        base = select(Project).where(Project.owner_id == owner_id)
        total = self.db.scalar(select(func.count()).select_from(base.subquery())) or 0
        items = self.db.scalars(base.order_by(Project.id.desc()).offset(skip).limit(limit)).all()
        return items, total

    def count_for_owner(self, owner_id: int) -> int:
        return self.db.scalar(select(func.count(Project.id)).where(Project.owner_id == owner_id)) or 0

    def add(self, project: Project) -> Project:
        self.db.add(project)
        self.db.flush()           # get id; commit is the service's decision
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
```

**`app/services/project_service.py`**
```python
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.project import Project
from app.models.user import User
from app.repositories.project_repo import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate

FREE_PLAN_LIMIT = 10


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db)

    def create(self, owner: User, data: ProjectCreate) -> Project:
        if owner.plan == "free" and self.repo.count_for_owner(owner.id) >= FREE_PLAN_LIMIT:
            raise ConflictError("Free plan project limit reached")
        project = self.repo.add(Project(**data.model_dump(), owner_id=owner.id))
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_owned(self, owner: User, project_id: int) -> Project:
        project = self.repo.get(project_id)
        if project is None:
            raise NotFoundError("Project not found")
        if project.owner_id != owner.id and owner.role != "admin":
            raise ForbiddenError("Not your project")
        return project

    def update(self, owner: User, project_id: int, data: ProjectUpdate) -> Project:
        project = self.get_owned(owner, project_id)
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(project, k, v)
        self.db.commit()
        self.db.refresh(project)
        return project
```

**`app/api/v1/projects.py`**
```python
from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.api.deps import CurrentUser, DbSession, Pagination
from app.schemas.common import Page
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service(db: DbSession) -> ProjectService:
    return ProjectService(db)

Service = Annotated[ProjectService, Depends(get_project_service)]


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, user: CurrentUser, svc: Service):
    return svc.create(user, data)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, user: CurrentUser, svc: Service):
    return svc.get_owned(user, project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, user: CurrentUser, svc: Service):
    return svc.update(user, project_id, data)
```
The router is thin: ~3 lines per endpoint.

💡 **Pragmatism:** for simple CRUD, a repository can feel like boilerplate. Senior engineers apply layers where they pay off (business rules, multiple data sources, testing) — not dogmatically.

---

## 6.4 Dependency Injection with `Depends()`

**Simple English:** Instead of each endpoint creating its own DB session, reading the token, checking permissions..., you declare "I *need* X" and FastAPI builds X for you — calling X's own dependencies first.

```python
from typing import Annotated
from fastapi import Depends, Query

# 1) function dependency
def pagination(page: Annotated[int, Query(ge=1)] = 1,
               size: Annotated[int, Query(ge=1, le=100)] = 20) -> dict:
    return {"skip": (page - 1) * size, "limit": size}

Pagination = Annotated[dict, Depends(pagination)]

@router.get("/items")
def items(p: Pagination):
    return p


# 2) class dependency (FastAPI calls the class → __init__ params become query params)
class SortParams:
    def __init__(self, sort_by: str = "id", desc: bool = False):
        self.sort_by, self.desc = sort_by, desc

@router.get("/things")
def things(sort: Annotated[SortParams, Depends()]):     # Depends() with no arg = use the type
    return vars(sort)


# 3) yield dependency (setup + teardown)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 4) parametrized dependency (factory / callable instance)
class RequireRole:
    def __init__(self, *roles: str):
        self.roles = roles

    def __call__(self, user: CurrentUser) -> User:
        if user.role not in self.roles:
            raise HTTPException(403, "Insufficient role")
        return user

@router.delete("/admin/users/{id}", dependencies=[Depends(RequireRole("admin"))])
def admin_delete(id: int): ...


# 5) dependencies on router / app level (run for every route, return value unused)
router = APIRouter(dependencies=[Depends(verify_api_key)])
app = FastAPI(dependencies=[Depends(log_request_id)])
```

### Dependency graph & caching
```
get_current_active_user ──► get_current_user ──► oauth2_scheme (reads header)
                                         └────► get_db
endpoint also needs get_db  ─────────────────────┘   (same instance reused!)
```
Within **one request**, a dependency is computed **once** and reused (`use_cache=True` default). `Depends(fn, use_cache=False)` to force re-run.

### `yield` dependencies & exceptions
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise                       # ★ re-raise! swallowing breaks error handling
    finally:
        db.close()
```

### Overriding dependencies (testing!)
```python
app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_current_user] = lambda: User(id=1, role="admin")
```
This is the single biggest reason to route everything through `Depends`.

---

## 6.5 Configuration with Pydantic Settings

```bash
$ pip install pydantic-settings
```

**`app/core/config.py`**
```python
from functools import lru_cache
from typing import Literal
from pydantic import Field, PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",              # read .env in dev (real env vars override it)
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Project API"
    environment: Literal["local", "dev", "staging", "prod"] = "local"
    debug: bool = False

    database_url: str = "postgresql+psycopg://app:app@localhost:5432/app"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: SecretStr                   # REQUIRED — app fails to start if missing ✅
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    cors_origins: list[str] = Field(default_factory=list)   # env: CORS_ORIGINS='["https://a.com"]'

    @computed_field
    @property
    def is_prod(self) -> bool:
        return self.environment == "prod"


@lru_cache                                       # build once, reuse (and overridable in tests)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

**`.env`** (never committed)
```
ENVIRONMENT=local
DEBUG=true
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app
JWT_SECRET_KEY=change-me-use-openssl-rand-hex-32
CORS_ORIGINS=["http://localhost:5173"]
```
**`.env.example`** (committed, no real values) — documents required variables.

Priority (highest first): init kwargs → **environment variables** → `.env` file → defaults.

Using settings in endpoints:
```python
from app.core.config import Settings, get_settings

@app.get("/info")
def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"app": settings.app_name, "env": settings.environment}
```

### Managing secrets
| Environment | Where secrets live |
|---|---|
| Local | `.env` (gitignored) |
| CI | CI secret store (GitHub Actions secrets) |
| Prod | Secret manager (AWS Secrets Manager / SSM, GCP Secret Manager, Azure Key Vault, Vault, K8s Secrets) injected as env vars or files |

- `SecretStr` hides values in `repr()`/logs: `settings.jwt_secret_key.get_secret_value()`.
- Generate secrets: `python -c "import secrets; print(secrets.token_hex(32))"` / `openssl rand -hex 32`.
- 🐞 Leaked a secret into git? **Rotate it.** Rewriting history isn't enough (forks, caches).
- Scan with `gitleaks` / GitHub secret scanning / `detect-secrets` pre-commit.

---

## 6.6 Lifespan: Startup and Shutdown

**Simple English:** Code that runs once when the app starts (open DB pool, create HTTP client, load ML model) and once when it stops (close them).

```python
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---------- startup ----------
    app.state.http = httpx.AsyncClient(timeout=10)
    app.state.model = load_ml_model()           # heavy objects loaded once
    yield                                       # app serves requests here
    # ---------- shutdown ----------
    await app.state.http.aclose()
    engine.dispose()                            # close pooled DB connections


app = FastAPI(lifespan=lifespan)
```
Access later: `request.app.state.http`.

⚠️ `@app.on_event("startup")` / `("shutdown")` are **deprecated** — use `lifespan`. (You can't mix both.)

💡 Lifespan **state dict** alternative: `yield {"http": client}` → available as `request.state.http` per request.

---

## 6.7 Modular Apps and Router Registration

**`app/api/v1/__init__.py`**
```python
from fastapi import APIRouter
from . import auth, users, projects

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(projects.router)
```

**`app/main.py` — application factory**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.lifespan import lifespan


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        docs_url=None if settings.is_prod else "/docs",
        redoc_url=None if settings.is_prod else "/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    app.include_router(api_router)

    @app.get("/health", tags=["ops"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
```
Why a factory? Tests can build apps with different settings; avoids import-time side effects.

`include_router` options: `prefix`, `tags`, `dependencies`, `responses`, `deprecated`, `include_in_schema`.

Mounting sub-apps: `app.mount("/admin", admin_app)` (separate FastAPI/ASGI app with its own docs), `app.mount("/static", StaticFiles(directory="static"))`.

---

## 6.8 Clean Architecture & Separation of Concerns

```
           ┌───────────────────────────────────────┐
           │ Frameworks & drivers: FastAPI, SQLAlch,│
           │ Redis, HTTP clients                    │
           │   ┌───────────────────────────────┐   │
           │   │ Interface adapters: routers,  │   │
           │   │ repositories, schemas          │   │
           │   │   ┌───────────────────────┐   │   │
           │   │   │ Use cases / services   │   │   │
           │   │   │   ┌───────────────┐   │   │   │
           │   │   │   │ Domain entities│   │   │   │
           │   │   │   └───────────────┘   │   │   │
           │   │   └───────────────────────┘   │   │
           │   └───────────────────────────────┘   │
           └───────────────────────────────────────┘
        Dependency rule: arrows point INWARD only.
```

Practical rules:
1. Routers know HTTP; services don't.
2. Services depend on **abstractions** (a repository interface / `Protocol`), not concrete DB code — for testability.
3. Domain errors are plain Python exceptions; HTTP mapping happens at the edge.
4. Pydantic schemas (API contract) ≠ ORM models (storage) — map between them.
5. Configuration is injected, not read from `os.environ` deep in code.
6. Side effects (email, payments) behind interfaces → easy to fake in tests.

Repository interface via `Protocol`:
```python
from typing import Protocol

class UserRepo(Protocol):
    def get_by_email(self, email: str) -> User | None: ...
    def add(self, user: User) -> User: ...

class FakeUserRepo:                      # for unit tests — satisfies the protocol structurally
    def __init__(self): self.items = {}
    def get_by_email(self, email): return self.items.get(email)
    def add(self, user): self.items[user.email] = user; return user
```

### Unit of Work (optional, advanced)
Groups repositories under one transaction:
```python
class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.projects = ProjectRepository(self.session)
        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()
```

| Approach | When |
|---|---|
| Logic in routes | Prototypes, < 10 endpoints |
| Routes + services | Most apps — good default |
| Routes + services + repositories | Complex domains, multiple data sources, heavy unit testing |
| + Unit of Work / DDD | Large domains, many invariants |

---

## ✅ Quick Revision — Chapter 6

- Start simple; refactor to `api/ services/ repositories/ models/ schemas/ core/` as you grow. Feature-based folders for large apps.
- **Router** = HTTP; **Service** = business rules + transactions; **Repository** = queries.
- `Depends()` builds a per-request dependency graph, cached per request, overridable in tests.
- `yield` dependencies for setup/teardown; re-raise exceptions.
- `Annotated[T, Depends(fn)]` aliases (`DbSession`, `CurrentUser`) keep signatures clean.
- Settings: `pydantic-settings` + `.env` locally + secret manager in prod; `SecretStr`; required secrets fail fast.
- Lifespan context manager (⚠️ not `on_event`) for startup/shutdown resources.
- App factory `create_app()` + `include_router` per module.

🎤 *"I keep routers thin: they validate input, resolve auth through dependencies, and call a service. Services hold business rules and own the transaction; repositories only do data access. Everything is injected with `Depends`, so tests can override the DB session or the current user without monkeypatching."*
