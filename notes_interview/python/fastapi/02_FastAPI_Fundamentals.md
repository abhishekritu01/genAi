# Chapter 2 — FastAPI Fundamentals

> **Goal:** Understand what FastAPI is, how it works under the hood, and master every way a request can send data (path, query, body, headers, cookies) and every way you can shape a response.

---

## 2.1 What Is FastAPI and Why Use It?

**Simple English:** FastAPI is a Python toolkit for building web APIs. You write normal Python functions with **type hints**, and FastAPI automatically:
1. reads and **validates** incoming data,
2. converts it into Python objects,
3. converts your return value into **JSON**,
4. generates **interactive documentation**.

**Why teams pick it**
- **Fast to run** — built on ASGI (async), among the fastest Python frameworks.
- **Fast to write** — type hints replace manual parsing/validation code.
- **Fewer bugs** — invalid input is rejected with a clear 422 error before your code runs.
- **Standards-based** — OpenAPI + JSON Schema → auto docs, client generation.
- **Great editor support** — autocomplete everywhere because everything is typed.

### Comparison: FastAPI vs Flask vs Django REST Framework

| Aspect | FastAPI | Flask | Django REST Framework (DRF) |
|---|---|---|---|
| Interface | ASGI (async native) | WSGI (sync; async views bolted on) | WSGI (Django ≥ 3.1 has partial ASGI) |
| Validation | Built-in via Pydantic + type hints | Manual / extensions (marshmallow) | Serializers |
| Auto API docs | ✅ Swagger + ReDoc built in | ❌ (extensions) | Partial (drf-spectacular) |
| ORM | Bring your own (SQLAlchemy, SQLModel) | Bring your own | Django ORM built in |
| Admin panel, auth, batteries | ❌ minimal core | ❌ minimal | ✅ lots built in |
| Performance | High | Medium | Medium/Lower |
| Learning curve | Low–medium (needs type hints, async) | Lowest | Higher (Django concepts) |
| Best for | APIs, microservices, ML/AI serving, high concurrency I/O | Small apps, simple services | Large data-heavy apps needing admin, ORM, auth out of the box |

🎤 *"FastAPI is an ASGI framework built on Starlette and Pydantic. It uses Python type hints to validate requests, serialize responses, and generate OpenAPI docs automatically. Compared with Flask it's async-native and validation is built in; compared with DRF it's lighter and faster but you assemble the ORM, auth and admin yourself."*

---

## 2.2 How FastAPI Works Internally

```
HTTP request bytes
      │
      ▼
┌────────────┐  parses HTTP, manages connections, event loop
│  Uvicorn   │  (ASGI SERVER)
└─────┬──────┘
      │ calls app(scope, receive, send)   ← the ASGI interface
      ▼
┌────────────┐  routing, middleware, Request/Response objects,
│ Starlette  │  WebSockets, background tasks, static files
└─────┬──────┘
      ▼
┌────────────┐  resolves dependencies (Depends), reads params from path/query/body,
│  FastAPI   │  validates with Pydantic, calls your function, validates/serializes
└─────┬──────┘  the return value, builds OpenAPI schema
      ▼
┌────────────┐
│  Pydantic  │  type coercion + validation + JSON serialization (Rust core in v2)
└────────────┘
```

| Term | Plain meaning |
|---|---|
| **WSGI** | Old Python web standard: one request = one blocking call. Flask, Django. |
| **ASGI** | Async successor: an app is `async def app(scope, receive, send)`. Supports long-lived connections (WebSockets), concurrency via `asyncio`. |
| **Uvicorn** | The ASGI *server* (like Gunicorn for WSGI). Speaks HTTP, calls your app. Alternatives: Hypercorn, Granian. |
| **Starlette** | Lightweight ASGI *toolkit*. `FastAPI` class literally subclasses `Starlette`. |
| **Pydantic** | Validation library. Turns `{"age": "5"}` into `age=5` (int) or raises a clear error. |
| **OpenAPI** | A JSON spec describing your API; Swagger UI / ReDoc render it. |

