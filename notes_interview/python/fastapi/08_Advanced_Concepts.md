# Chapter 8 — Advanced FastAPI Concepts

> **Goal:** Master the request lifecycle, middleware, background work, WebSockets, streaming, async concurrency, caching, rate limiting, logging/tracing, connection pooling, idempotency, and resilient integrations with external services and webhooks.

---

## 8.1 Middleware and the Request Lifecycle

**Middleware** wraps every request/response — like layers of an onion.

```
request ─► [Middleware A] ─► [Middleware B] ─► routing ─► dependencies ─► endpoint
response ◄─ [Middleware A] ◄─ [Middleware B] ◄──────────────────────────── return
```
- `app.add_middleware(X)` adds X as the **outermost** layer → the **last added runs first**.
- Exception handlers run inside the middleware stack (`ServerErrorMiddleware` is outermost, `ExceptionMiddleware` innermost).

### Request ID + timing middleware (function style)
```python
import time, uuid
from fastapi import Request

@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request.state.request_id = request_id
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["Server-Timing"] = f"app;dur={(time.perf_counter() - start)*1000:.1f}"
    return response
```

### Pure ASGI middleware (🔴 faster, works with streaming)
`@app.middleware("http")` / `BaseHTTPMiddleware` has overhead and historically had issues with streaming responses and contextvars. For high-performance or streaming apps, write raw ASGI middleware:
```python
from starlette.types import ASGIApp, Receive, Scope, Send

class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        rid = headers.get(b"x-request-id", uuid.uuid4().hex.encode())

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                message.setdefault("headers", []).append((b"x-request-id", rid))
            await send(message)

        await self.app(scope, receive, send_wrapper)

app.add_middleware(RequestIDMiddleware)
```

| Built-in middleware | Purpose |
|---|---|
| `CORSMiddleware` | Cross-origin browser access |
| `GZipMiddleware(minimum_size=1000)` | Compress responses |
| `TrustedHostMiddleware(allowed_hosts=[...])` | Reject spoofed `Host` headers |
| `HTTPSRedirectMiddleware` | Redirect http→https |
| `SessionMiddleware` | Signed cookie sessions |

| Middleware vs Dependency | |
|---|---|
| Middleware | Every request (incl. 404s, static); cross-cutting (logging, headers, timing, CORS); no access to route params/typed inputs |
| Dependency | Per route/router; typed; can be overridden in tests; appears in OpenAPI (auth) |

---

## 8.2 Background Tasks vs Task Queues

### `BackgroundTasks` (built in)
Runs **after the response is sent**, in the **same process**.
```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str) -> None:
    ...  # blocking SMTP is OK: sync functions run in the threadpool

@app.post("/signup", status_code=201)
def signup(data: UserRegister, tasks: BackgroundTasks):
    user = create_user(data)
    tasks.add_task(send_welcome_email, user.email)
    return user
```

### External queue (Celery, ARQ, Dramatiq, RQ, Taskiq, cloud queues)
```python
# worker.py (Celery)
from celery import Celery
celery_app = Celery("app", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def generate_report(self, report_id: int):
    ...

# api
@app.post("/reports", status_code=202)
def create_report(...):
    report = repo.create(status="pending")
    generate_report.delay(report.id)
    return {"id": report.id, "status_url": f"/reports/{report.id}"}
```
```bash
$ celery -A worker.celery_app worker --loglevel=info      # separate process
```

| | `BackgroundTasks` | Task queue |
|---|---|---|
| Setup | None | Broker (Redis/RabbitMQ/SQS) + workers |
| Survives crash/redeploy | ❌ lost | ✅ persisted |
| Retries, scheduling, priorities | ❌ | ✅ |
| Scales independently | ❌ shares API CPU | ✅ |
| CPU-heavy work | ❌ hurts API latency | ✅ |
| Use for | Fire-and-forget, small, non-critical (log, cache warm, non-critical email) | Emails that must go out, reports, video/ML processing, payments follow-ups |

