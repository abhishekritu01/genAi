# Chapter 12 — Practical Projects (Beginner → Senior)

> Four projects that build on each other. Each lists **requirements → architecture → folder structure → steps & commands → key code → testing → design decisions**.
>
> | # | Project | New skills |
> |---|---|---|
> | 1 | Task API (in-memory) | Routing, Pydantic, CRUD, status codes, Swagger |
> | 2 | Bookstore API (Postgres + SQLAlchemy + Alembic) | ORM, relationships, sessions, migrations |
> | 3 | Project-Management API (auth + roles + tests) | JWT, RBAC, ownership, pagination/filter/sort, service layer, pytest |
> | 4 | Production-style API | Docker, lifespan, structured logging, Redis caching, rate limiting, health/metrics, CI/CD |
>
> ✅ Verified when these notes were written (Python 3.13, FastAPI 0.162, SQLAlchemy 2.1, Pydantic 2.14, PyJWT 2.15, pwdlib): the Project 1 test passes, Project 2's CRUD flow was smoke-tested against SQLite, and **Project 3's 14 tests pass** with its code exactly as shown. Project 4 adds infrastructure (Postgres, Redis, Docker) on top of Project 3; its snippets are reference code you wire in yourself.

---

# Project 1 — Beginner: Task-Management API (in-memory)

### Requirements
- CRUD for tasks: `title` (1–200 chars), `description?`, `priority` (low/medium/high), `done`.
- List with filters `done`, `priority`, and `skip`/`limit`.
- Correct status codes: 201, 200, 204, 404, 422.
- Data lives in memory (resets on restart) — the focus is FastAPI basics.

### Architecture
```
Client ─► FastAPI routes ─► dict "database" (in-process memory)
```

### Folder structure
```
task-api/
├── main.py
└── requirements.txt      # fastapi[standard]
```

### Steps
```powershell
PS> mkdir task-api; cd task-api
PS> python -m venv .venv; .\.venv\Scripts\Activate.ps1
PS> pip install "fastapi[standard]"
PS> fastapi dev main.py
```
```bash
$ mkdir task-api && cd task-api
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install "fastapi[standard]"
$ fastapi dev main.py
```

### `main.py` (complete)
```python
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Task API", version="1.0.0")


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=200, examples=["Learn FastAPI"])
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority = Priority.medium
    done: bool = False


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: Priority | None = None
    done: bool | None = None


class Task(TaskCreate):
    id: int
    created_at: datetime


tasks: dict[int, Task] = {}
next_id = 1


def get_task_or_404(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return tasks[task_id]


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate, response: Response):
    global next_id
    task = Task(id=next_id, created_at=datetime.now(timezone.utc), **payload.model_dump())
    tasks[task.id] = task
    response.headers["Location"] = f"/tasks/{task.id}"
    next_id += 1
    return task


@app.get("/tasks", response_model=list[Task], tags=["tasks"])
def list_tasks(
    done: bool | None = None,
    priority: Priority | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    result = [t for t in tasks.values()
              if (done is None or t.done == done) and (priority is None or t.priority == priority)]
    return result[skip: skip + limit]


@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: int):
    return get_task_or_404(task_id)


@app.patch("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate):
    task = get_task_or_404(task_id)
    updated = task.model_copy(update=payload.model_dump(exclude_unset=True))
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int):
    get_task_or_404(task_id)
    del tasks[task_id]
```

### Try it in Swagger (`/docs`)
1. **POST /tasks** → Try it out → body `{"title": "Buy milk", "priority": "high"}` → 201.
2. **GET /tasks?priority=high** → list.
3. **PATCH /tasks/1** `{"done": true}` → 200.
4. **DELETE /tasks/1** → 204; **GET /tasks/1** → 404.
5. **POST** `{"title": ""}` → 422 with `string_too_short`.

### Test (`test_main.py`)
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_lifecycle():
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    tid = r.json()["id"]
    assert client.patch(f"/tasks/{tid}", json={"done": True}).json()["done"] is True
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404
```
`pip install pytest && pytest -q`

### Design decisions
- Separate `TaskCreate` / `TaskUpdate` / `Task` → clients can't set `id`/`created_at`; PATCH semantics via `exclude_unset`.
- `extra="forbid"` → typos in field names produce 422 instead of being silently ignored.
- `def` (not `async def`) — nothing awaits; FastAPI runs it in the threadpool. ⚠️ The global dict isn't safe for multi-worker deployments — that's why Project 2 adds a database.

---

# Project 2 — Intermediate: Bookstore API (PostgreSQL + SQLAlchemy + Alembic)

### Requirements
- Authors and Books (one author → many books), CRUD for both.
- Unique ISBN; price > 0; list books with author info, filter by author and price range, paginate.
- Schema managed by Alembic; Postgres in Docker.

### Architecture
```
Client ─► FastAPI router ─► crud.py (SQLAlchemy 2.x) ─► Session (per request) ─► PostgreSQL
                                                          Alembic manages schema versions
```

### Folder structure
```
bookstore/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── main.py
├── alembic/ (generated)  ├── alembic.ini
├── .env  ├── .env.example
└── requirements.txt
```

### Steps & commands
```bash
# 1. Postgres
$ docker run -d --name bookstore-db -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app \
    -e POSTGRES_DB=bookstore -p 5432:5432 postgres:17
# 2. deps
$ pip install "fastapi[standard]" "sqlalchemy>=2.0" "psycopg[binary]" alembic pydantic-settings
# 3. env
$ echo 'DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/bookstore' > .env
# 4. alembic
$ alembic init alembic          # then edit env.py (below)
$ alembic revision --autogenerate -m "create authors and books"
$ alembic upgrade head
# 5. run
$ fastapi dev app/main.py
```
(PowerShell: `Set-Content .env 'DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/bookstore'`; the `docker run` command goes on one line or uses backtick ` continuation.)