### Request lifecycle inside FastAPI
1. Uvicorn receives bytes → builds ASGI `scope`.
2. Starlette middleware stack runs (outermost first).
3. Router matches path + method → the route.
4. FastAPI solves the **dependency graph** (`Depends`), extracting path/query/header/cookie/body values.
5. Pydantic validates them → if invalid, return **422** immediately.
6. Your function runs (`async def` on the event loop; `def` in a thread pool).
7. Return value validated/filtered via `response_model`, serialized to JSON.
8. Response passes back out through middleware → Uvicorn → client.
9. Background tasks run *after* the response is sent; `yield` dependencies clean up.

---

## 2.3 First Application, Explained

**`main.py`**
```python
from fastapi import FastAPI

app = FastAPI(
    title="Bookstore API",
    description="Learning FastAPI step by step",
    version="1.0.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/books/{book_id}")
async def get_book(book_id: int, include_reviews: bool = False):
    return {"book_id": book_id, "include_reviews": include_reviews}
```

Run `fastapi dev main.py`, then:

```bash
$ curl "http://127.0.0.1:8000/books/42?include_reviews=true"
{"book_id":42,"include_reviews":true}

$ curl "http://127.0.0.1:8000/books/abc"
{"detail":[{"type":"int_parsing","loc":["path","book_id"],
  "msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
# HTTP 422 Unprocessable Content
```

You never wrote validation code — the type hint `book_id: int` did it.

---

## 2.4 Path Operations, Routes, HTTP Methods

- **Path** = URL part after the domain: `/books/42`.
- **Operation** = HTTP method: GET, POST, PUT, PATCH, DELETE (also HEAD, OPTIONS).
- **Path operation** = path + method → `@app.get("/books/{id}")`.
- **Path operation function** = the Python function that handles it.

| Method | Purpose | Safe? (no change) | Idempotent? (repeat = same result) | Has body? |
|---|---|---|---|---|
| GET | Read | ✅ | ✅ | No |
| POST | Create / action | ❌ | ❌ | Yes |
| PUT | Replace whole resource | ❌ | ✅ | Yes |
| PATCH | Partial update | ❌ | ❌ (usually, by spec) | Yes |
| DELETE | Remove | ❌ | ✅ | Usually no |
| HEAD | GET without body | ✅ | ✅ | No |
| OPTIONS | Capabilities / CORS preflight | ✅ | ✅ | No |

### 🐞 Route order matters
```python
@app.get("/users/me")          # ✅ declare the fixed path FIRST
async def read_me(): ...

@app.get("/users/{user_id}")   # otherwise "me" would be matched here as user_id
async def read_user(user_id: int): ...
```

### Status codes you must know

| Code | Name | When |
|---|---|---|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST that created something |
| 202 | Accepted | Work queued, not done yet |
| 204 | No Content | Successful DELETE (no body) |
| 301/302/307/308 | Redirects | Moved resources |
| 304 | Not Modified | Cache validation (ETag) |
| 400 | Bad Request | Generic client error / business-rule violation |
| 401 | Unauthorized | **Not authenticated** (missing/invalid credentials) |
| 403 | Forbidden | **Authenticated but not allowed** |
| 404 | Not Found | Resource doesn't exist (or hide existence) |
| 405 | Method Not Allowed | Wrong verb |
| 409 | Conflict | Duplicate email, version conflict |
| 412 | Precondition Failed | `If-Match` ETag mismatch |
| 415 | Unsupported Media Type | Wrong `Content-Type` |
| 422 | Unprocessable Content | Validation failed (FastAPI default) |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Bug |
| 502/503/504 | Bad Gateway / Unavailable / Gateway Timeout | Upstream or overload problems |

```python
from fastapi import status

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(...): ...
```

---

## 2.5 Path Parameters

```python
from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()


class Genre(str, Enum):           # restricts allowed values; shows dropdown in Swagger
    fiction = "fiction"
    science = "science"


@app.get("/genres/{genre}")
async def by_genre(genre: Genre):
    return {"genre": genre, "value": genre.value}


@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[int, Path(title="Item ID", ge=1, le=1_000_000)],
):
    return {"item_id": item_id}


@app.get("/files/{file_path:path}")   # ":path" lets the param contain slashes
async def read_file(file_path: str):
    return {"file_path": file_path}
```

