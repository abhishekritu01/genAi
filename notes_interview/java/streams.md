# 🌊 Java 8 Streams – Complete Deep-Dive Notes
> Everything about Stream API, Collectors, Stream Pipeline, Collections integration — explained with real examples for interview and daily use.

---

## 📌 Table of Contents
1. [What is a Stream?](#1-what-is-a-stream)
2. [Stream Pipeline – How It Works](#2-stream-pipeline--how-it-works)
3. [Creating Streams](#3-creating-streams)
4. [Intermediate Operations](#4-intermediate-operations)
5. [Terminal Operations](#5-terminal-operations)
6. [Collectors – Complete Guide](#6-collectors--complete-guide)
7. [Numeric Streams – IntStream, LongStream, DoubleStream](#7-numeric-streams--intstream-longstream-doublestream)
8. [Flatmap – Flattening Nested Structures](#8-flatmap--flattening-nested-structures)
9. [Optional – The Stream Companion](#9-optional--the-stream-companion)
10. [Parallel Streams](#10-parallel-streams)
11. [Stream with Collections – Complete Integration](#11-stream-with-collections--complete-integration)
12. [Custom Collectors](#12-custom-collectors)
13. [Stream Pitfalls & Best Practices](#13-stream-pitfalls--best-practices)
14. [Real-World Examples & Patterns](#14-real-world-examples--patterns)
15. [Quick-Fire Interview Q&A](#15-quick-fire-interview-qa)

---

## 1. What is a Stream?

### Definition
A **Stream** is a sequence of elements from a source (collection, array, I/O channel) that supports aggregate operations. It is NOT a data structure — it does not store data. It describes a pipeline of computations to be performed on data.

```
Source → [intermediate op 1] → [intermediate op 2] → terminal op → result
```

### Stream vs Collection

| Feature | Collection | Stream |
|---|---|---|
| Purpose | **Stores** data | **Processes** data |
| Iteration | External (you write the loop) | Internal (Stream handles it) |
| Reusability | Can iterate multiple times | **One-time use** — consumed after terminal op |
| Modification | You can add/remove elements | **Never modifies** the source |
| Evaluation | Eager — data exists immediately | **Lazy** — computed only when needed |
| Size | Always finite | Can be **infinite** |

```java
// Collection — you control iteration
List<String> names = List.of("Alice", "Bob", "Charlie");
for (String name : names) {   // external iteration — YOU write the loop
    if (name.startsWith("A")) System.out.println(name.toUpperCase());
}

// Stream — stream controls iteration
names.stream()                         // create stream from collection
     .filter(name -> name.startsWith("A"))  // internal iteration — Stream handles it
     .map(String::toUpperCase)
     .forEach(System.out::println);
```

### Key Characteristics of Streams
1. **Not a data structure** — doesn't store elements; computes on demand
2. **Lazy evaluation** — intermediate operations don't execute until a terminal operation is called
3. **One-time use** — once a stream is consumed (terminal op called), it cannot be reused
4. **Does not modify source** — the original collection is never changed
5. **Can be infinite** — `Stream.generate()` or `Stream.iterate()` produce endless streams
6. **Optionally parallel** — `.parallelStream()` processes elements concurrently

```java
// Stream is one-time use:
Stream<String> stream = names.stream();
stream.forEach(System.out::println);  // OK — consumes stream
stream.forEach(System.out::println);  // ❌ IllegalStateException: stream already operated upon
```

### Where Streams Come From — The `java.util.stream` Package

```
java.util.stream
├── Stream<T>           — generic object stream
├── IntStream           — stream of int primitives (avoids boxing)
├── LongStream          — stream of long primitives
├── DoubleStream        — stream of double primitives
├── Collectors          — factory for Collector implementations
└── Collector<T,A,R>   — interface for custom collectors
```

---

## 2. Stream Pipeline – How It Works

### Anatomy of a Stream Pipeline
A pipeline has exactly **three parts**:

```
[Source] → [0 or more Intermediate Operations] → [1 Terminal Operation]
```

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

int result = numbers.stream()          // 1️⃣ SOURCE
    .filter(n -> n % 2 == 0)          // 2️⃣ INTERMEDIATE — keep even numbers
    .map(n -> n * n)                   // 2️⃣ INTERMEDIATE — square each
    .reduce(0, Integer::sum);          // 3️⃣ TERMINAL — sum all

// result = 4 + 16 + 36 + 64 + 100 = 220
```

### Lazy Evaluation — The Most Important Concept
Intermediate operations do NOT execute when you call them. They build a **recipe**. The recipe executes only when a terminal operation is called.

```java
List<String> names = List.of("Alice", "Bob", "Charlie", "Anna");

// Nothing executes yet — just building the pipeline:
Stream<String> pipeline = names.stream()
    .filter(n -> {
        System.out.println("filter: " + n);  // NOT printed yet
        return n.startsWith("A");
    })
    .map(n -> {
        System.out.println("map: " + n);      // NOT printed yet
        return n.toUpperCase();
    });

System.out.println("--- Terminal operation called ---");
pipeline.forEach(System.out::println);  // NOW everything executes

// Output:
// --- Terminal operation called ---
// filter: Alice
// map: Alice
// ALICE
// filter: Bob
// filter: Charlie
// filter: Anna
// map: Anna
// ANNA
```

**Key insight:** Elements flow through the pipeline **one at a time** — not batch by batch. `filter` and `map` are applied to "Alice" before processing "Bob". This enables **short-circuiting**.

### Short-Circuit Operations
Some operations stop the pipeline early without processing all elements:

```java
// findFirst — stops as soon as first matching element is found
Optional<String> first = names.stream()
    .filter(n -> {
        System.out.println("checking: " + n);
        return n.startsWith("A");
    })
    .findFirst();
// Prints "checking: Alice" then STOPS — doesn't check Bob, Charlie, Anna
// Because Alice already satisfies the condition

// limit — stops after N elements
List<Integer> first5 = Stream.iterate(1, n -> n + 1)  // infinite stream: 1,2,3,...
    .limit(5)    // stops after 5 elements — makes infinite stream usable
    .collect(Collectors.toList()); // [1, 2, 3, 4, 5]

// anyMatch — stops as soon as one match is found
boolean hasEven = numbers.stream()
    .anyMatch(n -> n % 2 == 0); // stops at first even number found
```

### Pipeline Execution Order — Vertical vs Horizontal
Streams process elements **vertically** (one element through all ops), not **horizontally** (all elements through each op).

```java
List.of(1, 2, 3).stream()
    .filter(n -> n > 1)
    .map(n -> n * 10)
    .forEach(System.out::println);

// Execution order (VERTICAL — each element goes all the way through):
// filter(1) → false → skip
// filter(2) → true → map(2) → 20 → print(20)
// filter(3) → true → map(3) → 30 → print(30)

// NOT horizontal like:
// filter: 1,2,3 → [2,3]
// map: 2,3 → [20,30]
// forEach: 20,30
```

---

## 3. Creating Streams

### From Collections
```java
// List, Set, Queue — any Collection
List<String> list = List.of("a", "b", "c");
Stream<String> stream1 = list.stream();
Stream<String> stream2 = list.parallelStream();  // parallel

// Map — must convert first
Map<String, Integer> map = Map.of("a", 1, "b", 2);
Stream<Map.Entry<String,Integer>> entryStream = map.entrySet().stream();
Stream<String> keyStream = map.keySet().stream();
Stream<Integer> valueStream = map.values().stream();
```

### From Arrays
```java
String[] arr = {"Alice", "Bob", "Charlie"};
Stream<String> stream = Arrays.stream(arr);

// With range (not all elements):
Stream<String> partial = Arrays.stream(arr, 1, 3);  // "Bob", "Charlie"

// Primitive arrays:
int[] ints = {1, 2, 3, 4, 5};
IntStream intStream = Arrays.stream(ints);  // returns IntStream, not Stream<Integer>
```

### Stream.of() — Direct Values
```java
Stream<String> s1 = Stream.of("A", "B", "C");
Stream<Integer> s2 = Stream.of(1, 2, 3);

// Empty stream (useful as a default return value):
Stream<String> empty = Stream.empty();
```

### Stream.builder() — Build Incrementally
```java
Stream.Builder<String> builder = Stream.builder();
builder.add("A");
builder.add("B");
if (condition) builder.add("C");
Stream<String> stream = builder.build();
```

### Stream.generate() — Infinite Streams (Lazy, Stateless)
```java
// Produces infinite stream — must use limit() or findFirst() etc.
Stream<Double> randoms = Stream.generate(Math::random).limit(5);

Stream<String> hellos = Stream.generate(() -> "Hello").limit(3);
// ["Hello", "Hello", "Hello"]

// Generate UUIDs:
Stream<String> ids = Stream.generate(() -> UUID.randomUUID().toString()).limit(10);
```

### Stream.iterate() — Infinite Sequences
```java
// iterate(seed, function) — each element computed from previous
Stream<Integer> naturals = Stream.iterate(1, n -> n + 1); // 1,2,3,4,...
naturals.limit(10).forEach(System.out::println); // 1 through 10

// Powers of 2:
Stream.iterate(1, n -> n * 2).limit(10).forEach(System.out::println);
// 1, 2, 4, 8, 16, 32, 64, 128, 256, 512

// Java 9+ — iterate with predicate (like a for loop):
Stream.iterate(0, n -> n < 100, n -> n + 10)
      .forEach(System.out::println); // 0, 10, 20, ..., 90
```

### From String
```java
// Stream of characters (as IntStream):
"Hello".chars().forEach(c -> System.out.print((char)c));

// Stream of lines in a string (Java 11+):
"line1\nline2\nline3".lines().forEach(System.out::println);
```

### From Files (I/O)
```java
// Stream of lines from a file — auto-closed when stream is closed
try (Stream<String> lines = Files.lines(Path.of("data.txt"), StandardCharsets.UTF_8)) {
    lines.filter(line -> !line.isBlank())
         .map(String::trim)
         .forEach(System.out::println);
}

// Stream of file paths:
try (Stream<Path> paths = Files.walk(Path.of("src"))) {
    paths.filter(p -> p.toString().endsWith(".java"))
         .forEach(System.out::println);
}
```

### Combining Streams — Stream.concat()
```java
Stream<String> s1 = Stream.of("A", "B");
Stream<String> s2 = Stream.of("C", "D");
Stream<String> combined = Stream.concat(s1, s2);
// A, B, C, D
```

---

## 4. Intermediate Operations

Intermediate operations return a **new Stream**. They are **lazy** — they don't run until a terminal op is called. They can be chained.

### filter(Predicate) — Keep Elements Matching a Condition
```java
// Predicate<T>: T → boolean
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Keep even numbers:
numbers.stream().filter(n -> n % 2 == 0).collect(Collectors.toList());
// [2, 4, 6, 8, 10]

// Keep non-null, non-empty strings:
list.stream()
    .filter(Objects::nonNull)        // remove nulls
    .filter(s -> !s.isBlank())       // remove blanks
    .collect(Collectors.toList());

// Chaining multiple filters (each is an AND condition):
employees.stream()
    .filter(e -> e.getDepartment().equals("Engineering"))
    .filter(e -> e.getSalary() > 80000)
    .filter(e -> e.getYearsExp() >= 3)
    .collect(Collectors.toList());

// Equivalent using single filter with &&:
employees.stream()
    .filter(e -> e.getDepartment().equals("Engineering")
             && e.getSalary() > 80000
             && e.getYearsExp() >= 3)
    .collect(Collectors.toList());
```

### map(Function) — Transform Each Element
```java
// Function<T, R>: T → R (transforms each element to a different type/value)
List<String> names = List.of("alice", "bob", "charlie");

// String → String transformation:
names.stream().map(String::toUpperCase).collect(Collectors.toList());
// ["ALICE", "BOB", "CHARLIE"]

// String → Integer transformation (change type):
names.stream().map(String::length).collect(Collectors.toList());
// [5, 3, 7]

// Object → field extraction:
List<String> emails = employees.stream()
    .map(Employee::getEmail)
    .collect(Collectors.toList());

// Object → object transformation:
List<EmployeeDTO> dtos = employees.stream()
    .map(e -> new EmployeeDTO(e.getId(), e.getName(), e.getEmail()))
    .collect(Collectors.toList());

// Nested object access:
List<String> cities = orders.stream()
    .map(Order::getShippingAddress)
    .map(Address::getCity)
    .collect(Collectors.toList());
```

### flatMap(Function) — Transform + Flatten
```java
// Function<T, Stream<R>>: each element T becomes a Stream<R>, then all streams merged into one
// Use when each element maps to multiple elements

// Example: each sentence → stream of words
List<String> sentences = List.of("Hello World", "Java Streams", "are powerful");
List<String> words = sentences.stream()
    .flatMap(sentence -> Arrays.stream(sentence.split(" ")))
    .collect(Collectors.toList());
// ["Hello", "World", "Java", "Streams", "are", "powerful"]

// Example: each order → stream of items
List<List<String>> nested = List.of(
    List.of("A", "B"),
    List.of("C", "D"),
    List.of("E")
);
List<String> flat = nested.stream()
    .flatMap(Collection::stream)  // List::stream also works
    .collect(Collectors.toList());
// ["A", "B", "C", "D", "E"]

// Real example: get all unique skills from all employees
Set<String> allSkills = employees.stream()
    .flatMap(e -> e.getSkills().stream())  // each employee has a List<String> skills
    .collect(Collectors.toSet());
```

### distinct() — Remove Duplicates
```java
// Uses equals() to determine duplicates — must override equals() for custom objects
List<Integer> nums = List.of(1, 2, 2, 3, 3, 3, 4);
nums.stream().distinct().collect(Collectors.toList());
// [1, 2, 3, 4]

// Unique first characters:
List<String> names = List.of("Alice", "Anna", "Bob", "Brian", "Charlie");
names.stream()
     .map(n -> n.charAt(0))
     .distinct()
     .sorted()
     .collect(Collectors.toList());
// ['A', 'B', 'C']
```

### sorted() — Sort Elements
```java
List<Integer> nums = List.of(5, 3, 1, 4, 2);

// Natural order (Comparable):
nums.stream().sorted().collect(Collectors.toList()); // [1, 2, 3, 4, 5]

// Reverse order:
nums.stream().sorted(Comparator.reverseOrder()).collect(Collectors.toList()); // [5,4,3,2,1]

// Sort objects by field:
employees.stream()
    .sorted(Comparator.comparing(Employee::getSalary))  // ascending
    .collect(Collectors.toList());

// Sort descending:
employees.stream()
    .sorted(Comparator.comparing(Employee::getSalary).reversed())
    .collect(Collectors.toList());

// Sort by multiple fields (primary: department, secondary: salary desc):
employees.stream()
    .sorted(Comparator.comparing(Employee::getDepartment)
        .thenComparing(Comparator.comparing(Employee::getSalary).reversed()))
    .collect(Collectors.toList());

// Null-safe sorting (nulls last):
employees.stream()
    .sorted(Comparator.comparing(Employee::getName, Comparator.nullsLast(Comparator.naturalOrder())))
    .collect(Collectors.toList());
```

### limit(n) — Take First N Elements
```java
// Take first 5:
Stream.iterate(1, n -> n + 1).limit(5).collect(Collectors.toList()); // [1,2,3,4,5]

// Pagination — page 2, size 10:
int page = 2, size = 10;
list.stream()
    .skip((page - 1) * size)  // skip page 1's elements
    .limit(size)               // take page 2's elements
    .collect(Collectors.toList());
```

### skip(n) — Skip First N Elements
```java
// Skip first 3:
List.of(1,2,3,4,5).stream().skip(3).collect(Collectors.toList()); // [4, 5]

// Skip header in CSV lines:
Files.lines(Path.of("data.csv"))
     .skip(1)        // skip header row
     .map(line -> line.split(","))
     .collect(Collectors.toList());
```

### peek(Consumer) — Debug / Side Effects Without Consuming
```java
// peek lets you see elements without stopping the pipeline — for logging/debugging
List<Integer> result = numbers.stream()
    .peek(n -> System.out.println("Before filter: " + n))
    .filter(n -> n > 3)
    .peek(n -> System.out.println("After filter:  " + n))
    .map(n -> n * 10)
    .peek(n -> System.out.println("After map:     " + n))
    .collect(Collectors.toList());

// Output:
// Before filter: 1
// Before filter: 2
// Before filter: 3
// Before filter: 4
// After filter:  4
// After map:     40
// ...
```

> **Important:** `peek` should only be used for debugging. Don't rely on it for business logic — it may not execute in certain cases (e.g., with short-circuit terminals like `findFirst`).

### mapToInt / mapToLong / mapToDouble — Convert to Numeric Stream
```java
// Converts Stream<T> to IntStream (avoids boxing overhead)
int totalSalary = employees.stream()
    .mapToInt(Employee::getSalary)  // Stream<Employee> → IntStream
    .sum();                          // IntStream has sum(), avg(), min(), max()

double avgAge = employees.stream()
    .mapToDouble(Employee::getAge)
    .average()
    .orElse(0.0);
```

### takeWhile(Predicate) — Java 9+
```java
// Takes elements while condition is true, stops at first false (like break)
// Only meaningful on ordered streams
List.of(1, 2, 3, 4, 5, 1, 2).stream()
    .takeWhile(n -> n < 4)
    .collect(Collectors.toList()); // [1, 2, 3] — stops at 4
```

### dropWhile(Predicate) — Java 9+
```java
// Drops elements while condition is true, keeps the rest from first false
List.of(1, 2, 3, 4, 5, 1, 2).stream()
    .dropWhile(n -> n < 4)
    .collect(Collectors.toList()); // [4, 5, 1, 2] — drops 1,2,3
```

### Intermediate Operations Summary Table

| Operation | Input → Output | What it does | Short-circuits? |
|---|---|---|---|
| `filter(pred)` | `Stream<T>` → `Stream<T>` | Keep elements matching predicate | No |
| `map(func)` | `Stream<T>` → `Stream<R>` | Transform each element | No |
| `flatMap(func)` | `Stream<T>` → `Stream<R>` | Transform + flatten nested streams | No |
| `distinct()` | `Stream<T>` → `Stream<T>` | Remove duplicates | No |
| `sorted()` | `Stream<T>` → `Stream<T>` | Sort elements | No |
| `sorted(comp)` | `Stream<T>` → `Stream<T>` | Sort with custom comparator | No |
| `limit(n)` | `Stream<T>` → `Stream<T>` | Take first N elements | **Yes** |
| `skip(n)` | `Stream<T>` → `Stream<T>` | Skip first N elements | No |
| `peek(cons)` | `Stream<T>` → `Stream<T>` | Side effect (debug), pass through | No |
| `mapToInt(func)` | `Stream<T>` → `IntStream` | Map to int primitive stream | No |
| `mapToLong(func)` | `Stream<T>` → `LongStream` | Map to long primitive stream | No |
| `mapToDouble(func)` | `Stream<T>` → `DoubleStream` | Map to double primitive stream | No |
| `takeWhile(pred)` | `Stream<T>` → `Stream<T>` | Take while true (Java 9+) | **Yes** |
| `dropWhile(pred)` | `Stream<T>` → `Stream<T>` | Drop while true (Java 9+) | No |

---

## 5. Terminal Operations

Terminal operations **consume the stream** and produce a result or side effect. After a terminal operation, the stream is closed and cannot be reused.

### forEach / forEachOrdered — Consume Each Element
```java
// forEach — no guaranteed order (especially in parallel streams)
names.stream().forEach(System.out::println);

// forEachOrdered — maintains encounter order even in parallel streams
names.parallelStream().forEachOrdered(System.out::println); // always in original order
```

### collect(Collector) — Gather Into a Container
The most powerful terminal operation. See Section 6 for all Collectors in detail.

```java
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
String joined = stream.collect(Collectors.joining(", "));
Map<String, Integer> map = stream.collect(Collectors.toMap(k -> k, String::length));
```

### toList() — Java 16+
```java
// Shorthand for collect(Collectors.toList()) — returns unmodifiable list
List<String> list = stream.toList(); // Java 16+
```

### count() — Count Elements
```java
long count = employees.stream()
    .filter(e -> e.getDepartment().equals("Engineering"))
    .count(); // number of engineers
```

### findFirst() / findAny() — Find an Element
```java
// findFirst — returns first element (in encounter order), Optional<T>
Optional<String> first = names.stream()
    .filter(n -> n.startsWith("A"))
    .findFirst(); // Optional["Alice"] or Optional.empty()

first.ifPresent(System.out::println); // prints if present

// findAny — returns any element (faster in parallel, non-deterministic)
Optional<String> any = names.parallelStream()
    .filter(n -> n.startsWith("A"))
    .findAny();
```

### anyMatch / allMatch / noneMatch — Check Conditions
```java
List<Integer> numbers = List.of(2, 4, 6, 7, 8, 10);

// anyMatch — true if AT LEAST ONE element matches (short-circuits)
boolean hasOdd = numbers.stream().anyMatch(n -> n % 2 != 0); // true (7 is odd)

// allMatch — true if ALL elements match (short-circuits on first false)
boolean allEven = numbers.stream().allMatch(n -> n % 2 == 0); // false (7 fails)

// noneMatch — true if NO elements match (short-circuits on first match)
boolean noNegative = numbers.stream().noneMatch(n -> n < 0); // true

// With empty stream:
// anyMatch → false (no elements, so none match)
// allMatch → true (vacuously true — no element fails)
// noneMatch → true (no elements match)
Stream.<Integer>empty().allMatch(n -> n > 0); // true — vacuous truth
```

### min() / max() — Find Extremes
```java
// Returns Optional<T> — empty if stream is empty
Optional<Integer> min = numbers.stream().min(Comparator.naturalOrder()); // Optional[1]
Optional<Integer> max = numbers.stream().max(Comparator.naturalOrder()); // Optional[10]

// Find employee with highest salary:
Optional<Employee> highestPaid = employees.stream()
    .max(Comparator.comparing(Employee::getSalary));

highestPaid.ifPresent(e -> System.out.println(e.getName() + ": " + e.getSalary()));

// Find shortest string:
Optional<String> shortest = names.stream()
    .min(Comparator.comparingInt(String::length));
```

### reduce() — Fold Elements Into a Single Value
```java
// reduce(identity, BinaryOperator) — starts with identity, applies op cumulatively
int sum = IntStream.rangeClosed(1, 10).reduce(0, Integer::sum); // 55
int product = IntStream.rangeClosed(1, 5).reduce(1, (a, b) -> a * b); // 120 (5!)

// reduce(BinaryOperator) — no identity, returns Optional
Optional<Integer> max = numbers.stream()
    .reduce((a, b) -> a > b ? a : b); // same as max()

// reduce(identity, BiFunction, BinaryOperator) — for parallel reduction with type change
// Used when accumulating different types:
int totalLength = names.stream()
    .reduce(0,
        (acc, name) -> acc + name.length(),  // accumulator
        Integer::sum);                        // combiner (for parallel)
// 0 + 5 + 3 + 7 = 15

// Custom object accumulation:
int totalSalary = employees.stream()
    .reduce(0,
        (acc, emp) -> acc + emp.getSalary(),
        Integer::sum);
// Better: use mapToInt().sum()
int totalSalary2 = employees.stream().mapToInt(Employee::getSalary).sum();
```

### toArray() — Convert to Array
```java
Object[] arr = names.stream().toArray(); // Object[]

String[] strArr = names.stream().toArray(String[]::new); // String[]

int[] intArr = IntStream.rangeClosed(1, 5).toArray(); // int[]
```

### iterator() / spliterator() — Get Iterator
```java
// Convert stream to Iterator for external use
Iterator<String> it = names.stream().iterator();
while (it.hasNext()) {
    System.out.println(it.next());
}
```

### Terminal Operations Summary Table

| Operation | Returns | Description | Short-circuits? |
|---|---|---|---|
| `forEach(cons)` | `void` | Apply action to each element | No |
| `forEachOrdered(cons)` | `void` | Apply action, maintain order | No |
| `collect(coll)` | `R` | Gather into a container | No |
| `toList()` | `List<T>` | Unmodifiable list (Java 16+) | No |
| `count()` | `long` | Count elements | No |
| `findFirst()` | `Optional<T>` | First element | **Yes** |
| `findAny()` | `Optional<T>` | Any element | **Yes** |
| `anyMatch(pred)` | `boolean` | At least one match | **Yes** |
| `allMatch(pred)` | `boolean` | All elements match | **Yes** |
| `noneMatch(pred)` | `boolean` | No elements match | **Yes** |
| `min(comp)` | `Optional<T>` | Minimum element | No |
| `max(comp)` | `Optional<T>` | Maximum element | No |
| `reduce(...)` | `T` or `Optional<T>` | Fold to single value | No |
| `toArray()` | `Object[]` or `T[]` | Convert to array | No |
| `iterator()` | `Iterator<T>` | Get external iterator | — |

---

## 6. Collectors – Complete Guide

`Collectors` is a utility class with static factory methods that produce `Collector` implementations. A `Collector` describes how to accumulate stream elements into a result container.

```java
import static java.util.stream.Collectors.*;
// Allows: toList() instead of Collectors.toList()
```

### Basic Collectors

#### toList() — Collect to List
```java
List<String> list = names.stream()
    .filter(n -> n.length() > 3)
    .collect(Collectors.toList()); // mutable, allows nulls

// Java 16+ shorthand (unmodifiable):
List<String> list2 = names.stream().filter(n -> n.length() > 3).toList();
```

#### toSet() — Collect to Set (No Duplicates)
```java
Set<String> departments = employees.stream()
    .map(Employee::getDepartment)
    .collect(Collectors.toSet()); // HashSet — no guaranteed order
```

#### toUnmodifiableList() / toUnmodifiableSet() — Java 10+
```java
List<String> immutable = names.stream()
    .collect(Collectors.toUnmodifiableList()); // throws UnsupportedOperationException on modification
```

#### toCollection(Supplier) — Collect to Specific Collection Type
```java
// Collect to LinkedList:
LinkedList<String> linkedList = names.stream()
    .collect(Collectors.toCollection(LinkedList::new));

// Collect to TreeSet (sorted, no duplicates):
TreeSet<String> sortedSet = names.stream()
    .collect(Collectors.toCollection(TreeSet::new));

// Collect to ArrayDeque:
ArrayDeque<String> deque = names.stream()
    .collect(Collectors.toCollection(ArrayDeque::new));
```

### String Collectors

#### joining() — Concatenate Strings
```java
List<String> words = List.of("Java", "is", "awesome");

// No delimiter:
words.stream().collect(Collectors.joining()); // "Javaawesome"... no separator

// With delimiter:
words.stream().collect(Collectors.joining(" ")); // "Java is awesome"

// With delimiter + prefix + suffix:
words.stream().collect(Collectors.joining(", ", "[", "]")); // "[Java, is, awesome]"

// Common use: comma-separated IDs
String ids = employees.stream()
    .map(e -> String.valueOf(e.getId()))
    .collect(Collectors.joining(", ")); // "1, 2, 3, 4"
```

### Map Collectors

#### toMap(keyMapper, valueMapper) — Collect to Map
```java
// Map from name → age:
Map<String, Integer> nameToAge = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,    // key extractor
        Employee::getAge      // value extractor
    ));
// ⚠️ Throws IllegalStateException on DUPLICATE KEYS

// Handle duplicate keys with merge function:
Map<String, Integer> nameToSalary = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,
        Employee::getSalary,
        (existing, newValue) -> existing  // keep first on duplicate
        // or: Integer::sum — sum salaries of same-named employees
    ));

// Specify map type (LinkedHashMap to maintain insertion order):
Map<String, Integer> ordered = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,
        Employee::getAge,
        (e, n) -> e,
        LinkedHashMap::new   // map factory
    ));

// Map ID → whole object:
Map<Long, Employee> byId = employees.stream()
    .collect(Collectors.toMap(Employee::getId, e -> e));
// Or: .collect(Collectors.toMap(Employee::getId, Function.identity()));
```

#### toUnmodifiableMap() — Java 10+
```java
Map<String, Integer> immutableMap = employees.stream()
    .collect(Collectors.toUnmodifiableMap(Employee::getName, Employee::getAge));
```

### Grouping Collectors

#### groupingBy(classifier) — Group Into Map<K, List<V>>
This is one of the most powerful and frequently used collectors.

```java
// Group employees by department:
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));
// { "Engineering": [emp1, emp3], "Sales": [emp2, emp4], ... }

// Group by string length:
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));
// { 3: ["Bob"], 5: ["Alice", "Carol"], 7: ["Charlie"] }

// Group by custom condition:
Map<String, List<Employee>> bySeniority = employees.stream()
    .collect(Collectors.groupingBy(e -> {
        if (e.getYearsExp() < 2) return "Junior";
        else if (e.getYearsExp() < 5) return "Mid";
        else return "Senior";
    }));

// Group by enum:
Map<Department, List<Employee>> byDeptEnum = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartmentEnum));
```

#### groupingBy with Downstream Collector
The second argument to `groupingBy` is a **downstream collector** applied to each group.

```java
// Count per group:
Map<String, Long> countByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.counting()       // downstream: count elements in each group
    ));
// { "Engineering": 5, "Sales": 3, "HR": 2 }

// Average salary per department:
Map<String, Double> avgSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.averagingInt(Employee::getSalary)
    ));