**Async job pattern:** `POST` → `202 Accepted` + job id → client polls `GET /jobs/{id}` or receives webhook/WebSocket notification.

💡 **Transactional outbox:** to avoid "DB committed but message never enqueued", write an `outbox` row in the *same transaction*, and a relay process publishes it to the queue.

---

## 8.3 WebSockets and Real-Time Communication

HTTP = request → response. **WebSocket** = a persistent, two-way connection (chat, live dashboards, notifications, collaborative editing).

```python
from fastapi import WebSocket, WebSocketDisconnect, Query, status

class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, set[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(room, set()).add(ws)

    def disconnect(self, room: str, ws: WebSocket):
        self.rooms.get(room, set()).discard(ws)

    async def broadcast(self, room: str, message: dict):
        for ws in list(self.rooms.get(room, ())):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(room, ws)

manager = ConnectionManager()


@app.websocket("/ws/rooms/{room}")
async def chat(ws: WebSocket, room: str, token: str = Query(...)):
    user = verify_ws_token(token)                 # browsers can't set Authorization header on WS
    if user is None:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(room, ws)
    try:
        while True:
            data = await ws.receive_json()
            await manager.broadcast(room, {"user": user.name, "text": data["text"]})
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
```
JS client:
```js
const ws = new WebSocket(`wss://api.example.com/ws/rooms/general?token=${token}`);
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.send(JSON.stringify({text: "hi"}));
```

🔴 **Scaling:** the in-memory manager only knows connections on *this* process. With multiple workers/pods, use **Redis Pub/Sub** (or NATS/Kafka) to fan out messages across instances; configure the load balancer for long-lived connections (timeouts, sticky sessions optional).

Alternatives: **Server-Sent Events (SSE)** — one-way server→client over plain HTTP (simpler; great for notifications & LLM token streaming); long polling.

---

## 8.4 Dependency Injection in Depth

```python
# Sub-dependencies & caching
def get_settings(): ...
def get_db(): ...
def get_repo(db=Depends(get_db)): ...
def get_service(repo=Depends(get_repo), settings=Depends(get_settings)): ...
# get_db is executed once per request even if several deps need it.

# Security dependencies with scopes
from fastapi import Security
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="token", scopes={"items:read": "Read", "items:write": "Write"})

def current_user(scopes: SecurityScopes, token: str = Depends(oauth2)):
    payload = decode(token)
    granted = set(payload.get("scope", "").split())
    if not set(scopes.scopes) <= granted:
        raise HTTPException(403, "Not enough permissions")
    return payload

@app.post("/items")
def create(user=Security(current_user, scopes=["items:write"])): ...
```

`yield` dependency teardown timing: exactly *when* the code after `yield` runs, before or after the response is sent, has changed across FastAPI releases, and newer versions let you choose with a `scope` option on `Depends`. Check the release notes for your version. The practical rule doesn't depend on the version: don't rely on post-`yield` code to change the response, and do commits *before* returning.

Global singletons via DI:
```python
@lru_cache
def get_http_client() -> httpx.Client: ...   # or store in app.state in lifespan
```

---

## 8.5 Custom Responses and Streaming

```python
from fastapi.responses import StreamingResponse
import asyncio, json

