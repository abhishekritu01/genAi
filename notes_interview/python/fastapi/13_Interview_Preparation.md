# Chapter 13 — Interview Preparation

> Beginner → senior questions with short, speakable answers. 🎤 = model answer. Levels: 🟢 junior · 🟡 mid · 🔴 senior.
> Tip: answer in this shape → **definition → how it works → when/why → trade-off or example**.

---

## 13.0 Top 30 (revise these the night before)

1. What is FastAPI and how does it differ from Flask/Django? *(13.1 Q1)*
2. ASGI vs WSGI *(Q3)*
3. `def` vs `async def` in FastAPI *(13.5 Q1)*
4. What happens when you block inside `async def`? *(13.5 Q2)*
5. How does validation work / what is a 422? *(13.1 Q6)*
6. `response_model` — why? *(13.1 Q8)*
7. Path vs query vs body parameters *(13.1 Q5)*
8. Dependency injection with `Depends` — how and why *(13.2 Q1)*
9. `yield` dependencies *(13.2 Q3)*
10. Middleware vs dependency *(13.2 Q5)*
11. PUT vs PATCH; idempotency *(13.3 Q2–Q3)*
12. Status codes 401 vs 403, 400 vs 422, 409 *(13.3 Q4)*
13. Pagination strategies *(13.3 Q6)*
14. Engine vs Session; session per request *(13.4 Q1)*
15. N+1 problem and eager loading *(13.4 Q4)*
16. Transactions, commit/rollback/flush *(13.4 Q3)*
17. Alembic workflow; autogenerate limitations *(13.4 Q8–Q9)*
18. Zero-downtime migrations *(13.4 Q10)*
19. JWT structure and validation *(13.6 Q3)*
20. Access vs refresh tokens; revocation *(13.6 Q4–Q5)*
21. Password hashing *(13.6 Q2)*
22. RBAC + ownership (IDOR) *(13.6 Q6–Q7)*
23. Testing with TestClient + dependency_overrides *(13.7 Q1–Q2)*
24. BackgroundTasks vs Celery *(13.5 Q6)*
25. Lifespan events *(13.2 Q7)*
26. CORS *(13.8 Q3)*
27. Deployment: workers, Docker, Gunicorn/Uvicorn *(13.9 Q1–Q3)*
28. Caching & invalidation *(13.10 Q3)*
29. Idempotency keys *(13.10 Q4)*
30. Scaling a FastAPI service end to end *(13.10 Q1)*

---

## 13.1 FastAPI Fundamentals

**Q1 🟢 What is FastAPI and why use it?**
🎤 A modern Python web framework for building APIs, built on Starlette (web layer) and Pydantic (validation). Type hints drive request parsing, validation, serialization and automatic OpenAPI docs. It's async-native (ASGI), fast, and catches bad input before your code runs. Compared to Flask it has built-in validation, docs and async; compared to Django REST Framework it's lighter and faster but you bring your own ORM, auth and admin.

**Q2 🟢 What are Starlette, Pydantic and Uvicorn?**
🎤 Uvicorn is the ASGI server that handles HTTP connections. Starlette is the ASGI toolkit for routing, middleware, requests/responses, WebSockets. FastAPI subclasses Starlette and adds dependency injection, validation and OpenAPI. Pydantic validates and serializes data using type hints (Rust core in v2).

**Q3 🟢 ASGI vs WSGI?**
🎤 WSGI is the synchronous standard: one request occupies a worker until it finishes. ASGI is the async successor: the app is an async callable `(scope, receive, send)`, so one process can interleave many requests while they wait on I/O, and it supports long-lived connections like WebSockets.

**Q4 🟢 How do you run a FastAPI app?**
🎤 `fastapi dev main.py` for development with reload, `fastapi run` or `uvicorn app.main:app --host 0.0.0.0 --port 8000` in production — usually one process per container scaled by replicas, or multiple workers on a VM.

**Q5 🟢 How does FastAPI know whether a parameter is path, query or body?**
🎤 Names in the path template are path params; simple types (int, str, bool, enums) not in the path are query params; Pydantic models are the JSON body. You can be explicit with `Path()`, `Query()`, `Body()`, `Header()`, `Cookie()`, `Form()`, `File()`.

**Q6 🟢 What is a 422 error?**
🎤 "Unprocessable Content" — FastAPI's automatic response when request data fails validation. The body has a `detail` list with `loc` (where), `msg` and `type` for each error. You can customize it with an exception handler for `RequestValidationError`.

**Q7 🟢 What does `Optional`/`| None` mean for a query parameter?**
🎤 With a default (`q: str | None = None`) it's optional. Without a default it's required — even if the type allows None. The default decides required-ness.

**Q8 🟢 Why use `response_model`?**
🎤 It filters the output to the declared fields (so a `hashed_password` on the ORM object never leaks), validates it, converts it to JSON, and documents the response schema in OpenAPI. The return type annotation does the same in modern FastAPI.