- Path params are **always required**.
- `ge`, `gt`, `le`, `lt` = numeric constraints; `min_length`, `max_length`, `pattern` for strings.

---

## 2.6 Query Parameters

Any function parameter that is **not** in the path and is a simple type → query parameter.

```python
from typing import Annotated
from fastapi import Query

@app.get("/books")
async def list_books(
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,   # optional
    skip: Annotated[int, Query(ge=0)] = 0,                                 # default
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    tags: Annotated[list[str], Query()] = [],     # ?tags=a&tags=b   (list needs Query())
    in_stock: bool = True,                        # ?in_stock=false / 0 / no / off
    sort: Annotated[str, Query(alias="sort-by", pattern="^(title|price)$")] = "title",
):
    return {"q": q, "skip": skip, "limit": limit, "tags": tags, "sort": sort}
```

| Declaration | Meaning |
|---|---|
| `x: int` | **required** query param |
| `x: int = 10` | optional with default |
| `x: int \| None = None` | optional, may be absent |
| `Annotated[..., Query(deprecated=True)]` | marked deprecated in docs |
| `Query(include_in_schema=False)` | hidden from docs |

💡 **Query parameter models (FastAPI ≥ 0.115)** — group many params into one Pydantic model:
```python
from pydantic import BaseModel, Field

class BookFilters(BaseModel):
    model_config = {"extra": "forbid"}          # reject unknown query params
    q: str | None = None
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)

@app.get("/books/search")
async def search(filters: Annotated[BookFilters, Query()]):
    return filters
```

### `Annotated` — the modern style
⚠️ Old style: `q: str = Query(None, min_length=2)`. Still works, but **recommended** style is `Annotated[str | None, Query(min_length=2)] = None` because the default stays a real Python default and the function can be called normally (e.g., in tests).

---

## 2.7 Request Body (Pydantic Models)

**Simple English:** For POST/PUT/PATCH, the client sends JSON in the body. You describe its shape with a Pydantic class; FastAPI parses and validates it.

```python
from pydantic import BaseModel, Field, EmailStr

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str
    price: float = Field(gt=0, description="Price in USD")
    tags: list[str] = []
    isbn: str | None = Field(default=None, pattern=r"^\d{13}$")


@app.post("/books", status_code=201)
async def create_book(book: BookCreate):
    # book is a validated BookCreate instance
    data = book.model_dump()          # -> dict   (v1: .dict()  ⚠️ deprecated)
    return {"id": 1, **data}
```

Request / response:
```http
POST /books
Content-Type: application/json

{"title": "Dune", "author": "Frank Herbert", "price": 9.99}
```
```json
{"id": 1, "title": "Dune", "author": "Frank Herbert", "price": 9.99, "tags": [], "isbn": null}
```

How FastAPI decides where a parameter comes from:

| Parameter declared as | Read from |
|---|---|
| Name appears in path `{x}` | Path |
| Simple type (int, str, bool, float, enum, list w/ Query) | Query |
| Pydantic model | Body (JSON) |
| `Annotated[..., Header()]` / `Cookie()` / `Form()` / `File()` | Header / Cookie / form / multipart |
| `Request`, `Response`, `BackgroundTasks`, `WebSocket` | Injected by framework |

Mix them freely:
```python
from fastapi import Body

@app.put("/books/{book_id}")
async def update_book(
    book_id: int,                                  # path
    book: BookCreate,                              # body
    notify: bool = False,                          # query
    note: Annotated[str | None, Body()] = None,    # extra body key
):
    ...
# Two body params → body becomes {"book": {...}, "note": "..."}
# Single model + Body(embed=True) → {"book": {...}} instead of the bare object
```

---

## 2.8 Headers and Cookies