### `app/config.py`
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str

settings = Settings()
```

### `app/db.py`
```python
from collections.abc import Generator
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from app.config import settings

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s", "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", "pk": "pk_%(table_name)s",
    })

engine = create_engine(settings.database_url, pool_size=5, max_overflow=10, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `app/models.py`
```python
from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (CheckConstraint("price > 0", name="price_positive"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    author: Mapped[Author] = relationship(back_populates="books")
```

### `app/schemas.py`
```python
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class AuthorOut(AuthorCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    isbn: str = Field(pattern=r"^\d{13}$")
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    author_id: int

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    isbn: str
    price: Decimal
    created_at: datetime
    author: AuthorOut                       # nested → must be eager-loaded
```

### `app/crud.py`
```python
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.models import Author, Book
from app.schemas import AuthorCreate, BookCreate, BookUpdate

class DuplicateError(Exception): ...

def create_author(db: Session, data: AuthorCreate) -> Author:
    author = Author(**data.model_dump())
    db.add(author); db.commit(); db.refresh(author)
    return author

def create_book(db: Session, data: BookCreate) -> Book:
    book = Book(**data.model_dump())
    db.add(book)
    try:
        db.commit()
    except IntegrityError:            # duplicate ISBN or bad author_id (FK)
        db.rollback()
        raise DuplicateError("ISBN already exists or author not found")
    return get_book(db, book.id)

def get_book(db: Session, book_id: int) -> Book | None:
    return db.scalar(select(Book).options(joinedload(Book.author)).where(Book.id == book_id))

def list_books(db: Session, *, author_id: int | None, min_price: Decimal | None,
               max_price: Decimal | None, skip: int, limit: int) -> tuple[list[Book], int]:
    stmt = select(Book)
    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)
    if min_price is not None:
        stmt = stmt.where(Book.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Book.price <= max_price)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.options(joinedload(Book.author))        # avoid N+1 on author
                      .order_by(Book.id).offset(skip).limit(limit)).all()
    return list(rows), total

def update_book(db: Session, book: Book, data: BookUpdate) -> Book:
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(book, k, v)
    db.commit()
    return get_book(db, book.id)

def delete_book(db: Session, book: Book) -> None:
    db.delete(book); db.commit()
```

### `app/main.py`
```python
from decimal import Decimal
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud
from app.db import get_db
from app.schemas import AuthorCreate, AuthorOut, BookCreate, BookOut, BookUpdate

app = FastAPI(title="Bookstore API")
DbSession = Annotated[Session, Depends(get_db)]

class BookPage(BaseModel):
    items: list[BookOut]
    total: int

@app.post("/authors", response_model=AuthorOut, status_code=201)
def create_author(data: AuthorCreate, db: DbSession):
    return crud.create_author(db, data)

@app.post("/books", response_model=BookOut, status_code=201)
def create_book(data: BookCreate, db: DbSession):
    try:
        return crud.create_book(db, data)
    except crud.DuplicateError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))

@app.get("/books", response_model=BookPage)
def list_books(db: DbSession, author_id: int | None = None,
               min_price: Annotated[Decimal | None, Query(ge=0)] = None,
               max_price: Annotated[Decimal | None, Query(ge=0)] = None,
               skip: Annotated[int, Query(ge=0)] = 0,
               limit: Annotated[int, Query(ge=1, le=100)] = 20):
    items, total = crud.list_books(db, author_id=author_id, min_price=min_price,
                                   max_price=max_price, skip=skip, limit=limit)
    return BookPage(items=items, total=total)

def _book_or_404(db: Session, book_id: int):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(404, "Book not found")
    return book

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: DbSession):
    return _book_or_404(db, book_id)

@app.patch("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookUpdate, db: DbSession):
    return crud.update_book(db, _book_or_404(db, book_id), data)

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: DbSession):
    crud.delete_book(db, _book_or_404(db, book_id))
```

### `alembic/env.py` (changed lines)
```python
from app.config import settings
from app.db import Base
import app.models  # noqa: F401
config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata
```

### Exercise the migration workflow
```bash
# add a column
#   models.py → Book: published_year: Mapped[int | None]
$ alembic revision --autogenerate -m "add books.published_year"
$ alembic upgrade head
$ alembic current           # shows new head
$ alembic downgrade -1      # remove it again
$ alembic history
```

### Sample requests
```bash
$ curl -X POST localhost:8000/authors -H "Content-Type: application/json" -d '{"name":"Frank Herbert"}'
{"name":"Frank Herbert","id":1}
$ curl -X POST localhost:8000/books -H "Content-Type: application/json" \
       -d '{"title":"Dune","isbn":"9780441172719","price":"9.99","author_id":1}'
{"id":1,"title":"Dune","isbn":"9780441172719","price":"9.99","created_at":"...","author":{"name":"Frank Herbert","id":1}}
$ curl "localhost:8000/books?min_price=5&max_price=20"
```

### Design decisions
- `Decimal` + `Numeric(10,2)` for money (never float).
- DB constraints (unique ISBN, CHECK price, FK) are the source of truth; `IntegrityError` → 409.
- `joinedload(Book.author)` because `BookOut` nests the author (prevents N+1).
- Alembic from day one; naming convention for stable constraint names.

---

# Project 3 — Advanced: Project-Management API (auth, roles, relationships, pagination, tests)

### Requirements
- Users register/login (OAuth2 password flow → JWT access + refresh tokens).
- Roles: `user`, `manager`, `admin`. Admin can list users and change roles.
- Users own **projects**; projects contain **tasks** (status, priority 1–5, assignee, due date).
- Users only see/modify **their own** projects (admins see all) → 404 for others (no IDOR).
- Lists are paginated (`page`, `size ≤ 100`), searchable (`q`), sortable with a whitelist (`sort=-priority,id`), filterable (status, assignee, min priority).
- Unknown input fields are rejected (`extra="forbid"`) to block mass assignment.
- Automated tests for auth, permissions, CRUD, filtering.

### Architecture
```
Router (HTTP, validation, auth deps) ──► ProjectService (rules, ownership, transactions)
          │                                            │
          └─ deps.py: DbSession, CurrentUser, AdminUser, Pagination
                                                       ▼
                                              SQLAlchemy models ─► DB
```

### Folder structure
```
pmapi/
├── app/
│   ├── __init__.py
│   ├── main.py               # app factory, routers
│   ├── db.py                 # engine, Base, get_db
│   ├── models.py             # User, Project, Task
│   ├── schemas.py            # Pydantic DTOs, Page[T]
│   ├── deps.py               # auth + pagination dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Settings
│   │   ├── security.py       # hashing + JWT
│   │   └── exceptions.py     # domain errors + handler
│   ├── services/
│   │   ├── __init__.py
│   │   └── projects.py       # business logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       └── projects.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_projects.py
└── requirements.txt
```

### Steps
```bash
$ pip install "fastapi[standard]" "sqlalchemy>=2.0" pyjwt "pwdlib[argon2]" pydantic-settings pytest
$ python -c "from app.db import Base, engine; import app.models; Base.metadata.create_all(engine)"   # quick start (use Alembic in real life)
$ fastapi dev app/main.py
$ pytest -q
```

### `app/core/config.py`
```python
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Project Management API"
    database_url: str = "sqlite:///./pm.db"
    jwt_secret_key: SecretStr = SecretStr("dev-only-insecure-secret-change-me-32b")   # set JWT_SECRET_KEY in real envs
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```
(For production, remove the default on `jwt_secret_key` so a missing secret stops the app from starting — see Project 4.)

### `app/core/security.py`
```python
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def _create_token(subject: str, token_type: str, expires: timedelta, extra: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": subject, "type": token_type, "iat": now, "exp": now + expires,
               "jti": uuid4().hex, **(extra or {})}
    return jwt.encode(payload, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int, role: str) -> str:
    return _create_token(str(user_id), "access",
                         timedelta(minutes=settings.access_token_expire_minutes), {"role": role})


def create_refresh_token(user_id: int) -> str:
    return _create_token(str(user_id), "refresh", timedelta(days=settings.refresh_token_expire_days))


def decode_token(token: str, expected_type: str) -> dict:
    payload = jwt.decode(token, settings.jwt_secret_key.get_secret_value(),
                         algorithms=[settings.jwt_algorithm],
                         options={"require": ["exp", "sub", "type"]})
    if payload["type"] != expected_type:
        raise jwt.InvalidTokenError("wrong token type")
    return payload
```

### `app/core/exceptions.py`
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    status_code = 400
    code = "APP_ERROR"

    def __init__(self, message: str):
        self.message = message


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"


class ForbiddenError(AppError):
    status_code = 403
    code = "FORBIDDEN"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code,
                            content={"code": exc.code, "message": exc.message, "path": request.url.path})