**Q9 🟢 Why separate Create/Update/Out schemas?**
🎤 Inputs and outputs have different fields: clients shouldn't send `id`, `owner_id`, `role`; outputs shouldn't include secrets; updates need all-optional fields for PATCH. Separate models prevent mass assignment and data leaks, and make docs accurate.

**Q10 🟡 Pydantic v1 vs v2 changes you use daily?**
🎤 `model_dump()` replaces `dict()`, `model_validate()` replaces `parse_obj()`, `model_config = ConfigDict(from_attributes=True)` replaces `orm_mode`, `field_validator`/`model_validator` replace `validator`/`root_validator`, and `BaseSettings` moved to `pydantic-settings`. v2 is much faster because its core is in Rust.

**Q11 🟢 Where are the docs?**
🎤 `/docs` (Swagger UI), `/redoc` (ReDoc), `/openapi.json` (raw spec). They're generated from route signatures, models, `tags`, `summary`, docstrings and `responses`.

**Q12 🟡 How do you return a custom status code or headers?**
🎤 `status_code=` on the decorator for the default; inject `Response` to set headers/cookies; raise `HTTPException` for errors; or return a `JSONResponse` directly (which bypasses `response_model`).

**Q13 🟡 What is `jsonable_encoder`?**
🎤 It converts objects (datetime, UUID, Decimal, Pydantic models) into JSON-compatible primitives. FastAPI uses it internally; you use it before storing data in a JSON column or cache.

**Q14 🟡 What's `Annotated` and why is it preferred?**
🎤 `Annotated[int, Query(ge=1)]` attaches FastAPI metadata to a type without hijacking the default value. Defaults stay real Python defaults, the function remains callable normally, and you can create reusable aliases like `CurrentUser = Annotated[User, Depends(get_current_user)]`.

---

## 13.2 Dependency Injection, Middleware, Lifespan

**Q1 🟢 What is dependency injection in FastAPI?**
🎤 Declaring what an endpoint needs — a DB session, the current user, pagination params — via `Depends(fn)`. FastAPI resolves a graph of dependencies per request, passes results in, and caches each dependency once per request. It removes duplication and makes testing easy through `app.dependency_overrides`.

**Q2 🟡 Are dependencies cached?**
🎤 Yes, within a single request: if two dependencies both need `get_db`, it runs once and the same session is shared. `Depends(fn, use_cache=False)` disables that. Nothing is cached across requests unless you do it yourself (e.g., `lru_cache` on `get_settings`).

**Q3 🟡 How do `yield` dependencies work?**
🎤 Code before `yield` is setup, the yielded value is injected, and code after `yield` (ideally in `finally`) is teardown — like closing a DB session. If you catch exceptions there, re-raise them, or FastAPI can't produce the right error response.

**Q4 🟡 Class-based and parametrized dependencies?**
🎤 A class can be a dependency (its `__init__` params become inputs). For parametrized checks, use a factory or a callable instance — e.g., `require_roles("admin")` returns a function that checks `user.role`.

**Q5 🟡 Middleware vs dependency — when to use which?**
🎤 Middleware runs for every request, including 404s and static files, and is ideal for cross-cutting concerns like request IDs, logging, timing, CORS, security headers. Dependencies are per-route or per-router, typed, visible in OpenAPI and overridable in tests — ideal for auth, DB sessions and permissions.

**Q6 🟡 In what order does middleware run?**
🎤 Like an onion: the last-added middleware is the outermost, so it sees the request first and the response last.

**Q7 🟢 What are lifespan events?**
🎤 An async context manager passed to `FastAPI(lifespan=...)`: code before `yield` runs on startup (create DB pool, HTTP client, load ML model), code after runs on shutdown (close them). `@app.on_event` is deprecated.

**Q8 🟡 How do you share an `httpx.AsyncClient` across requests?**
🎤 Create it once in lifespan, store it on `app.state` (or yield it in the lifespan state), inject it via a dependency, and close it on shutdown. Creating a client per request loses connection pooling.

**Q9 🟡 How do you structure a large FastAPI project?**
🎤 App factory plus `APIRouter` per module, either layer-based (routers/services/repositories/models/schemas) or feature-based (one folder per domain). Thin routers call services that own business rules and transactions; repositories do data access; settings come from `pydantic-settings`.

---

## 13.3 REST & HTTP

**Q1 🟢 What makes an API RESTful?**
🎤 Resources identified by URLs, manipulated with standard HTTP methods, stateless requests, representations like JSON, proper status codes, and cacheability.

**Q2 🟢 PUT vs PATCH?**
🎤 PUT replaces the whole resource — missing fields reset. PATCH applies a partial update. In FastAPI, PATCH uses an all-optional model and `model_dump(exclude_unset=True)` so only fields the client sent are changed.

**Q3 🟢 Which methods are idempotent / safe?**
🎤 Safe (no state change): GET, HEAD, OPTIONS. Idempotent (repeat = same effect): those plus PUT and DELETE. POST isn't idempotent; PATCH isn't guaranteed to be. That matters for retries.