// Sum salaries per department:
Map<String, Integer> totalSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.summingInt(Employee::getSalary)
    ));

// Collect to Set per group (no duplicates in each group):
Map<String, Set<String>> skillsByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.mapping(Employee::getName, Collectors.toSet())
    ));

// Max salary employee per department:
Map<String, Optional<Employee>> highestPaidByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.maxBy(Comparator.comparing(Employee::getSalary))
    ));

// Join names per department:
Map<String, String> namesByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.mapping(Employee::getName, Collectors.joining(", "))
    ));
// { "Engineering": "Alice, Bob, Charlie", "Sales": "Dave, Eve" }

// Collect to TreeSet (sorted) per group:
Map<String, TreeSet<String>> sortedByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.mapping(Employee::getName, Collectors.toCollection(TreeSet::new))
    ));
```

#### groupingBy with Map Type Specification
```java
// Use TreeMap to have departments in sorted order:
TreeMap<String, List<Employee>> sorted = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        TreeMap::new,              // map factory
        Collectors.toList()        // downstream
    ));
```

#### Multi-Level Grouping (Nested groupingBy)
```java
// Group by department, then by seniority level:
Map<String, Map<String, List<Employee>>> byDeptAndLevel = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.groupingBy(e -> e.getYearsExp() >= 5 ? "Senior" : "Junior")
    ));