```

### `app/db.py`
```python
from collections.abc import Generator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `app/models.py`
```python
from datetime import date, datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(120))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user", server_default="user")
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    projects: Mapped[list["Project"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    owner: Mapped[User] = relationship(back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (CheckConstraint("priority BETWEEN 1 AND 5", name="priority_range"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="todo", index=True)
    priority: Mapped[int] = mapped_column(default=3)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    due_date: Mapped[date | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    project: Mapped[Project] = relationship(back_populates="tasks")
    assignee: Mapped[User | None] = relationship()
```

### `app/schemas.py`
```python
from datetime import date, datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int


# ---------- users / auth ----------
class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=120)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str | None
    role: Role
    is_active: bool


class RoleUpdate(BaseModel):
    role: Role


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


# ---------- projects ----------
class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime


# ---------- tasks ----------
class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=200)
    status: TaskStatus = TaskStatus.todo
    priority: int = Field(default=3, ge=1, le=5)
    assignee_id: int | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=1, max_length=200)
    status: TaskStatus | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    assignee_id: int | None = None
    due_date: date | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    title: str
    status: TaskStatus
    priority: int
    assignee_id: int | None
    due_date: date | None
    created_at: datetime
```

### `app/deps.py`
```python
from collections.abc import Callable
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

DbSession = Annotated[Session, Depends(get_db)]

CREDENTIALS_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    try:
        user_id = int(decode_token(token, expected_type="access")["sub"])
    except (jwt.InvalidTokenError, ValueError):
        raise CREDENTIALS_EXC
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise CREDENTIALS_EXC
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: str) -> Callable[[User], User]:
    def checker(user: CurrentUser) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker


AdminUser = Annotated[User, Depends(require_roles("admin"))]


class PageParams:
    def __init__(self, page: Annotated[int, Query(ge=1)] = 1,
                 size: Annotated[int, Query(ge=1, le=100)] = 20):
        self.page, self.size = page, size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


Pagination = Annotated[PageParams, Depends()]
```

