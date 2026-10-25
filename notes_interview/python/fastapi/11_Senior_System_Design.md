# Chapter 11 — Senior-Level System Design

> **Goal:** Think like a senior/staff engineer: design maintainable, scalable APIs, choose architectures deliberately, handle failures and high traffic, build observability in, and review code for maintainability, security and performance.

---

## 11.1 Designing Maintainable and Scalable REST APIs

**Contract first**
- Design the OpenAPI contract (resources, schemas, errors, pagination) and review it with consumers *before* coding.
- Consistent conventions document: naming, casing (`snake_case` JSON is common in Python shops; pick one), timestamps (ISO-8601 UTC), IDs (opaque strings/UUIDs externally), money (integer minor units or decimal strings), error format (RFC 9457), pagination (cursor), filtering syntax.
- Generate client SDKs from OpenAPI; run contract tests in CI; detect breaking changes (`oasdiff`).

**Evolvability**
- Additive changes only within a version; deprecation policy with `Sunset` headers and telemetry on old version usage.
- Expand/contract for both API fields and DB columns.
- Feature flags to roll out behavior gradually.

**Scalability by design**
- **Stateless** API servers (state in DB/Redis/object storage) → horizontal scaling is trivial.
- Every list endpoint paginated with a hard maximum.
- Long operations are async jobs (202 + status resource).
- Idempotent writes (Idempotency-Key), natural unique constraints.
- Bulk endpoints where clients would otherwise make N calls.

**IDs:** auto-increment ints leak volume and enable enumeration; UUIDv7/ULID are sortable by time and index-friendly → good external IDs.

---

## 11.2 Monolith vs Microservices

| | Modular monolith | Microservices |
|---|---|---|
| Deploy | One unit | Many independent units |
| Complexity | Low ops, in-process calls | High: network, discovery, distributed data, tracing |
| Data consistency | ACID transactions across modules | Eventual consistency, sagas |
| Team scaling | Fine to ~a few teams with module boundaries | Independent teams own services |
| Scaling | Scale whole app | Scale hot services independently |
| Failure isolation | One bug can take down all | Better isolation (if designed well) |
| Tech diversity | One stack | Per-service choices |
| Best for | Startups, most products, unclear domains | Large orgs, clear bounded contexts, different scaling/SLA needs |

🎤 *"I'd start with a modular monolith: feature-based modules with clear interfaces and no cross-module table access. When a module has a clear bounded context and a real reason — independent scaling, team autonomy, different release cadence — it can be extracted into a service. Microservices trade code complexity for operational complexity; the distributed-systems tax has to be worth it."*

Signals to split: independent scaling needs, team contention on deploys, different availability/security requirements, domain clearly separable.

---

## 11.3 Service-to-Service Communication

| Style | Tech | Use when | Trade-offs |
|---|---|---|---|
| Sync request/response | REST (httpx), gRPC | Need an immediate answer | Temporal coupling; cascading failures; latency adds up |
| Async messaging (queue) | RabbitMQ, SQS, Redis Streams | Commands/work distribution | Eventual consistency; need idempotent consumers |
| Async events (pub/sub, log) | Kafka, SNS, NATS, Pub/Sub | Broadcast facts to many consumers, event sourcing, analytics | Ordering, schema evolution, replay |

**gRPC vs REST internally:** gRPC = binary Protobuf, HTTP/2, streaming, strong contracts, faster; REST = universal, debuggable, browser-friendly.

**Reliability patterns:** timeouts on every call, retries with backoff+jitter (idempotent only), circuit breakers, bulkheads, fallbacks, **deadline propagation** (pass remaining time budget downstream), correlation IDs.

**Distributed transactions:** avoid 2PC. Use **sagas**:
```
Order created ─► Reserve inventory ─► Charge payment ─► Confirm order
                    ▲ failure? compensate: release inventory, cancel order
```
- Orchestration (central coordinator, e.g., Temporal) vs choreography (services react to events).
- **Transactional outbox** + **idempotent consumers (inbox)** guarantee "exactly-once effect" on top of at-least-once delivery.

---

## 11.4 API Gateways and Authentication Boundaries

