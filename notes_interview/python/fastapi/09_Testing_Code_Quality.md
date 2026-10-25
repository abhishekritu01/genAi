# Chapter 9 — Testing and Code Quality

> **Goal:** Write fast, reliable unit and integration tests for FastAPI apps (endpoints, validation, auth, DB, external APIs, async) and enforce code quality with formatting, linting, type checking and coverage.

---

## 9.1 Unit vs Integration vs End-to-End

```
            ▲  few, slow, brittle
           ╱ ╲        E2E (real deployed stack, browser/API flows)
          ╱───╲
         ╱     ╲      Integration (API + real DB in Docker, TestClient)
        ╱───────╲
       ╱         ╲    Unit (pure functions, services with fakes)
      ╱───────────╲   many, fast, cheap
```

| Type | Tests | Dependencies | Speed |
|---|---|---|---|
| Unit | One function/class (service, validator, util) | Fakes/mocks | ms |
| Integration | Endpoint → service → real DB | Test DB, overrides | 10–100 ms |
| Contract | Your API vs OpenAPI / consumer expectations | schemathesis, pact | — |
| E2E | Whole system | Deployed env | seconds |

---

## 9.2 Install and Configure pytest

```bash
$ pip install pytest pytest-cov httpx pytest-asyncio   # (anyio plugin ships with FastAPI deps)
```
**`pyproject.toml`**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q --strict-markers"
asyncio_mode = "auto"          # if using pytest-asyncio
filterwarnings = ["error::DeprecationWarning:app.*"]
```

Run:
```bash
$ pytest                         # all
$ pytest tests/test_tasks.py -v  # one file, verbose
$ pytest -k "create and not slow"# by name expression
$ pytest -x --lf                 # stop at first failure, rerun last failed
$ pytest -n auto                 # parallel (pip install pytest-xdist)
$ pytest --cov=app --cov-report=term-missing --cov-report=html
```

---

## 9.3 First Tests with `TestClient`

`TestClient` (built on httpx) calls your ASGI app **in-process** — no server needed.

**`app/main.py`** (from chapter 3, task API)
**`tests/test_tasks.py`**
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task_returns_201_and_body():
    resp = client.post("/tasks", json={"title": "Write tests", "priority": "high"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Write tests"
    assert body["done"] is False
    assert "id" in body
    assert resp.headers["Location"] == f"/tasks/{body['id']}"


def test_get_missing_task_returns_404():
    resp = client.get("/tasks/999999")
    assert resp.status_code == 404


def test_validation_error_on_empty_title():
    resp = client.post("/tasks", json={"title": ""})
    assert resp.status_code == 422
    err = resp.json()["detail"][0]
    assert err["loc"] == ["body", "title"]
    assert err["type"] == "string_too_short"


def test_invalid_query_param():
    assert client.get("/tasks?limit=1000").status_code == 422
```

Lifespan events run only when the client is used as a context manager:
```python
def test_with_lifespan():
    with TestClient(app) as c:          # startup runs here
        assert c.get("/health").status_code == 200
                                        # shutdown runs on exit
```

Parametrize to cover many cases compactly:
```python
import pytest

@pytest.mark.parametrize("payload,field", [
    ({}, "title"),
    ({"title": "x" * 201}, "title"),
    ({"title": "ok", "priority": "urgent"}, "priority"),
])
def test_invalid_payloads(payload, field):
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 422
    assert resp.json()["detail"][0]["loc"][-1] == field
```

---

## 9.4 Test Database + Dependency Overrides (fixtures)

**Strategy options**

| Option | Pros | Cons |
|---|---|---|
| SQLite in-memory | Zero setup, fast | Dialect differences (no `ILIKE`, JSONB, enums, `FOR UPDATE`) |
| **Real Postgres in Docker / testcontainers** | Same as prod ✅ | Needs Docker |
| Per-test transaction rollback | Fast isolation ✅ | Code that calls `commit()` needs the savepoint trick |

**`tests/conftest.py` — Postgres with per-test rollback (professional pattern)**
```python
import os
from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
import app.models  # noqa: F401  (register models)

TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg://app:app@localhost:5433/app_test")


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)           # or run `alembic upgrade head` to test migrations too
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db(engine) -> Generator[Session, None, None]:
    """Each test runs inside a transaction that is rolled back afterwards."""
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")  # SA 2.0: app commits → savepoints
    yield session
    session.close()
    trans.rollback()                           # wipe everything this test did
    connection.close()


@pytest.fixture
def app(db):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db    # ★ swap real DB session for test session
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(app) -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
```

Spin up the test DB:
```bash
$ docker run -d --name pg-test -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app -e POSTGRES_DB=app_test -p 5433:5432 postgres:17
```
Or automatically with **testcontainers**:
```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:17", driver="psycopg") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
```