// { "Engineering": { "Senior": [...], "Junior": [...] }, "Sales": { ... } }
```

### Partitioning

#### partitioningBy(predicate) — Split Into Two Groups (true/false)
```java
// Partition employees: passing salary threshold or not
Map<Boolean, List<Employee>> partitioned = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 80000));

List<Employee> highPaid = partitioned.get(true);
List<Employee> lowPaid = partitioned.get(false);

// Partition with downstream collector:
Map<Boolean, Long> countPartitioned = employees.stream()
    .collect(Collectors.partitioningBy(
        e -> e.getSalary() > 80000,
        Collectors.counting()
    ));
// { true: 12, false: 8 }

// Partition students: pass/fail
Map<Boolean, List<String>> results = students.stream()
    .collect(Collectors.partitioningBy(
        s -> s.getGrade() >= 60,
        Collectors.mapping(Student::getName, Collectors.toList())
    ));
// { true: ["Alice", "Bob", ...], false: ["Charlie", ...] }
```

### Statistics Collectors

#### counting() — Count Elements
```java
long count = employees.stream().collect(Collectors.counting());
// Same as: stream.count()
```

#### summingInt / summingLong / summingDouble
```java
int totalSalary = employees.stream().collect(Collectors.summingInt(Employee::getSalary));
double totalGpa = students.stream().collect(Collectors.summingDouble(Student::getGpa));
```

#### averagingInt / averagingLong / averagingDouble
```java
// Always returns Double (never int/long)
Double avgSalary = employees.stream().collect(Collectors.averagingInt(Employee::getSalary));
```

#### summarizingInt / summarizingLong / summarizingDouble
Computes count, sum, min, max, average in a single pass:

```java
IntSummaryStatistics stats = employees.stream()
    .collect(Collectors.summarizingInt(Employee::getSalary));