**Q4 🟢 401 vs 403? 400 vs 422? When 409?**
🎤 401 means not authenticated (missing or invalid credentials, include `WWW-Authenticate`); 403 means authenticated but not allowed. 422 is schema/validation failure; 400 is a generic bad request or business-rule violation. 409 is a conflict with current state — duplicate email, version mismatch.

**Q5 🟢 What should POST return when it creates something?**
🎤 201 Created with the created resource and a `Location` header pointing to it.

**Q6 🟡 Offset vs cursor pagination?**
🎤 Offset (`page/size`) is simple and supports jumping to page N, but deep pages are slow and results shift with inserts. Cursor/keyset (`WHERE id > last_id ORDER BY id LIMIT n`) is constant-time and stable, but you can only go next/previous. I use cursor for large or infinite lists.

**Q7 🟡 How do you version an API?**
🎤 Usually URL prefix (`/api/v1`) with separate routers. Within a version only additive changes; breaking changes go to v2; old versions get deprecated with `Sunset` headers and usage monitoring before removal.

**Q8 🟡 How do you design consistent errors?**
🎤 One envelope (e.g., RFC 9457 problem details or `{code, message, details, request_id}`), domain exceptions raised in services and mapped to HTTP codes in exception handlers, including overriding the default 422 and 500 handlers so nothing leaks stack traces.

**Q9 🟡 How do file uploads work?**
🎤 `UploadFile` with `python-multipart`; it's spooled to disk and read asynchronously in chunks. Validate size and type, generate your own filename, store in object storage — ideally with pre-signed URLs so big files bypass the API.

**Q10 🟡 What's CORS and does it secure an API?**
🎤 A browser mechanism allowing JS from one origin to read responses from another; the server opts in with `Access-Control-Allow-*` headers and preflight `OPTIONS` handling. It doesn't protect the API from non-browser clients — authentication does.

---

## 13.4 Databases, SQLAlchemy, Alembic

**Q1 🟢 Engine vs Session?**
🎤 The engine is the connection pool and dialect — one per application. A session is a unit of work that tracks objects and holds a transaction — one per request, created by a `yield` dependency and always closed.

**Q2 🟡 Why `expire_on_commit=False`?**
🎤 By default, after commit all attributes expire and are reloaded on next access — an extra query, and in async it raises because lazy IO isn't allowed. Setting it to False keeps the loaded values, which is what you want when returning objects after commit.

**Q3 🟡 add vs flush vs commit vs refresh?**
🎤 `add` stages the object; `flush` sends SQL inside the open transaction (IDs assigned, still rollback-able); `commit` flushes and makes it permanent; `refresh` reloads from the DB to get server-generated values. After an exception, `rollback()` before using the session again.

**Q4 🟡 What's the N+1 problem and how do you fix it?**
🎤 Loading N parents with one query and then lazy-loading a relationship per parent → N extra queries. Fix with eager loading: `joinedload` for many-to-one, `selectinload` for collections, and `raiseload` to catch accidental lazy loads. Response models that include nested relations make it easy to trigger accidentally.

**Q5 🟡 joinedload vs selectinload?**
🎤 `joinedload` uses a JOIN in the same query — great for to-one relationships but duplicates parent rows for collections. `selectinload` runs a second `IN (...)` query — best for one-to-many and many-to-many.

**Q6 🟡 Sync or async SQLAlchemy with FastAPI?**
🎤 Both work. Sync sessions in `def` endpoints run in the threadpool and are simpler. Async (`create_async_engine`, `AsyncSession`) fits fully async stacks with high concurrency, but you must eager-load (no lazy loading) and use `expire_on_commit=False`. Never use a sync session inside `async def`.

**Q7 🟡 How do you prevent lost updates?**
🎤 Atomic SQL updates (`stock = stock - 1 WHERE stock > 0`), pessimistic locks (`SELECT … FOR UPDATE`), or optimistic locking with a version column that raises on conflict → 409. Plus DB constraints as the final guard.

**Q8 🟢 Describe the Alembic workflow.**
🎤 Change models → `alembic revision --autogenerate -m "..."` → review the file → `alembic upgrade head` → test `downgrade -1` → commit model and migration together. `env.py` imports all models and sets `target_metadata = Base.metadata`.

**Q9 🟡 What can't autogenerate detect?**
🎤 Renames (it sees drop + add, which loses data), data migrations, some type/enum/server-default changes, unnamed constraints, views, triggers. Always review; edit renames into `alter_column(new_column_name=...)`.

**Q10 🔴 How do you do zero-downtime migrations?**
🎤 Expand-and-contract: add new nullable columns or tables first, deploy code that writes both and reads old, backfill in batches, switch reads, and only drop the old column in a later release. Create indexes `CONCURRENTLY`, set `lock_timeout`, avoid NOT NULL without defaults on big tables, and run migrations as a single pipeline job before the rolling deploy.

**Q11 🟡 What are multiple heads and how do you fix them?**
🎤 Two migrations created from the same parent on different branches. `alembic merge heads -m "merge"` creates a merge revision. CI can check that there's exactly one head.