# Server-Sent Events (e.g., LLM tokens, progress)
@app.get("/stream")
async def stream():
    async def event_gen():
        for i in range(5):
            yield f"data: {json.dumps({'progress': i * 25})}\n\n"
            await asyncio.sleep(1)
        yield "event: done\ndata: {}\n\n"
    return StreamingResponse(event_gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# Stream a large DB export without loading it into memory
@app.get("/export.ndjson")
def export(db: DbSession):
    def rows():
        for user in db.scalars(select(User).execution_options(yield_per=1000)):
            yield json.dumps({"id": user.id, "email": user.email}) + "\n"
    return StreamingResponse(rows(), media_type="application/x-ndjson")
```
- Detect client disconnects in long streams: `if await request.is_disconnected(): break`.
- Behind Nginx, disable buffering for SSE (`X-Accel-Buffering: no`).

Custom response class (e.g., set a default media type):
```python
from fastapi.responses import JSONResponse
class PrettyJSON(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(content, indent=2, ensure_ascii=False).encode()

app = FastAPI(default_response_class=PrettyJSON)
```
💡 Performance: when you declare a return type / `response_model`, FastAPI validates & serializes via Pydantic (Rust core) which is fast; returning a `Response` directly skips validation entirely.

---

## 8.6 Async Programming, Concurrency, Blocking Operations

```
Event loop (single thread):
  req1: await db ──────────┐          ┌─► continue req1
  req2:   await http ──────┼──┐       │
  req3:     compute (no await!) ████████ ← blocks everyone
```

| Workload | Tool |
|---|---|
| I/O-bound, async libs | `async def` + `await` |
| I/O-bound, sync libs | `def` endpoint (threadpool) or `await asyncio.to_thread(fn)` |
| CPU-bound | `ProcessPoolExecutor`, separate worker service, task queue |
| Many concurrent calls | `asyncio.gather` / `asyncio.TaskGroup` (3.11+) |

```python
import asyncio, httpx

async def fetch_dashboard(user_id: int, client: httpx.AsyncClient):
    async with asyncio.TaskGroup() as tg:                         # structured concurrency
        profile = tg.create_task(client.get(f"/profiles/{user_id}"))
        orders = tg.create_task(client.get(f"/orders?user={user_id}"))
    return profile.result().json(), orders.result().json()

# limit concurrency to protect a downstream
sem = asyncio.Semaphore(10)
async def limited(url):
    async with sem:
        return await client.get(url)

# timeout an operation
async with asyncio.timeout(2):          # 3.11+
    await slow_call()
```

Threadpool size (default 40 tokens) — raise if many concurrent `def` endpoints block on I/O:
```python
import anyio
@asynccontextmanager
async def lifespan(app):
    anyio.to_thread.current_default_thread_limiter().total_tokens = 100
    yield
```

🐞 Detect blocking: `PYTHONASYNCIODEBUG=1` / `loop.slow_callback_duration`, or profile with `py-spy`; symptoms = latency spikes across *all* endpoints when one is slow.

🐞 Don't share one SQLAlchemy `AsyncSession` across concurrent tasks (`gather`) — sessions aren't concurrency-safe. Use one session per task.

---

## 8.7 Lifespan Management and Resource Cleanup

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.asyncio.from_url(settings.redis_url, decode_responses=True)
    app.state.http = httpx.AsyncClient(timeout=httpx.Timeout(5, connect=2),
                                       limits=httpx.Limits(max_connections=100))
    try:
        yield
    finally:
        await app.state.http.aclose()
        await app.state.redis.aclose()
        await async_engine.dispose()
```
Rules: create clients **once** (connection reuse), close them on shutdown, never create a new `AsyncClient` per request in hot paths.

---

## 8.8 Caching

| Layer | Example | Notes |
|---|---|---|
| HTTP / client | `Cache-Control: max-age=60`, `ETag` + `If-None-Match` → 304 | Free speed for GETs; CDN can serve |
| In-process | `functools.lru_cache`, `cachetools.TTLCache` | Fast; per-worker; inconsistent across pods |
| Distributed | **Redis**, Memcached | Shared across instances |
| DB | Materialized views, query cache | — |

### Cache-aside with Redis
```python
import json
from redis.asyncio import Redis

async def get_product(product_id: int, redis: Redis, db: AsyncSession) -> dict:
    key = f"product:v1:{product_id}"
    if cached := await redis.get(key):
        return json.loads(cached)                                  # cache HIT
    product = await db.get(Product, product_id)                    # cache MISS
    if product is None:
        raise NotFoundError("Product not found")
    data = ProductOut.model_validate(product).model_dump(mode="json")
    await redis.set(key, json.dumps(data), ex=300)                 # TTL 5 min (+ jitter in prod)
    return data

async def update_product(...):
    ...  # update DB, commit
    await redis.delete(f"product:v1:{product_id}")                 # invalidate after commit
```

### ETag example
```python
import hashlib
@app.get("/products/{id}")
async def product(id: int, request: Request, response: Response):
    data = await get_product(id, ...)
    etag = '"' + hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16] + '"'
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "private, max-age=60"
    return data
```

Problems to know: **stale data** (TTL + invalidate on write), **cache stampede** (many misses at once → lock/single-flight, early refresh, TTL jitter), **penetration** (cache negative results briefly), **key versioning** (`v1` in key to invalidate on schema change).

---

## 8.9 Rate Limiting

Algorithms: **fixed window** (simple, bursty at edges), **sliding window**, **token bucket** (allows bursts, smooth), **leaky bucket**.

### Redis fixed-window limiter as a dependency
```python
from fastapi import Request, HTTPException

def rate_limit(limit: int, window_s: int):
    async def dep(request: Request):
        redis = request.app.state.redis
        ident = getattr(request.state, "user_id", None) or request.client.host
        key = f"rl:{request.url.path}:{ident}:{int(time.time() // window_s)}"
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, window_s)
        if count > limit:
            raise HTTPException(429, "Too many requests", headers={"Retry-After": str(window_s)})
    return Depends(dep)

@router.post("/auth/token", dependencies=[rate_limit(5, 60)])     # 5 login attempts / minute
def login(...): ...
```
Libraries: `slowapi` (Flask-Limiter port), `fastapi-limiter`. In production, also rate-limit at the **edge** (API gateway, Nginx `limit_req`, Cloudflare/WAF).

🐞 Behind a proxy, `request.client.host` is the proxy IP → run Uvicorn with `--proxy-headers --forwarded-allow-ips=<proxy ip>` so `X-Forwarded-For` is trusted only from your proxy.

---

## 8.10 Logging, Structured Logs, Request Tracing

**Structured logs** = JSON lines with consistent fields → searchable in ELK/Loki/Datadog/CloudWatch.

```python
# app/core/logging.py
import logging, sys
from contextvars import ContextVar
import structlog

request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)

def setup_logging(json: bool = True, level: str = "INFO") -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,             # include bound request_id, user_id
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if json else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(level)),
    )

log = structlog.get_logger()
```
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=rid, path=request.url.path, method=request.method)
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        log.exception("unhandled_error")
        raise
    log.info("request_completed", status=response.status_code,
             duration_ms=round((time.perf_counter() - start) * 1000, 1))
    response.headers["X-Request-ID"] = rid
    return response
```
Output:
```json
{"event":"request_completed","status":200,"duration_ms":12.4,"request_id":"9f1c...","path":"/api/v1/projects","method":"GET","level":"info","timestamp":"2026-10-25T10:00:00Z"}
```
(Standard-library-only alternative: `logging` + `python-json-logger`.)

Rules: log **events with context**, not prose; never log passwords/tokens/PII; propagate `X-Request-ID` to downstream calls; use log levels properly (DEBUG dev only; INFO business events; WARNING recoverable; ERROR needs attention).

**Distributed tracing:** OpenTelemetry auto-instrumentation creates spans for FastAPI, SQLAlchemy, httpx, Redis and propagates `traceparent` headers between services (details chapter 11).
```bash
$ pip install opentelemetry-distro opentelemetry-instrumentation-fastapi opentelemetry-exporter-otlp
$ opentelemetry-bootstrap -a install
$ opentelemetry-instrument uvicorn app.main:app
```

---

## 8.11 Database Connection Pooling

```
Workers × pool_size (+ max_overflow) ≤ DB max_connections (minus admin/migration headroom)
e.g. 4 pods × 4 workers × (5 + 10) = 240  →  Postgres default max_connections=100  ❌
```
| Setting | Meaning |
|---|---|
| `pool_size` | Connections kept open per process |
| `max_overflow` | Temporary extra connections under burst |
| `pool_timeout` | Seconds to wait for a free connection before error (default 30) |
| `pool_pre_ping` | Validate before use (handles dropped connections) |
| `pool_recycle` | Recycle before DB/proxy idle timeouts |

- Many pods/serverless → put **PgBouncer** (transaction pooling) or RDS Proxy in front of Postgres. With PgBouncer transaction mode + asyncpg, disable prepared statement cache (`connect_args={"prepared_statement_cache_size": 0}` / `statement_cache_size=0`).
- 🐞 "QueuePool limit of size 5 overflow 10 reached, connection timed out" → sessions not closed (missing `finally: db.close()`), long transactions, or pool too small for concurrency (`def` endpoints × threadpool 40 > pool 15!).

---

## 8.12 Idempotency and Retry-Safe API Design

**Problem:** Client sends `POST /payments`, network times out, client retries → **double charge**.

**Idempotent** = repeating the request has the same effect as doing it once. GET/PUT/DELETE are idempotent by definition; POST is not → use an **Idempotency-Key**.

```
Client: POST /payments   Idempotency-Key: 7b1e...   body {...}
Server:
  1. Look up key (scoped by user):
       - found + completed → return stored response (same status/body)
       - found + in progress → 409 "request in progress"
       - found + different body hash → 422 "key reused with different payload"
  2. Not found → insert key row (status=processing) with UNIQUE constraint (race-safe)
  3. Do the work in a transaction; store response; mark completed
  4. Keys expire after 24h
```
```python
class IdempotencyRecord(Base):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    request_hash: Mapped[str] = mapped_column(String(64))
    status_code: Mapped[int | None]
    response_body: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


@router.post("/payments", status_code=201)
def create_payment(body: PaymentIn, user: CurrentUser, db: DbSession,
                   idempotency_key: Annotated[str, Header(max_length=100)]):
    req_hash = hashlib.sha256(body.model_dump_json().encode()).hexdigest()
    existing = db.get(IdempotencyRecord, (idempotency_key, user.id))
    if existing:
        if existing.request_hash != req_hash:
            raise HTTPException(422, "Idempotency-Key reused with a different request")
        if existing.status_code is None:
            raise HTTPException(409, "Request is still being processed")
        return JSONResponse(status_code=existing.status_code, content=existing.response_body)
    record = IdempotencyRecord(key=idempotency_key, user_id=user.id, request_hash=req_hash)
    db.add(record)
    try:
        db.flush()                                       # UNIQUE(PK) wins the race
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Request is still being processed")
    payment = payment_service.charge(db, user, body)     # same transaction
    record.status_code, record.response_body = 201, PaymentOut.model_validate(payment).model_dump(mode="json")
    db.commit()
    return record.response_body
```
Other retry-safe techniques: natural unique constraints (`UNIQUE(order_id)` on payments), upserts (`INSERT ... ON CONFLICT DO NOTHING`), deduplicating consumers by message id.

---

## 8.13 Calling External Services (httpx) — Timeouts, Retries, Failures

```python
# app/clients/weather.py
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception


class UpstreamError(Exception): ...


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError)):
        return True
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code in {429, 502, 503, 504}