### Factories (test data builders)
```python
# tests/factories.py
from itertools import count
from app.core.security import hash_password
from app.models.user import User

_seq = count(1)

def make_user(db, *, role="user", password="Passw0rd!", **kw) -> User:
    n = next(_seq)
    user = User(email=kw.pop("email", f"user{n}@test.com"), hashed_password=hash_password(password),
                role=role, **kw)
    db.add(user); db.flush()
    return user
```
(Bigger projects: `factory_boy` or `polyfactory`.)

---

## 9.5 Testing Authentication

```python
# tests/conftest.py (continued)
from app.core.security import create_access_token
from tests.factories import make_user

@pytest.fixture
def user(db):
    return make_user(db)

@pytest.fixture
def admin(db):
    return make_user(db, role="admin")

@pytest.fixture
def auth_headers(user):
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role)}"}

@pytest.fixture
def admin_headers(admin):
    return {"Authorization": f"Bearer {create_access_token(admin.id, admin.role)}"}
```

```python
# tests/integration/test_auth.py
def test_register_then_login(client):
    r = client.post("/api/v1/auth/register", json={"email": "new@x.com", "password": "Passw0rd!"})
    assert r.status_code == 201
    r = client.post("/api/v1/auth/token", data={"username": "new@x.com", "password": "Passw0rd!"})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"


def test_login_wrong_password(client, user):
    r = client.post("/api/v1/auth/token", data={"username": user.email, "password": "wrong"})
    assert r.status_code == 401


def test_me_requires_token(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401
    assert r.headers["www-authenticate"] == "Bearer"


def test_me_with_token(client, user, auth_headers):
    r = client.get("/api/v1/auth/me", headers=auth_headers)
    assert r.status_code == 200 and r.json()["email"] == user.email


def test_expired_token_rejected(client, user, monkeypatch):
    from datetime import timedelta
    from app.core import security
    token = security._create_token(str(user.id), "access", timedelta(seconds=-1))
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_non_admin_forbidden(client, auth_headers):
    assert client.get("/api/v1/admin/stats", headers=auth_headers).status_code == 403


def test_cannot_read_other_users_project(client, db, auth_headers):
    other = make_user(db)
    project = make_project(db, owner=other)
    assert client.get(f"/api/v1/projects/{project.id}", headers=auth_headers).status_code == 404  # IDOR test
```

**Bypass auth entirely** when a test isn't about auth:
```python
app.dependency_overrides[get_current_active_user] = lambda: user
```

---

## 9.6 Testing Database Operations

```python
def test_create_project_persists(client, db, auth_headers, user):
    r = client.post("/api/v1/projects", json={"name": "Apollo"}, headers=auth_headers)
    assert r.status_code == 201
    project = db.get(Project, r.json()["id"])
    assert project is not None and project.owner_id == user.id


def test_duplicate_email_returns_409(client, user):
    r = client.post("/api/v1/auth/register", json={"email": user.email, "password": "Passw0rd!"})
    assert r.status_code == 409


def test_repository_pagination(db, user):
    for i in range(25):
        make_project(db, owner=user, name=f"p{i}")
    items, total = ProjectRepository(db).list_for_owner(user.id, skip=20, limit=10)
    assert total == 25 and len(items) == 5
```

Test migrations in CI:
```bash
alembic upgrade head && alembic check && alembic downgrade base && alembic upgrade head
```

---

## 9.7 Unit Testing Services with Fakes

```python
# tests/unit/test_project_service.py
import pytest
from unittest.mock import MagicMock
from app.core.exceptions import ConflictError
from app.services.project_service import ProjectService, FREE_PLAN_LIMIT

def test_free_plan_limit_enforced():
    db = MagicMock()
    svc = ProjectService(db)
    svc.repo = MagicMock()
    svc.repo.count_for_owner.return_value = FREE_PLAN_LIMIT
    owner = MagicMock(id=1, plan="free")

    with pytest.raises(ConflictError):
        svc.create(owner, MagicMock())

    svc.repo.add.assert_not_called()
    db.commit.assert_not_called()
```

---

## 9.8 Mocking External APIs and Services

### Option 1 — override the client dependency (cleanest)
```python
class FakeWeatherClient:
    async def current(self, city: str) -> dict:
        return {"city": city, "temp_c": 21}

def test_weather_endpoint(app, client):
    app.dependency_overrides[get_weather_client] = lambda: FakeWeatherClient()
    r = client.get("/weather?city=Pune")
    assert r.json()["temp_c"] == 21
```

### Option 2 — mock HTTP at the transport layer (`respx` for httpx)
```python
import httpx, respx

@respx.mock
async def test_weather_client_retries_on_503():
    route = respx.get("https://api.weather.example/v1/current").mock(
        side_effect=[httpx.Response(503), httpx.Response(200, json={"temp_c": 20})]
    )
    async with httpx.AsyncClient(base_url="https://api.weather.example") as http:
        data = await WeatherClient(http, "k").current("Pune")
    assert data["temp_c"] == 20 and route.call_count == 2
```
Also: `httpx.MockTransport(handler)`, `pytest-httpx`, `responses` (for `requests`).