```
Clients ─► CDN/WAF ─► API Gateway ─────────────► Service A (FastAPI)
                       • TLS termination          Service B
                       • AuthN (validate JWT/API key)
                       • Rate limiting, quotas
                       • Routing, versioning, request size limits
                       • Request ID, logging
```
- Gateway does **coarse** checks (valid token, rate limits); services still do **fine-grained authorization** (ownership, permissions) — never trust only the edge (zero-trust).
- Internal calls: propagate the user's token (or a signed internal token with user context), plus **service identity** (mTLS via service mesh like Istio/Linkerd, or OAuth2 client credentials).
- **BFF (Backend for Frontend):** a thin API per client type (web/mobile) that aggregates services and handles browser-session cookies, keeping tokens away from JS.
- Options: Kong, AWS API Gateway, Apigee, Envoy, Traefik, NGINX.

---

## 11.5 Database Indexing and Performance Tuning

**Index types (Postgres)**
| Type | Use |
|---|---|
| B-tree (default) | Equality, ranges, sorting |
| Composite `(a, b)` | Queries filtering by `a` (and `b`); leftmost-prefix rule |
| Partial `WHERE deleted_at IS NULL` | Index only hot subset |
| Covering `INCLUDE (col)` | Index-only scans |
| GIN | JSONB, arrays, full-text search |
| BRIN | Huge append-only time-series |
| Unique | Integrity + lookup |
| Expression `lower(email)` | Case-insensitive lookups |

**Trade-offs:** indexes speed reads but slow writes and take space; unused indexes are pure cost (`pg_stat_user_indexes`).

**Tuning workflow:** `pg_stat_statements` → top queries by total time → `EXPLAIN (ANALYZE, BUFFERS)` → add/adjust index or rewrite query → verify.

**Scaling the database:**
1. Optimize queries + indexes + connection pooling (PgBouncer).
2. Vertical scale (bigger instance).
3. **Read replicas** — route reads there (accept replication lag; read-your-writes from primary).
4. Caching layer.
5. **Partitioning** (by time/tenant) for huge tables.
6. **Sharding** (by tenant/user id) — last resort; complicates queries and transactions.
7. CQRS: separate write model from read-optimized projections (e.g., Elasticsearch for search).

---

## 11.6 Connection Pooling and Resource Management

- Every process holds a pool → total connections = instances × workers × (pool_size + max_overflow). Postgres connections are expensive (~process each).
- Use **PgBouncer**/RDS Proxy in transaction mode for many instances or serverless.
- Bound everything: DB pool, HTTP client pools, threadpool size, semaphores per downstream, queue consumer prefetch.
- Timeouts at every layer: client → gateway → app → DB (`statement_timeout`) — inner timeouts shorter than outer.
- Backpressure: when saturated, **fail fast** (503/429) rather than queue unboundedly (queues hide overload until latency explodes).

---

## 11.7 Caching Strategies and Distributed Systems Basics

| Strategy | Read | Write | Notes |
|---|---|---|---|
| **Cache-aside** (lazy) | App checks cache → DB on miss → fill | Write DB, invalidate cache | Most common |
| Read-through | Cache library loads from DB | — | Simpler app code |
| Write-through | — | Write cache + DB synchronously | Fresh cache, slower writes |
| Write-behind | — | Write cache, async flush to DB | Fast, risk of loss |
| Refresh-ahead | Refresh before TTL expiry | — | Avoid stampedes on hot keys |

**Where:** browser/CDN (static & public GETs) → gateway → app in-memory → Redis → DB.

**Hard parts:** invalidation (event-driven deletes, short TTLs, versioned keys), stampede (locks/single-flight, jittered TTL), consistency (decide acceptable staleness per data type), hot keys (local cache layer, key replication).

**Distributed-systems vocabulary**
| Term | Meaning |
|---|---|
| CAP | Under a network partition you choose Consistency or Availability |
| PACELC | Else (no partition) choose Latency vs Consistency |
| Eventual consistency | Replicas converge over time |
| Idempotency | Repeating an operation has the same effect |
| At-least-once / at-most-once / exactly-once | Delivery guarantees; "exactly-once" = at-least-once + idempotent processing |
| Consensus | Raft/Paxos (etcd, ZooKeeper) for leader election, config |
| Distributed lock | Redis (`SET NX PX`, with fencing tokens) / DB advisory locks |
| Clock skew | Don't rely on wall clocks across machines for ordering |