System.out.println("Count: " + stats.getCount());    // 20
System.out.println("Sum:   " + stats.getSum());      // 1600000
System.out.println("Min:   " + stats.getMin());      // 45000
System.out.println("Max:   " + stats.getMax());      // 150000
System.out.println("Avg:   " + stats.getAverage());  // 80000.0

DoubleSummaryStatistics gpaStats = students.stream()
    .collect(Collectors.summarizingDouble(Student::getGpa));
```

#### maxBy / minBy — Find Extreme Elements
```java
Optional<Employee> richest = employees.stream()
    .collect(Collectors.maxBy(Comparator.comparing(Employee::getSalary)));

Optional<Employee> youngest = employees.stream()
    .collect(Collectors.minBy(Comparator.comparing(Employee::getAge)));
```

### Transformation Collectors

#### mapping(mapper, downstream) — Transform Then Collect
```java
// Get just the names of Engineering employees as a Set:
Set<String> engineerNames = employees.stream()
    .filter(e -> e.getDepartment().equals("Engineering"))
    .collect(Collectors.mapping(Employee::getName, Collectors.toSet()));

// More useful inside groupingBy (shown above)
```

#### flatMapping(mapper, downstream) — Java 9+
```java
// Get all unique skills from all employees in each department:
Map<String, Set<String>> skillsByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.flatMapping(
            e -> e.getSkills().stream(),  // each employee has List<String> skills
            Collectors.toSet()
        )
    ));
```

#### filtering(predicate, downstream) — Java 9+
```java
// Inside groupingBy: only include senior employees in each department's list
Map<String, List<Employee>> seniorByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.filtering(
            e -> e.getYearsExp() >= 5,  // filter within each group
            Collectors.toList()
        )
    ));
```

#### collectingAndThen(downstream, finisher) — Apply a Function After Collection
```java
// Collect then wrap in unmodifiable list:
List<String> unmodifiable = names.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.toList(),
        Collections::unmodifiableList
    ));

// Collect then get size:
int count = names.stream()
    .collect(Collectors.collectingAndThen(Collectors.toList(), List::size));

// Collect then return Optional (useful in groupingBy):
Map<String, Optional<Integer>> maxSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.collectingAndThen(
            Collectors.mapping(Employee::getSalary, Collectors.toList()),
            list -> list.stream().max(Comparator.naturalOrder())
        )
    ));
```

#### teeing(collector1, collector2, merger) — Java 12+
Applies two collectors to the same stream, then merges the results:

```java
// Get both the sum and the count in one pass:
record SumAndCount(int sum, long count) {}

SumAndCount result = numbers.stream()
    .collect(Collectors.teeing(
        Collectors.summingInt(Integer::intValue),  // collector 1: sum
        Collectors.counting(),                      // collector 2: count
        (sum, count) -> new SumAndCount(sum, count) // merge both results
    ));

// Average using teeing:
double average = numbers.stream()
    .collect(Collectors.teeing(
        Collectors.summingDouble(Double::doubleValue),
        Collectors.counting(),
        (sum, count) -> sum / count
    ));

// Min and Max in one pass:
record MinMax(Optional<Integer> min, Optional<Integer> max) {}
MinMax minMax = numbers.stream()
    .collect(Collectors.teeing(
        Collectors.minBy(Comparator.naturalOrder()),
        Collectors.maxBy(Comparator.naturalOrder()),
        MinMax::new
    ));
```

### Collectors Summary Table

| Collector | Returns | Description |
|---|---|---|
| `toList()` | `List<T>` | Mutable list |
| `toUnmodifiableList()` | `List<T>` | Immutable list |
| `toSet()` | `Set<T>` | Mutable set |
| `toCollection(sup)` | `C extends Collection<T>` | Specific collection type |
| `toMap(k,v)` | `Map<K,V>` | Map with key/value extractors |
| `toMap(k,v,merge)` | `Map<K,V>` | Map with duplicate key handling |
| `joining()` | `String` | Concatenate strings |
| `joining(delim)` | `String` | Join with delimiter |
| `joining(d,pre,suf)` | `String` | Join with delimiter, prefix, suffix |
| `groupingBy(cls)` | `Map<K,List<T>>` | Group by classifier |
| `groupingBy(cls,down)` | `Map<K,R>` | Group + apply downstream |
| `partitioningBy(pred)` | `Map<Boolean,List<T>>` | Split into true/false groups |
| `counting()` | `Long` | Count elements |
| `summingInt(func)` | `Integer` | Sum int values |
| `averagingInt(func)` | `Double` | Average of int values |
| `summarizingInt(func)` | `IntSummaryStatistics` | All stats in one pass |
| `maxBy(comp)` | `Optional<T>` | Maximum element |
| `minBy(comp)` | `Optional<T>` | Minimum element |
| `mapping(map,down)` | `R` | Transform then collect |
| `flatMapping(map,down)` | `R` | FlatMap then collect (Java 9+) |
| `filtering(pred,down)` | `R` | Filter within group (Java 9+) |
| `collectingAndThen(d,f)` | `R` | Collect then apply finisher |
| `teeing(c1,c2,merge)` | `R` | Two collectors, merge results (Java 12+) |

---

## 7. Numeric Streams – IntStream, LongStream, DoubleStream

### Why Numeric Streams?
`Stream<Integer>` requires boxing every int into an `Integer` object — expensive. `IntStream` works directly with the `int` primitive — no boxing, less memory, faster.

```java
// Stream<Integer> — boxing overhead
Stream<Integer> boxed = Stream.of(1, 2, 3, 4, 5);
int sum = boxed.mapToInt(Integer::intValue).sum(); // must unbox to add

// IntStream — no boxing
IntStream intStream = IntStream.of(1, 2, 3, 4, 5);
int sum2 = intStream.sum(); // works directly on primitives
```

### Creating Numeric Streams

```java
// IntStream
IntStream.of(1, 2, 3, 4, 5)                     // from values
IntStream.range(0, 10)                            // 0,1,2,...,9 (exclusive end)
IntStream.rangeClosed(1, 10)                      // 1,2,...,10 (inclusive end)
IntStream.iterate(0, n -> n + 2).limit(5)        // 0,2,4,6,8
IntStream.generate(() -> 0).limit(5)             // 0,0,0,0,0

// LongStream
LongStream.rangeClosed(1L, 1_000_000_000L)       // 1 to 1 billion

// DoubleStream
DoubleStream.of(1.1, 2.2, 3.3)
DoubleStream.generate(Math::random).limit(5)     // 5 random doubles
```

### Converting Between Stream Types

```java
// Object Stream → Numeric Stream (mapToInt/Long/Double)
Stream<String> names = Stream.of("Alice", "Bob", "Charlie");
IntStream lengths = names.mapToInt(String::length);  // IntStream of [5, 3, 7]

Stream<Employee> emps = employees.stream();
IntStream salaries = emps.mapToInt(Employee::getSalary); // IntStream

// Numeric Stream → Object Stream (boxed() or mapToObj())
IntStream ints = IntStream.range(1, 6);
Stream<Integer> boxed = ints.boxed();                    // IntStream → Stream<Integer>
Stream<String> strs = IntStream.range(1, 6)
    .mapToObj(i -> "item-" + i);                         // IntStream → Stream<String>

// Convert between numeric types:
IntStream.of(1, 2, 3).asLongStream()    // IntStream → LongStream
IntStream.of(1, 2, 3).asDoubleStream()  // IntStream → DoubleStream
```

### Numeric Stream Operations (only available on numeric streams)

```java
IntStream nums = IntStream.rangeClosed(1, 10);

// Aggregate operations (not on Stream<Integer>!):
int sum     = nums.sum();              // 55
OptionalDouble avg = nums.average();   // OptionalDouble[5.5]
OptionalInt max = nums.max();          // OptionalInt[10]
OptionalInt min = nums.min();          // OptionalInt[1]
long count  = nums.count();            // 10
IntSummaryStatistics stats = nums.summaryStatistics(); // all above in one call

// summaryStatistics():
IntSummaryStatistics s = IntStream.of(3, 1, 4, 1, 5, 9).summaryStatistics();
s.getCount();    // 6
s.getSum();      // 23
s.getMin();      // 1
s.getMax();      // 9
s.getAverage();  // 3.8333...
```

### Practical Examples with Numeric Streams

```java
// Sum of first 100 natural numbers:
int sum = IntStream.rangeClosed(1, 100).sum(); // 5050

