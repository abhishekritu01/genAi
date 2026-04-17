# System Design & Design Patterns — Complete Notes

> **Audience:** Backend developers with 1–6 years of experience  
> **Purpose:** Interview preparation & quick revision  
> **Stack Context:** Java / Spring Boot

---

## Table of Contents

1. [Why Design Patterns Matter](#1-why-design-patterns-matter)
2. [SOLID Principles](#2-solid-principles)
3. [Composition vs Inheritance](#3-composition-vs-inheritance)
4. [Coupling — Tight vs Loose](#4-coupling--tight-vs-loose)
5. [Pattern Categories Overview](#5-pattern-categories-overview)
6. [Creational Patterns](#6-creational-patterns)
7. [Structural Patterns](#7-structural-patterns)
8. [Behavioral Patterns](#8-behavioral-patterns)
9. [Distributed System Patterns](#9-distributed-system-patterns)
10. [Data & Consistency Patterns](#10-data--consistency-patterns)
11. [Anti-Patterns](#11-anti-patterns)
12. [Pattern Selection Cheat Sheet](#12-pattern-selection-cheat-sheet)
13. [Interview Q&A](#13-interview-qa)

---

## 1. Why Design Patterns Matter

### The Real Problem

Real software faces constant change:
- Requirements evolve under time pressure
- New developers join and leave
- Code lives for years across many teams

**Without structure:** small changes break many files, refactoring feels risky, and bugs multiply.

### What Patterns Are — and Are Not

| Patterns ARE | Patterns ARE NOT |
|---|---|
| Battle-tested solutions to recurring problems | Fancy or clever code |
| A shared vocabulary for teams | Over-engineering for its own sake |
| Tools for surviving change | Mandatory rules |
| Ways to reduce coupling | A substitute for thinking |

> **Core insight:** Design patterns exist because developers kept facing the **same problems** in large, long-lived systems. They are solutions extracted from real experience.

---

## 2. SOLID Principles

SOLID is the **foundation** on which all design patterns are built.

| Letter | Principle | One-Line Summary |
|---|---|---|
| **S** | Single Responsibility | One class = one reason to change |
| **O** | Open/Closed | Extend without modifying |
| **L** | Liskov Substitution | Child must behave like parent |
| **I** | Interface Segregation | Small, focused interfaces |
| **D** | Dependency Inversion | Depend on abstractions, not concretions |

---

### S — Single Responsibility Principle (SRP)

**Rule:** A class should have only one reason to change.

#### ❌ Violation
```java
class InvoiceService {
    void calculateInvoice() {}  // business logic
    void saveToDB() {}          // persistence
    void sendEmail() {}         // notification
}
```
A DB change forces you to touch the same class as an email provider change — unrelated concerns are coupled.

#### ✅ Correct Design
```java
class InvoiceCalculator {          // business logic only
    double calculateTotal(Invoice invoice) { ... }
}

class InvoiceRepository {          // persistence only
    void save(Invoice invoice) { ... }
}

class EmailService {               // notification only
    void sendInvoice(Invoice invoice) { ... }
}

class InvoiceService {             // orchestration only
    void processInvoice(Invoice invoice) {
        double total = calculator.calculateTotal(invoice);
        invoice.setTotal(total);
        repository.save(invoice);
        emailService.sendInvoice(invoice);
    }
}
```

**Memory trick — CPNO:** Calculator · Persistence · Notification · Orchestrator

---

### O — Open/Closed Principle (OCP)

**Rule:** Open for extension, closed for modification.

#### ❌ Violation
```java
class PaymentService {
    void pay(String type) {
        if (type.equals("CARD")) { ... }
        else if (type.equals("UPI")) { ... }
        // Adding Wallet → must modify this class ❌
    }
}
```

#### ✅ Correct Design
```java
interface Payment {
    void pay(double amount);
}

class CardPayment implements Payment { ... }
class UpiPayment implements Payment { ... }

// Adding Wallet → new class, no existing code touched ✅
class WalletPayment implements Payment { ... }

class PaymentService {
    void processPayment(Payment payment, double amount) {
        payment.pay(amount);   // depends on abstraction
    }
}
```

**Pattern used:** Strategy Pattern  
**Memory trick:** "Add new class, don't touch old class."

---

### L — Liskov Substitution Principle (LSP)

**Rule:** A child class must be usable wherever a parent class is expected, without breaking behavior.

#### ❌ Classic Violation — Rectangle / Square
```java
class Rectangle {
    void setWidth(int w)  { this.width = w; }
    void setHeight(int h) { this.height = h; }
    int getArea() { return width * height; }
}

class Square extends Rectangle {
    void setWidth(int w)  { this.width = w; this.height = w; } // side effect!
    void setHeight(int h) { this.width = h; this.height = h; } // side effect!
}

// Breaking behavior:
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(10);
System.out.println(r.getArea()); // expected 50, got 100 ❌
```

#### ✅ Correct Design
```java
interface Shape { int getArea(); }

class Rectangle implements Shape {
    Rectangle(int w, int h) { ... }
    public int getArea() { return width * height; }
}

class Square implements Shape {
    Square(int side) { ... }
    public int getArea() { return side * side; }
}
```

**Key insight:** Square is NOT a proper Rectangle. Both are Shapes — use the right abstraction.

**Behavioral contract rules for child classes:**

| Rule | Meaning |
|---|---|
| Preconditions | Child must not require stricter inputs than parent |
| Postconditions | Child must not return weaker results |
| Exceptions | Child must not throw unexpected exceptions |
| Side effects | Child must not change expected behavior |

**Memory trick:** "Replace child without breaking code."

---

### I — Interface Segregation Principle (ISP)

**Rule:** Clients should not be forced to implement methods they don't use.

#### ❌ Violation
```java
interface Worker {
    void work();
    void eat(); // Robot doesn't eat!
}

class RobotWorker implements Worker {
    public void work() { ... }
    public void eat() { /* empty — forced, meaningless */ } // ❌
}
```

#### ✅ Correct Design
```java
interface Workable { void work(); }
interface Eatable  { void eat();  }

class HumanWorker implements Workable, Eatable { ... }
class RobotWorker implements Workable { ... }   // only what it needs
```

**Memory trick:** "Split big interface into small pieces."

---

### D — Dependency Inversion Principle (DIP)

**Rule:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

#### ❌ Violation
```java
class UserService {
    private MySQLDatabase db = new MySQLDatabase(); // concrete, tight coupling ❌
}
```

#### ✅ Correct Design
```java
interface Database { void save(String data); }

class MySQLDatabase implements Database { ... }
class MongoDatabase implements Database { ... }

class UserService {
    private final Database db;
    public UserService(Database db) { this.db = db; } // injected ✅
}
```

**Spring Boot applies DIP automatically via Dependency Injection:**
```java
@Repository class MySQLDatabase implements Database {}

@Service
class UserService {
    private final UserRepository repo;
    public UserService(UserRepository repo) { this.repo = repo; } // Spring injects
}
```

**Memory trick:** "Depend on Interface, not Implementation."

---

## 3. Composition vs Inheritance

### Prefer Composition over Inheritance

| Feature | Inheritance (IS-A) | Composition (HAS-A) |
|---|---|---|
| Relationship | Child IS a type of parent | Class HAS a behavior |
| Flexibility | Low — fixed at compile time | High — changeable at runtime |
| Coupling | Tight | Loose |
| Testability | Harder | Easier |
| Reusability | Limited | High |

### Why Inheritance Can Fail

```java
class Bird { void fly() {} }

class Ostrich extends Bird {
    void fly() { throw new UnsupportedOperationException(); } // ❌ breaks LSP
}
```

### Composition Solution

```java
interface FlyBehavior { void fly(); }

class CanFly    implements FlyBehavior { public void fly() { System.out.println("Flying"); } }
class CannotFly implements FlyBehavior { public void fly() { System.out.println("Cannot fly"); } }

class Bird {
    private FlyBehavior flyBehavior;
    public Bird(FlyBehavior flyBehavior) { this.flyBehavior = flyBehavior; }
    public void performFly() { flyBehavior.fly(); }
}

// Usage
Bird sparrow = new Bird(new CanFly());
Bird ostrich = new Bird(new CannotFly());

// Runtime flexibility ✅
bird.setFlyBehavior(new CanFly());
```

> **Rule of thumb:** Use inheritance only for true IS-A relationships. Use composition when you need flexibility and loose coupling.

---

## 4. Coupling — Tight vs Loose

**Coupling** = how strongly classes depend on each other.

| Feature | Tight Coupling ❌ | Loose Coupling ✅ |
|---|---|---|
| Depends on | Concrete class | Interface |
| Testing | Hard to mock | Easy to mock |
| Change impact | High — ripples everywhere | Low — isolated |
| Scalability | Limited | High |

### How to Achieve Loose Coupling
1. Program to **interfaces**, not implementations
2. Use **Dependency Injection**
3. Prefer **Composition** over Inheritance
4. Apply **Design Patterns** (Strategy, Factory, Repository…)

> **One-liner:** "Tight coupling means classes depend on concrete implementations, making change difficult. Loose coupling means classes depend on abstractions, making the system flexible and testable."

---

## 5. Pattern Categories Overview

| Category | Purpose | Memory Acronym |
|---|---|---|
| **Creational** | Control how objects are created | **SPBAF** — Singleton, Prototype, Builder, Abstract Factory, Factory |
| **Structural** | Manage relationships between objects | **ABCDFFP** — Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| **Behavioral** | Control how objects communicate | Observer, Strategy, Command, Chain, State, Iterator, Mediator, Memento, Template, Visitor |

---

## 6. Creational Patterns

> **Why they exist:** Object creation becomes complex, spreads everywhere, and increases coupling. Creational patterns centralize and control lifecycle.

---

### Singleton

**Intent:** Ensure only one instance of a class exists in the application.

**Use when:** The resource is shared, expensive to create, and must be consistent — e.g., DB connection manager, Logger, Cache.

```java
public class Logger {
    private static Logger instance;

    private Logger() {}

    public static synchronized Logger getInstance() {
        if (instance == null) instance = new Logger();
        return instance;
    }
}
```

**Thread-safe alternative (preferred):**
```java
public class Logger {
    private static final Logger INSTANCE = new Logger(); // eager initialization
    private Logger() {}
    public static Logger getInstance() { return INSTANCE; }
}
```

**⚠️ When NOT to use Singleton:**

| Reason | Why It Fails |
|---|---|
| Shared mutable state | Causes race conditions and hard-to-trace bugs |
| Testing | Singleton holds state across tests, making tests order-dependent |
| Scalability | Becomes a bottleneck; hard to parallelize |
| Multiple implementations | Can't have MySQL singleton AND Mongo singleton |

> **Senior answer:** "Singleton is often overused. In Spring, I let the framework manage bean scope instead of writing Singleton manually."

---

### Factory Method

**Intent:** Define an interface for creating objects, but let subclasses or configuration decide which class to instantiate.

**Use when:** The type of object depends on runtime conditions (user input, config, type flag).

```java
interface PaymentGateway { void pay(double amount); }

class CardPayment   implements PaymentGateway { ... }
class UpiPayment    implements PaymentGateway { ... }
class WalletPayment implements PaymentGateway { ... }

class PaymentGatewayFactory {
    public static PaymentGateway getGateway(String type) {
        return switch (type) {
            case "CARD"   -> new CardPayment();
            case "UPI"    -> new UpiPayment();
            case "WALLET" -> new WalletPayment();
            default -> throw new IllegalArgumentException("Unknown type");
        };
    }
}
```

**Benefit:** Adding a new payment method = new class + one line in factory. No business logic touched.

**⚠️ When NOT to use:** Only one implementation exists; simple object with no variation.

---

### Abstract Factory

**Intent:** Create families of related objects without specifying their concrete classes.

**Use when:** You need to switch between entire product families consistently (e.g., all Stripe components vs all Razorpay components).

```java
interface PaymentProcessorFactory {
    PaymentProcessor createProcessor();
    RefundProcessor  createRefundProcessor();
    SettlementService createSettlement();
}

class StripeFactory    implements PaymentProcessorFactory { ... }
class RazorpayFactory  implements PaymentProcessorFactory { ... }
```

> **Difference from Factory Method:** Factory creates *one* product. Abstract Factory creates *a family* of related products.

---

### Builder

**Intent:** Construct complex objects step-by-step, separating construction from representation.

**Use when:** Object has many (especially optional) fields; long constructors are hard to read.

```java
// Without Builder ❌
new User("Alice", "alice@mail.com", 28, "Mumbai", "+91...", "ADMIN", "ACTIVE");
// What does each argument mean?

// With Builder ✅
User user = User.builder()
    .name("Alice")
    .email("alice@mail.com")
    .role("ADMIN")
    .build();
```

**Lombok shortcut (Spring Boot):**
```java
@Builder
@Data
public class User {
    private String name;
    private String email;
    private String role;
}
```

**⚠️ When NOT to use:** Object has only 2–3 fields; performance-critical inner loops.

---

### Prototype

**Intent:** Create new objects by cloning an existing object instead of creating from scratch.

**Use when:** Object creation is expensive; you need many similar objects with minor variations.


```
# Prototype Design Pattern

## 📌 Intent

Create new objects by **cloning an existing object** instead of creating from scratch.

---

## 🤔 When to Use

* Object creation is **expensive** (DB calls, API calls, heavy computation)
* Need **many similar objects** with small changes
* Want to **avoid repeating setup logic**

---

## ❌ Without Prototype

```java
User user1 = new User("Alice", "ADMIN", loadPermissions());
User user2 = new User("Bob", "ADMIN", loadPermissions());
```

### Problems:

* ❗ Repeated expensive operations
* ❗ Duplicate code
* ❗ Hard to maintain

---

## ✅ With Prototype

```java
User template = new User("Template", "ADMIN", loadPermissions());

User user1 = template.clone();
user1.setName("Alice");

User user2 = template.clone();
user2.setName("Bob");
```

### Benefits:

* ✔ Faster object creation
* ✔ Reuse existing configuration
* ✔ Cleaner code

---

## 🧠 Clone Method

```java
@Override
public User clone() {
    return new User(this.name, this.role, this.permissions);
}
```

---

## ⚠️ Deep Copy vs Shallow Copy

### 🔸 Shallow Copy ❌

```java
return new User(this.name, this.role, this.permissions);
```

* Copies reference
* Changes affect all objects

---

### 🔸 Deep Copy ✅

```java
@Override
public User clone() {
    return new User(
        this.name,
        this.role,
        new ArrayList<>(this.permissions)
    );
}
```

* Creates new copy
* Safe from side effects

---

## 🌍 Real-World Examples

* 🕹 Game objects (enemy templates)
* 📄 Document templates (invoice, reports)
* ⚙️ Spring Prototype Beans

---

## 🆚 Builder vs Prototype

| Feature  | Builder               | Prototype             |
| -------- | --------------------- | --------------------- |
| Purpose  | Step-by-step creation | Clone existing object |
| Use Case | Complex construction  | Reuse configuration   |
| Speed    | Slower                | Faster                |

---

## 🔥 Interview One-Liner

> Prototype pattern creates objects by cloning existing instances, improving performance when object creation is costly.

---

## 🚨 Common Mistakes

* ❌ Not using deep copy
* ❌ Sharing mutable objects
* ❌ Using when object creation is simple

---


```

```java
@Override
public User clone() {
    return new User(this.name, this.role, this.permissions); // deep or shallow copy
}
```

**Real use:** Copying pre-configured templates, game objects sharing base configuration.

---

## 7. Structural Patterns

> **Why they exist:** To integrate systems safely and extend behavior without breaking existing code.

---

### Adapter

**Intent:** Convert one interface into another that a client expects. Makes incompatible interfaces work together.

**Use when:** You need to integrate a third-party or legacy system whose interface doesn't match yours, and you can't change either.

```java
// What your system expects
interface PaymentGateway {
    void pay(double amount);
}

// What the third-party SDK provides
class RazorpaySdk {
    void createOrder(Map<String, Object> params) { ... }
}

// Adapter: translates your interface to the SDK's
class RazorpayAdapter implements PaymentGateway {
    private final RazorpaySdk sdk;

    public RazorpayAdapter(RazorpaySdk sdk) { this.sdk = sdk; }

    @Override
    public void pay(double amount) {
        Map<String, Object> params = Map.of("amount", amount);
        sdk.createOrder(params); // translates the call
    }
}
```

> **Mindset:** "I will translate, not modify."

---

### Facade

**Intent:** Provide a simplified interface to a complex subsystem.

**Use when:** A system has many classes/steps and you want to expose one clean entry point to consumers.

```java
// Complex internals
class AuthService       { void authenticate() {} }
class ValidationService { void validate() {} }
class OrderService      { void createOrder() {} }
class PaymentCapture    { void capture() {} }

// Facade — hides all complexity
class PaymentFacade {
    public void pay(double amount) {
        auth.authenticate();
        validator.validate();
        order.createOrder();
        capture.capture();
    }
}
// Client only calls: paymentFacade.pay(100);
```

> **Important:** Facade does NOT remove complexity — it **hides** it.

---

### Proxy

**Intent:** Provide a surrogate or placeholder for another object to control access to it.

**Use when:** You need to add auth, caching, logging, or rate limiting without modifying the real object.

```java
interface OrderService { Order getOrder(String id); }

class RealOrderService implements OrderService {
    public Order getOrder(String id) { /* DB call */ }
}

class CachingOrderServiceProxy implements OrderService {
    private final OrderService real;
    private final Map<String, Order> cache = new HashMap<>();

    public Order getOrder(String id) {
        return cache.computeIfAbsent(id, real::getOrder);
    }
}
```

**Real-world example:** API Gateway acts as a Proxy — auth, rate limiting, logging — before forwarding to backend services.

---

### Decorator

**Intent:** Attach additional responsibilities to an object dynamically by wrapping it.

**Use when:** You need to add features (logging, auth, metrics) in a stackable, flexible way without subclass explosion.


```java
interface RequestHandler { void handle(Request req); }

class CoreHandler implements RequestHandler {
    public void handle(Request req) { /* business logic */ }
}

class LoggingDecorator implements RequestHandler {
    private final RequestHandler wrapped;
    public void handle(Request req) {
        log("Incoming: " + req);
        wrapped.handle(req);
    }
}

class AuthDecorator implements RequestHandler {
    private final RequestHandler wrapped;
    public void handle(Request req) {
        authenticate(req);
        wrapped.handle(req);
    }
}

// Stack decorators
RequestHandler handler = new LoggingDecorator(
                           new AuthDecorator(
                             new CoreHandler()));
```

**Real-world example:** Spring's filter chains and middleware pipelines are Decorator in action.

---

### Quick Structural Pattern Comparison

| Pattern | Problem Solved | Interface Change | Key Distinction |
|---|---|---|---|
| **Adapter** | Interface mismatch | Changes interface | Translates for compatibility |
| **Facade** | Complex subsystem | New simple interface | Simplifies access |
| **Proxy** | Access control | Same interface | Controls/guards the real object |
| **Decorator** | Add behavior dynamically | Same interface | Stacks additional responsibilities |

**Interview scenario map:**

| Question | Answer |
|---|---|
| Integrate third-party SDK? | Adapter + Facade |
| Add auth/logging without touching business code? | Proxy or Decorator |
| Simplify a complex module for consumers? | Facade |
| Proxy vs Decorator? | Proxy controls access; Decorator adds responsibility |

---

## 8. Behavioral Patterns

> **Why they exist:** To change how systems behave at runtime without modifying existing code.

---

### Strategy ⭐ (Most Important)

**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Use when:** You have multiple ways to do the same task (payment, sorting, load balancing, discount rules).


```
# Strategy Pattern (Simple Notes)

## 📌 What is it?

Choose different **algorithms (behaviors)** at runtime.

---

## 💡 Idea

Same task → multiple ways to do it → switch anytime

---

## 🧠 Example (Sorting)

```java
interface SortStrategy {
    void sort(int[] arr);
}

class AscendingSort implements SortStrategy {
    public void sort(int[] arr) {
        System.out.println("Sorting Ascending");
    }
}

class DescendingSort implements SortStrategy {
    public void sort(int[] arr) {
        System.out.println("Sorting Descending");
    }
}
```

---

## 🔥 Usage

```java
Sorter sorter = new Sorter(new AscendingSort());
sorter.sort(arr);

sorter.setStrategy(new DescendingSort()); // change at runtime
sorter.sort(arr);
```

---

## ⚙️ Flow

* First → Ascending sort
* Then → Change to Descending
* Behavior changes without modifying code

---

## 🎯 Key Point

👉 Same task (sorting), different behavior
👉 Behavior can change at runtime

---

## ✅ Benefits

* ✔ No if-else logic
* ✔ Easy to extend (add new strategy)
* ✔ Clean & flexible

---

## 🔥 Interview Line

> Strategy pattern allows switching algorithms at runtime.

---


```




```java
interface LoadBalancingStrategy {
    Server select(List<Server> servers);
}

class RoundRobin    implements LoadBalancingStrategy { ... }
class LeastConn     implements LoadBalancingStrategy { ... }
class RandomSelect  implements LoadBalancingStrategy { ... }

class LoadBalancer {
    private LoadBalancingStrategy strategy;

    public LoadBalancer(LoadBalancingStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(LoadBalancingStrategy strategy) {
        this.strategy = strategy; // change at runtime ✅
    }

    public Server getServer(List<Server> servers) {
        return strategy.select(servers);
    }
}
```

> **Key benefit:** Replaces if-else chains with polymorphism. Runtime behavior change without redeployment.

---

### Observer ⭐

**Intent:** Define a one-to-many dependency so that when one object changes state, all its dependents are notified automatically.

**Use when:** Multiple independent services must react to an event without the event publisher knowing about them.


```
# Observer Pattern (Simple Notes)

## 📌 What is it?

One object (subject) notifies **multiple objects (observers)** when something changes.

---

## 💡 Idea

One event → many reactions

---

## 🛒 Example (Order System)

When order is placed:

* 📧 Email sent
* 📱 SMS sent
* 📦 Inventory updated
* 📊 Analytics updated

👉 One action triggers multiple services

---

## 🧠 Code Example

```java
interface OrderEventListener {
    void onOrderPlaced(Order order);
}

class EmailService implements OrderEventListener {
    public void onOrderPlaced(Order order) {
        System.out.println("Send Email");
    }
}

class SmsService implements OrderEventListener {
    public void onOrderPlaced(Order order) {
        System.out.println("Send SMS");
    }
}
```

---

## 🔥 Subject (Main Class)

```java
class OrderService {
    private List<OrderEventListener> listeners = new ArrayList<>();

    public void addListener(OrderEventListener l) {
        listeners.add(l);
    }

    public void placeOrder(Order order) {
        // business logic
        listeners.forEach(l -> l.onOrderPlaced(order));
    }
}
```

---

## ⚙️ Flow

```java
OrderService service = new OrderService();

service.addListener(new EmailService());
service.addListener(new SmsService());

service.placeOrder(order);
```

* Order placed
* Email sent
* SMS sent

---

## 🎯 Key Point

👉 One event → notify many listeners
👉 Loose coupling (no direct dependency)

---

## ✅ Benefits

* ✔ Easy to add new listeners
* ✔ No change in main logic
* ✔ Scalable & flexible

---

## 🔥 Interview Line

> Observer pattern notifies multiple objects automatically when an event occurs.

---

## 🚨 Common Mistakes

* ❌ Forgetting to register listeners
* ❌ Too many listeners (performance issue)

---





```java
interface OrderEventListener {
    void onOrderPlaced(Order order);
}

class EmailService     implements OrderEventListener { ... }
class SmsService       implements OrderEventListener { ... }
class InventoryService implements OrderEventListener { ... }
class AnalyticsService implements OrderEventListener { ... }

class OrderService {
    private List<OrderEventListener> listeners = new ArrayList<>();

    public void addListener(OrderEventListener l) { listeners.add(l); }

    public void placeOrder(Order order) {
        // business logic
        listeners.forEach(l -> l.onOrderPlaced(order)); // notify all
    }
}
```

> **Adding a new observer:** Create one new class, register it. No change to `OrderService`.

---

### Command

**Intent:** Encapsulate a request as an object, allowing queuing, logging, and undoable operations.

**Use when:** You need to queue operations, implement undo/redo, or log all actions.

```java
# Command Pattern (Short Notes)

## 📌 What is it?

Convert a request/action into an **object**.

---

## 💡 Idea

Action → Object → can execute, store, undo

---

## 🎮 Example (Bank Transfer)

```java
interface Command {
    void execute();
    void undo();
}

class TransferMoneyCommand implements Command {
    public void execute() {
        account.debit(amount);
    }

    public void undo() {
        account.credit(amount);
    }
}
```

---

## 🔥 Usage

```java
CommandQueue queue = new CommandQueue();

queue.execute(new TransferMoneyCommand()); // debit
queue.undoLast(); // undo → credit
```

---

## ⚙️ Flow

* Execute command
* Store in history
* Undo when needed

---

## 🎯 Key Point

👉 Action is stored as object
👉 Can undo / log / queue

---

## ✅ Benefits

* ✔ Supports undo/redo
* ✔ Easy to log actions
* ✔ Can queue operations

---

## 🔥 Interview Line

> Command pattern turns actions into objects to support undo, logging, and queuing.



---

### Chain of Responsibility ⭐

**Intent:** Pass a request along a chain of handlers where each handler decides to process it or pass it on.

**Use when:** A request must go through multiple steps (auth, rate limit, validation, business logic) that can be composed and reordered.


🚪 Easy Real-Life Example

Think of security check at airport:

🪪 ID Check
🎒 Bag Scan
🛂 Boarding Pass Check

👉 If you fail at any step → stopped
👉 If you pass → go to next

```java
abstract class RequestHandler {
    private RequestHandler next;

    public RequestHandler setNext(RequestHandler next) {
        this.next = next;
        return next;
    }

    protected void passToNext(Request req) {
        if (next != null) next.handle(req);
    }

    public abstract void handle(Request req);
}

class AuthHandler extends RequestHandler {
    public void handle(Request req) {
        if (!authenticated(req)) throw new UnauthorizedException();
        passToNext(req);
    }
}

class RateLimitHandler extends RequestHandler {
    public void handle(Request req) {
        if (rateLimitExceeded(req)) throw new TooManyRequestsException();
        passToNext(req);
    }
}

// Chain setup
RequestHandler chain = new AuthHandler();
chain.setNext(new RateLimitHandler()).setNext(new ValidationHandler());
```

---

### Template Method

**Intent:** Define the skeleton of an algorithm in a base class, deferring some steps to subclasses.

**Use when:** Multiple classes follow the same process flow but differ in specific steps.


🍜 Easy Real-Life Example

Think of making tea vs coffee:

Steps are same:

Boil water
Add main ingredient
Pour into cup
Add extras

👉 But:

Tea → add tea leaves 🍃
Coffee → add coffee powder ☕

👉 Same flow, different steps
👉 This is Template Method


```java
abstract class ReportGenerator {
    // Template method — defines the skeleton
    public final void generate() {
        fetchData();
        processData();
        formatReport();   // subclasses override this
        exportReport();   // subclasses override this
    }

    abstract void formatReport();
    abstract void exportReport();

    private void fetchData()   { /* common logic */ }
    private void processData() { /* common logic */ }
}

class PdfReport   extends ReportGenerator { ... }
class ExcelReport extends ReportGenerator { ... }
```

> **Limitation:** Behavior is fixed at compile time. Use Strategy instead if you need runtime switching.

---

### Behavioral Pattern Comparison

| Pattern | What Changes | When |
|---|---|---|
| **Strategy** | Algorithm / logic | Runtime — config or context |
| **Observer** | Reaction to events | Event-driven, async |
| **Command** | Request handling | Queuing, undo, logging |
| **Chain** | Processing steps | Pipelines, middleware |
| **Template** | Step implementation | Compile-time — fixed flow |

---

## 9. Distributed System Patterns

> **Core philosophy:** Failure is normal. Design for it. Assume things will fail.

---

### Circuit Breaker ⭐

**Intent:** Prevent cascading failures by stopping calls to a failing downstream service and providing a fallback.

**States:**

| State | Behavior |
|---|---|
| **Closed** | Calls flow normally; failures are counted |
| **Open** | Failures exceeded threshold; calls fail immediately with fallback |
| **Half-Open** | Test requests allowed; if success → Closed; if fail → Open |

```
Order Service → [Circuit Breaker] → Payment Service
                     ↓ (Payment down)
               [Fallback Response]   ← system survives
```

**Tool:** Resilience4j in Spring Boot
```java
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest req) { ... }

public PaymentResponse paymentFallback(PaymentRequest req, Exception ex) {
    return PaymentResponse.queued(); // graceful degradation
}
```

---

### Retry + Exponential Backoff ⭐

**Intent:** Retry failed operations — but with increasing wait times to avoid hammering a recovering service.

**Pattern:** `wait = base * 2^attempt + jitter`

```
Attempt 1: wait 100ms
Attempt 2: wait 200ms
Attempt 3: wait 400ms
Attempt 4: wait 800ms + random jitter
```

**⚠️ Only retry idempotent operations.** Do NOT retry:
- Non-idempotent POST operations (may cause duplicates)
- Permanent failures (4xx errors)
- Business rule violations

```java
@Retry(name = "inventoryService", fallbackMethod = "fallback")
public InventoryResponse checkInventory(String productId) { ... }
```

---

### Bulkhead ⭐

**Intent:** Isolate different dependencies into separate resource pools so failure in one doesn't exhaust resources for others.

**Analogy:** Compartments in a ship — one compartment flooding doesn't sink the vessel.

```
Without Bulkhead:          With Bulkhead:
Payment hangs              Thread Pool A → Payment
  ↓                        Thread Pool B → Notification
All threads blocked         Thread Pool C → Analytics
  ↓                         Failure in A isolates to A ✅
Entire service crashes
```

**Types:** Thread pool isolation, Connection pool isolation, Resource quotas

---

### Rate Limiter

**Intent:** Control the rate of incoming requests to protect the system from overload and abuse.

| Algorithm | How It Works | Best For |
|---|---|---|
| **Token Bucket** | Tokens added at fixed rate; each request consumes a token; allows bursts | APIs, user-facing systems |
| **Leaky Bucket** | Requests processed at constant rate; excess queued or dropped | Background jobs, smooth traffic |

**Real use:** API Gateway enforces 100 req/sec per user → excess returns `HTTP 429`.

---

### Idempotency ⭐

**Intent:** Ensure that making the same request multiple times produces the same result — critical when combined with retries.

**Problem:** Network timeout → retry → payment charged twice ❌

**Solution:** Idempotency key
```
POST /payments
Headers: Idempotency-Key: txn-abc-12345

Server stores result with this key.
Duplicate request → same response returned, no re-execution.
```

| HTTP Method | Idempotent? |
|---|---|
| GET | ✅ Yes |
| PUT | ✅ Yes |
| DELETE | ✅ Yes |
| POST | ❌ No (usually) |

---

### How These Patterns Work Together

A real microservice call flow layers all of them:

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

---

### Failure Scenarios & Solutions

| Problem | Pattern |
|---|---|
| Downstream service slow/down | Circuit Breaker |
| Temporary network failure | Retry + Exponential Backoff |
| Thread pool exhaustion | Bulkhead |
| Traffic spike / abuse | Rate Limiter |
| Duplicate requests on retry | Idempotency |

---

## 10. Data & Consistency Patterns

> **Core insight:** Strong consistency doesn't scale in distributed systems. Design for controlled eventual consistency.

---

### Saga Pattern ⭐

**Intent:** Replace a distributed ACID transaction with a sequence of local transactions, each with a compensating action for rollback.

**Problem:** An order flow spans Order Service, Payment Service, and Inventory Service — you cannot use a single DB transaction across services.

**Flow:**
```
1. Create Order      → success ✅
2. Reserve Payment   → success ✅
3. Reserve Inventory → FAILS ❌
   ↓ compensate
3a. Refund Payment   (compensating action)
3b. Cancel Order     (compensating action)
```

#### Saga Orchestration vs Choreography

| | Orchestration | Choreography |
|---|---|---|
| **How** | Central coordinator tells services what to do | Services emit events; others react |
| **Pros** | Clear flow, easier to debug, centralized logic | Decentralized, scales well, loose coupling |
| **Cons** | Orchestrator = complexity + single point of failure | Hard to trace, event chaos risk |
| **Best for** | Complex workflows, strong business rules | Simple event-driven flows |

---

### CQRS — Command Query Responsibility Segregation ⭐

**Intent:** Separate the write model (commands) from the read model (queries) to allow independent scaling.

```
Write Side (Command)       Read Side (Query)
─────────────────          ──────────────────
Validate business rules    Optimized for reads
Save to Write DB           Denormalized Read DB
Emit events        ──→     Subscribe & update read store
```

**When to use:** Systems with very different read/write loads; complex reporting queries; analytics alongside transactional data.

**Trade-off:** Eventual consistency between write and read models; higher complexity.

---

### Event Sourcing ⭐

**Intent:** Store state as a sequence of immutable events rather than as current state only.

```
Traditional DB:   { account: "Alice", balance: 500 }   ← current state only

Event Sourcing:
  AccountCreated   { balance: 0 }
  MoneyDeposited   { amount: 1000 }
  MoneyWithdrawn   { amount: 500 }
  ─────────────────────────────────
  Current balance = 0 + 1000 - 500 = 500   ← derived
```

**Benefits:** Full audit trail, easy replay, time travel debugging, natural event-driven fit.

**Challenges:** Event schema evolution, storage growth, debugging complexity.

---

### Two-Phase Commit (2PC) — Why It Fails

**What it is:** Classic distributed transaction — Prepare phase + Commit phase across all participants.

**Why it fails at scale:**

| Problem | Impact |
|---|---|
| Blocking protocol | All participants lock until coordinator responds |
| Coordinator failure | System halts — no progress possible |
| Poor performance | Synchronous across network |
| Doesn't scale | Cannot work with hundreds of microservices |

> **Use Saga instead** of 2PC in microservice architectures.

---

### Consistency Pattern Comparison

| Pattern | Consistency | Scalability | Complexity |
|---|---|---|---|
| Saga | Eventual | High | Medium |
| CQRS | Eventual | High | High |
| Event Sourcing | Eventual | High | Very High |
| 2PC | Strong | Low | High |

---

## 11. Anti-Patterns

> **Why this matters:** Senior engineers are defined by what they **avoid**, not just what they add. Anti-patterns look right initially but cause long-term damage.

---

| Anti-Pattern | What It Looks Like | Problem | Fix |
|---|---|---|---|
| **God Object** | One class does everything | Hard to test, change, or reason about | Apply SRP; split into Service, Repository, Validator |
| **Spaghetti Code** | Deeply nested if-else, no clear flow | Debugging nightmare; hard to onboard | Extract methods; use Strategy / Chain of Responsibility |
| **Golden Hammer** | "We always use Kafka / microservices / Singleton" | Overengineering; wrong tool for job | Choose tools based on the problem |
| **Premature Optimization** | Caching, sharding, complex structures before measuring | Wrong bottleneck optimized | Measure first; optimize hotspots only |
| **Overengineering** | Too many patterns, layers, and abstractions | Slower dev; hard to understand | Start simple; apply YAGNI principle |
| **Tight Coupling** | `new MySQLDatabase()` inside service | Hard to test, change, or swap | Depend on interfaces; use DI |
| **Shared Database** | Multiple services on same DB tables | Schema changes break all services | Database per service; replicate via events |
| **Chatty Services** | Dozens of small network calls per request | High latency; network overhead | Coarse-grained APIs; aggregation layer |
| **Cascading Failures** | One service down brings down the entire system | No isolation of failure | Circuit Breaker, Bulkhead, graceful degradation |
| **No Idempotency** | Retry causes double payment, duplicate order | Data corruption | Idempotency keys and deduplication logic |
| **Synchronous Everything** | Blocking calls across 5 services per request | High latency, fragility | Async messaging; event-driven where possible |
| **Hardcoded Business Rules** | `if (amount > 10000) applyDiscount()` | Requires redeploy for rule change | Strategy Pattern; config-driven rules |

> **One-liner:** "Knowing anti-patterns shows engineering maturity more than knowing patterns."

---

## 12. Pattern Selection Cheat Sheet

### By Problem Type

| Problem | Pattern |
|---|---|
| Runtime algorithm/logic change | Strategy |
| Multiple services react to one event | Observer |
| Sequential processing steps (middleware) | Chain of Responsibility |
| Add behavior without modifying existing class | Decorator / Proxy |
| Third-party / legacy integration | Adapter |
| Simplify complex subsystem | Facade |
| Shared single resource | Singleton (or DI-managed scope) |
| Complex object construction | Builder |
| Family of related objects | Abstract Factory |
| Queue/undo operations | Command |
| Downstream service failures | Circuit Breaker |
| Transient failures | Retry + Backoff |
| Thread exhaustion from one dependency | Bulkhead |
| Duplicate requests | Idempotency |
| Distributed business transaction | Saga |
| High read/write asymmetry | CQRS |
| Full audit trail | Event Sourcing |

### Patterns That Commonly Go Together

| Scenario | Pattern Combination |
|---|---|
| Payment service | Strategy + Circuit Breaker + Retry + Idempotency |
| API Gateway | Proxy + Rate Limiter + Chain of Responsibility |
| Order placement | Saga + Observer (notifications) + Builder (request) |
| Notification system | Observer + Strategy (channel selection) |
| Multi-tenant system | Abstract Factory + Factory |

---

## 13. Interview Q&A

> Questions for developers with **1–6 years** of experience. Answers are intentionally concise.

---

### SOLID & OOP

**Q1. What is the Single Responsibility Principle? Give a real example.**
> A class should have only one reason to change. In practice, I separate `InvoiceCalculator` (business logic), `InvoiceRepository` (persistence), and `EmailService` (notification) rather than putting all three inside one `InvoiceService`.

**Q2. Explain Open/Closed Principle with a payment example.**
> OCP means you can add new behavior without modifying existing code. For payments, each type (Card, UPI, Wallet) implements a `Payment` interface. Adding Crypto = new class only. `PaymentService` never changes.

**Q3. What is the Liskov Substitution Principle and why does Square extending Rectangle violate it?**
> LSP says you should be able to replace a parent with its child without breaking behavior. Square overrides `setWidth` and `setHeight` to keep both equal, so `rect.setWidth(5); rect.setHeight(10); rect.getArea()` returns 100 instead of the expected 50. That's a broken contract.

**Q4. Difference between OCP and LSP?**
> OCP is about extending systems without modifying them (open for extension, closed for modification). LSP is about inheritance contracts — child classes must honor the behavioral promises of the parent.

**Q5. Why prefer composition over inheritance?**
> Inheritance creates tight coupling — child classes are fragile when parents change. Composition lets you inject behavior, swap it at runtime, and test independently. For example, `Bird` with a `FlyBehavior` interface works for Ostrich too, unlike `Bird extends FlyingAnimal`.

---

### Creational Patterns

**Q6. Why is Singleton considered problematic?**
> It creates global mutable state which makes tests order-dependent, prevents mocking, and becomes a bottleneck under load. In Spring, I let the framework manage scope (`@Service` is singleton-scoped by default) rather than writing the pattern manually.

**Q7. When would you use Builder pattern over constructor?**
> When a class has more than 4–5 fields, especially optional ones. `User.builder().name("A").role("ADMIN").build()` is far more readable and less error-prone than a 7-argument constructor where order matters.

**Q8. Factory vs Abstract Factory — what's the difference?**
> Factory creates one product; Abstract Factory creates a family of related products consistently. Factory → `PaymentGatewayFactory.get("CARD")`. Abstract Factory → `StripeFactory` that returns Stripe's `PaymentProcessor`, `RefundProcessor`, and `SettlementService` — all Stripe-specific, no mixing.

---

### Structural Patterns

**Q9. When would you use Adapter vs Facade?**
> Adapter: when two incompatible interfaces need to work together — e.g., your `PaymentGateway` interface vs a Razorpay SDK with a different API. Facade: when you want to simplify a complex subsystem — e.g., hiding 5 internal steps behind one `pay()` method.

**Q10. What's the difference between Proxy and Decorator?**
> Both wrap an object with the same interface. Proxy is about **controlling access** (auth, caching, rate limiting). Decorator is about **adding responsibility** (logging, metrics, transformation) in a stackable way. Spring AOP is a form of Proxy; Servlet filters are Decorators.

**Q11. Explain how middleware in Express.js or Spring's filter chain relates to a design pattern.**
> It's Chain of Responsibility — each handler (auth, rate limit, validation) does one thing and passes the request to the next. Adding a new step = new handler class, no existing code touched.

---

### Behavioral Patterns

**Q12. You have 15 if-else blocks for different discount rules. What pattern applies?**
> Strategy Pattern. Each discount rule becomes a class implementing a `DiscountStrategy` interface. The caller selects and injects the right strategy at runtime. New discount type = new class only.

**Q13. How does Observer pattern enable loose coupling in a notification system?**
> The `OrderService` publishes an event without knowing who listens. `EmailService`, `SMSService`, and `AnalyticsService` subscribe independently. Adding a new notification channel = new observer class, no change to `OrderService`.

**Q14. When would you use Template Method vs Strategy?**
> Template Method: the flow is fixed, only specific steps vary — define the skeleton in the base class. Strategy: you need to swap the entire algorithm or behavior at runtime. Template = compile-time flexibility; Strategy = runtime flexibility.

---

### Distributed Patterns

**Q15. What is a Circuit Breaker and what states does it have?**
> Circuit Breaker prevents cascading failures by stopping calls to a failing service. States: **Closed** (normal operation), **Open** (failures exceeded threshold — fail immediately with fallback), **Half-Open** (test requests to check recovery).

**Q16. Why should you use exponential backoff instead of constant retry intervals?**
> Constant retries cause a thundering herd — all clients hammer the recovering service at once, preventing it from recovering. Exponential backoff spreads the load: 100ms, 200ms, 400ms, 800ms — plus random jitter to de-synchronize clients.

**Q17. When should you NOT retry a failed operation?**
> Non-idempotent operations (could cause duplicates), permanent failures (business rule violations, 4xx errors), and cases where you don't have idempotency protection. Only retry safe, idempotent operations.

**Q18. What is the Bulkhead pattern and why does it matter?**
> Bulkhead isolates resources (thread pools, connection pools) per dependency. If the Payment service hangs, it exhausts only its thread pool — Notification and Analytics continue normally. Without it, one slow service can crash the entire application.

---

### Data & Consistency

**Q19. Why not use distributed transactions (2PC) in microservices?**
> 2PC is a blocking protocol — all services lock until the coordinator responds. If the coordinator fails, the system halts. It doesn't scale and introduces tight coupling. Saga is the preferred alternative: local commits with compensating actions on failure.

**Q20. When would you choose Saga Orchestration vs Choreography?**
> Orchestration: complex workflows with strong business rules where you need to trace execution — a central coordinator manages the flow. Choreography: simpler event-driven systems that need to scale and stay loosely coupled, where each service reacts to events independently.

**Q21. What problem does CQRS solve?**
> When read and write patterns are very different — e.g., thousands of reads per second with complex joins, but only occasional writes. CQRS separates read and write models so each can be optimized and scaled independently. The trade-off is eventual consistency.

**Q22. What is Event Sourcing and what are its drawbacks?**
> Store state changes as immutable events rather than just current state. Full audit trail, replay capability. Drawbacks: event schema evolution is painful, storage grows over time, and debugging requires replaying the entire event stream.

---

### Anti-Patterns & Trade-offs

**Q23. What is a God Object and how do you fix it?**
> A class that does too much — holds business logic, talks to DB, calls APIs, sends emails. It's hard to test, change, or reason about. Fix: apply SRP — split into focused classes: Service, Repository, Validator, Orchestrator.

**Q24. What does "premature optimization" mean and why is it harmful?**
> Adding caching, sharding, or complex data structures before measuring where the actual bottleneck is. It optimizes the wrong thing, adds complexity, and makes code harder to debug. Correct approach: measure → profile → optimize the actual hotspot.

**Q25. What is the "Shared Database" anti-pattern?**
> Multiple microservices reading and writing the same database tables. Any schema change breaks all services; teams cannot deploy independently. Fix: database-per-service, with data replication via events.

**Q26. How do you handle adding cross-cutting concerns (logging, auth, metrics) without modifying every service?**
> Use Proxy or Decorator pattern, or AOP (Aspect-Oriented Programming) in Spring. Define the concern once, apply it declaratively. `@Transactional` and `@Cacheable` in Spring are both AOP — i.e., Proxy/Decorator pattern applied transparently.

---

### Scenario-Based

**Q27. Design the pattern architecture for a payment service that must be resilient.**
> Rate Limiter at the gateway → Circuit Breaker around the payment provider call → Retry with exponential backoff for transient failures → Idempotency key on every payment request → Bulkhead to isolate payment threads from other dependencies → Saga for order/payment/inventory consistency.

**Q28. How would you explain why you picked Strategy over a large if-else block to a non-technical stakeholder?**
> "Each if-else branch was a different business rule. When we added a new rule, we risked breaking the existing ones. Now each rule is its own isolated unit — adding a new one doesn't touch any existing code, so the risk of regression drops dramatically."

---

*End of Notes — Good luck with your interviews! 🚀*