class WeatherClient:
    def __init__(self, http: httpx.AsyncClient, api_key: str):
        self.http, self.api_key = http, api_key

    @retry(
        retry=retry_if_exception(_is_retryable),
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=0.2, max=2),   # 0.2s, 0.4s… + jitter
        reraise=True,
    )
    async def _get(self, path: str, **params) -> dict:
        resp = await self.http.get(path, params=params, headers={"X-API-Key": self.api_key})
        resp.raise_for_status()
        return resp.json()

    async def current(self, city: str) -> dict:
        try:
            return await self._get("/v1/current", q=city)
        except (httpx.HTTPError,) as exc:
            raise UpstreamError(f"weather service failed: {exc}") from exc


# lifespan: one shared client with base_url, timeouts, pool limits
http = httpx.AsyncClient(
    base_url="https://api.weather.example",
    timeout=httpx.Timeout(5.0, connect=2.0),     # ★ ALWAYS set timeouts (httpx default is 5s; requests has NONE)
    limits=httpx.Limits(max_connections=50, max_keepalive_connections=20),
)
```
Map upstream failures to **502 Bad Gateway** / **503** / **504**, not 500.

Resilience toolkit:
| Pattern | Purpose |
|---|---|
| Timeouts (connect + read + total) | Never wait forever |
| Retries with exponential backoff + jitter | Transient failures; only for **idempotent** operations (or with idempotency keys) |
| Retry budget / max attempts | Avoid retry storms |
| Circuit breaker (`purgatory`, `aiobreaker`, `pybreaker`) | Stop calling a failing service; fail fast; probe later |
| Bulkhead (semaphore per dependency) | One slow dependency can't eat all workers |
| Fallback / cached response / degraded mode | Partial functionality |
| Respect `Retry-After` on 429/503 | Be a good client |

---

## 8.14 Webhooks and Event-Driven Integrations

### Receiving webhooks (e.g., Stripe, GitHub)
```python
import hmac, hashlib, time