// Factorial of 10:
long factorial = LongStream.rangeClosed(1, 10).reduce(1L, (a, b) -> a * b); // 3628800

// Sum of squares of even numbers 1-20:
int sumOfEvenSquares = IntStream.rangeClosed(1, 20)
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .sum();

// Average salary by department (using numeric stream):
Map<String, Double> avgSalaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.averagingInt(Employee::getSalary) // uses IntStream internally
    ));

// Generate multiplication table (streams within streams):
IntStream.rangeClosed(1, 10)
    .forEach(i ->
        IntStream.rangeClosed(1, 10)
                 .mapToObj(j -> String.format("%3d", i * j))
                 .collect(Collectors.joining(" "))
                 |> line -> System.out.println(line)
    );

// Find prime numbers up to N:
IntStream.rangeClosed(2, 100)
    .filter(n -> IntStream.rangeClosed(2, (int) Math.sqrt(n)).allMatch(i -> n % i != 0))
    .forEach(System.out::println);
```

---

## 8. FlatMap – Flattening Nested Structures

### The Problem flatMap Solves
`map` transforms each element to ONE new element. `flatMap` transforms each element to ZERO or MORE elements — perfect for nested collections.

```
map:     [a, b, c] → [f(a), f(b), f(c)]      — one-to-one
flatMap: [a, b, c] → [f1(a), f2(a), f1(b)]   — one-to-many, then flattened
```

```java
// Without flatMap — map gives nested structure:
List<List<String>> nested = List.of(
    List.of("A", "B"),
    List.of("C", "D"),
    List.of("E")
);
Stream<List<String>> mapped = nested.stream().map(list -> list);  // Stream<List<String>>
// still nested — not what we want

// With flatMap — flattens one level:
Stream<String> flat = nested.stream().flatMap(List::stream);
// Stream<String>: A, B, C, D, E
```

### flatMap Examples

```java
// 1. Flatten list of lists:
List<String> allWords = sentences.stream()
    .flatMap(sentence -> Arrays.stream(sentence.split("\\s+")))
    .collect(Collectors.toList());

// 2. All skills from all employees:
List<String> allSkills = employees.stream()
    .flatMap(e -> e.getSkills().stream())
    .distinct()
    .sorted()
    .collect(Collectors.toList());

// 3. All order items across all orders:
List<OrderItem> allItems = orders.stream()
    .flatMap(order -> order.getItems().stream())
    .collect(Collectors.toList());

// 4. Expand each number to itself and its double:
List<Integer> expanded = List.of(1, 2, 3).stream()
    .flatMap(n -> Stream.of(n, n * 2))
    .collect(Collectors.toList());
// [1, 2, 2, 4, 3, 6]

// 5. Optional → Stream (handle null/empty in flatMap pipeline):
List<Optional<String>> optionals = List.of(
    Optional.of("Alice"),
    Optional.empty(),
    Optional.of("Bob")
);
List<String> present = optionals.stream()
    .flatMap(Optional::stream)  // Optional.stream() returns Stream of 0 or 1 elements (Java 9+)
    .collect(Collectors.toList());
// ["Alice", "Bob"]

// 6. Split CSV into individual values across all rows:
List<String> allValues = csvRows.stream()
    .flatMap(row -> Arrays.stream(row.split(",")))
    .map(String::trim)
    .filter(s -> !s.isEmpty())
    .collect(Collectors.toList());
```

### flatMapToInt / flatMapToLong / flatMapToDouble
```java
// Get total number of items across all orders:
int totalItems = orders.stream()
    .flatMapToInt(order -> order.getItems().stream().mapToInt(OrderItem::getQuantity))
    .sum();

// All character codes from all strings:
IntStream allChars = words.stream()
    .flatMapToInt(String::chars);
```

### map vs flatMap Decision Rule
```
Ask: Does each element produce ONE result → use map
     Does each element produce MULTIPLE (or zero) results → use flatMap
     Does each element produce a nested stream → use flatMap
```

---

## 9. Optional – The Stream Companion

### What is Optional?
`Optional<T>` is a container that either holds a value or is empty. It makes it explicit in the API that a value might not be present, forcing callers to handle both cases.

```java
// Without Optional — implicit null, easy to forget null check:
String name = findName(id); // might return null
System.out.println(name.toUpperCase()); // NPE if null

// With Optional — explicit emptiness:
Optional<String> name = findName(id); // clearly might be empty
name.ifPresent(n -> System.out.println(n.toUpperCase())); // safe
```

### Creating Optional

```java
Optional<String> empty   = Optional.empty();          // no value
Optional<String> present = Optional.of("Hello");      // has value, throws NPE if null
Optional<String> nullable= Optional.ofNullable(null); // null-safe, returns empty
Optional<String> nullable2 = Optional.ofNullable("Hi"); // has value
```

### Checking and Getting Values

```java
Optional<String> opt = Optional.of("Hello");

// ❌ Don't use get() without checking — throws NoSuchElementException if empty:
String val = opt.get(); // BAD — never do this without isPresent() check

// ✅ Safe ways to get values:
opt.isPresent()                              // true if has value
opt.isEmpty()                                // true if empty (Java 11+)

opt.orElse("default")                        // return default if empty
opt.orElseGet(() -> computeDefault())         // lazy default — compute only if needed
opt.orElseThrow()                            // throw NoSuchElementException if empty
opt.orElseThrow(() -> new RuntimeException()) // throw custom exception if empty

// React to presence/absence:
opt.ifPresent(v -> System.out.println(v))    // action if present
opt.ifPresentOrElse(                          // (Java 9+)
    v -> System.out.println(v),               // if present
    () -> System.out.println("empty")         // if empty
);
```

### Transforming Optional (Chaining)

```java
// map — transform value if present
Optional<String> opt = Optional.of("hello");
Optional<String> upper = opt.map(String::toUpperCase); // Optional["HELLO"]
Optional<String> empty = Optional.<String>empty().map(String::toUpperCase); // Optional.empty

// filter — keep value only if it matches condition
Optional<String> filtered = opt.filter(s -> s.length() > 3); // Optional["hello"]
Optional<String> filtered2 = opt.filter(s -> s.length() > 10); // Optional.empty

// flatMap — when the function itself returns Optional
Optional<String> city = Optional.ofNullable(user)
    .flatMap(u -> Optional.ofNullable(u.getAddress())) // User::getAddress returns Optional<Address>
    .flatMap(a -> Optional.ofNullable(a.getCity()))    // Address::getCity returns Optional<String>
    .map(String::toUpperCase);

// or — Java 9+ — provide alternative Optional if empty
Optional<String> result = opt
    .filter(s -> s.startsWith("Z"))
    .or(() -> Optional.of("default")); // if filter made it empty, use this
```

### Optional in Streams

```java
// Stream → Optional (terminal ops that return Optional):
Optional<String> first = names.stream().filter(n -> n.startsWith("A")).findFirst();
Optional<String> any   = names.stream().filter(n -> n.startsWith("A")).findAny();
Optional<Integer> max  = numbers.stream().max(Comparator.naturalOrder());
Optional<Integer> min  = numbers.stream().min(Comparator.naturalOrder());
Optional<Integer> reduced = numbers.stream().reduce(Integer::sum);

// Optional → Stream (Java 9+):
// Use to filter out empty optionals in a stream of optionals:
List<Optional<String>> opts = List.of(Optional.of("A"), Optional.empty(), Optional.of("B"));
List<String> values = opts.stream()
    .flatMap(Optional::stream) // Optional.stream() → Stream of 0 or 1 elements
    .collect(Collectors.toList()); // ["A", "B"]
```

### Optional Best Practices

```java
// ✅ Return Optional from methods that may have no result:
public Optional<Employee> findByEmail(String email) {
    return employees.stream()
        .filter(e -> e.getEmail().equals(email))
        .findFirst();
}

// ✅ Chain operations safely:
String city = findEmployee(id)
    .map(Employee::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");

// ❌ Don't use Optional as method parameter:
// BAD: public void process(Optional<String> name) { ... }
// GOOD: public void process(String name) { ... } // caller passes null or actual value

// ❌ Don't use Optional as field:
// BAD: private Optional<String> middleName;
// GOOD: private String middleName; // nullable field is fine

// ❌ Don't use Optional with collections:
// BAD: return Optional<List<String>> — use empty list instead
// GOOD: return Collections.emptyList();

// ❌ Don't call get() directly:
// BAD: opt.get() — throws exception if empty
// GOOD: opt.orElse(default) or opt.ifPresent(action)
```

---

## 10. Parallel Streams

### What are Parallel Streams?
Parallel streams split the work across multiple threads using the **ForkJoinPool** (common pool). Each thread processes a portion of the data, then results are combined.

```java
// Sequential stream — single thread
long count = names.stream().filter(n -> n.startsWith("A")).count();

// Parallel stream — multiple threads
long count = names.parallelStream().filter(n -> n.startsWith("A")).count();

// Make any existing stream parallel:
long count = names.stream().parallel().filter(n -> n.startsWith("A")).count();

// Make a parallel stream sequential again:
stream.parallel().sequential()  // switches back to sequential
```

### When to Use Parallel Streams

**✅ Good candidates for parallel:**
- Large datasets (thousands+ of elements — overhead not worth it for small lists)
- CPU-intensive operations (heavy computation per element)
- Operations that are stateless and don't depend on order
- No shared mutable state

**❌ Poor candidates for parallel:**
- Small datasets (thread overhead > benefit)
- I/O-bound operations (threads just wait — no CPU benefit)
- Operations requiring synchronization (defeats the purpose)
- Ordered operations where order matters and you need `forEachOrdered`
- Operations with side effects on shared state (race conditions)

```java
// GOOD — CPU intensive, large data, no state:
long primeCount = LongStream.rangeClosed(2, 1_000_000)
    .parallel()
    .filter(n -> isPrime(n))
    .count();

// BAD — shared mutable state (race condition):
List<String> results = new ArrayList<>(); // NOT thread-safe
names.parallelStream().forEach(results::add); // ❌ random order, potential data loss

// GOOD — collect into thread-safe result:
List<String> results = names.parallelStream()
    .filter(n -> n.length() > 3)
    .collect(Collectors.toList()); // ✅ Collectors are thread-safe
```

### Parallel Stream Ordering
```java
// Unordered (faster in parallel — no ordering cost):
names.parallelStream()
     .unordered()         // tell stream ordering doesn't matter
     .filter(...)
     .collect(Collectors.toList()); // faster

// forEachOrdered — maintains original order in parallel:
names.parallelStream()
     .forEachOrdered(System.out::println); // slower but preserves order
```

### ForkJoinPool — Customizing Thread Count
```java
// Default: Runtime.getRuntime().availableProcessors() threads

// Custom thread pool (don't pollute common pool):
ForkJoinPool customPool = new ForkJoinPool(4);
List<String> result = customPool.submit(() ->
    names.parallelStream()
         .filter(n -> n.startsWith("A"))
         .collect(Collectors.toList())
).get();
customPool.shutdown();
```

### Parallel Stream Performance Considerations
```java
// Benchmark: sequential vs parallel
// Small list (100 elements) — sequential wins (thread overhead)
// Large list (1M+ elements) with CPU work — parallel wins

// This is fast in parallel:
long sum = LongStream.rangeClosed(1, 100_000_000L)
    .parallel()
    .sum();

// This does NOT benefit from parallel (I/O bound):
List<String> data = urls.parallelStream()
    .map(url -> downloadContent(url)) // threads block waiting for network
    .collect(Collectors.toList());
// Use CompletableFuture instead for I/O bound async work
```

---

## 11. Stream with Collections – Complete Integration

### Converting Between Streams and Collections

```java
// Collection → Stream:
list.stream()
list.parallelStream()
set.stream()
map.entrySet().stream()
map.keySet().stream()
map.values().stream()

// Stream → Collection:
stream.collect(Collectors.toList())
stream.collect(Collectors.toSet())
stream.collect(Collectors.toCollection(LinkedList::new))
stream.toList()                            // Java 16+ unmodifiable

// Stream → Array:
stream.toArray(String[]::new)             // typed array
stream.toArray()                          // Object[]

// Stream → Map:
stream.collect(Collectors.toMap(k -> k, v -> v))
```

### Common Collection Operations via Streams

```java
List<Employee> employees = /* ... */;

// 1. FILTER — get a sub-list
List<Employee> engineers = employees.stream()
    .filter(e -> "Engineering".equals(e.getDepartment()))
    .collect(Collectors.toList());

// 2. TRANSFORM — map to different type
List<String> names = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.toList());

