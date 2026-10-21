# 🏥 Script Assist — Complete Interview Preparation Guide
### Full-Stack Engineer (Node / NestJS / React / TypeScript)
### CTO Round with Arjun Rajyagor

---

> **About Script Assist:** UK-regulated medical cannabis prescribing & dispensing SaaS platform.
> Regulated by MHRA + Home Office. CQC compliant. 15 active clinics, 25,000+ patients, 35 prescribing specialists.
> The platform handles: Prescribing → Dispensing → Payment → Delivery → Repeat Prescriptions.

---

## 📋 TABLE OF CONTENTS

1. [Personal & Introduction](#section-1-personal--introduction) — Q1 to Q10
2. [NestJS & Backend Architecture](#section-2-nestjs--backend-architecture) — Q11 to Q25
3. [Multi-Tenancy & SaaS Architecture](#section-3-multi-tenancy--saas-architecture) — Q26 to Q35
4. [Transactional Systems & Idempotency](#section-4-transactional-systems--idempotency) — Q36 to Q45
5. [Async Processing & Queue Systems](#section-5-async-processing--queue-systems) — Q46 to Q53
6. [Database & Migrations](#section-6-database--migrations) — Q54 to Q60
7. [Security, GDPR & Compliance](#section-7-security-gdpr--compliance) — Q61 to Q68
8. [React & Frontend](#section-8-react--frontend) — Q69 to Q78
9. [Testing & Code Quality](#section-9-testing--code-quality) — Q79 to Q85
10. [System Design](#section-10-system-design) — Q86 to Q90
11. [CEO / Founder Mindset Questions](#section-11-ceo--founder-mindset-questions) — Q91 to Q100
12. [Questions YOU Should Ask at the End](#questions-you-should-ask-at-the-end) — 15 Smart Questions

---

---

## SECTION 1: Personal & Introduction

---

### Q1. Tell me about yourself.

**Answer:**

I am a full-stack engineer with 5+ years of experience in Node.js, TypeScript, and React. I have worked on complex B2B SaaS products — not simple CRUD apps, but real systems with workflows, state machines, payment flows, and multi-tenant architectures.

I understand that in regulated environments like healthcare, a bug is not just a bug — it can delay a patient's medication or cause a compliance failure. That is the level of care I bring to every feature I build.

I am excited about Script Assist because you are building the operating system for UK private healthcare — and the technical challenges here (idempotency, audit trails, multi-tenancy, regulated dispensing workflows) are exactly the kind of problems I enjoy solving.

> **Tip:** Keep this under 2 minutes. Mention "regulated environment", "reliability", and "correctness" — these words resonate with the CTO.

---

### Q2. Why do you want to join Script Assist specifically?

**Answer:**

Script Assist is doing something genuinely hard. You are not building a simple booking app — you are building a compliant, multi-tenant SaaS that connects clinicians, pharmacists, and patients in a regulated medical cannabis environment.

The fact that you are MHRA-regulated, Home Office licensed, and CQC-compliant means every feature has to be built with real care. That excites me as an engineer — I want to work where correctness and auditability actually matter.

I also see that you are growing — Wholesale SaaS is coming, you have 15 active clinics and 25,000+ patients. Being part of a platform at this stage, where my work directly shapes the architecture, is exactly where I want to be.

---

### Q3. What do you know about what Script Assist does?

**Answer:**

Script Assist is a white-labelled, multi-tenant SaaS platform for UK clinics, pharmacies, and prescribers — specifically in the medical cannabis space.

The platform handles the full workflow: a clinician prescribes → the pharmacy receives and dispenses → the patient pays securely → the order is tracked and delivered. It also supports repeat prescriptions with live inventory checks so only in-stock products are prescribed.

You are regulated by MHRA and the Home Office, and CQC compliant since 2019. You currently have 15 active clinics, 35 prescribing specialists, and over 25,000 patients. You process 80%+ of prescriptions within 48 hours and have reduced prescription errors down to near zero.

> **Tip:** This answer will immediately impress the CTO. Most candidates will not know these details.

---

### Q4. What is your biggest strength as an engineer?

**Answer:**

My biggest strength is building reliable backend systems that handle real-world complexity — not just the happy path. I think deeply about what happens when things go wrong: payments fail, queues back up, two requests arrive at the same time.

In practice, this means I naturally reach for idempotency keys, proper state machine design, and structured logging — not because someone asked me to, but because I have seen what happens when these are missing in production.

I also write things down. In regulated environments, clear documentation and audit trails are not extras — they are part of the feature.

---

### Q5. What is your biggest weakness?

**Answer:**

I sometimes go too deep into a technical problem and lose track of time. I find complex architecture decisions genuinely interesting, so I can over-engineer something that needed a simple solution.

I have learned to timebox exploratory work — I give myself 30 minutes to investigate, then I decide whether to go deeper or ship the simpler version. In regulated environments, a correct simple solution shipped on time is often better than a perfect complex one shipped late.

> **Tip:** Never say "I work too hard." Show a real weakness with a real fix.

---

### Q6. Where do you see yourself in 3 years?

**Answer:**

In 3 years, I want to be a technical owner of a meaningful product area — not just someone who ships tickets, but someone who helps shape how the system evolves.

At Script Assist, as you scale to more clinics and roll out Wholesale SaaS, the architecture will need to grow. I want to be part of those decisions — helping the platform scale reliably and safely.

I also want to mentor junior engineers by then, because strong teams are what build great products.

---

### Q7. How do you handle working under pressure?

**Answer:**

I stay calm by focusing on what I can control. When something breaks in production, I follow a clear mental process: first stabilise (stop the bleeding), then investigate (find the root cause), then fix properly (do not just patch symptoms).

I communicate early and clearly under pressure. If a release is at risk, I say so with enough lead time so the team can adjust — not 30 minutes before the deadline.

In a healthcare platform, pressure is real because patient workflows depend on the system. That is why I invest heavily in observability and testing upfront — so pressure incidents are rare, not routine.

---

### Q8. How do you keep up with new technology?

**Answer:**

I follow a few trusted sources — the NestJS changelog, TypeScript release notes, and engineering blogs from companies solving similar problems (like Stripe for payments, Notion for SaaS architecture).

But honestly, I am selective. In a regulated platform, adopting the newest library just because it is trending can introduce instability. I evaluate new technology based on: Is it stable? Is it well-maintained? Does it solve a real problem we have?

I prefer depth over breadth — being very good at the core stack (Node, NestJS, TypeScript, PostgreSQL) is more valuable than knowing 10 frameworks at a surface level.

---

### Q9. Have you worked in a regulated or compliance-heavy environment before?

**Answer:**

Yes. I have worked on systems where audit trails, data access controls, and GDPR compliance were hard requirements — not optional extras.

The mindset shift in regulated environments is: you build for the auditor, not just the user. Every state change must be traceable. Every access to sensitive data must be logged. Every system must behave predictably even in failure scenarios.

That mindset aligns well with what Script Assist needs — a platform that clinicians and pharmacists trust completely, because their patients depend on it.

---

### Q10. How do you approach learning a new codebase?

**Answer:**

I start by understanding the domain before touching the code. What does the business do? What are the core entities? What flows matter most?

Then I trace a single end-to-end flow through the codebase — for Script Assist, I would trace a prescription creation from the API endpoint to the database. This shows me the architecture, naming conventions, and key patterns in one pass.

After that, I look at the tests — tests tell me what the team considers important and where the edge cases are. Then I look at the git history to understand why decisions were made, not just what they are.

---

---

## SECTION 2: NestJS & Backend Architecture

---

### Q11. How does NestJS handle dependency injection? Why is it useful?

**Answer:**

In NestJS, Dependency Injection means you declare what you need and the framework provides it — you do not create objects manually.

For example, if my `OrderService` needs a `PaymentService`, I just put it in the constructor and NestJS creates and injects it automatically:

```typescript
constructor(private readonly paymentService: PaymentService) {}
```

This makes testing very easy — I can inject a `FakePaymentService` in tests without changing any real code. It also means modules are loosely coupled — `OrderModule` does not need to know how `PaymentModule` works internally.

In a large system like Script Assist with clinic workflows, pharmacy workflows, and payment flows all running together, this loose coupling is critical for maintainability.

---

### Q12. What are Guards in NestJS? Give a real example for this platform.

**Answer:**

A Guard decides whether a request is allowed to proceed before it reaches the controller.

For Script Assist, I would use two types of guards:

**Auth Guard:** Checks if the JWT token is valid and not expired. If the token is missing or invalid, the request is rejected with a 401.

**Tenant Guard:** After authentication, checks that the user belongs to the tenant they are trying to access. A pharmacist from Clinic A must never be able to access Clinic B's prescriptions — even with a valid token.

```typescript
@UseGuards(AuthGuard, TenantGuard, RolesGuard)
@Roles('pharmacist')
@Get('prescriptions')
async getPrescriptions() { ... }
```

Guards reject the request before any business logic runs — which is the right place for security checks.

---

### Q13. What are Interceptors in NestJS? How would you use them here?

**Answer:**

An Interceptor wraps around a request and can run logic both before AND after the controller handles it.

For Script Assist, I would use interceptors for:

**Audit Logging Interceptor:** Automatically captures every state-changing operation (POST, PATCH, DELETE) and writes an audit log entry — who did it, when, what entity, and what changed. This runs on every write request without polluting business logic.

**Response Transformation Interceptor:** Standardises all API responses into a consistent format — `{ data, meta, error }` — so the frontend always knows what to expect.

**Timing Interceptor:** Logs how long each request takes. Useful for spotting slow queries in a regulated platform where response times affect clinical workflows.

---

### Q14. How do you structure a NestJS module for a complex domain like pharmacy dispensing?

**Answer:**

I follow the principle: one module per bounded domain context.

```
DispensingModule
├── dispensing.controller.ts    → HTTP endpoints
├── dispensing.service.ts       → Business logic
├── dispensing.repository.ts    → Database queries
├── dispensing.dto.ts           → Input validation
├── dispensing.entity.ts        → DB entity
├── events/
│   └── dispensing.events.ts    → Domain events
└── dispensing.module.ts        → Module definition
```

The controller handles HTTP concerns only — it validates input and delegates to the service. The service contains all business logic — it has no knowledge of HTTP. The repository handles all database queries — the service never writes raw SQL.

This separation means I can test each layer independently and swap implementations without touching business logic.

---

### Q15. How do you implement a global exception filter in NestJS?

**Answer:**

A global exception filter catches all unhandled errors and returns consistent, structured responses — never raw stack traces to clients.

```typescript
@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    
    if (exception instanceof DomainException) {
      return response.status(exception.statusCode).json({
        code: exception.code,
        message: exception.message
      });
    }
    
    // Log unexpected errors with full context
    this.logger.error(exception, { userId, tenantId, requestId });
    
    return response.status(500).json({
      code: 'INTERNAL_ERROR',
      message: 'Something went wrong. Please try again.'
    });
  }
}
```

For domain errors like "product out of stock" or "prescription already dispensed", I create custom exception classes that carry a machine-readable error code — so the frontend can handle them programmatically.

---

### Q16. How do you validate incoming API requests in NestJS?

**Answer:**

I use `class-validator` and `class-transformer` with NestJS's built-in `ValidationPipe`.

Every endpoint has a DTO (Data Transfer Object) that describes exactly what input is acceptable:

```typescript
export class CreatePrescriptionDto {
  @IsUUID()
  patientId: string;

  @IsUUID()
  productId: string;

  @IsPositive()
  @Max(90) // max 90 days supply
  daysSupply: number;

  @IsEnum(DosageUnit)
  dosageUnit: DosageUnit;
}
```

I set `whitelist: true` in the ValidationPipe — this automatically strips any properties that are not defined in the DTO. In a healthcare platform, you never want unexpected data silently entering the system.

---

### Q17. How do you implement API versioning in NestJS?

**Answer:**

I use URL-based versioning — `/api/v1/prescriptions` and `/api/v2/prescriptions`. This is the clearest approach for a B2B platform where clinic integrations cannot break silently.

```typescript
const app = await NestFactory.create(AppModule);
app.enableVersioning({
  type: VersioningType.URI,
  defaultVersion: '1',
});
```

When I release a breaking change, I create a v2 version of the affected endpoint. The v1 endpoint continues to work for existing integrations. I deprecate v1 with a response header warning, give partners a migration timeline, then remove it in a planned release.

---

### Q18. How do you implement rate limiting in NestJS?

**Answer:**

I use `@nestjs/throttler` with different limits per endpoint based on risk:

```typescript
// High-risk endpoint — strict limit
@Throttle({ default: { limit: 5, ttl: 60000 } })
@Post('prescriptions')
async createPrescription() { ... }

// Read endpoint — generous limit
@Throttle({ default: { limit: 100, ttl: 60000 } })
@Get('products')
async getProducts() { ... }
```

For the prescription submit endpoint, 5 requests per minute is sufficient for normal clinical use. If someone is hitting it 50 times a minute, something is wrong.

I also implement tenant-level rate limiting — if one clinic is hammering the API, it should not affect other tenants.

---

### Q19. How do you implement structured logging in a production Node.js application?

**Answer:**

I use a structured logging library like Pino or Winston that outputs JSON — not plain text strings.

Every log entry includes: `timestamp`, `level`, `requestId`, `userId`, `tenantId`, `action`, `duration`, and `metadata`.

```typescript
logger.info({
  requestId: '123e4567',
  tenantId: 'clinic-a',
  userId: 'dr-smith',
  action: 'PRESCRIPTION_CREATED',
  prescriptionId: 'rx-001',
  duration: 145
});
```

JSON logs can be queried, filtered, and alerted on by observability tools (Datadog, CloudWatch). Plain text logs cannot.

**Critical rule:** Never log PII — no patient names, NHS numbers, or medication details in logs. I implement a log sanitiser that strips known sensitive fields before writing.

---

### Q20. How would you implement an audit trail system for a regulated healthcare platform?

**Answer:**

Every state-changing operation must be logged with: who did it, when, what entity was changed, and what the before and after values were.

I implement this as a NestJS interceptor that automatically runs on every write operation:

```typescript
// Audit log entry structure
{
  id: uuid,
  tenantId: 'clinic-a',
  userId: 'dr-smith',
  action: 'PRESCRIPTION_UPDATED',
  entityType: 'Prescription',
  entityId: 'rx-001',
  before: { status: 'PENDING', dosage: '10mg' },
  after: { status: 'APPROVED', dosage: '10mg' },
  ipAddress: '10.0.0.1',
  timestamp: '2025-03-23T10:00:00Z'
}
```

The audit log table is **append-only** — records can never be updated or deleted. This is the correct approach for regulated environments. If the CQC audits you, this log is your proof of compliance.

---

### Q21. How do you implement pagination in a REST API?

**Answer:**

For large datasets like dispensing history or patient lists, I use **cursor-based pagination**, not OFFSET/LIMIT.

```typescript
// Response shape
{
  data: [...prescriptions],
  meta: {
    nextCursor: 'eyJpZCI6MTAwfQ==',
    hasMore: true,
    total: 5420
  }
}
```

**Why not OFFSET?** `SELECT * FROM prescriptions OFFSET 5000 LIMIT 20` has to scan and discard 5000 rows every time. As the table grows, this gets slower and slower. Cursor-based pagination is always fast because it uses the index.

For simple, small datasets I do use OFFSET — but for pharmacy dispensing lists with thousands of records, cursor-based is essential.

---

### Q22. How do you implement background scheduled jobs in NestJS?

**Answer:**

I use the `@nestjs/schedule` package for cron jobs:

```typescript
@Injectable()
export class ExpiryCheckService {
  @Cron('0 6 * * *') // runs every day at 6am
  async checkExpiringStock() {
    const expiringBatches = await this.inventoryRepo.findExpiringWithin(30);
    
    for (const batch of expiringBatches) {
      await this.notificationService.alertPharmacist(batch);
    }
  }
}
```

For more complex jobs that need retry logic and queue management, I use BullMQ — the cron creates a queue job, and a worker processes it. This way, if the job fails, it retries with backoff instead of silently disappearing.

---

### Q23. How do you handle circular dependencies in NestJS?

**Answer:**

Circular dependencies happen when Module A imports Module B and Module B imports Module A. NestJS handles this with `forwardRef`:

```typescript
@Module({
  imports: [forwardRef(() => PharmacyModule)]
})
export class ClinicModule {}
```

But `forwardRef` is a code smell — it means your module boundaries are wrong. The better solution is to extract the shared dependency into a third module that both can import, or use domain events to decouple the two modules entirely.

In a platform like Script Assist, I would use an event bus: when a prescription is created in the Clinic module, it emits a `PrescriptionCreatedEvent`. The Pharmacy module listens for this event and reacts. They never import each other directly.

---

### Q24. How do you implement health checks in a NestJS API?

**Answer:**

I use `@nestjs/terminus` to create health check endpoints that monitor all critical dependencies:

```typescript
@Get('/health')
async checkHealth() {
  return this.healthCheckService.check([
    () => this.db.pingCheck('database'),
    () => this.redis.pingCheck('redis'),
    () => this.http.pingCheck('payment-provider', 'https://api.payment.com/health'),
  ]);
}
```

This endpoint is called by the load balancer every 30 seconds. If any check fails, the instance is removed from rotation. This prevents requests from reaching a server that cannot connect to the database.

In a healthcare platform, a silent database disconnect would cause prescription operations to silently fail — health checks catch this before patients are affected.

---

### Q25. How do you implement OpenAPI/Swagger documentation in NestJS?

**Answer:**

NestJS has first-class Swagger support through `@nestjs/swagger`. I decorate every DTO and controller with documentation metadata:

```typescript
@ApiTags('Prescriptions')
@ApiOperation({ summary: 'Create a new prescription' })
@ApiResponse({ status: 201, description: 'Prescription created', type: PrescriptionResponseDto })
@ApiResponse({ status: 409, description: 'Duplicate prescription (idempotency key conflict)' })
@Post()
async createPrescription(@Body() dto: CreatePrescriptionDto) { ... }
```

For Script Assist, good API documentation is important because partner pharmacies integrate with the platform. If the documentation is incomplete or wrong, their integrations break and patients are affected.

---

---

## SECTION 3: Multi-Tenancy & SaaS Architecture

---

### Q26. How would you implement multi-tenancy in this platform? Row-level or schema-level?

**Answer:**

For Script Assist's scale, I would use **row-level multi-tenancy with database-level Row Level Security (RLS) as a safety net**.

**Why not schema-per-tenant?** Clean isolation, but migrations become a nightmare at scale — if you have 100 clinics, every schema migration runs 100 times. Managing this reliably is very difficult.

**My approach:**
1. Every table has a `tenant_id` column with a database index.
2. Every query is automatically scoped to the current tenant via a NestJS middleware that reads tenant context from the JWT or subdomain.
3. PostgreSQL Row Level Security is enabled as a second layer — even if a code bug bypasses the application layer, the database blocks cross-tenant reads.

In healthcare, a cross-tenant data leak is a serious GDPR and regulatory incident. Defence in depth is non-negotiable.

---

### Q27. How do you set tenant context for every request?

**Answer:**

I use a NestJS middleware that runs before every request:

```typescript
@Injectable()
export class TenantMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const tenantId = this.extractTenantId(req); // from JWT or subdomain
    
    if (!tenantId) throw new UnauthorizedException('Tenant not identified');
    
    // Store in AsyncLocalStorage — available anywhere in the request lifecycle
    tenantContext.run({ tenantId }, next);
  }
}
```

I use Node.js `AsyncLocalStorage` to propagate the tenant context through the entire request — through services, repositories, and interceptors — without passing it manually to every function. The repository layer reads from this context and automatically adds `WHERE tenant_id = ?` to every query.

---

### Q28. How do you handle tenant onboarding in a multi-tenant SaaS?

**Answer:**

Tenant onboarding creates a new clinic or pharmacy account. It involves several steps that must succeed or fail as a unit:

1. Create the tenant record with a unique slug (used in subdomains like `clinic-a.scriptassist.co.uk`)
2. Create the default admin user for the tenant
3. Set up default roles and permissions for the tenant
4. Create initial configuration (notification settings, dispensing preferences)
5. Send a welcome email to the admin

I wrap these in a database transaction where possible. For steps that touch external systems (like sending email), I use the Outbox pattern — write the "send email" task to the database in the same transaction, and process it asynchronously after commit.

---

### Q29. How do you handle feature flags in a multi-tenant system?

**Answer:**

Different clinics may be on different pricing tiers with different features enabled. I implement feature flags at the tenant level:

```typescript
// tenant_features table
{ tenantId: 'clinic-a', feature: 'WHOLESALE_ORDERING', enabled: true }
{ tenantId: 'clinic-b', feature: 'WHOLESALE_ORDERING', enabled: false }
```

In the application, I check feature flags with a guard:

```typescript
@RequiresFeature('WHOLESALE_ORDERING')
@Post('wholesale/orders')
async createWholesaleOrder() { ... }
```

If the feature is not enabled for the tenant, the endpoint returns 403. The tenant-level feature flag system also allows gradual rollouts — enable a new feature for 10% of tenants first, validate, then roll out to all.

---

### Q30. How do you ensure data segregation in reports and analytics?

**Answer:**

Reports are a common source of cross-tenant data leaks in SaaS platforms because report queries are often complex and easy to get wrong.

My rules for report queries:
1. Every report query starts with `WHERE tenant_id = :tenantId` — no exceptions.
2. Reports are tested with two tenants in the test database — I verify that Tenant A's report never includes Tenant B's data.
3. For aggregated reports (like "total prescriptions this month"), the query groups by tenant_id and the result is filtered to the requesting tenant before returning.
4. Audit log reports are especially sensitive — I add an extra permission check before any cross-user audit log access.

---

### Q31. How would you approach white-labelling the platform for different clinics?

**Answer:**

Script Assist is fully white-labelled — each clinic has their own branded app. I implement this with a tenant configuration system:

```typescript
// tenant_branding table
{
  tenantId: 'clinic-a',
  primaryColor: '#2E75B6',
  logoUrl: 'https://cdn.scriptassist.co.uk/logos/clinic-a.png',
  appName: 'MediClinic Prescriptions',
  supportEmail: 'support@mediclinic.co.uk',
  domain: 'prescriptions.mediclinic.co.uk'
}
```

The frontend reads the tenant branding from the API on load and applies it via CSS variables. The email templates use the tenant's branding and sender name. The PDF prescriptions use the clinic's letterhead.

All of this is data-driven — no code changes required when onboarding a new clinic.

---

### Q32. How do you handle tenant-specific configuration without code changes?

**Answer:**

I use a tenant settings system where configuration is stored in the database, not in code:

**Examples of tenant-specific config:**
- Maximum days supply per prescription
- Which payment methods are enabled
- Notification preferences (email, SMS, both)
- Partner pharmacy preferences
- Dispensing workflow steps (some clinics have extra approval steps)

These settings are cached in Redis with a TTL of 5 minutes — so they are fast to read but also stay relatively fresh when a tenant admin changes a setting.

The key principle: configuration that varies per tenant should never be in environment variables or code — it should be in the database where tenant admins can control it.

---

### Q33. How do you handle schema migrations when you have many tenants?

**Answer:**

In a shared-schema multi-tenant system, a migration runs once and affects all tenants simultaneously — which is both an advantage and a risk.

**Safe migration process:**
1. Always use the expand-contract pattern (add nullable → backfill → add constraint).
2. Run migrations in a separate deployment step before deploying new code.
3. Test migrations on a copy of production data first — check how long they take on real data volumes.
4. For large tables (millions of rows), use batched backfills — process 1000 rows at a time to avoid table locks.
5. Have a rollback plan for every migration before running it.

The rule: if a migration takes more than 5 seconds on production data, it needs to be redesigned.

---

### Q34. How do you handle timezone differences for UK-based clinic operations?

**Answer:**

Script Assist operates in the UK, but the engineering team is in India and future patients may be in different timezones.

My approach:
1. **Store all timestamps in UTC** in the database — always.
2. **Convert to local timezone** only at the presentation layer (frontend or email templates).
3. **UK business hours checks** (for notifications, reminders) are calculated server-side using the tenant's configured timezone (`Europe/London`), not the user's browser timezone.
4. **Daylight saving time** is handled by using a proper timezone library (date-fns-tz or Luxon) — never manual UTC offset arithmetic.

Prescription timing is safety-critical. A reminder sent at 3am because of a timezone bug is a real problem.

---

### Q35. How do you scale a multi-tenant SaaS as the number of tenants grows?

**Answer:**

The main scaling challenges are: database connection limits, query performance as data grows, and noisy neighbour problems (one tenant's heavy queries affecting others).

**My approach:**
- Connection pooling with PgBouncer — 100 tenants should not mean 100 separate connection pools.
- Read replicas for report queries — complex dispensing reports go to a read replica, not the primary.
- Tenant-aware query optimisation — indexes always include `tenant_id` as the first column.
- Rate limiting per tenant at the application level — one clinic doing a bulk import should not slow down others.
- Async processing for heavy operations — large report generation runs as a background job, not a synchronous API call.

---

---

## SECTION 4: Transactional Systems & Idempotency

---

### Q36. What is idempotency and why is it critical in this system?

**Answer:**

Idempotency means: if you do the same operation twice, the result is the same as doing it once.

This is critical in Script Assist because the same request can arrive more than once — a payment webhook that fires twice, a network timeout causing a client retry, a queue consumer processing a message twice.

**Without idempotency:** A patient submits a prescription order and the network times out. Their app retries. The patient gets charged twice and two dispensing orders are created. This is both a financial error and a potential medication safety issue.

**With idempotency:** Every critical request carries a unique `idempotency-key` header. The server stores this key with the result. If the same key arrives again, it returns the stored result immediately without processing again.

Implementation: unique database constraint on `idempotency_key` column. First insert succeeds. Second insert throws a unique violation, and we return the original result.

---

### Q37. What is the Outbox Pattern and when would you use it?

**Answer:**

The Outbox Pattern solves the problem of "I need to do something in my database AND send an event/message, but they need to be atomic."

**The problem:** You save a prescription to the database and then publish a `PrescriptionCreated` event to a queue. If the database save succeeds but the queue publish fails, your data is inconsistent — the prescription exists but no one was notified.

**The solution:**
1. Write the prescription AND a `pending_events` record in a single database transaction.
2. A background worker reads pending events and publishes them to the queue.
3. Once published, delete the pending event record.

Now the database and the queue are always consistent — either both happen or neither happens.

I would use this for: prescription creation notifications, payment confirmations, dispensing alerts to pharmacists, and shipping notifications to patients.

---

### Q38. How do you design a prescription order state machine?

**Answer:**

A state machine defines all valid states and all valid transitions. This prevents invalid state changes — you cannot move a prescription from CANCELLED directly to DISPENSED.

```
DRAFT → SUBMITTED → APPROVED → PAYMENT_PENDING → PAID → DISPENSING → DISPENSED → SHIPPED → DELIVERED
                              ↘ PAYMENT_FAILED → PAYMENT_PENDING (retry)
              ↘ REJECTED
                              ↘ CANCELLED (from most states, by authorised user)
```

Every transition is:
- **Explicit** — defined in code, not implicit.
- **Validated** — the service checks if the transition is allowed before executing.
- **Logged** — every state change is written to the audit log with the reason and the user who triggered it.

This is important in a regulated environment — if a CQC auditor asks "why was this prescription cancelled?", the audit log has the answer.

---

### Q39. How do you prevent double-charging a patient?

**Answer:**

This is a classic payment idempotency problem.

**Layer 1:** Generate a unique `payment_intent_id` when the order is created. Pass this to the payment provider. If the same `payment_intent_id` is submitted twice, the payment provider rejects the second attempt.

**Layer 2:** Before initiating payment, check if a successful payment already exists for this order in our database. If yes, return the existing result.

**Layer 3:** Use an optimistic lock on the order record — when moving from `PAYMENT_PENDING` to `PAID`, use a conditional update: `UPDATE orders SET status='PAID' WHERE id=? AND status='PAYMENT_PENDING'`. If zero rows are updated, someone else already processed it.

Three layers of protection — in a healthcare payment system, this is the minimum acceptable.

---

### Q40. What is the Saga pattern and when would you use it?

**Answer:**

A Saga is a sequence of local transactions, each with a compensating transaction that undoes its effect if something later fails.

**Example for Script Assist — placing an order:**

| Step | Action | Compensating Action |
|------|--------|---------------------|
| 1 | Reserve stock | Release stock reservation |
| 2 | Create order | Cancel order |
| 3 | Charge payment | Issue refund |
| 4 | Create dispensing task | Cancel dispensing task |

If step 3 (payment) fails, the saga runs the compensating transactions for steps 1 and 2 — releasing the stock and cancelling the order.

I would use this for the full prescription-to-delivery flow where multiple systems (inventory, payment, dispensing, shipping) must all succeed together.

---

### Q41. How do you handle optimistic vs pessimistic locking in a database?

**Answer:**

**Pessimistic locking** (`SELECT FOR UPDATE`) locks the row when you read it, preventing anyone else from modifying it until you are done. Use this when conflicts are common and the cost of redoing work is high — for example, processing a dispensing job where two pharmacists might pick up the same order.

**Optimistic locking** adds a version column. You read the row (version = 3), do your work, then update only if the version is still 3. If someone else changed it, the update fails and you retry. Use this when conflicts are rare but correctness is critical — for example, updating prescription status.

In a pharmacy platform, I use pessimistic locking for the dispensing assignment step (prevent two pharmacists from dispensing the same prescription) and optimistic locking for status updates.

---

### Q42. How do you design a reconciliation system for payments?

**Answer:**

Reconciliation means verifying that what your system recorded matches what the payment provider actually processed.

**Daily reconciliation job:**
1. At midnight, fetch all payment transactions from the payment provider API for the previous day.
2. Compare each transaction to our internal `payments` table — match by `payment_intent_id`.
3. For any discrepancy — a payment we recorded as successful that the provider shows as failed, or vice versa — create a reconciliation alert for the finance team.
4. Write the reconciliation result to an `reconciliation_reports` table for audit purposes.

In a regulated platform, unreconciled payments are a compliance risk. A prescription was dispensed based on a payment that actually failed is a serious financial and operational issue.

---

### Q43. How do you handle payment webhooks reliably?

**Answer:**

Payment webhooks are the payment provider calling your system to update payment status. They can fire multiple times for the same event.

**My webhook handler:**
1. Immediately return HTTP 200 — acknowledge receipt before processing. If you take too long, the provider retries and you get a duplicate.
2. Write the raw webhook payload to a `webhook_events` table with the event ID.
3. Check if this event ID already exists — if yes, it is a duplicate, return 200 without processing.
4. Queue a background job to process the webhook event.
5. The background job updates the order status, sends notifications, and triggers the next step in the workflow.

Never do heavy processing in the webhook handler itself — always hand off to a queue.

---

### Q44. How do you manage order lifecycle for repeat prescriptions differently from new prescriptions?

**Answer:**

Repeat prescriptions share the same basic lifecycle but with additional pre-checks:

**New prescription flow:** Clinician creates → Approved → Patient pays → Dispensed → Shipped.

**Repeat prescription flow:** Patient requests → System checks (valid original prescription, product in stock, repeat allowance not exceeded, correct time interval since last prescription) → Auto-approved or sent for clinician review → Patient pays → Dispensed → Shipped.

The key difference is the automated eligibility check before the prescription enters the main workflow. If any check fails, the system does not just reject silently — it creates a task for the clinic team to resolve (like a stock issue) and notifies the patient of the delay with an estimated resolution time.

---

### Q45. How do you handle partial failures in a multi-step workflow?

**Answer:**

A partial failure is when some steps of a workflow complete and others fail — leaving the system in an inconsistent state.

**Prevention:** Use the Outbox pattern and explicit state machines so every step is either committed or not. Avoid operations that cannot be rolled back (like sending an email) until all database operations have succeeded.

**Detection:** Monitor for orders stuck in intermediate states — for example, an order in `PAYMENT_PENDING` for more than 30 minutes needs investigation.

**Recovery:** Every workflow step is idempotent and can be safely retried. I implement an admin tool that allows replaying a specific workflow step for a specific order — critical for manual recovery in a regulated environment.

---

---

## SECTION 5: Async Processing & Queue Systems

---

### Q46. What queue system would you use for this platform and why?

**Answer:**

I would use **BullMQ with Redis** for job queues in Script Assist.

**Why BullMQ:**
- Built for Node.js/TypeScript — first-class NestJS integration via `@nestjs/bull`.
- Handles retries, backoff, priorities, rate limiting, and DLQs natively.
- Jobs are persistent in Redis — if a worker crashes, jobs are not lost.
- Bull Board gives a visual dashboard to monitor queue health — useful for operations teams.

**Queue design for Script Assist:**
- `prescription-events` — high priority, processes prescription state changes
- `notifications` — sends emails/SMS to patients and clinicians
- `payment-webhooks` — processes payment provider callbacks
- `reports` — generates heavy reports asynchronously
- `expiry-checks` — runs scheduled inventory checks

Separate queues per domain means a slow report job never blocks an urgent prescription notification.

---

### Q47. What is a Dead Letter Queue (DLQ) and why is it important?

**Answer:**

A Dead Letter Queue is where jobs go after they have failed all their retry attempts. Instead of being silently dropped, they land in the DLQ for investigation.

**Why it matters in Script Assist:** If a payment webhook job fails 5 times and is dropped, the order stays in `PAYMENT_PENDING` forever and the patient never gets their medication. With a DLQ, the operations team sees the failed job, investigates the cause, fixes it, and replays the job.

**My DLQ setup:**
- Every queue has a corresponding DLQ.
- Failed jobs are written to the DLQ with: job payload, error message, number of attempts, timestamp of each failure.
- An alert is fired when any job enters the DLQ.
- Operations can replay DLQ jobs through an internal admin tool after fixing the root cause.

Never let failed jobs disappear silently in a healthcare platform.

---

### Q48. Explain at-least-once vs exactly-once message delivery.

**Answer:**

**At-least-once:** The queue guarantees every message will be delivered, but may deliver it more than once. Your consumer must be idempotent to handle duplicates safely. This is the realistic guarantee most queue systems provide.

**Exactly-once:** Each message is delivered and processed exactly once. This is much harder to guarantee and usually requires distributed transactions or two-phase commits.

**My stance:** I always design for at-least-once delivery and make my consumers idempotent. Exactly-once is often more of a marketing claim than a hard guarantee — even systems that claim it have edge cases. It is safer to assume duplicates will happen.

**In practice:** Each job has an `eventId`. My consumer checks `WHERE event_id = ? AND processed = true` before processing. If already processed, it logs a "duplicate received, skipping" message and returns success. This is both idempotent and fully auditable.

---

### Q49. How would you design the batch/expiry tracking system for pharmacy inventory?

**Answer:**

Every product in the pharmacy has a batch number, lot number, and expiry date. The system needs to enforce FEFO (First Expired, First Out).

**Data model:**
```
inventory_batches
- id, tenant_id, product_id
- batch_number, lot_number
- quantity_available
- expiry_date
- status: AVAILABLE | EXPIRING_SOON | EXPIRED | QUARANTINE
```

**When dispensing:** Always select the batch with the nearest non-expired `expiry_date` first (FEFO). The prescription cannot be dispensed if only expired stock is available.

**Daily scheduled job:**
- Flag batches expiring within 30 days as `EXPIRING_SOON`
- Flag batches past expiry as `EXPIRED` (blocked from dispensing)
- Send email alerts to pharmacy managers for `EXPIRING_SOON` items
- Generate a daily expiry report for compliance records

---

### Q50. How do you handle notification delivery failures?

**Answer:**

Notification failures (email/SMS not delivered) must not be silent.

**My approach:**
1. Every notification is queued as a job — not sent synchronously.
2. If delivery fails, the job retries 3 times with exponential backoff.
3. After 3 failures, it goes to the DLQ and triggers an alert.
4. Every notification attempt (success or failure) is logged in a `notification_logs` table with the delivery status.
5. For critical notifications (prescription ready, payment confirmed), if email fails, the system falls back to SMS.

In a healthcare platform, a patient not receiving a "prescription ready" notification might wait days for medication they could have collected. Notification reliability is a patient safety issue, not just a UX issue.

---

### Q51. How do you design a rate limiter for outbound API calls?

**Answer:**

When calling external APIs (payment providers, shipping couriers, SMS gateways), I must respect their rate limits to avoid being blocked.

**Implementation using a token bucket algorithm:**
- A Redis key stores the current token count for each API.
- Each API call consumes one token.
- Tokens are replenished at the API's rate limit (e.g., 100 per minute).
- If no tokens are available, the job waits and retries.

BullMQ has built-in rate limiting for job processing:

```typescript
const queue = new Queue('sms-notifications', {
  limiter: {
    max: 100,    // max 100 jobs
    duration: 60000  // per minute
  }
});
```

This prevents exceeding the SMS gateway's rate limit even when a large batch of notifications fires simultaneously.

---

### Q52. How do you monitor queue health in production?

**Answer:**

A backed-up queue in a healthcare platform means delayed prescriptions and patient notifications. I set up monitoring on:

- **Queue depth:** Alert if any queue has more than 100 pending jobs (could indicate a worker crash).
- **Processing latency:** Alert if average job processing time exceeds 30 seconds.
- **Error rate:** Alert if more than 1% of jobs in any queue are failing.
- **DLQ size:** Alert immediately when any job enters the DLQ.
- **Worker count:** Alert if the number of active workers drops below the minimum.

I use Bull Board for visual monitoring and integrate queue metrics with Datadog or CloudWatch for automated alerting.

---

### Q53. How do you design a shipping tracking integration?

**Answer:**

Script Assist integrates with couriers to give patients real-time order tracking.

**Design:**
1. When an order is shipped, the pharmacy records the tracking number and courier name.
2. A background job polls the courier's tracking API every 2 hours (or listens to their webhooks if available).
3. When the tracking status changes (e.g., OUT_FOR_DELIVERY, DELIVERED), the job updates the order status and sends a patient notification.
4. If the courier API is unavailable, the polling job retries with backoff — it does not fail the order, it just retries the status update.

I prefer webhook-driven tracking over polling when couriers support it — it is more real-time and uses fewer API calls.

---

---

## SECTION 6: Database & Migrations

---

### Q54. How do you run zero-downtime migrations in a production system?

**Answer:**

The **Expand-Contract pattern** in 3 separate deployments:

**Step 1 — Expand:** Add the new column as `nullable`. Deploy. Old code still works fine.

**Step 2 — Backfill:** Run a background job to populate the new column for existing rows. Batch it in groups of 1000 to avoid table locks. Do not deploy new code yet.

**Step 3 — Contract:** Once all rows have values, add the `NOT NULL` constraint. Deploy new code that uses the column.

**Why this works:** The old code and new code can run simultaneously during the deployment window because the column is nullable in steps 1 and 2. There is no moment where both the old code and new constraint are active at the same time.

Never run `ALTER TABLE ADD COLUMN NOT NULL` directly on a large production table — it will lock the table and take down your platform.

---

### Q55. How do you design a database schema for a prescription entity?

**Answer:**

```sql
CREATE TABLE prescriptions (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id   UUID NOT NULL REFERENCES tenants(id),
  patient_id  UUID NOT NULL REFERENCES patients(id),
  clinician_id UUID NOT NULL REFERENCES users(id),
  product_id  UUID NOT NULL REFERENCES products(id),
  batch_id    UUID REFERENCES inventory_batches(id),  -- set when dispensed
  
  status      TEXT NOT NULL DEFAULT 'DRAFT',  -- state machine
  dosage      TEXT NOT NULL,
  days_supply INTEGER NOT NULL,
  
  idempotency_key TEXT UNIQUE,  -- prevents duplicate submissions
  
  prescribed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  dispensed_at    TIMESTAMPTZ,
  expires_at      TIMESTAMPTZ NOT NULL,
  
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version     INTEGER NOT NULL DEFAULT 1  -- optimistic locking
);

-- All queries are tenant-scoped — this index is critical
CREATE INDEX idx_prescriptions_tenant ON prescriptions(tenant_id, status, created_at DESC);
```

---

### Q56. What is an index and how do you decide which columns to index?

**Answer:**

An index is a data structure that makes lookups faster by avoiding full table scans. The tradeoff: indexes speed up reads but slow down writes slightly (because the index must be updated on every insert/update/delete).

**Rules I follow:**
- Always index foreign keys — `tenant_id`, `patient_id`, `product_id`.
- Index columns used in `WHERE` clauses in frequent queries.
- Index columns used in `ORDER BY` for sorted lists.
- For multi-tenant systems, make `tenant_id` the first column in composite indexes.
- Do not over-index — every index adds write overhead.

I use `EXPLAIN ANALYZE` to check query plans and identify missing indexes in a running system. A query with `Seq Scan` on a large table needs an index.

---

### Q57. What is a database transaction and when do you use it?

**Answer:**

A transaction is a group of database operations that either all succeed or all fail together — atomicity.

**When I use transactions in Script Assist:**
- Creating a prescription AND the initial audit log entry — both must succeed or neither should.
- Processing a payment AND updating the order status — both or neither.
- Dispensing an order AND decrementing inventory — if inventory decrement fails, the dispensing must also roll back.

**When I avoid long transactions:**
- Never hold a transaction open while making external API calls (like a payment API). The transaction holds database locks, and external calls can take seconds. Use the Outbox pattern instead.
- Never put multiple HTTP requests in a single transaction (impossible, but some architectures try to approximate this).

---

### Q58. How do you handle soft deletes vs hard deletes?

**Answer:**

**Soft delete:** The record is not removed from the database — instead, a `deleted_at` timestamp is set. The record remains queryable but is filtered out of normal queries.

**Hard delete:** The record is physically removed.

**For Script Assist, I use soft deletes for:**
- Prescriptions — these are medical records and must be retained.
- Patients — GDPR right to erasure means we anonymise PII but keep the medical record.
- Audit logs — never deleted, ever.
- Dispensing records — regulatory requirement to retain.

**For Script Assist, hard deletes are acceptable for:**
- Draft orders that were never submitted.
- Temporary session data.
- Notification queue entries after successful delivery.

Soft deletes require every query to include `WHERE deleted_at IS NULL` — I enforce this at the repository layer so no query accidentally returns deleted records.

---

### Q59. How do you handle N+1 query problems?

**Answer:**

An N+1 problem happens when you load a list of records and then query the database once per record for related data.

**Example (bad):**
```typescript
const prescriptions = await getPrescriptions(); // 1 query → 100 prescriptions
for (const rx of prescriptions) {
  rx.patient = await getPatient(rx.patientId); // 100 queries — one per prescription
}
// Total: 101 queries
```

**Solution — join or DataLoader:**
```typescript
// Option 1: Use a JOIN in the original query
const prescriptions = await db.prescription.findMany({
  include: { patient: true, product: true }
});
// Total: 1 query with JOINs

// Option 2: DataLoader (batch + deduplicate)
// Collects all patientIds, then fetches in one WHERE IN query
```

N+1 problems in a dispensing list of 500 orders would fire 500 extra database queries. In a regulated platform where query performance affects clinical workflows, this is unacceptable.

---

### Q60. How do you handle database connection pooling in a Node.js application?

**Answer:**

Node.js is single-threaded but uses async I/O. A database connection pool pre-creates a set of connections and reuses them across requests — creating a new connection for every request is expensive (50-100ms overhead).

**My configuration for Script Assist:**
- Pool size: 10-20 connections per application instance.
- If all connections are busy, new requests wait up to 5 seconds before failing with a "connection pool exhausted" error.
- With PgBouncer as a connection pooler in front of PostgreSQL, the database handles hundreds of application connections efficiently.
- In Kubernetes, each pod has its own pool — I size the pool so `pod_count × pool_size` does not exceed the database's max connections.

---

---

## SECTION 7: Security, GDPR & Compliance

---

### Q61. How do you handle GDPR compliance for patient data?

**Answer:**

GDPR requires: purpose limitation, data minimisation, security, retention limits, and the right to erasure.

**My approach:**
- **Purpose limitation:** Patient data is only used for clinical and dispensing purposes — never for marketing without explicit consent.
- **Data minimisation:** Only collect data that is needed — I question every new field added to a patient record.
- **Security:** Encryption at rest and in transit. Column-level encryption for highly sensitive fields (medication names, clinical notes).
- **Retention:** Automatic deletion or anonymisation after the retention period. UK medical records must be kept for a minimum period — I implement a scheduled job that anonymises PII after the retention period expires.
- **Right to erasure:** When a patient requests deletion, I anonymise PII (replace name with "PATIENT_DELETED", remove contact details) but retain the medical record structure for regulatory compliance.

---

### Q62. How do you implement authentication securely?

**Answer:**

**JWT-based authentication:**
- Short-lived access tokens (15 minutes) + long-lived refresh tokens (7 days).
- Refresh tokens are stored in the database (hashed) — when a user logs out, the refresh token is invalidated server-side. This is critical — JWTs cannot be invalidated client-side alone.
- Refresh tokens are rotated on every use — if an old refresh token is used (possible token theft), all sessions for that user are immediately revoked.
- Passwords are hashed with bcrypt (cost factor 12) — never stored in plain text.
- Failed login attempts are rate-limited — 5 failures trigger a temporary account lock.

**For healthcare:** Multi-factor authentication (MFA) should be required for clinicians — a compromised clinician account can access thousands of patient records.

---

### Q63. How do you protect against SQL injection?

**Answer:**

SQL injection is impossible when you use parameterised queries — and with an ORM like TypeORM or Prisma, all queries are parameterised by default.

**The danger zone is raw queries:**

```typescript
// DANGEROUS — never do this
const result = await db.query(`SELECT * FROM prescriptions WHERE id = '${id}'`);

// SAFE — always use parameterised queries
const result = await db.query('SELECT * FROM prescriptions WHERE id = $1', [id]);
```

In NestJS with TypeORM, I use the QueryBuilder API which always parameterises:
```typescript
await this.repo.createQueryBuilder('rx')
  .where('rx.id = :id AND rx.tenantId = :tenantId', { id, tenantId })
  .getOne();
```

I also set up a linting rule that flags any use of string interpolation in database queries.

---

### Q64. How do you implement RBAC (Role-Based Access Control)?

**Answer:**

In Script Assist, roles are: `super_admin`, `clinic_admin`, `clinician`, `pharmacist`, `patient`, `operations`.

**Implementation:**
1. Every user has a role assigned per tenant (a user could be a clinician at Clinic A and an admin at Clinic B).
2. Each role has a set of permissions (e.g., `prescriptions:create`, `dispensing:approve`).
3. NestJS guards check permissions on each endpoint:

```typescript
@UseGuards(AuthGuard, TenantGuard, PermissionGuard)
@RequiresPermission('dispensing:approve')
@Patch('dispensing/:id/approve')
async approveDispensing() { ... }
```

4. Permissions are checked against the requesting user's role for the current tenant.
5. A pharmacist from Tenant A with `dispensing:approve` permission cannot approve dispensing for Tenant B — the tenant guard runs before the permission guard.

---

### Q65. How do you secure sensitive API endpoints?

**Answer:**

For high-risk endpoints (prescription creation, payment processing, patient data access), I apply multiple layers:

- **Authentication:** Valid JWT required.
- **Tenant scope:** Request must be scoped to a valid tenant.
- **Role/permission check:** User must have the required role.
- **Rate limiting:** Strict per-user rate limits to prevent bulk data extraction.
- **IP allowlisting:** For internal admin endpoints, only known IP ranges are allowed.
- **Request signing:** For partner pharmacy API integrations, requests are signed with HMAC — the signature is verified before processing.
- **Audit logging:** Every access to a prescription is logged — who, when, what was accessed.

In a regulated healthcare platform, a data breach is not just a technical incident — it is a regulatory failure with real consequences.

---

### Q66. What is OWASP Top 10 and how do you apply it?

**Answer:**

OWASP is the Open Web Application Security Project. Their Top 10 lists the most critical web security risks.

**Most relevant to Script Assist:**

- **Broken Access Control:** I enforce tenant isolation + RBAC on every endpoint. Users cannot access other tenants' data by guessing IDs.
- **Injection:** All database queries are parameterised. Input is validated with class-validator before any processing.
- **Insecure Design:** I use threat modelling for sensitive flows — "what happens if an attacker gets a valid patient session token?"
- **Security Misconfiguration:** No debug endpoints in production. No default credentials. Secrets in environment variables, never in code.
- **Cryptographic Failures:** HTTPS everywhere. Passwords hashed with bcrypt. Sensitive data encrypted at rest.
- **Identification and Authentication Failures:** Short-lived tokens, refresh token rotation, rate-limited login.

---

### Q67. How do you handle secrets management?

**Answer:**

Secrets (database passwords, API keys, JWT secrets) must never be committed to code or stored in plain text.

**My approach:**
- Development: `.env` files (gitignored), with a `.env.example` showing the required variables.
- Production: Secrets stored in AWS Secrets Manager or HashiCorp Vault. The application fetches secrets at startup — never at build time.
- In CI/CD: Secrets are injected as environment variables at deploy time, never stored in the repository.
- Rotation: I implement secret rotation — database passwords change every 90 days. The application gracefully handles rotation by fetching the new secret without a restart.

If I ever discover a secret was accidentally committed to git, I treat it as compromised immediately — rotate it, then clean the git history.

---

### Q68. How do you prevent Cross-Site Request Forgery (CSRF)?

**Answer:**

CSRF attacks trick a logged-in user's browser into making an unwanted request to your API.

**My approach for Script Assist:**
- API endpoints use JWT authentication — JWTs are stored in memory or `httpOnly` cookies, not `localStorage`. An attacker cannot steal a `httpOnly` cookie via JavaScript.
- For cookie-based sessions, I use the `SameSite=Strict` cookie attribute — browsers will not send the cookie on cross-site requests.
- For state-changing operations from the frontend, I include the JWT in the `Authorization` header — simple cross-origin form submissions cannot set custom headers.
- I implement a CSRF token for any form-based submissions as an additional layer.

---

---

## SECTION 8: React & Frontend

---

### Q69. How would you build a complex multi-step clinical prescription form?

**Answer:**

Multi-step clinical forms are one of the most important UIs in Script Assist — a clinician's workflow depends on them being fast, reliable, and accessible.

**My approach:**
- **React Hook Form** for form state — it does not re-render on every keystroke, which matters with 20+ fields.
- **Zod** for validation schemas — defined once, shared between frontend and backend.
- **State machine for steps** — each step has a status: `not_started`, `in_progress`, `completed`, `error`. The user can go back to any completed step.
- **Auto-save** every 30 seconds to the backend + immediately to `localStorage` — if the session expires, no work is lost.
- **Accessibility** — every field has a `<label>`, error messages are announced to screen readers, form is fully keyboard-navigable.
- **Optimistic updates** — when the clinician submits, show "prescription created" immediately while the API call happens in the background.

---

### Q70. How do you manage state in a large React application?

**Answer:**

The golden rule: **state should live as close as possible to where it is used.**

**Server state** (data from APIs — prescription lists, product catalogues): I use **React Query (TanStack Query)**. It handles caching, background refetching, loading states, and error states automatically. I never put server data in Redux/Zustand — React Query is the right tool for this.

**Global UI state** (current user, tenant, notification banners): **Zustand** — simple, lightweight, no boilerplate.

**Complex local state** (multi-step form logic, wizard state): **`useReducer`** with typed actions — essentially a local state machine.

**Simple local state** (modal open/closed, input value): **`useState`** — no need for anything heavier.

---

### Q71. How do you handle form validation with TypeScript?

**Answer:**

I use **Zod** for schema validation because it generates TypeScript types automatically — I define the validation once and get type safety everywhere.

```typescript
// Define schema once
const createPrescriptionSchema = z.object({
  patientId: z.string().uuid(),
  productId: z.string().uuid(),
  daysSupply: z.number().min(1).max(90),
  dosageUnit: z.enum(['mg', 'ml', 'drops']),
});

// Type is inferred automatically — no duplication
type CreatePrescriptionForm = z.infer<typeof createPrescriptionSchema>;

// Use in React Hook Form
const { register, handleSubmit, formState: { errors } } =
  useForm<CreatePrescriptionForm>({
    resolver: zodResolver(createPrescriptionSchema)
  });
```

The same schema can be used on the backend for API validation — one source of truth for validation rules.

---

### Q72. How do you handle API calls and loading states in React?

**Answer:**

I use **React Query** for all API calls — it solves loading states, caching, error handling, and refetching automatically.

```typescript
const { data: prescriptions, isLoading, error } = useQuery({
  queryKey: ['prescriptions', tenantId, filters],
  queryFn: () => api.prescriptions.list(filters),
  staleTime: 2 * 60 * 1000,  // 2 minutes — good for prescription lists
});

// For mutations (create/update/delete)
const { mutate: createPrescription, isPending } = useMutation({
  mutationFn: api.prescriptions.create,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['prescriptions'] }),
  onError: (error) => showErrorNotification(error.message),
});
```

Loading skeletons for initial loads, inline spinners for mutations, and toast notifications for errors — all consistent across the platform.

---

### Q73. How do you implement performance optimisation in React?

**Answer:**

I follow the principle: **measure first, then optimise.** I use React DevTools Profiler to identify actual bottlenecks before adding complexity.

**Common optimisations I apply:**
- **React.memo** for components that receive the same props frequently — prevents unnecessary re-renders.
- **useMemo** for expensive calculations that should not rerun on every render.
- **useCallback** for functions passed as props to memoised child components.
- **Virtual rendering** (TanStack Virtual) for long lists — render only visible rows, not all 1000.
- **Code splitting** with `React.lazy` and `Suspense` — the pharmacy dispensing module does not need to load when the clinician is prescribing.
- **Image optimisation** — lazy load images, use appropriate formats and sizes.

In a pharmacy dispensing list with 500+ orders, virtual rendering is the difference between a 60fps smooth scroll and a janky unusable interface.

---

### Q74. How do you implement accessibility in a healthcare application?

**Answer:**

Accessibility in healthcare is not optional — clinical staff may use assistive technology, and some patients have disabilities.

**My checklist:**
- Every form field has a visible, properly associated `<label>`.
- Error messages are linked to their fields with `aria-describedby` — screen readers announce the error.
- Interactive elements are reachable by keyboard (Tab key) in a logical order.
- Focus management in multi-step forms — when moving to the next step, focus is moved to the step heading.
- Colour contrast meets WCAG AA (4.5:1 for normal text).
- No information is conveyed by colour alone — status badges also have text labels.
- Tested with a screen reader (NVDA/VoiceOver) as part of the accessibility checklist.

---

### Q75. How do you handle real-time updates in a React application?

**Answer:**

For real-time order status updates (dispensing progress, shipping tracking), I use **WebSockets or Server-Sent Events (SSE)** depending on the use case.

**SSE** (server pushes updates, client does not send): Perfect for prescription status updates — the patient's app shows "being dispensed → shipped → delivered" without polling.

**WebSockets** (bidirectional): For collaborative features — if two pharmacists are working on the same dispensing queue, they need to see each other's actions in real-time.

**With React Query:** I combine WebSocket/SSE with React Query's `queryClient.setQueryData` to update the cache when a real-time event arrives — so the UI updates instantly without a full refetch.

---

### Q76. How do you handle error boundaries in React?

**Answer:**

Error boundaries catch JavaScript errors in a component tree and show a fallback UI instead of crashing the entire application.

```typescript
class PrescriptionErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, info) {
    // Log to error monitoring (Sentry/Datadog)
    errorLogger.capture(error, { componentStack: info.componentStack });
  }
  
  render() {
    if (this.state.hasError) {
      return <PrescriptionErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

In a clinical application, if the prescription form crashes, the clinician must see a clear error message with a "Try Again" option — not a blank white screen.

---

### Q77. How do you implement a pharmacy dispensing dashboard with complex filters?

**Answer:**

A dispensing dashboard shows all pending orders with filters for status, date range, product, and patient. This is a read-heavy interface that needs to be fast and responsive.

**Key design decisions:**
- **URL-driven filters** — filter state is in the URL query string (`?status=PENDING&date=today`). This means a pharmacist can bookmark a filtered view and share it with colleagues.
- **Debounced search** — text search input triggers a query after 300ms of no typing, not on every keystroke.
- **Server-side filtering** — filters are applied in the database query, not in JavaScript. Never load all 500 orders and filter client-side.
- **Optimistic status updates** — when a pharmacist marks an order as dispensed, it disappears from the list immediately while the API call is in progress. If the API fails, it reappears with an error.
- **Infinite scroll** with cursor-based pagination — smooth loading of more orders as the pharmacist scrolls down.

---

### Q78. How do you handle TypeScript strictly in a large codebase?

**Answer:**

TypeScript's value is proportional to how strictly you use it.

**My rules:**
- `strict: true` in tsconfig — enables all strict checks. No exceptions.
- No `any` types — if I need to type something complex, I use `unknown` and narrow it properly.
- All API response types are defined — either with Zod (which generates types) or with explicit interfaces.
- Shared types live in a `@scriptassist/types` package that both frontend and backend import — no type duplication.
- Exhaustive switch checks — if I handle an enum in a switch, TypeScript errors if I miss a case.

```typescript
function getStatusLabel(status: PrescriptionStatus): string {
  switch (status) {
    case 'DRAFT': return 'Draft';
    case 'APPROVED': return 'Approved';
    // If I add a new status to the enum and forget to handle it here,
    // TypeScript gives a compile error — never a runtime surprise.
    default: const _exhaustive: never = status; return _exhaustive;
  }
}
```

---

---

## SECTION 9: Testing & Code Quality

---

### Q79. What is your testing philosophy?

**Answer:**

I follow the **testing pyramid**: many fast unit tests at the base, fewer integration tests in the middle, and a small number of E2E tests at the top.

In a regulated healthcare platform, the testing philosophy is: **if a bug here could delay a patient's medication or cause a billing error, it must have a test.**

**What I always test:**
- All business logic — state machine transitions, eligibility checks, calculation logic.
- All API endpoints — correct responses, validation errors, auth failures.
- All payment flows — happy path, failure path, duplicate request handling.
- All critical user journeys — E2E: clinician prescribes → pharmacist dispenses → patient gets notified.

**What I do not obsess over testing:**
- Simple data mapping (DTO to entity).
- Logging statements.
- Framework boilerplate.

---

### Q80. How do you test NestJS services with Jest?

**Answer:**

```typescript
describe('PrescriptionService', () => {
  let service: PrescriptionService;
  let mockRepo: jest.Mocked<PrescriptionRepository>;
  let mockPaymentService: jest.Mocked<PaymentService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        PrescriptionService,
        { provide: PrescriptionRepository, useValue: {
          findById: jest.fn(),
          save: jest.fn(),
        }},
        { provide: PaymentService, useValue: {
          charge: jest.fn(),
        }},
      ],
    }).compile();

    service = module.get(PrescriptionService);
    mockRepo = module.get(PrescriptionRepository);
  });

  it('should throw if prescription is already dispensed', async () => {
    mockRepo.findById.mockResolvedValue({ status: 'DISPENSED' });
    await expect(service.dispense('rx-001')).rejects.toThrow(AlreadyDispensedException);
  });
});
```

Every test uses mocks for external dependencies — no real database, no real payment API. Tests run in milliseconds.

---

### Q81. How do you write integration tests for API endpoints?

**Answer:**

I use **Supertest** with a real test database (not mocked) to test the full API stack — routing, validation, business logic, and database queries together.

```typescript
describe('POST /prescriptions', () => {
  it('should create a prescription and return 201', async () => {
    const response = await request(app.getHttpServer())
      .post('/prescriptions')
      .set('Authorization', `Bearer ${clinicianToken}`)
      .set('idempotency-key', 'test-key-001')
      .send({
        patientId: testPatient.id,
        productId: testProduct.id,
        daysSupply: 30
      });

    expect(response.status).toBe(201);
    expect(response.body.data.status).toBe('DRAFT');
  });

  it('should return 409 on duplicate idempotency key', async () => {
    // Submit the same request again
    const response = await request(app.getHttpServer())
      .post('/prescriptions')
      .set('idempotency-key', 'test-key-001') // same key
      .send({ ... });

    expect(response.status).toBe(200); // returns the original result
  });
});
```

---

### Q82. How do you write E2E tests with Playwright?

**Answer:**

Playwright E2E tests cover the critical user journeys that matter most — if these break, the platform is effectively down.

**My top 5 E2E tests for Script Assist:**
1. Clinician logs in → creates a prescription → prescription appears in pharmacy queue.
2. Pharmacist logs in → approves dispensing → patient receives notification.
3. Patient logs in → requests repeat prescription → sees status updates.
4. Payment flow — patient pays → order status updates → dispensing begins.
5. Inventory check — product out of stock → prescription is blocked from submission.

```typescript
test('clinician creates prescription', async ({ page }) => {
  await loginAs(page, 'clinician');
  await page.goto('/prescriptions/new');
  await page.fill('[data-testid="patient-search"]', 'John Smith');
  await page.click('[data-testid="patient-John-Smith"]');
  await page.selectOption('[data-testid="product-select"]', 'product-001');
  await page.fill('[data-testid="days-supply"]', '30');
  await page.click('[data-testid="submit-prescription"]');
  await expect(page.locator('[data-testid="success-banner"]')).toBeVisible();
});
```

---

### Q83. How do you ensure code quality in a team?

**Answer:**

Code quality is a team habit, not an individual effort. I establish it through:

**Automated tools (no human effort needed after setup):**
- ESLint with strict TypeScript rules — catches common mistakes at save time.
- Prettier for consistent formatting — no style debates in code review.
- Husky pre-commit hooks — run lint and tests before a commit is allowed.
- CI pipeline — all tests must pass before a PR can be merged.

**Process:**
- Every PR requires at least one review from another engineer.
- Code review checklist: is it correct? is it tested? is it observable? is it secure?
- Architecture Decision Records (ADRs) for significant design choices — so future engineers understand why decisions were made.

---

### Q84. How do you approach Test-Driven Development (TDD)?

**Answer:**

I use TDD selectively — for business logic and complex algorithms, I write the test first. For boilerplate and simple CRUD, I write code then test.

**TDD workflow for a new feature:**
1. Write a failing test that describes the expected behaviour.
2. Write the minimum code to make the test pass.
3. Refactor the code while keeping the test green.

**Example for prescription dispensing:**
```typescript
// First, write the failing test
it('should not allow dispensing an expired prescription', async () => {
  const expiredRx = { status: 'APPROVED', expiresAt: yesterday };
  await expect(service.dispense(expiredRx)).rejects.toThrow(PrescriptionExpiredException);
});

// Then implement the logic to make it pass
```

TDD is particularly valuable in regulated code because the tests serve as executable documentation of the compliance rules.

---

### Q85. How do you handle test data management?

**Answer:**

Test data management is often overlooked but critical for reliable tests.

**My approach:**
- **Factories** for creating test entities — `PrescriptionFactory.create({ status: 'APPROVED' })`. Factories have sensible defaults and allow overrides.
- **Database seeding** for integration tests — a test database is seeded with a known set of tenants, users, products before each test suite runs.
- **Test isolation** — each test runs in a database transaction that is rolled back after the test. Tests do not affect each other.
- **No shared test state** — never rely on data created by a previous test. Every test creates what it needs.

In a multi-tenant system, test data must always include `tenantId` — tests that forget this will accidentally test cross-tenant behaviour.

---

---

## SECTION 10: System Design

---

### Q86. How would you design the notification system for Script Assist?

**Answer:**

Notifications need to reach patients, clinicians, and pharmacists via email, SMS, and in-app notifications.

**Architecture:**
```
Event → Notification Queue → Notification Service → Channel Selector → Email/SMS/Push
```

1. Any domain event (prescription approved, order shipped) publishes to a notification queue.
2. The Notification Service reads the event, looks up the user's notification preferences, and determines which channels to use.
3. A Channel Selector routes to the appropriate provider (SendGrid for email, Twilio for SMS).
4. Every notification attempt is logged — channel, status, timestamp.
5. If email fails, fall back to SMS for critical notifications (medication ready, payment failed).

**Template management:** All notification templates are stored in the database (not hardcoded), supporting tenant-specific customisation and multi-language support in the future.

---

### Q87. How would you design the inventory management system for a pharmacy?

**Answer:**

Pharmacy inventory is complex because it involves: batch tracking, expiry management, reservations, and real-time availability checks for prescribing.

**Core entities:**
- `products` — catalogue of all available medications
- `inventory_batches` — specific batch with quantity, expiry date, lot number
- `stock_reservations` — temporary holds on stock during the prescribing flow (released if prescription is cancelled, confirmed if dispensed)

**Key flows:**
1. **Check availability** (called during prescribing): Sum available quantity across non-expired batches for the product.
2. **Reserve stock** (when prescription is approved): Create a `stock_reservation` record. This prevents double-booking.
3. **Confirm consumption** (when dispensed): Delete the reservation, decrement the batch quantity, record which batch was used.
4. **Reorder alert**: When available stock drops below the reorder threshold, create an alert for the pharmacy manager.

---

### Q88. How would you design the reporting system for prescription analytics?

**Answer:**

Clinics and pharmacies need reports on prescription volumes, revenue, processing times, and stock usage.

**Architecture:**
- Reports run as background jobs — never as synchronous API calls.
- Complex reports query a **read replica** — never the primary database.
- For very heavy reports (monthly revenue reconciliation), I use a separate analytics database or data warehouse populated by a nightly ETL job.
- Report results are cached and stored — a report once generated is saved and can be retrieved instantly without rerunning.
- Reports have a defined schema — the frontend knows exactly what columns to expect.

**Report types for Script Assist:**
- Prescription volume by clinician, product, date range
- Revenue reconciliation by tenant
- Average time from prescription to delivery
- Stock usage and reorder recommendations
- Compliance reports (for MHRA/CQC audits)

---

### Q89. How would you design the repeat prescription eligibility check?

**Answer:**

Before approving a repeat prescription, the system must verify several conditions:

```typescript
async function checkRepeatEligibility(request: RepeatRequest): Promise<EligibilityResult> {
  const checks = await Promise.all([
    checkOriginalPrescriptionValid(request),     // original not expired/cancelled
    checkProductInStock(request.productId),       // product available
    checkRepeatAllowanceNotExceeded(request),      // under max repeats
    checkMinimumIntervalSinceLastDispense(request), // e.g. min 25 days since last
    checkPatientAccountInGoodStanding(request),    // no outstanding payments
  ]);

  const failed = checks.filter(c => !c.passed);
  
  if (failed.length === 0) {
    return { eligible: true, autoApprove: true };
  }
  
  if (failed.some(c => c.requiresClinicalReview)) {
    return { eligible: true, autoApprove: false, reason: 'REQUIRES_CLINICIAN_REVIEW' };
  }
  
  return { eligible: false, blockers: failed };
}
```

Each check is independent and can be run in parallel. The result is either auto-approved, sent for clinician review, or blocked with clear reasons communicated to the patient.

---

### Q90. How would you approach designing the Wholesale SaaS module?

**Answer:**

Wholesale SaaS is Script Assist's upcoming feature — pharmacies restocking from wholesalers digitally.

**Key differences from clinic-to-patient flow:**
- Buyers are businesses (pharmacies), not patients — different KYC/onboarding requirements.
- Order quantities are much larger — bulk pricing, minimum order quantities.
- Credit terms — pharmacies may order on credit rather than paying immediately.
- Inventory management is the wholesaler's responsibility, not the pharmacy's.

**Architecture approach:**
- New `wholesale_orders` and `wholesale_catalogue` tables — do not pollute the existing prescription tables.
- Separate module in NestJS — `WholesaleModule` with its own service, repository, and API versioning.
- Shared infrastructure: notifications, payments, and audit logging can be reused.
- Data model: A wholesaler is a new tenant type with different role permissions.
- The existing multi-tenant architecture supports this cleanly — wholesalers are just a new category of tenant.

---

---

## SECTION 11: CEO / Founder Mindset Questions

---

### Q91. What does "ownership" mean to you as an engineer?

**Answer:**

Ownership means I treat the product as if it is mine. It means I do not just close a ticket and move on — I ask: is this the right solution? Will it scale? What happens when it breaks at 2am?

Ownership means proactive communication. If a deadline is unrealistic, I say so early — not the day before. If I see a potential data issue in a migration script, I raise it before running it.

Ownership means caring about outcomes, not just outputs. Shipping a feature is not success — the feature working reliably for clinicians and patients every day is success.

In a regulated platform where patient workflows depend on the system, ownership is not optional — it is the baseline expectation.

---

### Q92. How do you handle disagreement with technical decisions?

**Answer:**

I disagree by proposing, not complaining. If I think an architectural decision is wrong, I write a short document: the current approach, the problem I see, my proposed alternative, and the tradeoffs of each.

If my proposal is rejected after discussion, I commit fully to the agreed decision. "Disagree and commit" is a healthy engineering culture — debating decisions indefinitely wastes more time than occasionally choosing a suboptimal approach.

The one exception: if a decision creates a compliance or safety risk in a regulated platform, I escalate clearly. A decision that could result in a patient safety issue or a regulatory breach is worth pushing back on firmly.

---

### Q93. How do you handle working across time zones (India team with UK business hours)?

**Answer:**

The JD specifies UK business hours, and I am committed to that. The Script Assist team is in the UK, clinics and pharmacies are in the UK, and critical production issues happen during UK hours.

Practically: I structure my day around UK overlap — UK morning (which is early afternoon India time) for collaborative work — standups, code reviews, design discussions. UK afternoon for focused deep work. I over-communicate in writing — async updates in Slack mean the team is never wondering what I am working on.

I treat timezone as a responsibility, not a constraint — if I commit to UK hours, I am available during UK hours.

---

### Q94. Tell me about a time you made a mistake in production. What happened?

**Answer:**

In a previous role, I deployed a database migration that added an index to a large table without specifying `CONCURRENTLY`. The index creation locked the table for 4 minutes during peak hours. Users could not load data and we had to roll back the deployment.

What I learned: every migration now goes through a pre-deployment checklist. Index creation on large tables always uses `CREATE INDEX CONCURRENTLY`. Migrations are tested against a production data replica to measure actual execution time before deployment.

The mistake made our deployment process significantly safer — we added automated migration time estimation to the CI pipeline as a direct result.

> **Tip:** Always have a real story ready. "I never made a mistake" is not credible.

---

### Q95. How do you prioritise when you have multiple urgent tasks?

**Answer:**

I use a simple framework: impact × urgency.

**First:** Any issue affecting patient safety or data integrity. A prescription workflow that is silently failing is a P0 — everything else waits.

**Second:** Issues affecting paying clinic/pharmacy customers who are actively using the platform — a dispensing dashboard that is down during pharmacy hours needs to be fixed immediately.

**Third:** Issues affecting internal tools or admin workflows — important, but the business can operate without them for a few hours.

**Fourth:** Everything else — features, improvements, technical debt.

I communicate priorities clearly so the team agrees on the order — not so I can protect "my" tasks, but so the team's effort is aligned on what actually matters.

---

### Q96. What would you do in your first 30 days at Script Assist?

**Answer:**

**Week 1 — Understand:** Read the codebase, trace a full prescription flow from API to database, run the platform locally, understand the module structure. Do not write any production code yet.

**Week 2 — Learn:** Talk to the engineers who built the system. Understand the design decisions and the tradeoffs. Look at the open bugs and support tickets — they tell you where the pain points are.

**Week 3 — Contribute:** Ship one small feature or fix — something safe that shows I understand the codebase and can contribute without breaking things.

**Week 4 — Propose:** Write up my understanding of one product area, identify one improvement, and present it to the team. Get feedback. This validates my understanding and shows I can think at the product level.

---

### Q97. How do you think about technical debt in a startup?

**Answer:**

Technical debt is not inherently bad — it is a tool. Sometimes taking on debt is the right decision to ship faster and validate an idea. The problem is when debt is unmanaged and unacknowledged.

**In a regulated healthcare platform, there are two types of debt:**

**Acceptable debt:** Code that works correctly and safely but could be cleaner or more elegant. We document it and address it when we have capacity.

**Dangerous debt:** Shortcuts in audit logging, skipped idempotency checks, incomplete tenant isolation. These must be fixed before they become compliance failures or patient safety issues. I flag these immediately and make a case for prioritising them.

My rule: dangerous debt must be fixed before the next release cycle. Acceptable debt is tracked and cleaned up regularly.

---

### Q98. Script Assist is growing fast. How do you ensure quality does not degrade as the team scales?

**Answer:**

Quality degrades when teams scale without deliberate effort to maintain standards. The things I would focus on:

**Automation over process:** Automated tests, linting, and CI checks catch quality issues without human effort. If it can be automated, it should be.

**Clear module ownership:** As the codebase grows, every module should have a clear owner who understands it deeply and reviews changes to it.

**Architecture Decision Records:** Document significant design decisions so new engineers understand the "why", not just the "what".

**Definition of Done:** Every feature must have: tests written, error handling implemented, audit logging added, feature documented, deployed to staging and verified. No shortcuts.

**Regular technical debt sprints:** One sprint in four is dedicated to cleanup — tests, refactoring, documentation. This is not optional; it is scheduled.

---

### Q99. What motivates you as an engineer?

**Answer:**

I am motivated by building things that actually matter. Code that runs in a production system used by real people every day — that is meaningful work.

At Script Assist, the stakes are real. A reliable dispensing workflow means a patient gets their medication on time. A correct audit trail means a clinic can prove compliance in a CQC inspection. That is not abstract — it has a direct impact on real people's lives and health.

I am also motivated by technical depth. Systems with real constraints — multi-tenancy, idempotency, regulatory compliance, zero-downtime migrations — require real engineering skill. I enjoy problems where there is no shortcut and the details actually matter.

---

### Q100. Do you have any concerns about this role?

**Answer:**

This is an invitation to have an honest conversation — not a trick question.

"One thing I want to make sure I understand is the on-call expectations. With a platform serving UK clinics and pharmacies during business hours, I want to understand what production incidents look like and what the escalation process is."

"I also want to understand the current technical debt situation — not because I am concerned about it, but because I want to know where to direct my energy in the first few months."

"Overall, this is the kind of role and product that genuinely excites me — the technical challenges are real, the domain is meaningful, and the team is clearly serious about building something of quality."

---

---

## 🎤 QUESTIONS YOU SHOULD ASK AT THE END

*Asking strong questions is one of the most impactful things you can do in an interview. It shows you think strategically, not just technically. Ask 3–4 of these.*

---

### Architecture & Technical

**1.** What does the current multi-tenancy architecture look like — shared schema with tenant_id, or isolated schemas? Are there plans to evolve it as you scale to more clinics?

**2.** What has been the biggest reliability challenge in the dispensing or prescribing workflow so far — and how did the team resolve it?

**3.** What does the observability stack look like today? When something goes wrong in production at 2am, what does the incident response process look like?

**4.** With Wholesale SaaS coming soon — how is the team thinking about the data model changes needed to support wholesale buyers without breaking existing clinic/pharmacy tenants?

**5.** How are database migrations handled across tenants today — is there a migration framework, or is it manual?

---

### Team & Culture

**6.** How is the engineering team structured today — are there separate frontend and backend engineers, or full-stack ownership of features end-to-end?

**7.** What does the code review process look like? How does the team balance shipping speed with code quality in a regulated environment?

**8.** How do engineers at Script Assist grow? Is there a clear path from senior engineer to tech lead or principal?

---

### Product & Business

**9.** What are the biggest product priorities for the next 6 months? Are there any technical challenges in those areas you are already thinking about?

**10.** How does the team handle the tension between moving fast (startup needs) and moving carefully (regulated healthcare requirements)?

**11.** You currently have 15 active clinics and 25,000+ patients. What does the growth trajectory look like — are there specific verticals or regions you are targeting next?

---

### Role-Specific

**12.** Which product area or module would I be owning primarily in the first 3 months? What does success look like in that area?

**13.** What does the onboarding process for engineers look like — is there a structured ramp-up period, or is it more learn-as-you-go?

**14.** What is the biggest technical challenge the team is facing right now that the person in this role would be expected to help solve?

**15.** What does the team look like in India currently — how many engineers, and how does collaboration with the UK team work in practice day-to-day?

---

---

## 📌 QUICK REFERENCE — KEY TERMS TO USE

| Term | Use it when talking about... |
|------|------------------------------|
| **Idempotency** | Payments, dispensing, queue consumers — preventing double-processing |
| **Tenant isolation** | Multi-tenancy, data segregation, GDPR |
| **Audit trail** | Compliance, regulated operations, state changes |
| **Expand-contract** | Zero-downtime migrations |
| **DLQ (Dead Letter Queue)** | Queue systems, failed job handling |
| **Outbox pattern** | Database + event consistency |
| **FEFO** | Pharmacy inventory, batch/expiry management |
| **At-least-once delivery** | Queue consumers, idempotent processing |
| **Row Level Security** | Database-level tenant isolation in PostgreSQL |
| **State machine** | Order/prescription lifecycle design |
| **MHRA** | UK medicines regulator — shows domain knowledge |
| **CQC** | UK health and social care regulator |
| **Compensating transaction** | Saga pattern, failure recovery |
| **Optimistic locking** | Concurrent update safety |
| **Cursor-based pagination** | Performance at scale for large datasets |

---

## ✅ FINAL TIPS

- **Address Arjun by name** — "That is a great question Arjun" shows preparation.
- **Use Script Assist's real numbers** — 15 clinics, 25,000+ patients, 80%+ in 48 hours.
- **Use domain language** — prescribing, dispensing, audit trail, tenant isolation.
- **Show ownership mindset** — "I would want to make sure..." not "Someone should..."
- **Mention regulated context** — "In an MHRA-regulated environment, correctness means..."
- **Ask 3–4 questions at the end** — it shows genuine interest and strategic thinking.
- **Be honest if you do not know** — "I have not used that specific tool, but I have used X which solves a similar problem, and I pick things up quickly."

---

*Good luck — you have done the hard work by getting to this round. Now show them who you are.*