### `app/services/projects.py`
```python
from collections.abc import Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import AppError, NotFoundError
from app.models import Project, Task, User
from app.schemas import ProjectCreate, ProjectUpdate, TaskCreate, TaskStatus, TaskUpdate

PROJECT_SORTS = {"name": Project.name, "created_at": Project.created_at, "id": Project.id}
TASK_SORTS = {"priority": Task.priority, "due_date": Task.due_date,
              "created_at": Task.created_at, "id": Task.id}


def _order_by(stmt: Select, sort: str, allowed: dict) -> Select:
    """'-priority,id' -> ORDER BY priority DESC, id ASC (whitelisted columns only)."""
    for part in sort.split(","):
        desc = part.startswith("-")
        column = allowed.get(part.lstrip("-+"))
        if column is None:
            raise AppError(f"Cannot sort by '{part}'. Allowed: {', '.join(allowed)}")
        stmt = stmt.order_by(column.desc() if desc else column.asc())
    return stmt


def _paginate(db: Session, stmt: Select, offset: int, limit: int) -> tuple[Sequence, int]:
    total = db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
    items = db.scalars(stmt.offset(offset).limit(limit)).all()
    return items, total


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    # ----- projects -----
    def list(self, user: User, offset: int, limit: int, q: str | None, sort: str):
        stmt = select(Project)
        if user.role != "admin":                                   # admins see everything
            stmt = stmt.where(Project.owner_id == user.id)
        if q:
            stmt = stmt.where(Project.name.ilike(f"%{q}%"))
        return _paginate(self.db, _order_by(stmt, sort, PROJECT_SORTS), offset, limit)

    def get_accessible(self, user: User, project_id: int) -> Project:
        project = self.db.get(Project, project_id)
        if project is None or (project.owner_id != user.id and user.role != "admin"):
            raise NotFoundError("Project not found")              # 404 hides other users' projects
        return project

    def create(self, user: User, data: ProjectCreate) -> Project:
        project = Project(**data.model_dump(), owner_id=user.id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, user: User, project_id: int, data: ProjectUpdate) -> Project:
        project = self.get_accessible(user, project_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, user: User, project_id: int) -> None:
        self.db.delete(self.get_accessible(user, project_id))
        self.db.commit()

    # ----- tasks -----
    def list_tasks(self, user: User, project_id: int, offset: int, limit: int, *,
                   status: TaskStatus | None, assignee_id: int | None,
                   min_priority: int | None, q: str | None, sort: str):
        self.get_accessible(user, project_id)
        stmt = select(Task).where(Task.project_id == project_id)
        if status is not None:
            stmt = stmt.where(Task.status == status.value)
        if assignee_id is not None:
            stmt = stmt.where(Task.assignee_id == assignee_id)
        if min_priority is not None:
            stmt = stmt.where(Task.priority >= min_priority)
        if q:
            stmt = stmt.where(Task.title.ilike(f"%{q}%"))
        return _paginate(self.db, _order_by(stmt, sort, TASK_SORTS), offset, limit)

    def _check_assignee(self, assignee_id: int | None) -> None:
        if assignee_id is not None and self.db.get(User, assignee_id) is None:
            raise AppError(f"Assignee {assignee_id} does not exist")

    def create_task(self, user: User, project_id: int, data: TaskCreate) -> Task:
        self.get_accessible(user, project_id)
        self._check_assignee(data.assignee_id)
        task = Task(**data.model_dump(mode="python"), project_id=project_id)
        task.status = data.status.value
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def _get_task(self, user: User, project_id: int, task_id: int) -> Task:
        self.get_accessible(user, project_id)
        task = self.db.get(Task, task_id)
        if task is None or task.project_id != project_id:
            raise NotFoundError("Task not found")
        return task

    def update_task(self, user: User, project_id: int, task_id: int, data: TaskUpdate) -> Task:
        task = self._get_task(user, project_id, task_id)
        changes = data.model_dump(exclude_unset=True)
        if "assignee_id" in changes:
            self._check_assignee(changes["assignee_id"])
        if changes.get("status") is not None:
            changes["status"] = changes["status"].value
        for field, value in changes.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, user: User, project_id: int, task_id: int) -> None:
        self.db.delete(self._get_task(user, project_id, task_id))
        self.db.commit()
```

### `app/routers/auth.py`
```python
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.core.security import (create_access_token, create_refresh_token, decode_token,
                               hash_password, verify_password)
from app.deps import CurrentUser, DbSession
from app.models import User
from app.schemas import RefreshRequest, TokenPair, UserOut, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])
_DUMMY_HASH = hash_password("timing-equalizer")
_BAD_LOGIN = HTTPException(status_code=401, detail="Incorrect email or password",
                           headers={"WWW-Authenticate": "Bearer"})


def _tokens(user: User) -> TokenPair:
    return TokenPair(access_token=create_access_token(user.id, user.role),
                     refresh_token=create_refresh_token(user.id))


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: DbSession):
    email = data.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email, full_name=data.full_name, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token", response_model=TokenPair)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if user is None:
        verify_password(form.password, _DUMMY_HASH)     # same timing as a real check
        raise _BAD_LOGIN
    if not verify_password(form.password, user.hashed_password) or not user.is_active:
        raise _BAD_LOGIN
    return _tokens(user)


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, db: DbSession):
    try:
        user_id = int(decode_token(body.refresh_token, expected_type="refresh")["sub"])
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return _tokens(user)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user
```

### `app/routers/users.py`
```python
from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app.deps import AdminUser, DbSession, Pagination
from app.models import User
from app.schemas import Page, RoleUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users (admin)"])


@router.get("", response_model=Page[UserOut])
def list_users(admin: AdminUser, db: DbSession, p: Pagination):
    total = db.scalar(select(func.count(User.id))) or 0
    items = db.scalars(select(User).order_by(User.id).offset(p.offset).limit(p.size)).all()
    return Page(items=items, total=total, page=p.page, size=p.size)


@router.patch("/{user_id}/role", response_model=UserOut)
def change_role(user_id: int, body: RoleUpdate, admin: AdminUser, db: DbSession):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = body.role.value
    db.commit()
    db.refresh(user)
    return user
```

