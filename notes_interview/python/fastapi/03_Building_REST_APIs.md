# Chapter 3 — Building REST APIs

> **Goal:** Design clean REST APIs and implement full CRUD with validation, pagination, filtering, consistent errors, versioning, files, and CORS.

---

## 3.1 REST Principles (in plain English)

**REST** = a style for designing APIs around **resources** (nouns) manipulated with **HTTP methods** (verbs).

| Principle | Meaning | Example |
|---|---|---|
| Resources & URIs | Each thing has a URL | `/users/7`, `/users/7/orders` |
| Uniform interface | Standard verbs + status codes | `DELETE /users/7` → 204 |
| Stateless | Each request carries everything needed (token); server keeps no session memory between requests | `Authorization: Bearer ...` |
| Representations | Resource is sent as JSON (or other media types) | `Content-Type: application/json` |
| Cacheable | Responses say if they can be cached | `Cache-Control`, `ETag` |
| Layered system | Client doesn't know if it hits a proxy, gateway, or app | CDN, LB |

### URL design best practices

| ✅ Do | ❌ Don't |
|---|---|
| `GET /books` | `GET /getAllBooks` |
| `POST /books` | `POST /books/create` |
| `GET /books/42` | `GET /book?id=42` |
| `GET /authors/3/books` (nested, max ~2 levels) | `/authors/3/books/9/reviews/2/likes` |
| plural nouns, lowercase, kebab-case: `/order-items` | `/OrderItems`, `/order_items` mixed |
| actions as sub-resources when needed: `POST /orders/9/cancel` | `GET /cancelOrder?id=9` (GET must not change state) |
| filter via query: `GET /books?author=herbert&sort=-price` | `/books/by-author/herbert/sorted-desc` |

---

## 3.2 Schema Design with Pydantic (Create / Update / Read)

```python
# schemas.py
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: Priority = Priority.medium
    done: bool = False


class TaskCreate(TaskBase):
    """Input for POST — client never sends id/created_at."""


class TaskReplace(TaskBase):
    """Input for PUT — full replacement, all fields required semantics (defaults allowed)."""


class TaskUpdate(BaseModel):
    """Input for PATCH — every field optional."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: Priority | None = None
    done: bool | None = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
```

Why separate models?
- **Security:** clients can't set `id`, `owner_id`, `is_admin`.
- **Clarity:** docs show exactly what each endpoint needs.
- **PATCH correctness:** all-optional model + `exclude_unset=True`.

### Nested models
```python
class Address(BaseModel):
    city: str
    zip: str = Field(pattern=r"^\d{5,6}$")

class Customer(BaseModel):
    name: str
    addresses: list[Address] = []
    metadata: dict[str, str] = {}
```
💡 Mutable defaults (`[]`, `{}`) are **safe in Pydantic** — it copies them per instance (unlike plain Python functions). `Field(default_factory=list)` is also fine.

---

## 3.3 Full CRUD (in-memory, runnable)

**`main.py`**
```python
from datetime import datetime, timezone
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, status, Response
from schemas import TaskCreate, TaskOut, TaskReplace, TaskUpdate, Priority

app = FastAPI(title="Tasks API")

_db: dict[int, dict] = {}
_next_id = 1


def _get_or_404(task_id: int) -> dict:
    task = _db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, response: Response):
    global _next_id
    task = {"id": _next_id, "created_at": datetime.now(timezone.utc), **payload.model_dump()}
    _db[_next_id] = task
    response.headers["Location"] = f"/tasks/{_next_id}"   # REST nicety for 201
    _next_id += 1
    return task


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(
    done: bool | None = None,
    priority: Priority | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items = list(_db.values())
    if done is not None:
        items = [t for t in items if t["done"] == done]
    if priority is not None:
        items = [t for t in items if t["priority"] == priority]
    return items[skip : skip + limit]


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    return _get_or_404(task_id)


@app.put("/tasks/{task_id}", response_model=TaskOut)
def replace_task(task_id: int, payload: TaskReplace):
    task = _get_or_404(task_id)
    task.update(payload.model_dump())                     # overwrite ALL fields
    return task


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate):
    task = _get_or_404(task_id)
    changes = payload.model_dump(exclude_unset=True)      # only fields client sent
    task.update(changes)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    _get_or_404(task_id)
    del _db[task_id]
    # returning nothing -> empty 204 body
```