**Q12 🟡 SQLAlchemy vs SQLModel?**
🎤 SQLModel combines a SQLAlchemy table and a Pydantic model in one class — less boilerplate for small apps. SQLAlchemy 2.x with separate Pydantic schemas is more flexible and keeps storage and API contracts decoupled. I default to SQLAlchemy for larger systems.

**Q13 🟡 How do you prevent SQL injection?**
🎤 Use the ORM/Core or `text()` with bound parameters — never f-strings. Identifiers like sort columns can't be parameters, so whitelist them. Use a least-privilege DB user.

**Q14 🔴 How do you find and fix a slow query?**
🎤 Find it via `pg_stat_statements`, APM traces or SQL logs; run `EXPLAIN (ANALYZE, BUFFERS)`; look for sequential scans, bad row estimates, sorts on disk; add or adjust indexes (composite order matters), rewrite the query, eager-load properly, paginate, or cache. Then verify the plan changed.

---

## 13.5 Async & Concurrency

**Q1 🟢 `def` vs `async def` endpoints?**
🎤 `async def` runs on the event loop and should only await non-blocking I/O. `def` runs in a threadpool, so blocking libraries are safe there. If a library is blocking (requests, sync DB driver), use `def` or offload with `run_in_threadpool`/`asyncio.to_thread`.

**Q2 🟡 What happens if you call `time.sleep()` or `requests.get()` inside `async def`?**
🎤 It blocks the event loop — every other request on that worker freezes until it returns. Latency spikes across all endpoints. Use `await asyncio.sleep`, `httpx.AsyncClient`, or move it to a `def` endpoint/threadpool.

**Q3 🟡 How do you run several I/O calls concurrently?**
🎤 `asyncio.gather` or `asyncio.TaskGroup` (structured concurrency, 3.11+), with a semaphore to bound concurrency and `asyncio.timeout` for deadlines.

**Q4 🟡 How do you handle CPU-heavy work?**
🎤 Not in the event loop and not just threads (GIL). Use a process pool, a separate worker service via a task queue, or a dedicated inference service. The API returns 202 with a job ID.