### `app/routers/projects.py`
```python
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.deps import CurrentUser, DbSession, Pagination
from app.schemas import (Page, ProjectCreate, ProjectOut, ProjectUpdate, TaskCreate, TaskOut,
                         TaskStatus, TaskUpdate)
from app.services.projects import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


def get_service(db: DbSession) -> ProjectService:
    return ProjectService(db)


Service = Annotated[ProjectService, Depends(get_service)]


# ---------------- projects ----------------
@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, user: CurrentUser, svc: Service):
    return svc.create(user, data)


@router.get("", response_model=Page[ProjectOut])
def list_projects(user: CurrentUser, svc: Service, p: Pagination,
                  q: Annotated[str | None, Query(max_length=100)] = None,
                  sort: str = "-created_at,-id"):
    items, total = svc.list(user, p.offset, p.size, q, sort)
    return Page(items=items, total=total, page=p.page, size=p.size)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, user: CurrentUser, svc: Service):
    return svc.get_accessible(user, project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, user: CurrentUser, svc: Service):
    return svc.update(user, project_id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, user: CurrentUser, svc: Service):
    svc.delete(user, project_id)


# ---------------- tasks (nested resource) ----------------
@router.post("/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, data: TaskCreate, user: CurrentUser, svc: Service):
    return svc.create_task(user, project_id, data)


@router.get("/{project_id}/tasks", response_model=Page[TaskOut])
def list_tasks(project_id: int, user: CurrentUser, svc: Service, p: Pagination,
               status: TaskStatus | None = None,
               assignee_id: int | None = None,
               min_priority: Annotated[int | None, Query(ge=1, le=5)] = None,
               q: Annotated[str | None, Query(max_length=100)] = None,
               sort: str = "-priority,id"):
    items, total = svc.list_tasks(user, project_id, p.offset, p.size, status=status,
                                  assignee_id=assignee_id, min_priority=min_priority, q=q, sort=sort)
    return Page(items=items, total=total, page=p.page, size=p.size)


@router.patch("/{project_id}/tasks/{task_id}", response_model=TaskOut)
def update_task(project_id: int, task_id: int, data: TaskUpdate, user: CurrentUser, svc: Service):
    return svc.update_task(user, project_id, task_id, data)


@router.delete("/{project_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(project_id: int, task_id: int, user: CurrentUser, svc: Service):
    svc.delete_task(user, project_id, task_id)
```

### `app/main.py`
```python
from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import auth, projects, users


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="1.0.0")
    register_exception_handlers(app)

    api = APIRouter(prefix="/api/v1")
    api.include_router(auth.router)
    api.include_router(users.router)
    api.include_router(projects.router)
    app.include_router(api)

    @app.get("/health", tags=["ops"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
```

### `tests/conftest.py`
```python
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.core.security import create_access_token, hash_password
from app.db import Base, get_db
from app.main import create_app
from app.models import User

# In-memory SQLite shared across threads (TestClient runs sync endpoints in a threadpool).
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(engine)          # fresh schema per test → full isolation
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


def make_user(db: Session, email: str, role: str = "user", password: str = "Passw0rd!") -> User:
    user = User(email=email, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.commit()
    return user


def auth_header(user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role)}"}


@pytest.fixture
def alice(db):
    return make_user(db, "alice@example.com")


@pytest.fixture
def bob(db):
    return make_user(db, "bob@example.com")


@pytest.fixture
def admin(db):
    return make_user(db, "admin@example.com", role="admin")
```
(SQLite keeps this project zero-setup. For Postgres-specific behavior, use the transaction-rollback fixture from Chapter 9.)

### `tests/test_auth.py`
```python
from tests.conftest import auth_header


def test_register_login_me_flow(client):
    r = client.post("/api/v1/auth/register", json={"email": "New@Example.com", "password": "Passw0rd!"})
    assert r.status_code == 201
    assert r.json()["email"] == "new@example.com"
    assert "hashed_password" not in r.json()                       # response_model filtered it

    r = client.post("/api/v1/auth/token", data={"username": "new@example.com", "password": "Passw0rd!"})
    assert r.status_code == 200
    tokens = r.json()

    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert r.status_code == 200 and r.json()["role"] == "user"


def test_duplicate_email_conflict(client, alice):
    r = client.post("/api/v1/auth/register", json={"email": alice.email, "password": "Passw0rd!"})
    assert r.status_code == 409


def test_short_password_rejected(client):
    r = client.post("/api/v1/auth/register", json={"email": "x@example.com", "password": "short"})
    assert r.status_code == 422


def test_wrong_password(client, alice):
    r = client.post("/api/v1/auth/token", data={"username": alice.email, "password": "nope-nope"})
    assert r.status_code == 401


def test_me_without_token(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401
    assert r.headers["www-authenticate"] == "Bearer"


def test_refresh_token_cannot_be_used_as_access(client, alice):
    tokens = client.post("/api/v1/auth/token",
                         data={"username": alice.email, "password": "Passw0rd!"}).json()
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['refresh_token']}"})
    assert r.status_code == 401
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert r.status_code == 200 and "access_token" in r.json()


def test_admin_only_endpoints(client, alice, admin):
    assert client.get("/api/v1/users", headers=auth_header(alice)).status_code == 403
    r = client.get("/api/v1/users", headers=auth_header(admin))
    assert r.status_code == 200 and r.json()["total"] == 2
    r = client.patch(f"/api/v1/users/{alice.id}/role", json={"role": "manager"}, headers=auth_header(admin))
    assert r.json()["role"] == "manager"
```