---

## 11.8 Horizontal Scaling and Load Balancing

```
                    ┌──► pod 1 (uvicorn) ─┐
Internet ─► LB ─────┼──► pod 2            ├──► PgBouncer ─► Postgres primary ─► replicas
                    └──► pod N            ┘           Redis (cache, rate limits, pub/sub)
                                                     Queue ─► workers (autoscaled by queue depth)
```
- Requirements: stateless app, shared session/state store, externalized files (S3), idempotent startup.
- LB algorithms: round robin, least connections, consistent hashing (sticky for caches/WebSockets).
- L4 (TCP) vs L7 (HTTP-aware: path routing, headers, TLS).
- **Autoscaling:** CPU/RPS/latency (HPA), queue depth for workers (KEDA). Scale-out must not overwhelm the DB → connection pooler + max replicas.
- Vertical vs horizontal: vertical is simpler but bounded; horizontal needs statelessness but scales further and improves availability.
- Multi-AZ for availability; multi-region for latency/DR (complex data replication).

---

## 11.9 Observability: Logs, Metrics, Traces

| Pillar | Answers | Tools |
|---|---|---|
| **Logs** | What happened in detail? | structlog JSON → Loki / ELK / CloudWatch |
| **Metrics** | How much / how fast / how often? Trends & alerts | Prometheus + Grafana, Datadog |
| **Traces** | Where did time go across services? | OpenTelemetry → Jaeger / Tempo / Honeycomb |

**Golden signals / RED method** per endpoint: **Rate**, **Errors**, **Duration** (p50/p95/p99), plus **Saturation** (pool usage, CPU, queue depth).

Metrics with Prometheus:
```python
# pip install prometheus-fastapi-instrumentator
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
```
Custom business metric:
```python
from prometheus_client import Counter
ORDERS = Counter("orders_created_total", "Orders created", ["plan"])
ORDERS.labels(plan="pro").inc()
```
⚠️ Keep label cardinality low (no user IDs/URLs with IDs as labels).

Tracing with OpenTelemetry (programmatic):
```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
FastAPIInstrumentor.instrument_app(app, excluded_urls="health,metrics")
SQLAlchemyInstrumentor().instrument(engine=engine)
HTTPXClientInstrumentor().instrument()
```
Correlate: put `trace_id` into every log line → jump from a log to its trace.

**SLI/SLO/SLA:** SLI = measured indicator (99.2% requests < 300 ms); SLO = target (99.5%/30 days); SLA = contractual promise. **Error budget** = 1 − SLO → governs release velocity. Alert on **symptoms** (SLO burn rate), not causes (CPU 80%).

---

## 11.10 High Traffic, Failures, Retries, Duplicate Requests

| Problem | Techniques |
|---|---|
| Traffic spikes | Autoscaling, caching/CDN, queue-based load leveling, rate limits, graceful degradation (disable non-critical features) |
| Slow dependency | Timeouts, circuit breaker, bulkhead, fallback/cached data, async processing |
| Retry storms | Exponential backoff + jitter, retry budgets, only retry idempotent ops, honor `Retry-After` |
| Duplicate requests | Idempotency keys, unique constraints, upserts, dedupe tables for events |
| Thundering herd on cache expiry | Jittered TTL, single-flight lock, stale-while-revalidate |
| Partial failures (DB ok, email failed) | Outbox, sagas with compensation, retries from queue, DLQ |
| Poison messages | Max retries → dead-letter queue + alert |
| Cascading failure | Load shedding (503 early), backpressure, isolate thread/connection pools |
| Data loss | Backups + PITR, tested restores, multi-AZ |
| Hot partition / hot key | Key spreading, local caching, sharding changes |

**Graceful degradation example:** recommendations service down → return product page without recommendations instead of 500.

---

## 11.11 Architecture Trade-offs and Design Decisions