@router.post("/webhooks/payments", status_code=200)
async def payment_webhook(request: Request, db: DbSession, tasks: BackgroundTasks):
    raw = await request.body()                               # ★ verify on RAW bytes
    sig = request.headers.get("X-Signature", "")
    ts = request.headers.get("X-Timestamp", "0")
    if abs(time.time() - int(ts)) > 300:                     # replay protection (5 min)
        raise HTTPException(400, "Stale webhook")
    expected = hmac.new(settings.webhook_secret.encode(), f"{ts}.".encode() + raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):               # constant-time compare
        raise HTTPException(401, "Bad signature")
    event = json.loads(raw)
    if db.get(ProcessedEvent, event["id"]):                  # ★ dedupe — providers retry (at-least-once)
        return {"status": "duplicate"}
    db.add(ProcessedEvent(id=event["id"])); db.commit()
    tasks.add_task(handle_event, event)                      # respond fast (<few s); process async (queue in prod)
    return {"status": "ok"}
```
Receiving checklist: verify signature, check timestamp, dedupe by event id, respond 2xx quickly, process asynchronously, handle out-of-order events.

### Sending webhooks
- Sign payloads (HMAC with per-subscriber secret), include event id + timestamp.
- Deliver from a **queue** with retries + exponential backoff, dead-letter after N failures, delivery logs.
- Don't send to internal IPs (SSRF protection when URLs are user-provided).

### Event-driven architecture basics
Services publish **events** ("OrderPlaced") to a broker (Kafka, RabbitMQ, SNS/SQS, NATS); consumers react independently. Gains: decoupling, scalability. Costs: eventual consistency, ordering, idempotent consumers, observability. Use the **outbox pattern** to publish reliably after DB commits.

---

## ✅ Quick Revision — Chapter 8

- Middleware: last added = outermost; pure ASGI middleware for performance/streaming.
- `BackgroundTasks` = after-response, in-process, not durable → use Celery/ARQ for critical work.
- WebSockets: `accept`, loop `receive`, handle `WebSocketDisconnect`; Redis pub/sub to scale; SSE for one-way.
- Dependencies cached per request; `Security` + scopes; `yield` cleanup.
- `StreamingResponse` for SSE/large exports; detect disconnects.
- Never block the event loop; `to_thread` / process pools for blocking/CPU work; `TaskGroup` for concurrency.
- Lifespan: one shared `AsyncClient`/Redis/engine, closed on shutdown.
- Cache-aside + TTL + invalidate on write; ETags; watch stampede.
- Rate-limit with Redis/edge; trust proxy headers carefully.
- Structured JSON logs with request ID via contextvars; OpenTelemetry traces.
- Pool math: pods × workers × (pool + overflow) ≤ DB max; PgBouncer.
- Idempotency-Key for unsafe retries; unique constraints; upserts.
- httpx with timeouts + tenacity retries (idempotent only) + circuit breakers.
- Webhooks: verify HMAC on raw body, timestamp, dedupe, ack fast, process async.