### PUT vs PATCH — the key detail
```
Stored: {"title": "A", "priority": "high", "done": false}

PATCH {"done": true}  → {"title": "A", "priority": "high", "done": true}
PUT   {"title": "B"}  → {"title": "B", "priority": "medium", "done": false}   (missing fields reset to defaults)
```
`exclude_unset=True` distinguishes "client didn't send `description`" from "client sent `description: null`" — critical for PATCH.

Sample session:
```bash
$ curl -X POST localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Learn FastAPI","priority":"high"}'
{"title":"Learn FastAPI","description":null,"priority":"high","done":false,"id":1,"created_at":"2026-10-25T10:00:00Z"}

$ curl -X PATCH localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"done":true}'
$ curl -X DELETE -i localhost:8000/tasks/1
HTTP/1.1 204 No Content
```
PowerShell:
```powershell
PS> Invoke-RestMethod -Method Post -Uri localhost:8000/tasks -ContentType "application/json" -Body '{"title":"Learn FastAPI"}'
```

---

## 3.4 Pagination, Filtering, Sorting, Searching, Field Selection

### Offset pagination (simple)
`GET /tasks?skip=40&limit=20` (or `page=3&size=20`).
- ✅ Easy, supports "jump to page N".
- ❌ Slow on deep pages (`OFFSET 1000000` scans rows), results shift if rows are inserted.

### Cursor / keyset pagination (scales)
`GET /tasks?limit=20&cursor=eyJpZCI6IDEyMH0` → `WHERE id > 120 ORDER BY id LIMIT 20`.
- ✅ Constant speed, stable under inserts. ❌ No random page access.

### Paginated response envelope
```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


@app.get("/v2/tasks", response_model=Page[TaskOut])
def list_tasks_paged(page: Annotated[int, Query(ge=1)] = 1,
                     size: Annotated[int, Query(ge=1, le=100)] = 20):
    items = sorted(_db.values(), key=lambda t: t["id"])
    total = len(items)
    start = (page - 1) * size
    return Page(items=items[start:start + size], total=total, page=page, size=size,
                pages=(total + size - 1) // size)
```
(Python 3.12+: `class Page[T](BaseModel)` syntax also works with Pydantic.)

### Sorting with whitelist (security!)
```python
SORTABLE = {"id", "title", "created_at", "priority"}

def parse_sort(sort: str) -> list[tuple[str, bool]]:
    """'-created_at,title' -> [('created_at', True), ('title', False)]"""
    result = []
    for part in sort.split(","):
        desc = part.startswith("-")
        field = part.lstrip("-+")
        if field not in SORTABLE:
            raise HTTPException(400, f"Cannot sort by '{field}'")
        result.append((field, desc))
    return result
```
⚠️ Never interpolate user-provided column names into SQL — always whitelist.

### Search
`GET /tasks?q=fastapi` → `ILIKE '%fastapi%'` (small data) or Postgres full-text search / Elasticsearch (large data).

### Field selection (sparse fieldsets)
`GET /tasks?fields=id,title`
```python
@app.get("/tasks-lite")
def tasks_lite(fields: str | None = None):
    allowed = set(TaskOut.model_fields)
    wanted = set(fields.split(",")) & allowed if fields else allowed
    return [{k: v for k, v in t.items() if k in wanted} for t in _db.values()]
```
(For heavy field selection needs, consider GraphQL.)

💡 Library: `fastapi-pagination` provides ready-made `Page`, `paginate()` for SQLAlchemy.

---

## 3.5 Errors: Status Codes and Consistent Error Responses

### `HTTPException`
```python
raise HTTPException(
    status_code=409,
    detail="Email already registered",
    headers={"X-Error-Code": "EMAIL_TAKEN"},
)
# -> 409 {"detail": "Email already registered"}
```

### Default validation error (422)
```json
{"detail": [{"type": "missing", "loc": ["body", "title"], "msg": "Field required", "input": {}}]}
```