### `tests/test_projects.py`
```python
from tests.conftest import auth_header

API = "/api/v1/projects"


def _create_project(client, user, name="Apollo"):
    r = client.post(API, json={"name": name}, headers=auth_header(user))
    assert r.status_code == 201
    return r.json()


def test_project_crud(client, alice):
    h = auth_header(alice)
    project = _create_project(client, alice)
    assert project["owner_id"] == alice.id

    r = client.patch(f"{API}/{project['id']}", json={"description": "Moon"}, headers=h)
    assert r.status_code == 200
    assert r.json()["description"] == "Moon" and r.json()["name"] == "Apollo"   # PATCH kept name

    assert client.delete(f"{API}/{project['id']}", headers=h).status_code == 204
    assert client.get(f"{API}/{project['id']}", headers=h).status_code == 404


def test_unknown_field_rejected(client, alice):
    r = client.post(API, json={"name": "X", "owner_id": 999}, headers=auth_header(alice))
    assert r.status_code == 422                                     # mass assignment blocked


def test_cannot_access_other_users_project(client, alice, bob):
    project = _create_project(client, alice)
    r = client.get(f"{API}/{project['id']}", headers=auth_header(bob))
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"


def test_admin_sees_all_projects(client, alice, bob, admin):
    _create_project(client, alice, "A")
    _create_project(client, bob, "B")
    assert client.get(API, headers=auth_header(alice)).json()["total"] == 1
    assert client.get(API, headers=auth_header(admin)).json()["total"] == 2


def test_pagination_search_and_sort(client, alice):
    for name in ["delta", "alpha", "charlie", "bravo", "alpine"]:
        _create_project(client, alice, name)
    h = auth_header(alice)

    page = client.get(API, params={"page": 2, "size": 2, "sort": "name"}, headers=h).json()
    assert page["total"] == 5
    assert [p["name"] for p in page["items"]] == ["bravo", "charlie"]   # alpha, alpine | bravo, charlie | delta

    found = client.get(API, params={"q": "alp"}, headers=h).json()
    assert {p["name"] for p in found["items"]} == {"alpha", "alpine"}

    bad = client.get(API, params={"sort": "password"}, headers=h)
    assert bad.status_code == 400


def test_tasks_filtering(client, alice, bob):
    h = auth_header(alice)
    pid = _create_project(client, alice)["id"]
    tasks = [
        {"title": "Design", "priority": 5, "status": "done"},
        {"title": "Build", "priority": 4, "assignee_id": bob.id},
        {"title": "Test", "priority": 2},
    ]
    for t in tasks:
        assert client.post(f"{API}/{pid}/tasks", json=t, headers=h).status_code == 201

    r = client.get(f"{API}/{pid}/tasks", params={"status": "todo"}, headers=h).json()
    assert [t["title"] for t in r["items"]] == ["Build", "Test"]     # default sort -priority

    r = client.get(f"{API}/{pid}/tasks", params={"min_priority": 4}, headers=h).json()
    assert r["total"] == 2

    r = client.get(f"{API}/{pid}/tasks", params={"assignee_id": bob.id}, headers=h).json()
    assert r["items"][0]["title"] == "Build"

    assert client.get(f"{API}/{pid}/tasks", headers=auth_header(bob)).status_code == 404


def test_task_validation_and_update(client, alice):
    h = auth_header(alice)
    pid = _create_project(client, alice)["id"]
    assert client.post(f"{API}/{pid}/tasks", json={"title": "X", "priority": 9}, headers=h).status_code == 422
    assert client.post(f"{API}/{pid}/tasks", json={"title": "X", "assignee_id": 999}, headers=h).status_code == 400

    task = client.post(f"{API}/{pid}/tasks", json={"title": "Write docs"}, headers=h).json()
    r = client.patch(f"{API}/{pid}/tasks/{task['id']}", json={"status": "in_progress"}, headers=h)
    assert r.status_code == 200 and r.json()["status"] == "in_progress"
    assert client.delete(f"{API}/{pid}/tasks/{task['id']}", headers=h).status_code == 204
```

### Running the tests
```bash
$ pytest -q
..............                                                   [100%]
14 passed
```

### Manual walkthrough (Swagger)
1. `POST /api/v1/auth/register` → create `you@example.com`.
2. Click **Authorize 🔒** → username = email, password → **Authorize**.
3. `POST /api/v1/projects` `{"name": "Website"}` → 201.
4. `POST /api/v1/projects/1/tasks` `{"title": "Landing page", "priority": 5}`.
5. `GET /api/v1/projects/1/tasks?status=todo&sort=-priority,id&page=1&size=10`.
6. Make yourself admin (in DB: `UPDATE users SET role='admin' WHERE id=1`) → `GET /api/v1/users`.

### Design decisions
| Decision | Why |
|---|---|
| Service layer owns ownership checks + commits | Routers stay thin; rules are testable and reused |
| 404 (not 403) for other users' projects | Doesn't reveal that the resource exists |
| `extra="forbid"` on inputs | Clients can't set `owner_id`/`project_id` (mass assignment) |
| Sort whitelist dict → column objects | No SQL injection via `sort`, clear error message |
| `Page[T]` generic response | Consistent pagination envelope across endpoints |
| `type` claim in JWT | Refresh tokens can't be used as access tokens (tested) |
| Dummy hash on unknown email | Equal timing → no user enumeration |
| SQLite in tests + `StaticPool` | Zero-setup, fast; switch to Postgres fixture for dialect-specific features |
| Next steps | Alembic migrations, project memberships (many-to-many `project_members` with role per project), refresh-token rotation table, rate-limit login |

---

# Project 4 — Senior: Production-Style API

**Goal:** Take Project 3 and make it production-grade: modular architecture, Postgres + Alembic, Docker, structured logging with request IDs, Redis caching + rate limiting, health/readiness, Prometheus metrics, security hardening, CI/CD.

### Requirements (non-functional)
- Config via env vars; required secrets fail fast.
- JSON logs with `request_id`; no secrets in logs.
- `GET /health/live`, `GET /health/ready` (DB + Redis), `/metrics`.
- Login rate limit 5/min per IP; cached `GET /projects/{id}` (60 s, invalidated on update).
- Docker image non-root; `docker compose up` runs API + Postgres + Redis + migrations.
- CI: lint, type-check, tests with coverage, `alembic check`, build image.

### Architecture
```
            ┌──────────── docker compose / k8s ─────────────┐
Client ──► Nginx/LB ──► api (uvicorn, N replicas) ──► Postgres
                         │  middleware: request-id, logging, security headers, CORS
                         │  deps: auth, rate-limit (Redis), db session
                         │  services ─► repositories / cache (Redis)
                         └─► /metrics ──► Prometheus ──► Grafana
           migrate job: alembic upgrade head (runs before rollout)
```