```python
from fastapi import Header, Cookie

@app.get("/whoami")
async def whoami(
    user_agent: Annotated[str | None, Header()] = None,     # reads "User-Agent" (underscore → hyphen)
    x_request_id: Annotated[str | None, Header()] = None,   # reads "X-Request-Id"
    session_id: Annotated[str | None, Cookie()] = None,
):
    return {"ua": user_agent, "rid": x_request_id, "session": session_id}
```

Setting response headers/cookies:
```python
from fastapi import Response

@app.post("/login")
async def login(response: Response):
    response.set_cookie(
        key="session_id", value="abc123",
        httponly=True, secure=True, samesite="lax", max_age=3600,
    )
    response.headers["X-App-Version"] = "1.0"
    return {"ok": True}
```

---

## 2.9 Response Models and Serialization

**Why:** You often store more than you should return (e.g., `hashed_password`). `response_model` **filters and validates** the output and documents it.

```python
class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

class UserInDB(UserOut):
    hashed_password: str


@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    db_user = UserInDB(id=1, email=user.email, hashed_password="x$hash")
    return db_user                    # hashed_password is stripped by response_model
```

Modern alternative — the **return type annotation** acts as response model:
```python
@app.post("/users", status_code=201)
async def create_user(user: UserIn) -> UserOut:
    ...
```
Use `response_model=` when the actual returned object differs from the declared type (e.g., you return an ORM object or a dict) to keep type-checkers happy.

| Option | Effect |
|---|---|
| `response_model_exclude_unset=True` | Omit fields never set (great for PATCH-style responses) |
| `response_model_exclude_none=True` | Omit `null` fields |
| `response_model_include={"id"}` / `exclude={...}` | Quick filter (prefer separate models) |
| `response_model=None` | Disable validation (returning a raw `Response`) |

### Reading from ORM objects
```python
from pydantic import ConfigDict

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # v1: orm_mode = True ⚠️
    id: int
    title: str
```

### Pydantic v1 → v2 quick map (⚠️ old names)

| v1 (deprecated) | v2 |
|---|---|
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `parse_obj()` | `model_validate()` |
| `class Config: orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `BaseSettings` from pydantic | `pydantic_settings.BaseSettings` |

### Validators
```python
from pydantic import field_validator, model_validator

class SignUp(BaseModel):
    username: str
    password: str
    confirm: str

    @field_validator("username")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("username must not contain spaces")
        return v.lower()

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm:
            raise ValueError("passwords do not match")
        return self
```

---

## 2.10 Response Types

| Class | Use |
|---|---|
| `JSONResponse` (default) | JSON |
| `HTMLResponse` | HTML pages |
| `PlainTextResponse` | Plain text |
| `RedirectResponse` | Redirects (307 by default) |
| `FileResponse` | Send a file from disk (streams it) |
| `StreamingResponse` | Generator/iterator body (large data, SSE, LLM tokens) |
| `Response` | Raw bytes with your own media type |

```python
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

@app.get("/page", response_class=HTMLResponse)
async def page():
    return "<h1>Hello</h1>"

@app.get("/old")
async def old():
    return RedirectResponse("/new", status_code=301)

@app.get("/custom")
async def custom():
    return JSONResponse(status_code=202, content={"queued": True}, headers={"X-Job": "7"})
```

⚠️ When you return a `Response` object directly, FastAPI **skips** `response_model` validation and `jsonable_encoder` — you're responsible for the content.

---

## 2.11 Automatic Docs: Swagger UI & ReDoc

- **`/docs`** — Swagger UI: click an endpoint → **Try it out** → fill params → **Execute** → see curl, request URL, response body/status/headers.
- **`/redoc`** — ReDoc: clean, read-only reference docs.
- **`/openapi.json`** — the raw spec; generate typed clients (`openapi-generator`, `openapi-typescript`).

Enrich the docs:
```python
@app.post(
    "/books",
    tags=["books"],                      # groups endpoints
    summary="Create a book",
    response_description="The created book",
    responses={409: {"description": "ISBN already exists"}},
)
async def create_book(book: BookCreate):
    """
    Create a book.

    - **title**: required
    - **price**: must be > 0
    """