### 🟡 Professional: one consistent error format
Pick a format and use it everywhere. RFC 9457 "Problem Details" is a good standard:
```json
{
  "type": "https://api.example.com/errors/task-not-found",
  "title": "Task not found",
  "status": 404,
  "detail": "Task 42 does not exist",
  "code": "TASK_NOT_FOUND",
  "request_id": "a1b2c3"
}
```

### Custom exceptions + handlers
```python
# errors.py
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppError(Exception):
    """Base for domain errors. Services raise these, not HTTPException."""
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


def _body(status_code: int, code: str, message: str, request: Request, **extra):
    return {
        "status": status_code,
        "code": code,
        "message": message,
        "path": request.url.path,
        "request_id": request.headers.get("x-request-id"),
        **extra,
    }


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content=_body(exc.status_code, exc.code, exc.message, request))

    @app.exception_handler(StarletteHTTPException)          # catches FastAPI HTTPException + 404/405 routing
    async def http_error_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(status_code=exc.status_code, content=_body(exc.status_code, "HTTP_ERROR", str(exc.detail), request),
                            headers=getattr(exc, "headers", None))

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        errors = [{"field": ".".join(map(str, e["loc"][1:])), "message": e["msg"]} for e in exc.errors()]
        return JSONResponse(status_code=422, content=_body(422, "VALIDATION_ERROR", "Invalid request", request, errors=errors))

    @app.exception_handler(Exception)                        # last resort — never leak stack traces
    async def unhandled_handler(request: Request, exc: Exception):
        # log full exception with traceback here
        return JSONResponse(status_code=500, content=_body(500, "INTERNAL_ERROR", "Something went wrong", request))
```
```python
# main.py
from errors import register_exception_handlers, NotFoundError
app = FastAPI()
register_exception_handlers(app)
```

💡 **Why domain exceptions?** Services shouldn't know about HTTP. `NotFoundError` can be raised from a service used by an API, a CLI, or a Celery worker; the API layer maps it to 404.

🐞 Register handlers for `starlette.exceptions.HTTPException` (not only `fastapi.HTTPException`) so that router-level 404/405 errors also use your format.

---

## 3.6 API Versioning and Backward Compatibility

| Strategy | Example | Pros | Cons |
|---|---|---|---|
| **URL path** (most common) | `/api/v1/tasks` | Obvious, cache-friendly, easy routing | URL changes |
| Header | `Accept: application/vnd.myapp.v2+json` / `X-API-Version: 2` | Clean URLs | Harder to test/debug |
| Query | `?version=2` | Simple | Easy to forget, pollutes caching |

```python
from fastapi import APIRouter

v1 = APIRouter(prefix="/api/v1", tags=["v1"])
v2 = APIRouter(prefix="/api/v2", tags=["v2"])

@v1.get("/tasks/{id}")
def get_v1(id: int): return {"id": id, "name": "old field name"}

@v2.get("/tasks/{id}")
def get_v2(id: int): return {"id": id, "title": "renamed field"}

app.include_router(v1)
app.include_router(v2)
```

### Backward compatibility rules
- ✅ **Non-breaking:** add optional request fields, add response fields, add endpoints, add enum values *only if clients tolerate unknowns*.
- ❌ **Breaking:** remove/rename fields, change types, make optional field required, change status codes or error format, change auth.
- Deprecate before removing: `@router.get(..., deprecated=True)` + `Deprecation`/`Sunset` response headers + changelog + usage metrics.
- Clients should be "tolerant readers" (ignore unknown fields).

---

## 3.7 Form Data, File Uploads and Downloads

Requires `python-multipart` (included in `fastapi[standard]`).