Senior engineers make trade-offs **explicit** — write **ADRs (Architecture Decision Records)**:
```markdown
# ADR-007: Use cursor pagination for /events
Status: Accepted (2026-10-25)
Context: /events has 200M rows; offset pagination p95 = 4s on deep pages.
Decision: Keyset pagination on (created_at, id); opaque base64 cursor; no total count.
Consequences: + constant-time pages, stable under inserts. − no "jump to page N"; UI changes needed.
Alternatives: offset + caching (rejected: still O(n)), search index (overkill now).
```

Common decisions & trade-offs:
| Decision | Option A | Option B | Lean |
|---|---|---|---|
| Sync vs async stack | Sync SQLAlchemy + `def` (simple) | Full async (higher concurrency) | Async when I/O fan-out is heavy; else sync is fine |
| ORM vs raw SQL | Productivity, safety | Control, performance | ORM + raw SQL for hot/report queries |
| JWT vs opaque session tokens | Stateless, scales, hard to revoke | Revocable, needs lookup (Redis) | Short JWT + revocable refresh |
| REST vs GraphQL vs gRPC | Simple, cacheable | Flexible client queries | Internal high-perf | REST public, gRPC internal if needed |
| Consistency vs availability | Strong (single DB tx) | Eventual (events) | Strong within service, eventual across |
| Build vs buy (auth, search, queues) | Control | Speed, reliability | Buy undifferentiated heavy lifting |

Framework for design interviews: **requirements (functional + non-functional: QPS, latency, availability, data size) → API design → data model → high-level architecture → deep dives (scaling, caching, consistency, failure modes) → observability & security → trade-offs.**

### Back-of-envelope example
"10M users, 5% DAU-active per hour peak, 20 requests/session"
→ 10M × 0.05 × 20 / 3600 ≈ **2,800 RPS peak**. If one Uvicorn worker does ~500 RPS for this workload (measure!), need ~6 workers + headroom ×2 → 12 workers ≈ 3–4 pods × 4 workers. DB: 2,800 RPS with 80% cache hits → ~560 QPS to Postgres → single primary + replica is fine.

---

## 11.12 Reviewing Code (Senior Checklist)

**Correctness & design**
- [ ] Logic in the right layer (thin routers, services own rules/transactions)?
- [ ] Clear names, small functions, no duplicated business rules?
- [ ] Error paths handled; domain errors mapped consistently?
- [ ] Backward-compatible API & schema changes? Migration reviewed (renames, locks, backfills)?

**Security**
- [ ] AuthN on every non-public route; ownership/permission checks (IDOR)?
- [ ] Input schemas forbid server-owned fields; response models hide sensitive fields?
- [ ] No string-built SQL; identifiers whitelisted?
- [ ] Secrets from settings; nothing sensitive logged?
- [ ] External URLs validated (SSRF); uploads size/type-checked?

**Performance & reliability**
- [ ] N+1 queries? Indexes for new filters/sorts? Pagination limits?
- [ ] Blocking calls inside `async def`?
- [ ] Timeouts/retries on external calls; retries only for idempotent operations?
- [ ] Transactions short; side effects after commit?
- [ ] Resources created once (clients/pools), closed on shutdown?

**Operability & tests**
- [ ] Logs with context (request ID), metrics for new features?
- [ ] Tests for happy path, validation, auth, edge cases; deterministic?
- [ ] Config via settings; feature flag for risky changes?
- [ ] Docs/OpenAPI descriptions updated?

How to give review feedback: explain the *why*, distinguish blocking vs nit, suggest concrete code, praise good patterns.

---

## ✅ Quick Revision — Chapter 11

- Contract-first, consistent conventions, additive evolution, stateless servers.
- Modular monolith first; microservices when boundaries & scaling needs are clear.
- Sync calls need timeouts/retries/breakers; async messaging needs idempotent consumers + outbox; sagas over 2PC.
- Gateway = coarse auth & limits; services = fine-grained authz (zero trust).
- DB: indexes (composite/partial/GIN), `EXPLAIN ANALYZE`, pooler, replicas, partitioning, sharding last.
- Cache-aside + invalidation + stampede protection.
- Horizontal scale behind LB; autoscale; protect DB.
- Observability: logs + metrics (RED) + traces (OTel); SLOs & error budgets.
- Failures: backoff+jitter, idempotency, DLQ, load shedding, graceful degradation.
- Write ADRs; state trade-offs explicitly.