### Option 3 — `unittest.mock.patch`
```python
from unittest.mock import patch, AsyncMock

def test_signup_sends_email(client):
    with patch("app.api.v1.auth.send_welcome_email") as send:     # patch where it's USED
        client.post("/api/v1/auth/register", json={"email": "z@x.com", "password": "Passw0rd!"})
    send.assert_called_once_with("z@x.com")
```
🐞 Patch the name **where it's looked up** (`app.api.v1.auth.send_welcome_email`), not where it's defined.

Background tasks run synchronously in TestClient after the response, so their effects are visible right after the call.

---

## 9.9 Testing Async Endpoints and Code

`TestClient` works for async endpoints too (it runs the loop for you). Use an **async client** when the test itself must `await` (e.g., async DB fixtures):

```python
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.anyio                      # or pytest-asyncio with asyncio_mode=auto
async def test_health_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200

@pytest.fixture
def anyio_backend():
    return "asyncio"
```
⚠️ `AsyncClient(app=app)` shortcut is deprecated/removed in recent httpx → use `ASGITransport`.
Note: `ASGITransport` doesn't run lifespan; use `asgi-lifespan`'s `LifespanManager(app)` if needed.

Async DB fixture sketch:
```python
@pytest.fixture
async def async_db(async_engine):
    async with async_engine.connect() as conn:
        trans = await conn.begin()
        session = AsyncSession(bind=conn, join_transaction_mode="create_savepoint", expire_on_commit=False)
        yield session
        await session.close()
        await trans.rollback()
```

Testing WebSockets:
```python
def test_ws(client):
    with client.websocket_connect("/ws/rooms/general?token=valid") as ws:
        ws.send_json({"text": "hi"})
        assert ws.receive_json()["text"] == "hi"
```

---

## 9.10 Formatting, Linting, Type Checking

| Tool | Job | Command |
|---|---|---|
| **Ruff** | Linter + formatter (replaces flake8, isort, black, pyupgrade…) | `ruff check . --fix` · `ruff format .` |
| **mypy** / **pyright** | Static type checking | `mypy app` · `pyright` |
| **pre-commit** | Run tools on every commit | `pre-commit install` |
| bandit | Security lint | `bandit -r app` |
| pip-audit | Vulnerable dependencies | `pip-audit` |

**`pyproject.toml`**
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "N", "S", "ASYNC", "SIM", "RUF", "FAST"]
ignore = ["S101"]            # allow assert (tests)

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S", "ARG"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]
```
(`ASYNC` rules catch blocking calls in async functions; `FAST` rules are FastAPI-specific, e.g., prefer `Annotated`.)

**`.pre-commit-config.yaml`**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, sqlalchemy]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks:
      - id: gitleaks
```
(Pin `rev`s to the versions your team uses; `pre-commit autoupdate` bumps them.)

---

## 9.11 Coverage and Practical Testing Strategy

```bash
$ pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=85
```
```
Name                              Stmts   Miss Branch BrPart  Cover   Missing
app/services/project_service.py      42      2     12      1    94%   57-58
```

- Coverage shows what's **not** tested; 100% doesn't mean correct. Aim ~80–90% on services/routers, focus on critical paths.
- **What to test for each endpoint:** happy path; validation (422); not found (404); auth missing (401); forbidden / other user's resource (403/404); conflict (409); pagination edges (empty, last page); side effects (DB row, email called).
- **Property-based / fuzz:** `hypothesis` for validators; `schemathesis run http://localhost:8000/openapi.json` fuzzes your API from its schema → finds 500s.
- **Load testing:** `locust`, `k6` (not unit tests, but part of quality).

### Reliable tests checklist
- ✅ Independent (any order, parallel-safe) — transaction rollback per test.
- ✅ Deterministic — freeze time (`time-machine`/`freezegun`), seed randoms, no real network.
- ✅ Fast — unit tests dominate; share expensive fixtures with `scope="session"`.
- ✅ Same DB engine as prod for integration tests.
- ✅ Test behavior via public API (HTTP), not private internals.
- ✅ Clear names: `test_<action>_<condition>_<expected>`.
- ❌ No `time.sleep` for async waits; no shared mutable global state.

---

## ✅ Quick Revision — Chapter 9

- `TestClient(app)` (sync, in-process); `with TestClient(app)` triggers lifespan.
- Async tests: `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")`.
- `app.dependency_overrides[get_db] = ...` — the key to testing FastAPI.
- Test DB: real Postgres (Docker/testcontainers) + per-test transaction rollback with `join_transaction_mode="create_savepoint"`.
- Auth tests: 401 without token, 403 wrong role, 404 other's resource, expired token.
- Mock externals via dependency override, `respx`, or `patch` where used.
- Quality gate: `ruff check`, `ruff format --check`, `mypy`, `pytest --cov --cov-fail-under`, `pip-audit`, `alembic check`.

🎤 *"I test FastAPI mostly at the integration level with TestClient against a real Postgres, wrapping each test in a transaction that rolls back, and I override dependencies for the DB session, current user and external clients. Business rules get fast unit tests with fake repositories. CI runs ruff, mypy, tests with coverage, and migration checks."*