```python
from pathlib import Path
from uuid import uuid4
from fastapi import File, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

UPLOAD_DIR = Path("uploads"); UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED = {"image/png", "image/jpeg", "application/pdf"}
MAX_BYTES = 5 * 1024 * 1024


@app.post("/login-form")
async def login_form(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@app.post("/upload", status_code=201)
async def upload(
    file: Annotated[UploadFile, File(description="PNG/JPEG/PDF up to 5 MB")],
    caption: Annotated[str | None, Form()] = None,
):
    if file.content_type not in ALLOWED:                 # client-claimed; also sniff magic bytes in prod
        raise HTTPException(415, "Unsupported file type")
    safe_name = f"{uuid4().hex}{Path(file.filename or '').suffix.lower()}"   # never trust filename
    dest = UPLOAD_DIR / safe_name
    size = 0
    with dest.open("wb") as out:
        while chunk := await file.read(1024 * 1024):    # stream in 1 MB chunks
            size += len(chunk)
            if size > MAX_BYTES:
                out.close(); dest.unlink(missing_ok=True)
                raise HTTPException(413, "File too large")
            out.write(chunk)
    return {"id": safe_name, "size": size, "caption": caption}


@app.post("/upload-many")
async def upload_many(files: list[UploadFile]):
    return [{"name": f.filename, "type": f.content_type} for f in files]


@app.get("/files/{file_id}")
async def download(file_id: str):
    path = (UPLOAD_DIR / file_id).resolve()
    if UPLOAD_DIR.resolve() not in path.parents or not path.is_file():   # path traversal guard
        raise HTTPException(404, "Not found")
    return FileResponse(path, filename=file_id)           # sets Content-Disposition: attachment


@app.get("/export.csv")
def export_csv():
    def rows():
        yield "id,title\n"
        for t in _db.values():
            yield f'{t["id"]},{t["title"]}\n'
    return StreamingResponse(rows(), media_type="text/csv",
                             headers={"Content-Disposition": 'attachment; filename="tasks.csv"'})
```

| Type | When |
|---|---|
| `bytes = File()` | Tiny files (loaded fully into memory) |
| `UploadFile` | Anything real — spooled to disk after a threshold, async `read/seek/close`, has `filename`, `content_type`, `size` |

🟡 **Production:** upload directly to object storage (S3/GCS/Azure Blob) via **pre-signed URLs** so large files never pass through your API workers.

⚠️ Can't mix JSON body (`BaseModel`) and `File` in the same request — multipart and JSON are different encodings. Send metadata as `Form` fields (or a JSON string in a form field).

---

## 3.8 CORS and Middleware

**CORS (Cross-Origin Resource Sharing):** Browsers block JavaScript on `https://app.com` from reading responses from `https://api.com` unless the API says it's allowed. Non-browser clients (curl, servers) ignore CORS entirely — **CORS is not security for your API**; it protects users' browsers.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "http://localhost:5173"],   # explicit list
    allow_credentials=True,                    # allow cookies/Authorization
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
    max_age=600,                               # cache preflight 10 min
)
```
⚠️ `allow_origins=["*"]` with `allow_credentials=True` is invalid per the CORS spec (browsers reject it) and dangerous. Use explicit origins, or `allow_origin_regex=r"https://.*\.example\.com"`.

**Preflight:** For non-simple requests (e.g., `PUT`, JSON content-type, `Authorization` header) the browser first sends `OPTIONS` with `Origin` and `Access-Control-Request-Method`; the middleware answers it.

### A simple custom middleware
```python
import time
from fastapi import Request

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)                   # run the route
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - start)*1000:.1f}"
    return response
```
Other built-ins: `GZipMiddleware`, `TrustedHostMiddleware`, `HTTPSRedirectMiddleware`. (More in chapter 8.)

---

## ✅ Quick Revision — Chapter 3

- Resources = plural nouns; verbs = HTTP methods; filter/sort/paginate via query params.
- Models: `XCreate`, `XUpdate` (all optional), `XOut` (`from_attributes=True`).
- PATCH → `model_dump(exclude_unset=True)`; PUT → replace everything.
- POST → 201 (+ `Location`), DELETE → 204, validation → 422, conflict → 409, auth → 401/403.
- Offset pagination is simple; cursor pagination scales.
- Whitelist sort fields; never interpolate user input into SQL.
- Domain exceptions in services → mapped to HTTP in handlers → one error format.
- Version in URL (`/api/v1`); additive changes only; deprecate before removing.
- `UploadFile` + chunked reads + size/type checks + random filenames.
- CORS: explicit origins; never `*` with credentials.

🎤 *"A good REST API is predictable: noun-based URLs, correct verbs and status codes, consistent error format, pagination on every list, versioning, and separate input/output schemas so clients can't set server-owned fields or see sensitive ones."*