// 3. SORT — sorted copy (original unchanged)
List<Employee> sorted = employees.stream()
    .sorted(Comparator.comparing(Employee::getSalary).reversed())
    .collect(Collectors.toList());

// 4. DEDUPLICATE — unique values
List<String> uniqueDepts = employees.stream()
    .map(Employee::getDepartment)
    .distinct()
    .sorted()
    .collect(Collectors.toList());

// 5. SEARCH — find by condition
Optional<Employee> manager = employees.stream()
    .filter(e -> e.getTitle().equals("Manager"))
    .findFirst();

// 6. EXISTS — check condition
boolean hasVP = employees.stream().anyMatch(e -> e.getTitle().equals("VP"));

// 7. COUNT — count matching elements
long seniorCount = employees.stream().filter(e -> e.getYearsExp() >= 5).count();

// 8. SUM / AVG — aggregate
int totalSalary = employees.stream().mapToInt(Employee::getSalary).sum();
double avgSalary = employees.stream().mapToDouble(Employee::getSalary).average().orElse(0);

// 9. GROUP — group by field
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));

// 10. INDEX — find position (no built-in, use iterate):
OptionalInt index = IntStream.range(0, employees.size())
    .filter(i -> employees.get(i).getId() == targetId)
    .findFirst();

// 11. PARTITION — split into two groups
Map<Boolean, List<Employee>> partitioned = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 80000));

// 12. FLATTEN — merge nested lists
List<String> allSkills = employees.stream()
    .flatMap(e -> e.getSkills().stream())
    .distinct()
    .collect(Collectors.toList());
```

### Working with Maps Using Streams

```java
Map<String, Integer> scores = Map.of("Alice", 85, "Bob", 92, "Charlie", 78, "Dave", 95);

// Filter map entries:
Map<String, Integer> highScorers = scores.entrySet().stream()
    .filter(e -> e.getValue() >= 90)
    .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
// {"Bob": 92, "Dave": 95}

// Transform values:
Map<String, String> grades = scores.entrySet().stream()
    .collect(Collectors.toMap(
        Map.Entry::getKey,
        e -> e.getValue() >= 90 ? "A" : e.getValue() >= 80 ? "B" : "C"
    ));

// Sort map by value:
Map<String, Integer> sortedByScore = scores.entrySet().stream()
    .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
    .collect(Collectors.toMap(
        Map.Entry::getKey,
        Map.Entry::getValue,
        (e1, e2) -> e1,
        LinkedHashMap::new  // maintain sort order
    ));

// Invert a Map (swap key and value):
Map<Integer, String> inverted = scores.entrySet().stream()
    .collect(Collectors.toMap(Map.Entry::getValue, Map.Entry::getKey));

// Sum all values:
int totalScore = scores.values().stream().mapToInt(Integer::intValue).sum();

// Get key with max value:
Optional<String> topStudent = scores.entrySet().stream()
    .max(Map.Entry.comparingByValue())
    .map(Map.Entry::getKey);

// Convert Map to List of formatted strings:
List<String> summaries = scores.entrySet().stream()
    .map(e -> e.getKey() + ": " + e.getValue())
    .collect(Collectors.toList());
```

### Stream-Based Collection Manipulation Patterns

```java
// Remove duplicates while preserving order (LinkedHashSet trick):
List<String> deduped = new ArrayList<>(
    new LinkedHashSet<>(originalList)  // converts to set (remove dups), then back to list
);
// OR with streams:
List<String> deduped2 = originalList.stream().distinct().collect(Collectors.toList());

// Find duplicates:
Set<String> seen = new HashSet<>();
List<String> duplicates = names.stream()
    .filter(n -> !seen.add(n))  // add() returns false if already present
    .collect(Collectors.toList());

// Frequency map (count occurrences):
Map<String, Long> freq = names.stream()
    .collect(Collectors.groupingBy(n -> n, Collectors.counting()));

// Most frequent element:
String mostFrequent = freq.entrySet().stream()
    .max(Map.Entry.comparingByValue())
    .map(Map.Entry::getKey)
    .orElse(null);

// Rotate / chunk a list into batches of size N:
int batchSize = 3;
List<List<String>> batches = IntStream.range(0, (names.size() + batchSize - 1) / batchSize)
    .mapToObj(i -> names.subList(i * batchSize, Math.min((i + 1) * batchSize, names.size())))
    .collect(Collectors.toList());

// Zip two lists together (no built-in, use IntStream):
List<String> keys = List.of("a", "b", "c");
List<Integer> vals = List.of(1, 2, 3);
Map<String, Integer> zipped = IntStream.range(0, keys.size())
    .boxed()
    .collect(Collectors.toMap(keys::get, vals::get));
// {a=1, b=2, c=3}
```

---

## 12. Custom Collectors

### Collector Interface — Anatomy
```java
public interface Collector<T, A, R> {
    Supplier<A>          supplier();     // Creates the mutable container
    BiConsumer<A, T>     accumulator();  // Adds element to container
    BinaryOperator<A>    combiner();     // Merges two containers (for parallel)
    Function<A, R>       finisher();     // Converts container to final result
    Set<Characteristics> characteristics(); // Hints to runtime
}
```

```
T = type of input elements
A = type of accumulator (mutable container)
R = type of result
```

### Building a Custom Collector with Collector.of()

```java
// Custom collector: collect into an unmodifiable List
Collector<String, List<String>, List<String>> unmodifiableListCollector =
    Collector.of(
        ArrayList::new,                    // supplier: create new ArrayList
        List::add,                         // accumulator: add element
        (l1, l2) -> { l1.addAll(l2); return l1; }, // combiner: merge two lists
        Collections::unmodifiableList,     // finisher: wrap in unmodifiable
        Collector.Characteristics.UNORDERED // optional characteristics
    );

List<String> result = names.stream().collect(unmodifiableListCollector);
```

### Custom Collector: Statistics Object

```java
// Custom collector that computes running average
public class AverageCollector implements Collector<Integer, int[], Double> {
    // int[0] = sum, int[1] = count

    @Override
    public Supplier<int[]> supplier() {
        return () -> new int[]{0, 0};        // {sum=0, count=0}
    }

    @Override
    public BiConsumer<int[], Integer> accumulator() {
        return (acc, n) -> {
            acc[0] += n;  // add to sum
            acc[1]++;     // increment count
        };
    }

    @Override
    public BinaryOperator<int[]> combiner() {
        return (acc1, acc2) -> new int[]{acc1[0] + acc2[0], acc1[1] + acc2[1]};
    }

    @Override
    public Function<int[], Double> finisher() {
        return acc -> acc[1] == 0 ? 0.0 : (double) acc[0] / acc[1];
    }

    @Override
    public Set<Characteristics> characteristics() {
        return Set.of(Characteristics.UNORDERED);
    }
}

// Usage:
double avg = Stream.of(1, 2, 3, 4, 5).collect(new AverageCollector()); // 3.0
```

### Custom Collector: StringBuilder (Practical)

```java
// Custom joining collector with first-element special handling:
Collector<String, StringBuilder, String> firstUpperRestLower =
    Collector.of(
        StringBuilder::new,
        (sb, s) -> {
            if (sb.length() == 0) sb.append(s.toUpperCase());
            else sb.append(", ").append(s.toLowerCase());
        },
        (sb1, sb2) -> sb1.append(sb2),
        StringBuilder::toString
    );

String result = Stream.of("alice","BOB","CHARLIE").collect(firstUpperRestLower);
// "ALICE, bob, charlie"
```

### Characteristics
```java
// CONCURRENT — accumulator can be called from multiple threads concurrently
// UNORDERED — result doesn't depend on encounter order (can skip ordering)
// IDENTITY_FINISH — finisher is identity function (can skip finisher call)
Collector.Characteristics.CONCURRENT
Collector.Characteristics.UNORDERED
Collector.Characteristics.IDENTITY_FINISH
```

---

## 13. Stream Pitfalls & Best Practices

### Pitfall 1: Reusing a Consumed Stream
```java
Stream<String> stream = names.stream().filter(n -> n.length() > 3);
List<String> list1 = stream.collect(Collectors.toList()); // OK
List<String> list2 = stream.collect(Collectors.toList()); // ❌ IllegalStateException

