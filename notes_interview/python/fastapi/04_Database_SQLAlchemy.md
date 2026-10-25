# Chapter 4 — Database Integration and ORMs (SQLAlchemy 2.x)

> **Goal:** Connect FastAPI to a relational database, model tables and relationships with modern SQLAlchemy 2.x, manage sessions safely with dependency injection, write efficient queries, and know when to go async.

---

## 4.1 Relational Database Basics (2-minute refresher)

| Term | Meaning | Example |
|---|---|---|
| Table | A collection of rows of the same shape | `users` |
| Row / record | One entry | user #7 |
| Column | A typed attribute | `email VARCHAR(255)` |
| Primary key (PK) | Unique row identifier | `id` |
| Foreign key (FK) | Column pointing to another table's PK | `posts.user_id → users.id` |
| Constraint | Rule the DB enforces | `UNIQUE`, `NOT NULL`, `CHECK (price > 0)` |
| Index | Lookup structure for fast search | index on `users.email` |
| Join | Combine rows of related tables | users ⨝ posts |
| Transaction | Group of statements that all succeed or all fail | transfer money |
| ACID | Atomicity, Consistency, Isolation, Durability | — |
| Normalization | Avoid duplicated data by splitting tables | — |

**Which database?**

| DB | Use for | Driver (sync / async) | URL |
|---|---|---|---|
| SQLite | Learning, tests, tiny apps (single file) | built-in / `aiosqlite` | `sqlite:///./app.db` |
| **PostgreSQL** | Default production choice | `psycopg` (v3) / `asyncpg` or psycopg async | `postgresql+psycopg://user:pw@host:5432/db` |
| MySQL/MariaDB | Existing MySQL shops | `pymysql` / `aiomysql`, `asyncmy` | `mysql+pymysql://user:pw@host:3306/db` |

```bash
$ pip install "sqlalchemy>=2.0" "psycopg[binary]"     # Postgres
$ pip install pymysql                                 # MySQL
```

Quick Postgres with Docker:
```bash
$ docker run -d --name pg -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app -e POSTGRES_DB=app -p 5432:5432 postgres:17
```

---

## 4.2 What Is an ORM?

**ORM (Object-Relational Mapper)** lets you work with tables as Python classes and rows as objects.

```python
# without ORM
cur.execute("SELECT id, email FROM users WHERE id = %s", (7,))
# with ORM
user = session.get(User, 7); print(user.email)
```

| ORM pros | ORM cons |
|---|---|
| Less boilerplate, Pythonic | Can hide expensive queries (N+1) |
| Parameterized queries → SQL-injection safe by default | Learning curve |
| DB-portable | Complex reporting queries may be easier in raw SQL |
| Relationships, unit of work, identity map | |

SQLAlchemy has two layers: **Core** (SQL expression language: `select()`, `insert()`) and **ORM** (classes, sessions). In 2.x they share the same `select()` API.

---

## 4.3 Engine, Session and Base (sync setup)

**`app/db.py`**
```python
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "postgresql+psycopg://app:app@localhost:5432/app"
# DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,            # persistent connections kept open
    max_overflow=10,        # extra connections under burst
    pool_pre_ping=True,     # test connection before use (survives DB restarts)
    pool_recycle=1800,      # recycle connections older than 30 min
    echo=False,             # True = log every SQL statement (debugging)
    # SQLite only: connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """All ORM models inherit from this."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: one session per request, always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

| Object | What it is | Lifetime |
|---|---|---|
| **Engine** | Connection pool + dialect. Knows *how* to talk to the DB. | **One per app** (process) |
| **Session** | Unit of work: tracks objects, holds a transaction | **One per request** |
| **Connection** | A real DB connection borrowed from the pool | Borrowed during a transaction |

💡 `expire_on_commit=False`: after `commit()`, objects keep their loaded values — avoids surprise lazy reloads (and is **required** for async).

⚠️ Old style `declarative_base()` from `sqlalchemy.ext.declarative` is deprecated → use `class Base(DeclarativeBase)`.

---

## 4.4 Models: Tables, Columns, Constraints (2.x typed style)

**`app/models.py`**
```python
from datetime import datetime
from decimal import Decimal
from sqlalchemy import (CheckConstraint, ForeignKey, Index, Numeric, String, Text,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(120))   # Optional → NULL allowed
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False,
                                              cascade="all, delete-orphan")
    posts: Mapped[list["Post"]] = relationship(back_populates="author",
                                               cascade="all, delete-orphan")


