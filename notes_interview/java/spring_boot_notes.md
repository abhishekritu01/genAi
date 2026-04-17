# 🚀 Spring Boot – Complete Interview Ready Notes
> Every concept explained in interview-answerable language. No term left undefined.

---

## 📌 Table of Contents
1. [Core Spring & Spring Boot Basics](#1-core-spring--spring-boot-basics)
2. [Key Annotations – Explained](#2-key-annotations--explained)
3. [Spring Beans & Dependency Injection](#3-spring-beans--dependency-injection)
4. [Spring Boot Actuator & Monitoring](#4-spring-boot-actuator--monitoring)
5. [REST API Development](#5-rest-api-development)
6. [JPA & Database Persistence](#6-jpa--database-persistence)
7. [Spring Boot Security](#7-spring-boot-security)
8. [Microservices & Spring Cloud](#8-microservices--spring-cloud)
9. [Caching, Async & Scheduling](#9-caching-async--scheduling)
10. [Logging](#10-logging)
11. [Testing](#11-testing)
12. [Advanced & Real-World Scenarios](#12-advanced--real-world-scenarios)
13. [Quick-Fire One-Liners](#-quick-fire-one-liners-last-minute-revision)

---

## 1. Core Spring & Spring Boot Basics

### What is Spring Framework?
Spring is a lightweight, open-source Java framework that helps you build enterprise applications. Its core strength is that it manages object creation and wiring for you through IoC and DI, so you don't need to manually create and connect your objects. It also provides AOP, transaction management, security, and web support.

### What is Spring Boot?
Spring Boot is built on top of Spring Framework. Its goal is to eliminate all the manual setup and configuration that Spring requires. It gives you auto-configuration (Spring decides sensible defaults based on your classpath), an embedded server (no need to install Tomcat separately), and production-ready features like health checks and metrics — all out of the box.

### Spring vs Spring Boot

| Feature | Spring | Spring Boot |
|---|---|---|
| Configuration | Manual XML/Java config | Auto-configuration |
| Server | External (Tomcat/Jetty) | Embedded server |
| Deployment | WAR | JAR (standalone) |
| Boilerplate | High | Minimal |
| Monitoring | Manual setup | Actuator built-in |

### JAR vs WAR
- **JAR (Java ARchive)** – A self-contained package that includes your application code AND an embedded server. You run it directly with `java -jar app.jar`. Spring Boot uses JAR by default.
- **WAR (Web ARchive)** – A package meant to be deployed inside an external web server like Apache Tomcat. You cannot run a WAR directly; the server must unpack and host it.

> **Interview tip:** "Spring Boot prefers JAR because it packages everything including the server, making deployment simpler — especially in Docker/Kubernetes environments."

### Inversion of Control (IoC)
IoC means you give up control of object creation to the Spring container. Normally, if class A needs class B, A would do `new B()` itself. With IoC, Spring creates B and gives it to A. This makes your code loosely coupled and easier to test.

### Dependency Injection (DI)
DI is the mechanism Spring uses to implement IoC. When your class needs a dependency (another object), Spring *injects* it — either through the constructor, a setter method, or directly into a field. DI is a specific form of IoC.

> **Simple analogy:** IoC is the concept ("someone else manages objects"), DI is how Spring actually does it ("Spring injects them into your class").

### IoC Container
The IoC container is the heart of Spring. It reads your bean definitions (from annotations or XML), creates all the objects (beans), injects their dependencies, and manages their entire lifecycle from creation to destruction.

Two types:
- **BeanFactory** – The basic, bare-minimum container. It uses *lazy loading*, meaning beans are created only when you first ask for them. Good for memory-constrained environments.
- **ApplicationContext** – The full-featured container used in almost every real application. It uses *eager loading* (creates all beans at startup), supports AOP, event publishing, internationalization, and annotation-based config. Always prefer this.

### Auto-Configuration
Auto-configuration is Spring Boot's ability to look at what's on your classpath and automatically set up the beans you probably need — without you writing any configuration code.

**How it works internally:**
1. `@EnableAutoConfiguration` (part of `@SpringBootApplication`) kicks off the process.
2. Spring reads `META-INF/spring.factories` to find a list of auto-configuration classes.
3. Each class uses conditions like `@ConditionalOnClass` or `@ConditionalOnMissingBean` to decide whether to apply.

**Example:** If you add `spring-boot-starter-data-jpa`, Spring Boot sees Hibernate on the classpath and automatically configures a `DataSource`, `EntityManagerFactory`, and `TransactionManager`.

**Disable specific auto-config:**
```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
```

### Spring Boot Starters
Starters are pre-packaged sets of dependencies for common use cases. Instead of manually adding 5–10 individual libraries, you add one starter and get everything you need.

- `spring-boot-starter-web` → Spring MVC + embedded Tomcat + Jackson (JSON)
- `spring-boot-starter-data-jpa` → JPA + Hibernate + Spring Data + HikariCP
- `spring-boot-starter-security` → Spring Security
- `spring-boot-starter-actuator` → Monitoring & management endpoints
- `spring-boot-starter-test` → JUnit + Mockito + AssertJ

### @SpringBootApplication
This single annotation on your main class does three things:
```java
@Configuration           // This class can define @Bean methods
@EnableAutoConfiguration // Enable Spring Boot's auto-config mechanism
@ComponentScan           // Scan this package and sub-packages for components
```

### Profiles
Profiles let you define different configurations for different environments (dev, test, prod) and activate only the relevant one at runtime.

```properties
# application-dev.properties → used in development
spring.datasource.url=jdbc:h2:mem:testdb

# application-prod.properties → used in production
spring.datasource.url=jdbc:mysql://prod-server/mydb
```

**Activate profile:**
```properties
spring.profiles.active=dev
```
```bash
java -jar app.jar --spring.profiles.active=prod
```

### application.properties vs application.yml

| Feature | .properties | .yml |
|---|---|---|
| Format | Flat key=value | Hierarchical/nested |
| Readability | Simple, familiar | Cleaner for complex configs |
| Example | `server.port=8080` | `server:\n  port: 8080` |

Both work the same way — use whichever your team prefers.

---

## 2. Key Annotations – Explained

### Stereotype Annotations
These tell Spring what role a class plays and to manage it as a bean.

| Annotation | Meaning & When to Use |
|---|---|
| `@Component` | Generic Spring-managed bean. Use when the class doesn't clearly fit service or DAO role. |
| `@Service` | Business logic layer. Functionally same as `@Component` but communicates intent clearly. |
| `@Repository` | Data access layer (DAO). Same as `@Component` but also catches DB-specific exceptions and wraps them into Spring's `DataAccessException`. |
| `@Controller` | Handles web requests in an MVC app. Returns a view name (HTML/JSP). |
| `@RestController` | Combines `@Controller` + `@ResponseBody`. Every method returns data (JSON/XML) directly as the HTTP response body, not a view. |

### Request Mapping Annotations

| Annotation | Meaning |
|---|---|
| `@RequestMapping("/path")` | Maps any HTTP method to this URL. Restrict with `method = RequestMethod.GET`. |
| `@GetMapping` | Shortcut for GET — used to *read/fetch* data. |
| `@PostMapping` | Shortcut for POST — used to *create* data. |
| `@PutMapping` | Shortcut for PUT — used to *update/replace* entire resource. |
| `@DeleteMapping` | Shortcut for DELETE — used to *delete* a resource. |
| `@PatchMapping` | Shortcut for PATCH — used to *partially update* a resource. |

### Bean & Configuration Annotations

**`@Configuration`**
Marks a class as a source of bean definitions. Spring processes this class specially — methods annotated with `@Bean` are intercepted so beans are singletons by default.

**`@Bean`**
Placed on a method inside a `@Configuration` class. Spring calls this method and registers the returned object as a bean. Use it when you need to configure third-party objects that you can't annotate directly.
```java
@Bean
public ObjectMapper objectMapper() {
    return new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
}
```

**`@Autowired`**
Tells Spring to inject a dependency automatically by type. Spring looks in the container for a bean matching the field/parameter type and injects it.

**`@Qualifier("beanName")`**
Used together with `@Autowired` when there are multiple beans of the same type. You specify exactly which one you want by name.
```java
@Autowired
@Qualifier("emailNotificationService")
private NotificationService notificationService;
```

**`@Primary`**
When multiple beans of the same type exist, `@Primary` marks one as the default. If no `@Qualifier` is specified, Spring picks the `@Primary` bean.

**`@Lazy`**
By default, Spring creates all singleton beans at startup. `@Lazy` tells Spring to delay creation until the bean is first actually needed. Useful for expensive beans that may not always be used.

**`@Scope`**
Defines how many instances of a bean Spring creates. Default is `singleton`. Use `@Scope("prototype")` when each requester should get their own fresh copy.

### Lifecycle Annotations

**`@PostConstruct`**
Method runs once after the bean is created and all dependencies are injected. Use it for initialization logic (e.g., loading config, warming caches).

**`@PreDestroy`**
Method runs just before the bean is destroyed (when the application shuts down). Use it for cleanup (e.g., closing connections, flushing data).

```java
@PostConstruct
public void init() { System.out.println("Bean ready"); }

@PreDestroy
public void cleanup() { System.out.println("Bean destroyed"); }
```

### Property Injection

**`@Value`** – Injects a single property value from `application.properties`:
```java
@Value("${app.name}")
private String appName;

@Value("${app.timeout:5000}") // 5000 is default if not found
private int timeout;
```

**`@ConfigurationProperties`** – Binds a group of related properties to a POJO. Cleaner than multiple `@Value` annotations:
```java
@ConfigurationProperties(prefix = "app")
@Component
public class AppConfig {
    private String name;
    private int timeout;
    private String dbUrl;
    // getters and setters
}
```
Properties file:
```properties
app.name=MyApp
app.timeout=5000
app.db-url=jdbc:mysql://localhost/mydb
```

### Conditional Bean Annotations

**`@ConditionalOnClass`** – Creates the bean only if a specific class exists on the classpath. This is how auto-configuration is selective — e.g., only configure Redis beans if the Redis client library is present.

**`@ConditionalOnMissingBean`** – Creates the bean only if no bean of that type has already been defined by the user. This lets auto-configuration provide defaults while allowing users to override them.

### Web/REST Annotations

| Annotation | What it does |
|---|---|
| `@RequestBody` | Deserializes the JSON/XML from the request body into a Java object using Jackson. |
| `@PathVariable` | Extracts a value embedded in the URL path. E.g., `/users/{id}` → `@PathVariable Long id` |
| `@RequestParam` | Extracts a query string parameter. E.g., `/users?page=2` → `@RequestParam int page` |
| `@ResponseBody` | Serializes the return value of a method to JSON/XML and writes it to the HTTP response. Already included in `@RestController`. |
| `@CrossOrigin` | Allows browsers to make requests from a different domain (CORS). E.g., React app on port 3000 calling an API on port 8080. |
| `@ControllerAdvice` | A global class that intercepts exceptions thrown from any controller. Used for centralized error handling. |
| `@ExceptionHandler` | Placed inside `@ControllerAdvice`, defines which exception type this method handles and what response to return. |

### Validation Annotations

| Annotation | What it validates |
|---|---|
| `@Valid` | Triggers validation on the annotated object. Must be present to activate constraints. |
| `@NotNull` | Field must not be `null`. Empty string `""` is allowed. |
| `@NotEmpty` | Field must not be `null` or empty string `""`. Whitespace `"   "` is allowed. |
| `@NotBlank` | Field must not be `null`, empty, or whitespace-only. Most strict. Use for strings. |
| `@Size(min=2, max=50)` | String length or collection size must be within the given range. |
| `@Email` | String must be a valid email format (contains `@` and domain). |
| `@Min(value)` / `@Max(value)` | Numeric value must be above/below the given number. |
| `@Pattern(regexp="")` | String must match the regular expression. |

### Scheduling & Async

**`@EnableScheduling`** – Activates Spring's task scheduling infrastructure. Without this, `@Scheduled` methods won't run.

**`@Scheduled`** – Marks a method to run automatically on a schedule:
```java
@Scheduled(fixedRate = 5000)            // Runs every 5 seconds from start of last execution
@Scheduled(fixedDelay = 5000)           // Waits 5s after last execution ENDS before running again
@Scheduled(cron = "0 30 9 * * MON-FRI")// 9:30 AM on weekdays
```

**`@EnableAsync`** – Activates Spring's async execution infrastructure. Without this, `@Async` is ignored.

**`@Async`** – Marks a method to run in a separate thread from a thread pool. The caller doesn't wait.

### Caching Annotations

**`@EnableCaching`** – Activates Spring's caching proxy infrastructure.

**`@Cacheable("cacheName")`** – Before executing the method, Spring checks the cache. If result exists → return it without calling the method. If not → run method, store result, return it.

**`@CacheEvict("cacheName")`** – Removes an entry from the cache. Use this when data is deleted or updated so stale data doesn't stay.

**`@CachePut("cacheName")`** – Always executes the method AND updates the cache with the new result. Use when you want to refresh cache after an update.

---

## 3. Spring Beans & Dependency Injection

### What is a Spring Bean?
A Spring Bean is simply a Java object that is created, configured, and managed by the Spring IoC container. You don't create it with `new` — Spring does it for you based on your annotations or configuration.

### Bean Lifecycle (step by step)
1. **Bean definition loaded** – Spring reads `@Component`, `@Bean`, XML, etc.
2. **Instantiated** – Spring calls the constructor
3. **Dependencies injected** – `@Autowired` fields/constructor params are set
4. **`@PostConstruct` runs** – Your custom initialization logic
5. **Bean is ready and in use** – Serves requests
6. **`@PreDestroy` runs** – Your cleanup logic
7. **Bean is destroyed** – Removed from container on shutdown

### Bean Scopes – Full Explanations

**`singleton` (default)**
Only one instance of the bean exists per Spring container. Every class that injects this bean gets the same shared object. This is the most common and memory-efficient scope. Use for stateless beans (services, repositories).

**`prototype`**
Spring creates a brand-new instance every single time the bean is requested. Two classes injecting the same prototype bean get two different objects. Use for stateful beans where each caller needs their own isolated copy.

**`request`**
One instance per HTTP request. The bean is created when a request comes in and destroyed when the response is sent. Only valid in web applications. Use for things like tracking request-specific data.

**`session`**
One instance per HTTP session. The bean lives as long as the user's session (e.g., logged-in shopping cart). Only valid in web applications.

**`application`**
One instance per `ServletContext` — essentially one per deployed application. Similar to singleton but specifically scoped to the web application context.

**`websocket`**
One instance per WebSocket session. Used in real-time WebSocket applications.

### Injection Types – Compared

**Constructor Injection (Recommended):**
```java
@Service
public class OrderService {
    private final PaymentService paymentService;

    // Spring injects automatically (no @Autowired needed in modern Spring)
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```
✅ Dependencies are mandatory and explicit. ✅ Field is `final` (immutable). ✅ Easy to unit test. ✅ Circular dependencies visible at startup.

**Setter Injection:**
```java
@Autowired
public void setPaymentService(PaymentService paymentService) {
    this.paymentService = paymentService;
}
```
✅ Good for optional dependencies. ❌ Mutable — someone could call the setter at any time.

**Field Injection (Not Recommended):**
```java
@Autowired
private PaymentService paymentService;
```
✅ Shortest syntax. ❌ Hard to unit test. ❌ Hides dependencies. ❌ Can't make field `final`.

### Circular Dependency
This happens when Bean A depends on Bean B, and Bean B depends on Bean A.

- Spring **can** resolve with setter injection (creates A first, then B, then sets them into each other).
- Spring **cannot** resolve with constructor injection — throws `BeanCurrentlyInCreationException`.
- Best fix: redesign to break the cycle. Workaround: add `@Lazy` on one of the injections.

### @Qualifier vs @Primary
- **`@Primary`** – Set it on the bean you want as the default. Spring uses it when there's ambiguity and no `@Qualifier` is given.
- **`@Qualifier`** – More specific. Use it at the injection point to say exactly which bean you want by name.

```java
@Component @Primary
public class EmailService implements NotificationService { ... }

@Component
public class SmsService implements NotificationService { ... }

// Will inject EmailService (it's @Primary)
@Autowired
private NotificationService notificationService;

// Will inject SmsService specifically
@Autowired @Qualifier("smsService")
private NotificationService smsNotification;
```

### Inject Prototype Bean into Singleton (Problem & Solution)
If you inject a prototype bean into a singleton, the singleton gets the prototype injected once at startup — making it effectively a singleton. To get a fresh prototype instance each time:

```java
// Solution 1: ObjectFactory
@Autowired
private ObjectFactory<PrototypeBean> factory;

public void doWork() {
    PrototypeBean bean = factory.getObject(); // fresh instance each time
}

// Solution 2: @Lookup (Spring overrides this method at runtime)
@Lookup
public PrototypeBean getPrototypeBean() {
    return null; // Spring replaces this body
}
```

### BeanFactory vs ApplicationContext

| Feature | BeanFactory | ApplicationContext |
|---|---|---|
| Loading strategy | Lazy (bean created on first request) | Eager (all beans at startup) |
| Event publishing | No | Yes |
| AOP support | Limited | Full |
| Internationalization | No | Yes |
| Use case | Resource-constrained (rare) | Every real-world app |

### BeanFactoryPostProcessor
An interface that allows you to modify bean *definitions* (the recipe for creating beans) after Spring reads them but before it actually creates the beans. Example: `PropertySourcesPlaceholderConfigurer` uses this to resolve `${...}` placeholders.

### ApplicationContextAware
An interface a bean can implement to get a reference to the `ApplicationContext` itself. Useful when you need to programmatically look up beans at runtime.

### FactoryBean
A special interface for beans whose creation logic is complex. The container returns whatever `getObject()` returns, not the `FactoryBean` itself. Used by Spring internally (e.g., `ProxyFactoryBean` for AOP).

---

## 4. Spring Boot Actuator & Monitoring

### What is Spring Boot Actuator?
Actuator is a Spring Boot module that automatically exposes HTTP endpoints giving you visibility into the internals of your running application — without writing any code. You can check health, view metrics, see environment properties, and more.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Key Endpoints

| Endpoint | What it shows |
|---|---|
| `/actuator/health` | App health: UP/DOWN. Also shows DB connectivity, disk space, etc. |
| `/actuator/metrics` | JVM memory, GC stats, HTTP request counts, thread counts |
| `/actuator/info` | Custom app info you define (version, name, build info) |
| `/actuator/env` | All environment properties, system variables, config values |
| `/actuator/loggers` | View current log levels; change them at runtime without restart |
| `/actuator/threaddump` | Snapshot of all running threads — useful for debugging deadlocks |
| `/actuator/prometheus` | Metrics in Prometheus scraping format |

### Expose & Secure Endpoints
By default, only `/health` and `/info` are exposed. To expose more:
```properties
management.endpoints.web.exposure.include=health,info,metrics,loggers
# Restrict health endpoint to ADMIN role:
management.endpoint.health.roles=ADMIN
```

### What is Micrometer?
Micrometer is the metrics collection library built into Spring Boot Actuator. It acts as a vendor-neutral facade — you write metrics code once, and it exports to any monitoring system (Prometheus, Datadog, New Relic) by just changing a dependency.

### Prometheus + Grafana Integration
1. Add `micrometer-registry-prometheus` to `pom.xml`
2. Spring exposes metrics at `/actuator/prometheus` in Prometheus format
3. Configure Prometheus to scrape that endpoint
4. Connect Grafana to Prometheus as a data source
5. Import Spring Boot dashboards to visualize CPU, memory, HTTP latency, etc.

### Custom Actuator Endpoint
```java
@Endpoint(id = "appinfo")  // Accessible at /actuator/appinfo
@Component
public class AppInfoEndpoint {
    @ReadOperation  // HTTP GET
    public Map<String, String> info() {
        return Map.of("status", "running", "version", "1.0");
    }
}
```

---

## 5. REST API Development

### What is REST?
REST (Representational State Transfer) is an architectural style for building APIs over HTTP. A RESTful API uses standard HTTP methods (GET, POST, PUT, DELETE), is stateless (no session), and communicates via JSON or XML.

### Creating a REST API
```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(service.findUser(id));
    }

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
        User saved = service.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### @PathVariable vs @RequestParam
```java
// URL: GET /users/42  → PathVariable extracts from path
@GetMapping("/{id}")
public User get(@PathVariable Long id) { ... }

// URL: GET /users?page=2&size=10  → RequestParam extracts query params
@GetMapping
public Page<User> list(@RequestParam int page, @RequestParam int size) { ... }
```

### ResponseEntity
`ResponseEntity<T>` gives you full control over the HTTP response — status code, headers, and body.

```java
ResponseEntity.ok(data)                          // 200 OK
ResponseEntity.status(201).body(data)            // 201 Created
ResponseEntity.noContent().build()               // 204 No Content
ResponseEntity.notFound().build()                // 404 Not Found
ResponseEntity.badRequest().body("Error msg")    // 400 Bad Request
```

### Global Exception Handling
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors()
            .stream().map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return ResponseEntity.badRequest().body(new ErrorResponse("VALIDATION_FAILED", message));
    }
}
```

### REST API Versioning Strategies
1. **URI versioning** (most common): `/api/v1/users`, `/api/v2/users`
2. **Request param**: `/users?version=1`
3. **Header-based**: `X-API-VERSION: 1`
4. **Content negotiation**: `Accept: application/vnd.company.v1+json`

### Pagination
```java
@GetMapping
public Page<User> getUsers(Pageable pageable) {
    return repo.findAll(pageable);
}
// Request: GET /users?page=0&size=10&sort=name,asc
```

### RestTemplate vs WebClient

| | RestTemplate | WebClient |
|---|---|---|
| Threading model | Blocking (waits for response) | Non-blocking (doesn't wait) |
| Style | Synchronous | Asynchronous / reactive |
| Status | Legacy (still works) | Recommended for new code |

### REST vs SOAP

| | REST | SOAP |
|---|---|---|
| Format | JSON or XML | XML only |
| Protocol | HTTP | Any transport |
| Flexibility | High | Rigid (WSDL contract) |
| Performance | Lightweight & fast | Heavier due to XML envelope |

---

## 6. JPA & Database Persistence

### What is JPA?
JPA (Java Persistence API) is a *specification* — it defines standard annotations and APIs for mapping Java objects to database tables. It is not a framework itself. Implementations like **Hibernate** do the actual work of generating SQL, managing connections, and executing queries.

### What is ORM?
ORM (Object-Relational Mapping) is the technique of automatically mapping Java objects to database tables and vice versa. Instead of writing `INSERT INTO users VALUES (...)`, you just call `save(user)` and ORM generates the SQL for you.

### JDBC vs JPA vs Hibernate

| | JDBC | JPA | Hibernate |
|---|---|---|---|
| What it is | Low-level DB API | ORM Specification | JPA Implementation |
| SQL | Manual | Auto-generated | Auto-generated |
| Boilerplate | Very high | Low | Low |

### Entity Basics
```java
@Entity                        // Maps this class to a DB table
@Table(name = "users")         // Specifies table name (defaults to class name if omitted)
public class User {

    @Id                        // This field is the primary key
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;

    @Enumerated(EnumType.STRING)  // Stores "ADMIN" or "USER" (not 0 or 1)
    private Role role;

    @Transient                 // NOT saved to DB
    private String displayName;
}
```

### GenerationType Strategies – Explained

**`IDENTITY`** – The database column is set to auto-increment (e.g., MySQL `AUTO_INCREMENT`). Spring inserts the row and the DB assigns the next ID. Most common strategy.

**`SEQUENCE`** – Spring calls a database sequence object (a DB-managed counter) to get the next ID before inserting. Supported by PostgreSQL and Oracle. More efficient because IDs can be pre-fetched in batches.

**`AUTO`** – JPA decides which strategy to use based on the database dialect. May pick SEQUENCE or IDENTITY depending on the DB.

**`TABLE`** – Uses a separate table in the DB to maintain a counter. Works with any DB but is the slowest (requires extra query per insert). Rarely used today.

### Relationships – Fully Explained

**`@OneToOne`** – One record in table A maps to exactly one record in table B.
Example: One `User` has one `UserProfile`.
```java
@OneToOne(cascade = CascadeType.ALL)
@JoinColumn(name = "profile_id")  // FK column in users table
private UserProfile profile;
```

**`@OneToMany`** – One parent record maps to many child records.
Example: One `User` has many `Orders`.
```java
@OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
private List<Order> orders;
```

**`@ManyToOne`** – Many child records point to one parent record.
Example: Many `Orders` belong to one `User`.
```java
@ManyToOne
@JoinColumn(name = "user_id")  // FK column in orders table
private User user;
```

**`@ManyToMany`** – Multiple records on both sides relate to each other.
Example: A `Student` can enroll in many `Courses`, and a `Course` can have many `Students`.
```java
@ManyToMany
@JoinTable(name = "student_course",
    joinColumns = @JoinColumn(name = "student_id"),
    inverseJoinColumns = @JoinColumn(name = "course_id"))
private Set<Course> courses;
```

### Fetch Types – Explained

**`FetchType.LAZY`** (default for collections: `@OneToMany`, `@ManyToMany`)
The related data is **NOT** loaded from DB when the parent entity is fetched. It is loaded only when you actually access the field in your code (e.g., `user.getOrders()`). This is efficient — you only pay for what you use.

**`FetchType.EAGER`** (default for single-valued: `@ManyToOne`, `@OneToOne`)
The related data **IS** loaded immediately when the parent is fetched — in the same query or an additional query. Use carefully; loading large collections eagerly can cause performance issues.

```java
@OneToMany(fetch = FetchType.LAZY)    // Load orders only when accessed
private List<Order> orders;

@ManyToOne(fetch = FetchType.EAGER)   // Load user immediately with each order
private User user;
```

> **Interview tip:** "Lazy is the preferred default. Only use EAGER when you always need the associated data and the collection is small."

### Cascade Types – Every Type Explained

Cascade defines: "When I perform an operation on the parent entity, automatically apply the same operation to the child entities."

**`CascadeType.PERSIST`**
When you call `save()` or `persist()` on the parent, Spring also saves any new child entities automatically. Without this, you'd have to save each child separately before linking it to the parent.

```java
// Without PERSIST: you must save address separately first
// With PERSIST: saving user automatically saves the address
user.setAddress(new Address("123 Main St"));
userRepo.save(user); // Also inserts the Address row
```

**`CascadeType.MERGE`**
When you call `merge()` or `save()` on a detached parent entity, Spring also merges any changes made to child entities. Updates to children are propagated to the DB automatically.

**`CascadeType.REMOVE`**
When you delete the parent entity, Spring also deletes all its child entities automatically. Use carefully — this is a hard delete of all related records.

```java
// With CascadeType.REMOVE: deleting user also deletes all their orders
userRepo.delete(user);
```

**`CascadeType.REFRESH`**
When you call `refresh()` on the parent (discarding in-memory changes and reloading from DB), Spring also refreshes all child entities from the DB.

**`CascadeType.DETACH`**
When you detach the parent from the persistence context (making it unmanaged so Hibernate stops tracking it), Spring also detaches all child entities.

**`CascadeType.ALL`**
A shortcut that includes all five types: PERSIST + MERGE + REMOVE + REFRESH + DETACH. Use when the child entity's entire lifecycle is controlled by the parent and the child has no independent existence.

```java
// Example: User owns Orders. Orders cannot exist without a User.
@OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
private List<Order> orders;
```

> **Interview tip:** "I use `CascadeType.ALL` when the child entity is fully owned by the parent — for example, order line items. If an order is deleted, all its line items should be deleted too."

### Orphan Removal
`orphanRemoval = true` means: if a child entity is removed from the parent's Java collection, it should also be automatically deleted from the database.

```java
user.getOrders().remove(order);
// With orphanRemoval=true → DELETE FROM orders WHERE id = ?
// Without it → nothing happens in DB, the row remains
```

The difference between `CascadeType.REMOVE` and `orphanRemoval`:
- `CascadeType.REMOVE` triggers when the parent is deleted
- `orphanRemoval` triggers when the child is removed from the collection

### N+1 Problem – Explained
When you have a lazy `@OneToMany` and you fetch a list of 10 users, then loop over each to get their orders:
- **1 query** to get all users
- **10 more queries** — one per user to get their orders = **11 total queries**

This is the N+1 problem. It gets exponentially worse as data grows.

**Solutions:**
```java
// Solution 1: JOIN FETCH in JPQL — loads everything in one query
@Query("SELECT u FROM User u JOIN FETCH u.orders")
List<User> findAllWithOrders();

// Solution 2: @EntityGraph — declare what to fetch eagerly for this query
@EntityGraph(attributePaths = {"orders"})
List<User> findAll();

// Solution 3: @BatchSize — fetches children in batches instead of one-by-one
@OneToMany(mappedBy = "user")
@BatchSize(size = 10)
private List<Order> orders;
```

### Spring Data JPA Repositories

| Interface | What you get |
|---|---|
| `CrudRepository` | `save()`, `findById()`, `findAll()`, `delete()` |
| `PagingAndSortingRepository` | Everything above + `findAll(Pageable)`, `findAll(Sort)` |
| `JpaRepository` | Everything above + `flush()`, `saveAndFlush()`, `deleteInBatch()` |

In practice, extend `JpaRepository` — it gives you everything.

### Custom Queries
```java
// Derived method — Spring generates SQL from method name
List<User> findByEmailAndStatus(String email, String status);

// JPQL — uses entity/field names (not table/column names)
@Query("SELECT u FROM User u WHERE u.email = :email AND u.active = true")
User findActiveByEmail(@Param("email") String email);

// Native SQL — raw database SQL
@Query(value = "SELECT * FROM users WHERE email = :email", nativeQuery = true)
User findByEmailNative(@Param("email") String email);
```

### @Transactional – Explained
Marks a method as transactional. Spring wraps it in a DB transaction: if the method completes normally → commits. If an unchecked exception is thrown → rolls back automatically.

```java
@Transactional                                         // Rollback on RuntimeException
@Transactional(rollbackFor = Exception.class)          // Also rollback on checked exceptions
@Transactional(noRollbackFor = IllegalArgumentException.class) // Don't rollback for this
@Transactional(readOnly = true)                        // Optimization hint for read-only queries
@Transactional(propagation = Propagation.REQUIRES_NEW) // Always start a fresh transaction
```

**How it works internally:** Spring creates a proxy around your bean. When the annotated method is called, the proxy begins a DB transaction, calls your real method, then commits or rolls back based on the outcome.

### Transaction Propagation Types – Explained

**`REQUIRED` (default)**
If there's already an active transaction, join it. If not, create a new one. This is the standard behavior for most methods.

**`REQUIRES_NEW`**
Always create a brand-new transaction, regardless of whether one already exists. If an existing transaction is running, it is *suspended* until this one completes. Use when you need a method to commit independently (e.g., logging an audit record even if the main transaction rolls back).

**`SUPPORTS`**
If there's an active transaction, join it. If not, run without a transaction. Use for read operations that work fine either way.

**`NOT_SUPPORTED`**
Always run without a transaction. If one exists, suspend it. Use for operations that must not run in a transaction.

**`MANDATORY`**
Must run within an existing transaction. Throws an exception if called without one. Use to enforce that a method is only called from a transactional context.

**`NEVER`**
Must NOT run within a transaction. Throws an exception if one exists. Use for operations that are explicitly non-transactional.

### Optimistic vs Pessimistic Locking

**Optimistic Locking** – Assumes conflicts are rare. Doesn't lock the DB row. Adds a `@Version` field (an integer counter). When updating, JPA checks if the version number still matches. If another transaction changed it first, it throws `OptimisticLockException`. Good for read-heavy apps with low conflict.
```java
@Version
private int version; // JPA auto-increments this on every update
```

**Pessimistic Locking** – Assumes conflicts are frequent. Locks the DB row for the entire transaction duration — no other transaction can modify it. Prevents conflicts but reduces concurrency. Good for write-heavy scenarios (e.g., inventory reservation).

### Dirty Checking
When an entity is in the "managed" state (inside an active `@Transactional` method), Hibernate automatically tracks every change you make to its fields. At the end of the transaction, Hibernate compares current state with the loaded state and generates `UPDATE` statements for only the changed fields. You never need to call `save()` on a managed entity.

```java
@Transactional
public void updateUserName(Long id, String newName) {
    User user = repo.findById(id).get(); // user is now "managed"
    user.setName(newName);               // Hibernate detects this change
    // No save() call needed — UPDATE fires automatically on commit
}
```

### save() vs saveAndFlush()
- **`save()`** – Stages the entity for saving. Hibernate may batch the SQL and not write to DB until the transaction commits (or an explicit flush).
- **`saveAndFlush()`** – Forces immediate writing to DB. Use when another query in the same transaction needs to see the saved data right away.

### DTO vs Entity

| | Entity | DTO (Data Transfer Object) |
|---|---|---|
| Purpose | Maps to DB table | Transfers data to/from API |
| Exposed externally | Never | Used in request/response |
| Contains | All DB fields | Only what the client needs |
| Security | May have sensitive fields | Control exactly what's exposed |

### Embeddable & MappedSuperclass

**`@Embeddable`** – A class whose fields are embedded directly into the parent entity's DB table (no separate table created). Used for reusable value objects like `Address`.
```java
@Embeddable
public class Address {
    private String street;
    private String city;
}

@Entity
public class User {
    @Embedded
    private Address address; // street, city stored in users table
}
```

**`@MappedSuperclass`** – A base class with common fields (like `id`, `createdAt`, `updatedAt`) that subclasses inherit. It is **NOT** mapped to its own DB table — the fields appear in each subclass's table.
```java
@MappedSuperclass
public abstract class BaseEntity {
    @Id @GeneratedValue
    private Long id;
    @CreatedDate
    private LocalDateTime createdAt;
}

@Entity
public class User extends BaseEntity { ... } // users table has id, created_at + user fields
```

### Inheritance Strategies

**`SINGLE_TABLE`** – All classes in the hierarchy go into one table. A discriminator column (`dtype`) tells which type each row represents. Fastest queries (no joins) but has nullable columns for subclass-specific fields.

**`TABLE_PER_CLASS`** – Each concrete class gets its own table with all fields (including inherited ones). No joins needed to fetch a single type, but data duplication and `UNION` queries needed to find all records of the parent type.

**`JOINED`** – Parent class has one table, each subclass has its own table with only the extra fields. A `JOIN` is needed to assemble the full object. Most normalized but slower due to joins.

### Soft Delete
Instead of physically deleting the DB row, you mark it as deleted with a flag. Historical data is preserved for auditing.
```java
@SQLDelete(sql = "UPDATE users SET deleted = true WHERE id = ?")
@Where(clause = "deleted = false")  // All queries automatically filter deleted rows
@Entity
public class User {
    private boolean deleted = false;
}
```

### Auditing
Automatically track when records are created/modified and by whom:
```java
@EntityListeners(AuditingEntityListener.class)
@MappedSuperclass
public class Auditable {
    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @CreatedBy
    private String createdBy;

    @LastModifiedBy
    private String modifiedBy;
}
// Must also add @EnableJpaAuditing to a @Configuration class
```

### Database Migrations (Flyway)
Flyway tracks and applies SQL migration scripts in version order. Every script runs exactly once and is recorded in a `flyway_schema_history` table. If the DB already has the schema at a certain version, Flyway only runs newer scripts.

```sql
-- src/main/resources/db/migration/V1__create_users.sql
CREATE TABLE users (id BIGINT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(100) NOT NULL);

-- V2__add_name_column.sql
ALTER TABLE users ADD COLUMN name VARCHAR(100);
```
Spring Boot runs migrations automatically on startup.

---

## 7. Spring Boot Security

### What is Spring Security?
Spring Security is a framework that handles authentication (who are you?) and authorization (what can you do?) for Spring applications. It works by inserting a chain of security filters in front of every HTTP request.

### Security Filter Chain
Every request passes through a series of filters. Each filter checks something — is the user authenticated? Do they have the right role? Is the CSRF token valid? You configure the chain by defining a `SecurityFilterChain` bean.

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
        .build();
}
```

### JWT Authentication – How It Works
1. User sends `POST /login` with username and password
2. Server validates credentials and generates a signed JWT token
3. Client receives the JWT and stores it (in memory or localStorage)
4. On every subsequent request, client sends: `Authorization: Bearer <token>`
5. A custom JWT filter intercepts the request and validates the token
6. If valid, sets the user in Spring Security context → request proceeds
7. If invalid/expired → returns 401 Unauthorized

### JWT vs Session-Based Authentication

| | Session-Based | JWT |
|---|---|---|
| Server state | Stateful (stores session in memory/DB) | Stateless (no server storage) |
| Scalability | Harder — servers must share session store | Easy — any server can validate the token |
| Client storage | Session cookie | Token in Authorization header |
| Expiry | Server-controlled | Encoded in the token |

### BCryptPasswordEncoder
BCrypt is a strong one-way hashing algorithm designed specifically for passwords. It automatically adds a random *salt* to each password (preventing rainbow table attacks) and applies multiple rounds of hashing (making brute-force attacks slow).

```java
@Bean
PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(); // Default: 10 hashing rounds
}

String hashed = passwordEncoder.encode("myPassword"); // One-way hash
boolean matches = passwordEncoder.matches("myPassword", hashed); // Verify
// Note: You never decode — you only compare
```

### Role-Based Access Control
```java
.requestMatchers("/admin/**").hasRole("ADMIN")          // Must have ADMIN role
.requestMatchers("/user/**").hasAnyRole("USER","ADMIN") // Either role works
.requestMatchers("/api/**").hasAuthority("READ_DATA")   // Specific permission
```

### @PreAuthorize vs @PostAuthorize
- **`@PreAuthorize`** – Runs the security check BEFORE the method executes. If the user doesn't have the right role/permission, the method is never called. Most commonly used.
- **`@PostAuthorize`** – Runs the check AFTER the method executes, using the return value in the expression. Used to ensure users can only see their own data.

```java
@PreAuthorize("hasRole('ADMIN')")
public List<User> getAllUsers() { ... }  // Only admins can call this

@PostAuthorize("returnObject.username == principal.username")
public User getUser(Long id) { ... }  // Runs, but result only returned if it's the caller's own data
```

### CSRF (Cross-Site Request Forgery)
An attack where a malicious website tricks a logged-in user's browser into making a request to your server — using the user's cookies. Spring Security enables CSRF protection by default for form-based apps by requiring a hidden CSRF token in every state-changing request.

For stateless REST APIs using JWT (no cookies), CSRF is not a concern, so you disable it:
```java
http.csrf(csrf -> csrf.disable());
```

### OAuth2
An authorization framework that allows a user to grant a third-party application limited access to their data on another service — without sharing their password. Example: "Sign in with Google" — you authorize the app to see your Google profile, but you never give your Google password to the app.

---

## 8. Microservices & Spring Cloud

### What are Microservices?
An architectural approach where a large application is split into many small, independent services — each responsible for a single business capability. Each service has its own codebase, database, and deployment pipeline. They communicate via HTTP (REST/gRPC) or messaging (Kafka/RabbitMQ).

### Monolithic vs Microservices

| | Monolithic | Microservices |
|---|---|---|
| Codebase | Single large app | Many small services |
| Deployment | Entire app for any change | Only the changed service |
| Scaling | Must scale entire app | Scale individual services |
| Failure impact | One bug can crash everything | Failures are isolated |
| Complexity | Simpler initially | Needs more infrastructure |

### Service Discovery (Eureka)
In microservices, services are deployed dynamically — their IP addresses and ports change. Service discovery solves this: each service registers itself with a central registry (Eureka Server). Other services ask the registry "where is the user-service?" instead of hardcoding the address.

```yaml
# Client registers with:
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka
```

### API Gateway
A single entry point that sits in front of all your microservices. It handles routing, authentication (validates JWT before forwarding), rate limiting, load balancing, SSL termination, and cross-cutting concerns — so individual services don't have to.

### Zuul vs Spring Cloud Gateway

| | Zuul (legacy) | Spring Cloud Gateway |
|---|---|---|
| I/O model | Blocking (thread-per-request) | Non-blocking (reactive) |
| Performance | Lower under high load | Higher, handles more connections |
| Status | Netflix maintenance mode | Actively developed |

### Feign Client
A declarative HTTP client — you define an interface with annotations and Spring generates the implementation at runtime. Makes inter-service calls look like local method calls.

```java
@FeignClient(name = "user-service")  // Looks up "user-service" in Eureka
public interface UserServiceClient {
    @GetMapping("/users/{id}")
    User getUserById(@PathVariable Long id);
}

// Usage in another service:
User user = userClient.getUserById(1L);  // Spring handles the HTTP call
```

### Circuit Breaker Pattern (Resilience4j)
When a service is failing or slow, repeatedly calling it wastes resources and can cause cascading failures. The Circuit Breaker prevents this by "opening" after a threshold of failures, immediately returning a fallback response.

**States:**
- **CLOSED** – Normal operation. All calls go through.
- **OPEN** – Failure threshold reached. All calls immediately return fallback without calling the service.
- **HALF-OPEN** – After a wait, allows one test call. Success → CLOSED. Failure → OPEN again.

```java
@CircuitBreaker(name = "userService", fallbackMethod = "fallbackUser")
public User getUser(Long id) {
    return userServiceClient.getUserById(id);
}

public User fallbackUser(Long id, Exception ex) {
    return new User(id, "Default User");
}
```

### Resilience4j Additional Patterns
- **Retry** – Automatically retry a failed call N times with a backoff delay
- **RateLimiter** – Limit how many calls can be made in a time period
- **Bulkhead** – Limit concurrent calls to prevent one service from exhausting all threads
- **TimeLimiter** – Cancel calls that take longer than a configured timeout

### Distributed Tracing (Sleuth + Zipkin)
In microservices, a single user request may flow through 5+ services. If something fails, you need to trace the full journey. Each request gets a unique `traceId`, and each service hop gets a `spanId`.

- **Spring Cloud Sleuth** – Automatically adds `traceId` and `spanId` to all log messages
- **Zipkin** – Collects trace data and provides a UI to visualize the full request path, timing per service, and where failures occurred

### Config Server
Centralizes all microservice configurations in one place (usually a Git repo). Instead of each service having its own `application.properties`, they all fetch config from the Config Server at startup. You can update config in Git and trigger a refresh without redeploying.

### Saga Pattern
Handles distributed transactions across multiple microservices. Since each service has its own DB, a single DB transaction isn't possible. Saga chains local transactions: each step publishes an event; if a step fails, compensating transactions undo previous steps.

**Example:** Place order → (1) Reserve inventory → (2) Charge payment → (3) Confirm shipment. If payment fails, compensate step 1 by releasing the reservation.

### CQRS (Command Query Responsibility Segregation)
Separate the model used for writing (commands: create/update/delete) from the model used for reading (queries). This allows you to optimize each side independently — for example, a normalized relational DB for writes and a denormalized cache or read-replica for fast reads.

### Kafka – Key Concepts
- **Topic** – Named channel where messages are published (like a table in DB)
- **Producer** – Sends messages to a topic
- **Consumer** – Reads messages from a topic
- **Consumer Group** – Multiple consumers share the work; each message goes to one consumer in the group
- **Partition** – A topic is split into partitions for parallel processing; messages within a partition are ordered
- **Offset** – Position of a message in a partition; consumers track this to know what they've read

### Kafka vs RabbitMQ

| | Kafka | RabbitMQ |
|---|---|---|
| Model | Append-only event log (messages persist after read) | Message queue (messages deleted after consumed) |
| Throughput | Millions of messages/sec | Thousands |
| Message ordering | Guaranteed per partition | Not guaranteed |
| Best for | Event sourcing, audit logs, stream processing | Task queues, RPC, complex routing |

---

## 9. Caching, Async & Scheduling

### Why Cache?
Every DB call has latency. If the same data is requested frequently and doesn't change often (user profile, product catalog), caching stores the result in fast memory so subsequent requests don't hit the DB at all.

### Spring Cache Annotations

**`@Cacheable(value = "users", key = "#id")`**
First call: runs the method, stores result in cache under the key. Subsequent calls with the same key: returns cached result without running the method. Ideal for expensive read operations.

**`@CachePut(value = "users", key = "#user.id")`**
Always runs the method AND updates the cache with the result. Use this after an update operation to keep the cache in sync. Unlike `@Cacheable`, it never skips the method.

**`@CacheEvict(value = "users", key = "#id")`**
Removes a specific entry from the cache. Use after a delete operation to prevent stale data. You can also use `allEntries = true` to clear the entire cache.

```java
@Cacheable(value = "users", key = "#id")
public User getUserById(Long id) { return repo.findById(id).get(); }

@CachePut(value = "users", key = "#user.id")
public User updateUser(User user) { return repo.save(user); }

@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) { repo.deleteById(id); }
```

### In-memory vs Distributed Cache

| | In-memory (Caffeine) | Distributed (Redis) |
|---|---|---|
| Scope | Single JVM instance only | All instances in cluster |
| Speed | Fastest (local memory, no network) | Fast (small network roundtrip) |
| Persistence | Lost on app restart | Survives restarts |
| Use case | Single-node apps | Microservices, clustered apps |

### @Async – How It Works
Without `@Async`: the caller thread runs the method and waits for it to finish before moving on.
With `@Async`: Spring hands the work to a thread pool. The caller gets back immediately, and the method runs in the background.

```java
@Async
public CompletableFuture<String> sendEmail(String to) {
    emailClient.send(to); // runs in background thread
    return CompletableFuture.completedFuture("Sent");
}
```

> **Important:** `@Async` uses Spring's proxy mechanism. If you call an `@Async` method from *within the same class*, it bypasses the proxy and runs synchronously. Always call from a different bean.

### @Scheduled – Options Explained

```java
@Scheduled(fixedRate = 5000)
// Runs every 5 seconds measured from START of previous execution.
// If the task takes 3s, next run starts 2s after it finishes.

@Scheduled(fixedDelay = 5000)
// Waits 5 seconds after END of previous execution before running again.
// Guarantees a minimum gap between executions.

@Scheduled(cron = "0 30 9 * * MON-FRI")
// Cron syntax: second(0) minute(30) hour(9) day(*) month(*) weekday(MON-FRI)
// Runs at 9:30 AM every weekday.
```

---

## 10. Logging

### What is SLF4J?
SLF4J (Simple Logging Facade for Java) is an abstraction/API for logging. Your code calls SLF4J methods, and at runtime a real logging framework (Logback, Log4j2) does the actual work. This means you can switch logging implementations without changing any application code — just swap the dependency.

### Logback
The default logging implementation in Spring Boot. Configured via `application.properties` or `logback-spring.xml`.

```java
private static final Logger log = LoggerFactory.getLogger(UserService.class);

log.trace("Most detailed — every tiny step");
log.debug("Variable values, method entry/exit");
log.info("Normal flow: user logged in, order placed");
log.warn("Unexpected but recoverable: retry attempt");
log.error("Something failed: DB connection lost", exception);
```

### Log Levels – When to Use Each

| Level | When to use |
|---|---|
| `TRACE` | Every tiny step in a loop or process. Only for deep debugging. Never in production. |
| `DEBUG` | Variable values, which branch was taken. Useful during development. Turn off in prod. |
| `INFO` | Significant normal events: app started, user logged in, order processed. Always on in prod. |
| `WARN` | Something unexpected but the app continues: deprecated API called, retry attempt, near capacity. |
| `ERROR` | A failure occurred that needs attention: DB down, API failed, exception caught. Always on in prod. |

Setting `logging.level.root=INFO` means INFO, WARN, and ERROR are shown; DEBUG and TRACE are suppressed.

### MDC (Mapped Diagnostic Context)
MDC lets you attach contextual data (like a request ID or user ID) to the current thread. Every log line printed in that thread automatically includes this data. Essential in microservices to trace all logs belonging to a single request.

```java
// In a servlet filter:
MDC.put("requestId", UUID.randomUUID().toString());
MDC.put("userId", currentUser.getId().toString());

log.info("Processing order");
// Output: 2024-01-01 [req-abc123] [user-42] Processing order

MDC.clear(); // Always clear at the end of the request thread
```

### ELK Stack – Centralized Logging
When you have 20 microservices each writing to their own log files, debugging is impossible. ELK aggregates everything:

- **Logstash** – Collects logs from all services (via file watchers, TCP, or Filebeat) and transforms/normalizes them
- **Elasticsearch** – Stores and indexes all log entries with extremely fast full-text search
- **Kibana** – Web dashboard to search, filter, and visualize logs across all services in one place

---

## 11. Testing

### Why Different Test Annotations?
Loading the full Spring context (`@SpringBootTest`) for every test is slow. Spring provides *test slice* annotations that load only the parts of the context needed for that test type.

### Test Annotations Explained

**`@SpringBootTest`**
Loads the complete application context — all beans, configs, DB connections, security. Use for full end-to-end integration tests. Slowest but most realistic. Good for testing the whole flow.

**`@WebMvcTest(UserController.class)`**
Loads only the web layer: controllers, filters, `@ControllerAdvice`, `MockMvc`. No service or repository beans are loaded. You mock the service layer with `@MockBean`. Fast. Use for testing URL mapping, request/response format, validation, HTTP status codes.

**`@DataJpaTest`**
Loads only JPA-related beans: repositories, entity classes, and an in-memory H2 database. No web layer or service beans. Each test rolls back automatically. Use for testing repository queries, derived methods, and custom `@Query`.

**`@MockBean`**
Creates a Mockito mock and registers it as a Spring bean in the test context. Any existing bean of that type is replaced by the mock. Used in `@WebMvcTest` to mock the service that the controller depends on.

**`@ActiveProfiles("test")`**
Activates the "test" Spring profile, so `application-test.properties` or `application-test.yml` is loaded. Use to point tests at an in-memory DB or test-specific configuration.

### Example: Controller Test
```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void getUser_shouldReturn200() throws Exception {
        when(userService.findUser(1L)).thenReturn(new User(1L, "Alice", "alice@test.com"));

        mockMvc.perform(get("/api/users/1"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.name").value("Alice"));
    }

    @Test
    void createUser_withInvalidEmail_shouldReturn400() throws Exception {
        String body = "{\"name\":\"Bob\", \"email\":\"not-an-email\"}";

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON).content(body))
               .andExpect(status().isBadRequest());
    }
}
```

### Example: Repository Test
```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository repo;

    @Test
    void findByEmail_shouldReturnUser() {
        repo.save(new User("Alice", "alice@test.com"));

        Optional<User> found = repo.findByEmail("alice@test.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alice");
    }
}
```

---

## 12. Advanced & Real-World Scenarios

### AOP (Aspect-Oriented Programming)
AOP lets you add cross-cutting concerns (logging, security, transaction management) to methods without modifying their code. Spring wraps your bean in a **proxy** at startup. When you call a `@Transactional` method, you're actually calling the proxy, which starts a transaction → calls your real method → commits or rolls back.

**Key terms:**
- **Aspect** – The cross-cutting concern module (e.g., transaction management, logging)
- **Advice** – The code that runs (e.g., begin transaction, log request)
- **Pointcut** – Expression specifying which methods to intercept (e.g., all methods in service layer)
- **JoinPoint** – The specific method execution being intercepted

### Performance Tuning Checklist
- Add DB **indexes** on columns used in `WHERE`, `JOIN`, `ORDER BY`
- Fix **N+1 queries** with JOIN FETCH or `@EntityGraph`
- Tune **HikariCP** pool size for your load
- Use `@Cacheable` for repeated **read-only** data
- Use **DTO projections** instead of loading full entities for read APIs
- Use `@Async` for **non-critical background tasks** (email, notifications)
- Always use **pagination** — never `findAll()` on large tables
- Use `@Transactional(readOnly = true)` for query methods — Hibernate skips dirty checking

### Common Pitfalls

| Pitfall | Fix |
|---|---|
| N+1 query problem | Use JOIN FETCH or @EntityGraph |
| `@SpringBootTest` in every unit test | Use `@WebMvcTest` or `@DataJpaTest` |
| Field injection everywhere | Use constructor injection |
| Hardcoded passwords/secrets | Use env vars or Vault |
| No global exception handling | Use `@RestControllerAdvice` |
| Not using profiles | Use `application-{profile}.yml` per env |
| Returning entities directly in API | Use DTOs |
| `findAll()` without pagination | Always use `Pageable` |

### Design Patterns in Spring Boot

| Pattern | Where Spring uses it |
|---|---|
| **Singleton** | Every `@Component`, `@Service`, `@Repository` bean |
| **Factory** | `@Bean` methods in `@Configuration`, `FactoryBean` |
| **Proxy** | AOP — `@Transactional`, `@Cacheable`, `@Async` |
| **Observer** | `ApplicationEventPublisher` + `@EventListener` |
| **Template Method** | `JdbcTemplate`, `RestTemplate`, `KafkaTemplate` |
| **Strategy** | `PasswordEncoder` (BCrypt, SCrypt), `AuthenticationProvider` |

### Docker Deployment
```dockerfile
FROM openjdk:17-slim
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```
```bash
docker build -t myapp:1.0 .
docker run -p 8080:8080 -e SPRING_PROFILES_ACTIVE=prod myapp:1.0
```

### HikariCP – Connection Pool
HikariCP is the default and fastest JDBC connection pool in Spring Boot. Instead of creating a new DB connection for every request (expensive — involves network handshake, auth), it maintains a pool of reusable connections. Requests borrow a connection, use it, and return it to the pool.

```properties
spring.datasource.hikari.maximum-pool-size=20     # Max connections in pool
spring.datasource.hikari.minimum-idle=5           # Keep at least 5 connections ready
spring.datasource.hikari.connection-timeout=30000 # Wait up to 30s for a connection
```

### Managing Secrets
Never put passwords or API keys in code or in `application.properties` committed to Git.

- **Environment variables** – Set in OS, Docker, or Kubernetes
- **Spring Cloud Vault** – Fetches secrets from HashiCorp Vault at startup
- **AWS Secrets Manager** – For AWS deployments
- **Kubernetes Secrets** – Injected as environment variables into pods

---

## 🎯 Quick-Fire One-Liners (Last-Minute Revision)

| Concept | Interview Answer |
|---|---|
| **IoC** | Spring manages object creation; you give up control to the container |
| **DI** | Spring automatically injects dependencies into your class |
| **`@SpringBootApplication`** | `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan` |
| **Auto-configuration** | Spring reads classpath and uses conditions to set up beans automatically |
| **`@RestController`** | `@Controller` + `@ResponseBody` — returns JSON/XML, not views |
| **Singleton scope** | One shared instance per Spring container |
| **Prototype scope** | New instance every time the bean is requested |
| **Request scope** | One instance per HTTP request |
| **Session scope** | One instance per user HTTP session |
| **`@PostConstruct`** | Runs initialization logic after bean creation and injection |
| **`@PreDestroy`** | Runs cleanup logic before bean is destroyed |
| **`@Transactional`** | Wraps method in DB transaction; auto commits or rolls back |
| **Propagation REQUIRED** | Join existing transaction or create new one (default) |
| **Propagation REQUIRES_NEW** | Always start fresh transaction, suspend existing |
| **Dirty checking** | Hibernate auto-detects managed entity changes, generates UPDATE automatically |
| **N+1 problem** | 1 parent query + N child queries; fix with JOIN FETCH |
| **`CascadeType.PERSIST`** | Saving parent also saves new child entities |
| **`CascadeType.MERGE`** | Updating parent also updates child entities |
| **`CascadeType.REMOVE`** | Deleting parent also deletes child entities |
| **`CascadeType.ALL`** | All cascade operations; use when child lifecycle is owned by parent |
| **`orphanRemoval=true`** | Child removed from collection → automatically deleted from DB |
| **LAZY fetch** | Related data loaded only when accessed in code |
| **EAGER fetch** | Related data loaded immediately with the parent |
| **Optimistic locking** | `@Version` field detects concurrent update conflicts |
| **Pessimistic locking** | Locks DB row for entire transaction duration |
| **`save()` vs `saveAndFlush()`** | save() may defer DB write; saveAndFlush() writes immediately |
| **`persist()` vs `merge()`** | persist() inserts new; merge() updates existing/detached |
| **JWT** | Stateless signed token; server stores nothing |
| **CSRF** | Attack using cookies; disable for stateless JWT REST APIs |
| **BCrypt** | One-way password hashing with salt; cannot be decoded |
| **OAuth2** | Delegated authorization (Sign in with Google) |
| **`@PreAuthorize`** | Checks role/permission before method runs |
| **`@PostAuthorize`** | Checks return value after method runs |
| **Circuit breaker** | Opens after failures, returns fallback; prevents cascading failures |
| **Service discovery** | Services register with Eureka; others look them up by name |
| **Feign Client** | Declarative HTTP client; define interface, Spring handles calls |
| **Kafka** | Distributed event log; high throughput; ordered per partition |
| **`@Cacheable`** | Returns cached result if available; calls method only on cache miss |
| **`@CachePut`** | Always runs method AND updates cache |
| **`@CacheEvict`** | Removes entry from cache |
| **`@Async`** | Runs method in background thread; caller doesn't wait |
| **`@Scheduled(fixedRate)`** | Runs every N ms from start of last execution |
| **`@Scheduled(fixedDelay)`** | Waits N ms after last execution ends, then runs |
| **Actuator** | Exposes health, metrics, env, and management endpoints |
| **Micrometer** | Metrics facade; exports to Prometheus, Grafana, Datadog |
| **MDC** | Attaches requestId/userId to all log lines in a thread |
| **ELK Stack** | Elasticsearch + Logstash + Kibana; centralized log aggregation |
| **HikariCP** | Default connection pool; reuses DB connections for performance |
| **Saga pattern** | Distributed transaction via local transactions + compensations |
| **CQRS** | Separate read and write models for independent optimization |
| **`@WebMvcTest`** | Tests controller layer only; fast; mock services |
| **`@DataJpaTest`** | Tests repository layer with in-memory DB; auto rollback |
| **`@MockBean`** | Creates Mockito mock and registers it as Spring bean in test |

---

*Good luck with your interview! 🚀*