# System Design Fundamentals — Phase 2 Notes

> **Days 8–14 | Audience:** Backend developers with 1–6 years of experience  
> **Purpose:** Interview preparation & quick revision  
> **Stack context:** Java / Spring Boot

---

## Table of Contents

1. [Day 8 — System Design Basics](#day-8--system-design-basics)
2. [Day 9 — Capacity Estimation](#day-9--capacity-estimation)
3. [Day 10 — API & Communication Design](#day-10--api--communication-design)
4. [Day 11 — Databases](#day-11--databases)
5. [Day 12 — Caching](#day-12--caching)
6. [Day 13 — Scalability](#day-13--scalability)
7. [Day 14 — Load Balancing & Consistency](#day-14--load-balancing--consistency)
8. [Interview Q&A](#interview-qa)

---

## Day 8 — System Design Basics

> **Theme:** Think before you draw. Requirements drive everything.

---

### The System Design Interview Framework

Always follow this order — interviewers reward structured thinking over jumping to solutions.

```
1. Clarify requirements      (2–3 min)
2. State constraints         (1–2 min)
3. Estimate capacity         (3–5 min)
4. Design high-level         (5–10 min)
5. Deep dive components      (10–15 min)
6. Address bottlenecks       (5 min)
```

---

### Functional vs Non-Functional Requirements

This is the **most important first step** in any system design. Never skip it.

#### Functional Requirements (What the system does)

These define **features and behavior** — the "what."

Examples for a URL Shortener:
- Users can submit a long URL and get a short URL
- Visiting the short URL redirects to the original
- Users can optionally set a custom alias
- Links expire after 1 year by default

> **Interview tip:** Ask "what does this system need to do?" and list 3–5 core features. Then confirm scope: "Should I focus on the core shortening and redirect flow?"

#### Non-Functional Requirements (How the system behaves)

These define **quality attributes** — the "how well."

| NFR | Description | Example |
|---|---|---|
| **Availability** | System uptime | 99.99% = ~52 min downtime/year |
| **Latency** | Response time | Redirect < 10ms |
| **Throughput** | Requests per second | 10,000 QPS reads |
| **Durability** | Data not lost | URLs stored for 5 years |
| **Consistency** | Same data everywhere | Eventual is OK for URL reads |
| **Scalability** | Grows with load | 100M users without redesign |
| **Security** | Access control | No malicious URL hosting |

> **Interview tip:** Always call out the top 2–3 NFRs that will drive your design decisions. "This is a read-heavy system, so I'll optimize for low-latency reads over write throughput."

---

### Constraints & Assumptions

State these explicitly before designing. This shows senior-level thinking.

**Common constraints to clarify:**

| Constraint | Why It Matters |
|---|---|
| Read vs write ratio | Drives DB and caching strategy |
| Global vs regional | Drives CDN and data replication needs |
| Consistency requirement | Drives choice of SQL vs NoSQL |
| Budget / team size | Affects complexity of solution |
| Existing tech stack | May limit choices |

**Examples of good assumptions to state:**
- "I'll assume 100M daily active users."
- "I'll assume reads are 100x more frequent than writes."
- "I'll assume eventual consistency is acceptable for analytics."
- "I'll assume we're designing for global scale."

> **Interviewers reward explicit assumptions.** Unstated assumptions lead to a design that solves the wrong problem.

---

### The Trade-offs Mindset ⭐

This is the single most important skill in system design interviews. There is no perfect system — only trade-offs.

**The holy trinity of trade-offs:**

```
        Consistency
            /\
           /  \
          /    \
   Availability ── Partition Tolerance
```

**Common trade-off pairs:**

| Trade-off | Choose A when | Choose B when |
|---|---|---|
| Consistency vs Availability | Banking, payments | Social feeds, analytics |
| Latency vs Durability | CDN, cache | Financial records |
| Cost vs Performance | Startup, MVP | High-traffic production |
| Simplicity vs Scalability | Early stage | Proven product need |
| SQL vs NoSQL | Relations matter | Scale & flexibility |

**How to express trade-offs in interviews:**

> ❌ "I'll use Redis for caching."  
> ✅ "I'll use Redis for caching to reduce DB load on reads. The trade-off is that cache invalidation adds complexity and we may serve stale data for a short window — which is acceptable for this use case."

Always finish a design choice with: **"The trade-off is..."**

---

## Day 9 — Capacity Estimation

> **Theme:** Numbers give your design credibility. Estimate, don't guess.

---

### Why Capacity Estimation Matters

Estimation drives:
- Which DB you choose
- Whether you need caching
- How many servers you need
- Whether a single DB or sharding is required

---

### The Estimation Toolkit

Memorize these approximations:

| Unit | Value |
|---|---|
| 1 KB | 1,000 bytes |
| 1 MB | 1,000 KB |
| 1 GB | 1,000 MB |
| 1 TB | 1,000 GB |
| 1 PB | 1,000 TB |
| Seconds in a day | ~86,400 (use 100,000 for math) |
| Seconds in a month | ~2.5M |
| Seconds in a year | ~30M |

**Latency numbers to know:**

| Operation | Time |
|---|---|
| L1 cache reference | 0.5 ns |
| Main memory reference | 100 ns |
| SSD read | 100 µs |
| HDD read | 10 ms |
| Network round trip (same DC) | 0.5 ms |
| Network round trip (cross-region) | 150 ms |

---

### The Estimation Formula

```
Daily Active Users (DAU)
    ↓
Actions per user per day
    ↓
Total requests per day
    ↓
QPS = Total requests / 86,400
    ↓
Peak QPS ≈ QPS × 2-3 (rule of thumb)
    ↓
Storage = requests × data size per request × retention period
    ↓
Bandwidth = QPS × average response size
```

---

### Practice: URL Shortener Estimation ⭐

#### Assumptions
- 100M daily active users
- Each user creates 1 short URL per day (write)
- Each user visits 10 short URLs per day (read)
- Average URL length = 200 bytes
- Retention period = 5 years
- Read : Write ratio = 10:1

#### Step 1 — QPS

```
Write QPS:
  100M users × 1 write/day = 100M writes/day
  100M / 86,400 ≈ 1,200 writes/second
  Peak write QPS ≈ 2,400/sec

Read QPS:
  100M users × 10 reads/day = 1B reads/day
  1B / 86,400 ≈ 11,500 reads/second
  Peak read QPS ≈ 23,000/sec
```

#### Step 2 — Storage

```
Per URL record:
  Short URL:       7 bytes
  Long URL:        200 bytes
  User ID:         8 bytes
  Created at:      8 bytes
  Expires at:      8 bytes
  Total per row ≈  ~250 bytes

Daily new records: 100M
Storage per day:   100M × 250 bytes = 25 GB/day
Storage for 5 yrs: 25 GB × 365 × 5 ≈ 45 TB
```

#### Step 3 — Bandwidth

```
Write bandwidth:
  1,200 writes/sec × 200 bytes = 240 KB/sec ≈ trivial

Read bandwidth:
  11,500 reads/sec × 200 bytes (response) = 2.3 MB/sec
  Peak: ~5 MB/sec ← manageable
```

#### Step 4 — Cache Estimation

```
Follow Pareto's law: 20% of URLs get 80% of traffic
Cache the hot 20%:
  Daily reads: 1B
  Cache 20% of unique URLs: 100M × 0.2 × 250 bytes = 5 GB/day
  → A single Redis node (32 GB RAM) can handle this comfortably
```

#### Summary Table

| Metric | Value |
|---|---|
| Write QPS | ~1,200 (peak 2,400) |
| Read QPS | ~11,500 (peak 23,000) |
| Storage (5 yrs) | ~45 TB |
| Read Bandwidth | ~2.3 MB/s |
| Cache size | ~5 GB/day |
| Bottleneck | Reads → needs caching + read replicas |

> **Interview insight:** The 10:1 read/write ratio tells you immediately: optimize for reads. Use a cache. Add read replicas. Design the redirect path to be sub-10ms.

---

### Estimation for Other Common Systems

| System | Key Metric | Typical Scale |
|---|---|---|
| Twitter/X feed | Tweets per second | ~6,000 tweets/sec |
| WhatsApp | Messages per day | ~100B/day |
| YouTube | Video storage | ~500 hours uploaded/min |
| Uber | Location updates | ~1M location pings/sec |
| Netflix | Bandwidth | ~37% of internet traffic |

---

## Day 10 — API & Communication Design

> **Theme:** APIs are contracts. Break them and you break your users.

---

### REST vs GraphQL

#### REST (Representational State Transfer)

REST maps HTTP verbs to CRUD operations on resources.

```
GET    /users/123         → fetch user
POST   /users             → create user
PUT    /users/123         → replace user
PATCH  /users/123         → partial update
DELETE /users/123         → delete user
```

**REST characteristics:**
- Stateless — each request contains all needed context
- Resource-based — URLs represent nouns, not verbs
- Uses HTTP status codes semantically (200, 201, 404, 400, 500…)
- Cacheable responses by default (GET is idempotent)

**When to use REST:**
- CRUD operations on well-defined resources
- Public APIs consumed by many different clients
- Simple data access patterns
- Caching is important

#### GraphQL

GraphQL lets clients request exactly the fields they need, in one request.

```graphql
# REST would require 3 calls:
GET /users/123
GET /users/123/orders
GET /orders/456/items

# GraphQL: one call, exactly what you need
query {
  user(id: "123") {
    name
    email
    orders {
      id
      total
      items { name, price }
    }
  }
}
```

**When to use GraphQL:**
- Mobile clients where bandwidth is expensive
- Multiple different clients needing different data shapes
- Complex nested data with many relations
- Rapid frontend iteration without backend changes

#### REST vs GraphQL Comparison

| Feature | REST | GraphQL |
|---|---|---|
| Over-fetching | Common — get whole object | ✅ Fetch only needed fields |
| Under-fetching | Common — multiple requests | ✅ One request for nested data |
| Caching | ✅ Easy — HTTP caching | Harder — all POST to /graphql |
| Learning curve | Low | Higher |
| Tooling / adoption | Mature, universal | Growing |
| API versioning | Needed (v1, v2) | Schema evolution — less needed |
| Best for | Public APIs, CRUD | Complex frontends, mobile |

---

### API Versioning

Why versioning exists: APIs are contracts with external consumers. You can't change them without breaking clients.

**Three common strategies:**

#### 1. URL Path Versioning (Most Common)
```
/api/v1/users
/api/v2/users
```
✅ Visible, explicit, easy to route  
❌ URL pollution; clients must migrate

#### 2. Request Header Versioning
```
GET /api/users
Accept: application/vnd.myapi.v2+json
```
✅ Clean URLs  
❌ Less visible; harder to test in browser

#### 3. Query Parameter Versioning
```
GET /api/users?version=2
```
✅ Easy to add  
❌ Easy to forget; messy at scale

> **Best practice:** Use URL path versioning (`/v1/`, `/v2/`) for public APIs. Maintain at least one previous version for a deprecation window (typically 6–12 months). Document what changed.

---

### Pagination

Never return unbounded lists. Always paginate.

#### Offset-Based Pagination
```
GET /users?page=3&limit=20
SQL: SELECT * FROM users LIMIT 20 OFFSET 60
```
✅ Easy to implement; users can jump to any page  
❌ Slow on large offsets (DB must scan to offset); inconsistent if rows are inserted/deleted mid-session

#### Cursor-Based Pagination (Recommended for feeds)
```
GET /posts?cursor=eyJpZCI6MTAwfQ==&limit=20
SQL: SELECT * FROM posts WHERE id > 100 LIMIT 20
```
✅ Fast at any position; stable under inserts/deletes  
❌ Cannot jump to arbitrary pages; cursor must be opaque to clients

#### Keyset Pagination
```
GET /orders?after_id=5000&limit=20
SQL: SELECT * FROM orders WHERE id > 5000 ORDER BY id LIMIT 20
```
Similar benefits to cursor-based; good for ordered data.

> **Rule of thumb:** Use cursor/keyset pagination for feeds and timelines. Use offset for admin UIs where page jumping is needed and dataset is small.

---

### Rate Limiting

**Why it exists:**
- Protect backend from abuse and DDoS
- Enforce fair usage among tenants
- Prevent runaway clients

**Where to apply it:**
- API Gateway (preferred — before any backend load)
- Application layer (for business-specific rules)
- Per user, per IP, or per API key

**Common algorithms:**

| Algorithm | How It Works | Characteristic |
|---|---|---|
| **Token Bucket** | Tokens added at fixed rate; each request consumes one | Allows short bursts |
| **Leaky Bucket** | Requests processed at constant rate; excess queued | Smooth output |
| **Fixed Window** | Count requests per time window (e.g., per minute) | Simple; prone to boundary spikes |
| **Sliding Window** | Weighted average across current and previous window | Smoother than fixed window |

**HTTP Response for rate-limited requests:**
```
HTTP 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1700000000
```

---

### Idempotency in APIs

An operation is **idempotent** if calling it once or multiple times produces the same result.

| Method | Idempotent | Safe (no side effects) |
|---|---|---|
| GET | ✅ | ✅ |
| HEAD | ✅ | ✅ |
| PUT | ✅ | ❌ |
| DELETE | ✅ | ❌ |
| POST | ❌ | ❌ |
| PATCH | ❌ (usually) | ❌ |

**Implementing idempotency for POST:**
```
POST /payments
Idempotency-Key: client-generated-uuid-12345

Server behavior:
1. Check if key exists in idempotency store
2. If yes → return stored response (no re-execution)
3. If no  → execute, store result with key, return response
```

**Storage:** Redis with TTL (e.g., 24 hours) is a common choice for the idempotency key store.

> **Why this matters:** Retries are inevitable in distributed systems. Without idempotency, retries cause double charges, duplicate orders, and data corruption.

---

## Day 11 — Databases

> **Theme:** Choose the right database for the access pattern, not out of habit.

---

### SQL vs NoSQL

#### SQL (Relational Databases)

Examples: PostgreSQL, MySQL, Oracle

**Characteristics:**
- Structured schema — tables, rows, columns
- ACID transactions guaranteed
- Powerful joins across related data
- Vertical scaling primarily; horizontal is complex
- Strong consistency by default

**Use SQL when:**
- Data has clear relationships (orders → users → products)
- ACID compliance is required (payments, banking)
- Complex queries with joins and aggregations
- Schema is stable and well-defined

#### NoSQL (Non-Relational Databases)

**Four main types:**

| Type | Examples | Best For |
|---|---|---|
| **Document** | MongoDB, Firestore | Flexible schemas, JSON data, user profiles |
| **Key-Value** | Redis, DynamoDB | Sessions, caching, high-speed lookups |
| **Column-Family** | Cassandra, HBase | Time-series, write-heavy, large scale |
| **Graph** | Neo4j, Neptune | Social graphs, recommendations, fraud detection |

**Use NoSQL when:**
- Massive scale (millions of writes/sec)
- Flexible or evolving schema
- No complex joins needed
- High availability > strong consistency
- Specific access patterns (key lookups, time-series)

#### SQL vs NoSQL Comparison

| Feature | SQL | NoSQL |
|---|---|---|
| Schema | Fixed | Flexible |
| Transactions | ✅ ACID | Limited (BASE) |
| Joins | ✅ Powerful | ❌ Limited/manual |
| Horizontal scaling | Hard | ✅ Built for it |
| Consistency | Strong | Eventual (usually) |
| Query flexibility | ✅ SQL | Varies by type |
| Learning curve | Lower | Higher (varies) |

> **Interview answer:** "I'd use PostgreSQL when data integrity and complex relations matter — like an order management system. I'd use Cassandra or DynamoDB when I need to handle millions of writes per second with predictable low latency, like a user activity log."

---

### Indexing

An index is a **data structure that speeds up reads** at the cost of slower writes and extra storage.

**Without index:** Full table scan — O(n)  
**With index:** B-tree or hash lookup — O(log n) or O(1)

#### How Indexes Work (B-Tree)

```
Table: users (10M rows)
Query: SELECT * FROM users WHERE email = 'alice@mail.com'

Without index: scan all 10M rows ❌
With index on email: B-tree lookup → found in microseconds ✅
```

#### Types of Indexes

| Type | Use Case |
|---|---|
| **B-Tree** (default) | Range queries, equality, ORDER BY |
| **Hash** | Exact equality only; faster than B-Tree for point lookups |
| **Composite** | Multiple columns — order matters! |
| **Partial** | Index a subset of rows (e.g., active users only) |
| **Covering** | Index includes all columns the query needs — no table access |
| **Full-Text** | Text search (LIKE, contains) |

#### Composite Index — Column Order Matters

```sql
-- Index: (last_name, first_name)

SELECT * WHERE last_name = 'Smith'              -- ✅ uses index
SELECT * WHERE last_name = 'Smith'
           AND first_name = 'John'              -- ✅ uses index
SELECT * WHERE first_name = 'John'              -- ❌ cannot use index
```

> **Rule:** Index the most selective column first. The leading column must be present in the WHERE clause.

#### Index Trade-offs

| Benefit | Cost |
|---|---|
| Faster reads (SELECT) | Slower writes (INSERT, UPDATE, DELETE) |
| — | Extra storage (can be significant) |
| — | Index maintenance overhead |

> **Don't over-index.** Every index adds write overhead. Index columns that appear in WHERE, JOIN, and ORDER BY clauses with high cardinality.

---

### ACID Transactions

ACID guarantees safe, reliable database transactions.

| Property | Meaning | Example |
|---|---|---|
| **Atomicity** | All operations succeed or all fail | Transfer: debit AND credit, never one alone |
| **Consistency** | DB moves from one valid state to another | Balance never goes negative |
| **Isolation** | Concurrent transactions don't interfere | Two transfers don't corrupt each other |
| **Durability** | Committed data survives failures | Power outage doesn't lose committed data |

---

### Isolation Levels

Isolation levels control the trade-off between **consistency** and **concurrency**. Higher isolation = fewer anomalies = lower concurrency.

#### The Four Anomalies

| Anomaly | Description |
|---|---|
| **Dirty Read** | Read uncommitted data from another transaction |
| **Non-Repeatable Read** | Same row gives different values within one transaction |
| **Phantom Read** | Same query returns different rows within one transaction |
| **Lost Update** | Two transactions overwrite each other's changes |

#### Isolation Levels and What They Prevent

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|---|---|---|---|---|
| **Read Uncommitted** | ❌ Possible | ❌ Possible | ❌ Possible | Fastest |
| **Read Committed** | ✅ Prevented | ❌ Possible | ❌ Possible | Fast |
| **Repeatable Read** | ✅ Prevented | ✅ Prevented | ❌ Possible | Moderate |
| **Serializable** | ✅ Prevented | ✅ Prevented | ✅ Prevented | Slowest |

> **PostgreSQL default:** Read Committed  
> **MySQL InnoDB default:** Repeatable Read  
> **Use Serializable when:** Financial transactions where no anomaly is acceptable.

---

### Read Replicas

**Problem:** One DB node can't handle 50,000 reads/sec.

**Solution:** Add read replicas — copies of the primary DB that serve reads only.

```
Primary DB (writes)
    ↓ replication (async)
Replica 1 (reads) ← application read traffic
Replica 2 (reads) ← application read traffic
Replica 3 (reads) ← analytics / reporting
```

**Characteristics:**
- Replication is usually **asynchronous** — slight lag (milliseconds to seconds)
- Replicas may serve **slightly stale data** — acceptable for most reads
- Primary handles all writes
- Failover: promote a replica to primary if primary fails

**When to use:**
- Read : Write ratio is high (10:1 or more)
- Reporting queries that would slow down the primary
- Geographic distribution — replica in each region

> **Trade-off:** Eventual consistency on reads. A user might see old data for a brief window after a write. Usually acceptable; not acceptable for banking/payments.

---

## Day 12 — Caching

> **Theme:** The fastest request is one that never hits the database.

---

### Why Cache?

| Without Cache | With Cache |
|---|---|
| Every read hits DB | Hot data served from memory |
| DB becomes bottleneck | DB load drops dramatically |
| Higher latency | Sub-millisecond response |
| Scales poorly | Scales cheaply |

**Cache is effective when:**
- Data is read frequently and written infrequently
- Data is expensive to compute (aggregations, joins)
- Slight staleness is acceptable

---

### Cache-Aside (Lazy Loading) ⭐

The application manages the cache manually. Most common pattern.

```
Read flow:
1. Check cache → cache hit? Return value ✅
2. Cache miss → query DB
3. Store result in cache
4. Return value

Write flow:
1. Write to DB
2. Invalidate (delete) the cache entry
   → next read will re-populate from DB
```

```java
public User getUser(String id) {
    User cached = redis.get("user:" + id);
    if (cached != null) return cached;

    User user = userRepository.findById(id);
    redis.setex("user:" + id, 3600, user); // TTL 1 hour
    return user;
}

public void updateUser(User user) {
    userRepository.save(user);
    redis.delete("user:" + user.getId()); // invalidate
}
```

**Pros:** Only caches what's actually requested; DB is the source of truth.  
**Cons:** Cache miss causes 3 operations (check + DB + write to cache); initial cold start is slow.

---

### Write-Through

Every write goes to cache AND DB simultaneously.

```
Write flow:
1. Write to cache
2. Write to DB (synchronously)
3. Return success

Read flow:
1. Check cache → almost always a hit
```

**Pros:** Cache is always up-to-date; no cold start on reads.  
**Cons:** Write latency is higher (two writes); cache fills with data that may never be read.

---

### Write-Behind (Write-Back)

Write to cache immediately; write to DB asynchronously later.

```
Write flow:
1. Write to cache → return immediately ✅ (fast)
2. Async: flush to DB (batched or after delay)
```

**Pros:** Very fast writes; DB write batching reduces load.  
**Cons:** Risk of data loss if cache fails before DB flush; complex to implement correctly.

---

### Cache Strategy Comparison

| Strategy | Read Performance | Write Performance | Consistency | Complexity |
|---|---|---|---|---|
| Cache-Aside | Good (miss on first) | Good | Eventual | Low |
| Write-Through | Excellent | Slower (2 writes) | Strong | Medium |
| Write-Behind | Excellent | Excellent (async) | Weak | High |

---

### Redis ⭐

Redis (Remote Dictionary Server) is the industry-standard in-memory data store.

**Data structures Redis supports:**

| Structure | Use Case |
|---|---|
| **String** | Simple key-value, counters, session tokens |
| **Hash** | Object storage (user profile fields) |
| **List** | Queues, activity feeds |
| **Set** | Unique tags, user relationships |
| **Sorted Set** | Leaderboards, priority queues |
| **Pub/Sub** | Real-time messaging |
| **Streams** | Event logs, message queues |

**Common Redis commands:**
```bash
SET key value EX 3600       # set with 1-hour TTL
GET key                     # get value
DEL key                     # delete
INCR counter                # atomic increment
EXPIRE key 300              # set TTL
TTL key                     # check remaining TTL
HSET user:123 name "Alice"  # hash field set
ZADD leaderboard 1500 "Alice"  # sorted set add
```

**Redis deployment modes:**
- **Standalone:** Single node. Simple; no HA.
- **Sentinel:** Auto-failover to replica if primary dies.
- **Cluster:** Horizontal sharding across nodes. Scales to TB of data.

---

### Cache Eviction Strategies

When cache is full, something must be evicted.

| Strategy | Rule | Best For |
|---|---|---|
| **LRU** (Least Recently Used) | Evict the item unused longest | General purpose — most common |
| **LFU** (Least Frequently Used) | Evict the item accessed least often | Frequency-based access patterns |
| **FIFO** | Evict the oldest item | Simple; often suboptimal |
| **TTL-based** | Evict when time-to-live expires | Time-sensitive data (OTPs, sessions) |
| **Random** | Evict a random item | Rarely used; last resort |

> **Redis default:** `allkeys-lru` or `volatile-lru` depending on config. In most cases, LRU is the right choice.

---

### Cache Consistency Problems

#### Cache Stampede (Thundering Herd)
**Problem:** A popular cache key expires → thousands of simultaneous requests hit the DB.

**Solutions:**
- **Mutex/lock:** First request fetches from DB and repopulates; others wait.
- **Staggered TTL:** Add random jitter to expiry time so not all expire at once.
- **Background refresh:** Refresh the cache before TTL expires (proactive).

#### Stale Data
**Problem:** DB updated but cache still has old value.

**Solutions:**
- Set appropriate TTL
- Explicit invalidation on write
- Event-driven invalidation (DB → event → cache invalidation)

#### Cache Penetration
**Problem:** Requests for non-existent data bypass cache and hammer DB.

**Solution:** Cache null results too (with short TTL). Use Bloom filters to reject invalid keys upfront.

---

## Day 13 — Scalability

> **Theme:** Design for 10x your current load. Build for where you're going, not just where you are.

---

### Vertical vs Horizontal Scaling

#### Vertical Scaling (Scale Up)

Add more resources to the **same machine**: more CPU, RAM, faster SSD.

```
Before: 4 cores, 16 GB RAM
After:  32 cores, 256 GB RAM
```

**Pros:** Simple; no code changes; no distribution complexity.  
**Cons:** Hardware limit — you can't scale forever; single point of failure; expensive at the high end; downtime during upgrade.

#### Horizontal Scaling (Scale Out)

Add **more machines** to distribute load.

```
Before: 1 server
After:  10 servers behind a load balancer
```

**Pros:** Theoretically unlimited scale; fault tolerant (one server dies, others continue); cost-effective with commodity hardware.  
**Cons:** Application must be stateless; data consistency becomes complex; requires load balancing.

#### When to Use Each

| Scenario | Recommendation |
|---|---|
| Early-stage startup | Vertical first — simpler |
| Proven product, growing fast | Horizontal — for scale |
| DB scaling | Vertical first, then read replicas, then sharding |
| Stateless services (APIs) | Horizontal — easy and cheap |
| Stateful services | Harder — extract state to shared store first |

---

### Stateless Services ⭐

A **stateless service** holds no user-specific state in memory. Every request is self-contained.

**Why stateless matters for scaling:**
```
Stateful service:
  User session stored on Server A
  If load balancer routes to Server B → session not found ❌

Stateless service:
  Session stored in Redis
  Any server can handle any request ✅
  Add/remove servers freely
```

**How to make services stateless:**
- Store sessions in Redis or a distributed cache
- Use JWTs (stateless authentication tokens)
- Store uploaded files in object storage (S3), not local disk
- No in-memory state that isn't derived from the request

> **Rule:** If you can kill and restart any instance without users noticing, your service is stateless. That's the goal.

---

### Sharding Strategies

**Sharding** = splitting data across multiple database nodes (horizontal partitioning).

**When to shard:**
- Single DB can't handle write load
- Dataset is too large for one machine
- Need to distribute geographically

#### 1. Range-Based Sharding

Split data by a range of the shard key.

```
Shard 1: user_id 1 – 10M
Shard 2: user_id 10M – 20M
Shard 3: user_id 20M – 30M
```

✅ Easy range queries  
❌ Hotspots — new users go to the last shard; uneven load

#### 2. Hash-Based Sharding

Apply a hash function to the shard key.

```
shard = hash(user_id) % number_of_shards
```

✅ Even distribution; no hotspots  
❌ Range queries are hard; resharding requires moving data

#### 3. Directory-Based Sharding

A lookup service maps each key to its shard.

```
Lookup table:
  user_id 123 → Shard 2
  user_id 456 → Shard 1
```

✅ Maximum flexibility; easy to rebalance  
❌ Lookup service is a bottleneck and single point of failure

#### 4. Geo-Based Sharding

Split data by geography.

```
Shard US:  US users
Shard EU:  European users
Shard APAC: Asia-Pacific users
```

✅ Low latency for regional users; GDPR compliance  
❌ Uneven shard sizes; cross-region queries are expensive

#### Sharding Challenges

| Challenge | Solution |
|---|---|
| Cross-shard joins | Denormalize data; application-level joins |
| Cross-shard transactions | Saga pattern; avoid if possible |
| Resharding | Consistent hashing to minimize data movement |
| Hotspots | Hash-based sharding; add shard key entropy |

> **Interview insight:** Most systems don't need sharding until they're at 10TB+ or millions of writes/sec. Exhaust vertical scaling and read replicas first.

---

### Consistent Hashing

Standard hash sharding breaks when you add/remove nodes — all data must move.

**Consistent hashing** minimizes data movement.

```
Virtual ring: 0 ────────────────── 360°

Nodes placed at positions: A=0°, B=120°, C=240°
Keys hashed to ring positions
Each key → first node clockwise from its position

Adding node D at 60°:
  Only keys between 0° and 60° move from A to D
  All other keys stay put ✅
```

**Used by:** DynamoDB, Cassandra, Memcached distributed clusters, consistent Redis Cluster.

---

## Day 14 — Load Balancing & Consistency

> **Theme:** Traffic distribution and the fundamental limits of distributed systems.

---

### Load Balancing

A load balancer distributes incoming traffic across multiple servers to maximize throughput and avoid overloading any single server.

---

### L4 vs L7 Load Balancers

#### L4 — Transport Layer Load Balancer

Operates at **TCP/UDP level**. Routes packets based on IP address and port only. Cannot see application content.

```
Client → L4 LB → Server
         (sees: IP, port, protocol)
         (cannot see: URLs, headers, cookies)
```

**Characteristics:**
- Very fast — minimal processing
- No SSL termination at this layer (pass-through)
- Cannot route based on URL path or request content
- Examples: AWS NLB, HAProxy (TCP mode)

#### L7 — Application Layer Load Balancer

Operates at **HTTP level**. Can inspect full request — URL, headers, cookies, payload.

```
Client → L7 LB → Server
         (sees: URL path, headers, cookies, content-type)
         (can: SSL terminate, route by path, sticky sessions)
```

**Characteristics:**
- Content-aware routing (route `/api/` to API servers, `/static/` to CDN)
- SSL termination (decrypts HTTPS at LB, forwards HTTP internally)
- Sticky sessions (route user to same server by cookie)
- Can return responses directly (caching at LB level)
- Examples: AWS ALB, Nginx, HAProxy (HTTP mode)

#### L4 vs L7 Comparison

| Feature | L4 | L7 |
|---|---|---|
| Routing basis | IP + Port | URL, headers, cookies |
| SSL termination | ❌ (pass-through) | ✅ |
| Content-based routing | ❌ | ✅ |
| Performance | Faster | Slightly more overhead |
| Observability | Low | High (can log requests) |
| Use case | High-throughput, low-level | Web apps, microservices |

---

### Load Balancing Algorithms

| Algorithm | How It Works | Best For |
|---|---|---|
| **Round Robin** | Requests distributed in rotation | Homogeneous servers, uniform requests |
| **Weighted Round Robin** | Servers with more capacity get more traffic | Heterogeneous server capacities |
| **Least Connections** | Route to server with fewest active connections | Long-lived connections (WebSockets) |
| **IP Hash** | Hash client IP → same server always | Sticky sessions without cookies |
| **Random** | Pick random server | Simple, approximates round robin at scale |

---

### CAP Theorem ⭐

In a distributed system, you can only guarantee **two of three** properties simultaneously.

```
        Consistency (C)
              /\
             /  \
            /    \
  Availability (A)──Partition Tolerance (P)
```

| Property | Meaning |
|---|---|
| **Consistency** | Every read receives the most recent write (or an error) |
| **Availability** | Every request receives a response (not necessarily the latest) |
| **Partition Tolerance** | System continues operating despite network partitions |

**The key insight:** In a real distributed system, **network partitions are unavoidable**. Therefore P is not a choice — you always need it. The real trade-off is **C vs A** when a partition occurs.

#### CP Systems (Consistency + Partition Tolerance)

Sacrifice availability. During a partition, refuse to serve stale data — return an error instead.

**Examples:** HBase, Zookeeper, traditional RDBMS with single primary  
**Use when:** Financial data, inventory counts, anything where reading stale data causes real harm.

#### AP Systems (Availability + Partition Tolerance)

Sacrifice consistency. During a partition, return possibly stale data rather than refusing to serve.

**Examples:** Cassandra, DynamoDB, CouchDB  
**Use when:** Social feeds, shopping carts, analytics — where slight staleness is acceptable.

#### CA Systems (Consistency + Availability)

Only possible without partitions — i.e., single-node systems. Not realistic for distributed systems.

> **Interview gotcha:** "CA systems don't really exist in distributed settings. The question is always CP vs AP."

---

### Strong vs Eventual Consistency

#### Strong Consistency

After a write succeeds, any subsequent read will see that write — guaranteed.

```
Timeline:
  T1: Write balance = $100
  T2: Read balance → $100 ✅ (always)
```

**How:** Synchronous replication — write to primary AND all replicas before acknowledging.  
**Cost:** Higher write latency; lower availability during failures.  
**Use when:** Banking, payments, inventory — anywhere incorrect data causes real harm.

#### Eventual Consistency

After a write, replicas will *eventually* converge to the same value. Reads may temporarily see stale data.

```
Timeline:
  T1: Write balance = $100 to Primary
  T2: Read from Replica → $95 (stale, not yet replicated) ⚠️
  T3: Replication completes
  T4: Read from Replica → $100 ✅
```

**How:** Asynchronous replication — write to primary, replicas catch up independently.  
**Cost:** Temporary inconsistency; conflict resolution logic needed.  
**Use when:** Social feeds, user profiles, product catalog, analytics — where temporary staleness is acceptable.

#### Consistency Models Spectrum

```
← Strongest                                    Weakest →
Linearizability → Sequential → Causal → Read-Your-Writes → Eventual
```

| Model | Guarantee |
|---|---|
| **Linearizability** | Operations appear instantaneous; real-time ordering |
| **Sequential** | All nodes see operations in same order; may lag real time |
| **Causal** | Causally related operations appear in order |
| **Read-Your-Writes** | You always see your own writes |
| **Eventual** | All replicas converge; no timing guarantee |

---

### PACELC Theorem (Extension of CAP)

CAP only considers behavior during partitions. PACELC also considers the normal case:

```
IF (Partition)  → tradeoff between Availability vs Consistency
ELSE (normal)   → tradeoff between Latency vs Consistency
```

| System | Partition choice | Normal case choice |
|---|---|---|
| DynamoDB | Availability | Latency |
| Cassandra | Availability | Latency |
| HBase | Consistency | Consistency |
| PostgreSQL | Consistency | Consistency |

> **Why it matters:** Even without failures, there's a latency cost to strong consistency (synchronous replication). PACELC acknowledges this real-world trade-off.

---

### Putting It All Together — Design Checklist

Use this mental checklist when designing any system:

```
□ What are the top 3 functional requirements?
□ What are the critical NFRs (latency, availability, consistency)?
□ What is the read:write ratio?
□ What is the peak QPS?
□ Does the data have relations? → SQL or NoSQL?
□ Is eventual consistency acceptable?
□ Where are the hotspots? → Caching needed?
□ Is the service stateless? → Can scale horizontally?
□ Do I need sharding? → How much data?
□ What fails gracefully if a component goes down?
```

---

## Interview Q&A

> 35 questions covering all Phase 2 topics, calibrated for 1–6 YOE developers.

---

### System Design Basics

**Q1. What's the difference between functional and non-functional requirements? Give examples.**
> Functional requirements define what a system does — features like "user can shorten a URL" or "system redirects to the original URL." Non-functional requirements define how well it does it — availability (99.99% uptime), latency (redirect < 10ms), and scalability (supports 100M users). NFRs often drive the most important architectural decisions.

**Q2. Why do you state assumptions before starting a system design?**
> Because the right design depends entirely on the context. A system for 1,000 users looks nothing like one for 100M users. Stating assumptions aligns expectations, prevents designing for the wrong scale, and shows the interviewer you think before building. It also gives them a chance to correct you early.

**Q3. What are the most important trade-offs to discuss in a system design interview?**
> The key ones: consistency vs availability (do I need every read to be up-to-date?), read vs write optimization (which is the bottleneck?), latency vs durability (how much can I cache?), and simplicity vs scalability (is this premature complexity?). The best engineers don't just make choices — they explain what they're giving up.

---

### Capacity Estimation

**Q4. Walk me through estimating QPS for a system with 100M daily active users.**
> Assume each user makes 10 requests per day = 1B requests/day. Dividing by 86,400 seconds ≈ 11,500 QPS average. Apply a 2–3x peak multiplier for traffic spikes → peak QPS ≈ 23,000–35,000. That tells me whether I need caching, how many servers, and whether a single DB can handle it.

**Q5. A URL shortener stores 100M URLs. Estimate storage.**
> Each record: short URL (7 bytes) + long URL (200 bytes) + metadata (40 bytes) ≈ 250 bytes. 100M records × 250 bytes = 25 GB for the base data. Over 5 years at 100M new URLs/year: 500M records × 250 bytes = 125 GB. Easily fits on a single DB with room to spare — no sharding needed at this scale.

**Q6. Why does knowing the read:write ratio matter?**
> It tells you where to optimize. A 10:1 read:write ratio means reads are the bottleneck — invest in caching and read replicas. A 1:10 write-heavy ratio means writes are the bottleneck — invest in write throughput, partitioning, and async processing. Getting this wrong leads to optimizing the wrong thing.

---

### API Design

**Q7. When would you choose GraphQL over REST?**
> When different clients need different data shapes — a mobile app wants minimal fields to save bandwidth, a web app wants rich nested data. GraphQL lets clients specify exactly what they need in one request, avoiding over-fetching and multiple round trips. For simple CRUD APIs with consistent data needs, REST is simpler and has better caching support.

**Q8. How do you version a REST API without breaking existing clients?**
> Use URL path versioning: `/api/v1/users` and `/api/v2/users`. Run both versions simultaneously during a deprecation period (typically 6–12 months). Document the changes clearly. Avoid breaking changes — prefer additive changes (new optional fields) within the same version.

**Q9. Explain the difference between offset and cursor-based pagination.**
> Offset pagination (`?page=3&limit=20`) uses `SKIP + LIMIT` in SQL. It's simple but degrades at large offsets and is unstable when rows are inserted or deleted. Cursor-based pagination uses a pointer to the last seen item (`?cursor=xxx`) and fetches the next N items after it. It's consistently fast, stable under concurrent writes, and ideal for infinite scroll feeds.

**Q10. What HTTP status code should a rate-limited request return and what headers should be included?**
> Return `429 Too Many Requests`. Include `Retry-After` (seconds until the client can retry), `X-RateLimit-Limit` (total allowed), `X-RateLimit-Remaining` (remaining in current window), and `X-RateLimit-Reset` (timestamp when the window resets). This lets clients implement smart retry logic.

**Q11. Why is idempotency critical in payment APIs?**
> Network timeouts mean a client never knows if its request succeeded. Without idempotency, a retry would charge the user twice. With an idempotency key, the server detects duplicate requests and returns the original result without re-executing. This makes retries safe — essential for payment and order creation APIs.

---

### Databases

**Q12. When would you choose NoSQL over SQL?**
> When you need massive horizontal scale (millions of writes/sec), the data structure is flexible or varies per record, there are no complex joins, and eventual consistency is acceptable. For example, a user activity log or a product catalog with variable attributes. If you need ACID transactions and complex relationships (orders → users → inventory), stick with SQL.

**Q13. What is a covering index and why is it useful?**
> A covering index contains all the columns a query needs, so the DB can answer the query purely from the index without accessing the table. For example, `INDEX(user_id, status, created_at)` covers `SELECT status, created_at FROM orders WHERE user_id = 123`. It eliminates the "table lookup" step and can be dramatically faster for high-frequency queries.

**Q14. Explain what "Repeatable Read" isolation level prevents.**
> Repeatable Read prevents dirty reads (reading uncommitted data) and non-repeatable reads (the same row returning different values within one transaction). It does NOT prevent phantom reads — a query might return different rows if another transaction inserts new matching rows during your transaction. Serializable is needed to prevent phantoms.

**Q15. What is a read replica and what problem does it solve?**
> A read replica is a copy of the primary database that serves read queries. It solves the problem of a single DB node being overwhelmed by reads. The application routes all writes to the primary and all reads to replicas. Replication is asynchronous, so replicas may lag by milliseconds — data may be slightly stale, which is acceptable for most reads. It also enables failover if the primary goes down.

**Q16. How do you decide whether a column should be indexed?**
> Index a column if: it appears frequently in WHERE, JOIN ON, or ORDER BY clauses; it has high cardinality (many distinct values — email is better than status); and the table is large (indexes help less on small tables). Don't index columns that are written to frequently or have low cardinality (like a boolean flag) — the write overhead outweighs the read benefit.

---

### Caching

**Q17. Explain cache-aside pattern. When does it fail?**
> In cache-aside, the application checks the cache first. On miss, it reads from DB, writes to cache, and returns the value. Writes invalidate the cache entry. It fails under high concurrency: if two threads both get a cache miss simultaneously, both query the DB and race to write the cache — this is a cache stampede. Solve it with a distributed lock on the key or probabilistic early expiration.

**Q18. What's the difference between write-through and write-behind caching?**
> Write-through: every write goes to both cache and DB synchronously. Cache is always consistent; writes are slower. Write-behind: write to cache immediately, flush to DB asynchronously. Writes are fast; risk of data loss if cache crashes before flush. Write-through is safer; write-behind is faster but complex.

**Q19. What eviction policy would you choose for a session cache and why?**
> TTL-based eviction for sessions — sessions should naturally expire after a fixed inactivity period (e.g., 30 minutes). LRU would be second choice if TTLs aren't set explicitly. I'd avoid LFU for sessions because a session hit frequently early in a user's activity shouldn't override a newer session's right to stay in cache.

**Q20. What is cache penetration and how do you prevent it?**
> Cache penetration occurs when requests for non-existent data bypass the cache every time (cache miss on an invalid key → DB hit → no result → nothing cached → repeat). Prevent it by: caching null results with a short TTL (so subsequent requests for the same invalid key hit cache), or using a Bloom filter at the API layer to reject requests for keys that provably don't exist.

**Q21. How does Redis Cluster handle data distribution?**
> Redis Cluster uses hash slots — the key space is divided into 16,384 slots, and each node owns a range of slots. Keys are mapped to slots via `CRC16(key) % 16384`. When adding a node, some slots are migrated to it. This is similar to consistent hashing — only the data in moved slots needs to transfer, not everything.

---

### Scalability

**Q22. What does it mean for a service to be stateless and why does it matter for scaling?**
> A stateless service holds no user-specific state in its own memory. Each request contains everything needed to process it. State is externalized to Redis, a DB, or object storage. This matters because you can add or remove server instances freely — any server can handle any request. Without statelessness, you need sticky sessions, which tie users to specific servers and complicate scaling and failover.

**Q23. What's the difference between horizontal partitioning (sharding) and vertical partitioning?**
> Horizontal partitioning (sharding): split rows across multiple DB nodes — users 1–10M on Shard 1, 10M–20M on Shard 2. Vertical partitioning: split columns — core user data in one table, activity logs in another, or separate DB for analytics. Sharding helps with write scale and data volume. Vertical partitioning helps with query performance and separating concerns.

**Q24. When would you use hash-based sharding vs range-based sharding?**
> Range-based: when you frequently query ranges (e.g., orders by date) and can tolerate potential hotspots. Hash-based: when you need even distribution and most queries are point lookups (find by user_id). Hash-based is safer for avoiding hotspots; range-based is better for sequential scans.

**Q25. What problem does consistent hashing solve?**
> Standard hash sharding (`hash(key) % N`) breaks when N changes — adding or removing a node reshuffles almost all keys. Consistent hashing places nodes on a virtual ring. Adding a node only moves keys from its neighbor — typically `1/N` of all keys. This is critical for cache clusters where rehashing means a thundering herd of cache misses.

---

### Load Balancing

**Q26. What's the difference between an L4 and L7 load balancer? When would you use each?**
> L4 (transport layer) routes based on IP and port only — it's fast but cannot see request content. Use it for high-throughput TCP scenarios like database connections or raw streaming. L7 (application layer) inspects HTTP content — it can route by URL path, handle SSL termination, and enable smart routing. Use it for web applications and microservices where content-aware routing matters.

**Q27. Your API servers have uneven load — some are overloaded, some idle. What load balancing algorithm would help?**
> Least Connections — route each new request to the server with the fewest active connections at that moment. This dynamically accounts for requests with varying processing times, unlike Round Robin which ignores current server load. Weighted Round Robin is an alternative if the servers have known different capacities.

---

### CAP Theorem & Consistency

**Q28. Explain CAP theorem in simple terms.**
> In a distributed system, you can only guarantee two of three: Consistency (reads always return the latest write), Availability (requests always get a response), and Partition Tolerance (system works despite network failures). Since network partitions are unavoidable in practice, the real choice is: during a partition, do you return potentially stale data (AP) or refuse to answer (CP)?

**Q29. Is it possible to build a CA (Consistent + Available) distributed system?**
> No — not in practice. A CA system assumes no network partitions, which isn't realistic in any distributed deployment. The moment two nodes can't communicate, you must choose between serving stale data (AP) or refusing to serve (CP). CA is only achievable in a single-node system, which isn't distributed.

**Q30. Give an example of a system that should be CP and one that should be AP.**
> CP: A banking ledger — reading a stale balance and acting on it could mean lending money that's already been spent. Better to return an error than wrong data. AP: A social media feed — if a user doesn't see a post for a few seconds due to replication lag, no real harm done. Availability matters more than strict consistency here.

**Q31. What is the difference between strong and eventual consistency? Give a real-world analogy.**
> Strong consistency: after you deposit $100 at an ATM, your bank app immediately shows the updated balance — every read reflects the latest write. Eventual consistency: after you post a tweet, your follower might see it appear 2 seconds later — the system converges but not instantly. Strong consistency is like a whiteboard in a meeting room — everyone sees the same thing simultaneously. Eventual is like a bulletin board — you update it, but others across the office may not see it for a few minutes.

**Q32. What is Read-Your-Writes consistency and when is it important?**
> Read-Your-Writes guarantees that after you perform a write, your subsequent reads will always reflect that write — even if the system uses eventual consistency globally. This is important for user-facing features: after you update your profile, you shouldn't see the old profile when you refresh. Implemented by routing a user's reads back to the same primary (or the replica that received their write) for a short window.

---

### Scenario-Based

**Q33. Design a simple caching strategy for a product catalog that has 1M products, mostly reads, and updates every few hours.**
> Cache-aside with Redis. Cache each product by ID with a TTL of 1 hour. On product update, explicitly invalidate the cache entry. For the homepage featuring popular products, pre-warm the cache after each update using a background job. Add a short random jitter (±5 min) to TTLs so not all 1M entries expire simultaneously — avoids a cache stampede after a bulk update.

**Q34. A service is getting 50,000 read QPS but only 500 write QPS. Walk through your scaling approach.**
> Step 1: Add Redis caching (cache-aside) for hot data — likely eliminates 90%+ of DB reads. Step 2: Add read replicas to spread remaining DB reads — 3–5 replicas handles this comfortably. Step 3: Make the application layer stateless and scale horizontally with a load balancer. Step 4: Monitor — if write QPS grows significantly later, consider partitioning or write queuing. At 500 write QPS, a single primary DB is fine.

**Q35. How would you ensure high availability for a system that must have 99.99% uptime?**
> 99.99% means < 52 minutes downtime per year. Eliminate all single points of failure: multiple application servers behind a load balancer, DB primary with failover replicas (automatic promotion), Redis Sentinel or Cluster, CDN for static assets. Use health checks and auto-scaling to replace failed instances automatically. Multi-AZ deployment ensures an entire data center failure doesn't bring the system down. Implement circuit breakers for dependencies. Define and test a runbook for each failure scenario — availability is as much about recovery speed as prevention.

---

*End of Phase 2 Notes — You've got this! 🚀*