class Profile(Base):                               # one-to-one with User
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    bio: Mapped[str | None] = mapped_column(Text)
    user: Mapped[User] = relationship(back_populates="profile")


# association table for many-to-many (no extra columns → plain Table)
from sqlalchemy import Column, Table
post_tags = Table(
    "post_tags", Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Post(TimestampMixin, Base):                  # many-to-one with User
    __tablename__ = "posts"
    __table_args__ = (
        UniqueConstraint("author_id", "slug", name="uq_post_author_slug"),
        CheckConstraint("char_length(title) > 0", name="ck_post_title_nonempty"),
        Index("ix_posts_author_created", "author_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(220))
    body: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    author: Mapped[User] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")


class Tag(Base):                                   # many-to-many with Post
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    posts: Mapped[list[Post]] = relationship(secondary=post_tags, back_populates="tags")
```

Key ideas:
- `Mapped[int]` → NOT NULL; `Mapped[str | None]` → NULLable. Type drives the column type.
- `default=` → Python-side default; `server_default=` → DB-side default (also present in migrations; safer for raw inserts).
- `index=True`, `unique=True` → indexes/constraints. Composite ones in `__table_args__`.
- `ondelete="CASCADE"` → DB deletes children; `cascade="all, delete-orphan"` → ORM deletes children it knows about. Use both for consistency.
- Always **name constraints** (or set a naming convention, see chapter 5) so Alembic can drop/alter them.

⚠️ Old 1.x style `id = Column(Integer, primary_key=True)` still works but lacks type-checker support. Prefer `Mapped` + `mapped_column`.

### Many-to-many with extra columns → Association Object
```python
class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    grade: Mapped[str | None] = mapped_column(String(2))
    enrolled_at: Mapped[datetime] = mapped_column(server_default=func.now())
    student: Mapped["Student"] = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")
```

### Relationship cheat table

| Relationship | FK lives on | Python side |
|---|---|---|
| One-to-one | child (`profiles.user_id UNIQUE`) | `Mapped["Profile"]` + `uselist=False` |
| One-to-many | "many" side (`posts.author_id`) | parent: `Mapped[list["Post"]]`; child: `Mapped["User"]` |
| Many-to-many | association table | `relationship(secondary=table)` |
| M2M + data | association object (own class) | two one-to-many relationships |

### Creating tables (learning only)
```python
Base.metadata.create_all(engine)     # creates missing tables; never alters existing ones
```
⚠️ In real projects, use **Alembic** (chapter 5). `create_all` can't add columns or migrate data.

---

## 4.5 Dependency Injection for Sessions

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db

DbSession = Annotated[Session, Depends(get_db)]   # reusable alias


@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: DbSession):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

How the `yield` dependency works:
```
request ─► get_db(): db = SessionLocal() ─► yield db ─► endpoint uses db ─► response
                                                                     └─► finally: db.close()
```
Closing returns the connection to the pool and rolls back any uncommitted transaction.

### Transaction-per-request variant (commit automatically)
```python
def get_db_tx() -> Generator[Session, None, None]:
    with SessionLocal() as db:          # closes automatically
        with db.begin():                # commits on success, rolls back on exception
            yield db
```
Trade-off: convenient, but the commit happens *after* the endpoint returns — if the commit fails (e.g., unique violation at flush time), the response may already be decided. Many teams commit explicitly in the service layer instead (shown below). Pick one convention and stick to it.

---

## 4.6 CRUD with SQLAlchemy 2.x

```python
# app/crud.py
from collections.abc import Sequence
from sqlalchemy import select, func, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate


def create_user(db: Session, data: UserCreate, hashed_password: str) -> User:
    user = User(email=data.email, full_name=data.full_name, hashed_password=hashed_password)
    db.add(user)                 # stage INSERT
    try:
        db.commit()              # flush + COMMIT
    except IntegrityError:
        db.rollback()            # session unusable until rollback
        raise ValueError("Email already exists")
    db.refresh(user)             # reload DB-generated values (id, created_at)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)                     # PK lookup (uses identity map)


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()                  # or db.execute(stmt).scalar_one_or_none()


def list_users(db: Session, skip: int = 0, limit: int = 20,
               q: str | None = None) -> tuple[Sequence[User], int]:
    stmt = select(User)
    if q:
        stmt = stmt.where(User.email.ilike(f"%{q}%"))     # parameterized → safe
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = db.scalars(stmt.order_by(User.id).offset(skip).limit(limit)).all()
    return rows, total


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)                  # ORM tracks changes → UPDATE on commit
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


# bulk operations (no objects loaded, one SQL statement)
def deactivate_inactive(db: Session) -> int:
    result = db.execute(update(User).where(User.is_active.is_(True), User.full_name.is_(None))
                        .values(is_active=False))
    db.commit()
    return result.rowcount
```

### 2.x query API vs ⚠️ legacy 1.x

| Task | 2.x style ✅ | 1.x legacy ⚠️ |
|---|---|---|
| By PK | `db.get(User, 1)` | `db.query(User).get(1)` |
| Filter | `db.scalars(select(User).where(User.age > 18)).all()` | `db.query(User).filter(User.age > 18).all()` |
| One/None | `.scalar_one_or_none()` | `.one_or_none()` |
| Count | `db.scalar(select(func.count(User.id)))` | `db.query(User).count()` |
| Columns only | `db.execute(select(User.id, User.email)).all()` → Row tuples | `db.query(User.id, User.email)` |

`db.query()` still works in 2.x (legacy), but new code should use `select()` — it's identical for sync and async.

### Result methods

| Method | Returns |
|---|---|
| `db.execute(stmt)` | `Result` of `Row`s |
| `db.scalars(stmt)` | first column of each row (ORM objects) |
| `.all()` / `.first()` | list / first or None |
| `.one()` | exactly one, else raises |
| `.scalar_one_or_none()` | one object or None, raises if >1 |
| `db.scalar(stmt)` | first column of first row |

---

## 4.7 Joins, Filtering, Aggregation

```python
from sqlalchemy import select, func, and_, or_, desc

# filter combos
stmt = select(Post).where(
    and_(Post.author_id == 7, or_(Post.title.ilike("%fastapi%"), Post.body.contains("async")))
).order_by(desc(Post.created_at))

# IN, NULL, BETWEEN
select(User).where(User.id.in_([1, 2, 3]), User.full_name.is_not(None))
select(Post).where(Post.price.between(10, 50))

# explicit join (uses relationship to infer ON clause)
stmt = select(Post.title, User.email).join(Post.author).where(User.is_active)

# outer join + aggregation: post count per user
stmt = (
    select(User.email, func.count(Post.id).label("post_count"))
    .outerjoin(Post, Post.author_id == User.id)
    .group_by(User.id)
    .having(func.count(Post.id) > 2)
    .order_by(desc("post_count"))
)
for email, post_count in db.execute(stmt):
    print(email, post_count)

# many-to-many filter: posts with tag "python"
stmt = select(Post).join(Post.tags).where(Tag.name == "python")

# EXISTS
stmt = select(User).where(User.posts.any(Post.title.ilike("%sql%")))

# raw SQL when needed (still parameterized!)
from sqlalchemy import text
db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
```

---

## 4.8 Transactions: Commit, Rollback, Flush, Savepoints

| Operation | What happens |
|---|---|
| `db.add(obj)` | Object becomes *pending* (in memory) |
| `db.flush()` | SQL is sent (INSERT/UPDATE) **inside the open transaction**; IDs are generated; not yet permanent |
| `db.commit()` | Flush + `COMMIT` → permanent; starts fresh transaction next time |
| `db.rollback()` | Undo everything since the last commit |
| `db.refresh(obj)` | Reload from DB |
| `db.begin_nested()` | SAVEPOINT — partial rollback inside a transaction |

### Atomic multi-step operation
```python
def transfer(db: Session, from_id: int, to_id: int, amount: Decimal) -> None:
    with db.begin():                                    # commit or rollback automatically
        src = db.get(Account, from_id, with_for_update=True)   # SELECT ... FOR UPDATE (row lock)
        dst = db.get(Account, to_id, with_for_update=True)
        if src.balance < amount:
            raise ValueError("Insufficient funds")      # → automatic rollback
        src.balance -= amount
        dst.balance += amount
```
⚠️ `db.begin()` raises if a transaction is already in progress (autobegin happened earlier, e.g., because you already ran a query). Either structure code so `begin()` is first, or just use explicit `commit()`/`rollback()`.

### Savepoint
```python
for row in rows:
    try:
        with db.begin_nested():          # SAVEPOINT
            db.add(Item(**row))
    except IntegrityError:
        continue                         # only this row rolled back
db.commit()
```

### Concurrency: lost updates
Two requests read `stock=5`, both write `stock=4` → one sale lost. Fixes:
1. **Atomic update in SQL:** `update(Product).where(Product.id == pid, Product.stock > 0).values(stock=Product.stock - 1)` and check `rowcount`.
2. **Pessimistic lock:** `SELECT ... FOR UPDATE` (`with_for_update=True`).
3. **Optimistic lock:** a `version` column — `__mapper_args__ = {"version_id_col": version}` → `StaleDataError` on conflict → return 409.

---

## 4.9 Loading Strategies: Lazy vs Eager (and the N+1 Problem)

**N+1 problem:**
```python
posts = db.scalars(select(Post)).all()       # 1 query
for p in posts:
    print(p.author.email)                    # +1 query PER post (lazy load) → N+1
```

| Strategy | How | SQL | Best for |
|---|---|---|---|
| `lazyload` (default `lazy="select"`) | Load on attribute access | 1 + N | Rarely-accessed relations |
| `joinedload` | LEFT OUTER JOIN in same query | 1 | many-to-one / one-to-one |
| `selectinload` | 2nd query `WHERE id IN (...)` | 2 | one-to-many / many-to-many (collections) |
| `subqueryload` | legacy, prefer selectinload | 2 | — |
| `raiseload` | Raise if lazy-loaded | — | Catch accidental N+1 (great in async) |
| `contains_eager` | Use rows from your explicit join | 1 | When you already joined & filtered |

```python
from sqlalchemy.orm import joinedload, selectinload, raiseload

stmt = (
    select(Post)
    .options(
        joinedload(Post.author),          # many-to-one → join
        selectinload(Post.tags),          # collection → IN query
        raiseload("*"),                   # anything else → error if touched
    )
    .where(Post.author_id == 7)
)
posts = db.scalars(stmt).unique().all()   # .unique() required with joinedload on collections
```

💡 Default per relationship: `relationship(lazy="selectin")` — but explicit `.options()` per query is clearer.

🐞 With **Pydantic response models**, serialization touches every field in the schema — if `PostOut` includes `author`, FastAPI will lazy-load it per post. Always eager-load what the response model needs.

---

## 4.10 Query Optimization Checklist

1. **Index** columns used in `WHERE`, `JOIN`, `ORDER BY` (FKs are *not* auto-indexed in Postgres!).
2. Composite index order matters: `(author_id, created_at)` serves `WHERE author_id=? ORDER BY created_at`.
3. Avoid N+1 — eager load; check with `echo=True` or logs.
4. Select only needed columns for heavy lists: `select(User.id, User.email)` or `load_only()`.
5. Paginate everything; keyset for deep pages.
6. Use bulk `insert()`/`update()` statements for batches instead of looping `add()`.
7. Use `EXPLAIN ANALYZE` on slow queries:
   ```sql
   EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = 7 ORDER BY created_at DESC LIMIT 20;
   ```
   Look for `Seq Scan` on big tables → missing index.
8. Keep transactions short (locks!). Don't call external APIs while a transaction is open.
9. Count is expensive on huge tables — consider estimates or cursor pagination without totals.

---

## 4.11 Async SQLAlchemy

**When to use:** fully async stack (`async def` endpoints) with many concurrent I/O-bound requests. Sync SQLAlchemy in `def` endpoints is **perfectly fine** for most apps — FastAPI runs them in a thread pool.

```bash
$ pip install "sqlalchemy[asyncio]" asyncpg     # or psycopg (v3 supports async)
```

**`app/db_async.py`**
```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://app:app@localhost:5432/app",
    pool_size=10, max_overflow=20, pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)   # expire_on_commit=False is essential


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

@app.get("/users/{user_id}/posts")
async def user_posts(user_id: int, db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = select(User).options(selectinload(User.posts)).where(User.id == user_id)
    user = (await db.execute(stmt)).scalar_one_or_none()
    if not user:
        raise HTTPException(404)
    return [{"id": p.id, "title": p.title} for p in user.posts]


@app.post("/users", status_code=201)
async def create(data: UserCreate, db: Annotated[AsyncSession, Depends(get_async_db)]):
    user = User(email=data.email, hashed_password="...")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id}
```

| Sync | Async |
|---|---|
| `db.execute(stmt)` | `await db.execute(stmt)` |
| `db.get(User, 1)` | `await db.get(User, 1)` |
| `db.commit()` | `await db.commit()` |
| `db.add(x)` | `db.add(x)` (no await — no I/O) |
| lazy loading works | 🐞 **lazy loading raises `MissingGreenlet`** — always eager load, or use `AsyncAttrs` + `await obj.awaitable_attrs.posts` |

Startup/shutdown: `await engine.dispose()` in lifespan (chapter 6).

### Sync vs async — decision table
| Situation | Choice |
|---|---|
| CRUD app, moderate traffic, team new to async | **Sync** session + `def` endpoints |
| Very high concurrency, lots of I/O waiting (DB + HTTP calls) | Async |
| Mixing: async endpoints calling sync SQLAlchemy | ❌ blocks the loop — don't |

---

## 4.12 SQLAlchemy vs SQLModel vs Others

| Tool | What | Pros | Cons |
|---|---|---|---|
| **SQLAlchemy 2.x** | The standard Python ORM + Core | Most powerful, mature, any complexity | Separate Pydantic schemas (more code) |
| **SQLModel** | By FastAPI's author; one class = SQLAlchemy model + Pydantic model | Less duplication, great for small/medium apps | Thinner abstraction, lags SQLAlchemy features; mixing DB & API schema can leak fields |
| Tortoise ORM | Async-first, Django-like | Simple async | Smaller ecosystem |
| Django ORM | Inside Django | Batteries | Not natural in FastAPI |
| Peewee / Pony | Lightweight ORMs | Small | Less common in FastAPI |
| Raw SQL (`asyncpg`, `psycopg`) | No ORM | Max control/performance | More code, manual mapping |
| Query builders (SQLAlchemy Core) | SQL in Python, no objects | Explicit | No unit of work |

SQLModel example:
```python
from sqlmodel import Field, SQLModel

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = None

class Hero(HeroBase, table=True):        # table=True → DB table
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

class HeroPublic(HeroBase):              # API output (no secret_name)
    id: int
```

🎤 *"I default to SQLAlchemy 2.x with typed `Mapped` columns and separate Pydantic schemas — the API contract and the storage model evolve independently. SQLModel reduces boilerplate for smaller services but I still keep separate read/write models to avoid leaking fields."*

---

## ✅ Quick Revision — Chapter 4

- Engine = pool (one per app); Session = unit of work (one per request) via `yield` dependency.
- Models: `class Base(DeclarativeBase)`, `Mapped[...]`, `mapped_column(...)`, `relationship(back_populates=...)`.
- Queries: `select()` + `db.scalars()` / `db.execute()`; `db.get()` for PK.
- `add → flush → commit`; `rollback()` after errors; `refresh()` for DB defaults.
- Prevent N+1: `joinedload` for to-one, `selectinload` for collections, `raiseload` to catch mistakes.
- Index FKs and filter/sort columns; check with `EXPLAIN ANALYZE`.
- Concurrency: atomic `UPDATE`, `FOR UPDATE`, or optimistic `version_id_col`.
- Async: `create_async_engine`, `async_sessionmaker(expire_on_commit=False)`, no lazy loading.
- Never `create_all` in production — use Alembic.