### Folder structure (feature-based)
```
pm-prod/
├── app/
│   ├── main.py                  # create_app()
│   ├── core/
│   │   ├── config.py            # Settings (no default secret)
│   │   ├── logging.py           # structlog setup + redaction
│   │   ├── middleware.py        # request-id/logging, security headers
│   │   ├── lifespan.py          # redis, engine dispose
│   │   ├── cache.py             # cache helpers
│   │   ├── ratelimit.py         # Redis limiter dependency
│   │   ├── security.py          # (from P3)
│   │   └── exceptions.py        # (from P3) + generic 500 handler
│   ├── db/{base.py, session.py}
│   ├── auth/{router.py, schemas.py, service.py}
│   ├── users/{router.py, models.py, schemas.py}
│   ├── projects/{router.py, models.py, schemas.py, service.py}
│   └── health/router.py
├── alembic/  alembic.ini
├── tests/
├── Dockerfile  .dockerignore  docker-compose.yml
├── pyproject.toml  requirements.txt  requirements-dev.txt
├── Makefile
└── .github/workflows/ci.yml
```

### `app/core/config.py`
```python
from functools import lru_cache
from typing import Literal
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "PM API"
    environment: Literal["local", "staging", "prod"] = "local"
    log_level: str = "INFO"
    log_json: bool = True
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: SecretStr                          # no default → must be provided
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    cors_origins: list[str] = Field(default_factory=list)
    allowed_hosts: list[str] = Field(default_factory=lambda: ["*"])

    @property
    def is_prod(self) -> bool:
        return self.environment == "prod"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### `app/core/logging.py`
```python
import logging
import structlog

SENSITIVE = {"password", "token", "access_token", "refresh_token", "authorization", "secret"}

def _redact(_, __, event: dict) -> dict:
    for key in list(event):
        if key.lower() in SENSITIVE:
            event[key] = "***"
    return event

def setup_logging(level: str = "INFO", json: bool = True) -> None:
    logging.basicConfig(format="%(message)s", level=level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            _redact,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if json else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(level)),
        cache_logger_on_first_use=True,
    )
```

### `app/core/middleware.py`
```python
import time
import uuid
import structlog
from fastapi import FastAPI, Request

log = structlog.get_logger("http")

def add_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
        return response

    @app.middleware("http")                       # added last → runs first (outermost)
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id, method=request.method,
                                               path=request.url.path)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            log.exception("unhandled_exception")
            raise
        duration = round((time.perf_counter() - start) * 1000, 1)
        if request.url.path not in {"/health/live", "/metrics"}:
            log.info("request", status=response.status_code, duration_ms=duration)
        response.headers["X-Request-ID"] = request_id
        return response
```

### `app/core/lifespan.py`
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis
from app.core.config import settings
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis.from_url(settings.redis_url, decode_responses=True)
    yield
    await app.state.redis.aclose()
    engine.dispose()
```

### `app/core/ratelimit.py`
```python
import time
from fastapi import Depends, HTTPException, Request

def rate_limit(limit: int, window_seconds: int):
    async def dependency(request: Request) -> None:
        redis = request.app.state.redis
        client_ip = request.client.host if request.client else "unknown"
        bucket = int(time.time() // window_seconds)
        key = f"rl:{request.url.path}:{client_ip}:{bucket}"
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, window_seconds)
        if count > limit:
            raise HTTPException(429, "Too many requests", headers={"Retry-After": str(window_seconds)})
    return Depends(dependency)
```
Use: `@router.post("/token", dependencies=[rate_limit(5, 60)])`.

### `app/core/cache.py` + usage in the projects router
```python
import json
from redis.asyncio import Redis

def project_key(project_id: int) -> str:
    return f"project:v1:{project_id}"

async def cache_get(redis: Redis, key: str) -> dict | None:
    raw = await redis.get(key)
    return json.loads(raw) if raw else None

async def cache_set(redis: Redis, key: str, value: dict, ttl: int = 60) -> None:
    await redis.set(key, json.dumps(value), ex=ttl)
```
```python
# app/projects/router.py (excerpt) — async endpoint, sync service in threadpool
from starlette.concurrency import run_in_threadpool

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int, request: Request, user: CurrentUser, svc: Service):
    redis = request.app.state.redis
    project = await run_in_threadpool(svc.get_accessible, user, project_id)   # authz ALWAYS checked
    key = project_key(project_id)
    if cached := await cache_get(redis, key):
        return cached
    data = ProjectOut.model_validate(project).model_dump(mode="json")
    await cache_set(redis, key, data)
    return data

@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, data: ProjectUpdate, request: Request,
                         user: CurrentUser, svc: Service):
    project = await run_in_threadpool(svc.update, user, project_id, data)
    await request.app.state.redis.delete(project_key(project_id))            # invalidate after commit
    return project
```
💡 This toy example still loads the row for the authorization check, so the cache only saves serialization. In a real system you'd cache expensive aggregates (e.g., project dashboard stats) — the pattern is identical. Never let a cache hit skip authorization.

### `app/health/router.py`
```python
import asyncio
from fastapi import APIRouter, Request, Response
from sqlalchemy import text
from starlette.concurrency import run_in_threadpool
from app.db.session import engine

router = APIRouter(prefix="/health", tags=["ops"])

@router.get("/live")
def live():
    return {"status": "alive"}

def _db_ping() -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

@router.get("/ready")
async def ready(request: Request, response: Response):
    checks = {}
    try:
        await asyncio.wait_for(run_in_threadpool(_db_ping), timeout=2)
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "fail"
    try:
        await asyncio.wait_for(request.app.state.redis.ping(), timeout=1)
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "fail"
    ok = all(v == "ok" for v in checks.values())
    response.status_code = 200 if ok else 503
    return {"status": "ready" if ok else "not_ready", "checks": checks}
```

