# 🚀 Spring Boot – Missing Topics (Interview Supplement)
> These topics were absent or thin in the original notes. Study both files together.

---

## 📌 Table of Contents
1. [Filter vs Interceptor vs AOP](#1-filter-vs-interceptor-vs-aop)
2. [Custom UserDetailsService & Security Internals](#2-custom-userdetailsservice--security-internals)
3. [JWT Refresh Token Flow](#3-jwt-refresh-token-flow)
4. [CORS Configuration (Detailed)](#4-cors-configuration-detailed)
5. [Spring Events (Publish / Listen)](#5-spring-events-publish--listen)
6. [JPA Projections](#6-jpa-projections)
7. [JPA Specifications (Dynamic Queries)](#7-jpa-specifications-dynamic-queries)
8. [Testcontainers](#8-testcontainers)
9. [WireMock](#9-wiremock)
10. [Security Testing (@WithMockUser)](#10-security-testing-withmockuser)
11. [Spring Cloud Contract](#11-spring-cloud-contract)
12. [Graceful Shutdown](#12-graceful-shutdown)
13. [Virtual Threads (Java 21 + Spring Boot 3.2)](#13-virtual-threads-java-21--spring-boot-32)
14. [GraalVM Native Image](#14-graalvm-native-image)
15. [Externalized Config & Property Source Order](#15-externalized-config--property-source-order)
16. [Spring Batch](#16-spring-batch)
17. [Outbox Pattern](#17-outbox-pattern)
18. [Distributed Locking](#18-distributed-locking)
19. [Multipart File Upload & Download](#19-multipart-file-upload--download)
20. [@DependsOn, @Import, Spring Environment](#20-dependson-import-spring-environment)
21. [Liquibase vs Flyway](#21-liquibase-vs-flyway)
22. [OAuth2 Resource Server (JWT)](#22-oauth2-resource-server-jwt)
23. [Quick-Fire One-Liners (Supplement)](#-quick-fire-one-liners-supplement)

---

## 1. Filter vs Interceptor vs AOP

This is one of the most common interview questions. You must know **where** each operates and **when** to use each.

### The Request Pipeline

```
HTTP Request
    ↓
[ Servlet Filters ]         ← Servlet level (before Spring)
    ↓
[ DispatcherServlet ]       ← Spring MVC entry point
    ↓
[ HandlerInterceptors ]     ← Spring MVC level (before/after controller)
    ↓
[ Controller Method ]
    ↓
[ AOP Advice ]              ← Bean method level (wraps any Spring bean)
    ↓
[ Service / Repository ]
```

### Servlet Filter
- Lives **outside** Spring's context — at the raw Servlet/HTTP level.
- Intercepts **every** request/response passing through the servlet container.
- Has access to `HttpServletRequest` and `HttpServletResponse`.
- Can modify the request/response body, headers, or block the request entirely.
- Use for: **JWT authentication**, logging request/response, GZIP compression, rate limiting.

```java
@Component
public class RequestLoggingFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest request = (HttpServletRequest) req;
        System.out.println("Incoming: " + request.getMethod() + " " + request.getRequestURI());

        chain.doFilter(req, res); // pass to next filter or servlet

        System.out.println("Response sent");
    }
}
```

To control filter order:
```java
@Bean
public FilterRegistrationBean<RequestLoggingFilter> loggingFilter() {
    FilterRegistrationBean<RequestLoggingFilter> bean = new FilterRegistrationBean<>();
    bean.setFilter(new RequestLoggingFilter());
    bean.setOrder(1); // lower = runs first
    return bean;
}
```

### HandlerInterceptor
- Lives **inside** Spring MVC — runs after `DispatcherServlet` selects the handler (controller).
- Has access to the handler method object and `ModelAndView`.
- Three hook methods: `preHandle`, `postHandle`, `afterCompletion`.
- Use for: **auth checks, role checking, logging, setting request-scoped attributes, audit trails**.

```java
@Component
public class AuditInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        // return false to abort request; true to continue
        System.out.println("Before controller: " + req.getRequestURI());
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest req, HttpServletResponse res,
                           Object handler, ModelAndView modelAndView) {
        // Runs after controller but before view rendering
        System.out.println("After controller");
    }

    @Override
    public void afterCompletion(HttpServletRequest req, HttpServletResponse res,
                                Object handler, Exception ex) {
        // Runs after view is rendered (or after response is committed)
        System.out.println("Request complete");
    }
}

// Register it:
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Autowired AuditInterceptor auditInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(auditInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/public/**");
    }
}
```

### AOP Advice
- Operates at the **Spring bean method level** — not HTTP-aware at all.
- Can intercept **any** Spring bean's method (service, repository, etc.), not just controllers.
- Has no access to `HttpServletRequest` by default.
- Use for: **transaction management, caching, logging method calls, performance monitoring, retry logic**.

```java
@Aspect
@Component
public class PerformanceAspect {

    @Around("execution(* com.example.service.*.*(..))")
    public Object measureTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed(); // calls the real method
        long elapsed = System.currentTimeMillis() - start;
        System.out.println(joinPoint.getSignature().getName() + " took " + elapsed + "ms");
        return result;
    }
}
```

### Comparison Table

| | Filter | Interceptor | AOP |
|---|---|---|---|
| Level | Servlet (outside Spring) | Spring MVC | Spring Bean method |
| HTTP aware | Yes | Yes | No (unless injected) |
| Applies to | All requests | Controller requests | Any bean method |
| Access to handler | No | Yes | No |
| Use case | Auth, logging, GZIP | Pre/post controller logic | Transactions, caching |
| Spring context | No (unless @Component) | Yes | Yes |

> **Interview answer:** "Filters are for raw HTTP concerns before Spring sees the request — like JWT validation. Interceptors are for controller-level concerns like checking if a user has access to a resource. AOP is for cross-cutting concerns on any Spring bean — like timing a service method."

---

## 2. Custom UserDetailsService & Security Internals

### How Spring Security Authenticates a User (Full Flow)

```
1. Request arrives with credentials (username + password, or JWT)
2. AuthenticationFilter extracts credentials
3. Creates an Authentication object (e.g. UsernamePasswordAuthenticationToken)
4. Passes it to AuthenticationManager
5. AuthenticationManager delegates to AuthenticationProvider
6. AuthenticationProvider calls UserDetailsService.loadUserByUsername()
7. You return a UserDetails object from your DB
8. Spring compares the submitted password with stored hash (BCrypt)
9. If match → creates authenticated token → stores in SecurityContextHolder
10. Request proceeds to controller
```

### Implementing Custom UserDetailsService

```java
@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        // Load user from YOUR database
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new UsernameNotFoundException("User not found: " + email));

        // Convert your User entity to Spring's UserDetails
        return org.springframework.security.core.userdetails.User
            .withUsername(user.getEmail())
            .password(user.getPassword()) // already BCrypt-hashed in DB
            .roles(user.getRole().name()) // e.g. "USER", "ADMIN"
            .accountExpired(!user.isActive())
            .build();
    }
}
```

### Custom UserDetails (if you need extra fields)

```java
public class CustomUserDetails implements UserDetails {

    private final User user; // your entity

    public CustomUserDetails(User user) { this.user = user; }

    public Long getUserId() { return user.getId(); } // extra method

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority("ROLE_" + user.getRole().name()));
    }

    @Override public String getPassword() { return user.getPassword(); }
    @Override public String getUsername() { return user.getEmail(); }
    @Override public boolean isAccountNonExpired() { return true; }
    @Override public boolean isAccountNonLocked() { return !user.isLocked(); }
    @Override public boolean isCredentialsNonExpired() { return true; }
    @Override public boolean isEnabled() { return user.isActive(); }
}
```

### Wire it into SecurityConfig

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired private CustomUserDetailsService userDetailsService;
    @Autowired private JwtAuthFilter jwtAuthFilter;

    @Bean
    public AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder());
        return provider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config)
            throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authenticationProvider(authenticationProvider())
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

### @Secured vs @PreAuthorize

| | `@Secured` | `@PreAuthorize` |
|---|---|---|
| Expression language | No (just role names) | Yes (SpEL — full expressions) |
| Example | `@Secured("ROLE_ADMIN")` | `@PreAuthorize("hasRole('ADMIN') and #id == principal.id")` |
| Flexibility | Low | High |
| Recommended | Legacy | Modern standard |

---

## 3. JWT Refresh Token Flow

### Why Refresh Tokens?
Access tokens are short-lived (15–30 min) for security. If stolen, the damage window is small. But you don't want users to log in every 15 minutes. Refresh tokens solve this — they are long-lived (7–30 days) and stored securely, used only to get a new access token.

### Complete Flow

```
1. User logs in → server returns:
   {
     "accessToken": "eyJ...",        // expires in 15 min
     "refreshToken": "abc123xyz"     // expires in 7 days
   }

2. Client stores:
   - accessToken in memory (not localStorage — XSS risk)
   - refreshToken in HttpOnly cookie (can't be read by JS)

3. Client sends accessToken in every request:
   Authorization: Bearer eyJ...

4. When accessToken expires → server returns 401

5. Client automatically calls POST /api/auth/refresh
   with the refreshToken (sent automatically via cookie)

6. Server:
   a. Validates refreshToken against DB (it's stored there)
   b. If valid → issue new accessToken (and optionally rotate refreshToken)
   c. If expired/invalid → return 401, force re-login

7. Client receives new accessToken and retries the original request
```

### Refresh Token Entity

```java
@Entity
public class RefreshToken {
    @Id @GeneratedValue
    private Long id;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;

    @Column(nullable = false, unique = true)
    private String token;

    @Column(nullable = false)
    private Instant expiryDate;

    public boolean isExpired() {
        return expiryDate.isBefore(Instant.now());
    }
}
```

### Refresh Token Service

```java
@Service
public class RefreshTokenService {

    @Value("${app.refresh-token.expiry-ms:604800000}") // 7 days
    private long expiryMs;

    @Autowired private RefreshTokenRepository repo;
    @Autowired private UserRepository userRepo;

    public RefreshToken createRefreshToken(Long userId) {
        RefreshToken token = new RefreshToken();
        token.setUser(userRepo.findById(userId).get());
        token.setToken(UUID.randomUUID().toString());
        token.setExpiryDate(Instant.now().plusMillis(expiryMs));
        return repo.save(token);
    }

    public RefreshToken verifyExpiration(RefreshToken token) {
        if (token.isExpired()) {
            repo.delete(token);
            throw new RuntimeException("Refresh token expired. Please log in again.");
        }
        return token;
    }
}
```

### Token Rotation
Best practice: every time a refresh token is used, issue a **new** refresh token and invalidate the old one. This limits the damage window if a refresh token is stolen.

---

## 4. CORS Configuration (Detailed)

### What is CORS?
Browsers block requests from one origin (e.g. `http://localhost:3000`) to another origin (e.g. `http://localhost:8080`) by default. CORS (Cross-Origin Resource Sharing) is the mechanism where the **server** tells the browser which cross-origin requests are allowed.

### Option 1: Global CORS via WebMvcConfigurer

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("https://myfrontend.com", "http://localhost:3000")
            .allowedMethods("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS")
            .allowedHeaders("*")
            .allowCredentials(true)   // required if sending cookies/auth headers
            .maxAge(3600);            // browser caches preflight for 1 hour
    }
}
```

### Option 2: CORS in Spring Security Filter Chain (Recommended when using Spring Security)

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .cors(cors -> cors.configurationSource(corsConfigurationSource()))
        // ... rest of config
        .build();
}

@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://myfrontend.com", "http://localhost:3000"));
    config.setAllowedMethods(List.of("GET","POST","PUT","DELETE","OPTIONS"));
    config.setAllowedHeaders(List.of("Authorization","Content-Type"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);

    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", config);
    return source;
}
```

> **Important:** When using Spring Security, always configure CORS through the security filter chain, not just `WebMvcConfigurer`. Security filters run before MVC filters — if you don't add it here, preflight `OPTIONS` requests get blocked before reaching your MVC config.

### Option 3: Per-controller / Per-method

```java
@CrossOrigin(origins = "http://localhost:3000", maxAge = 3600)
@RestController
@RequestMapping("/api/users")
public class UserController { ... }
```

### Preflight Request
Before making a cross-origin `POST`/`PUT`/`DELETE` with custom headers, the browser automatically sends an `OPTIONS` request to check if the server allows it. Your server must respond with the correct CORS headers. Spring handles this automatically when CORS is configured.

---

## 5. Spring Events (Publish / Listen)

### What are Spring Events?
Spring has a built-in event/listener mechanism (Observer pattern). One component publishes an event; any number of listeners react to it — without the publisher knowing who's listening. Great for decoupling.

### Publishing an Event

```java
// 1. Define your custom event
public class UserRegisteredEvent {
    private final User user;
    public UserRegisteredEvent(User user) { this.user = user; }
    public User getUser() { return user; }
}

// 2. Publish it from a service
@Service
public class UserService {

    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public User register(User user) {
        User saved = userRepository.save(user);
        eventPublisher.publishEvent(new UserRegisteredEvent(saved)); // fire and continue
        return saved;
    }
}
```

### Listening to an Event

```java
// 3. Handle it in any bean
@Component
public class EmailNotificationListener {

    @EventListener
    public void onUserRegistered(UserRegisteredEvent event) {
        emailService.sendWelcomeEmail(event.getUser().getEmail());
    }
}

@Component
public class AuditListener {

    @EventListener
    public void onUserRegistered(UserRegisteredEvent event) {
        auditService.log("New user registered: " + event.getUser().getEmail());
    }
}
```

### Async Events
By default, event listeners run synchronously in the same thread as the publisher. Add `@Async` to run them in a background thread:

```java
@Async
@EventListener
public void onUserRegistered(UserRegisteredEvent event) {
    emailService.sendWelcomeEmail(event.getUser().getEmail()); // runs in background
}
// Don't forget @EnableAsync on a @Configuration class
```

### Built-in Spring Events
| Event | When it fires |
|---|---|
| `ContextRefreshedEvent` | ApplicationContext initialized or refreshed |
| `ContextStartedEvent` | ApplicationContext started |
| `ContextStoppedEvent` | ApplicationContext stopped |
| `ContextClosedEvent` | ApplicationContext closed / app shutting down |
| `ApplicationReadyEvent` | App fully started and ready to serve requests |

```java
@EventListener(ApplicationReadyEvent.class)
public void onStartup() {
    System.out.println("Application is ready!");
}
```

---

## 6. JPA Projections

### What are Projections?
Instead of loading a full entity (all columns), projections let you fetch only the fields you need — reducing memory usage and query payload. They act as read-only, lightweight DTOs directly from the repository.

### Interface-Based Projection (Closed)

```java
// Define an interface with only the fields you need
public interface UserSummary {
    String getName();
    String getEmail();
}

// Use it in the repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<UserSummary> findByActive(boolean active);
}

// Spring generates a proxy — only name and email are fetched from DB
```

### Interface-Based Projection (Open — with SpEL)

```java
public interface UserSummary {
    String getFirstName();
    String getLastName();

    @Value("#{target.firstName + ' ' + target.lastName}") // computed field
    String getFullName();
}
```

### Class-Based Projection (DTO Projection)

```java
public class UserSummaryDto {
    private final String name;
    private final String email;

    // Spring maps constructor by matching parameter names to entity fields
    public UserSummaryDto(String name, String email) {
        this.name = name;
        this.email = email;
    }

    // getters...
}

// In repository:
@Query("SELECT new com.example.dto.UserSummaryDto(u.name, u.email) FROM User u WHERE u.active = true")
List<UserSummaryDto> findActiveSummaries();
```

### Projection vs DTO — When to Use Which

| | Interface Projection | Class-Based Projection | Full Entity |
|---|---|---|---|
| Fields loaded | Only specified | Only specified | All columns |
| Usage | Read-only views | Read-only views | Read + write |
| Custom logic | SpEL only | Constructor only | Full object |
| Best for | Simple read APIs | API responses | CRUD operations |

---

## 7. JPA Specifications (Dynamic Queries)

### What is the Problem?
When building a search endpoint with optional filters (name, status, date range), you'd end up with many conditional query methods or a growing list of `@Query` methods:

```java
// Bad — combinatorial explosion of methods
findByName(String name);
findByStatus(String status);
findByNameAndStatus(String name, String status);
findByNameAndStatusAndCreatedAfter(String name, String status, LocalDate date);
// ... and so on
```

### Solution: JPA Specification

```java
// 1. Extend JpaSpecificationExecutor in repository
public interface UserRepository
    extends JpaRepository<User, Long>, JpaSpecificationExecutor<User> { }

// 2. Build dynamic specifications
public class UserSpecifications {

    public static Specification<User> hasName(String name) {
        return (root, query, cb) ->
            name == null ? null : cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
    }

    public static Specification<User> hasStatus(String status) {
        return (root, query, cb) ->
            status == null ? null : cb.equal(root.get("status"), status);
    }

    public static Specification<User> createdAfter(LocalDate date) {
        return (root, query, cb) ->
            date == null ? null : cb.greaterThanOrEqualTo(root.get("createdAt"), date);
    }
}

// 3. Combine and execute dynamically
@GetMapping("/search")
public List<User> search(
        @RequestParam(required = false) String name,
        @RequestParam(required = false) String status,
        @RequestParam(required = false) LocalDate from) {

    Specification<User> spec = Specification
        .where(UserSpecifications.hasName(name))
        .and(UserSpecifications.hasStatus(status))
        .and(UserSpecifications.createdAfter(from));

    return userRepository.findAll(spec);
}
```

When a parameter is `null`, the corresponding specification returns `null`, which Spring Data ignores — so only the provided filters are applied.

---

## 8. Testcontainers

### What is Testcontainers?
A Java library that spins up real Docker containers during tests — giving you an actual MySQL, PostgreSQL, Redis, Kafka instance rather than an H2 in-memory fake. Tests run against the real technology, catching bugs that H2 would miss (e.g. MySQL-specific SQL, Redis commands, Kafka consumer groups).

### Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-testcontainers</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>mysql</artifactId>
    <scope>test</scope>
</dependency>
```

### Basic Usage (JPA Test with Real MySQL)

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE) // don't replace with H2
@Testcontainers
class UserRepositoryTest {

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldSaveAndFindUser() {
        userRepository.save(new User("Alice", "alice@test.com"));
        assertThat(userRepository.findByEmail("alice@test.com")).isPresent();
    }
}
```

### Shared Container (Performance Optimization)

Starting a container per test class is slow. Use `@TestConfiguration` to share one container across the whole test suite:

```java
@TestConfiguration(proxyBeanMethods = false)
public class TestcontainersConfig {

    @Bean
    @ServiceConnection // Spring Boot 3.1+ — auto-configures datasource
    MySQLContainer<?> mysqlContainer() {
        return new MySQLContainer<>("mysql:8.0");
    }
}
```

> **Interview tip:** "I use Testcontainers for integration tests because it tests against the real database engine. H2 doesn't support all MySQL/PostgreSQL features, so tests that pass with H2 can fail in production."

---

## 9. WireMock

### What is WireMock?
WireMock stubs external HTTP APIs during tests. When your service calls another service (e.g. a payment gateway, a third-party API), WireMock intercepts those HTTP calls and returns a configured fake response — no real network call is made.

### Dependency

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-contract-wiremock</artifactId>
    <scope>test</scope>
</dependency>
```

### Usage

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureWireMock(port = 0) // starts WireMock on a random port
class PaymentServiceTest {

    @Value("${wiremock.server.port}")
    private int wireMockPort;

    @Autowired
    private PaymentService paymentService;

    @Test
    void shouldProcessPayment_whenGatewayReturnsSuccess() {
        // Stub the external API
        stubFor(post(urlEqualTo("/payments"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("{\"status\": \"APPROVED\", \"transactionId\": \"tx-123\"}")));

        // Call your service (which internally calls the stubbed HTTP endpoint)
        PaymentResult result = paymentService.processPayment(new PaymentRequest(100.0, "USD"));

        assertThat(result.getStatus()).isEqualTo("APPROVED");
    }

    @Test
    void shouldHandleGatewayTimeout() {
        stubFor(post(urlEqualTo("/payments"))
            .willReturn(aResponse().withFixedDelay(5000))); // simulates timeout

        assertThrows(TimeoutException.class,
            () -> paymentService.processPayment(new PaymentRequest(100.0, "USD")));
    }
}
```

---

## 10. Security Testing (@WithMockUser)

### @WithMockUser — Simulate a Logged-In User

```java
@WebMvcTest(UserController.class)
class UserControllerSecurityTest {

    @Autowired private MockMvc mockMvc;

    @Test
    @WithMockUser(username = "alice", roles = "USER")
    void getProfile_asUser_shouldReturn200() throws Exception {
        mockMvc.perform(get("/api/profile"))
               .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void getAllUsers_asAdmin_shouldReturn200() throws Exception {
        mockMvc.perform(get("/api/admin/users"))
               .andExpect(status().isOk());
    }

    @Test
    void getProfile_notAuthenticated_shouldReturn401() throws Exception {
        mockMvc.perform(get("/api/profile"))
               .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "USER") // not admin
    void getAllUsers_asUser_shouldReturn403() throws Exception {
        mockMvc.perform(get("/api/admin/users"))
               .andExpect(status().isForbidden());
    }
}
```

### @WithUserDetails — Use Your Custom UserDetailsService

```java
@Test
@WithUserDetails(value = "alice@test.com", userDetailsServiceBeanName = "customUserDetailsService")
void getProfile_withRealUser_shouldReturn200() throws Exception {
    mockMvc.perform(get("/api/profile"))
           .andExpect(status().isOk())
           .andExpect(jsonPath("$.email").value("alice@test.com"));
}
```

### Testing JWT Endpoints

```java
@Test
void getProfile_withValidJwt_shouldReturn200() throws Exception {
    String token = jwtService.generateToken("alice@test.com");

    mockMvc.perform(get("/api/profile")
            .header("Authorization", "Bearer " + token))
           .andExpect(status().isOk());
}
```

---

## 11. Spring Cloud Contract

### What is Contract Testing?
In microservices, Service A calls Service B. If Service B changes its API without telling Service A, things break silently. Contract testing defines a **shared contract** between consumer and provider, verified by automated tests on both sides.

### How It Works

```
1. Consumer (Service A) writes a contract describing what response it expects
2. Contract is shared with Provider (Service B)
3. Provider's tests verify its API matches the contract
4. Consumer's tests use WireMock stubs generated from the contract
```

### Example Contract (Groovy DSL)

```groovy
// src/test/resources/contracts/get_user.groovy
org.springframework.cloud.contract.spec.Contract.make {
    description "should return user by ID"
    request {
        method GET()
        url '/api/users/1'
        headers { header('Authorization', 'Bearer token123') }
    }
    response {
        status OK()
        headers { contentType(applicationJson()) }
        body([
            id: 1,
            name: "Alice",
            email: "alice@example.com"
        ])
    }
}
```

---

## 12. Graceful Shutdown

### What is Graceful Shutdown?
When you stop a Spring Boot app (e.g. during a deployment), in-flight requests may be abruptly terminated. Graceful shutdown waits for active requests to complete before shutting down — preventing data corruption and 500 errors for users.

### Enable It (One Line)

```properties
# application.properties
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s  # wait up to 30 seconds
```

That's it. Spring Boot will:
1. Stop accepting new requests immediately.
2. Wait up to 30 seconds for ongoing requests to finish.
3. Then shut down.

### How It Works Internally
Spring Boot uses `SmartLifecycle` beans that have a phase order. On shutdown, Spring calls `stop()` on each lifecycle bean in reverse order. The embedded server stops accepting connections first (phase 2147483646), then other beans are stopped.

### `@PreDestroy` for Cleanup

```java
@Component
public class KafkaConsumerManager {

    @PreDestroy
    public void shutdownConsumer() {
        kafkaConsumer.close(Duration.ofSeconds(10)); // flush and close
        log.info("Kafka consumer closed gracefully");
    }
}
```

---

## 13. Virtual Threads (Java 21 + Spring Boot 3.2)

### What are Virtual Threads?
Traditional Java threads are OS threads — heavy, limited in number (thousands), and expensive to create. Virtual threads are lightweight JVM-managed threads — you can have **millions** of them. They are ideal for I/O-bound work (DB calls, HTTP calls) where threads spend most time waiting.

### Enable in Spring Boot (One Line)

```properties
spring.threads.virtual.enabled=true
```

That's it. Spring Boot automatically configures:
- Embedded Tomcat to use virtual threads for request handling
- `@Async` task executor to use virtual threads
- Scheduled tasks to use virtual threads

### Why It Matters
Before virtual threads, scaling required reactive programming (WebFlux, Mono/Flux) — complex and hard to debug. Virtual threads give you the same scalability with the simple imperative/blocking code you're already writing.

```java
// This blocking code now scales like reactive code — thanks to virtual threads
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow(); // blocks virtual thread, not OS thread
}
```

> **Interview tip:** "Virtual threads eliminate the need for reactive programming in most cases. With `spring.threads.virtual.enabled=true` in Spring Boot 3.2+, standard blocking code handles the same concurrency as WebFlux."

---

## 14. GraalVM Native Image

### What is GraalVM Native Image?
Compiles your Spring Boot app **ahead of time** into a native binary (no JVM needed at runtime). The result starts in milliseconds and uses far less memory — ideal for serverless (AWS Lambda) and containerized deployments.

### Comparison

| | JVM App | Native Image |
|---|---|---|
| Startup time | 2–10 seconds | 50–100 milliseconds |
| Memory usage | 200–500 MB | 50–100 MB |
| Throughput | High (JIT optimized) | Slightly lower |
| Build time | Fast | Very slow (5–20 min) |
| Best for | Long-running services | Serverless, CLI tools |

### How to Build

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.graalvm.buildtools</groupId>
    <artifactId>native-maven-plugin</artifactId>
</plugin>
```

```bash
./mvnw -Pnative native:compile
./target/myapp  # runs natively, no java command needed
```

### With Spring Boot's Buildpacks (no GraalVM installed)

```bash
./mvnw spring-boot:build-image -Pnative
docker run myapp:latest
```

---

## 15. Externalized Config & Property Source Order

### Spring Boot's Property Resolution Order (Higher = Wins)

```
1. Command-line arguments           --server.port=9090
2. SPRING_APPLICATION_JSON          env var with JSON
3. ServletConfig init parameters
4. ServletContext init parameters
5. JNDI (java:comp/env)
6. System properties                -Dserver.port=9090
7. OS environment variables         SERVER_PORT=9090
8. Profile-specific outside jar     application-{profile}.properties (outside)
9. Profile-specific inside jar      application-{profile}.properties (inside)
10. application.properties outside jar
11. application.properties inside jar
12. @PropertySource annotations
13. Default properties (SpringApplication.setDefaultProperties)
```

> **Interview tip:** "Command-line arguments always win. This is why you can override any property at deployment time without rebuilding the app."

### Relaxed Binding
Spring Boot allows flexible property key formats — all of these bind to the same field:

```properties
spring.datasource.url=...       # standard kebab-case (recommended)
spring.datasource.URL=...       # uppercase
SPRING_DATASOURCE_URL=...       # OS environment variable format
spring.datasource.url=...       # underscore format
```

Your `@ConfigurationProperties` class just needs a standard camelCase field:
```java
private String url; // binds to all of the above
```

---

## 16. Spring Batch

### What is Spring Batch?
A framework for processing large volumes of data in scheduled bulk operations — reading from a source (DB, CSV, API), transforming it, and writing to a destination. Handles restartability, chunk processing, error handling, and job monitoring.

### Core Concepts

| Concept | Meaning |
|---|---|
| **Job** | The entire batch process (e.g., "process monthly reports") |
| **Step** | A phase within a Job (e.g., "read CSV", "transform", "write to DB") |
| **ItemReader** | Reads data one item at a time (from DB, file, API) |
| **ItemProcessor** | Transforms/validates each item (optional) |
| **ItemWriter** | Writes processed items to destination |
| **Chunk** | Spring reads N items, processes them, then writes all at once (atomic) |
| **JobRepository** | Stores job execution metadata in DB (enables restart from failure point) |

### Simple Example

```java
@Configuration
@EnableBatchProcessing
public class ReportJobConfig {

    @Bean
    public Job generateReportsJob(JobRepository jobRepository, Step processStep) {
        return new JobBuilder("generateReportsJob", jobRepository)
            .start(processStep)
            .build();
    }

    @Bean
    public Step processStep(JobRepository jobRepository,
                            PlatformTransactionManager txManager) {
        return new StepBuilder("processStep", jobRepository)
            .<User, ReportRow>chunk(100, txManager) // process 100 items at a time
            .reader(userReader())
            .processor(userToReportProcessor())
            .writer(reportWriter())
            .build();
    }

    @Bean
    public JpaPagingItemReader<User> userReader() {
        return new JpaPagingItemReaderBuilder<User>()
            .name("userReader")
            .queryString("SELECT u FROM User u WHERE u.active = true")
            .pageSize(100)
            .entityManagerFactory(entityManagerFactory)
            .build();
    }
}
```

---

## 17. Outbox Pattern

### What Problem Does It Solve?
In microservices, you often need to save data to your DB **and** publish an event to Kafka/RabbitMQ atomically. If you save to DB and then Kafka publish fails, you have data without the event (inconsistency). The Outbox Pattern guarantees both happen together.

### How It Works

```
1. Within a single DB transaction:
   a. Save your domain entity (e.g. Order)
   b. Save an OutboxEvent record in the same DB

2. A separate process (poller or Debezium CDC) reads OutboxEvent records
3. It publishes them to Kafka/RabbitMQ
4. After successful publish, marks OutboxEvent as processed

Result: DB write and event publish are effectively atomic
```

### Outbox Entity

```java
@Entity
@Table(name = "outbox_events")
public class OutboxEvent {
    @Id @GeneratedValue
    private Long id;

    private String aggregateType;   // e.g. "ORDER"
    private String aggregateId;     // e.g. "order-123"
    private String eventType;       // e.g. "ORDER_PLACED"

    @Column(columnDefinition = "JSON")
    private String payload;         // serialized event data

    private boolean processed = false;
    private LocalDateTime createdAt = LocalDateTime.now();
}
```

---

## 18. Distributed Locking

### What is the Problem?
In a clustered app (multiple instances), a `@Scheduled` job runs on every instance simultaneously — leading to duplicate processing. You need a way to ensure only one instance executes a critical section at a time.

### Using Redis (Redisson)

```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
</dependency>
```

```java
@Service
public class ReportScheduler {

    @Autowired
    private RedissonClient redisson;

    @Scheduled(cron = "0 0 2 * * *") // 2 AM daily
    public void generateDailyReport() {
        RLock lock = redisson.getLock("daily-report-lock");

        boolean acquired = lock.tryLock(); // non-blocking — return false if already locked
        if (!acquired) {
            log.info("Another instance is running the report job. Skipping.");
            return;
        }

        try {
            reportService.generateDailyReport();
        } finally {
            lock.unlock(); // always release
        }
    }
}
```

### Using ShedLock (Simpler, DB-based)

```java
@Scheduled(cron = "0 0 2 * * *")
@SchedulerLock(name = "daily-report-lock", lockAtMostFor = "10m", lockAtLeastFor = "1m")
public void generateDailyReport() {
    reportService.generateDailyReport();
}
// ShedLock stores the lock in a DB table — no Redis needed
```

---

## 19. Multipart File Upload & Download

### File Upload

```java
@RestController
@RequestMapping("/api/files")
public class FileController {

    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("File is empty");
        }

        String filename = StringUtils.cleanPath(file.getOriginalFilename());
        Path targetPath = Paths.get("uploads/" + filename);
        Files.copy(file.getInputStream(), targetPath, StandardCopyOption.REPLACE_EXISTING);

        return ResponseEntity.ok("Uploaded: " + filename);
    }

    // Multiple files
    @PostMapping("/upload-multiple")
    public ResponseEntity<List<String>> uploadMultiple(
            @RequestParam("files") List<MultipartFile> files) {
        List<String> names = files.stream()
            .map(MultipartFile::getOriginalFilename)
            .collect(Collectors.toList());
        // save each...
        return ResponseEntity.ok(names);
    }
}
```

### File Download

```java
@GetMapping("/download/{filename}")
public ResponseEntity<Resource> downloadFile(@PathVariable String filename) throws Exception {
    Path filePath = Paths.get("uploads/" + filename);
    Resource resource = new UrlResource(filePath.toUri());

    if (!resource.exists()) {
        return ResponseEntity.notFound().build();
    }

    String contentType = Files.probeContentType(filePath);

    return ResponseEntity.ok()
        .contentType(MediaType.parseMediaType(contentType))
        .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filename + "\"")
        .body(resource);
}
```

### Configuration

```properties
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=50MB
```

---

## 20. @DependsOn, @Import, Spring Environment

### @DependsOn
Forces Spring to initialize one bean before another, even if there's no direct dependency:

```java
@Bean
@DependsOn("databaseInitializer") // this bean must be created first
public UserService userService() {
    return new UserService();
}
```

### @Import
Explicitly imports a configuration class into the current context — useful when it's not in the component scan path:

```java
@Configuration
@Import({SecurityConfig.class, CacheConfig.class})
public class AppConfig { }
```

### Spring Environment
The `Environment` object holds all properties from all sources (application.properties, env vars, system props). Inject it to read properties programmatically:

```java
@Autowired
private Environment env;

public void doSomething() {
    String dbUrl = env.getProperty("spring.datasource.url");
    boolean isProd = env.matchesProfiles("prod");
    String[] activeProfiles = env.getActiveProfiles();
}
```

---

## 21. Liquibase vs Flyway

Both tools manage database schema version control. They run migration scripts in order and track which ones have already been applied.

| | Flyway | Liquibase |
|---|---|---|
| Script format | SQL only | SQL, XML, YAML, JSON |
| Change tracking | `flyway_schema_history` table | `databasechangelog` table |
| Rollback | Manual (write undo scripts) | Built-in rollback support |
| Simplicity | Simpler — easier to start | More powerful — more complex |
| Conditional logic | No | Yes (preconditions) |
| Spring Boot default | Flyway (more common) | Both supported |

```properties
# Enable Flyway (default: auto-detects if on classpath)
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration

# Enable Liquibase
spring.liquibase.enabled=true
spring.liquibase.change-log=classpath:db/changelog/master.xml
```

> **Interview tip:** "I prefer Flyway for simplicity — plain SQL scripts are easy for the whole team to read. I'd choose Liquibase if I needed rollback support or multi-DB format flexibility."

---

## 22. OAuth2 Resource Server (JWT)

### What is an OAuth2 Resource Server?
Your Spring Boot API acts as a **Resource Server** — it protects resources (endpoints) and validates JWT tokens issued by an external **Authorization Server** (e.g. Keycloak, Auth0, Okta, Spring Authorization Server).

### Configuration

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
</dependency>
```

```properties
# Point to your authorization server's JWK endpoint (public keys for JWT verification)
spring.security.oauth2.resourceserver.jwt.jwk-set-uri=https://auth.mycompany.com/auth/realms/myrealm/protocol/openid-connect/certs
```

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .anyRequest().authenticated())
        .oauth2ResourceServer(oauth2 -> oauth2
            .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter())))
        .build();
}

// Extract roles from JWT claims (Keycloak format)
@Bean
public JwtAuthenticationConverter jwtAuthConverter() {
    JwtGrantedAuthoritiesConverter converter = new JwtGrantedAuthoritiesConverter();
    converter.setAuthoritiesClaimName("realm_access.roles");
    converter.setAuthorityPrefix("ROLE_");

    JwtAuthenticationConverter jwtConverter = new JwtAuthenticationConverter();
    jwtConverter.setJwtGrantedAuthoritiesConverter(converter);
    return jwtConverter;
}
```

### OAuth2 Roles Clarified

| Role | Meaning |
|---|---|
| **Resource Owner** | The user (owns their data) |
| **Client** | The app requesting access (React frontend, mobile app) |
| **Authorization Server** | Issues tokens after user consents (Keycloak, Auth0, Okta) |
| **Resource Server** | Your Spring Boot API — validates tokens and serves protected data |

---

## 🎯 Quick-Fire One-Liners (Supplement)

| Concept | Interview Answer |
|---|---|
| **Filter** | Servlet-level HTTP interception — before Spring; use for JWT, GZIP, rate limiting |
| **Interceptor** | Spring MVC level — pre/post controller; use for auth checks, audit logging |
| **AOP** | Bean method level — any Spring bean; use for transactions, caching, performance |
| **UserDetailsService** | Interface to load user from your DB; `loadUserByUsername()` returns `UserDetails` |
| **Refresh token** | Long-lived token to get new access tokens; stored in DB; rotated on each use |
| **CORS** | Server tells browser which cross-origins are allowed; configure in Security filter chain |
| **Spring Events** | `ApplicationEventPublisher` publishes; `@EventListener` listens; decouples components |
| **Interface projection** | Repository returns only specific fields via an interface; Spring generates proxy |
| **Class-based projection** | DTO populated via JPQL constructor expression; type-safe read-only result |
| **JPA Specification** | Dynamic `WHERE` clauses via `Specification<T>`; combine with `and()`/`or()` |
| **Testcontainers** | Real Docker containers in tests; catches bugs H2 misses; `@Container` annotation |
| **WireMock** | Stubs external HTTP calls in tests; `stubFor(get(...).willReturn(...))` |
| **@WithMockUser** | Simulates authenticated user in `@WebMvcTest`; sets security context |
| **Contract testing** | Consumer writes contract; provider verifies; catches API breakage at build time |
| **Graceful shutdown** | `server.shutdown=graceful`; waits for in-flight requests before stopping |
| **Virtual threads** | `spring.threads.virtual.enabled=true`; millions of lightweight threads; Java 21+ |
| **GraalVM native** | Compiles to binary; 50ms startup; ideal for serverless; slow build time |
| **@DependsOn** | Forces one bean to be created before another regardless of injection |
| **Outbox pattern** | Write domain entity + event to DB atomically; poller publishes to Kafka |
| **Distributed locking** | Redis/ShedLock prevents duplicate `@Scheduled` execution across instances |
| **Spring Batch chunk** | Read N → process N → write N atomically; restart picks up from failure point |
| **Liquibase vs Flyway** | Liquibase has rollback + multi-format; Flyway is simpler plain-SQL |
| **OAuth2 Resource Server** | Your API validates tokens from external auth server (Keycloak/Auth0) |
| **Property source order** | CLI args > env vars > profile props > application.properties > defaults |
| **Relaxed binding** | `MY_APP_URL`, `my.app.url`, `my-app-url` all bind to the same `@ConfigurationProperties` field |

---

*Combine with your original notes for complete Spring Boot interview preparation. 🚀*