**Q5 🟡 GIL — does it matter for FastAPI?**
🎤 The GIL prevents parallel Python bytecode in one process, but I/O releases it, so async/threads still give concurrency for I/O-bound APIs. For CPU parallelism, run multiple worker processes. (Free-threaded Python builds exist from 3.13 but aren't the default yet.)

**Q6 🟡 BackgroundTasks vs Celery?**
🎤 `BackgroundTasks` runs after the response in the same process — fine for small fire-and-forget work, but it's lost on crash and competes with request handling. Celery/ARQ/RQ persist jobs in a broker, retry, schedule, and scale workers independently — use them for anything that must happen or is heavy.

**Q7 🟡 WebSockets vs SSE vs polling?**
🎤 WebSockets are bidirectional persistent connections (chat, collaboration). SSE is one-way server→client over HTTP, simple and auto-reconnecting (notifications, LLM token streams). Polling is simplest but wasteful. Scaling WebSockets across instances needs a pub/sub backbone like Redis.

**Q8 🔴 Threadpool size and DB pool — how do they interact?**
🎤 Sync endpoints run on AnyIO's threadpool (40 by default). If 40 threads can each hold a DB connection but the pool allows 15, requests wait on `pool_timeout`. Size them consistently and multiply by workers and replicas to stay under the DB's `max_connections`, or add PgBouncer.

---

## 13.6 Authentication & Authorization

**Q1 🟢 Authentication vs authorization?**
🎤 Authentication verifies identity (401 on failure); authorization decides what that identity may do (403, or 404 to hide existence).

**Q2 🟢 How should passwords be stored?**
🎤 Never in plain text or with fast hashes. Use a slow, salted, memory-hard algorithm — Argon2id (or bcrypt) via `pwdlib`. Verify in constant time; equalize timing for unknown users.

**Q3 🟡 What's in a JWT and how do you validate it?**
🎤 Header, payload (claims like `sub`, `exp`, `iat`, `jti`, roles), and signature, base64url-encoded. It's signed, not encrypted — no secrets inside. Validate the signature with an explicit algorithm allow-list, require `exp`, check `iss`/`aud` if used, and check a `type` claim so refresh tokens can't be used as access tokens.

**Q4 🟡 Why access + refresh tokens?**
🎤 Access tokens are short-lived (minutes) and sent on every request, so a leaked one expires soon. Refresh tokens are long-lived, used only at the refresh endpoint, stored server-side so they can be revoked, and rotated on each use with reuse detection.

**Q5 🟡 How do you log out / revoke a JWT?**
🎤 Stateless JWTs can't be revoked by themselves. Options: keep access tokens short and revoke the refresh token; denylist the `jti` in Redis until expiry; or a per-user `token_version` claim that's bumped to invalidate all tokens.

**Q6 🟡 How do you implement RBAC in FastAPI?**
🎤 A role on the user (or claims in the token) and a dependency factory like `require_roles("admin")` used on routes or routers. For finer control, map roles to permissions and check a permission string, or use OAuth2 scopes with `Security`.

**Q7 🔴 What is IDOR/BOLA and how do you prevent it?**
🎤 Accessing someone else's object by changing an ID — OWASP API #1. Every object access must check ownership or membership, ideally in the query itself (`WHERE id=:id AND owner_id=:uid`) or in a reusable dependency, returning 404 to avoid leaking existence. Write tests that try to access other users' resources.

**Q8 🟡 OAuth2PasswordBearer — what does it do?**
🎤 It's a dependency that reads `Authorization: Bearer <token>`, returns 401 if missing, and registers the security scheme so Swagger shows the Authorize button. `tokenUrl` points to your login endpoint; you still decode and validate the token yourself.

**Q9 🟡 Where should a browser app store tokens?**
🎤 Avoid localStorage (XSS-readable). Keep the access token in memory and the refresh token in an HttpOnly, Secure, SameSite cookie — with CSRF protection on the refresh endpoint — or use a BFF with session cookies.

**Q10 🟡 How do you secure API keys?**
🎤 Generate long random keys with a recognizable prefix, show once, store only a hash, support multiple active keys for rotation, scope them, track last use, and rate-limit per key.

**Q11 🟡 Design a password reset.**
🎤 Forgot-password always returns the same response (no enumeration). Generate a random token, store its hash with short expiry and single use, email the link. On reset, validate, set the new hash, invalidate the token and all sessions, and notify the user.

---

## 13.7 Testing

**Q1 🟢 How do you test FastAPI endpoints?**
🎤 With `TestClient(app)` (httpx-based, in-process): send requests and assert on status, JSON and headers. Using it as a context manager runs lifespan events. For async tests, `httpx.AsyncClient` with `ASGITransport`.

**Q2 🟡 How do you use a test database?**
🎤 Override the DB dependency: `app.dependency_overrides[get_db] = lambda: test_session`. I use a real Postgres (Docker/testcontainers) and wrap each test in a transaction that's rolled back (`join_transaction_mode="create_savepoint"`), so tests are isolated and fast.

**Q3 🟡 How do you test authenticated routes?**
🎤 Either create a user and a real token in a fixture and send the header, or override `get_current_user` to return a fake user. Also test 401 without a token, 403 for wrong roles, and 404 for others' resources.

**Q4 🟡 How do you mock external APIs?**
🎤 Prefer overriding the client dependency with a fake. At the HTTP level, `respx` or `httpx.MockTransport`. With `unittest.mock.patch`, patch where the name is used, not where it's defined.

**Q5 🟡 What makes tests flaky and how do you avoid it?**
🎤 Shared state, test order dependence, real network, time and randomness, sleeps. Use per-test transactions, fakes, frozen time, seeded randomness, and no `sleep`-based waits.

**Q6 🟡 What code quality tools do you use?**
🎤 Ruff for linting and formatting, mypy or pyright for types, pytest-cov for coverage gates, pre-commit hooks, pip-audit/bandit for security, and `alembic check` in CI.

---

## 13.8 Security

**Q1 🟡 Top API security risks?**
🎤 OWASP API Top 10: broken object-level authorization, broken authentication, property-level issues (mass assignment/data exposure), unrestricted resource consumption, function-level authorization, SSRF, misconfiguration, poor inventory, unsafe consumption of third-party APIs.

**Q2 🟡 How do you prevent mass assignment?**
🎤 Dedicated input schemas that exclude server-owned fields, `extra="forbid"`, and never constructing models from raw request dicts.

**Q3 🟡 How do you configure CORS safely?**
🎤 An explicit list of origins per environment, never `*` with credentials, restricted methods and headers, and remember it doesn't replace auth.

**Q4 🟡 How do you handle secrets?**
🎤 Environment variables loaded via pydantic-settings, with values from a secret manager in production; `SecretStr` to avoid logging; required with no defaults; rotated; never in git or Docker image layers.

**Q5 🟡 How do you prevent sensitive data leaks?**
🎤 Response models on every endpoint, generic 500 handler, redaction in logs, no tokens or PII in URLs, docs disabled or protected in production, and careful error messages that don't enumerate users.

**Q6 🔴 How do you protect against SSRF when accepting webhook URLs?**
🎤 Allow-list schemes (https), resolve DNS and block private, loopback, link-local and metadata IPs, re-check after redirects or disable redirects, set timeouts and size limits, and send from an egress-restricted network.

---

## 13.9 Deployment & Operations

**Q1 🟡 How do you deploy FastAPI to production?**
🎤 Build a slim, non-root Docker image; run Uvicorn (one process per container, scaled by replicas on Kubernetes/ECS/Cloud Run) behind a load balancer that terminates TLS; configuration via env and secret manager; migrations as a separate job; health probes; logs, metrics and traces shipped centrally.

**Q2 🟡 Gunicorn with Uvicorn workers — still needed?**
🎤 Not in containers — the orchestrator manages processes, so one Uvicorn process per container is standard. On VMs you can use `uvicorn --workers N` or Gunicorn with the `uvicorn-worker` package's `UvicornWorker` (the old `uvicorn.workers` path is deprecated) for process management features.

**Q3 🟡 How many workers?**
🎤 Start near the number of CPU cores per host and load test. Async I/O-bound apps rarely need more. Factor in memory per worker and DB pool math.

**Q4 🟡 Liveness vs readiness?**
🎤 Liveness asks "is the process alive?" — no dependencies, failure restarts the container. Readiness asks "can I serve traffic?" — checks DB, Redis; failure removes the pod from the load balancer without restarting.

**Q5 🟡 What happens on graceful shutdown?**
🎤 SIGTERM → the LB stops routing, Uvicorn stops accepting connections and finishes in-flight requests within the timeout, lifespan shutdown closes pools, then the process exits before SIGKILL.

**Q6 🟡 What does your CI/CD pipeline look like?**
🎤 Lint, type-check, test with coverage against a real DB, migration checks, dependency audit → build an image tagged with the commit SHA → push → run migrations → deploy to staging → smoke tests → prod via rolling or canary deploy → monitor and roll back automatically on SLO regressions.

**Q7 🟡 How do you run migrations in deployment?**
🎤 As a dedicated one-off job before rollout (K8s Job/Helm hook/ECS task), not in every container's entrypoint, with backward-compatible expand/contract migrations so old and new code run safely during the rollout.

---

## 13.10 System Design & Senior Topics

**Q1 🔴 How would you scale a FastAPI service from 100 to 10,000 RPS?**
🎤 Measure first. Make the app stateless and scale horizontally behind a load balancer with autoscaling. Fix query performance (indexes, N+1, pagination), add PgBouncer, add Redis caching for hot reads and CDN/HTTP caching for public data, move heavy work to queues, use read replicas for read-heavy traffic, rate-limit abusive clients, and ensure non-blocking async I/O. Observe with RED metrics and traces, and load test each step.

**Q2 🔴 Monolith or microservices?**
🎤 Start with a modular monolith with clean module boundaries. Extract services only with clear bounded contexts and real drivers — independent scaling, team autonomy, different reliability needs — because microservices add network failure, distributed data and operational overhead.

**Q3 🔴 Caching strategy and invalidation?**
🎤 Cache-aside in Redis with TTLs and explicit invalidation after commits, versioned keys, jittered TTLs and single-flight locks against stampedes; HTTP caching with ETags/Cache-Control for clients and CDNs. Decide acceptable staleness per data type and never skip authorization on cache hits.

**Q4 🔴 How do you make POST requests safe to retry?**
🎤 Idempotency keys: the client sends a unique key; the server stores key + request hash + response under a unique constraint. Retries with the same key return the stored response; a different payload returns 422; in-progress returns 409. Plus natural unique constraints and idempotent consumers for events.

**Q5 🔴 How do you call unreliable third-party APIs?**
🎤 Shared `httpx.AsyncClient` with connect and read timeouts, retries with exponential backoff and jitter only for idempotent or keyed operations, circuit breaker, bulkhead/semaphore, fallbacks or cached data, mapping failures to 502/503/504, and metrics per dependency.

**Q6 🔴 How do you guarantee an event is published after a DB write?**
🎤 Transactional outbox: write the business change and an outbox row in the same transaction; a relay publishes outbox rows to the broker and marks them sent. Consumers are idempotent because delivery is at-least-once.

**Q7 🔴 What do you monitor?**
🎤 RED per endpoint (rate, errors, p50/p95/p99 duration), saturation (DB pool usage, CPU, memory, queue depth, event-loop lag), business KPIs, and dependency health; structured logs with request/trace IDs; distributed traces with OpenTelemetry; SLO-based burn-rate alerts.

**Q8 🔴 How do you handle a multi-tenant SaaS API?**
🎤 Tenant resolved from the token; every query scoped by `tenant_id` (enforced in a base repository or Postgres Row-Level Security); per-tenant rate limits and quotas; indexes leading with `tenant_id`; options from shared schema → schema-per-tenant → DB-per-tenant depending on isolation needs.

---

## 13.11 Scenario & Debugging Questions

**S1. "The API is fast alone, but under load every endpoint becomes slow — even `/health`."**
🎤 Classic sign of a blocked event loop. Look for sync I/O or CPU work inside `async def` (requests, time.sleep, sync DB driver, big JSON processing). Confirm with py-spy or asyncio debug mode. Fix by making the code async, moving it to `def`, or offloading to a threadpool/process/worker.

**S2. "Intermittent `QueuePool limit of size 5 overflow 10 reached, connection timed out`."**
🎤 Pool exhaustion. Check for sessions not closed (missing `finally`), long transactions (external calls inside transactions), threadpool concurrency higher than the pool, slow queries holding connections. Fix leaks, shorten transactions, align pool size with concurrency, add PgBouncer, index slow queries.

**S3. "`MissingGreenlet: greenlet_spawn has not been called` with async SQLAlchemy."**
🎤 A lazy load happened in async context — usually a response model touching an unloaded relationship or an expired attribute after commit. Eager-load with `selectinload`, set `expire_on_commit=False`, or use `AsyncAttrs`.

**S4. "Users occasionally see other users' data."**
🎤 Check for IDOR (missing ownership filters), caching keyed without user/tenant, shared mutable globals or module-level state across requests, context variables leaking, and CDN caching authenticated responses (`Cache-Control: private`/`no-store`). Add tests for cross-user access.

**S5. "After deploy, a migration locked the users table and the site went down."**
🎤 A blocking DDL (e.g., index without `CONCURRENTLY`, column rewrite) waited behind or blocked traffic. Immediate: cancel the migration. Prevention: `lock_timeout`, concurrent index creation, expand/contract, backfills in batches, testing on production-sized data, `--sql` review.

**S6. "Swagger shows a 422 for a request that looks right."**
🎤 Read the `loc`: maybe the param is expected in the body but sent as a query (or vice versa), a single model got embedded, wrong `Content-Type` (form vs JSON), a list query param missing `Query()`, or a field typo blocked by `extra="forbid"`.

**S7. "Frontend gets CORS errors but curl works."**
🎤 CORS is enforced by browsers only. Check the origin is exactly listed (scheme + host + port), credentials + wildcard misconfig, preflight blocked by auth middleware or a proxy, and that error responses (500s) also carry CORS headers — an unhandled 500 often appears as a CORS error.

**S8. "Duplicate orders are being created."**
🎤 Client or proxy retries on timeouts, double-clicks, or at-least-once consumers. Add idempotency keys, a unique constraint on a natural key, upserts, and dedupe in consumers.

**S9. "Memory keeps growing in production."**
🎤 Unbounded in-process caches (`lru_cache` without maxsize on parameterized functions), accumulating global lists (connection managers), large responses loaded into memory instead of streamed, creating clients per request. Use tracemalloc/memray, cap caches, stream, and reuse clients.

**S10. "JWT works locally but every request is 401 in production."**
🎤 Different `JWT_SECRET_KEY` across replicas or environments, clock skew affecting `exp/nbf` (add leeway), algorithm mismatch, proxy stripping the `Authorization` header, or `tokenUrl`/prefix mismatch.

**S11. "Tests pass individually but fail together."**
🎤 Shared state: data left in DB, module-level globals, dependency overrides not cleared, cached settings. Use per-test transaction rollback, clear `dependency_overrides`, reset caches, avoid global mutable state.

**S12. "Background email task sometimes never sends."**
🎤 `BackgroundTasks` are in-process — lost on restarts and deploys or if an exception is swallowed. Move to a durable queue with retries, and use the outbox pattern so the job is created atomically with the DB change.

---

## 13.12 Common Mistakes & How to Explain the Correct Approach

| Mistake | Correct approach (say this) |
|---|---|
| Blocking call in `async def` | "I keep async code non-blocking; blocking libs go in `def` or a threadpool." |
| Returning ORM objects without `response_model` | "Every endpoint has an output schema, so sensitive fields can't leak." |
| One global session | "Session per request via a `yield` dependency; engine per app." |
| `create_all` in production | "Schema changes go through reviewed Alembic migrations." |
| Logic in routers | "Routers are thin; services own rules and transactions; easy to unit test." |
| Using `HTTPException` in services | "Services raise domain errors; handlers map them to HTTP." |
| Long-lived JWTs, no refresh | "Short access tokens plus rotating, revocable refresh tokens." |
| Only checking role, not ownership | "RBAC plus object-level checks scoped in queries — prevents IDOR." |
| `allow_origins=["*"]` with credentials | "Explicit origins per environment." |
| No timeouts on HTTP calls | "Every external call has timeouts, bounded retries and a breaker." |
| Retrying non-idempotent POSTs | "Retries only for idempotent operations or with idempotency keys." |
| Running migrations in every container | "One migration job before rollout, backward-compatible schema changes." |
| Hardcoded secrets | "Settings from env + secret manager, `SecretStr`, rotation." |
| `@app.on_event` | "Lifespan context manager — `on_event` is deprecated." |
| passlib / python-jose in new code | "pwdlib with Argon2 and PyJWT — the maintained options FastAPI's docs use." |
| Offset pagination on huge tables | "Keyset pagination with an opaque cursor." |
| Testing against SQLite for Postgres features | "Integration tests run against the same DB engine as production." |

---

## 13.13 Practical Coding Exercises (with solutions)

### Exercise 1 🟢 — Validated endpoint
*Create `POST /users` accepting `email`, `age` (18–120), `username` (3–20 chars, alphanumeric). Return 201 with the user minus `password`.*
```python
from pydantic import BaseModel, EmailStr, Field

class UserIn(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9]+$")
    age: int = Field(ge=18, le=120)
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    age: int

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    return {"id": 1, **user.model_dump(exclude={"password"})}
```
**Explain:** constraints live in the schema → automatic 422; `response_model` guarantees no password in output.

### Exercise 2 🟡 — Reusable pagination dependency with total
```python
from typing import Annotated, Generic, TypeVar
from fastapi import Depends, Query
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int

class PageParams(BaseModel):
    page: int
    size: int
    @property
    def offset(self) -> int: return (self.page - 1) * self.size

def page_params(page: Annotated[int, Query(ge=1)] = 1,
                size: Annotated[int, Query(ge=1, le=100)] = 20) -> PageParams:
    return PageParams(page=page, size=size)

@app.get("/items", response_model=Page[ItemOut])
def items(p: Annotated[PageParams, Depends(page_params)], db: DbSession):
    total = db.scalar(select(func.count(Item.id)))
    rows = db.scalars(select(Item).order_by(Item.id).offset(p.offset).limit(p.size)).all()
    return Page(items=rows, total=total, page=p.page, size=p.size)
```

### Exercise 3 🟡 — Fix the N+1
```python
# BEFORE: 1 + N queries
posts = db.scalars(select(Post)).all()
return [{"title": p.title, "author": p.author.name, "tags": [t.name for t in p.tags]} for p in posts]

# AFTER: 3 queries total regardless of N
posts = db.scalars(
    select(Post).options(joinedload(Post.author), selectinload(Post.tags))
).unique().all()
```

### Exercise 4 🟡 — Owner-only dependency
```python
def get_owned_note(note_id: int, user: CurrentUser, db: DbSession) -> Note:
    note = db.scalar(select(Note).where(Note.id == note_id, Note.owner_id == user.id))
    if note is None:
        raise HTTPException(404, "Note not found")
    return note

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note: Annotated[Note, Depends(get_owned_note)], db: DbSession):
    db.delete(note); db.commit()
```
**Explain:** ownership enforced in the query; 404 hides existence; reusable across GET/PATCH/DELETE.

### Exercise 5 🟡 — Async fan-out with timeout and partial failure
```python
import asyncio, httpx

async def fetch_all(client: httpx.AsyncClient, urls: list[str]) -> dict[str, dict | None]:
    sem = asyncio.Semaphore(5)

    async def one(url: str):
        async with sem:
            try:
                async with asyncio.timeout(2):
                    r = await client.get(url)
                    r.raise_for_status()
                    return url, r.json()
            except (httpx.HTTPError, TimeoutError):
                return url, None             # degrade gracefully

    results = await asyncio.gather(*(one(u) for u in urls))
    return dict(results)
```

### Exercise 6 🟡 — Simple in-memory token-bucket rate limiter (per process)
```python
import time
from dataclasses import dataclass, field
from fastapi import HTTPException, Request

@dataclass
class Bucket:
    tokens: float
    updated: float = field(default_factory=time.monotonic)

RATE, CAPACITY = 1.0, 5          # 1 token/sec, burst 5
buckets: dict[str, Bucket] = {}

def token_bucket(request: Request) -> None:
    key = request.client.host if request.client else "anon"
    now = time.monotonic()
    b = buckets.setdefault(key, Bucket(tokens=CAPACITY))
    b.tokens = min(CAPACITY, b.tokens + (now - b.updated) * RATE)
    b.updated = now
    if b.tokens < 1:
        raise HTTPException(429, "Too many requests", headers={"Retry-After": "1"})
    b.tokens -= 1
```
**Discuss:** per-process only → use Redis (Lua script) for multiple workers; memory growth → evict idle keys.

### Exercise 7 🔴 — Idempotent POST (outline)
See Chapter 8 §8.12 — explain: unique (key, user) row, request hash, stored response, 409 in-progress, 422 mismatched payload, TTL cleanup.

### Exercise 8 🟡 — Test with dependency override
```python
def test_create_note_as_fake_user():
    app.dependency_overrides[get_current_user] = lambda: User(id=1, email="t@t.com", role="user")
    try:
        r = TestClient(app).post("/notes", json={"text": "hi"})
        assert r.status_code == 201
    finally:
        app.dependency_overrides.clear()
```

### Exercise 9 🟡 — Write the migration for a rename safely
```python
def upgrade():
    op.alter_column("users", "name", new_column_name="full_name")
def downgrade():
    op.alter_column("users", "full_name", new_column_name="name")
```
**Explain:** autogenerate would emit drop+add (data loss). For zero downtime with rolling deploys, use expand/contract instead of an in-place rename.

### Exercise 10 🔴 — Design question: "Design a URL shortener API with FastAPI"
Outline answer:
- **API:** `POST /links {url, custom_alias?, expires_at?}` → 201 `{code, short_url}`; `GET /{code}` → 307/301 redirect; `GET /links/{code}/stats`.
- **Data:** `links(code PK, url, owner_id, created_at, expires_at, clicks)`; code = base62 of a unique ID (or random 7 chars + unique constraint + retry).
- **Read path (hot):** Redis cache `code → url` (TTL), CDN for redirects; DB on miss. Reads ≫ writes.
- **Clicks:** don't update the DB per redirect; publish events to a queue/stream → batch aggregate.
- **Security:** validate URLs (scheme allow-list, malware lists), rate-limit creation, auth for custom aliases.
- **Scale:** stateless API pods, Redis cluster, Postgres primary + replicas; partition analytics by time.
- **Trade-offs:** 301 (cacheable, less analytics) vs 307/302 (counted); random vs sequential codes (enumeration).
