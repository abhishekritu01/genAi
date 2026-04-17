# ☕ Core Java – Complete Interview & Developer Notes
> Covers everything a 1–7 year Java developer must know. Topic-wise, explained with examples.

---

## 📌 Table of Contents
1. [Java Basics & Fundamentals](#1-java-basics--fundamentals)
2. [Data Types, Variables & Operators](#2-data-types-variables--operators)
3. [Control Flow](#3-control-flow)
4. [Object-Oriented Programming (OOP)](#4-object-oriented-programming-oop)
5. [Inheritance & Polymorphism](#5-inheritance--polymorphism)
6. [Interfaces & Abstract Classes](#6-interfaces--abstract-classes)
7. [Exception Handling](#7-exception-handling)
8. [String Handling](#8-string-handling)
9. [Collections Framework](#9-collections-framework)
10. [Generics](#10-generics)
11. [Java 8+ Features](#11-java-8-features)
12. [Multithreading & Concurrency](#12-multithreading--concurrency)
13. [Java Memory Model & JVM Internals](#13-java-memory-model--jvm-internals)
14. [File I/O & NIO](#14-file-io--nio)
15. [Design Patterns in Java](#15-design-patterns-in-java)
16. [Java 9–17+ Modern Features](#16-java-9-17-modern-features)
17. [Best Practices & Common Pitfalls](#17-best-practices--common-pitfalls)
18. [Quick-Fire One-Liners](#-quick-fire-one-liners)

---

## 1. Java Basics & Fundamentals

### What is Java?
Java is a high-level, object-oriented, platform-independent programming language. It follows the **Write Once, Run Anywhere (WORA)** principle — Java code compiles into **bytecode** which runs on the **JVM (Java Virtual Machine)** on any platform.

### JDK vs JRE vs JVM

| | Full Name | What it contains | Who needs it |
|---|---|---|---|
| **JVM** | Java Virtual Machine | Executes bytecode | Everyone at runtime |
| **JRE** | Java Runtime Environment | JVM + standard libraries | End users running Java apps |
| **JDK** | Java Development Kit | JRE + compiler (`javac`) + tools | Developers writing Java |

> **Interview answer:** "JDK is for development (includes compiler), JRE is for running Java apps, JVM is the engine that actually runs the bytecode. JDK ⊇ JRE ⊇ JVM."

### How Java Code Executes
```
Source code (.java)
      ↓  javac (compiler)
  Bytecode (.class)
      ↓  JVM
  Machine Code (platform-specific)
```

### Class & Object
- **Class** – A blueprint or template that defines the state (fields) and behavior (methods) of objects.
- **Object** – A concrete instance created from the class using the `new` keyword. Each object has its own copy of instance variables.

```java
// Class (blueprint)
public class Car {
    String brand;   // state
    int speed;

    void accelerate() {   // behavior
        speed += 10;
    }
}

// Object (instance)
Car myCar = new Car();   // new creates an object on the heap
myCar.brand = "Toyota";
myCar.accelerate();
```

### main() Method
```java
public static void main(String[] args) {
    // public  → accessible by JVM from anywhere
    // static  → JVM calls it without creating an object
    // void    → returns nothing
    // args    → command-line arguments
}
```

### Access Modifiers

| Modifier | Same Class | Same Package | Subclass | Everywhere |
|---|---|---|---|---|
| `private` | ✅ | ❌ | ❌ | ❌ |
| `(default)` | ✅ | ✅ | ❌ | ❌ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| `public` | ✅ | ✅ | ✅ | ✅ |

### static Keyword
`static` means the member belongs to the **class**, not to any specific object. All objects share the same static field or method.

```java
public class Counter {
    static int count = 0;  // shared across all objects
    int id;

    Counter() {
        count++;
        id = count;
    }
}

Counter c1 = new Counter(); // count = 1, c1.id = 1
Counter c2 = new Counter(); // count = 2, c2.id = 2
System.out.println(Counter.count); // 2 (accessed via class name)
```

**When to use static:**
- Utility/helper methods that don't need object state (`Math.sqrt()`, `Collections.sort()`)
- Constants: `static final double PI = 3.14159;`
- Factory methods: `Integer.valueOf(42)`

### final Keyword
- **`final` variable** – Value cannot be changed after assignment (effectively a constant)
- **`final` method** – Cannot be overridden in subclasses
- **`final` class** – Cannot be subclassed (e.g., `String`, `Integer`)

```java
final int MAX = 100;           // constant
MAX = 200;                     // ❌ compile error

final class UtilityClass { }   // cannot be extended
class Sub extends UtilityClass { } // ❌ compile error
```

### Wrapper Classes
Every primitive type has a corresponding wrapper class in `java.lang`. Needed when you require an object (e.g., in collections).

| Primitive | Wrapper |
|---|---|
| `int` | `Integer` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | `Character` |
| `long` | `Long` |
| `byte` | `Byte` |

**Autoboxing** – Automatic conversion from primitive to wrapper:
```java
Integer i = 42;        // autoboxing: int → Integer
int x = i;             // unboxing: Integer → int
List<Integer> list = new ArrayList<>();
list.add(5);           // autoboxing happens automatically
```

**Integer cache** (important interview topic):
```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);   // true  (cached range: -128 to 127)

Integer c = 128;
Integer d = 128;
System.out.println(c == d);   // false (outside cache, new objects)
System.out.println(c.equals(d)); // true (always use .equals() for comparison)
```

---

## 2. Data Types, Variables & Operators

### Primitive Data Types

| Type | Size | Range | Default |
|---|---|---|---|
| `byte` | 1 byte | -128 to 127 | 0 |
| `short` | 2 bytes | -32,768 to 32,767 | 0 |
| `int` | 4 bytes | -2^31 to 2^31-1 (~2.1 billion) | 0 |
| `long` | 8 bytes | -2^63 to 2^63-1 | 0L |
| `float` | 4 bytes | ~6-7 decimal digits | 0.0f |
| `double` | 8 bytes | ~15 decimal digits | 0.0d |
| `char` | 2 bytes | 0 to 65,535 (Unicode) | '\u0000' |
| `boolean` | JVM-specific | true / false | false |

```java
int a = 2_000_000;      // underscores for readability (Java 7+)
long big = 9_000_000_000L;  // L suffix required for long literals
float f = 3.14f;            // f suffix required for float
double d = 3.14159;         // default decimal is double
```

### Type Casting

**Widening (automatic — no data loss):**
```
byte → short → int → long → float → double
```
```java
int i = 100;
long l = i;     // implicit, safe
double d = i;   // implicit, safe
```

**Narrowing (explicit — may lose data):**
```java
double d = 9.99;
int i = (int) d;    // i = 9, decimal part lost — explicit cast required
long l = 1000L;
int x = (int) l;    // explicit cast
```

### var (Local Variable Type Inference — Java 10+)
```java
var name = "Alice";         // compiler infers String
var list = new ArrayList<String>(); // compiler infers ArrayList<String>
var i = 42;                 // compiler infers int
```
`var` can only be used for local variables, not fields, method parameters, or return types.

### Operators

**Arithmetic:** `+`, `-`, `*`, `/`, `%`
```java
System.out.println(10 / 3);   // 3 (integer division)
System.out.println(10 % 3);   // 1 (remainder)
System.out.println(10.0 / 3); // 3.3333 (double division)
```

**Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`

**Logical:** `&&` (AND), `||` (OR), `!` (NOT)
- `&&` and `||` are **short-circuit** operators — if the first operand decides the result, the second is not evaluated.

**Bitwise:** `&`, `|`, `^`, `~`, `<<`, `>>`, `>>>`
```java
int a = 5;   // 0101
int b = 3;   // 0011
System.out.println(a & b);  // 1  (0001)
System.out.println(a | b);  // 7  (0111)
System.out.println(a ^ b);  // 6  (0110) XOR
System.out.println(a << 1); // 10 (1010) left shift = multiply by 2
System.out.println(a >> 1); // 2  (0010) right shift = divide by 2
```

**Ternary:** `condition ? valueIfTrue : valueIfFalse`
```java
int max = (a > b) ? a : b;
```

**instanceof:**
```java
Object obj = "Hello";
if (obj instanceof String s) {  // Java 16+ pattern matching
    System.out.println(s.toUpperCase());
}
```

---

## 3. Control Flow

### if / else if / else
```java
int score = 75;
if (score >= 90) {
    System.out.println("A");
} else if (score >= 75) {
    System.out.println("B");  // prints this
} else {
    System.out.println("C");
}
```

### Switch Statement (classic)
```java
int day = 3;
switch (day) {
    case 1: System.out.println("Monday"); break;
    case 2: System.out.println("Tuesday"); break;
    case 3: System.out.println("Wednesday"); break; // prints this
    default: System.out.println("Other");
}
// Without break, execution "falls through" to next case
```

### Switch Expression (Java 14+) — preferred
```java
String result = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3 -> "Wednesday";
    default -> "Other";
};

// With multiple statements per case:
String category = switch (score) {
    case 1, 2, 3 -> "Low";
    case 4, 5 -> {
        System.out.println("Processing...");
        yield "Medium";   // yield returns value in block switch
    }
    default -> "High";
};
```

### Loops

**for loop:**
```java
for (int i = 0; i < 5; i++) {
    System.out.println(i); // 0, 1, 2, 3, 4
}
```

**Enhanced for loop (for-each):**
```java
int[] numbers = {1, 2, 3, 4, 5};
for (int n : numbers) {
    System.out.println(n);
}
// Works on arrays and any Iterable (List, Set, etc.)
```

**while loop:**
```java
int i = 0;
while (i < 5) {
    System.out.println(i++);
}
```

**do-while loop:**
```java
int i = 0;
do {
    System.out.println(i++); // runs at least once
} while (i < 5);
```

### break, continue, return
```java
for (int i = 0; i < 10; i++) {
    if (i == 3) continue;  // skip 3, go to next iteration
    if (i == 7) break;     // exit loop entirely at 7
    System.out.println(i); // prints 0,1,2,4,5,6
}
```

**Labeled break** (breaks out of outer loop):
```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) break outer; // breaks both loops
    }
}
```

---

## 4. Object-Oriented Programming (OOP)

### The Four Pillars of OOP

### 1. Encapsulation
Wrapping data (fields) and behavior (methods) together, and controlling access to the data through access modifiers. Fields are typically `private`, accessed through `public` getters/setters.

```java
public class BankAccount {
    private double balance;  // hidden from outside
    private String owner;

    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        this.balance = initialBalance;
    }

    public double getBalance() {        // controlled read access
        return balance;
    }

    public void deposit(double amount) { // controlled write with validation
        if (amount > 0) {
            balance += amount;
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && balance >= amount) {
            balance -= amount;
            return true;
        }
        return false;
    }
}
```

**Why encapsulation matters:**
- Prevents invalid state (e.g., negative balance)
- You can change the internal implementation without breaking callers
- Makes code testable and maintainable

### 2. Inheritance
A class (subclass/child) inherits fields and methods from another class (superclass/parent) using `extends`. Promotes code reuse.

```java
public class Animal {
    String name;
    int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void eat() {
        System.out.println(name + " is eating");
    }

    public String describe() {
        return name + ", age " + age;
    }
}

public class Dog extends Animal {
    String breed;

    public Dog(String name, int age, String breed) {
        super(name, age);  // must call parent constructor first
        this.breed = breed;
    }

    public void bark() {
        System.out.println(name + " says Woof!");
    }

    @Override
    public String describe() {
        return super.describe() + ", breed: " + breed;
    }
}

Dog d = new Dog("Rex", 3, "Labrador");
d.eat();       // inherited from Animal
d.bark();      // Dog's own method
d.describe();  // overridden method
```

### 3. Polymorphism
The ability of an object to take many forms. A variable of a parent type can hold objects of any subtype. The actual method called is determined at runtime.

```java
Animal a1 = new Dog("Rex", 3, "Lab");   // Dog object in Animal reference
Animal a2 = new Cat("Whiskers", 2);

a1.makeSound(); // calls Dog's makeSound() — decided at RUNTIME
a2.makeSound(); // calls Cat's makeSound()

// Process any Animal the same way:
List<Animal> animals = List.of(a1, a2);
for (Animal a : animals) {
    a.makeSound(); // polymorphic call — correct method called for each type
}


Polymorphism in Java allows one interface to be used for different data types or objects. It is achieved through method overloading (compile-time) and method overriding (runtime). Runtime polymorphism enables dynamic method dispatch, where the method call is resolved at runtime based on the object type.

# Method Overloading
class Calculator {
    int add(int a, int b) {
        return a + b;
    }

    int add(int a, int b, int c) {
        return a + b + c;
    }
}


# Method Overriding
class Animal {
    void sound() {
        System.out.println("Animal sound");
    }
}


// Method Overriding
class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("Dog barks");
    }
}


Overloading increases readability by using the same method name for similar operations, while overriding enables runtime polymorphism and dynamic behavior in inheritance.

⚠️ Common Trap Question
👉 Can we override static methods?
No, static methods are hidden, not overridden.

```

### 4. Abstraction
Hiding complex implementation details and exposing only what is necessary. Achieved through abstract classes and interfaces.

```java
// User doesn't need to know HOW it works, just WHAT it does
List<String> list = new ArrayList<>();
list.add("Java");      // don't know/care about internal array resizing
list.get(0);           // don't know how indexing works internally
```

### Constructors

**Default constructor:** If you define no constructor, Java provides a no-arg constructor that does nothing.

**Constructor overloading:**
```java
public class Person {
    String name;
    int age;

    Person() {
        this("Unknown", 0);  // calls another constructor (constructor chaining)
    }

    Person(String name) {
        this(name, 0);
    }

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

**`this` keyword:**
- `this.field` – refers to the current object's field (distinguishes from local var)
- `this()` – calls another constructor in the same class
- `this` as a method argument – passes the current object

### Method Overloading vs Overriding

**Overloading (compile-time polymorphism):**
Same method name, different parameter list in the SAME class. Decided at compile time.

```java
public class Calculator {
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }    // different param types
    int add(int a, int b, int c) { return a + b + c; }  // different param count
}
```

**Overriding (runtime polymorphism):**
Subclass provides a different implementation of a method already defined in the parent. Must have same name, return type (or covariant), and parameter list.

```java
class Animal {
    String makeSound() { return "..."; }
}

class Dog extends Animal {
    @Override
    String makeSound() { return "Woof"; }  // overrides parent's method
}
```

**Rules for overriding:**
- Cannot reduce visibility (private → public OK, public → private NOT OK)
- Cannot override `final`, `static`, or `private` methods
- Can throw fewer or narrower checked exceptions than parent
- `@Override` annotation is optional but strongly recommended (catches mistakes)

### Object Class — Methods Every Java Object Has
Every class implicitly extends `java.lang.Object`. Key methods:

**`equals(Object o)`** – Checks logical equality. Default implementation checks reference equality (`==`). Override to compare field values.
```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;              // same reference
    if (!(o instanceof Person p)) return false; // null check + type check
    return age == p.age && Objects.equals(name, p.name);
}
```

**`hashCode()`** – Returns an integer hash. **Contract:** If `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` MUST be true. Always override both together.
```java
@Override
public int hashCode() {
    return Objects.hash(name, age);
}
```

**`toString()`** – String representation of the object. Called automatically when object is printed.
```java
@Override
public String toString() {
    return "Person{name='" + name + "', age=" + age + "}";
}
```

**`clone()`** – Creates a copy (shallow). Class must implement `Cloneable`.

**`equals() vs ==`**
```java
String s1 = new String("hello");
String s2 = new String("hello");

s1 == s2        // false (different objects in heap)
s1.equals(s2)   // true  (same character content)

// For String literals, == works due to String pool:
String a = "hello";
String b = "hello";
a == b  // true (both point to same String pool object)
```

### Inner Classes

**Static nested class** – Doesn't need an instance of the outer class. Like a top-level class but grouped inside another.
```java
public class Outer {
    static class StaticNested {
        void hello() { System.out.println("Static nested"); }
    }
}
Outer.StaticNested obj = new Outer.StaticNested();
```

**Inner class (non-static)** – Needs an instance of the outer class. Can access outer class members.
```java
public class Outer {
    int x = 10;
    class Inner {
        void print() { System.out.println(x); }  // can access outer's x
    }
}
Outer outer = new Outer();
Outer.Inner inner = outer.new Inner();
```

**Anonymous class** – One-time use class defined and instantiated inline. Common before lambdas.
```java
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Anonymous class");
    }
};
// With lambda (Java 8+):
Runnable r2 = () -> System.out.println("Lambda");
```

**Local class** – Defined inside a method. Rare in modern Java.

---

## 5. Inheritance & Polymorphism

### super Keyword
- `super.method()` – Calls the parent class's version of a method
- `super(args)` – Calls the parent class constructor (must be first line in child constructor)
- `super.field` – Accesses parent field (when hidden by child field with same name)

```java
class Vehicle {
    String type = "Vehicle";
    void info() { System.out.println("I am a vehicle"); }
}

class Car extends Vehicle {
    String type = "Car";  // hides parent's type field

    void info() {
        super.info();                          // calls Vehicle's info()
        System.out.println("I am a car");
    }

    void showTypes() {
        System.out.println(type);       // Car
        System.out.println(super.type); // Vehicle
    }
}
```

### Method Resolution Order (MRO)
At runtime, Java uses the **actual type** of the object (not the reference type) to decide which method to call.

```java
Animal a = new Dog("Rex", 3, "Lab");
a.makeSound(); // calls Dog's makeSound() — runtime type is Dog
```

### Covariant Return Type
An overriding method can return a subtype of the parent's return type:
```java
class Animal {
    Animal getInstance() { return new Animal(); }
}
class Dog extends Animal {
    @Override
    Dog getInstance() { return new Dog(); }  // Dog is subtype of Animal — OK
}
```

### Upcasting & Downcasting
```java
// Upcasting — implicit, always safe
Animal a = new Dog("Rex", 3, "Lab");  // Dog → Animal

// Downcasting — explicit, may throw ClassCastException
Dog d = (Dog) a;  // Animal → Dog (only safe if actual type IS Dog)

// Safe downcasting with instanceof:
if (a instanceof Dog dog) {    // Java 16+ pattern matching
    dog.bark();                // no explicit cast needed
}
```

### Abstract Classes
A class declared with `abstract` — cannot be instantiated directly. May have abstract methods (no body) that subclasses must implement.

```java
public abstract class Shape {
    String color;

    Shape(String color) { this.color = color; }

    // Abstract method — no body, must be implemented by subclass
    public abstract double area();

    // Concrete method — has body, inherited as-is
    public void describe() {
        System.out.println("A " + color + " shape with area " + area());
    }
}

public class Circle extends Shape {
    double radius;

    Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;  // must implement
    }
}
```

---

## 6. Interfaces & Abstract Classes

### Interface
A contract that defines what a class CAN do (not how). A class `implements` an interface and must provide implementations for all abstract methods.

```java
public interface Drawable {
    void draw();              // abstract by default (public abstract)
    double area();

    // Default method (Java 8+) — has a body, doesn't break existing implementations
    default String getInfo() {
        return "Drawable shape with area: " + area();
    }

    // Static method (Java 8+) — utility method on the interface
    static Drawable createCircle(double radius) {
        return new Circle(radius);
    }
}

public class Circle implements Drawable {
    double radius;

    Circle(double radius) { this.radius = radius; }

    @Override
    public void draw() { System.out.println("Drawing circle"); }

    @Override
    public double area() { return Math.PI * radius * radius; }
}
```

### Multiple Interface Implementation
```java
public interface Flyable {
    void fly();
    default String getType() { return "Flyable"; }
}

public interface Swimmable {
    void swim();
    default String getType() { return "Swimmable"; }
}

public class Duck implements Flyable, Swimmable {
    @Override public void fly() { System.out.println("Duck flying"); }
    @Override public void swim() { System.out.println("Duck swimming"); }

    // Must override when two interfaces have conflicting defaults
    @Override
    public String getType() {
        return Flyable.super.getType() + " & " + Swimmable.super.getType();
    }
}
```

### Interface vs Abstract Class

| Feature | Interface | Abstract Class |
|---|---|---|
| Instantiation | ❌ Cannot instantiate | ❌ Cannot instantiate |
| Multiple inheritance | ✅ A class can implement many | ❌ A class can extend only one |
| Constructors | ❌ No constructors | ✅ Has constructors |
| Fields | Only `public static final` constants | Any fields (instance, static) |
| Methods | Abstract + default + static | Abstract + concrete |
| `extends`/`implements` | `implements` | `extends` |
| When to use | Define a capability/role (can-do) | Share common code among related classes (is-a) |

```java
// Abstract class: shared base for related things
abstract class Vehicle { int speed; void move() { ... } }

// Interface: capability that unrelated things can share
interface GPS { String getLocation(); }  // Car, Phone, Watch can all implement
```

### Functional Interface (Java 8+)
An interface with exactly **one abstract method**. Can be implemented with a lambda expression.

A Functional Interface in Java (introduced in Java 8) is an interface that contains exactly one abstract method.

It is mainly used to enable lambda expressions and functional programming in Java.

🔹 Definition

A functional interface:

Has only one abstract method
Can have multiple default and static methods
Can be annotated with @FunctionalInterface (optional but recommended)

```java
@FunctionalInterface  // optional but recommended — compiler enforces single method
public interface Predicate<T> {
    boolean test(T t);
    // Can have default and static methods — those don't count
}

// Using lambda instead of anonymous class:
Predicate<Integer> isEven = n -> n % 2 == 0;
System.out.println(isEven.test(4)); // true
```

**Built-in functional interfaces (java.util.function):**

| Interface | Method | Purpose |
|---|---|---|
| `Predicate<T>` | `boolean test(T t)` | Test a condition |
| `Function<T,R>` | `R apply(T t)` | Transform T to R |
| `Consumer<T>` | `void accept(T t)` | Consume/use T, return nothing |
| `Supplier<T>` | `T get()` | Provide/produce a T |
| `BiFunction<T,U,R>` | `R apply(T t, U u)` | Two inputs, one output |
| `UnaryOperator<T>` | `T apply(T t)` | Input and output same type |
| `BinaryOperator<T>` | `T apply(T t1, T t2)` | Two same-type inputs, same output |

---

## 7. Exception Handling

### Exception Hierarchy
```
Throwable
├── Error              (JVM errors — don't catch these)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception
    ├── RuntimeException (Unchecked — compiler doesn't force handling)
    │   ├── NullPointerException
    │   ├── ArrayIndexOutOfBoundsException
    │   ├── ClassCastException
    │   ├── IllegalArgumentException
    │   ├── IllegalStateException
    │   └── ArithmeticException
    └── Checked Exceptions (compiler forces try-catch or throws declaration)
        ├── IOException
        ├── SQLException
        ├── FileNotFoundException
        └── ClassNotFoundException
```

### Checked vs Unchecked Exceptions

**Checked exceptions** – Must be either caught with `try-catch` or declared with `throws`. Represent recoverable conditions (file not found, network error).

**Unchecked exceptions (RuntimeException)** – Don't need explicit handling. Represent programming errors (null pointer, array out of bounds).

**Error** – Serious JVM-level problems you generally cannot recover from. Don't catch `Error`.

### try-catch-finally
```java
try {
    // code that might throw
    FileReader fr = new FileReader("file.txt");
    int data = fr.read();
} catch (FileNotFoundException e) {
    // handle specific exception first
    System.out.println("File not found: " + e.getMessage());
} catch (IOException e) {
    // more general exception — must come after specific ones
    System.out.println("IO error: " + e.getMessage());
} catch (Exception e) {
    // most general — catches anything (rarely needed)
    e.printStackTrace();
} finally {
    // ALWAYS runs, whether exception thrown or not
    // Use for resource cleanup
    System.out.println("Cleanup done");
}
```

### Multi-catch (Java 7+)
```java
try {
    // ...
} catch (IOException | SQLException e) {
    System.out.println("IO or SQL error: " + e.getMessage());
}
```

### try-with-resources (Java 7+)
Automatically closes resources that implement `AutoCloseable`. The `finally` block for closing is generated by the compiler.

```java
// Old way — manual close in finally
FileReader fr = null;
try {
    fr = new FileReader("file.txt");
    // use fr
} finally {
    if (fr != null) fr.close();  // must remember to close
}

// New way — try-with-resources
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
    // fr and br are automatically closed — even if exception thrown
}
```

### throws Declaration
```java
// Method declares it might throw a checked exception — callers must handle it
public void readFile(String path) throws IOException, FileNotFoundException {
    FileReader fr = new FileReader(path);
    // ...
}
```

### throw (manually throw an exception)
```java
public void setAge(int age) {
    if (age < 0 || age > 150) {
        throw new IllegalArgumentException("Age must be between 0 and 150, got: " + age);
    }
    this.age = age;
}
```

### Custom Exception
```java
// Checked custom exception
public class InsufficientFundsException extends Exception {
    private double amount;

    public InsufficientFundsException(double amount) {
        super("Insufficient funds. Need: " + amount);
        this.amount = amount;
    }

    public double getAmount() { return amount; }
}

// Unchecked custom exception
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(Long id) {
        super("User not found with id: " + id);
    }
}

// Usage
public void withdraw(double amount) throws InsufficientFundsException {
    if (balance < amount) {
        throw new InsufficientFundsException(amount - balance);
    }
    balance -= amount;
}
```

### Exception Chaining
Preserves the original cause when wrapping exceptions:
```java
try {
    connectToDatabase();
} catch (SQLException e) {
    throw new RuntimeException("Failed to connect to DB", e); // e is the cause
}
// Later, e.getCause() returns the original SQLException
```

### Best Practices for Exception Handling
- Catch the **most specific** exception first, most general last
- **Never** swallow exceptions silently: `catch(Exception e) {}` — always log or rethrow
- Use **try-with-resources** for any `Closeable` resource
- Don't use exceptions for **flow control** — exceptions are expensive
- Always log the **full stack trace**: `log.error("Failed", e)` not just `e.getMessage()`
- Use **custom exceptions** to convey specific business meaning
- **Don't catch `Error`** — `OutOfMemoryError`, `StackOverflowError` are unrecoverable

---

## 8. String Handling

### String Immutability
`String` objects are **immutable** — once created, their value cannot be changed. Every "modification" operation creates a new String object.

```java
String s = "Hello";
s.concat(" World");   // creates new String, original unchanged
System.out.println(s); // still "Hello"

s = s.concat(" World"); // now s points to new object "Hello World"
```

**Why immutable?**
- Thread-safe (no synchronization needed for reading)
- Safe to use as HashMap keys (hashCode doesn't change)
- String pool optimization (same literal can be shared)

### String Pool
String literals are stored in a special area called the **String Pool** (part of the heap). The same literal is reused rather than creating a new object each time.

```java
String a = "hello";        // stored in String pool
String b = "hello";        // reuses same pool object
System.out.println(a == b);          // true (same reference)

String c = new String("hello");     // explicitly creates new heap object
System.out.println(a == c);         // false (different objects)
System.out.println(a.equals(c));    // true (same content)

String d = c.intern();              // intern() adds to pool or returns existing
System.out.println(a == d);         // true
```

### Key String Methods
```java
String s = "  Hello World  ";

// Basic info
s.length()                          // 15
s.isEmpty()                         // false
s.isBlank()                         // false (Java 11+)
s.charAt(2)                         // 'H'

// Searching
s.indexOf("World")                  // 8
s.contains("Hello")                 // true
s.startsWith("  He")               // true
s.endsWith("d  ")                  // true

// Transformation
s.trim()                            // "Hello World" (removes leading/trailing spaces)
s.strip()                           // "Hello World" (Java 11+, Unicode-aware)
s.toLowerCase()                     // "  hello world  "
s.toUpperCase()                     // "  HELLO WORLD  "
s.replace("World", "Java")         // "  Hello Java  "
s.replaceAll("\\s+", "")           // "HelloWorld" (regex-based)

// Splitting / Joining
"a,b,c".split(",")                  // ["a", "b", "c"]
String.join("-", "a", "b", "c")    // "a-b-c"
String.join(", ", List.of("x","y")) // "x, y"

// Extraction
"Hello".substring(1)                // "ello"
"Hello".substring(1, 3)            // "el"

// Comparison
"abc".equals("abc")                 // true
"abc".equalsIgnoreCase("ABC")       // true
"abc".compareTo("abd")              // negative (a < d in dictionary order)

// Conversion
String.valueOf(42)                  // "42"
Integer.parseInt("42")              // 42
"42".toCharArray()                  // ['4','2']
```

### String.format() and printf
```java
String msg = String.format("Hello %s, you are %d years old", "Alice", 30);
// "Hello Alice, you are 30 years old"

System.out.printf("Pi = %.2f%n", Math.PI); // "Pi = 3.14"

// Java 15+ text blocks:
String json = """
        {
            "name": "Alice",
            "age": 30
        }
        """;
```

### StringBuilder vs StringBuffer

**`String`** – Immutable. Safe for use as keys. Creates new objects on modification.

**`StringBuilder`** – Mutable. NOT thread-safe. Use when building strings in single-threaded context. Much faster than String concatenation in loops.

**`StringBuffer`** – Mutable. Thread-safe (synchronized methods). Use only when multiple threads access the same builder.

```java
// BAD: String concatenation in a loop creates N+1 objects
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;  // creates new String each iteration
}

// GOOD: StringBuilder — only one mutable object
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String result = sb.toString();

// StringBuilder methods:
sb.append(" World")          // add to end
sb.insert(5, " Beautiful")  // insert at index
sb.delete(5, 15)             // remove range
sb.reverse()                 // reverse content
sb.replace(0, 5, "Hi")      // replace range
sb.length()                  // current length
sb.charAt(0)                 // get char at index
```

### String Comparison — The Rule
```
Always use .equals() to compare String content.
Never use == for Strings (unless you explicitly want reference equality).
```

---

## 9. Collections Framework

### Overview — The Collection Hierarchy
```
Iterable
└── Collection
    ├── List (ordered, allows duplicates)
    │   ├── ArrayList
    │   ├── LinkedList
    │   └── Vector (legacy, synchronized)
    ├── Set (no duplicates)
    │   ├── HashSet (unordered)
    │   ├── LinkedHashSet (insertion order)
    │   └── TreeSet (sorted)
    └── Queue (FIFO)
        ├── LinkedList
        ├── PriorityQueue (sorted by priority)
        └── ArrayDeque

Map (key-value pairs, not a Collection)
├── HashMap (unordered)
├── LinkedHashMap (insertion order)
├── TreeMap (sorted by key)
├── Hashtable (legacy, synchronized)
└── ConcurrentHashMap (thread-safe)
```

### List

#### ArrayList
Backed by a dynamic array. Fast random access (O(1)), slow insertion/deletion in middle (O(n)).

```java
List<String> list = new ArrayList<>();
list.add("Java");
list.add("Python");
list.add(0, "C++");       // insert at index (shifts elements right)
list.get(1);              // "Java" — O(1) random access
list.remove(0);           // remove by index
list.remove("Python");    // remove by value
list.size();              // 1
list.contains("Java");    // true
list.indexOf("Java");     // 0

// Iterate
for (String s : list) { System.out.println(s); }
list.forEach(System.out::println);

// Sort
Collections.sort(list);
list.sort(Comparator.naturalOrder());
list.sort(Comparator.reverseOrder());

// Convert to array
String[] arr = list.toArray(new String[0]);
// Array to list (fixed-size)
List<String> fixed = Arrays.asList("a", "b", "c");
// Array to list (modifiable)
List<String> mutable = new ArrayList<>(Arrays.asList("a","b","c"));
```

#### LinkedList
Backed by a doubly-linked list. Fast insertion/deletion at ends (O(1)), slow random access (O(n)). Implements both `List` and `Deque`.

```java
LinkedList<String> ll = new LinkedList<>();
ll.addFirst("A");  // add to front
ll.addLast("C");   // add to end
ll.add("B");
ll.getFirst();     // peek at front
ll.getLast();      // peek at end
ll.removeFirst();  // remove and return front
ll.removeLast();   // remove and return end

// Use as Stack (LIFO):
ll.push("X");  // same as addFirst
ll.pop();      // same as removeFirst

// Use as Queue (FIFO):
ll.offer("Y"); // same as addLast
ll.poll();     // same as removeFirst
```

#### ArrayList vs LinkedList

| Operation | ArrayList | LinkedList |
|---|---|---|
| `get(i)` | O(1) ✅ | O(n) ❌ |
| `add(end)` | O(1) amortized | O(1) |
| `add(middle)` | O(n) ❌ | O(1) after reaching node |
| `remove(middle)` | O(n) | O(1) after reaching node |
| Memory | Less (contiguous array) | More (node + 2 pointers) |
| **Use when** | Random access, iteration | Frequent insert/delete at ends |

### Set

#### HashSet
No duplicates. No guaranteed order. O(1) average for add/remove/contains. Based on `HashMap` internally.

```java
Set<String> set = new HashSet<>();
set.add("A");
set.add("B");
set.add("A");   // duplicate — ignored silently
System.out.println(set.size()); // 2
set.contains("A"); // true
set.remove("B");

// Set operations:
Set<Integer> s1 = new HashSet<>(Arrays.asList(1, 2, 3, 4));
Set<Integer> s2 = new HashSet<>(Arrays.asList(3, 4, 5, 6));

// Union
Set<Integer> union = new HashSet<>(s1);
union.addAll(s2);  // {1,2,3,4,5,6}

// Intersection
Set<Integer> intersection = new HashSet<>(s1);
intersection.retainAll(s2);  // {3,4}

// Difference
Set<Integer> diff = new HashSet<>(s1);
diff.removeAll(s2);  // {1,2}
```

#### LinkedHashSet
Same as HashSet but maintains **insertion order**.

#### TreeSet
Sorted in natural order (or by Comparator). O(log n) for operations. Based on Red-Black tree.

```java
TreeSet<Integer> ts = new TreeSet<>();
ts.add(5); ts.add(1); ts.add(3);
System.out.println(ts); // [1, 3, 5] — sorted

ts.first();           // 1
ts.last();            // 5
ts.floor(4);          // 3 (largest element ≤ 4)
ts.ceiling(2);        // 3 (smallest element ≥ 2)
ts.headSet(4);        // [1, 3] (elements < 4)
ts.tailSet(3);        // [3, 5] (elements ≥ 3)
ts.subSet(1, 4);      // [1, 3] (elements from 1 inclusive to 4 exclusive)
```

### Map

#### HashMap
Key-value pairs. No duplicate keys. No ordering. O(1) average for get/put/remove.

```java
Map<String, Integer> map = new HashMap<>();
map.put("Alice", 30);
map.put("Bob", 25);
map.put("Alice", 31);   // overwrites existing key

map.get("Alice");       // 31
map.getOrDefault("Unknown", 0);  // 0 (key doesn't exist)
map.containsKey("Bob"); // true
map.containsValue(25);  // true
map.remove("Bob");
map.size();             // 1

// Iterate
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + " = " + entry.getValue());
}
map.forEach((k, v) -> System.out.println(k + " = " + v));

// Useful Java 8+ Map methods:
map.putIfAbsent("Charlie", 28);        // only puts if key not present
map.computeIfAbsent("Dave", k -> 0);  // computes value if key absent
map.merge("Alice", 1, Integer::sum);   // Alice = 31 + 1 = 32
map.getOrDefault("Missing", -1);       // -1

// Word count pattern:
String[] words = {"apple","banana","apple","cherry","banana","apple"};
Map<String, Integer> count = new HashMap<>();
for (String w : words) {
    count.merge(w, 1, Integer::sum);
    // or: count.put(w, count.getOrDefault(w, 0) + 1);
}
```

#### LinkedHashMap
Maintains **insertion order** of entries.

#### TreeMap
Sorted by key (natural order or Comparator). O(log n).

```java
TreeMap<String, Integer> tm = new TreeMap<>();
tm.put("Banana", 2); tm.put("Apple", 1); tm.put("Cherry", 3);
System.out.println(tm); // {Apple=1, Banana=2, Cherry=3} — sorted by key

tm.firstKey();    // "Apple"
tm.lastKey();     // "Cherry"
tm.floorKey("B"); // "Banana" (largest key ≤ "B")
tm.headMap("C");  // {Apple=1, Banana=2}
```

### Queue & Deque

#### PriorityQueue
Elements are retrieved in **priority order** (min-heap by default — smallest first).

```java
// Min-heap (default)
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(5); pq.offer(1); pq.offer(3);
pq.peek();   // 1 (doesn't remove)
pq.poll();   // 1 (removes and returns smallest)
pq.poll();   // 3

// Max-heap
PriorityQueue<Integer> maxPQ = new PriorityQueue<>(Comparator.reverseOrder());

// Custom priority (by String length):
PriorityQueue<String> strPQ = new PriorityQueue<>(Comparator.comparingInt(String::length));
```

#### ArrayDeque
Double-ended queue. Can be used as Stack or Queue. Faster than `LinkedList` for both.

```java
ArrayDeque<String> deque = new ArrayDeque<>();
// As Stack (LIFO):
deque.push("A");    // addFirst
deque.push("B");
deque.pop();        // removes "B" (LIFO)

// As Queue (FIFO):
deque.offer("A");   // addLast
deque.offer("B");
deque.poll();       // removes "A" (FIFO)
```

### Collections Utility Class
```java
List<Integer> list = new ArrayList<>(Arrays.asList(3,1,4,1,5,9));

Collections.sort(list);                          // sort ascending
Collections.sort(list, Comparator.reverseOrder()); // sort descending
Collections.reverse(list);                       // reverse order
Collections.shuffle(list);                       // random shuffle
Collections.max(list);                           // 9
Collections.min(list);                           // 1
Collections.frequency(list, 1);                 // count occurrences of 1
Collections.unmodifiableList(list);             // read-only view
Collections.synchronizedList(list);             // thread-safe wrapper (prefer CopyOnWriteArrayList)
```

### Immutable Collections (Java 9+)
```java
List<String> immutable = List.of("A", "B", "C");     // cannot add/remove
Set<Integer> immutableSet = Set.of(1, 2, 3);
Map<String, Integer> immutableMap = Map.of("a", 1, "b", 2);
// All throw UnsupportedOperationException if you try to modify
```

### Comparator & Comparable

**`Comparable<T>`** – Natural ordering defined inside the class:
```java
public class Student implements Comparable<Student> {
    String name;
    int gpa;

    @Override
    public int compareTo(Student other) {
        return Double.compare(this.gpa, other.gpa); // sort by GPA ascending
    }
}
Collections.sort(students); // uses compareTo
```

**`Comparator<T>`** – External, flexible ordering:
```java
// Sort by name
Comparator<Student> byName = Comparator.comparing(s -> s.name);
// Sort by GPA descending, then name ascending
Comparator<Student> byGpaDesc = Comparator
    .comparingDouble(Student::getGpa).reversed()
    .thenComparing(Student::getName);

students.sort(byGpaDesc);
```

---

## 10. Generics

### What are Generics?
Generics allow classes, interfaces, and methods to work with any type while providing compile-time type safety. Without generics, you'd use `Object` and need casting everywhere.

```java
// Without generics — unsafe
List list = new ArrayList();
list.add("hello");
list.add(42);
String s = (String) list.get(1); // ClassCastException at runtime

// With generics — safe
List<String> list = new ArrayList<>();
list.add("hello");
list.add(42);    // compile error — caught at compile time
String s = list.get(0); // no cast needed
```

### Generic Class
```java
public class Box<T> {   // T is a type parameter (placeholder)
    private T value;

    public Box(T value) { this.value = value; }
    public T getValue() { return value; }

    @Override
    public String toString() { return "Box[" + value + "]"; }
}

Box<String> strBox = new Box<>("Hello");
Box<Integer> intBox = new Box<>(42);

String s = strBox.getValue();  // no cast needed
int i = intBox.getValue();
```

### Generic Method
```java
public class Utils {
    // Method has its own type parameter <T>
    public static <T> T findFirst(List<T> list, Predicate<T> condition) {
        for (T item : list) {
            if (condition.test(item)) return item;
        }
        return null;
    }

    // Swap two elements in an array
    public static <T> void swap(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

String first = Utils.findFirst(List.of("A","BB","CCC"), s -> s.length() > 1); // "BB"
```

### Bounded Type Parameters

**Upper bound (`extends`)** — T must be Number or a subclass of Number:
```java
public static <T extends Number> double sum(List<T> list) {
    double total = 0;
    for (T item : list) {
        total += item.doubleValue();  // can call Number's methods
    }
    return total;
}
sum(List.of(1, 2, 3));         // works with Integer
sum(List.of(1.5, 2.5, 3.5));  // works with Double
```

**Multiple bounds:**
```java
public <T extends Comparable<T> & Cloneable> T findMax(List<T> list) { ... }
```

### Wildcards

**`?` (unbounded wildcard)** — Any type:
```java
public void printList(List<?> list) {
    for (Object o : list) System.out.println(o);
}
printList(List.of("a","b")); // works with any List
```

**`? extends T` (upper-bounded wildcard)** — T or any subtype of T. Use when you're **reading** from the collection (Producer):
```java
public double sumAll(List<? extends Number> list) {
    // Can read items as Number, but can't add to the list
    return list.stream().mapToDouble(Number::doubleValue).sum();
}
sumAll(List.of(1, 2, 3));    // Integer extends Number
sumAll(List.of(1.1, 2.2));   // Double extends Number
```

**`? super T` (lower-bounded wildcard)** — T or any supertype of T. Use when you're **writing** to the collection (Consumer):
```java
public void addNumbers(List<? super Integer> list) {
    list.add(1);  // can add Integers
    list.add(2);
    // Can't reliably read typed items (gets Object)
}
addNumbers(new ArrayList<Integer>());  // works
addNumbers(new ArrayList<Number>());   // works (Number is super of Integer)
addNumbers(new ArrayList<Object>());   // works
```

**PECS Rule — Producer Extends, Consumer Super:**
- If the collection produces values for you to read → use `? extends T`
- If you're putting/consuming values into the collection → use `? super T`

### Type Erasure
At compile time, Java checks generic types for safety. At runtime, all generic type information is **erased** and replaced with `Object` (or bounds). This is why you can't do `new T()` or `instanceof List<String>` at runtime.

```java
List<String> strList = new ArrayList<>();
List<Integer> intList = new ArrayList<>();
System.out.println(strList.getClass() == intList.getClass()); // true! Both are ArrayList
```

---

## 11. Java 8+ Features

### Lambda Expressions
A concise way to implement functional interfaces (interfaces with one abstract method). Eliminates anonymous class boilerplate.

```java
// Anonymous class (old way):
Runnable r = new Runnable() {
    @Override
    public void run() { System.out.println("Running"); }
};

// Lambda (new way):
Runnable r = () -> System.out.println("Running");

// Various forms:
() -> System.out.println("no params")
x -> x * x                       // single param, expression body
(x, y) -> x + y                  // two params
(int x, int y) -> { return x + y; }  // explicit types, block body

// Comparator example:
List<String> names = Arrays.asList("Charlie", "Alice", "Bob");
names.sort((a, b) -> a.compareTo(b));          // old comparator lambda
names.sort(Comparator.naturalOrder());          // cleaner
names.sort(String::compareTo);                 // method reference
```

### Method References
Shorthand for lambdas that call existing methods:

```java
// Lambda → Method Reference
// instance::method — call method on a specific instance
String prefix = "Hello, ";
Function<String, String> greeter = name -> prefix.concat(name);
Function<String, String> greeter2 = prefix::concat;

// ClassName::staticMethod — call a static method
Function<String, Integer> parser = s -> Integer.parseInt(s);
Function<String, Integer> parser2 = Integer::parseInt;

// ClassName::instanceMethod — call method on parameter
Function<String, String> upper = s -> s.toUpperCase();
Function<String, String> upper2 = String::toUpperCase;

// ClassName::new — constructor reference
Supplier<ArrayList<String>> listMaker = () -> new ArrayList<>();
Supplier<ArrayList<String>> listMaker2 = ArrayList::new;

// Usage:
List<String> names = List.of("Alice","Bob","Charlie");
names.stream()
     .map(String::toUpperCase)  // method reference
     .forEach(System.out::println);
```

### Stream API
Streams allow you to process collections declaratively (what to do, not how). Operations are chained and executed lazily.

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Anna", "Brian");

// Example: Get sorted names starting with 'A', uppercased
List<String> result = names.stream()
    .filter(name -> name.startsWith("A"))    // intermediate: filter
    .map(String::toUpperCase)                 // intermediate: transform
    .sorted()                                 // intermediate: sort
    .collect(Collectors.toList());            // terminal: collect to List
// Result: ["ALICE", "ANNA"]
```

**Intermediate operations (lazy — don't execute until terminal is called):**
```java
stream.filter(x -> x > 0)          // keep elements matching predicate
stream.map(x -> x * 2)             // transform each element
stream.flatMap(list -> list.stream()) // flatten nested streams
stream.distinct()                   // remove duplicates
stream.sorted()                     // sort (natural order)
stream.sorted(Comparator.reverseOrder()) // sort with comparator
stream.limit(10)                    // take first 10 elements
stream.skip(5)                      // skip first 5 elements
stream.peek(x -> System.out.println(x)) // for debugging/side effects
```

**Terminal operations (trigger execution):**
```java
stream.collect(Collectors.toList())   // collect to List
stream.collect(Collectors.toSet())    // collect to Set
stream.collect(Collectors.joining(", ")) // join strings
stream.count()                        // count elements
stream.findFirst()                    // Optional<T> — first element
stream.findAny()                      // Optional<T> — any element (parallel)
stream.anyMatch(x -> x > 0)          // true if any element matches
stream.allMatch(x -> x > 0)          // true if ALL elements match
stream.noneMatch(x -> x < 0)         // true if NO elements match
stream.min(Comparator.naturalOrder()) // Optional<T> minimum
stream.max(Comparator.naturalOrder()) // Optional<T> maximum
stream.forEach(System.out::println)   // consume each element
stream.reduce(0, Integer::sum)        // reduce to single value
stream.toArray()                      // convert to array
```

**Collectors:**
```java
// Group students by their grade
Map<String, List<Student>> byGrade = students.stream()
    .collect(Collectors.groupingBy(Student::getGrade));

// Count by grade
Map<String, Long> countByGrade = students.stream()
    .collect(Collectors.groupingBy(Student::getGrade, Collectors.counting()));

// Average GPA by grade
Map<String, Double> avgGpa = students.stream()
    .collect(Collectors.groupingBy(Student::getGrade,
        Collectors.averagingDouble(Student::getGpa)));

// Partition into two groups (pass/fail)
Map<Boolean, List<Student>> partitioned = students.stream()
    .collect(Collectors.partitioningBy(s -> s.getGpa() >= 2.0));

// Joining strings
String joined = names.stream().collect(Collectors.joining(", ", "[", "]"));
// "[Alice, Bob, Charlie]"

// Summarizing stats
IntSummaryStatistics stats = numbers.stream()
    .collect(Collectors.summarizingInt(Integer::intValue));
stats.getMin(); stats.getMax(); stats.getAverage(); stats.getSum();

// To Map
Map<String, Integer> nameLength = names.stream()
    .collect(Collectors.toMap(name -> name, String::length));
```

**Numeric Streams:**
```java
IntStream.range(0, 5).forEach(System.out::println);   // 0,1,2,3,4
IntStream.rangeClosed(1, 5).sum();                    // 15
IntStream.of(1,2,3,4,5).average().getAsDouble();      // 3.0

// Convert Stream<Integer> to IntStream:
List<Integer> nums = List.of(1,2,3,4,5);
int sum = nums.stream().mapToInt(Integer::intValue).sum();
```

**Parallel Streams:**
```java
// Process in parallel using multiple threads (ForkJoinPool)
long count = largeList.parallelStream()
    .filter(s -> s.startsWith("A"))
    .count();
// Use for CPU-intensive operations on large datasets
// Avoid for small lists or IO-bound operations — overhead not worth it
```

### Optional
A container object that may or may not contain a non-null value. Eliminates NullPointerException.

```java
// Creating Optional:
Optional<String> empty = Optional.empty();
Optional<String> of = Optional.of("Hello");       // throws NPE if null
Optional<String> nullable = Optional.ofNullable(null); // null-safe

// Using Optional:
String value = optional.get();                    // throws if empty — avoid
String value = optional.orElse("default");        // return default if empty
String value = optional.orElseGet(() -> computeDefault()); // lazy default
String value = optional.orElseThrow(() -> new RuntimeException("Missing")); // throw if empty

optional.isPresent()                              // true if has value
optional.isEmpty()                                // true if empty (Java 11+)
optional.ifPresent(v -> System.out.println(v))   // run action if present
optional.ifPresentOrElse(                         // (Java 9+)
    v -> System.out.println(v),
    () -> System.out.println("empty")
);

// Chaining (the right way to use Optional):
Optional<String> result = Optional.ofNullable(user)
    .map(User::getAddress)          // null-safe transformation
    .map(Address::getCity)
    .filter(city -> city.length() > 3)
    .map(String::toUpperCase);

// ✅ Return Optional from methods that may not return a value
// ❌ Don't use Optional as method parameter or field type
// ❌ Don't use Optional with collections (use empty collection instead)
```

### Default & Static Interface Methods (Java 8)
```java
public interface Collection<E> {
    // Abstract method — must implement
    boolean add(E e);

    // Default method — optional to override, provides backward compatibility
    default boolean addAll(Collection<? extends E> c) {
        boolean changed = false;
        for (E e : c) if (add(e)) changed = true;
        return changed;
    }

    // Static method — called on the interface, not on instances
    static <E> List<E> emptyList() { return Collections.emptyList(); }
}
```

### Date & Time API (java.time — Java 8+)
The new API is immutable, thread-safe, and much better than the old `Date`/`Calendar`.

```java
// Current date/time
LocalDate today = LocalDate.now();           // 2024-01-15 (date only)
LocalTime now = LocalTime.now();             // 10:30:45.123 (time only)
LocalDateTime dateTime = LocalDateTime.now(); // date + time (no timezone)
ZonedDateTime zoned = ZonedDateTime.now();   // with timezone

// Creating specific dates
LocalDate birthday = LocalDate.of(1990, 3, 15);
LocalDate birthday2 = LocalDate.of(1990, Month.MARCH, 15);
LocalTime morning = LocalTime.of(9, 30, 0);
LocalDateTime appointment = LocalDateTime.of(2024, 3, 15, 14, 30);

// Manipulation (returns new instance — immutable)
LocalDate nextWeek = today.plusDays(7);
LocalDate lastMonth = today.minusMonths(1);
LocalDate nextYear = today.plusYears(1);

// Comparison
today.isBefore(nextWeek);    // true
today.isAfter(lastMonth);    // true
today.isEqual(LocalDate.now()); // true

// Extracting info
today.getYear();             // 2024
today.getMonth();            // JANUARY
today.getDayOfMonth();       // 15
today.getDayOfWeek();        // MONDAY

// Formatting / Parsing
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd/MM/yyyy");
String formatted = today.format(fmt);         // "15/01/2024"
LocalDate parsed = LocalDate.parse("15/01/2024", fmt);

// Duration and Period
Duration duration = Duration.between(startTime, endTime); // for time
Period period = Period.between(startDate, endDate);        // for dates
long days = duration.toDays();
int months = period.getMonths();

// Instant (machine time, for timestamps)
Instant now2 = Instant.now();
Instant past = now2.minusSeconds(3600); // 1 hour ago
```

---

## 12. Multithreading & Concurrency

### Thread Basics

**What is a Thread?**
A thread is the smallest unit of execution. Java supports multithreading, allowing multiple threads to run concurrently within a single process, sharing memory.

### Creating Threads

**Method 1: Extend Thread**
```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
}
MyThread t = new MyThread();
t.start();  // starts the thread — calls run() in new thread
// t.run()  // would run in the CURRENT thread, not a new one
```

**Method 2: Implement Runnable (preferred)**
```java
Runnable task = () -> System.out.println("Task running");
Thread t = new Thread(task);
t.start();

// Or directly:
new Thread(() -> {
    System.out.println("Quick task");
}).start();
```

**Method 3: Callable + Future (returns a result)**
```java
Callable<Integer> task = () -> {
    Thread.sleep(1000);
    return 42;
};

ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Integer> future = executor.submit(task);

// Main thread can do other work here...

Integer result = future.get();        // blocks until result is ready
Integer result2 = future.get(5, TimeUnit.SECONDS); // timeout version
future.isDone();                      // non-blocking check
future.cancel(true);                  // cancel the task
executor.shutdown();
```

### Thread Lifecycle
```
NEW → RUNNABLE → RUNNING → (BLOCKED/WAITING/TIMED_WAITING) → TERMINATED
```
- **NEW** – Thread created but not started
- **RUNNABLE** – Ready to run (in queue for CPU)
- **RUNNING** – Actually executing on CPU
- **BLOCKED** – Waiting for a monitor lock
- **WAITING** – Waiting indefinitely for another thread (wait(), join())
- **TIMED_WAITING** – Waiting with timeout (sleep(), wait(timeout))
- **TERMINATED** – Finished execution

### Thread Methods
```java
Thread.currentThread().getName()     // current thread's name
Thread.currentThread().getId()       // unique ID

t.start()     // start new thread
t.join()      // wait for this thread to finish before continuing
t.join(2000)  // wait at most 2000ms
Thread.sleep(1000)  // pause current thread for 1 second (throws InterruptedException)
t.interrupt() // request thread to stop (sets interrupt flag)
Thread.currentThread().isInterrupted() // check if interrupted
t.setDaemon(true) // daemon threads don't prevent JVM exit (e.g., background GC)
t.setPriority(Thread.MAX_PRIORITY) // 1-10, hint to scheduler
```

### Synchronization
When multiple threads access shared mutable data, you can get **race conditions** — the result depends on thread scheduling order.

**Race condition example:**
```java
class Counter {
    int count = 0;
    void increment() { count++; }  // NOT atomic: read, add 1, write (3 steps)
}
// Two threads calling increment() 1000 times each might give count < 2000
```

**`synchronized` method:**
```java
class SafeCounter {
    int count = 0;

    synchronized void increment() {  // only one thread at a time
        count++;
    }

    synchronized int getCount() {
        return count;
    }
}
```

**`synchronized` block (more fine-grained):**
```java
class SafeCounter {
    int count = 0;
    final Object lock = new Object();

    void increment() {
        synchronized(lock) {   // lock only the critical section
            count++;
        }
        // rest of method runs without synchronization
    }
}
```

**`volatile` keyword:**
Ensures that a variable's value is always read from/written to **main memory**, not a thread's local cache. Use for flags and simple single-variable state. Does NOT make compound operations (like `count++`) atomic.


In Java, volatile ensures two key things:

Visibility
Changes made by one thread are immediately visible to other threads
No thread-local caching → always read/write from main memory
Happens-before guarantee
A write to a volatile variable happens-before every subsequent read of that variable

```java
class Worker implements Runnable {
    volatile boolean running = true;  // visible to all threads immediately

    @Override
    public void run() {
        while (running) {
            // do work
        }
    }

    public void stop() {
        running = false;  // seen by worker thread immediately
    }
}
```

### java.util.concurrent

#### ExecutorService & Thread Pools
Creating threads is expensive. Thread pools reuse threads for multiple tasks.

```java
// Fixed pool — always exactly N threads
ExecutorService pool = Executors.newFixedThreadPool(4);

// Single thread — tasks execute sequentially
ExecutorService single = Executors.newSingleThreadExecutor();

// Cached pool — creates threads as needed, reuses idle ones
ExecutorService cached = Executors.newCachedThreadPool();

// Scheduled pool — for periodic/delayed tasks
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(2);

// Submit tasks:
pool.execute(() -> System.out.println("Fire and forget"));
Future<String> future = pool.submit(() -> "result");

// Always shut down properly:
pool.shutdown();                          // stop accepting new tasks, finish existing
pool.awaitTermination(30, TimeUnit.SECONDS); // wait for completion
pool.shutdownNow();                       // interrupt running tasks
```

#### Atomic Classes
Provide thread-safe operations without synchronization:

```java
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();  // atomic increment, returns new value
count.getAndIncrement();  // atomic increment, returns old value
count.addAndGet(5);       // atomic add
count.compareAndSet(10, 20); // if value is 10, set to 20 (CAS)
count.get();              // read current value

AtomicBoolean flag = new AtomicBoolean(false);
flag.getAndSet(true);     // set to true, return old value

AtomicReference<String> ref = new AtomicReference<>("hello");
ref.compareAndSet("hello", "world"); // atomic update
```

#### Locks (java.util.concurrent.locks)
More flexible than `synchronized`:

```java
ReentrantLock lock = new ReentrantLock();

// Basic lock/unlock (must unlock in finally to avoid deadlock):
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}

// Try lock (non-blocking):
if (lock.tryLock()) {
    try { /* got the lock */ }
    finally { lock.unlock(); }
} else {
    // couldn't get lock — do something else
}

// Timed lock:
if (lock.tryLock(100, TimeUnit.MILLISECONDS)) { ... }

// ReentrantReadWriteLock — multiple readers OR one writer:
ReadWriteLock rwLock = new ReentrantReadWriteLock();
rwLock.readLock().lock();   // many threads can hold read lock simultaneously
rwLock.writeLock().lock();  // only one thread at a time
```

#### CountDownLatch
One or more threads wait until a set of operations completes:

```java
CountDownLatch latch = new CountDownLatch(3); // countdown from 3

// Worker threads:
new Thread(() -> {
    doWork();
    latch.countDown();  // decrement counter
}).start();

// Main thread waits until count reaches 0:
latch.await();          // blocks until count = 0
latch.await(10, TimeUnit.SECONDS); // with timeout
```

#### CyclicBarrier
All threads wait at a barrier point until ALL have arrived:

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier"); // runs when all arrive
});

Runnable task = () -> {
    doFirstPhase();
    barrier.await();  // wait for others
    doSecondPhase();  // all threads start second phase together
};
```

#### Semaphore
Limits the number of threads accessing a resource simultaneously:

```java
Semaphore semaphore = new Semaphore(3); // allow max 3 threads concurrently

semaphore.acquire(); // get a permit (blocks if none available)
try {
    accessDatabase();
} finally {
    semaphore.release(); // return permit
}
```

#### Concurrent Collections
Thread-safe collections designed for concurrent access:

```java
// ConcurrentHashMap — thread-safe HashMap (lock per segment, not whole map)
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.putIfAbsent("key", 1);
map.computeIfAbsent("key", k -> expensiveCompute(k));

// CopyOnWriteArrayList — thread-safe List (creates copy on write)
// Fast reads, slow writes. Good for frequently-read, rarely-modified lists.
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("A");  // creates new internal array

// BlockingQueue — thread-safe queue with blocking operations
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);
queue.put(task);     // blocks if queue is full (producer)
Task t = queue.take(); // blocks if queue is empty (consumer)
```

### CompletableFuture (Java 8+)
Powerful async programming:

```java
// Async computation
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return fetchFromDatabase();  // runs in ForkJoinPool thread
});

// Chain transformations
CompletableFuture<String> result = future
    .thenApply(data -> data.toUpperCase())      // transform (sync)
    .thenApplyAsync(data -> process(data))       // transform (async)
    .thenCompose(data -> fetchMore(data))        // flat-map (returns CF)
    .exceptionally(ex -> "default value");       // handle exception

// Combine multiple futures
CompletableFuture<String> cf1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> cf2 = CompletableFuture.supplyAsync(() -> " World");

CompletableFuture<String> combined = cf1.thenCombine(cf2, (a, b) -> a + b);
combined.get(); // "Hello World"

// Wait for all:
CompletableFuture.allOf(cf1, cf2, cf3).join();

// Wait for first:
CompletableFuture.anyOf(cf1, cf2).get();
```

### Common Concurrency Problems

**Deadlock** – Thread A holds lock X and waits for lock Y. Thread B holds lock Y and waits for lock X. Both wait forever.
```java
// Prevention: always acquire locks in the same order across all threads
// Detection: thread dump shows threads in BLOCKED state
```

**Livelock** – Threads keep responding to each other's actions without making progress. Like two people dodging each other in a hallway.

**Starvation** – A thread is perpetually denied access to a resource because other (higher priority) threads keep taking it.

**Race Condition** – The outcome depends on the timing/order of thread execution. Fix with synchronization.

---

## 13. Java Memory Model & JVM Internals

### JVM Memory Areas

**Heap** – Where all objects are allocated. Shared across all threads. Divided into:
- **Young Generation** – Newly created objects go here. Divided into Eden and two Survivor spaces.
- **Old Generation (Tenured)** – Objects that survive multiple GC cycles are promoted here.
- **Metaspace** (Java 8+, replaced PermGen) – Stores class metadata (class structure, method bytecode).

**Stack** – Each thread has its own stack. Stores method call frames (local variables, parameters, return addresses). Grows/shrinks with method calls. `StackOverflowError` happens when it runs out of space (usually due to infinite recursion).

**Method Area (Metaspace)** – Stores class-level data: class structure, static variables, method code.

**Program Counter (PC) Register** – Tracks the current instruction being executed for each thread.

**Native Method Stack** – For native (non-Java) method execution.

### Garbage Collection (GC)
Java manages memory automatically. The GC identifies and removes objects that are no longer reachable.

**Object reachability:** An object is garbage-collectible when no live thread can reach it through any chain of references.

**GC Algorithms:**

**Minor GC** – Cleans Young Generation (Eden + Survivors). Frequent, fast.

**Major/Full GC** – Cleans Old Generation. Infrequent, slower (Stop-the-World pause).

**GC Types:**
- **Serial GC** – Single-threaded. Good for small apps.
- **Parallel GC** – Uses multiple threads for Young Gen collection. High throughput. Default for many JVMs.
- **G1 GC (Garbage First)** – Default since Java 9. Low-pause GC. Divides heap into regions.
- **ZGC / Shenandoah** – Very low pause times (sub-millisecond). For large heaps.

**GC Tuning flags:**
```
-Xms512m          # Initial heap size
-Xmx4g            # Maximum heap size
-XX:+UseG1GC      # Use G1 garbage collector
-XX:MaxGCPauseMillis=200  # Target max GC pause time
```

### Memory Leaks in Java
Java can still have memory leaks — objects are reachable (so GC won't collect them) but no longer needed.

Common causes:
- **Static collections that grow without bound:** `static List<Object> cache` that never clears
- **Listeners not removed:** Adding event listeners without removing them
- **Unclosed resources:** Database connections, streams (use try-with-resources)
- **ThreadLocal not cleaned:** ThreadLocal variables in thread pools
- **Inner class holding outer class reference:** Anonymous inner class keeps outer object alive

### Stack vs Heap

| | Stack | Heap |
|---|---|---|
| Stores | Primitive values, object references | Objects, arrays |
| Per thread | Yes (each thread has own stack) | No (shared) |
| Size | Fixed (small) | Dynamic (large) |
| Allocation | LIFO (method frame push/pop) | GC managed |
| Error | StackOverflowError | OutOfMemoryError |

```java
void method() {
    int x = 10;           // x stored in stack
    Person p = new Person(); // p reference in stack, Person object in HEAP
}  // when method returns, stack frame popped; p reference gone; object eligible for GC
```

### String Pool
String literals are stored in a special region of the heap (String Pool / String Intern Pool). When you write `"hello"`, Java checks the pool first. If the string already exists there, it reuses it. This is why `"hello" == "hello"` is `true`.

### ClassLoader
Responsible for loading `.class` files into the JVM at runtime.

**Three built-in ClassLoaders:**
1. **Bootstrap ClassLoader** – Loads core Java classes (`java.lang.*`, `java.util.*`)
2. **Extension ClassLoader** – Loads extension libraries
3. **Application ClassLoader** – Loads your application's classes (from classpath)

ClassLoaders use **parent delegation** — before loading a class, they ask the parent ClassLoader first. This ensures core Java classes can't be overridden.

---

## 14. File I/O & NIO

### Classic I/O (java.io)

**Reading a file:**
```java
// Buffered reading (efficient — reads in chunks)
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}

// Or with Files utility (Java 7+):
List<String> lines = Files.readAllLines(Path.of("file.txt"), StandardCharsets.UTF_8);
String content = Files.readString(Path.of("file.txt")); // Java 11+
```

**Writing a file:**
```java
try (BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"))) {
    bw.write("Hello World");
    bw.newLine();
    bw.write("Second line");
}

// With Files utility:
Files.writeString(Path.of("output.txt"), "Hello World", StandardCharsets.UTF_8);
Files.write(Path.of("output.txt"), lines); // write list of lines
```

**Binary files:**
```java
try (FileInputStream fis = new FileInputStream("image.png");
     FileOutputStream fos = new FileOutputStream("copy.png")) {
    byte[] buffer = new byte[4096];
    int bytesRead;
    while ((bytesRead = fis.read(buffer)) != -1) {
        fos.write(buffer, 0, bytesRead);
    }
}
```

### NIO.2 (java.nio.file — Java 7+)
Modern, cleaner API for file operations:

```java
Path path = Path.of("src", "main", "file.txt");  // platform-independent
Path absolute = path.toAbsolutePath();
Path parent = path.getParent();
String filename = path.getFileName().toString();

// File operations
Files.exists(path)
Files.isDirectory(path)
Files.createFile(path)
Files.createDirectory(path)
Files.createDirectories(path)  // creates parent dirs too
Files.delete(path)
Files.deleteIfExists(path)
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING)
Files.move(source, target, StandardCopyOption.REPLACE_EXISTING)
long size = Files.size(path)

// Walk directory tree:
Files.walk(Path.of("src"))
     .filter(p -> p.toString().endsWith(".java"))
     .forEach(System.out::println);

// List directory contents:
Files.list(Path.of("."))
     .filter(Files::isRegularFile)
     .forEach(System.out::println);
```

### Serialization
Converting an object to a byte stream (for saving to file or sending over network), and back:

```java
// Make class serializable:
public class User implements Serializable {
    private static final long serialVersionUID = 1L; // version control
    String name;
    transient String password; // transient = NOT serialized
    int age;
}

// Serialize (write to file):
try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("user.ser"))) {
    oos.writeObject(new User("Alice", "secret", 30));
}

// Deserialize (read from file):
try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("user.ser"))) {
    User user = (User) ois.readObject();
}
```

**`serialVersionUID`** – A version number used during deserialization to verify that the sender and receiver have compatible versions of a Serializable class. Always define it explicitly to avoid `InvalidClassException` when the class changes.

**`transient`** – Marks a field to be skipped during serialization (passwords, connection objects, cache fields).

---

## 15. Design Patterns in Java

### Creational Patterns

#### Singleton
Ensures only one instance of a class exists. Provides global access point.

```java
// Thread-safe Singleton using enum (best practice):
public enum DatabaseConnection {
    INSTANCE;

    private Connection connection;

    DatabaseConnection() {
        connection = createConnection();
    }

    public Connection getConnection() { return connection; }
}
// Usage: DatabaseConnection.INSTANCE.getConnection()

// Thread-safe Singleton using double-checked locking:
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {                    // first check (no lock)
            synchronized (Singleton.class) {
                if (instance == null) {            // second check (with lock)
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

#### Factory Method
Defines an interface for creating objects, but lets subclasses decide which class to instantiate:

```java
public interface Shape { void draw(); }
public class Circle implements Shape { public void draw() { System.out.println("Circle"); } }
public class Rectangle implements Shape { public void draw() { System.out.println("Rect"); } }

public class ShapeFactory {
    public static Shape create(String type) {
        return switch (type.toLowerCase()) {
            case "circle" -> new Circle();
            case "rectangle" -> new Rectangle();
            default -> throw new IllegalArgumentException("Unknown shape: " + type);
        };
    }
}

Shape s = ShapeFactory.create("circle");
s.draw(); // "Circle"
```

#### Builder
Constructs complex objects step by step. Avoids telescoping constructors.

```java
public class User {
    private final String name;      // required
    private final String email;     // required
    private final int age;
    private final String phone;

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
        this.age = builder.age;
        this.phone = builder.phone;
    }

    public static class Builder {
        private final String name;
        private final String email;
        private int age;
        private String phone;

        public Builder(String name, String email) {
            this.name = name;
            this.email = email;
        }

        public Builder age(int age) { this.age = age; return this; }
        public Builder phone(String phone) { this.phone = phone; return this; }
        public User build() { return new User(this); }
    }
}

// Usage — clean and readable:
User user = new User.Builder("Alice", "alice@example.com")
    .age(30)
    .phone("555-1234")
    .build();
```

#### Prototype
Creates new objects by copying (cloning) an existing object:

```java
public class Address implements Cloneable {
    String street, city;

    @Override
    public Address clone() {
        try {
            return (Address) super.clone(); // shallow copy
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}
```

### Structural Patterns

#### Decorator
Adds behavior to objects dynamically without modifying their class:

```java
interface Coffee { double getCost(); String getDescription(); }

class SimpleCoffee implements Coffee {
    public double getCost() { return 1.0; }
    public String getDescription() { return "Coffee"; }
}

abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    CoffeeDecorator(Coffee c) { this.coffee = c; }
}

class MilkDecorator extends CoffeeDecorator {
    MilkDecorator(Coffee c) { super(c); }
    public double getCost() { return coffee.getCost() + 0.5; }
    public String getDescription() { return coffee.getDescription() + ", Milk"; }
}

// Usage:
Coffee coffee = new MilkDecorator(new MilkDecorator(new SimpleCoffee()));
coffee.getCost();         // 2.0
coffee.getDescription();  // "Coffee, Milk, Milk"
```

#### Adapter
Allows incompatible interfaces to work together:

```java
// Existing (legacy) interface
interface OldPrinter { void printOld(String text); }

// New interface we want to use
interface NewPrinter { void print(String text); }

// Adapter makes OldPrinter look like NewPrinter
class PrinterAdapter implements NewPrinter {
    private OldPrinter oldPrinter;
    PrinterAdapter(OldPrinter op) { this.oldPrinter = op; }
    public void print(String text) { oldPrinter.printOld(text); }
}
```

#### Proxy
Provides a surrogate for another object to control access:

```java
interface Service { void doWork(); }

class RealService implements Service {
    public void doWork() { System.out.println("Doing real work"); }
}

class ServiceProxy implements Service {
    private Service real = new RealService();

    public void doWork() {
        System.out.println("Proxy: Logging before");
        if (checkPermission()) {
            real.doWork();
        }
        System.out.println("Proxy: Logging after");
    }
}
// Spring uses this for @Transactional, @Cacheable, @Async
```

### Behavioral Patterns

#### Strategy
Defines a family of algorithms, encapsulates each one, and makes them interchangeable:

```java
interface SortStrategy { void sort(int[] data); }
class BubbleSort implements SortStrategy { public void sort(int[] d) { /* bubble sort */ } }
class QuickSort implements SortStrategy { public void sort(int[] d) { /* quick sort */ } }

class Sorter {
    private SortStrategy strategy;

    Sorter(SortStrategy strategy) { this.strategy = strategy; }
    void setStrategy(SortStrategy strategy) { this.strategy = strategy; }
    void sort(int[] data) { strategy.sort(data); }
}

Sorter sorter = new Sorter(new QuickSort());
sorter.sort(data);
sorter.setStrategy(new BubbleSort()); // switch strategy at runtime
```

#### Observer
Defines a one-to-many dependency — when one object changes, all dependents are notified:

```java
interface Observer { void update(String event); }

class EventPublisher {
    private List<Observer> observers = new ArrayList<>();

    public void subscribe(Observer o) { observers.add(o); }
    public void unsubscribe(Observer o) { observers.remove(o); }

    public void notifyAll(String event) {
        observers.forEach(o -> o.update(event));
    }
}

// In Spring: ApplicationEventPublisher + @EventListener
```

#### Template Method
Defines the skeleton of an algorithm, deferring specific steps to subclasses:

```java
abstract class DataProcessor {
    // Template method — final so subclasses can't change the algorithm structure
    public final void process() {
        readData();    // step 1
        processData(); // step 2 — must override
        writeOutput(); // step 3 — may override
    }

    abstract void processData(); // must implement
    void readData() { System.out.println("Reading data"); } // default
    void writeOutput() { System.out.println("Writing output"); } // default
}

class CSVProcessor extends DataProcessor {
    @Override
    void processData() { System.out.println("Processing CSV"); }
}
```

---

## 16. Java 9–17+ Modern Features

### Java 9 — Modules (Project Jigsaw)
```java
// module-info.java
module com.myapp {
    requires java.sql;           // depend on this module
    requires com.google.gson;
    exports com.myapp.api;       // expose this package
    opens com.myapp.model to com.google.gson;  // allow reflection
}
```

### Java 9 — Collection Factory Methods
```java
List<String> list = List.of("A", "B", "C");         // immutable
Set<Integer> set = Set.of(1, 2, 3);                  // immutable
Map<String, Integer> map = Map.of("a", 1, "b", 2);  // immutable
Map<String, Integer> map2 = Map.ofEntries(
    Map.entry("key1", 1),
    Map.entry("key2", 2)
);
```

### Java 10 — Local Variable Type Inference
```java
var name = "Alice";                         // String
var list = new ArrayList<String>();          // ArrayList<String>
var map = Map.of("a", 1);                   // Map<String, Integer>
// Cannot use var for fields, parameters, or return types
```

### Java 11 — String Methods
```java
"  ".isBlank()                              // true
"Hello\nWorld\n".lines().count()           // 2 (Stream<String>)
"Hello".repeat(3)                          // "HelloHelloHello"
"  hello  ".strip()                        // "hello" (Unicode-aware trim)
"  hello  ".stripLeading()                 // "hello  "
"  hello  ".stripTrailing()               // "  hello"
```

### Java 14 — Records (preview, final in Java 16)
Records are immutable data classes. Auto-generate constructor, getters, `equals()`, `hashCode()`, `toString()`.

```java
public record Point(double x, double y) {
    // Compact canonical constructor (validation):
    Point {
        if (x < 0 || y < 0) throw new IllegalArgumentException("Negative coords");
    }

    // Add methods:
    public double distanceTo(Point other) {
        return Math.sqrt(Math.pow(x - other.x, 2) + Math.pow(y - other.y, 2));
    }
}

Point p = new Point(3.0, 4.0);
p.x();           // 3.0 (accessor — not getX())
p.y();           // 4.0
p.toString();    // "Point[x=3.0, y=4.0]"
new Point(3.0, 4.0).equals(new Point(3.0, 4.0)); // true
```

### Java 14 — Pattern Matching for instanceof
```java
// Old way:
if (obj instanceof String) {
    String s = (String) obj;  // explicit cast
    System.out.println(s.toUpperCase());
}

// New way (Java 16+ final):
if (obj instanceof String s) {  // s is already typed, no cast needed
    System.out.println(s.toUpperCase());
}

// In conditions:
if (obj instanceof String s && s.length() > 5) {
    System.out.println(s);
}
```

### Java 15 — Text Blocks
```java
String json = """
        {
            "name": "Alice",
            "age": 30
        }
        """;

String html = """
        <html>
            <body>
                <p>Hello World</p>
            </body>
        </html>
        """;
// Preserves formatting, no need for \n and \" escaping
```

### Java 17 — Sealed Classes
Restricts which classes can extend/implement a class:

```java
public sealed class Shape permits Circle, Rectangle, Triangle {
    abstract double area();
}

public final class Circle extends Shape {
    double radius;
    Circle(double r) { this.radius = r; }
    double area() { return Math.PI * radius * radius; }
}

public final class Rectangle extends Shape {
    double w, h;
    Rectangle(double w, double h) { this.w = w; this.h = h; }
    double area() { return w * h; }
}

// Exhaustive pattern matching with switch (Java 21+):
double area = switch (shape) {
    case Circle c -> Math.PI * c.radius * c.radius;
    case Rectangle r -> r.w * r.h;
    case Triangle t -> 0.5 * t.base * t.height;
    // No default needed — all cases covered
};
```

### Java 21 — Virtual Threads (Project Loom)
```java
// Traditional thread — OS-level, expensive to create
Thread.ofPlatform().start(() -> handleRequest());

// Virtual thread — JVM-level, very lightweight (millions possible)
Thread.ofVirtual().start(() -> handleRequest());

// With ExecutorService:
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> handleRequest());
}
// Perfect for I/O-bound concurrent applications
```

---

## 17. Best Practices & Common Pitfalls

### Code Quality

**Favor composition over inheritance:**
```java
// BAD: inheritance for code reuse when relationship isn't truly "is-a"
class Stack extends ArrayList { ... }  // Stack is NOT an ArrayList

// GOOD: composition
class Stack {
    private ArrayList list = new ArrayList();  // has-a relationship
    public void push(Object o) { list.add(o); }
    public Object pop() { return list.remove(list.size()-1); }
}
```

**Program to interfaces, not implementations:**
```java
// BAD:
ArrayList<String> list = new ArrayList<>();

// GOOD: can swap implementation without changing callers
List<String> list = new ArrayList<>();
Map<String, Integer> map = new HashMap<>();
```

**Use `final` for immutability:**
```java
// Immutable class:
public final class Money {
    private final BigDecimal amount;
    private final String currency;

    public Money(BigDecimal amount, String currency) {
        this.amount = Objects.requireNonNull(amount);
        this.currency = Objects.requireNonNull(currency);
    }
    // No setters — immutable after creation
    public Money add(Money other) {
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

**Avoid null — use Optional or empty collections:**
```java
// BAD: return null
public String findUserName(int id) {
    return null; // caller might forget null check
}

// GOOD: return Optional
public Optional<String> findUserName(int id) {
    return Optional.ofNullable(database.get(id));
}

// For collections: return empty, never null
public List<String> getNames() {
    return Collections.emptyList(); // never return null
}
```

**Use `Objects.requireNonNull` for validation:**
```java
public class Service {
    private final Repository repo;

    public Service(Repository repo) {
        this.repo = Objects.requireNonNull(repo, "repo must not be null");
    }
}
```

### Performance Pitfalls

**String concatenation in loops:**
```java
// BAD — O(n²) memory, creates n intermediate String objects
String result = "";
for (String s : list) result += s;

// GOOD — O(n) memory
StringBuilder sb = new StringBuilder();
for (String s : list) sb.append(s);
String result = sb.toString();
```

**Unnecessary boxing/unboxing:**
```java
// BAD — autoboxing in tight loop
Long sum = 0L;
for (long i = 0; i < 1_000_000; i++) sum += i; // unbox, add, box 1M times

// GOOD
long sum = 0L;
for (long i = 0; i < 1_000_000; i++) sum += i;
```

**Using wrong collection type:**
```java
// BAD — LinkedList for random access
LinkedList<String> list = new LinkedList<>();
list.get(500); // O(n) — traverse 500 nodes

// GOOD — ArrayList for random access
ArrayList<String> list = new ArrayList<>();
list.get(500); // O(1) — direct array index
```

### Common Mistakes

**1. Using `==` instead of `.equals()` for Objects:**
```java
String a = new String("hello");
String b = new String("hello");
a == b      // false — different objects
a.equals(b) // true — same content
```

**2. Modifying collection while iterating:**
```java
// Throws ConcurrentModificationException:
for (String s : list) {
    if (s.isEmpty()) list.remove(s); // BAD
}

// Use Iterator:
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().isEmpty()) it.remove(); // GOOD

// Or use removeIf (Java 8+):
list.removeIf(String::isEmpty);
```

**3. Catching Exception or Throwable too broadly:**
```java
// BAD — hides programming errors
try { ... }
catch (Exception e) {} // silently swallows everything

// GOOD — catch specific exceptions
try { ... }
catch (IOException e) { log.error("IO error", e); }
catch (IllegalArgumentException e) { throw e; } // let programming errors propagate
```

**4. Not closing resources:**
```java
// BAD — may leak connection if exception thrown
Connection conn = dataSource.getConnection();
Statement stmt = conn.createStatement();
// ... exception here leaks conn!

// GOOD — try-with-resources
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement()) {
    // conn and stmt auto-closed
}
```

**5. Integer overflow:**
```java
int maxInt = Integer.MAX_VALUE;
System.out.println(maxInt + 1); // -2147483648 (overflow — no exception!)
// Use long or Math.addExact() for overflow detection:
Math.addExact(maxInt, 1); // throws ArithmeticException
```

**6. Float/Double precision:**
```java
System.out.println(0.1 + 0.2); // 0.30000000000000004 (floating point imprecision)
// Use BigDecimal for financial calculations:
BigDecimal result = new BigDecimal("0.1").add(new BigDecimal("0.2")); // 0.3 exactly
```

---

## 🎯 Quick-Fire One-Liners

| Concept | Answer |
|---|---|
| **JVM** | Executes Java bytecode on any platform |
| **JDK vs JRE** | JDK = development tools + JRE; JRE = JVM + libraries for running |
| **OOP Pillars** | Encapsulation, Inheritance, Polymorphism, Abstraction |
| **Encapsulation** | Hide fields, expose through getters/setters |
| **Polymorphism** | Same method behaves differently based on actual object type |
| **`static`** | Belongs to the class, not any instance; shared |
| **`final` variable** | Cannot be reassigned after initialization |
| **`final` class** | Cannot be subclassed (e.g., String) |
| **`final` method** | Cannot be overridden |
| **Autoboxing** | Automatic primitive ↔ wrapper conversion |
| **String immutability** | String value never changes; modifications create new object |
| **String pool** | Shared area for string literals; `"hello" == "hello"` is true |
| **StringBuilder** | Mutable string; use in loops for performance |
| **Overloading** | Same name, different params in same class (compile-time) |
| **Overriding** | Subclass redefines parent's method (runtime) |
| **`super()`** | Call parent class constructor; must be first line |
| **`this()`** | Call another constructor in same class |
| **Abstract class** | Can't instantiate; may have abstract methods |
| **Interface** | Contract with abstract methods; a class can implement many |
| **Default method** | Concrete method in interface (Java 8+); backward compatible |
| **Checked exception** | Compiler forces handling; represents recoverable conditions |
| **Unchecked exception** | RuntimeException; programming errors |
| **`finally`** | Always runs after try-catch; use for cleanup |
| **try-with-resources** | Auto-closes AutoCloseable resources |
| **`throws`** | Method declaration that it may throw checked exception |
| **`throw`** | Manually throw an exception |
| **ArrayList** | Dynamic array; fast random access O(1) |
| **LinkedList** | Doubly-linked; fast insert/delete at ends O(1) |
| **HashSet** | No duplicates, no order, O(1) operations |
| **TreeSet** | No duplicates, sorted, O(log n) operations |
| **HashMap** | Key-value, no order, O(1) average |
| **TreeMap** | Key-value, sorted by key, O(log n) |
| **LinkedHashMap** | Key-value, insertion order maintained |
| **Comparable** | Natural ordering defined in the class itself |
| **Comparator** | External ordering; passed to sort methods |
| **Generics** | Type-safe reusable code; type info erased at runtime |
| **Wildcard `? extends T`** | Producer — read from collection of T or subtype |
| **Wildcard `? super T`** | Consumer — write to collection of T or supertype |
| **Lambda** | Anonymous function implementing a functional interface |
| **Functional interface** | Interface with exactly one abstract method |
| **Stream** | Pipeline for processing collections declaratively |
| **`filter`** | Keep elements matching predicate |
| **`map`** | Transform each element |
| **`collect`** | Terminal operation gathering results |
| **Optional** | Container that may or may not have a value; avoids NPE |
| **`volatile`** | Variable always read/written to main memory; visibility guarantee |
| **`synchronized`** | Ensures only one thread executes block at a time |
| **`AtomicInteger`** | Thread-safe integer using CAS; no locks needed |
| **Deadlock** | Two threads each holding a lock the other needs |
| **ExecutorService** | Thread pool for managing concurrent tasks |
| **CompletableFuture** | Async computation with chaining and combination |
| **Record** | Immutable data class with auto-generated methods (Java 16+) |
| **Sealed class** | Restricts which classes can extend it (Java 17+) |
| **Text block** | Multi-line string literal (Java 15+) |
| **var** | Local type inference; compiler infers type (Java 10+) |
| **Singleton pattern** | One instance per JVM; use enum for thread safety |
| **Builder pattern** | Construct complex objects step-by-step |
| **Factory pattern** | Delegate object creation to factory method |
| **Strategy pattern** | Swappable algorithms at runtime |
| **Observer pattern** | Notify dependents when state changes |
| **Heap** | Where objects live; shared across threads; GC managed |
| **Stack** | Per-thread; local variables and call frames |
| **GC** | Automatically reclaims memory of unreachable objects |
| **`transient`** | Field excluded from serialization |
| **`serialVersionUID`** | Version ID for serializable class; prevents mismatch |
| **ClassLoader** | Loads .class files into JVM; uses parent delegation |

---

*Master these concepts and you'll be ready for any Java interview from junior to senior level! ☕🚀*