```

Examples shown in Swagger:
```python
class BookCreate(BaseModel):
    model_config = {"json_schema_extra": {"examples": [{"title": "Dune", "author": "Herbert", "price": 9.99}]}}
```

Disable in production if the API is private:
```python
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
```

---

## 2.12 Sync vs Async Endpoints (`def` vs `async def`)

**Simple English:**
- `async def` runs **on the event loop** (one thread juggling many requests). While it `await`s I/O, other requests proceed.
- `def` is run by FastAPI **in a thread pool** (default ~40 threads via AnyIO), so blocking code doesn't freeze the loop.

| You call... | Use | Why |
|---|---|---|
| Async libraries (`httpx.AsyncClient`, `asyncpg`, SQLAlchemy async, `redis.asyncio`) | `async def` | Non-blocking, most scalable |
| Blocking libraries (`requests`, sync SQLAlchemy, `time.sleep`, boto3, file I/O) | `def` | FastAPI offloads to a thread |
| Pure CPU work, tiny | either | negligible |
| Heavy CPU (image processing, ML inference) | `def` **or** process pool / task queue | Threads don't escape the GIL; offload to a worker |

### 🐞 The #1 FastAPI performance bug
```python
import time, requests

@app.get("/bad")
async def bad():
    time.sleep(2)                       # ❌ blocks the ENTIRE event loop
    requests.get("https://example.com") # ❌ blocking I/O inside async def
    return {}

@app.get("/good-sync")
def good_sync():                        # ✅ runs in threadpool
    time.sleep(2)
    return {}

@app.get("/good-async")
async def good_async():
    import asyncio, httpx
    await asyncio.sleep(2)              # ✅ yields to the loop
    async with httpx.AsyncClient() as c:
        await c.get("https://example.com")
    return {}
```
With `/bad`, 10 concurrent requests take ~20 s; with `/good-async`, ~2 s.

Calling blocking code from async code:
```python
from starlette.concurrency import run_in_threadpool
# or: import anyio; await anyio.to_thread.run_sync(fn, arg)
# or: await asyncio.to_thread(fn, arg)

@app.get("/report")
async def report():
    data = await run_in_threadpool(generate_pdf_blocking, 42)
    return data
```

🎤 *"Use `async def` only when everything inside is non-blocking and awaited. If you use a blocking library, declare the endpoint with plain `def` and FastAPI runs it in a thread pool. Blocking inside `async def` stalls every request on that worker."*

---

## 2.13 `jsonable_encoder`, `Request` object, misc

```python
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from datetime import datetime

@app.get("/debug")
async def debug(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host if request.client else None,
        "headers": dict(request.headers),
        "now": jsonable_encoder(datetime.now()),   # -> ISO string
    }
```
`jsonable_encoder` converts datetimes, UUIDs, Decimals, Pydantic models etc. into JSON-safe types — useful before storing in a JSON column or cache.

---

## ✅ Quick Revision — Chapter 2

| Concept | One-liner |
|---|---|
| FastAPI stack | Uvicorn (server) → Starlette (web toolkit) → FastAPI (DI, validation, docs) → Pydantic |
| ASGI vs WSGI | Async callable `(scope, receive, send)` vs blocking call per request |
| Path param | `{id}` in URL, always required |
| Query param | non-path simple type; optional if it has a default |
| Body | Pydantic model param |
| Header/Cookie | `Annotated[str, Header()]` / `Cookie()` |
| Validation error | automatic **422** with `detail` list |
| `response_model` | filters, validates, documents output |
| `from_attributes=True` | read ORM objects into Pydantic |
| `def` vs `async def` | threadpool vs event loop — never block in `async def` |
| Docs | `/docs`, `/redoc`, `/openapi.json` |

**Key takeaways**
1. Type hints *are* the API contract.
2. Separate input (`XCreate`), output (`XOut`) and storage (`XInDB`) models.
3. Use `Annotated[...]` style and Pydantic v2 APIs.
4. Blocking call inside `async def` = production outage.
