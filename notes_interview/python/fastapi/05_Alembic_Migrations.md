# Chapter 5 — Database Migrations with Alembic

> **Goal:** Evolve your database schema safely — from your laptop to production — with versioned, reviewable, reversible migrations.

---

## 5.1 What Are Migrations and Why Do You Need Them?

**Simple English:** Your code changes over time ("add a `phone` column"). The database must change too — on every developer's machine, CI, staging and production — *in the same order*. A **migration** is a small versioned script that says "how to go from schema version A to B" (`upgrade`) and back (`downgrade`).

Without migrations:
- `Base.metadata.create_all()` creates tables but **never alters** existing ones.
- Manual `ALTER TABLE` in prod = forgotten steps, drift, no history.

With **Alembic** (made by SQLAlchemy's author):
- Each migration is a Python file with a unique **revision id** and a pointer to its parent (`down_revision`) → a linked list / graph.
- The DB stores its current version in a table `alembic_version`.
- `alembic upgrade head` brings any DB to the latest version.

```
base ──► a1b2 (create users) ──► c3d4 (add posts) ──► e5f6 (add users.phone) ◄── head
                                                       ▲
                                    alembic_version table says: "e5f6"
```

---

## 5.2 Install and Initialize

```bash
(.venv) $ pip install alembic
(.venv) $ alembic init alembic                 # sync template
# or for async engines:
(.venv) $ alembic init -t async alembic
```

Generated:
```
project/
├── alembic.ini              # config (script location, logging, DB URL placeholder)
└── alembic/
    ├── env.py               # ★ connects Alembic to your models & DB
    ├── script.py.mako       # template for new migration files
    └── versions/            # migration files live here
```

---

## 5.3 Connect Alembic to Your SQLAlchemy Models

### Step 1 — naming convention on `Base` (do this on day 1!)
```python
# app/db.py
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
```
Why: constraints get deterministic names → Alembic can drop/alter them later. Without names, Postgres invents names and future migrations break.

### Step 2 — edit `alembic/env.py`
```python
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import settings          # reads DATABASE_URL from env (chapter 6)
from app.db import Base
import app.models  # noqa: F401   ★ import ALL models so they register on Base.metadata

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)   # don't hardcode secrets in alembic.ini

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata          # ★ what autogenerate compares against


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,               # detect column type changes
            compare_server_default=True,     # detect server_default changes
            render_as_batch=connection.dialect.name == "sqlite",   # SQLite ALTER support
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

🐞 If you use `%` in the URL (URL-encoded password), escape it for configparser: `settings.database_url.replace("%", "%%")`.

### Step 3 (optional) — nicer filenames in `alembic.ini`
```ini
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```

---

## 5.4 Initial Migration

```bash
(.venv) $ alembic revision --autogenerate -m "create users and posts"
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added table 'posts'
  Generating .../alembic/versions/2026_10_25_1000-a1b2c3d4e5f6_create_users_and_posts.py ...  done
```

Generated file:
```python
"""create users and posts

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-10-25 10:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = None              # first migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    # ... posts table


def downgrade() -> None:
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
```

Apply:
```bash
(.venv) $ alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade  -> a1b2c3d4e5f6, create users and posts
```

---

## 5.5 Day-to-day Workflow

```
1. Edit models.py          (add column/table/index)
2. alembic revision --autogenerate -m "describe change"
3. ★ REVIEW the generated file (autogenerate is not perfect)
4. alembic upgrade head    (local DB)
5. Test downgrade:  alembic downgrade -1  &&  alembic upgrade head
6. Commit model change + migration file together in the same PR
```

### Command reference

| Command | Purpose |
|---|---|
| `alembic revision -m "msg"` | Empty migration (manual / data migration) |
| `alembic revision --autogenerate -m "msg"` | Generate from model diff |
| `alembic upgrade head` | Apply all pending |
| `alembic upgrade +1` / `alembic upgrade <rev>` | One step / to a specific revision |
| `alembic downgrade -1` | Undo last |
| `alembic downgrade <rev>` / `base` | Back to revision / empty DB |
| `alembic current` | Revision the DB is at |
| `alembic history --verbose` | All revisions |
| `alembic heads` | Current head(s) — >1 means branches |
| `alembic show <rev>` | Details of one revision |
| `alembic upgrade head --sql > migrate.sql` | **Offline mode**: print SQL for DBA review instead of running |
| `alembic stamp head` | Mark DB as at `head` *without running* (adopting an existing DB) |
| `alembic merge -m "merge" <rev1> <rev2>` | Merge two heads |
| `alembic check` | Fail if models have changes not in migrations (great for CI) |

---

## 5.6 What Autogenerate Detects (and Misses)

| Detects ✅ | Misses / unreliable ⚠️ |
|---|---|
| Added/removed tables | **Renamed tables/columns** (sees drop + add → DATA LOSS) |
| Added/removed columns | Changes to anonymous (unnamed) constraints |
| Nullable changes | Some type changes (needs `compare_type=True`, enabled by default in 1.12+) |
| Indexes, unique constraints, FKs (named) | Enum value changes (Postgres) |
| Server defaults (with flag) | Check constraints (often), triggers, views, sequences, functions |
| | Data migrations (it never moves data) |

**Rule: always read the generated migration before applying it.**

---

## 5.7 Common Schema Changes — Practical Examples

### Add a nullable column (safe)
```python
def upgrade():
    op.add_column("users", sa.Column("phone", sa.String(20), nullable=True))

def downgrade():
    op.drop_column("users", "phone")
```

### Add a NOT NULL column to a table with data
❌ `op.add_column("users", sa.Column("status", sa.String(20), nullable=False))` → fails: existing rows have NULL.

✅ Option A — server default:
```python
op.add_column("users", sa.Column("status", sa.String(20), nullable=False, server_default="active"))
```
✅ Option B — three steps (big tables / computed values):
```python
def upgrade():
    op.add_column("users", sa.Column("status", sa.String(20), nullable=True))
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")   # backfill (batch if huge)
    op.alter_column("users", "status", nullable=False)
```

### Rename a column (edit autogenerate output!)
Autogenerate produces `drop_column("name") + add_column("full_name")` — **deletes data**. Replace with:
```python
def upgrade():
    op.alter_column("users", "name", new_column_name="full_name")

def downgrade():
    op.alter_column("users", "full_name", new_column_name="name")
```
Rename table: `op.rename_table("old", "new")`.

### Add an index (Postgres, no table lock)
```python
def upgrade():
    with op.get_context().autocommit_block():          # CONCURRENTLY can't run in a transaction
        op.create_index("ix_posts_created_at", "posts", ["created_at"],
                        postgresql_concurrently=True, if_not_exists=True)

def downgrade():
    with op.get_context().autocommit_block():
        op.drop_index("ix_posts_created_at", table_name="posts", postgresql_concurrently=True)
```

### Add constraints
```python
op.create_unique_constraint("uq_users_phone", "users", ["phone"])
op.create_foreign_key("fk_posts_category_id_categories", "posts", "categories",
                      ["category_id"], ["id"], ondelete="SET NULL")
op.create_check_constraint("ck_products_price_positive", "products", "price > 0")
op.drop_constraint("uq_users_phone", "users", type_="unique")
```

### Change a column type
```python
op.alter_column("products", "price",
                type_=sa.Numeric(12, 2), existing_type=sa.Numeric(10, 2),
                postgresql_using="price::numeric(12,2)")
```

### Data migration (separate revision, no ORM models!)
```python
from sqlalchemy.sql import table, column

def upgrade():
    users = table("users", column("id", sa.Integer), column("email", sa.String))
    op.execute(users.update().values(email=sa.func.lower(users.c.email)))
```
⚠️ Never import your app's ORM models in migrations — the models change in the future, but the migration must keep working against the schema *as it was at that revision*. Use lightweight `table()/column()` or raw SQL.

### Postgres enum add value
```python
def upgrade():
    op.execute("ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'refunded'")
```
(💡 Many teams store enums as `VARCHAR + CHECK` to avoid enum migration pain.)

### SQLite limitations
SQLite can't `ALTER COLUMN`/drop constraints → use batch mode (enabled via `render_as_batch=True`):
```python
with op.batch_alter_table("users") as batch:
    batch.alter_column("email", nullable=False)
```

---

## 5.8 Multiple Environments (dev → staging → prod)

- **Same migration files** everywhere; **different `DATABASE_URL`** via environment variables.
  ```powershell
  PS> $env:DATABASE_URL = "postgresql+psycopg://user:pw@staging-db/app"; alembic upgrade head
  ```
  ```bash
  $ DATABASE_URL=postgresql+psycopg://user:pw@staging-db/app alembic upgrade head
  ```
- Pipeline: **CI** spins up an empty Postgres → `alembic upgrade head` → tests → `alembic check` → (optionally `downgrade base` to test reversibility).
- **Staging** gets the migration first with production-like data volume.
- **Production** runs migrations as a **separate step/job** before (or during) the rolling deploy — *not* on every app container startup (N containers racing to migrate).
- Keep `alembic_version` in sync: never edit a migration that has run in a shared environment — create a new one.

### Team branching: "multiple heads"
Two developers both create a migration from revision `c3d4`:
```bash
$ alembic heads
e5f6 (head)
f7a8 (head)
$ alembic merge -m "merge heads" e5f6 f7a8
$ alembic upgrade head
```
CI check: `test $(alembic heads | wc -l) -eq 1`.

---

## 5.9 Safe Production Migration Practices (zero-downtime)

**Expand → Migrate → Contract** (aka parallel change):

| Phase | Example: rename `name` → `full_name` |
|---|---|
| 1. **Expand** (deploy N) | Add `full_name` (nullable). App writes **both** columns, reads old. |
| 2. **Migrate** | Backfill `full_name` from `name` in batches. |
| 3. Switch (deploy N+1) | App reads/writes `full_name` only. |
| 4. **Contract** (deploy N+2) | Drop `name` once no running version uses it. |

Why: during a rolling deploy, old and new app versions run simultaneously against one DB — every migration must be compatible with both.

Checklist:
- ✅ Additive changes first; destructive later.
- ✅ Indexes on big tables: `CONCURRENTLY`.
- ✅ Set `lock_timeout` / `statement_timeout` so a migration fails fast instead of blocking traffic:
  `op.execute("SET lock_timeout = '5s'")`
- ✅ Backfill large tables in batches (separate script/job), not one giant `UPDATE`.
- ✅ Backup / snapshot before risky migrations; know your restore time.
- ✅ Review SQL with `alembic upgrade head --sql`.
- ⚠️ `downgrade` of destructive changes can't restore data — rollback plan is often "roll forward with a fix".
- ⚠️ Avoid `NOT NULL` without default on large tables; avoid changing column types on huge tables in one step.

---

## 5.10 🐞 Common Migration Errors

| Error | Cause | Fix |
|---|---|---|
| Autogenerate creates **empty** migration | Models not imported in `env.py` / wrong `target_metadata` | `import app.models` in env.py; `target_metadata = Base.metadata` |
| `Target database is not up to date` | Pending migrations not applied | `alembic upgrade head` before generating |
| `Can't locate revision identified by 'xxxx'` | DB `alembic_version` refers to a deleted/unknown file | Restore file, or `alembic stamp <known_rev>` carefully |
| `Multiple head revisions are present` | Parallel branches | `alembic merge heads` |
| `relation "users" already exists` | Tables made by `create_all` then migration tries again | Drop & re-run, or `alembic stamp head` on that DB |
| `column ... contains null values` | Adding NOT NULL to populated table | server_default or 3-step backfill |
| Constraint can't be dropped (`None` name) | No naming convention | Add convention; name explicitly in migration |
| SQLite `No support for ALTER of constraints` | SQLite limits | `render_as_batch=True` |
| `ModuleNotFoundError: app` when running alembic | Project root not on path | Run from root; `prepend_sys_path = .` in alembic.ini |
| Migration hangs in prod | Waiting on table lock behind long transaction | `lock_timeout`, run in low traffic, `CONCURRENTLY` |

---

## ✅ Quick Revision — Chapter 5

```bash
alembic init alembic                               # once
alembic revision --autogenerate -m "msg"           # create
alembic upgrade head                               # apply
alembic downgrade -1                               # undo one
alembic current / history / heads                  # inspect
alembic upgrade head --sql                         # SQL preview
alembic stamp head                                 # adopt existing DB
alembic merge heads -m "merge"                     # fix branches
alembic check                                      # CI drift detection
```
- `env.py`: import all models, `target_metadata = Base.metadata`, URL from env.
- Naming convention on `MetaData` from day one.
- Always review autogenerate (renames = drop+add!).
- No ORM models inside migrations.
- Zero downtime: expand → migrate → contract; `CONCURRENTLY`; `lock_timeout`; batch backfills.
- Run migrations as one deploy step, not in every container.

🎤 *"Alembic versions the schema as a chain of revisions stored in `alembic_version`. I autogenerate from SQLAlchemy metadata but always review the file — renames and data moves need manual edits. In production I use expand-and-contract so old and new app versions both work during a rolling deploy, create indexes concurrently, and run migrations as a dedicated pipeline step."*