// Fix: create new stream each time
List<String> list2 = names.stream().filter(n -> n.length() > 3).collect(Collectors.toList());
```

### Pitfall 2: Stateful Lambda in Parallel Streams
```java
// BAD: shared mutable state — race condition in parallel
List<String> results = new ArrayList<>();
names.parallelStream().forEach(results::add); // data loss, wrong order

// GOOD: use collect — thread-safe result building
List<String> results = names.parallelStream().collect(Collectors.toList());
```

### Pitfall 3: Forgetting Stream is Lazy
```java
// This does NOTHING — no terminal operation:
names.stream()
    .filter(n -> n.length() > 3)
    .map(String::toUpperCase);
// No result, no execution — just built a pipeline that is discarded

// GOOD: always end with terminal operation
names.stream()
    .filter(n -> n.length() > 3)
    .map(String::toUpperCase)
    .forEach(System.out::println); // terminal — now it executes
```

### Pitfall 4: Side Effects in map/filter
```java
// BAD: side effects in intermediate operations — unpredictable in parallel
int[] counter = {0};
names.stream().map(n -> { counter[0]++; return n; }); // don't modify state

// BAD: calling println in filter — confusing debug artifact
names.stream().filter(n -> { System.out.println(n); return n.length() > 3; });

// GOOD: use peek for debugging, not filter/map
names.stream()
    .peek(n -> System.out.println("before: " + n))
    .filter(n -> n.length() > 3)
    .peek(n -> System.out.println("after: " + n))
    .collect(Collectors.toList());
```

### Pitfall 5: NullPointerException in Streams
```java
// NPE when element is null:
List<String> withNulls = Arrays.asList("Alice", null, "Bob");
withNulls.stream().map(String::toUpperCase).collect(Collectors.toList()); // NPE at null

// Fix: filter nulls out:
withNulls.stream()
    .filter(Objects::nonNull)
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Fix: use Optional.ofNullable:
withNulls.stream()
    .map(n -> Optional.ofNullable(n).map(String::toUpperCase).orElse("UNKNOWN"))
    .collect(Collectors.toList());

// toMap() NPE — toMap does not allow null values!
Map<String, Integer> map = names.stream()
    .collect(Collectors.toMap(n -> n, n -> null)); // ❌ NPE in HashMap

// Fix: use HashMap directly or handle nulls
```

### Pitfall 6: collect(toList()) vs toList()
```java
Collectors.toList()   // mutable, allows null, can add/remove elements
stream.toList()       // Java 16+, UNMODIFIABLE, throws on modification
                      // Use Collectors.toList() if you need to modify result
```

### Pitfall 7: Infinite Stream Without Limit
```java
Stream.generate(() -> "A").forEach(System.out::println); // ❌ runs forever

Stream.generate(() -> "A").limit(10).forEach(System.out::println); // ✅
```

### Pitfall 8: Wrong Use of Parallel for Ordered Operations
```java
// This is slower than sequential — parallel + ordered = expensive:
names.parallelStream()
    .sorted()            // sorting requires seeing ALL elements first
    .limit(5)            // then ordered limit
    .collect(Collectors.toList()); // worse than names.stream().sorted().limit(5)
```

### Pitfall 9: Using peek for Production Logic
```java
// peek is NOT guaranteed to execute if terminal is short-circuit:
Optional<String> first = names.stream()
    .peek(n -> saveToDatabase(n)) // ❌ may not run for all elements
    .filter(n -> n.startsWith("A"))
    .findFirst();

// GOOD: don't use peek for real business logic — only debugging
```

### Best Practices

```java
// 1. Prefer method references over lambdas when clear:
.map(s -> s.toUpperCase())  →  .map(String::toUpperCase)
.filter(s -> s != null)     →  .filter(Objects::nonNull)

// 2. Use numeric streams for primitives (avoids boxing):
employees.stream().map(Employee::getSalary).reduce(0, Integer::sum) // boxing
employees.stream().mapToInt(Employee::getSalary).sum()              // no boxing ✅

// 3. Put expensive operations after cheap filters:
stream.filter(cheap)      // filter first — reduces elements
      .filter(expensive)  // then expensive check on fewer elements ✅

// 4. Avoid stream of streams — use flatMap:
stream.map(list -> list.stream())  // BAD: Stream<Stream<T>>
      .flatMap(List::stream)       // GOOD: Stream<T>

// 5. Use collect over manual forEach+add:
List<String> result = new ArrayList<>();
names.forEach(result::add);              // BAD: imperative, not idiomatic

List<String> result = names.stream()
    .collect(Collectors.toList());       // GOOD: declarative ✅

// 6. Prefer lazy evaluation — don't convert to list before streaming again:
list.stream().collect(toList()).stream() // BAD: collect then re-stream
list.stream()                           // GOOD: keep as stream ✅

// 7. Close I/O streams after use:
try (Stream<String> lines = Files.lines(path)) {
    lines.filter(...).forEach(...);
} // auto-closed ✅
```

---

## 14. Real-World Examples & Patterns

### Employee Management System — All Patterns

```java
// Domain:
record Employee(long id, String name, String department,
                double salary, int yearsExp, List<String> skills) {}

List<Employee> employees = List.of(
    new Employee(1, "Alice", "Engineering", 95000, 6, List.of("Java", "Python", "SQL")),
    new Employee(2, "Bob",   "Engineering", 75000, 2, List.of("Java", "JavaScript")),
    new Employee(3, "Carol", "Sales",       65000, 4, List.of("CRM", "Excel")),
    new Employee(4, "Dave",  "HR",          70000, 8, List.of("Recruiting", "Excel")),
    new Employee(5, "Eve",   "Engineering", 110000,10, List.of("Java", "Kubernetes", "SQL")),
    new Employee(6, "Frank", "Sales",       80000, 5, List.of("CRM", "Python"))
);
```

```java
// 1. Get names of senior engineers sorted alphabetically:
List<String> seniorEngineers = employees.stream()
    .filter(e -> "Engineering".equals(e.department()))
    .filter(e -> e.yearsExp() >= 5)
    .sorted(Comparator.comparing(Employee::name))
    .map(Employee::name)
    .collect(Collectors.toList());
// ["Alice", "Eve"]

// 2. Total salary bill per department:
Map<String, Double> salaryByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::department,
        Collectors.summingDouble(Employee::salary)
    ));
// {Engineering=280000, Sales=145000, HR=70000}

// 3. Highest paid employee per department:
Map<String, Optional<Employee>> topPaidByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::department,
        Collectors.maxBy(Comparator.comparingDouble(Employee::salary))
    ));

// 4. Average salary across all departments:
double avgSalary = employees.stream()
    .mapToDouble(Employee::salary)
    .average()
    .orElse(0.0); // 82500.0

// 5. All unique skills in the company (sorted):
List<String> allSkills = employees.stream()
    .flatMap(e -> e.skills().stream())
    .distinct()
    .sorted()
    .collect(Collectors.toList());
// [CRM, Excel, Java, JavaScript, Kubernetes, Python, Recruiting, SQL]

// 6. Skills used by more than one department:
Map<String, Set<String>> skillToDepts = employees.stream()
    .flatMap(e -> e.skills().stream().map(s -> Map.entry(s, e.department())))
    .collect(Collectors.groupingBy(
        Map.Entry::getKey,
        Collectors.mapping(Map.Entry::getValue, Collectors.toSet())
    ));
List<String> crossDeptSkills = skillToDepts.entrySet().stream()
    .filter(e -> e.getValue().size() > 1)
    .map(Map.Entry::getKey)
    .sorted()
    .collect(Collectors.toList());

// 7. Salary report: name, department, formatted salary (sorted by salary desc):
String report = employees.stream()
    .sorted(Comparator.comparingDouble(Employee::salary).reversed())
    .map(e -> String.format("%-10s %-15s $%,.0f", e.name(), e.department(), e.salary()))
    .collect(Collectors.joining("\n", "Name       Department      Salary\n", ""));

// 8. Employee count by seniority level:
Map<String, Long> countBySeniority = employees.stream()
    .collect(Collectors.groupingBy(
        e -> e.yearsExp() < 3 ? "Junior" : e.yearsExp() < 7 ? "Mid" : "Senior",
        Collectors.counting()
    ));
// {Junior=1, Mid=2, Senior=3}

// 9. Employees who know Java, grouped by department:
Map<String, List<String>> javaDevsByDept = employees.stream()
    .filter(e -> e.skills().contains("Java"))
    .collect(Collectors.groupingBy(
        Employee::department,
        Collectors.mapping(Employee::name, Collectors.toList())
    ));
// {Engineering=[Alice, Bob, Eve]}

// 10. Top N earners:
int N = 3;
List<Employee> top3 = employees.stream()
    .sorted(Comparator.comparingDouble(Employee::salary).reversed())
    .limit(N)
    .collect(Collectors.toList());

// 11. Check if all engineers know Java:
boolean allEngineersKnowJava = employees.stream()
    .filter(e -> "Engineering".equals(e.department()))
    .allMatch(e -> e.skills().contains("Java"));

// 12. Department with highest average salary:
Optional<Map.Entry<String, Double>> richestDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::department,
        Collectors.averagingDouble(Employee::salary)
    ))
    .entrySet().stream()
    .max(Map.Entry.comparingByValue());
```

### Word Frequency Analysis

```java
String text = "the quick brown fox jumps over the lazy dog the fox";

// Word frequency map:
Map<String, Long> wordFreq = Arrays.stream(text.split("\\s+"))
    .collect(Collectors.groupingBy(w -> w, Collectors.counting()));
// {the=3, fox=2, quick=1, ...}

// Top 3 most frequent words:
List<String> top3Words = wordFreq.entrySet().stream()
    .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
    .limit(3)
    .map(Map.Entry::getKey)
    .collect(Collectors.toList());
// [the, fox, quick]

// All unique words sorted:
List<String> uniqueWords = Arrays.stream(text.split("\\s+"))
    .distinct()
    .sorted()
    .collect(Collectors.toList());

// Words longer than 4 chars:
long longWords = Arrays.stream(text.split("\\s+"))
    .filter(w -> w.length() > 4)
    .distinct()
    .count();