### `app/main.py`
```python
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.auth.router import router as auth_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.core.middleware import add_middlewares
from app.health.router import router as health_router
from app.projects.router import router as projects_router
from app.users.router import router as users_router


def create_app() -> FastAPI:
    setup_logging(settings.log_level, settings.log_json)
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        docs_url=None if settings.is_prod else "/docs",
        redoc_url=None if settings.is_prod else "/redoc",
        openapi_url=None if settings.is_prod else "/openapi.json",
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True,
                       allow_methods=["GET", "POST", "PATCH", "DELETE"],
                       allow_headers=["Authorization", "Content-Type", "X-Request-ID"])
    add_middlewares(app)
    register_exception_handlers(app)

    api = APIRouter(prefix="/api/v1")
    for r in (auth_router, users_router, projects_router):
        api.include_router(r)
    app.include_router(api)
    app.include_router(health_router)
    Instrumentator(excluded_handlers=["/health.*", "/metrics"]).instrument(app).expose(
        app, endpoint="/metrics", include_in_schema=False)
    return app


app = create_app()
```
Add to `exceptions.py` a catch-all that logs and returns a generic 500:
```python
@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    structlog.get_logger().exception("unhandled_error")
    return JSONResponse(status_code=500, content={"code": "INTERNAL_ERROR", "message": "Internal server error"})
```

### Alembic for Project 4
```bash
$ alembic init alembic                            # edit env.py as in Chapter 5 (import all feature models)
$ alembic revision --autogenerate -m "initial schema"
$ alembic upgrade head
```
Feature-based layout: `app/db/models.py` should `from app.users.models import *` / `from app.projects.models import *` so `env.py` imports one module.

### `requirements.txt`
```
fastapi[standard]>=0.115
sqlalchemy>=2.0
psycopg[binary]>=3.2
alembic>=1.13
pydantic-settings>=2.4
pyjwt>=2.9
pwdlib[argon2]>=0.2
redis>=5.0
structlog>=24.1
prometheus-fastapi-instrumentator>=7.0
```
`requirements-dev.txt`: `-r requirements.txt`, `pytest`, `pytest-cov`, `ruff`, `mypy`, `fakeredis`, `respx`.

### `Dockerfile`
Use the multi-stage, non-root Dockerfile from Chapter 10 §10.13 unchanged.

### `docker-compose.yml`
```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql+psycopg://app:app@db:5432/pm
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?set JWT_SECRET_KEY}
      ENVIRONMENT: local
      CORS_ORIGINS: '["http://localhost:5173"]'
    depends_on:
      migrate: { condition: service_completed_successfully }
      redis: { condition: service_started }
  migrate:
    build: .
    command: ["alembic", "upgrade", "head"]
    environment:
      DATABASE_URL: postgresql+psycopg://app:app@db:5432/pm
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:?set JWT_SECRET_KEY}
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:17
    environment: { POSTGRES_USER: app, POSTGRES_PASSWORD: app, POSTGRES_DB: pm }
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD-SHELL", "pg_isready -U app"], interval: 5s, retries: 10 }
  redis:
    image: redis:7-alpine
volumes:
  pgdata:
```

### `Makefile` (developer UX)
```makefile
.PHONY: dev test lint migrate up down
dev:      ; fastapi dev app/main.py
test:     ; pytest --cov=app --cov-report=term-missing
lint:     ; ruff check . && ruff format --check . && mypy app
migrate:  ; alembic upgrade head
up:       ; docker compose up --build -d
down:     ; docker compose down
```
(Windows without `make`: run the commands directly, or use `uv run` / `just` / a `tasks.ps1`.)

### CI: `.github/workflows/ci.yml`
Use the workflow from Chapter 10 §10.14 (Postgres service, ruff, mypy, `alembic upgrade head && alembic check`, pytest with `--cov-fail-under`, pip-audit, build and push the image, migration job, then deploy).

### Testing Project 4
- Reuse Project 3 tests. Override Redis with `fakeredis`:
  ```python
  import fakeredis
  @pytest.fixture
  def client(app):
      with TestClient(app) as c:                      # lifespan creates real Redis client...
          app.state.redis = fakeredis.FakeAsyncRedis(decode_responses=True)   # ...replace it
          yield c
  ```
- New tests: rate limit returns 429 on 6th login; cache invalidated after PATCH; `/health/ready` returns 503 when DB ping is patched to fail; `X-Request-ID` echoed; 500 handler hides details.
- Smoke test after deploy: `curl -fsS https://api.example.com/health/ready`.

### Run it
```bash
$ export JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
$ docker compose up --build
$ curl localhost:8000/health/ready
{"status":"ready","checks":{"database":"ok","redis":"ok"}}
$ curl localhost:8000/metrics | head
```
```powershell
PS> $env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
PS> docker compose up --build
```

### Design decisions (what to say in a design review)
| Decision | Rationale | Trade-off |
|---|---|---|
| Feature-based modules | Ownership & future extraction | More folders |
| Sync SQLAlchemy + threadpool; async for Redis/HTTP | Simpler ORM usage; async where it's free | Threadpool size must match DB pool |
| Migrations as a separate job | No races between replicas; explicit failure | One more pipeline step |
| Readiness checks deps, liveness doesn't | Avoid restart storms during DB outages | — |
| Redis for cache + rate limit | Shared across replicas | Extra infra; fail-open vs fail-closed decision for limiter |
| JSON logs + request ID + Prometheus | Debuggable, alertable | Log volume cost |
| Docs disabled in prod | Smaller attack surface | Publish OpenAPI separately for consumers |
| Non-root image, secrets from env | Least privilege | — |

**Extensions to practice:** OpenTelemetry tracing, Celery worker for emails, refresh-token rotation table, idempotency keys on `POST /projects`, cursor pagination for tasks, Kubernetes manifests (Deployment with probes, HPA, Job for migrations).