// Character frequency:
Map<Character, Long> charFreq = text.chars()
    .filter(c -> c != ' ')
    .mapToObj(c -> (char) c)
    .collect(Collectors.groupingBy(c -> c, Collectors.counting()));
```

### Data Transformation Pipeline

```java
// E-commerce: Order processing pipeline
record Order(long id, String customer, String status, List<OrderItem> items) {}
record OrderItem(String product, int quantity, double price) {}

List<Order> orders = /* ... */;

// 1. Revenue by customer (only from completed orders):
Map<String, Double> revenueByCustomer = orders.stream()
    .filter(o -> "COMPLETED".equals(o.status()))
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.flatMapping(
            o -> o.items().stream(),
            Collectors.summingDouble(item -> item.quantity() * item.price())
        )
    ));

// 2. Products ordered more than 10 times total:
Map<String, Integer> productTotals = orders.stream()
    .flatMap(o -> o.items().stream())
    .collect(Collectors.groupingBy(
        OrderItem::product,
        Collectors.summingInt(OrderItem::quantity)
    ));

List<String> popularProducts = productTotals.entrySet().stream()
    .filter(e -> e.getValue() > 10)
    .map(Map.Entry::getKey)
    .collect(Collectors.toList());

// 3. Average order value:
OptionalDouble avgOrderValue = orders.stream()
    .mapToDouble(o -> o.items().stream()
        .mapToDouble(item -> item.quantity() * item.price())
        .sum())
    .average();
```

### Stream Chaining — Complex Pipeline

```java
// Find the department that has the most employees who know SQL,
// and return their names sorted alphabetically:
String result = employees.stream()
    .filter(e -> e.skills().contains("SQL"))
    .collect(Collectors.groupingBy(Employee::department))
    .entrySet().stream()
    .max(Comparator.comparingInt(e -> e.getValue().size()))
    .map(e -> e.getValue().stream()
        .map(Employee::name)
        .sorted()
        .collect(Collectors.joining(", ")))
    .orElse("None");
```

---

## 15. Quick-Fire Interview Q&A

### Core Concepts

**Q: What is the difference between Collection and Stream?**
A: A Collection stores data and can be iterated multiple times. A Stream does NOT store data — it processes elements from a source in a pipeline. Streams are single-use (consumed after terminal op), lazy (intermediate ops don't execute until terminal), and never modify the source. Collections support external iteration; Streams use internal iteration.

**Q: What does "lazy evaluation" mean in streams?**
A: Intermediate operations like `filter()`, `map()`, `sorted()` do not execute when called — they just register the operation in the pipeline. Execution only happens when a terminal operation (`collect`, `count`, `findFirst`, etc.) is invoked. This enables optimizations like short-circuiting (stopping early when result is found).

**Q: What is the difference between intermediate and terminal operations?**
A: Intermediate operations return a new Stream and are lazy (e.g., `filter`, `map`, `sorted`). Terminal operations consume the stream, produce a result or side effect, and close the stream (e.g., `collect`, `count`, `forEach`, `reduce`). After a terminal op, the stream cannot be reused.

**Q: What is a short-circuit operation?**
A: An operation that may not process all elements — it stops early when the result can be determined. Short-circuit intermediate: `limit`, `takeWhile`. Short-circuit terminal: `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`.

**Q: What is the difference between map and flatMap?**
A: `map` transforms each element to exactly one new element (1-to-1 transformation). `flatMap` transforms each element to zero or more elements — it takes a function that returns a Stream and merges all those streams into one (1-to-many + flatten). Use `flatMap` when you have nested collections or each element produces multiple results.

**Q: Difference between findFirst() and findAny()?**
A: Both return `Optional<T>`. `findFirst()` always returns the first element in encounter order — consistent in both sequential and parallel streams. `findAny()` returns any element — in parallel streams it may return a different element each time, but is potentially faster. For sequential streams, both usually return the same element.

**Q: What does reduce() do?**
A: `reduce` is a terminal operation that combines all stream elements into a single value using a binary operator. Example: `stream.reduce(0, Integer::sum)` sums all elements starting from 0. Without identity value, it returns `Optional<T>` (empty if stream is empty).

**Q: What is the difference between forEach and forEachOrdered?**
A: `forEach` processes elements without guaranteeing order (in parallel, elements may be processed in any order). `forEachOrdered` processes in the stream's encounter order even in parallel streams — but is slower in parallel.

**Q: When should you use parallel streams?**
A: When: dataset is large (1000+ elements), computation per element is CPU-intensive (not I/O-bound), operations are stateless (no shared mutable state), and order doesn't matter. Avoid for small data, I/O operations, or operations needing synchronization — thread overhead will hurt performance.

### Collectors

**Q: What is the difference between groupingBy and partitioningBy?**
A: Both produce a `Map`. `groupingBy` groups elements by any key (result: `Map<K, List<T>>`). `partitioningBy` divides elements into exactly two groups based on a boolean predicate (result: `Map<Boolean, List<T>>`). `partitioningBy` is more efficient for true/false splits.

**Q: What is a downstream collector in groupingBy?**
A: The second argument to `groupingBy`. Instead of collecting each group into `List<T>` (default), a downstream collector transforms each group. Examples: `counting()` counts elements per group, `summingInt(func)` sums values, `joining()` joins strings, `mapping(func, downstream)` transforms then collects.

**Q: How does toMap handle duplicate keys?**
A: `Collectors.toMap(k, v)` throws `IllegalStateException` on duplicate keys. To handle duplicates, use the 3-argument form: `Collectors.toMap(k, v, mergeFunction)` where `mergeFunction` decides which value to keep (e.g., `(existing, newVal) -> existing` keeps first, `Integer::sum` sums them).

**Q: What is collectingAndThen used for?**
A: Applies a "finisher" function after a collector completes. Common uses: wrap result in `Collections.unmodifiableList()`, apply `Optional.of()`, get the size, or any post-processing of the collected result.

**Q: What is teeing()?**
A: Java 12+ collector that applies two independent collectors to the same stream simultaneously, then merges both results. Useful when you need two different aggregations in one pass: e.g., sum and count at the same time to compute average.

### Advanced

**Q: Why are numeric streams (IntStream, etc.) preferred over Stream<Integer>?**
A: `Stream<Integer>` requires boxing every `int` into an `Integer` object (heap allocation, GC pressure). `IntStream` operates directly on primitive `int` values — faster, less memory, no boxing. Also provides aggregate methods like `sum()`, `average()`, `summaryStatistics()` that aren't on `Stream<Integer>`.

**Q: Can a stream be infinite? How do you use it safely?**
A: Yes — `Stream.generate()` and `Stream.iterate()` produce infinite streams. Use `limit(n)` to take the first N elements, or short-circuit terminals like `findFirst()`, `takeWhile()` that stop when their condition is met.

**Q: What is the Collector interface contract?**
A: It has four components: `supplier()` creates the mutable result container, `accumulator()` adds one element to the container, `combiner()` merges two containers (for parallel execution), and `finisher()` converts the container to the final result type. The `characteristics()` method provides hints like `CONCURRENT` or `UNORDERED`.

**Q: Explain the Stream pipeline execution model with lazy evaluation.**
A: When you chain intermediate operations, each operation creates a new `Stream` that wraps the previous with the new operation attached. No processing happens. When a terminal op is called, the JVM "pulls" elements one at a time through the entire pipeline — each element goes through `filter` → `map` → etc. before the next element is pulled. This vertical processing (vs batch horizontal) enables short-circuiting and infinite stream support.

**Q: What happens if you put sorted() before filter() vs after?**
A: `sorted()` requires seeing ALL elements before it can produce any (it's a "stateful" operation that buffers). If `sorted()` comes before `filter()`, it processes all N elements before filtering. If `sorted()` comes after `filter()`, only the filtered subset (smaller set) is sorted — much faster. **Always filter before sorting.**

```java
// Slow: sort 1M elements then filter to 100:
stream.sorted().filter(condition).collect(...)

// Fast: filter to 100 then sort just those:
stream.filter(condition).sorted().collect(...)
```

---

## 🎯 One-Liner Summary

| Concept | One-Liner |
|---|---|
| **Stream** | Pipeline to process data — doesn't store it |
| **Lazy evaluation** | Intermediate ops don't run until terminal op is called |
| **Short-circuit** | Stops pipeline early when result is determined |
| **filter** | Keep elements matching predicate |
| **map** | Transform each element 1-to-1 |
| **flatMap** | Transform each element to 0-many, then flatten |
| **distinct** | Remove duplicates using equals() |
| **sorted** | Sort; stateful — must see all elements |
| **limit(n)** | Take first N (short-circuits) |
| **skip(n)** | Skip first N |
| **peek** | Debug side-effect, passes elements through unchanged |
| **collect** | Terminal — gather elements into container |
| **count** | Terminal — count elements |
| **reduce** | Terminal — fold elements to single value |
| **findFirst** | Terminal — first element, short-circuits |
| **anyMatch** | Terminal — true if any matches, short-circuits |
| **allMatch** | Terminal — true if all match, short-circuits |
| **noneMatch** | Terminal — true if none match, short-circuits |
| **Collectors.toList()** | Mutable List |
| **Collectors.toSet()** | Deduplicated Set |
| **Collectors.joining()** | Concatenate strings with optional delimiter |
| **Collectors.toMap()** | Key-value map; throws on duplicate keys |
| **groupingBy** | Group by key → Map<K, List<T>> |
| **partitioningBy** | Split by boolean → Map<Boolean, List<T>> |
| **counting** | Count per group |
| **summingInt** | Sum per group |
| **averagingInt** | Average per group |
| **summarizingInt** | All stats (count, sum, min, max, avg) per group |
| **mapping** | Transform elements within a collector |
| **collectingAndThen** | Collect then apply finisher function |
| **teeing** | Two collectors in one pass, merged (Java 12+) |
| **IntStream** | Primitive int stream — no boxing, has sum/avg/etc. |
| **Optional** | Container for possibly-absent value; avoids NPE |
| **parallelStream** | ForkJoinPool multi-threaded processing |
| **Stream.generate** | Infinite stream from Supplier |
| **Stream.iterate** | Infinite sequence from seed + function |
| **Stream.concat** | Merge two streams into one |

---

*🌊 Master streams and you'll write cleaner, more declarative Java — and ace every interview question about Java 8+!*