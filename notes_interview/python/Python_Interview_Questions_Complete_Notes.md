# Python Interview Questions — Complete Notes

> One consolidated guide built from `Python_interview_questions_part1.md` (Q1–Q50) and `Python_interview_questions_part2.md` (Q51–Q100).
> Duplicates are merged, topics are ordered from fundamentals to advanced/backend, and every answer follows the same interview-ready format.
> All code targets **Python 3** (tested on **Python 3.13**; minimum versions are noted where a feature needs one).

---

## How to Use This Guide

### Answer format

Every question follows the same structure so you can revise quickly:

| Part | What it gives you |
|---|---|
| **Definition** | One or two lines you can memorize |
| **Explanation** | The concept in simple words, step by step |
| **Code** | A practical Python example |
| **Output** | What the code prints (core-Python examples were run to confirm this) |
| **🎤 Say this in the interview** | A short answer you can speak confidently |
| **Follow-ups** | Questions interviewers commonly ask next, with answers |
| **Key takeaway** | The one thing to remember |

### Priority legend

| Badge | Meaning | When to study |
|---|---|---|
| 🔴 **P1 — Must know** | Marked "Very frequent" in the source notes, or a core concept everything else builds on | Week 1 / first pass |
| 🟠 **P2 — Important** | Commonly asked; expected for mid-level roles | Second pass |
| 🟢 **P3 — Good to know** | Advanced/niche; shows depth for senior roles | Final pass |

> **Level** (Easy / Medium / Hard) and **Frequency** labels come from the original notes. They describe how often a topic tends to come up in general — they are **not** claims about any specific company.

### Suggested study order

1. **Day 1–2 (🔴 fundamentals):** Sections 1, 3, 5 — data structures, `==` vs `is`, copies, mutability, `*args/**kwargs`, mutable defaults, classes and inheritance.
2. **Day 3 (🔴 advanced core):** Section 8 — iterators, generators, decorators, context managers.
3. **Day 4 (🔴 concurrency):** Section 10 — GIL, threading vs multiprocessing vs asyncio.
4. **Day 5 (backend roles):** Sections 12–14 — FastAPI, databases, testing.
5. **Day 6:** Sections 6, 7, 9, 11, 15 (🟠/🟢 depth topics).
6. **Day before the interview:** Section 17 — Quick Revision only.

---

## Table of Contents

- [1. Data Types & Core Language Concepts](#1-data-types--core-language-concepts)
  - [1.1 List vs Tuple vs Set vs Dict](#11-list-vs-tuple-vs-set-vs-dict)
  - [1.2 Mutability and Hashability](#12-mutability-and-hashability)
  - [1.3 `==` vs `is` (and `is None`)](#13--vs-is-and-is-none)
  - [1.4 Assignment vs Shallow Copy vs Deep Copy](#14-assignment-vs-shallow-copy-vs-deep-copy)
  - [1.5 Truthy and Falsy Values](#15-truthy-and-falsy-values)
  - [1.6 `any()` vs `all()`](#16-any-vs-all)
  - [1.7 Sorting: `sorted()` vs `list.sort()`](#17-sorting-sorted-vs-listsort)
  - [1.8 f-strings](#18-f-strings)
  - [1.9 The Walrus Operator (`:=`)](#19-the-walrus-operator-)
  - [1.10 Comprehensions (List, Dict, Set, Generator)](#110-comprehensions-list-dict-set-generator)
  - [1.11 `enumerate()` and `zip()`](#111-enumerate-and-zip)
- [2. Standard Library Essentials](#2-standard-library-essentials)
  - [2.1 The `collections` Module (Counter, defaultdict, deque, namedtuple)](#21-the-collections-module-counter-defaultdict-deque-namedtuple)
  - [2.2 The `itertools` Module](#22-the-itertools-module)
  - [2.3 The `functools` Module (`lru_cache`, `partial`, `cached_property`, `wraps`, `reduce`)](#23-the-functools-module-lru_cache-partial-cached_property-wraps-reduce)
  - [2.4 Command-Line Arguments: `sys.argv` and `argparse`](#24-command-line-arguments-sysargv-and-argparse)
- [3. Functions](#3-functions)
  - [3.1 `*args` and `**kwargs`](#31-args-and-kwargs)
  - [3.2 The Mutable Default Argument Trap](#32-the-mutable-default-argument-trap)
  - [3.3 `lambda`, `map`, `filter`, `reduce`](#33-lambda-map-filter-reduce)
  - [3.4 Variable Scope: LEGB, `global`, `nonlocal`](#34-variable-scope-legb-global-nonlocal)
  - [3.5 Closures](#35-closures)
  - [3.6 Type Hints](#36-type-hints)
- [4. Exception Handling](#4-exception-handling)
  - [4.1 Exception Handling Best Practices](#41-exception-handling-best-practices)
- [5. Object-Oriented Programming (OOP)](#5-object-oriented-programming-oop)
  - [5.1 Classes, Objects, and `__init__`](#51-classes-objects-and-__init__)
  - [5.2 The Four Pillars of OOP in Python](#52-the-four-pillars-of-oop-in-python)
  - [5.3 Multiple Inheritance and MRO (Method Resolution Order)](#53-multiple-inheritance-and-mro-method-resolution-order)
  - [5.4 Composition vs Inheritance](#54-composition-vs-inheritance)
  - [5.5 Instance Method vs `@classmethod` vs `@staticmethod`](#55-instance-method-vs-classmethod-vs-staticmethod)
  - [5.6 `@property` — Getters, Setters, Computed Attributes](#56-property--getters-setters-computed-attributes)
  - [5.7 Dataclasses](#57-dataclasses)
  - [5.8 `__slots__`](#58-__slots__)
- [6. Dunder Methods & the Python Object Model](#6-dunder-methods--the-python-object-model)
  - [6.1 Dunder (Magic) Methods](#61-dunder-magic-methods)
  - [6.2 `__str__` vs `__repr__`](#62-__str__-vs-__repr__)
  - [6.3 `__eq__` and `__hash__`](#63-__eq__-and-__hash__)
  - [6.4 `__call__` and Callable Objects](#64-__call__-and-callable-objects)
  - [6.5 `__getattr__` vs `__getattribute__`](#65-__getattr__-vs-__getattribute__)
  - [6.6 Descriptors](#66-descriptors)
  - [6.7 Metaclasses](#67-metaclasses)
  - [6.8 `__init_subclass__` (Simpler Alternative to Metaclasses)](#68-__init_subclass__-simpler-alternative-to-metaclasses)
  - [6.9 `typing.Protocol` (Structural Subtyping) vs ABC](#69-typingprotocol-structural-subtyping-vs-abc)
  - [6.10 Monkey Patching](#610-monkey-patching)
- [7. Design Patterns in Python](#7-design-patterns-in-python)
  - [7.1 Singleton](#71-singleton)
  - [7.2 Factory](#72-factory)
  - [7.3 Observer (Pub/Sub, Event Emitter)](#73-observer-pubsub-event-emitter)
- [8. Iterators, Generators, Decorators & Context Managers](#8-iterators-generators-decorators--context-managers)
  - [8.1 Iterable vs Iterator (and Custom Iterators)](#81-iterable-vs-iterator-and-custom-iterators)
  - [8.2 Generators and `yield`](#82-generators-and-yield)
  - [8.3 Decorators](#83-decorators)
  - [8.4 Decorators with Arguments](#84-decorators-with-arguments)
  - [8.5 Context Managers and the `with` Statement](#85-context-managers-and-the-with-statement)
- [9. Memory Management & Python Internals](#9-memory-management--python-internals)
  - [9.1 How Python Manages Memory (Reference Counting + Garbage Collector)](#91-how-python-manages-memory-reference-counting--garbage-collector)
  - [9.2 How the Import System Works](#92-how-the-import-system-works)
- [10. Concurrency & Parallelism](#10-concurrency--parallelism)
  - [10.1 The GIL (Global Interpreter Lock)](#101-the-gil-global-interpreter-lock)
  - [10.2 Threading vs Multiprocessing vs Asyncio](#102-threading-vs-multiprocessing-vs-asyncio)
  - [10.3 `concurrent.futures`: `ThreadPoolExecutor` and `ProcessPoolExecutor`](#103-concurrentfutures-threadpoolexecutor-and-processpoolexecutor)
  - [10.4 `multiprocessing.Pool` vs `ProcessPoolExecutor`](#104-multiprocessingpool-vs-processpoolexecutor)
  - [10.5 `async`/`await` and the Event Loop](#105-asyncawait-and-the-event-loop)
  - [10.6 Blocking the Event Loop (and How to Avoid It)](#106-blocking-the-event-loop-and-how-to-avoid-it)
  - [10.7 `asyncio.Queue` and the Producer–Consumer Pattern](#107-asyncioqueue-and-the-producerconsumer-pattern)
- [11. Performance & Optimization](#11-performance--optimization)
  - [11.1 Profiling Python Code](#111-profiling-python-code)
  - [11.2 Common Performance Anti-Patterns](#112-common-performance-anti-patterns)
- [12. FastAPI & Web Backend](#12-fastapi--web-backend)
  - [12.1 What is FastAPI and How Does It Compare to Flask?](#121-what-is-fastapi-and-how-does-it-compare-to-flask)
  - [12.2 Pydantic Validation in FastAPI](#122-pydantic-validation-in-fastapi)
  - [12.3 Dependency Injection with `Depends()`](#123-dependency-injection-with-depends)
  - [12.4 Exception Handling in FastAPI](#124-exception-handling-in-fastapi)
  - [12.5 Middleware and CORS](#125-middleware-and-cors)
  - [12.6 Building a CRUD API with a Database](#126-building-a-crud-api-with-a-database)
  - [12.7 JWT Authentication](#127-jwt-authentication)
  - [12.8 Rate Limiting](#128-rate-limiting)
  - [12.9 Background Tasks](#129-background-tasks)
  - [12.10 File Uploads](#1210-file-uploads)
  - [12.11 API Versioning](#1211-api-versioning)
  - [12.12 Pagination (Offset vs Cursor)](#1212-pagination-offset-vs-cursor)
  - [12.13 Configuration and Environment Variables](#1213-configuration-and-environment-variables)
- [13. Databases, SQL & Redis](#13-databases-sql--redis)
  - [13.1 SQL JOINs (INNER, LEFT, FULL OUTER, CROSS)](#131-sql-joins-inner-left-full-outer-cross)
  - [13.2 Database Indexing](#132-database-indexing)
  - [13.3 The N+1 Query Problem](#133-the-n1-query-problem)
  - [13.4 Connection Pooling](#134-connection-pooling)
  - [13.5 Database Migrations with Alembic](#135-database-migrations-with-alembic)
  - [13.6 Transaction Isolation Levels](#136-transaction-isolation-levels)
  - [13.7 Preventing SQL Injection](#137-preventing-sql-injection)
  - [13.8 Full-Text Search in PostgreSQL](#138-full-text-search-in-postgresql)
  - [13.9 Redis and Its Data Structures](#139-redis-and-its-data-structures)
- [14. Testing](#14-testing)
  - [14.1 Writing Tests with `pytest`](#141-writing-tests-with-pytest)
  - [14.2 Fixture Scope](#142-fixture-scope)
  - [14.3 Mocking with `unittest.mock`](#143-mocking-with-unittestmock)
  - [14.4 Code Coverage](#144-code-coverage)
- [15. DevOps, Architecture & System Design](#15-devops-architecture--system-design)
  - [15.1 Docker and Containerizing a FastAPI App](#151-docker-and-containerizing-a-fastapi-app)
  - [15.2 The 12-Factor App](#152-the-12-factor-app)
  - [15.3 Designing a Task Queue (Celery)](#153-designing-a-task-queue-celery)
  - [15.4 Designing a URL Shortener](#154-designing-a-url-shortener)
  - [15.5 Debugging a Slow API Endpoint in Production](#155-debugging-a-slow-api-endpoint-in-production)
- [16. Interview Strategy & Answer Templates](#16-interview-strategy--answer-templates)
  - [16.1 General Tips](#161-general-tips)
  - [16.2 "Tell me about your most challenging technical problem" (STAR)](#162-tell-me-about-your-most-challenging-technical-problem-star)
  - [16.3 "How do you ensure code quality?"](#163-how-do-you-ensure-code-quality)
  - [16.4 "How do you handle a production incident?"](#164-how-do-you-handle-a-production-incident)
- [17. Quick Revision (Last-Minute Preparation)](#17-quick-revision-last-minute-preparation)
  - [17.1 Key Definitions (One-Liners)](#171-key-definitions-one-liners)
  - [17.2 Important Differences (Side by Side)](#172-important-differences-side-by-side)
  - [17.3 Common Pitfalls (Gotchas)](#173-common-pitfalls-gotchas)
  - [17.4 Rapid-Fire FAQ](#174-rapid-fire-faq)
  - [17.5 Top 25 Must-Know Topics (Study These First)](#175-top-25-must-know-topics-study-these-first)
- [Appendix: Source Coverage Map](#appendix-source-coverage-map)

---

## 1. Data Types & Core Language Concepts

### 1.1 List vs Tuple vs Set vs Dict

🔴 **P1** · Level: Easy · Frequency: Very frequent · *(Source: Q1)*

**Definition:** Python's four main built-in collections. They differ in **ordering**, **mutability**, and whether **duplicates** are allowed.

**Explanation:**

| Feature | `list` | `tuple` | `set` | `dict` |
|---|---|---|---|---|
| Syntax | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{"a": 1}` |
| Ordered? | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes (insertion order, Python 3.7+) |
| Mutable? | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Duplicates? | ✅ Allowed | ✅ Allowed | ❌ No | Keys ❌ unique, values ✅ |
| Indexing | `lst[0]` | `tup[0]` | ❌ Not supported | `d["key"]` |
| Membership test (`in`) | O(n) | O(n) | **O(1)** average | **O(1)** average (keys) |
| Hashable (can be dict key)? | ❌ | ✅ (if all items are hashable) | ❌ (`frozenset` ✅) | ❌ |
| Typical use | Changing sequence of items | Fixed record (e.g., coordinates) | Uniqueness, fast lookup | Key → value mapping |

```python
a = [1, 2, 2]        # list  — mutable, ordered, duplicates OK
b = (1, 2, 2)        # tuple — immutable, ordered, duplicates OK
c = {1, 2, 2}        # set   — duplicates removed
d = {"name": "Raj"}  # dict  — key-value pairs

a.append(3)
print(a)
print(b)
print(c)
print(d["name"])
print(2 in c)        # fast O(1) membership test
```

**Output:**
```text
[1, 2, 2, 3]
(1, 2, 2)
{1, 2}
Raj
True
```

#### List vs Tuple — the most common comparison

| | List | Tuple |
|---|---|---|
| Mutability | Mutable | Immutable |
| Memory | Slightly more (over-allocates for growth) | Slightly less |
| Speed | Slightly slower to create | Slightly faster to create |
| Can be a dict key? | No | Yes (if contents are hashable) |
| Meaning | "A collection of similar things" | "A fixed record" (e.g., `(lat, lon)`) |

```python
import sys

lst = [1, 2, 3]
tup = (1, 2, 3)
print(sys.getsizeof(lst) > sys.getsizeof(tup))   # tuple is smaller

locations = {(12.97, 77.59): "Bengaluru"}         # tuple as a dict key
print(locations[(12.97, 77.59)])
```

**Output:**
```text
True
Bengaluru
```

**🎤 Say this in the interview:**
> "A list is an ordered, mutable sequence; a tuple is ordered but immutable, so it's hashable and can be a dict key. A set is an unordered collection of unique items with O(1) average membership tests. A dict maps unique keys to values and keeps insertion order since Python 3.7. I use tuples for fixed records like coordinates, sets for de-duplication and fast lookups, and dicts for key-based access."

**Follow-ups:**
- **Q: When would you choose each?** — Sets for O(1) lookup/de-duplication, tuples for fixed data like coordinates or function return values, lists for ordered data that changes, dicts for lookup by key.
- **Q: Is a tuple always immutable?** — The tuple itself is, but it can contain mutable objects: `t = ([1], 2); t[0].append(5)` works. Such a tuple is **not hashable**.
- **Q: Are dicts ordered?** — Yes, insertion order is guaranteed from Python 3.7 (it was a CPython implementation detail in 3.6).

**Key takeaway:** Ordered + mutable → list. Ordered + fixed → tuple. Unique + fast lookup → set. Key → value → dict.

---

### 1.2 Mutability and Hashability

🔴 **P1** · Level: Easy · Frequency: Frequent · *(Source: Q3)*

**Definition:** A **mutable** object can be changed after creation; an **immutable** object cannot. An object is **hashable** if it has a hash value that never changes during its lifetime — which is why immutable objects can be dict keys and set members.

**Explanation:**

| Mutable | Immutable |
|---|---|
| `list`, `dict`, `set`, `bytearray`, most user-defined objects | `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes`, `None` |

- "Changing" an immutable object actually **creates a new object** (e.g., `s = s + "x"` builds a new string).
- Dicts and sets locate items by **hash**. If a key could change, its hash would change and the item would be "lost" — so mutable built-ins are unhashable.

```python
lst = [1, 2]
lst.append(3)            # OK — list is mutable
print(lst)

tup = (1, 2)
try:
    tup[0] = 9           # tuples are immutable
except TypeError as e:
    print("TypeError:", e)

try:
    d = {[1, 2]: "val"}  # lists can't be dict keys
except TypeError as e:
    print("TypeError:", e)

s = "hi"
print(id(s) == id(s + "!"))   # a new string object is created
```

**Output:**
```text
[1, 2, 3]
TypeError: 'tuple' object does not support item assignment
TypeError: unhashable type: 'list'
False
```

**🎤 Say this in the interview:**
> "Mutable objects like lists, dicts and sets can be modified in place; immutable ones like ints, strings, tuples and frozensets can't — any 'change' creates a new object. Immutable objects are hashable, which is why they can be dict keys or set members."

**Follow-ups:**
- **Q: Why does mutability matter for function arguments?** — Python passes references ("pass by object reference"). A function can modify a mutable argument in place, and the caller will see the change. Reassigning the parameter inside the function does not affect the caller.
- **Q: Is `frozenset` hashable?** — Yes, it's the immutable version of `set`.

**Key takeaway:** Immutable ⇒ hashable ⇒ usable as dict key / set member.

---

### 1.3 `==` vs `is` (and `is None`)

🔴 **P1** · Level: Easy · Frequency: Very frequent · *(Sources: Q2 + Q8 — merged)*

**Definition:** `==` checks **value equality** (calls `__eq__`). `is` checks **identity** — whether both names point to the **same object in memory** (same `id()`).

**Explanation:**
1. Two different list objects can have equal contents → `==` is `True`, `is` is `False`.
2. CPython caches small integers (**-5 to 256**) and interns some strings, so `is` may *accidentally* return `True` for equal values. This is an implementation detail — never rely on it.
3. `None` is a **singleton** (there is only one `None` object), so always check it with `is None` / `is not None`. PEP 8 recommends this explicitly. `== None` can be fooled by a class that overrides `__eq__`.

| | `==` | `is` |
|---|---|---|
| Compares | Values | Identity (memory address) |
| Can be overridden? | Yes, via `__eq__` | No |
| Use for | Comparing data | `None`, `True`/`False` singletons, sentinel objects |

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)    # same value
print(a is b)    # different objects

x = 256
y = 256
print(x is y)    # True in CPython — small ints are cached (don't rely on this!)

class Weird:
    def __eq__(self, other):
        return True          # claims to equal everything

w = Weird()
print(w == None)  # fooled by __eq__
print(w is None)  # correct
```

**Output:**
```text
True
False
True
True
False
```

**🎤 Say this in the interview:**
> "`==` compares values by calling `__eq__`, while `is` compares identity — whether both names refer to the same object. I use `==` for data comparison and `is` only for singletons like `None`. CPython caches small integers from -5 to 256, so `is` can appear to work for numbers, but that's an implementation detail."

**Follow-ups:**
- **Q: Why does `x is y` sometimes return `True` for equal ints and sometimes `False`?** — Small ints (-5..256) are cached; larger ints created at runtime are usually separate objects. Constants in the same code block may also be shared by the compiler. Behaviour varies, so use `==`.
- **Q: Why `is None` instead of `== None`?** — `None` is a singleton, `is` is faster, and it can't be overridden by a custom `__eq__`.

**Key takeaway:** `==` → "same value?" · `is` → "same object?" · Always `is None`.

---

### 1.4 Assignment vs Shallow Copy vs Deep Copy

🔴 **P1** · Level: Easy–Medium · Frequency: Frequent · *(Sources: Q4 + Q51 — merged)*

**Definition:**
- **Assignment (`=`)** creates a new **name** for the same object — no copy at all.
- **Shallow copy** creates a **new outer object**, but the nested objects inside are **shared**.
- **Deep copy** creates a **fully independent clone**, recursively copying all nested objects.

**Explanation:**

| | Assignment `b = a` | Shallow `copy.copy(a)` / `a[:]` / `list(a)` / `a.copy()` | Deep `copy.deepcopy(a)` |
|---|---|---|---|
| New outer object? | ❌ | ✅ | ✅ |
| Nested objects copied? | ❌ | ❌ (shared) | ✅ |
| `a is b` | `True` | `False` | `False` |
| Cost | O(1) | O(n) for top level | O(total size), slowest |
| Changing nested item in original affects copy? | Yes | **Yes** | No |

```python
import copy

original = [[1, 2], [3, 4]]
alias   = original                 # assignment — same object
shallow = copy.copy(original)      # new outer list, shared inner lists
deep    = copy.deepcopy(original)  # completely independent

original[0][0] = 99                # change a NESTED item
original.append([5, 6])            # change the OUTER list

print(alias)     # sees everything
print(shallow)   # sees the nested change, not the append
print(deep)      # sees nothing
print(original is alias, original is shallow, original is deep)
```

**Output:**
```text
[[99, 2], [3, 4], [5, 6]]
[[99, 2], [3, 4]]
[[1, 2], [3, 4]]
True False False
```

**🎤 Say this in the interview:**
> "Assignment just creates another reference to the same object. A shallow copy creates a new container but shares the nested objects, so modifying a nested list affects both. A deep copy recursively copies everything, so the clone is fully independent. Assignment is O(1); deepcopy is the most expensive, so I only use it when I really need independence for nested mutable data."

**Follow-ups:**
- **Q: When would deep copy cause a problem?** — Very large objects (memory/time cost), and objects that can't be copied (open files, sockets, locks). `deepcopy` handles circular references using a `memo` dict, but it's still slow.
- **Q: Does a shallow copy matter for a list of integers?** — No. Integers are immutable, so a shallow copy is effectively independent. The difference only matters for **nested mutable** objects.
- **Q: How do you customise copying for a class?** — Implement `__copy__` and `__deepcopy__`.

**Key takeaway:** Shallow = new box, same contents. Deep = new box, new contents.

---

### 1.5 Truthy and Falsy Values

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q5)*

**Definition:** Every Python object has a boolean value when used in `if`, `while`, `and`, `or`, `not`. **Falsy** values evaluate to `False`; everything else is **truthy**.

**Explanation:** Falsy values:
- `None`, `False`
- Numeric zero: `0`, `0.0`, `0j`, `Decimal(0)`
- Empty collections: `''`, `[]`, `()`, `{}`, `set()`, `range(0)`
- Objects whose `__bool__` returns `False` or whose `__len__` returns `0`

`a or b` returns the **first truthy operand** (or the last one) — not necessarily `True`/`False`. This enables the default-value pattern.

```python
if not []:    print("empty list is falsy")
if not "":    print("empty string is falsy")
if not 0:     print("zero is falsy")
if not None:  print("None is falsy")

input_name = ""                 # e.g., user left the field blank
name = input_name or "Guest"    # default-value pattern
print(name)

print(0 or [] or "first truthy")
print(bool([0]))                # a list containing 0 is NOT empty → truthy
```

**Output:**
```text
empty list is falsy
empty string is falsy
zero is falsy
None is falsy
Guest
first truthy
True
```

**🎤 Say this in the interview:**
> "Falsy values are `None`, `False`, zero of any numeric type, and empty containers. Everything else is truthy. I use this for guard clauses like `if not items: return` and for defaults like `name = value or 'Guest'`."

**Follow-ups:**
- **Q: What's the pitfall with `x or default`?** — If `0` or `""` is a *valid* value, `or` will wrongly replace it. Use `default if x is None else x` in that case.
- **Q: How do you make a custom object falsy?** — Define `__bool__` (or `__len__`).

**Key takeaway:** Empty or zero ⇒ falsy. Use `is None` when `0`/`""` are valid values.

---

### 1.6 `any()` vs `all()`

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q60)*

**Definition:** `any(iterable)` returns `True` if **at least one** element is truthy. `all(iterable)` returns `True` if **every** element is truthy. Both **short-circuit** — they stop as soon as the answer is known.

**Explanation:**

| | `any()` | `all()` |
|---|---|---|
| True when | At least one truthy | All truthy |
| Stops at | First truthy item | First falsy item |
| Empty iterable | `False` | `True` (vacuous truth — a classic gotcha) |

```python
scores = [85, 92, 78, 95, 60]

print(any(s > 90 for s in scores))    # did anyone score above 90?
print(all(s >= 60 for s in scores))   # did everyone pass?
print(all(x > 0 for x in []))         # vacuous truth — gotcha!
print(any(x > 0 for x in []))

def check(x):
    print(f"checking {x}")
    return x > 3

print(any(check(x) for x in [1, 2, 5, 6]))   # stops at 5
```

**Output:**
```text
True
True
True
False
checking 1
checking 2
checking 5
True
```

**🎤 Say this in the interview:**
> "`any` returns True if at least one element is truthy, `all` if every element is. Both short-circuit, so I pass them a generator expression rather than a list — that way evaluation stops at the first decisive element. One gotcha: `all([])` is True and `any([])` is False."

**Follow-ups:**
- **Q: Why a generator instead of a list?** — A list comprehension evaluates *every* element first, so you lose short-circuiting and use more memory.

**Key takeaway:** Pass a generator to `any`/`all`; remember `all([]) is True`.

---

### 1.7 Sorting: `sorted()` vs `list.sort()`

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q62)*

**Definition:** `sorted(iterable)` **returns a new list**; `list.sort()` sorts **in place** and returns `None`. Both use **Timsort** — O(n log n), and **stable**.

**Explanation:**
- `key=` takes a function that extracts the value to sort by.
- `reverse=True` sorts descending.
- **Stable** means equal elements keep their original relative order — this lets you sort by multiple criteria in steps.
- `operator.itemgetter` / `attrgetter` are slightly faster and cleaner than lambdas for multi-key sorts.

| | `sorted(x)` | `x.sort()` |
|---|---|---|
| Works on | Any iterable | Lists only |
| Returns | New list | `None` |
| Original changed? | No | Yes |

```python
from operator import itemgetter

users = [
    {"name": "Priya", "age": 28},
    {"name": "Raj",   "age": 25},
    {"name": "Anita", "age": 28},
]

by_age = sorted(users, key=lambda u: u["age"])
print([u["name"] for u in by_age])            # stable: Priya before Anita

by_name_desc = sorted(users, key=lambda u: u["name"], reverse=True)
print([u["name"] for u in by_name_desc])

multi = sorted(users, key=itemgetter("age", "name"))   # age, then name
print([u["name"] for u in multi])

words = ["Banana", "apple", "Cherry"]
print(sorted(words, key=str.lower))           # case-insensitive

nums = [3, 1, 2]
print(nums.sort(), nums)                      # sort() returns None
```

**Output:**
```text
['Raj', 'Priya', 'Anita']
['Raj', 'Priya', 'Anita']
['Raj', 'Anita', 'Priya']
['apple', 'Banana', 'Cherry']
None [1, 2, 3]
```

**🎤 Say this in the interview:**
> "`sorted()` returns a new list from any iterable, while `list.sort()` sorts in place and returns None. Both use Timsort, which is O(n log n) and stable. I pass a `key` function for custom ordering and use `itemgetter` for multi-key sorts."

**Follow-ups:**
- **Q: What does "stable" buy you?** — You can sort by a secondary key first, then by the primary key, and ties keep the secondary order.
- **Q: Common bug?** — `lst = lst.sort()` sets `lst` to `None`.

**Key takeaway:** New list → `sorted()`. In-place → `.sort()`. Timsort is stable.

---

### 1.8 f-strings

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q13)*

**Definition:** f-strings (formatted string literals, Python 3.6+) embed expressions directly inside strings: `f"Hello {name}"`. They are the most readable and generally the fastest way to format strings.

**Explanation:** Format spec goes after a colon: `{value:spec}`.

| Spec | Meaning | Example → result |
|---|---|---|
| `.2f` | 2 decimal places | `f"{3.14159:.2f}"` → `3.14` |
| `,` | Thousands separator | `f"{1234567:,}"` → `1,234,567` |
| `>10` / `<10` / `^10` | Right / left / centre align in width 10 | |
| `=` (3.8+) | Debug: prints `name=value` | `f"{x=}"` → `x=5` |
| `%` | Percentage | `f"{0.25:.0%}"` → `25%` |

```python
name = "Raj"
score = 95.678

print(f"Hello, {name}! Score: {score:.2f}")
print(f"2 + 2 = {2 + 2}")
print(f"{name=}")              # debug format (3.8+)

value = 1234567
print(f"{value:,}")
print(f"{score:.1f}")
print(f"[{name:>6}]")          # right-aligned in width 6
print(f"{0.25:.0%}")
```

**Output:**
```text
Hello, Raj! Score: 95.68
2 + 2 = 4
name='Raj'
1,234,567
95.7
[   Raj]
25%
```

**🎤 Say this in the interview:**
> "f-strings, available since Python 3.6, let me embed expressions directly in string literals. They're more readable and generally faster than `%` formatting or `.format()`, and they support format specs like `:.2f`, `:,` and alignment. Since 3.8, `{var=}` is handy for debugging."

**Follow-ups:**
- **Q: When should you NOT use f-strings?** — In logging calls prefer `logger.info("x=%s", x)` (lazy formatting), and **never** to build SQL queries (SQL injection — see 13.7).

**Key takeaway:** `f"{value:spec}"` — readable, fast, never for SQL.

---

### 1.9 The Walrus Operator (`:=`)

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q61)*

**Definition:** The walrus operator (`:=`, "assignment expression", Python 3.8+) **assigns a value and returns it in the same expression**, so you don't have to compute a value twice.

**Explanation:** Normal `=` is a statement and can't be used inside `if`/`while` conditions. `:=` can. Typical uses: `while` loops that read until a condition, regex matches, and comprehensions that reuse a computed value.

```python
import re

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Without walrus — len() is called twice
if len(data) > 5:
    print(f"Long list: {len(data)} items")

# With walrus — compute once
if (n := len(data)) > 5:
    print(f"Long list: {n} items")

# Regex: assign and test in one step
text = "Order ID: 12345"
if m := re.search(r"\d+", text):
    print(f"Found number: {m.group()}")

# Reading in chunks until there is nothing left
chunks = iter(["ab", "cd", ""])
while (chunk := next(chunks)) != "":
    print("chunk:", chunk)

# Reuse a computed value inside a comprehension
values = [1, 5, 9]
print([y for x in values if (y := x * 2) > 5])
```

**Output:**
```text
Long list: 10 items
Long list: 10 items
Found number: 12345
chunk: ab
chunk: cd
[10, 18]
```

A loop with random values (from the original notes) — output varies on every run:

```python
import random
while (val := random.randint(1, 10)) != 7:
    print(f"Got {val}, trying again...")
print("Got 7!")
```

**🎤 Say this in the interview:**
> "The walrus operator, added in Python 3.8, assigns a value as part of an expression. I use it to avoid computing something twice — for example in `while (line := f.readline())` loops or `if m := re.search(...)`. I don't overuse it, because readability matters more."

**Key takeaway:** `:=` = assign + use in one expression. Use only when it removes duplication.

---

### 1.10 Comprehensions (List, Dict, Set, Generator)

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q6)*

**Definition:** A comprehension builds a new collection from an iterable in a single readable expression: `[expr for item in iterable if condition]`.

**Explanation:**
- **List** `[...]`, **dict** `{k: v ...}`, **set** `{...}`, **generator** `(...)` (lazy — see 8.2).
- Usually faster than a `for` loop with `.append()`, because CPython uses a specialised bytecode instruction and avoids looking up `.append` on every iteration.
- Use them for **simple transforms/filters**. If the logic needs several lines, nested conditions, or side effects, a normal loop is more readable.

```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
word_len = {w: len(w) for w in ["python", "fast", "api"]}
unique_lens = {len(w) for w in ["hi", "hello", "hey"]}
labels = ["even" if x % 2 == 0 else "odd" for x in range(4)]   # if/else goes BEFORE for
matrix = [[1, 2], [3, 4]]
flat = [n for row in matrix for n in row]                        # nested: outer loop first
total = sum(x * x for x in range(5))                             # generator expression

print(squares)
print(evens)
print(word_len)
print(sorted(unique_lens))
print(labels)
print(flat)
print(total)
```

**Output:**
```text
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
{'python': 6, 'fast': 4, 'api': 3}
[2, 3, 5]
['even', 'odd', 'even', 'odd']
[1, 2, 3, 4]
30
```

**🎤 Say this in the interview:**
> "Comprehensions create lists, dicts, or sets in one expression. They're more concise and usually faster than a loop with append. I use them for simple transforms and filters, and switch to a regular loop when the logic gets complex — readability wins. For large data I use a generator expression so nothing is materialised in memory."

**Follow-ups:**
- **Q: Comprehension vs `map`/`filter`?** — Comprehensions are generally preferred for readability; `map` is fine when applying an existing function (`map(str, nums)`).
- **Q: Do comprehension variables leak?** — No (Python 3). The loop variable is local to the comprehension.

**Key takeaway:** Simple transform → comprehension. Complex logic → loop. Big data → generator expression.

---

### 1.11 `enumerate()` and `zip()`

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q11)*

**Definition:** `enumerate(iterable, start=0)` yields `(index, value)` pairs. `zip(*iterables)` yields tuples pairing items from several iterables. Both return **lazy iterators**.

**Explanation:**
- Replace `for i in range(len(lst))` with `enumerate` — a very common code-review fix.
- `zip` stops at the **shortest** iterable. Use `itertools.zip_longest` to keep going, or `zip(..., strict=True)` (3.10+) to raise an error if lengths differ.

```python
fruits = ["apple", "banana", "cherry"]
prices = [1.5, 2.0, 3.5]

for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

for fruit, price in zip(fruits, prices):
    print(f"{fruit}: ₹{price}")

print(list(zip([1, 2, 3], ["a", "b"])))     # stops at shortest
print(dict(zip(fruits, prices)))            # build a dict from two lists
names, costs = zip(*[("x", 1), ("y", 2)])   # "unzip"
print(names, costs)
```

**Output:**
```text
1. apple
2. banana
3. cherry
apple: ₹1.5
banana: ₹2.0
cherry: ₹3.5
[(1, 'a'), (2, 'b')]
{'apple': 1.5, 'banana': 2.0, 'cherry': 3.5}
('x', 'y') (1, 2)
```

**🎤 Say this in the interview:**
> "`enumerate` gives me the index and value together, so I never write `range(len(x))`. `zip` pairs items from multiple iterables and stops at the shortest one. Both are lazy iterators."

**Key takeaway:** Index + value → `enumerate`. Parallel iteration → `zip` (watch the shortest-length rule).

---

## 2. Standard Library Essentials

### 2.1 The `collections` Module (Counter, defaultdict, deque, namedtuple)

🟠 **P2** · Level: Easy–Medium · Frequency: Frequent · *(Sources: Q12 + Q73 — merged)*

**Definition:** `collections` provides specialised container types that extend the built-ins.

**Explanation:**

| Type | What it is | Typical use |
|---|---|---|
| `Counter` | Dict subclass that counts hashable items | Word/character frequency, top-N |
| `defaultdict` | Dict that creates a default value for missing keys | Grouping, graphs (no `KeyError`) |
| `deque` | Double-ended queue, O(1) append/pop at **both** ends | Queues, BFS, sliding windows |
| `namedtuple` | Tuple subclass with named fields | Lightweight immutable records |
| `OrderedDict` | Dict with extra ordering methods (`move_to_end`) | LRU caches; regular dicts are already ordered (3.7+) |
| `ChainMap` | Groups several dicts into one view | Layered config lookups |

```python
from collections import Counter, defaultdict, deque

words = ["hi", "hello", "hi", "world", "hi"]
print(Counter(words).most_common(2))

graph = defaultdict(list)          # no KeyError, no "if key not in dict"
graph["a"].append("b")
graph["a"].append("c")
print(dict(graph))

q = deque([1, 2, 3])
q.appendleft(0)                    # O(1) — list.insert(0, x) is O(n)
q.append(4)
print(q)
print(q.popleft(), q.pop())
```

**Output:**
```text
[('hi', 3), ('hello', 1)]
{'a': ['b', 'c']}
deque([0, 1, 2, 3, 4])
0 4
```

#### `namedtuple` and `typing.NamedTuple`

`namedtuple` creates tuple subclasses with named fields — more readable than plain tuples, lighter than full classes. The **typed** `typing.NamedTuple` form is preferred today (better IDE support and type checking).

```python
from collections import namedtuple
from typing import NamedTuple

Point = namedtuple("Point", ["x", "y"])      # classic style
p = Point(3, 4)
print(p.x, p.y)
print(p[0], p[1])                            # still a tuple
print(p._asdict())

class Coordinate(NamedTuple):                # typed style (preferred)
    latitude: float
    longitude: float
    altitude: float = 0.0

loc = Coordinate(12.9716, 77.5946)
print(loc.latitude)
print(loc)

lat, lon, alt = loc                          # unpacks like a tuple
print(alt)
```

**Output:**
```text
3 4
3 4
{'x': 3, 'y': 4}
12.9716
Coordinate(latitude=12.9716, longitude=77.5946, altitude=0.0)
0.0
```

**🎤 Say this in the interview:**
> "`collections` gives specialised containers. I use `Counter` for frequency problems, `defaultdict` to avoid the 'if key not in dict' pattern, `deque` for O(1) operations at both ends — for example BFS queues — and `NamedTuple` for small immutable records like returning multiple values from a function."

**Follow-ups:**
- **Q: `NamedTuple` vs `dataclass`?** — `NamedTuple` is immutable and behaves like a tuple (indexing, unpacking). `@dataclass` is a regular class, mutable by default, with more features (defaults via `field`, `frozen`, `slots`). See 5.7.
- **Q: Why not use a list as a queue?** — `list.pop(0)` is O(n); `deque.popleft()` is O(1).

**Key takeaway:** Counting → `Counter`. Grouping → `defaultdict`. Queue → `deque`. Immutable record → `NamedTuple`.

---

### 2.2 The `itertools` Module

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q59)*

**Definition:** `itertools` provides fast, memory-efficient building blocks that work on iterators lazily.

**Explanation:**

| Function | Does | Example result |
|---|---|---|
| `chain(a, b)` | Joins iterables end to end | `1 2 3 4` |
| `product(a, b)` | Cartesian product (nested loops) | `('A',1) ('A',2) ...` |
| `combinations(x, r)` | r-length combos, order doesn't matter | `(1,2) (1,3) (2,3)` |
| `permutations(x, r)` | r-length arrangements, order matters | `(1,2) (2,1) ...` |
| `groupby(x, key)` | Groups **consecutive** equal keys | needs sorted input! |
| `islice(it, n)` | Slices any iterator (even infinite) | |
| `count()`, `cycle()`, `repeat()` | Infinite iterators | |
| `accumulate()` | Running totals | `1 3 6` |

```python
import itertools

print(list(itertools.chain([1, 2], [3, 4], [5, 6])))
print(list(itertools.product("AB", [1, 2])))
print(list(itertools.combinations([1, 2, 3], 2)))
print(len(list(itertools.permutations([1, 2, 3], 2))))

data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))

# groupby gotcha: unsorted input creates split groups
print([k for k, _ in itertools.groupby("AABA")])

gen = itertools.count(1)                       # infinite counter
print(list(itertools.islice(gen, 5)))
print(list(itertools.accumulate([1, 2, 3])))
```

**Output:**
```text
[1, 2, 3, 4, 5, 6]
[('A', 1), ('A', 2), ('B', 1), ('B', 2)]
[(1, 2), (1, 3), (2, 3)]
6
A [('A', 1), ('A', 2)]
B [('B', 3), ('B', 4)]
['A', 'B', 'A']
[1, 2, 3, 4, 5]
[1, 3, 6]
```

**🎤 Say this in the interview:**
> "`itertools` gives lazy, memory-efficient iterator tools — `chain` to concatenate, `product`/`combinations`/`permutations` for combinatorics, `islice` to take items from any iterator, and `groupby` for grouping. The classic gotcha is that `groupby` only groups *consecutive* items, so you must sort by the key first."

**Key takeaway:** `groupby` needs sorted input. `islice` is how you slice a generator.

---

### 2.3 The `functools` Module (`lru_cache`, `partial`, `cached_property`, `wraps`, `reduce`)

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Sources: Q58 + Q92 — merged; `reduce` also in 3.3)*

**Definition:** `functools` provides higher-order functions — tools that take or return functions.

**Explanation:**

| Tool | Purpose |
|---|---|
| `@lru_cache(maxsize=N)` | Memoization: caches results by arguments, evicts **L**east **R**ecently **U**sed entries |
| `@cache` (3.9+) | Same as `lru_cache(maxsize=None)` — unbounded |
| `partial(func, ...)` | Creates a new function with some arguments pre-filled |
| `@cached_property` | Computes an attribute once per instance, then stores it |
| `@wraps(func)` | Preserves a function's metadata inside decorators (see 8.3) |
| `reduce(func, seq)` | Folds a sequence into a single value |

#### `lru_cache` — memoization

- Only safe for **pure functions** (same input → same output, no side effects).
- Arguments must be **hashable** (no lists/dicts as arguments).
- `maxsize=None` → unlimited (watch memory). `maxsize=128` → LRU eviction.
- Turns naive Fibonacci from **O(2ⁿ)** into **O(n)**.

```python
from functools import lru_cache, partial, cached_property

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))                 # instant — subproblems are cached
print(fib.cache_info())
fib.cache_clear()              # clear when underlying data changes

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(5), cube(3))

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def area(self):
        print("computing...")
        return round(3.14159 * self.radius ** 2, 2)

c = Circle(5)
print(c.area)                  # computes
print(c.area)                  # cached — no "computing..."
```

**Output:**
```text
12586269025
CacheInfo(hits=48, misses=51, maxsize=None, currsize=51)
25 27
computing...
78.54
78.54
```

A realistic use — caching a slow lookup. (The original notes built the SQL with an f-string, which is an **SQL-injection risk**; use a parameter instead.)

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def get_country_code(country_name: str) -> str:
    # db.query_sync is a placeholder for your DB helper
    return db.query_sync(
        "SELECT code FROM countries WHERE name = :name", {"name": country_name}
    )
```

**🎤 Say this in the interview:**
> "`functools` has tools for working with functions. `lru_cache` memoizes pure functions — one of the easiest performance wins in Python; it turns recursive Fibonacci from exponential to linear. `partial` pre-fills arguments, `cached_property` computes an attribute once per instance, and `wraps` keeps metadata correct in decorators."

**Follow-ups:**
- **Q: Why can't you cache a function that takes a list?** — The cache is a dict keyed by arguments; lists are unhashable. Convert to a tuple.
- **Q: Risks of `lru_cache`?** — Stale data if the source changes (call `cache_clear()`), unbounded memory with `maxsize=None`, and on methods it keeps `self` alive (can leak memory).
- **Q: `cached_property` vs `property`?** — `property` recomputes on every access; `cached_property` computes once and stores the result in the instance `__dict__`.

**Key takeaway:** Pure + repeated + hashable args → `@lru_cache`.

---

### 2.4 Command-Line Arguments: `sys.argv` and `argparse`

🟢 **P3** · Level: Easy · Frequency: Frequent · *(Source: Q63)*

**Definition:** `sys.argv` is the raw list of command-line arguments (`sys.argv[0]` is the script name). `argparse` (standard library) parses them properly, with types, defaults, validation and auto-generated `--help`.

**Explanation:** Use `sys.argv` only for trivial scripts. Use `argparse` for real tools. For large CLIs with sub-commands, the third-party `click` (or `typer`) is cleaner.

```python
import argparse

parser = argparse.ArgumentParser(description="Process data")
parser.add_argument("--input", required=True, help="Input file path")
parser.add_argument("--output", default="out.csv", help="Output file")
parser.add_argument("--verbose", action="store_true")

# parse_args() normally reads sys.argv; a list is passed here so the example runs anywhere
args = parser.parse_args(["--input", "data.csv", "--verbose"])
print(args.input, args.output, args.verbose)
```

**Output:**
```text
data.csv out.csv True
```

From a terminal: `python script.py --input data.csv --verbose` → `sys.argv` is `['script.py', '--input', 'data.csv', '--verbose']`.

**🎤 Say this in the interview:**
> "`sys.argv` gives the raw argument list. For anything real I use `argparse` from the standard library — it handles types, defaults, required flags and `--help`. For complex CLIs with sub-commands I'd reach for `click` or `typer`."

**Key takeaway:** Raw → `sys.argv`. Real CLI → `argparse`. Big CLI → `click`/`typer`.

---
## 3. Functions

### 3.1 `*args` and `**kwargs`

🔴 **P1** · Level: Easy · Frequency: Very frequent · *(Source: Q15)*

**Definition:** `*args` collects extra **positional** arguments into a **tuple**. `**kwargs` collects extra **keyword** arguments into a **dict**.

**Explanation:**
- The names `args`/`kwargs` are convention; the `*` and `**` are what matter.
- **Parameter order:** regular → `*args` → keyword-only → `**kwargs`.
- The same symbols **unpack** when calling: `f(*my_list, **my_dict)`.
- Very common in decorators and wrapper functions to forward any arguments.

```python
def greet(*args, **kwargs):
    print(type(args).__name__, args)
    print(type(kwargs).__name__, kwargs)
    for name in args:
        print(f"Hello, {name}")
    for key, val in kwargs.items():
        print(f"{key}: {val}")

greet("Raj", "Priya", role="Dev", city="Bengaluru")

def full_signature(a, b=2, *args, only_kw, **kwargs):
    print(a, b, args, only_kw, kwargs)

full_signature(1, 3, 4, 5, only_kw="x", extra=True)

nums = [1, 2]
opts = {"b": 9}
def add(a, b): return a + b
print(add(*nums), add(1, **opts))     # unpacking at call time
```

**Output:**
```text
tuple ('Raj', 'Priya')
dict {'role': 'Dev', 'city': 'Bengaluru'}
Hello, Raj
Hello, Priya
role: Dev
city: Bengaluru
1 3 (4, 5) x {'extra': True}
3 10
```

**🎤 Say this in the interview:**
> "`*args` gathers extra positional arguments into a tuple and `**kwargs` gathers extra keyword arguments into a dict. The order in a signature is regular parameters, `*args`, keyword-only parameters, then `**kwargs`. I use them mostly in decorators and wrappers to forward arguments, and the same `*`/`**` syntax unpacks sequences and dicts at call time."

**Follow-ups:**
- **Q: What's a keyword-only argument?** — Any parameter after `*args` (or after a bare `*`) must be passed by name: `def f(a, *, b)`.
- **Q: Positional-only?** — Parameters before `/` (Python 3.8+): `def f(a, /, b)` — `a` can't be passed as `a=1`.

**Key takeaway:** `*` → tuple of positionals. `**` → dict of keywords. Same symbols unpack at call time.

---

### 3.2 The Mutable Default Argument Trap

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q16)*

**Definition:** Default argument values are evaluated **once, when the function is defined** — not on each call. A mutable default (like `[]` or `{}`) is therefore **shared across all calls**.

**Explanation (step by step):**
1. `def add_item(item, lst=[])` runs → Python creates **one** list object and stores it in `add_item.__defaults__`.
2. Every call that doesn't pass `lst` reuses **that same list**.
3. Appending modifies the shared list, so items "leak" between calls.
4. **Fix:** use `None` as a sentinel and create a new list inside the function.

```python
def add_item_bad(item, lst=[]):
    lst.append(item)
    return lst

print(add_item_bad(1))
print(add_item_bad(2))                 # bug — remembers the 1
print(add_item_bad.__defaults__)       # the shared list lives here

def add_item(item, lst=None):          # GOOD — None sentinel
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(add_item(1))
print(add_item(2))
```

**Output:**
```text
[1]
[1, 2]
([1, 2],)
[1]
[2]
```

**🎤 Say this in the interview:**
> "Default values are evaluated once at function definition time, so a mutable default like an empty list is shared by every call and accumulates data. The fix is to default to `None` and create a new list inside the function."

**Follow-ups:**
- **Q: Is it ever useful?** — Occasionally as a deliberate cache, but `functools.lru_cache` is clearer.
- **Q: Does the same apply to `datetime.now()` as a default?** — Yes — it's evaluated once, so every call gets the same timestamp. Use `None` and compute inside.
- **Q: How do dataclasses avoid it?** — They forbid mutable defaults and require `field(default_factory=list)`.

**Key takeaway:** Never use a mutable default. Use `None` + create inside.

---

### 3.3 `lambda`, `map`, `filter`, `reduce`

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q17)*

**Definition:**
- `lambda` — a small **anonymous** function limited to a single expression.
- `map(func, iterable)` — applies `func` to every item (lazy).
- `filter(func, iterable)` — keeps items where `func` returns truthy (lazy).
- `functools.reduce(func, iterable[, initial])` — folds a sequence into **one value**.

**Explanation:** `map` and `filter` return **iterators** in Python 3, so wrap with `list()` to see values. Comprehensions are usually more readable; `map`/`filter` shine when you already have a named function (`map(str, nums)`).

| Tool | Comprehension equivalent |
|---|---|
| `map(lambda x: x**2, nums)` | `[x**2 for x in nums]` |
| `filter(lambda x: x % 2 == 0, nums)` | `[x for x in nums if x % 2 == 0]` |
| `reduce(lambda a, b: a + b, nums)` | `sum(nums)` |

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))
total = reduce(lambda a, b: a + b, nums)          # ((((1+2)+3)+4)+5)
product = reduce(lambda a, b: a * b, nums, 1)     # with an initial value

print(squared)
print(evens)
print(total)
print(product)
print(list(map(str, nums)))                       # named function — map is clean
print(sorted(["bb", "a", "ccc"], key=lambda s: len(s)))
```

**Output:**
```text
[1, 4, 9, 16, 25]
[2, 4]
15
120
['1', '2', '3', '4', '5']
['a', 'bb', 'ccc']
```

**🎤 Say this in the interview:**
> "A lambda is a one-expression anonymous function, typically used as a `key` for sorting. `map` transforms each item, `filter` keeps matching items, and `reduce` folds a sequence into a single value. In Python 3, map and filter are lazy. In real projects I usually prefer comprehensions for readability, but map and filter are fine in functional pipelines."

**Follow-ups:**
- **Q: Limitations of lambda?** — Single expression only, no statements, no annotations, and it shows as `<lambda>` in tracebacks. Don't assign a lambda to a name (PEP 8) — use `def`.
- **Q: Why was `reduce` moved to `functools`?** — Explicit loops or built-ins (`sum`, `max`, `any`) are usually clearer.

**Key takeaway:** Lambda = tiny anonymous function. Prefer comprehensions; `reduce` lives in `functools`.

---

### 3.4 Variable Scope: LEGB, `global`, `nonlocal`

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q18)*

**Definition:** Python resolves names using the **LEGB** rule: **L**ocal → **E**nclosing function → **G**lobal (module) → **B**uilt-in.

**Explanation:**
- **Reading** a variable searches L → E → G → B.
- **Assigning** to a name inside a function makes it **local** for the *whole* function — unless declared otherwise.
- `global x` → assignment targets the module-level `x`.
- `nonlocal y` → assignment targets `y` in the nearest enclosing function.

```python
x = 10                      # global

def outer():
    y = 20                  # enclosing
    def inner():
        nonlocal y
        global x
        x = 99              # modifies global x
        y = 88              # modifies enclosing y
    inner()
    print(y)

outer()
print(x)

counter = 0
def broken():
    try:
        counter += 1        # assignment makes 'counter' local → read fails
    except UnboundLocalError as e:
        print("UnboundLocalError:", e)

broken()
```

**Output:**
```text
88
99
UnboundLocalError: cannot access local variable 'counter' where it is not associated with a value
```

**🎤 Say this in the interview:**
> "Python looks up names in Local, Enclosing, Global, then Built-in scope — LEGB. Reading a global inside a function works, but assigning to it makes it local unless I declare `global`. `nonlocal` does the same for a variable in an enclosing function, which is how closures keep mutable state."

**Follow-ups:**
- **Q: What happens if you read a global, then assign to it in the same function?** — `UnboundLocalError`, because the assignment makes the name local for the entire function body.
- **Q: Is `global` good practice?** — Rarely. Prefer passing values and returning results, or using a class.

**Key takeaway:** LEGB for lookup; assignment makes a name local unless `global`/`nonlocal`.

---

### 3.5 Closures

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Source: Q33)*

**Definition:** A **closure** is a nested function that **remembers variables from its enclosing scope** even after the outer function has finished.

**Explanation:**
1. `make_multiplier(2)` runs and creates `multiply`, which uses `n`.
2. `make_multiplier` returns — normally `n` would be gone.
3. But `multiply` keeps a reference to `n` in its **closure cells** (`__closure__`).
4. Closures are the foundation of **decorators** (the wrapper "closes over" the original function).

```python
def make_multiplier(n):
    def multiply(x):
        return x * n          # 'n' is captured from the outer scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))
print(triple(5))
print(double.__closure__[0].cell_contents)

def make_counter():           # closure with state, using nonlocal
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = make_counter()
print(c(), c(), c())

# Late-binding gotcha: closures capture variables, not values
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
funcs = [lambda i=i: i for i in range(3)]     # fix: bind the value as a default
print([f() for f in funcs])
```

**Output:**
```text
10
15
2
1 2 3
[2, 2, 2]
[0, 1, 2]
```

**🎤 Say this in the interview:**
> "A closure is an inner function that remembers variables from the enclosing scope after that scope has finished. It's how decorators store the original function, and it's a lightweight way to keep state without a class. One gotcha is late binding — closures capture the variable, not its value at creation time."

**Follow-ups:**
- **Q: Where does a decorator store the original function?** — In a closure (the wrapper's `__closure__`).
- **Q: Closure vs class?** — A closure is lighter for one behaviour with a little state; a class is better for multiple methods or complex state.

**Key takeaway:** Closure = function + remembered enclosing variables. Watch late binding in loops.

---

### 3.6 Type Hints

🟠 **P2** · Level: Easy · Frequency: Frequent · *(Source: Q7)*

**Definition:** Type hints annotate the expected types of parameters, return values, and variables. They are **not enforced at runtime** — they're used by static checkers (mypy, pyright), IDEs, and frameworks like FastAPI/Pydantic.

**Explanation:**

| Older (`typing`) | Modern |
|---|---|
| `List[str]`, `Dict[str, int]` | `list[str]`, `dict[str, int]` (3.9+) |
| `Optional[int]` | `int \| None` (3.10+) |
| `Union[int, str]` | `int \| str` (3.10+) |

```python
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:      # older style
    return {"id": user_id} if user_id > 0 else None

def find(uid: int) -> dict | None:                  # 3.10+ style
    return None

def process(data: list[str]) -> list[str]:          # 3.9+ built-in generics
    return [d.upper() for d in data]

print(find_user(1), find(5))
print(process(["a", "b"]))
print(process.__annotations__)

def add(a: int, b: int) -> int:
    return a + b

print(add("x", "y"))       # no runtime error — hints are not enforced!
```

**Output:**
```text
{'id': 1} None
['A', 'B']
{'data': list[str], 'return': list[str]}
xy
```

**🎤 Say this in the interview:**
> "Type hints document expected types and enable static analysis with tools like mypy, plus better IDE autocomplete. Python doesn't enforce them at runtime, but frameworks like FastAPI and Pydantic read them to validate data and generate API docs. I run mypy in CI to catch type errors before runtime."

**Follow-ups:**
- **Q: Do hints slow code down?** — No meaningful runtime cost; they're stored in `__annotations__`.
- **Q: How do you enforce types at runtime?** — Pydantic models, or explicit `isinstance` checks.

**Key takeaway:** Hints = documentation + static checking, not runtime enforcement (except via Pydantic etc.).

---

## 4. Exception Handling

### 4.1 Exception Handling Best Practices

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Source: Q14)*

**Definition:** Exceptions signal errors. `try` runs code, `except` handles specific errors, `else` runs if no exception occurred, `finally` **always** runs (for cleanup).

**Explanation — best practices:**
1. Catch **specific** exceptions — never a bare `except:` (it even catches `KeyboardInterrupt`).
2. **Never swallow errors** (`except Exception: pass` hides bugs). Log or re-raise.
3. Use `finally` (or a context manager) for cleanup.
4. Create **custom exception classes** for domain errors, inheriting from a relevant built-in.
5. Use `raise NewError(...) from e` to keep the original cause in the traceback.

| Block | Runs when |
|---|---|
| `try` | Always (first) |
| `except X` | An exception of type X (or subclass) is raised |
| `else` | No exception was raised in `try` |
| `finally` | Always — even after `return` or an unhandled exception |

```python
class InsufficientFundsError(ValueError):
    def __init__(self, amount, balance):
        super().__init__(f"Need {amount}, have {balance}")
        self.amount = amount
        self.balance = balance

def withdraw(amount, balance):
    try:
        if amount > balance:
            raise InsufficientFundsError(amount, balance)
        new_balance = balance - amount
    except InsufficientFundsError:
        raise                      # re-raise — don't swallow
    else:
        print("Withdrawal OK")
        return new_balance
    finally:
        print("Transaction attempt logged")

print(withdraw(50, 100))
try:
    withdraw(500, 100)
except InsufficientFundsError as e:
    print("Error:", e, "| shortfall:", e.amount - e.balance)

try:
    int("abc")
except ValueError as e:
    try:
        raise RuntimeError("Config is invalid") from e     # exception chaining
    except RuntimeError as err:
        print(type(err.__cause__).__name__)
```

**Output:**
```text
Withdrawal OK
Transaction attempt logged
50
Transaction attempt logged
Error: Need 500, have 100 | shortfall: 400
ValueError
```

**🎤 Say this in the interview:**
> "I catch specific exceptions instead of using a bare except, I never silently swallow errors — I log or re-raise them — and I use `finally` or context managers for cleanup. For business errors I define custom exception classes, and I use `raise ... from e` to preserve the original cause."

**Follow-ups:**
- **Q: Difference between `Exception` and `BaseException`?** — `BaseException` also includes `KeyboardInterrupt`, `SystemExit` and `GeneratorExit`. Catch `Exception` at most, never `BaseException` in normal code.
- **Q: Why use `else`?** — It keeps the `try` block minimal, so you don't accidentally catch exceptions from code that shouldn't be protected.
- **Q: EAFP vs LBYL?** — Python favours **EAFP** ("Easier to Ask Forgiveness than Permission": try it and catch the error) over **LBYL** ("Look Before You Leap": check first).

**Key takeaway:** Specific `except`, never `pass`, cleanup in `finally`, custom exceptions for domain errors.

---

## 5. Object-Oriented Programming (OOP)

### 5.1 Classes, Objects, and `__init__`

🔴 **P1** · Level: Easy · Frequency: Very frequent · *(Source: Q19)*

**Definition:** A **class** is a blueprint; an **object** (instance) is a concrete thing built from it. `__init__` is the **initializer** that runs right after an object is created, to set its attributes.

**Explanation:**
- `self` is the instance the method is called on (passed automatically).
- **Instance attributes** (`self.balance`) belong to one object; **class attributes** are shared by all instances.
- Technically `__new__` **creates** the object and `__init__` **initializes** it (see Singleton, 7.1).

```python
class BankAccount:
    bank_name = "PyBank"                 # class attribute — shared

    def __init__(self, owner, balance=0):
        self.owner = owner               # instance attributes
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def __str__(self):
        return f"{self.owner}: ₹{self.balance}"

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"

acc = BankAccount("Raj", 5000)
acc.deposit(1000)
print(acc)
print(repr(acc))
print(acc.bank_name, BankAccount.bank_name)
```

**Output:**
```text
Raj: ₹6000
BankAccount(owner='Raj', balance=6000)
PyBank PyBank
```

**🎤 Say this in the interview:**
> "A class is a blueprint and an object is an instance of it. `__init__` initializes the new object's attributes, and `self` refers to the current instance. I also define `__repr__` for debugging and `__str__` for user-friendly output."

**Follow-ups:**
- **Q: Is `__init__` a constructor?** — Loosely, yes. Strictly, `__new__` constructs the object and `__init__` initializes it.
- **Q: Pitfall with class attributes?** — A mutable class attribute (e.g., `items = []`) is shared by all instances — same issue as mutable defaults.

**Key takeaway:** Class = blueprint, object = instance, `__init__` = set up attributes.

---

### 5.2 The Four Pillars of OOP in Python

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Sources: Q20, Q21, Q22, Q23 — grouped)*

| Pillar | Meaning | Python mechanism |
|---|---|---|
| **Inheritance** | Child class reuses/extends a parent | `class Dog(Animal)`, `super()` |
| **Polymorphism** | Same interface, different behaviour | Method overriding, duck typing |
| **Encapsulation** | Hide internal state, expose a controlled API | `_protected`, `__private` (name mangling), `@property` |
| **Abstraction** | Define *what* must be done, not *how* | `abc.ABC`, `@abstractmethod`, `Protocol` |

#### 5.2.1 Inheritance and Method Overriding *(Q20)*

**Definition:** Inheritance lets a child class reuse and extend a parent class. **Overriding** means the child redefines a parent method. `super()` calls the next class's version in the MRO.

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):                     # override
        return "Woof!"

class GuideDog(Dog):
    def speak(self):
        return super().speak() + " (trained)"   # extend parent behaviour

print(GuideDog().speak())
print(isinstance(GuideDog(), Animal), issubclass(GuideDog, Dog))
print([c.__name__ for c in GuideDog.__mro__])
```

**Output:**
```text
Woof! (trained)
True True
['GuideDog', 'Dog', 'Animal', 'object']
```

#### 5.2.2 Polymorphism and Duck Typing *(Q21)*

**Definition:** Polymorphism means different classes can be used through the **same interface**. Python uses **duck typing** — "if it walks like a duck and quacks like a duck, it's a duck": if an object has the right method, it works, regardless of its type.

```python
class Circle:
    def area(self): return 3.14 * 5 ** 2

class Rectangle:
    def area(self): return 4 * 6

for shape in [Circle(), Rectangle()]:    # no common base class needed
    print(shape.area())

print(len("abc"), len([1, 2]), len({"a": 1}))   # built-in polymorphism
```

**Output:**
```text
78.5
24
3 2 1
```

#### 5.2.3 Encapsulation *(Q22)*

**Definition:** Python has **no true private members**. It uses conventions:
- `_name` → "protected": internal use, by convention only.
- `__name` → **name mangling**: renamed to `_ClassName__name`, which makes accidental access and subclass clashes harder — but not impossible.

```python
class User:
    def __init__(self, name, password):
        self.name = name
        self._role = "user"              # protected by convention
        self.__password = password       # name-mangled

    def check_password(self, pwd):
        return self.__password == pwd

u = User("Raj", "secret123")
print(u.check_password("secret123"))
try:
    print(u.__password)
except AttributeError as e:
    print("AttributeError:", e)
print(u._User__password)                 # still reachable — not real privacy
```

**Output:**
```text
True
AttributeError: 'User' object has no attribute '__password'
secret123
```

#### 5.2.4 Abstraction with Abstract Base Classes *(Q23)*

**Definition:** An **abstract base class (ABC)** defines a contract — methods every subclass **must** implement. You can't instantiate an ABC, or a subclass that hasn't implemented all abstract methods.

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): ...

class UPI(Payment):
    def pay(self, amount):
        print(f"Paying ₹{amount} via UPI")

class Card(Payment):
    def pay(self, amount):
        print(f"Paying ₹{amount} via card")

try:
    Payment()
except TypeError as e:
    print("TypeError:", e)

for method in [UPI(), Card()]:
    method.pay(500)
```

**Output:**
```text
TypeError: Can't instantiate abstract class Payment without an implementation for abstract method 'pay'
Paying ₹500 via UPI
Paying ₹500 via card
```

> The exact `TypeError` wording varies slightly between Python versions.

**🎤 Say this in the interview:**
> "The four pillars are inheritance, polymorphism, encapsulation and abstraction. In Python, inheritance uses `super()` and follows the MRO; polymorphism is natural because of duck typing — I don't need interfaces like in Java. Encapsulation is by convention: a single underscore means internal, a double underscore triggers name mangling, but nothing is truly private. For abstraction I use ABCs with `@abstractmethod` to enforce a contract — for example a `Payment` base class with UPI and Card implementations."

**Follow-ups:**
- **Q: Does Python enforce private attributes?** — No. It's convention plus name mangling, not access control.
- **Q: How do you inspect method resolution?** — `ClassName.__mro__` or `ClassName.mro()` (C3 linearization — see 5.3).
- **Q: ABC vs Protocol?** — See 6.9: ABCs need explicit inheritance (nominal typing); Protocols match by structure.

**Key takeaway:** Inheritance (`super()`), polymorphism (duck typing), encapsulation (conventions), abstraction (ABCs).

---

### 5.3 Multiple Inheritance and MRO (Method Resolution Order)

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Sources: Q54 + Q20 follow-up — merged)*

**Definition:** With multiple inheritance, Python decides which parent's method to use via the **MRO**, computed by the **C3 linearization** algorithm. Inspect it with `ClassName.__mro__`.

**Explanation:**
- MRO rules: a child comes before its parents, and parents keep the order they're listed in.
- **Diamond problem:** `D(B, C)` where both `B` and `C` inherit from `A`. The MRO `D → B → C → A → object` guarantees `A` appears only **once**.
- `super()` does **not** mean "my parent". It means "**the next class in the MRO of the object's actual type**". This is what makes *cooperative* multiple inheritance work.

```python
class A:
    def greet(self): return "A"

class B(A):
    def greet(self): return "B"

class C(A):
    def greet(self): return "C"

class D(B, C):                     # inherits from B and C
    pass

print([cls.__name__ for cls in D.__mro__])
print(D().greet())                 # B comes before C in the MRO

# Cooperative super(): each class calls the NEXT class in the MRO
class A2:
    def greet(self): return "A2"

class B2(A2):
    def greet(self): return "B2 + " + super().greet()

class C2(A2):
    def greet(self): return "C2 + " + super().greet()

class D2(B2, C2):
    def greet(self): return "D2 + " + super().greet()

print(D2().greet())                # B2's super() calls C2, not A2!
```

**Output:**
```text
['D', 'B', 'C', 'A', 'object']
B
D2 + B2 + C2 + A2
```

**🎤 Say this in the interview:**
> "Python resolves methods in multiple inheritance using the MRO, computed with C3 linearization — children before parents, and parents in the order listed. In the diamond case, the shared base appears once at the end. `super()` follows the MRO of the actual object, not just the immediate parent, so in `D(B, C)`, B's `super()` call goes to C. That's what enables cooperative multiple inheritance."

**Follow-ups:**
- **Q: What if no consistent MRO exists?** — Python raises `TypeError: Cannot create a consistent method resolution order` at class creation.
- **Q: What are mixins?** — Small classes that add one behaviour (e.g., `JsonMixin`) and are combined via multiple inheritance. They should call `super()` cooperatively.

**Key takeaway:** MRO = C3 linearization; `super()` = next in MRO, not "the parent".

---

### 5.4 Composition vs Inheritance

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q65)*

**Definition:** **Inheritance** models an **"is-a"** relationship (a Dog *is an* Animal). **Composition** models a **"has-a"** relationship (a Car *has an* Engine) by holding other objects as attributes.

**Explanation:**

| | Inheritance | Composition |
|---|---|---|
| Relationship | is-a | has-a |
| Coupling | Tight (child depends on parent internals) | Loose (depends only on the part's interface) |
| Change behaviour at runtime | Hard | Easy — swap the component |
| Testing | Harder | Easier — inject a fake component |
| Risk | Deep, fragile hierarchies | More small objects to wire together |

"**Favour composition over inheritance**" is a principle from the *Design Patterns* book by the "Gang of Four".

```python
class Animal:                              # inheritance — is-a
    def breathe(self): return "breathing"

class Dog(Animal):
    def bark(self): return "woof"

print(Dog().breathe(), Dog().bark())

class Engine:                              # composition — has-a
    def start(self): return "vroom"

class ElectricEngine:
    def start(self): return "whoosh"

class Car:
    def __init__(self, engine=None):
        self.engine = engine or Engine()   # composed, not inherited

    def drive(self):
        return f"{self.engine.start()} ... driving"

print(Car().drive())
print(Car(ElectricEngine()).drive())       # swap the part — Car is unchanged
```

**Output:**
```text
breathing woof
vroom ... driving
whoosh ... driving
```

**🎤 Say this in the interview:**
> "Inheritance models is-a relationships, composition models has-a. I favour composition because it's loosely coupled — I can swap or mock components without touching the class, which also makes testing easier. I use inheritance for true is-a relationships, like custom exception hierarchies, and composition for everything else."

**Key takeaway:** is-a → inheritance; has-a → composition (default choice).

---

### 5.5 Instance Method vs `@classmethod` vs `@staticmethod`

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Source: Q27)*

**Definition:**
- **Instance method** — receives `self`; works with one object's data.
- **`@classmethod`** — receives `cls` (the class); works with class-level data, commonly used for **alternative constructors** (factory methods).
- **`@staticmethod`** — receives nothing automatically; a plain function placed in the class namespace because it's related to the class.

**Explanation:**

| | Instance method | `@classmethod` | `@staticmethod` |
|---|---|---|---|
| First argument | `self` | `cls` | none |
| Access instance data? | ✅ | ❌ | ❌ |
| Access/modify class data? | ✅ (via `type(self)`) | ✅ | ❌ |
| Works with subclasses? | ✅ | ✅ `cls` is the subclass | n/a |
| Typical use | Normal behaviour | `from_string`, `from_json`, `from_env` factories; class counters | Validation/utility helpers |

```python
class Math:
    @staticmethod
    def add(a, b):                 # no self, no cls — just a related helper
        return a + b

print(Math.add(2, 3))

class Student:
    school = "ABC School"

    @classmethod
    def change_school(cls, name):  # modifies class-level data
        cls.school = name

Student.change_school("XYZ School")
print(Student.school)

class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_string(cls, s):       # alternative constructor
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_valid(s):               # utility — needs no class or instance
        return len(s.split("-")) == 3

    def __repr__(self):
        return f"{type(self).__name__}({self.y}, {self.m}, {self.d})"

class IndianDate(Date):
    pass

print(Date.is_valid("2024-03-15"))
print(Date.from_string("2024-03-15"))
print(IndianDate.from_string("2024-03-15"))   # cls is the subclass
```

**Output:**
```text
5
XYZ School
True
Date(2024, 3, 15)
IndianDate(2024, 3, 15)
```

**🎤 Say this in the interview:**
> "An instance method gets `self` and works on one object. A classmethod gets `cls`, so it can work with class-level state, and it's the standard way to write alternative constructors like `from_string` or `from_json` — it also returns the correct subclass. A staticmethod gets neither; it's just a utility function grouped with the class because it's logically related."

**Key takeaway:** `self` → object; `cls` → class (factories); static → plain helper.

---

### 5.6 `@property` — Getters, Setters, Computed Attributes

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q26)*

**Definition:** `@property` turns a method into an attribute-style accessor, so you can add **validation** or **computed values** without changing the public API (`obj.x` instead of `obj.get_x()`).

**Explanation:** Start with a plain public attribute. If you later need validation, convert it into a property — callers don't change. `@x.setter` and `@x.deleter` add write/delete behaviour.

```python
class Temperature:
    def __init__(self, celsius=0):
        self.celsius = celsius            # goes through the setter → validated

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):                 # computed, read-only
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.fahrenheit)
t.celsius = 100
print(t.fahrenheit)
try:
    t.celsius = -300
except ValueError as e:
    print("ValueError:", e)
try:
    t.fahrenheit = 50
except AttributeError:
    print("fahrenheit is read-only")
```

**Output:**
```text
77.0
212.0
ValueError: Below absolute zero!
fahrenheit is read-only
```

**🎤 Say this in the interview:**
> "`@property` lets me expose a method as an attribute, so I can add validation or computed values while keeping a clean `obj.attr` API. It's more Pythonic than Java-style get/set methods, and I can start with a public attribute and switch to a property later without breaking callers."

**Follow-ups:**
- **Q: How does `property` work internally?** — It's a **descriptor** (see 6.6).
- **Q: `property` vs `cached_property`?** — See 2.3.

**Key takeaway:** Property = attribute syntax + method logic (validation / computed values).

---

### 5.7 Dataclasses

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Source: Q24)*

**Definition:** `@dataclass` (Python 3.7+) auto-generates `__init__`, `__repr__` and `__eq__` from annotated class fields — removing boilerplate for classes that mainly hold data.

**Explanation:**
- Mutable defaults need `field(default_factory=list)` (avoids the 3.2 trap).
- `frozen=True` → immutable and hashable (usable as dict keys; safe to share between threads).
- `order=True` → generates `<`, `>` etc. `slots=True` (3.10+) → uses `__slots__`.
- `__post_init__` → runs validation after the generated `__init__`.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    tags: list = field(default_factory=list)

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("invalid email")

u = User("Raj", "raj@example.com")
print(u)
print(u == User("Raj", "raj@example.com"))

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
print({p: "origin-ish"}[Point(1, 2)])        # frozen → hashable
try:
    p.x = 10
except Exception as e:
    print(type(e).__name__)
```

**Output:**
```text
User(name='Raj', email='raj@example.com', tags=[])
True
origin-ish
FrozenInstanceError
```

#### Comparison: plain class vs dataclass vs NamedTuple vs Pydantic

| | Plain class | `@dataclass` | `NamedTuple` | Pydantic `BaseModel` |
|---|---|---|---|---|
| Boilerplate | High | Low | Low | Low |
| Mutable | Yes | Yes (or `frozen=True`) | No | Yes (configurable) |
| Runtime type validation | No | No | No | **Yes** |
| Tuple behaviour (index/unpack) | No | No | Yes | No |
| Best for | Behaviour-heavy objects | Internal data objects | Small immutable records | External input (APIs, config) |

**🎤 Say this in the interview:**
> "`@dataclass` generates `__init__`, `__repr__` and `__eq__` from type-annotated fields, so data-holding classes need far less boilerplate. I use `field(default_factory=list)` for mutable defaults, `frozen=True` for immutable, hashable value objects, and `__post_init__` for validation. If I need runtime validation of external input, I use Pydantic instead."

**Key takeaway:** Data-holding class → `@dataclass`; immutable → `frozen=True`; validated input → Pydantic.

---

### 5.8 `__slots__`

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Sources: Q28 + Q9 tip — merged)*

**Definition:** `__slots__` declares a fixed set of attributes. Instances then store attributes in a compact fixed-size structure instead of a per-instance `__dict__`, which **reduces memory** and slightly speeds up attribute access.

**Explanation:**
- ✅ Saves memory when you create **millions** of instances.
- ❌ You can't add attributes that aren't listed.
- ❌ Inheritance is trickier (each subclass needs its own `__slots__`, or it gets a `__dict__` again); multiple inheritance from two slotted classes can conflict.
- Use only when memory profiling shows a real problem. `@dataclass(slots=True)` (3.10+) is an easy way to get it.

```python
import sys

class PointDict:
    def __init__(self, x, y):
        self.x, self.y = x, y

class PointSlots:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y

a, b = PointDict(1, 2), PointSlots(1, 2)
print(hasattr(a, "__dict__"), hasattr(b, "__dict__"))

dict_total = sys.getsizeof(a) + sys.getsizeof(a.__dict__)
print(sys.getsizeof(b) < dict_total)      # slotted instance is smaller

try:
    b.z = 3
except AttributeError as e:
    print("AttributeError:", e)
```

**Output:**
```text
True False
True
AttributeError: 'PointSlots' object has no attribute 'z' and no __dict__ for setting new attributes
```

> The `AttributeError` message wording differs slightly in older Python versions.

**🎤 Say this in the interview:**
> "`__slots__` replaces the per-instance `__dict__` with a fixed set of attribute slots, which cuts memory per instance — useful when creating millions of objects. The trade-offs are that you can't add new attributes dynamically and inheritance gets trickier, so I only use it when profiling shows memory is a real problem."

**Key takeaway:** `__slots__` = less memory, less flexibility. Use after profiling.

---
## 6. Dunder Methods & the Python Object Model

### 6.1 Dunder (Magic) Methods

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q52)*

**Definition:** Dunder ("**d**ouble **under**score") methods like `__add__` or `__len__` are special methods that Python calls **automatically** for operators, built-in functions, and statements. Implementing them lets your objects behave like built-in types.

**Explanation:**

| You write | Python calls |
|---|---|
| `obj = Cls(...)` | `__new__`, then `__init__` |
| `str(obj)`, `print(obj)` / `repr(obj)` | `__str__` / `__repr__` |
| `a + b`, `a * b` | `__add__`, `__mul__` |
| `a == b`, `a < b` | `__eq__`, `__lt__` |
| `hash(obj)`, dict key / set member | `__hash__` |
| `len(obj)`, `bool(obj)` | `__len__`, `__bool__` |
| `obj[i]`, `obj[i] = v` | `__getitem__`, `__setitem__` |
| `x in obj` | `__contains__` |
| `for x in obj` | `__iter__` / `__next__` |
| `obj()` | `__call__` |
| `with obj:` | `__enter__` / `__exit__` |

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):       # v * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __len__(self):               # len(v)
        return 2

    def __getitem__(self, idx):      # v[0]
        return (self.x, self.y)[idx]

    def __contains__(self, val):     # 3 in v
        return val in (self.x, self.y)

    def __eq__(self, other):         # v1 == v2
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)
print(v1 * 3)
print(len(v1))
print(v1[0])
print(2 in v1)
print(v1 + v2 == Vector(4, 6))
x, y = v1                            # unpacking works via __getitem__
print(x, y)
```

**Output:**
```text
Vector(4, 6)
Vector(3, 6)
2
1
True
True
1 2
```

**🎤 Say this in the interview:**
> "Dunder methods are hooks Python calls for built-in operations — `__add__` for `+`, `__len__` for `len()`, `__eq__` for `==`, `__enter__`/`__exit__` for `with`, and so on. Implementing them lets my classes behave like native types. The ones I'd always know are `__init__`, `__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, `__getitem__`, `__iter__`, `__next__`, `__call__`, `__enter__` and `__exit__`."

**Follow-ups:**
- **Q: What should `__add__` return for an unsupported type?** — `NotImplemented` (not raise), so Python can try the other operand's `__radd__`.

**Key takeaway:** Dunder methods = operator/built-in hooks that make objects feel native.

---

### 6.2 `__str__` vs `__repr__`

🔴 **P1** · Level: Easy · Frequency: Frequent · *(Source: Q25)*

**Definition:** `__str__` returns a **readable, user-facing** string (used by `print()` and `str()`). `__repr__` returns an **unambiguous, developer-facing** string (used by the REPL, `repr()`, debuggers, and inside containers) — ideally one that could recreate the object.

**Explanation:**

| | `__str__` | `__repr__` |
|---|---|---|
| Audience | End users | Developers |
| Called by | `print()`, `str()`, f-strings | `repr()`, REPL, containers (`print([obj])`), `f"{obj!r}"` |
| Fallback | Falls back to `__repr__` if not defined | Default `<Cls object at 0x...>` |
| Rule | Optional | **Always implement** |

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Point at ({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(str(p))
print(repr(p))
print([p])            # containers use __repr__
print(f"{p} | {p!r}")

class OnlyRepr:
    def __repr__(self):
        return "OnlyRepr()"

print(OnlyRepr())     # str() falls back to __repr__
```

**Output:**
```text
Point at (3, 4)
Point(x=3, y=4)
[Point(x=3, y=4)]
Point at (3, 4) | Point(x=3, y=4)
OnlyRepr()
```

**🎤 Say this in the interview:**
> "`__str__` is for end users and is what `print` shows; `__repr__` is for developers — it should be unambiguous and ideally look like the code to recreate the object. If `__str__` isn't defined, Python falls back to `__repr__`, so I always implement `__repr__` and add `__str__` only when I need a friendlier display."

**Key takeaway:** Always `__repr__`; `__str__` only when you need a pretty version.

---

### 6.3 `__eq__` and `__hash__`

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q53)*

**Definition:** `__hash__` returns an integer used to place an object in a dict or set. `__eq__` decides equality. **If you define `__eq__`, Python sets `__hash__` to `None`** (the object becomes unhashable) — so you must define `__hash__` too if you need it as a key.

**Explanation — the hash contract:**
1. If `a == b`, then `hash(a) == hash(b)` **must** be true.
2. The hash must **not change** during the object's lifetime → only hash **immutable** fields.
3. Easiest implementation: `hash(tuple_of_fields)`.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))      # hash a tuple of the fields

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)
print(p1 is p2)
seen = {p1}
print(p2 in seen)                          # works: equal hash + equal value

class OnlyEq:
    def __eq__(self, other):
        return True

print(OnlyEq.__hash__)                     # defining __eq__ removed __hash__
try:
    {OnlyEq()}
except TypeError as e:
    print("TypeError:", e)
```

**Output:**
```text
True
False
True
None
TypeError: unhashable type: 'OnlyEq'
```

**🎤 Say this in the interview:**
> "`__hash__` is what dicts and sets use to locate an object. The rule is that objects that compare equal must have the same hash, and the hash must never change. Defining `__eq__` sets `__hash__` to None, so if I need the object as a key I define `__hash__` as the hash of a tuple of its immutable fields — or simply use a frozen dataclass."

**Follow-ups:**
- **Q: What happens if you hash mutable state and then mutate it?** — The object ends up in the "wrong bucket"; lookups fail and the set/dict appears corrupted.

**Key takeaway:** Equal objects ⇒ equal hashes. Hash only immutable fields.

---

### 6.4 `__call__` and Callable Objects

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q69)*

**Definition:** Defining `__call__` makes an **instance callable like a function**: `obj(args)`. Useful for stateful functions and class-based decorators.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

double = Multiplier(2)
print(double(5))
print(callable(double))

class CountCalls:                      # class-based decorator that keeps state
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    print(f"Hello, {name}!")

greet("Raj")
greet("Priya")
print(greet.count)
```

**Output:**
```text
10
True
Call #1
Hello, Raj!
Call #2
Hello, Priya!
2
```

**🎤 Say this in the interview:**
> "`__call__` makes an object callable like a function. That's useful when a function needs to keep state between calls — for example a class-based decorator that counts calls or a configured strategy object."

**Key takeaway:** `__call__` = function behaviour + object state.

---

### 6.5 `__getattr__` vs `__getattribute__`

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q71)*

**Definition:**
- `__getattribute__` is called on **every** attribute access.
- `__getattr__` is called **only when normal lookup fails** (attribute not found).

**Explanation:**

| | `__getattribute__` | `__getattr__` |
|---|---|---|
| When called | Every access | Only for missing attributes |
| Risk | Infinite recursion if you use `self.x` inside it | Low |
| Typical use | Rare — logging/proxies | Dynamic attributes, delegation, config wrappers |

```python
class DynamicConfig:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):       # only called when normal lookup fails
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No config key: {name}")

cfg = DynamicConfig({"debug": True, "db_url": "postgresql://..."})
print(cfg.debug)
print(cfg.db_url)
try:
    cfg.missing
except AttributeError as e:
    print("AttributeError:", e)

class Logged:
    def __init__(self):
        self.value = 42

    def __getattribute__(self, name):  # called for EVERY access
        print(f"Accessing: {name}")
        return super().__getattribute__(name)   # must delegate to avoid recursion

print(Logged().value)
```

**Output:**
```text
True
postgresql://...
AttributeError: No config key: missing
Accessing: value
42
```

**🎤 Say this in the interview:**
> "`__getattr__` is a fallback called only when an attribute isn't found normally — great for dynamic attributes or delegating to a wrapped object. `__getattribute__` runs on every single access; I'd override it only for something like a proxy, and I must call `super().__getattribute__` inside it to avoid infinite recursion."

**Key takeaway:** `__getattr__` = fallback (safe). `__getattribute__` = every access (dangerous).

---

### 6.6 Descriptors

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q70)*

**Definition:** A **descriptor** is an object, stored as a **class attribute**, that defines `__get__`, `__set__` and/or `__delete__` to control how that attribute is accessed on instances. `property`, `classmethod`, `staticmethod` and regular functions (methods) are all built on descriptors.

**Explanation:**
- `__set_name__` (3.6+) tells the descriptor which attribute name it was assigned to.
- **Data descriptor** (defines `__set__`) takes priority over the instance `__dict__`.
- Use one when the **same validation logic** applies to many attributes/classes — instead of writing many near-identical properties.

```python
class NonNegativeInt:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:                        # accessed on the class itself
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{self.name} must be a non-negative int")
        obj.__dict__[self.name] = value

class Product:
    price = NonNegativeInt()                   # one reusable rule …
    quantity = NonNegativeInt()                # … for two attributes

    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

p = Product(100, 5)
print(p.price, p.quantity)
try:
    p.price = -10
except ValueError as e:
    print("ValueError:", e)
```

**Output:**
```text
100 5
ValueError: price must be a non-negative int
```

**🎤 Say this in the interview:**
> "A descriptor is a class attribute that implements `__get__`, `__set__` or `__delete__` to control attribute access. It's how `@property`, `classmethod` and bound methods work under the hood. I'd use a custom descriptor when the same validation logic needs to apply to multiple attributes across multiple classes — like ORM field types."

**Key takeaway:** Descriptor = reusable property logic; powers `property`, methods, ORM fields.

---

### 6.7 Metaclasses

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q56)*

**Definition:** A **metaclass** is the "class of a class" — it controls how **classes themselves** are created. `type` is the default metaclass of every class.

**Explanation:**
- Objects are instances of classes; classes are instances of metaclasses.
- A metaclass can modify the class at creation time: add methods, enforce rules, auto-register subclasses.
- Most real-world needs are now better served by `__init_subclass__` (6.8) or class decorators.

```python
print(type(int))
print(type(list))

class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:                          # skip the base class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class CSVPlugin(Plugin): pass
class JSONPlugin(Plugin): pass

print(PluginMeta.registry)
print(type(CSVPlugin).__name__)
```

**Output:**
```text
<class 'type'>
<class 'type'>
{'CSVPlugin': <class '__main__.CSVPlugin'>, 'JSONPlugin': <class '__main__.JSONPlugin'>}
PluginMeta
```

**🎤 Say this in the interview:**
> "A metaclass is the class of a class — `type` by default — and it controls class creation. I could use one to auto-register subclasses or enforce structure. In practice, most of those use cases are simpler with `__init_subclass__` or a class decorator, so I'd reach for those first."

**Key takeaway:** Objects ← classes ← metaclasses (`type`). Prefer `__init_subclass__`.

---

### 6.8 `__init_subclass__` (Simpler Alternative to Metaclasses)

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q57)*

**Definition:** `__init_subclass__` (Python 3.6+) is a classmethod hook on a base class that runs **every time the class is subclassed**. It covers most metaclass use cases with far less complexity.

```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls
        print(f"Registered plugin: {name}")

class CSVPlugin(Plugin, plugin_name="csv"):
    pass

class JSONPlugin(Plugin, plugin_name="json"):
    pass

print(Plugin._registry)
```

**Output:**
```text
Registered plugin: csv
Registered plugin: json
{'csv': <class '__main__.CSVPlugin'>, 'json': <class '__main__.JSONPlugin'>}
```

| | Metaclass | `__init_subclass__` |
|---|---|---|
| Complexity | High | Low |
| Conflicts | Two metaclasses in one hierarchy can clash | None |
| Can customise the base class itself | Yes | No (only subclasses) |
| Can change how the class is constructed (namespace, `__call__`) | Yes | No |

**🎤 Say this in the interview:**
> "`__init_subclass__` runs whenever a class is subclassed, so I can register plugins or validate subclasses without writing a metaclass. It's simpler, more readable, and avoids metaclass conflicts. I'd only use a real metaclass if I needed to control class construction itself."

**Key takeaway:** Subclass hooks → `__init_subclass__` first, metaclass last.

---

### 6.9 `typing.Protocol` (Structural Subtyping) vs ABC

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Sources: Q74 + Q23 — compared)*

**Definition:** A `Protocol` (Python 3.8+) defines an interface by **structure**: any class that has the required methods satisfies it — **no inheritance needed**. This is "duck typing with type checking".

**Explanation:**

| | ABC (`abc.ABC`) | `typing.Protocol` |
|---|---|---|
| Typing style | Nominal — must inherit | Structural — just have the methods |
| Enforced at instantiation | ✅ (`TypeError` if methods missing) | ❌ (checked by mypy/pyright) |
| `isinstance` support | ✅ | Only with `@runtime_checkable` (checks method **names** only) |
| Best for | Owning a class hierarchy, sharing base code | Loosely coupled code, third-party classes |

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...
    def area(self) -> float: ...

class Circle:                            # no inheritance from Drawable
    def draw(self): print("Drawing circle")
    def area(self): return 3.14 * 5 ** 2

class Square:
    def draw(self): print("Drawing square")
    def area(self): return 4 * 4

def render(shape: Drawable) -> None:
    shape.draw()
    print(f"Area: {shape.area()}")

render(Circle())
render(Square())
print(isinstance(Circle(), Drawable))
print(isinstance("text", Drawable))
```

**Output:**
```text
Drawing circle
Area: 78.5
Drawing square
Area: 16
True
False
```

**🎤 Say this in the interview:**
> "A Protocol defines an interface structurally — any class with matching methods satisfies it, without inheriting from it. It's duck typing that static type checkers understand. I prefer Protocols for loosely coupled code, because the implementer doesn't need to know my interface exists, and ABCs when I own the hierarchy and want enforcement at instantiation."

**Key takeaway:** ABC = "inherit from me". Protocol = "look like me".

---

### 6.10 Monkey Patching

🟢 **P3** · Level: Medium · Frequency: Frequent · *(Source: Q55)*

**Definition:** **Monkey patching** means modifying a class, module or object **at runtime** — replacing or adding attributes/methods without changing the original source code. It's most common in **tests**.

**Explanation:**
- Risky in production: behaviour changes globally and invisibly.
- In tests, prefer **scoped** patching that undoes itself: `unittest.mock.patch` or pytest's `monkeypatch` fixture.
- Note: you cannot set attributes on built-in types like `datetime.datetime` itself (e.g., `datetime.datetime.now = ...` fails), so you patch the **name** a module uses instead.

```python
class Greeter:
    def greet(self):
        return "Hello"

def patched_greet(self):
    return "Patched hello"

original = Greeter.greet
Greeter.greet = patched_greet            # monkey patch at runtime
print(Greeter().greet())
Greeter.greet = original                 # always restore!
print(Greeter().greet())

import datetime
try:
    datetime.datetime.now = lambda: None
except TypeError as e:
    print("TypeError:", e)
```

**Output:**
```text
Patched hello
Hello
TypeError: cannot set 'now' attribute of immutable type 'datetime.datetime'
```

The safer, test-scoped way with pytest (snippet — requires `pytest`; `myapp.orders` is a placeholder module that does `import datetime` and calls `datetime.datetime.now()`):

```python
import datetime
import myapp.orders

class FakeDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2024, 1, 1, 12, 0, 0)

def test_order_timestamp(monkeypatch):
    # Replace the name 'datetime' that myapp.orders uses; undone automatically after the test
    monkeypatch.setattr(myapp.orders.datetime, "datetime", FakeDatetime)
    assert myapp.orders.create_order().created_at.year == 2024
```

**🎤 Say this in the interview:**
> "Monkey patching is changing a class or module at runtime without touching its source. It's useful in tests to fake things like the current time or an external API, but I avoid it in production because it makes behaviour hard to reason about. In tests I use `unittest.mock.patch` or pytest's `monkeypatch`, which undo the change automatically."

**Key takeaway:** Patch in tests with `mock.patch`/`monkeypatch`, not globally in production.

---

## 7. Design Patterns in Python

### 7.1 Singleton

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q66)*

**Definition:** The **Singleton** pattern ensures a class has **only one instance** and provides a global access point to it.

**Explanation — three ways in Python:**

| Approach | How | Notes |
|---|---|---|
| Module-level instance | Create the object in a module and import it | **Most Pythonic** — modules are cached in `sys.modules`, so the code runs once |
| `__new__` override | Return the stored instance if one exists | Note: `__init__` still runs on every call |
| Decorator | Wrap the class in a function that caches the instance | The name now refers to a function, not a class (breaks `isinstance`) |

```python
# Method 1 — __new__
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)

# Method 2 — module level (in a file config.py):
class _Config:
    debug = False
    db_url = "postgresql://..."

config = _Config()        # other modules do: from config import config

# Method 3 — decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Connecting once")

print(Database() is Database())
```

**Output:**
```text
True
Connecting once
True
```

**🎤 Say this in the interview:**
> "A singleton guarantees one instance. In Python the most Pythonic version is just a module-level object, because imports are cached in `sys.modules`, so the module runs once. I can also override `__new__` or use a decorator. Singletons are global state, though, so in apps like FastAPI I'd usually prefer dependency injection."

**Follow-ups:**
- **Q: Is the `__new__` version thread-safe?** — Not strictly; two threads could create instances simultaneously. Guard creation with a `threading.Lock` if needed.

**Key takeaway:** Pythonic singleton = module-level instance.

---

### 7.2 Factory

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q67)*

**Definition:** The **Factory** pattern creates objects **without the caller naming the exact class**. The factory decides which class to instantiate based on input or configuration.

**Explanation:** A **dict mapping** names to classes is more Pythonic and extensible than a long `if/elif` chain — adding a new type means adding one entry.

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str): ...

class EmailNotification(Notification):
    def send(self, message): print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message): print(f"SMS: {message}")

class PushNotification(Notification):
    def send(self, message): print(f"Push: {message}")

class NotificationFactory:
    _types = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, ntype: str) -> Notification:
        if ntype not in cls._types:
            raise ValueError(f"Unknown type: {ntype}")
        return cls._types[ntype]()

NotificationFactory.create("email").send("Your order shipped!")
NotificationFactory.create("sms").send("OTP is 1234")
try:
    NotificationFactory.create("fax")
except ValueError as e:
    print("ValueError:", e)
```

**Output:**
```text
Email: Your order shipped!
SMS: OTP is 1234
ValueError: Unknown type: fax
```

**🎤 Say this in the interview:**
> "A factory creates objects without the caller knowing the concrete class. I usually implement it with a dict that maps a type name to a class — that's more Pythonic than an if/elif chain, and adding a new type doesn't require changing the factory logic. Combined with an ABC, every product is guaranteed to have the same interface."

**Key takeaway:** Factory = name → class lookup; caller depends only on the interface.

---

### 7.3 Observer (Pub/Sub, Event Emitter)

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q68)*

**Definition:** The **Observer** pattern lets objects **subscribe** to events and be **notified automatically** when they happen. It decouples the event producer from the reactions.

```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

class OrderService(EventEmitter):
    def place_order(self, order):
        print(f"Order placed: {order['id']}")
        self.emit("order_placed", order)

service = OrderService()
service.on("order_placed", lambda o: print(f"Send email for {o['id']}"))
service.on("order_placed", lambda o: print(f"Update inventory for {o['item']}"))
service.on("order_placed", lambda o: print(f"Notify warehouse for {o['id']}"))

service.place_order({"id": 42, "item": "Laptop"})
```

**Output:**
```text
Order placed: 42
Send email for 42
Update inventory for Laptop
Notify warehouse for 42
```

**🎤 Say this in the interview:**
> "The observer pattern lets subscribers register for events and get notified when they fire, so the producer doesn't need to know who reacts. For example, an order service just emits `order_placed`, and email, inventory and warehouse handlers subscribe independently. Event systems, signals and message queues are larger-scale versions of the same idea."

**Follow-ups:**
- **Q: Real-world examples?** — Django signals, GUI event handlers, and framework lifecycle hooks. (FastAPI's older `@app.on_event("startup")` hooks are now deprecated in favour of a `lifespan` context manager.) At system scale: Redis Pub/Sub, Kafka.

**Key takeaway:** Observer = subscribe/notify; decouples "what happened" from "who reacts".

---
## 8. Iterators, Generators, Decorators & Context Managers

### 8.1 Iterable vs Iterator (and Custom Iterators)

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Sources: Q32 + Q72 — merged)*

**Definition:**
- An **iterable** is any object you can loop over. It implements `__iter__()`, which returns a **new iterator**. Examples: list, tuple, str, dict, set, range.
- An **iterator** is the object that does the actual stepping. It implements **both** `__iter__()` (returning itself) and `__next__()` (returning the next value, or raising `StopIteration` when done). It **remembers its position** and is **consumed** after one pass.

**Explanation — what a `for` loop really does:**
1. Calls `iter(obj)` → gets an iterator.
2. Repeatedly calls `next(iterator)`.
3. Stops when `StopIteration` is raised.

| | Iterable | Iterator |
|---|---|---|
| Methods | `__iter__` | `__iter__` **and** `__next__` |
| Keeps position/state? | No | Yes |
| Can loop over it again? | ✅ Yes (each loop gets a fresh iterator) | ❌ No — exhausted after one pass |
| Examples | `list`, `str`, `dict`, `range` | `iter(list)`, file objects, generators, `map`, `zip` |

```python
lst = [1, 2, 3]            # iterable
it = iter(lst)             # iterator
print(next(it), next(it), next(it))
try:
    next(it)
except StopIteration:
    print("exhausted")

print(list(lst), list(lst))          # iterable: can loop again
gen = (x**2 for x in range(3))       # generators are iterators
print(list(gen), list(gen))          # second pass is empty!
print(iter(gen) is gen)              # an iterator's __iter__ returns itself

class CountDown:                     # custom ITERATOR
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

print(list(CountDown(5)))

class Range:                         # custom ITERABLE (re-usable)
    def __init__(self, start, stop):
        self.start, self.stop = start, stop
    def __iter__(self):              # generator function → new iterator each time
        current = self.start
        while current < self.stop:
            yield current
            current += 1

r = Range(1, 4)
print(list(r), list(r))
```

**Output:**
```text
1 2 3
exhausted
[1, 2, 3] [1, 2, 3]
[0, 1, 4] []
True
[5, 4, 3, 2, 1]
[1, 2, 3] [1, 2, 3]
```

**🎤 Say this in the interview:**
> "An iterable is anything that can give me an iterator through `__iter__` — like a list. An iterator implements `__next__`, keeps track of its position, and raises StopIteration when it's done. A for loop calls `iter()` once and then `next()` repeatedly. The key test: an iterable can be looped over again, but an exhausted iterator can't. Generators are iterators."

**Follow-ups:**
- **Q: Is a list an iterator?** — No, it's an iterable. `next([1, 2])` raises `TypeError`.
- **Q: How do you make a reusable custom iterable?** — Make `__iter__` a generator function (as in `Range`) so each loop gets a fresh iterator.

**Key takeaway:** Iterable = can produce an iterator. Iterator = has `__next__`, single-use.

---

### 8.2 Generators and `yield`

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q31)*

**Definition:** A **generator** is a function that uses `yield` to produce values **lazily** — one at a time, on demand — pausing its state between values. Calling it returns a **generator object** (which is an iterator).

**Explanation (step by step):**
1. Calling a generator function runs **no code** yet — it returns a generator object.
2. Each `next()` runs the function until the next `yield`, returns that value, and **pauses** (local variables are kept).
3. When the function ends, `StopIteration` is raised.
4. Only one value exists in memory at a time → ideal for large files, streams, infinite sequences, and ETL pipelines.

```python
def fibonacci():
    a, b = 0, 1
    while True:                       # infinite — fine, because it's lazy
        yield a
        a, b = b, a + b

gen = fibonacci()
print([next(gen) for _ in range(8)])

def steps():
    print("start")
    yield 1
    print("resumed")
    yield 2

g = steps()                           # nothing printed yet
print("created")
print(next(g))
print(next(g))

import sys
big_list = [x for x in range(1_000_000)]
big_gen = (x for x in range(1_000_000))
print(sys.getsizeof(big_gen) < 1000 < sys.getsizeof(big_list))

def numbers():                        # generator pipeline
    yield from range(10)
evens = (n for n in numbers() if n % 2 == 0)
squares = (n * n for n in evens)
print(sum(squares))
```

**Output:**
```text
[0, 1, 1, 2, 3, 5, 8, 13]
created
start
1
resumed
2
True
120
```

Reading a large file line by line (snippet — needs a real file path):

```python
def read_large_file(path):
    with open(path) as f:
        for line in f:            # file objects are lazy iterators too
            yield line.strip()    # one line in memory at a time
```

#### Generator vs Iterator vs List

| | List | Iterator class | Generator |
|---|---|---|---|
| Memory | Stores all items | One item at a time | One item at a time |
| How you write it | `[...]` | Class with `__iter__` + `__next__` | Function with `yield`, or `(...)` expression |
| Boilerplate | None | High | Low |
| Re-iterable | ✅ | ❌ | ❌ |
| Random access `x[i]` | ✅ | ❌ | ❌ |

> **Every generator is an iterator, but not every iterator is a generator.** A generator is simply the easiest way to write an iterator.

**🎤 Say this in the interview:**
> "A generator is a function that uses `yield` to produce values lazily, pausing its state between each value. It's an iterator, but much less code than writing a class with `__next__`. Because only one item is in memory at a time, I use generators for large files, streaming data and ETL pipelines where loading everything would run out of memory."

**Follow-ups:**
- **Q: `yield` vs `return`?** — `return` ends the function and sends back one value; `yield` produces a value and pauses, so the function can resume.
- **Q: What is `yield from`?** — Delegates to a sub-iterator/generator: `yield from range(10)`.
- **Q: Generator expression vs list comprehension?** — `( )` is lazy and memory-light; `[ ]` builds the full list immediately.

**Key takeaway:** `yield` = lazy, paused function. Generators are the easy way to write iterators.

---

### 8.3 Decorators

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q29)*

**Definition:** A **decorator** is a function that takes a function and returns a new function that **adds behaviour** (logging, timing, caching, auth) **without changing the original code**. `@decorator` above `def f` is shorthand for `f = decorator(f)`.

**Explanation (step by step):**
1. Functions are first-class objects — they can be passed and returned.
2. The decorator defines an inner `wrapper(*args, **kwargs)` that runs extra code around `func(...)`.
3. `wrapper` is a **closure** — it remembers `func`.
4. Always use `@functools.wraps(func)` so the wrapper keeps the original `__name__`, `__doc__`, etc.

```python
import functools

def log_calls(func):
    @functools.wraps(func)                     # preserve metadata
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b

add(2, 3)
print(add.__name__, "|", add.__doc__)

def no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@no_wraps
def hello():
    """Say hello."""

print(hello.__name__, "|", hello.__doc__)     # metadata lost without wraps
```

**Output:**
```text
Calling add(2, 3)
add returned 5
add | Add two numbers.
wrapper | None
```

The timing decorator from the original notes (output varies):

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_task():
    time.sleep(0.1)

slow_task()
```

**Output (timing varies):**
```console
slow_task took 0.1003s
```

**🎤 Say this in the interview:**
> "A decorator is a function that wraps another function to add behaviour — like logging, timing, caching or authentication — without modifying it. `@decorator` is syntactic sugar for `func = decorator(func)`. The wrapper is a closure over the original function, and I always use `functools.wraps` so the name and docstring are preserved for debugging and tools."

**Follow-ups:**
- **Q: Built-in decorators you use?** — `@property`, `@classmethod`, `@staticmethod`, `@functools.lru_cache`, `@dataclass`, `@contextmanager`; framework ones like `@app.get` (FastAPI) and `@pytest.fixture`.
- **Q: Order of stacked decorators?** — Applied bottom-up: `@a @b def f` → `f = a(b(f))`. The top decorator runs first when called.
- **Q: Class-based decorator?** — Use `__call__` (see 6.4) when you need state.

**Key takeaway:** Decorator = wrapper closure + `@functools.wraps`.

---

### 8.4 Decorators with Arguments

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q30)*

**Definition:** A decorator that accepts its own arguments needs **three levels of nesting**: the outer function takes the arguments and returns the actual decorator, which returns the wrapper.

**Explanation:** `@retry(times=3)` first **calls** `retry(times=3)` → returns `decorator`, which is then applied: `func = decorator(func)`.

```
retry(times)          ← level 1: receives decorator arguments
 └── decorator(func)  ← level 2: receives the function
      └── wrapper(*args, **kwargs)  ← level 3: runs on each call
```

```python
import functools

def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == times:
                        raise
                    print(f"Attempt {attempt} failed, retrying...")
        return wrapper
    return decorator

calls = {"n": 0}

@retry(times=3)
def call_api():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("network down")
    return "success"

print(call_api())
print(call_api.__name__)
```

**Output:**
```text
Attempt 1 failed, retrying...
Attempt 2 failed, retrying...
success
call_api
```

**🎤 Say this in the interview:**
> "A decorator with arguments needs three layers: the outer function takes the arguments and returns a decorator, the decorator takes the function, and the wrapper runs on each call. A typical example is `@retry(times=3)`. I still use `functools.wraps` on the wrapper. In production I'd also add exponential backoff and only retry transient errors."

**Key takeaway:** Arguments → one extra layer of nesting.

---

### 8.5 Context Managers and the `with` Statement

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Source: Q34)*

**Definition:** A **context manager** handles **setup and teardown** around a block of code. It implements `__enter__` (setup) and `__exit__` (cleanup). The `with` statement **guarantees cleanup runs**, even if an exception occurs.

**Explanation:**
- `__enter__`'s return value is bound by `as`.
- `__exit__(exc_type, exc_val, tb)` receives exception info; returning `True` **suppresses** the exception (use carefully).
- `@contextlib.contextmanager` turns a generator into a context manager: code before `yield` = setup, after = cleanup (put it in `finally`).
- Common examples: files, locks, DB sessions/transactions, timers, temporary settings.

```python
class DBConnection:                        # class-based
    def __enter__(self):
        print("Connecting...")
        return self
    def __exit__(self, exc_type, exc_val, tb):
        print(f"Closing connection (error: {exc_type.__name__ if exc_type else None})")
        return False                       # don't suppress exceptions

with DBConnection() as conn:
    print("Doing work")

try:
    with DBConnection():
        raise ValueError("query failed")
except ValueError:
    print("Exception still propagated")

from contextlib import contextmanager, suppress

@contextmanager                            # generator-based (simpler)
def db_conn():
    print("Connecting...")
    try:
        yield "conn-object"
    finally:
        print("Closing connection")

with db_conn() as c:
    print("Using", c)

with suppress(FileNotFoundError):          # ready-made context manager
    open("does-not-exist.txt")
print("continued safely")
```

**Output:**
```text
Connecting...
Doing work
Closing connection (error: None)
Connecting...
Closing connection (error: ValueError)
Exception still propagated
Connecting...
Using conn-object
Closing connection
continued safely
```

**🎤 Say this in the interview:**
> "A context manager wraps a block with setup and teardown via `__enter__` and `__exit__`, and the `with` statement guarantees the teardown runs even if an exception is raised — that's why we use `with open(...)`. For simple cases I write one with `@contextlib.contextmanager` and a `try/finally` around the `yield`; I use a class when I need more control, like deciding whether to suppress specific exceptions."

**Follow-ups:**
- **Q: Async version?** — `async with`, implemented with `__aenter__`/`__aexit__` or `@contextlib.asynccontextmanager` (e.g., DB sessions in FastAPI).

**Key takeaway:** `with` = guaranteed cleanup. `@contextmanager` + `try/finally` for quick ones.

---

## 9. Memory Management & Python Internals

### 9.1 How Python Manages Memory (Reference Counting + Garbage Collector)

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q9)*

**Definition:** CPython frees memory mainly through **reference counting**: each object counts how many references point to it, and it's freed immediately when the count reaches **0**. A **cyclic garbage collector** (`gc` module) periodically finds and frees **reference cycles** that reference counting alone can't handle.

**Explanation:**
1. `a = [1, 2, 3]` → refcount 1. `b = a` → 2. `del b` → 1. `del a` → 0 → freed.
2. **Cycle problem:** `n1.ref = n2; n2.ref = n1` → after `del n1, n2` both still have refcount 1, so they'd never be freed by refcounting alone.
3. The **generational GC** tracks container objects in generations (young objects are checked more often, since most objects die young) and breaks unreachable cycles.
4. Memory for small objects comes from CPython's own allocator (**pymalloc**) and may be reused rather than returned to the OS immediately.

```python
import sys
import gc

a = [1, 2, 3]
before = sys.getrefcount(a)        # includes the temporary reference from the call itself
b = a
print(sys.getrefcount(a) - before) # one more reference
del b
print(sys.getrefcount(a) - before) # back to where it was

class Node:
    def __init__(self):
        self.ref = None

n1, n2 = Node(), Node()
n1.ref, n2.ref = n2, n1            # reference cycle
del n1, n2                         # refcounts never reach 0 by themselves
print(gc.collect() >= 2)           # the cyclic GC finds and frees them
```

**Output:**
```text
1
0
True
```

> Absolute `getrefcount` values can differ between Python versions, so compare differences rather than memorising numbers.

**🎤 Say this in the interview:**
> "CPython mainly uses reference counting — every object tracks how many references point to it and is freed as soon as that hits zero. Reference counting can't handle cycles, so there's also a generational cyclic garbage collector in the `gc` module. To reduce memory per object I can use `__slots__`, and for large data I use generators instead of building big lists."

**Follow-ups:**
- **Q: Can Python have memory leaks?** — Yes: lingering references (global caches, unbounded `lru_cache`, listeners never removed), or cycles involving objects the GC can't collect. Tools: `tracemalloc`, `gc.get_objects()`, `objgraph`.
- **Q: What does `del` do?** — Deletes a **name** (decrements the refcount); it doesn't directly free the object.
- **Q: What is `weakref`?** — A reference that doesn't increase the refcount — useful for caches that shouldn't keep objects alive.

**Key takeaway:** Refcounting frees most objects instantly; the GC cleans up cycles.

---

### 9.2 How the Import System Works

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q10)*

**Definition:** On `import x`, Python first checks the **`sys.modules` cache**. If the module isn't there, it searches the directories in **`sys.path`**, **executes the module once**, stores it in `sys.modules`, and binds the name.

**Explanation:**
1. Check `sys.modules` → if found, reuse it (this is why module-level objects behave like singletons — see 7.1).
2. Otherwise search `sys.path` (script directory, `PYTHONPATH`, standard library, site-packages).
3. Execute the module's top-level code once and cache it.
4. **Circular imports**: `a` imports `b` while `b` imports `a` → one sees a **partially initialised** module → `ImportError`/`AttributeError`.

**Fixing circular imports:**
- ✅ Best: restructure — move shared code into a **third module**.
- Import inside the function that needs it (deferred import).
- `import module` instead of `from module import name`.
- For type hints only: `if TYPE_CHECKING:` imports.

```python
import sys
import json

print("json" in sys.modules)          # cached after first import
import json as again
print(again is json)                  # same module object — executed only once
print(isinstance(sys.path, list))     # the search path is a plain list
```

**Output:**
```text
True
True
True
```

Deferred import to break a cycle (snippet — `module_b` is a placeholder):

```python
def get_thing():
    from module_b import Thing    # imported when called, not at module load time
    return Thing()
```

**🎤 Say this in the interview:**
> "When importing, Python checks the `sys.modules` cache first; if it's not there, it searches `sys.path`, runs the module once and caches it. Circular imports happen when two modules import each other and one sees the other half-initialised. I treat them as a design smell and fix them by extracting the shared code into a third module; as a quick fix I can defer the import into a function."

**Key takeaway:** Import = check cache → search `sys.path` → execute once → cache.

---

## 10. Concurrency & Parallelism

### 10.1 The GIL (Global Interpreter Lock)

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Source: Q35)*

**Definition:** The **GIL** is a mutex in **CPython** that allows only **one thread to execute Python bytecode at a time**, even on multi-core CPUs.

**Explanation:**
- **Why it exists:** it protects CPython's reference counts and internal memory structures from race conditions and keeps single-threaded code fast and C extensions simple.
- **Effect on CPU-bound code:** threads **can't run Python code in parallel** → no speed-up (often slower).
- **Effect on I/O-bound code:** little impact — a thread **releases the GIL** while waiting on I/O (network, disk, `time.sleep`), so other threads run.
- **C extensions** like NumPy release the GIL during heavy computation.
- **Workarounds for CPU-bound work:** `multiprocessing` / `ProcessPoolExecutor` (each process has its own interpreter and GIL), or C extensions.
- **Recent change:** Python 3.13 added an **experimental free-threaded build** (no GIL, PEP 703). The standard CPython build still has the GIL.

```python
import threading
import time

def io_task():
    time.sleep(0.2)                  # I/O wait releases the GIL

start = time.perf_counter()
threads = [threading.Thread(target=io_task) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
elapsed = time.perf_counter() - start
print(elapsed < 0.5)                 # ~0.2s total, not 5 × 0.2s = 1.0s
```

**Output:**
```text
True
```

**🎤 Say this in the interview:**
> "The GIL is a lock in CPython that lets only one thread run Python bytecode at a time. It protects CPython's memory management. It barely affects I/O-bound work because threads release it while waiting, but it prevents CPU-bound threads from running in parallel. For CPU-heavy work I use multiprocessing, or libraries like NumPy that release the GIL in C code. Python 3.13 also has an experimental free-threaded build without the GIL."

**Follow-ups:**
- **Q: Does the GIL make my code thread-safe?** — No. It protects interpreter internals, not your logic. `counter += 1` is several bytecode steps and can still race — use `threading.Lock`.
- **Q: Do other Python implementations have a GIL?** — Jython and IronPython don't; PyPy does.

**Key takeaway:** GIL blocks CPU parallelism in threads, not I/O concurrency.

---

### 10.2 Threading vs Multiprocessing vs Asyncio

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Sources: Q36 + Q35 — merged)*

**Definition:**
- **Multithreading** — multiple threads in **one process**, sharing memory. Concurrent but not parallel for Python code (GIL).
- **Multiprocessing** — multiple **processes**, each with its own memory and GIL → **true parallelism**.
- **Asyncio** — **one thread**, one event loop, many coroutines that **cooperatively** yield at `await` points.

**Explanation:**

| | Threading | Multiprocessing | Asyncio |
|---|---|---|---|
| Best for | I/O-bound, moderate number of tasks; blocking libraries | **CPU-bound** work | **Many** concurrent I/O tasks (thousands of connections) |
| Parallel CPU execution | ❌ (GIL) | ✅ | ❌ |
| Memory | Shared (needs locks) | Separate (data copied via pickling/IPC) | Shared, single thread |
| Switching | Pre-emptive (OS decides) | OS processes | Cooperative (at `await`) |
| Overhead | Low–medium | High (process start-up, IPC) | Very low per task |
| Main risk | Race conditions, deadlocks | Pickling cost, memory use | One blocking call freezes everything |
| Stdlib API | `threading`, `ThreadPoolExecutor` | `multiprocessing`, `ProcessPoolExecutor` | `asyncio` |

**Decision rule:**
- CPU-bound → **multiprocessing**
- I/O-bound + many tasks + async libraries available → **asyncio**
- I/O-bound + few tasks, or blocking libraries (e.g., `requests`) → **threads**

#### Concurrency vs Parallelism

| Concurrency | Parallelism |
|---|---|
| Dealing with many tasks by **interleaving** them | Doing many tasks **at the same instant** on multiple cores |
| Threads (with GIL), asyncio | Multiprocessing |

```python
import asyncio
import time

async def fetch(url):
    await asyncio.sleep(0.2)            # non-blocking wait (simulated network call)
    return f"data from {url}"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(fetch("url1"), fetch("url2"), fetch("url3"))
    print(results)
    print(time.perf_counter() - start < 0.5)   # ~0.2s total, not 0.6s

asyncio.run(main())
```

**Output:**
```text
['data from url1', 'data from url2', 'data from url3']
True
```

**🎤 Say this in the interview:**
> "Threads share memory in one process and are good for I/O-bound work, but because of the GIL they don't speed up CPU-bound Python code. Multiprocessing uses separate processes with their own GIL, so it gives real parallelism for CPU-bound work, at the cost of more memory and inter-process communication. Asyncio runs many coroutines on a single thread and switches at `await` points, which is the most efficient option for thousands of concurrent network calls. My rule: CPU-bound → processes, lots of I/O → async, a few blocking I/O calls → threads."

**Follow-ups:**
- **Q: Why not always use multiprocessing?** — Process start-up cost, higher memory, and arguments/results must be pickled and copied.
- **Q: How do threads share data safely?** — `threading.Lock`, `queue.Queue` (thread-safe), or avoid shared state.

**Key takeaway:** CPU → processes. Many I/O → asyncio. Some blocking I/O → threads.

---

### 10.3 `concurrent.futures`: `ThreadPoolExecutor` and `ProcessPoolExecutor`

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q64)*

**Definition:** `concurrent.futures` is a high-level, unified API for running functions in a **pool** of threads (`ThreadPoolExecutor`, for I/O-bound work) or processes (`ProcessPoolExecutor`, for CPU-bound work — bypasses the GIL).

**Explanation:**
- `executor.map(fn, items)` → results **in input order**.
- `executor.submit(fn, arg)` → a `Future`; use `.result()` (blocks, re-raises errors) or `.exception()`.
- `as_completed(futures)` → yields futures **as they finish** (not in submission order).
- With processes, put the start code under `if __name__ == "__main__":` — required on Windows and macOS (which start processes with "spawn").

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def fetch(url):                       # pretend I/O-bound work
    time.sleep(0.1)
    return f"fetched {url}"

def crunch(n):                        # CPU-bound work
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    urls = ["/1", "/2", "/3"]
    with ThreadPoolExecutor(max_workers=10) as executor:
        print(list(executor.map(fetch, urls)))        # keeps input order

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(crunch, n) for n in (10, 100, 1000)]
        print([f.result() for f in futures])
```

**Output:**
```text
['fetched /1', 'fetched /2', 'fetched /3']
[285, 328350, 332833500]
```

**🎤 Say this in the interview:**
> "`concurrent.futures` gives one API for thread and process pools. I use `ThreadPoolExecutor` for I/O-bound tasks like HTTP calls and `ProcessPoolExecutor` for CPU-bound tasks because it sidesteps the GIL. `map` keeps input order; `submit` returns Futures, and `as_completed` lets me handle results as soon as each one finishes."

**Key takeaway:** Threads pool for I/O, process pool for CPU; `map` = ordered, `as_completed` = fastest-first.

---

### 10.4 `multiprocessing.Pool` vs `ProcessPoolExecutor`

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q94)*

**Definition:** Both run work in separate processes to bypass the GIL. `ProcessPoolExecutor` (`concurrent.futures`) is the newer, cleaner API based on `Future` objects. `multiprocessing.Pool` is older, with more fine-grained options (`imap`, `starmap`, `chunksize`, `maxtasksperchild`).

| | `ProcessPoolExecutor` | `multiprocessing.Pool` |
|---|---|---|
| API style | Futures (`submit`, `as_completed`) | `map`, `imap`, `imap_unordered`, `starmap`, `apply_async` |
| Same API as thread pool | ✅ (easy switch) | ❌ |
| `chunksize` batching | ✅ in `map` | ✅ |
| Recommended for new code | ✅ | When you need its extra controls |

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Pool

def cpu_task(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(cpu_task, n): n for n in range(5)}
        done = sorted(f.result() for f in as_completed(futures))  # finish order varies → sort
        print(done)

    with Pool(processes=4) as pool:
        # chunksize batches tasks → less inter-process overhead for many small tasks
        print(pool.map(cpu_task, range(5), chunksize=2))
```

**Output:**
```text
[0, 0, 1, 5, 14]
[0, 0, 1, 5, 14]
```

**🎤 Say this in the interview:**
> "Both use processes to get around the GIL. I default to `ProcessPoolExecutor` because it has the same Future-based API as the thread pool and `as_completed` for processing results as they finish. I'd use `multiprocessing.Pool` when I need its extras, like `imap_unordered` or `maxtasksperchild`. In both, `chunksize` reduces overhead for many small tasks."

**Key takeaway:** Default to `ProcessPoolExecutor`; `Pool` for advanced controls.

---

### 10.5 `async`/`await` and the Event Loop

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Source: Q37)*

**Definition:** `async def` defines a **coroutine**. `await` **pauses** the coroutine until the awaited operation finishes, handing control back to the **event loop**, which runs other ready coroutines in the meantime.

**Explanation (step by step):**
1. `asyncio.run(main())` creates an event loop and runs `main`.
2. When a coroutine hits `await` on I/O (e.g., a network call), it's suspended.
3. The loop runs other coroutines that are ready.
4. When the I/O completes, the suspended coroutine resumes.
5. Everything runs on **one thread** — no locks needed for most code, but **any blocking call stops everything** (see 10.6).

| Term | Meaning |
|---|---|
| Coroutine | Function defined with `async def`; calling it returns a coroutine object (doesn't run yet) |
| `await` | Suspend until the awaitable completes |
| Task | A coroutine scheduled on the loop (`asyncio.create_task`) — runs concurrently |
| `asyncio.gather` | Run several awaitables concurrently, collect results in order |
| Event loop | Scheduler that switches between coroutines at `await` points |

```python
import asyncio

async def worker(name, delay):
    print(f"{name} start")
    await asyncio.sleep(delay)          # yields control to the event loop
    print(f"{name} done")
    return name

async def main():
    coro = worker("X", 0)
    print(type(coro).__name__)          # nothing has run yet
    await coro
    results = await asyncio.gather(worker("A", 0.2), worker("B", 0.1))
    print(results)                      # gather keeps argument order

asyncio.run(main())
```

**Output:**
```text
coroutine
X start
X done
A start
B start
B done
A done
['A', 'B']
```

Real HTTP calls need an async client (snippet — requires `pip install aiohttp`):

```python
import asyncio
import aiohttp

async def fetch_user(session, user_id):
    async with session.get(f"/users/{user_id}") as r:
        return await r.json()

async def main():
    async with aiohttp.ClientSession(base_url="https://api.example.com") as session:
        return await asyncio.gather(*(fetch_user(session, i) for i in (1, 2, 3)))

users = asyncio.run(main())
```

**🎤 Say this in the interview:**
> "`async def` defines a coroutine and `await` suspends it while waiting, giving control back to the event loop, which runs other coroutines in the meantime. It's single-threaded cooperative multitasking, which is very efficient for many concurrent network calls. The common mistake is calling blocking code like `time.sleep` or `requests.get` inside a coroutine — that blocks the whole loop — so I use async libraries like `aiohttp`/`httpx` and `asyncio.sleep`."

**Key takeaway:** `await` = pause and let others run. Single thread, so never block.

---

### 10.6 Blocking the Event Loop (and How to Avoid It)

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q38)*

**Definition:** **Blocking the event loop** means running synchronous, long-running code inside a coroutine — the code never `await`s, so **no other coroutine can run** until it finishes.

**Explanation — fixes:**
1. Use async-native libraries (`asyncio.sleep`, `aiohttp`/`httpx`, `asyncpg`).
2. Offload blocking calls to a thread: `await asyncio.to_thread(func, *args)` (Python 3.9+). The older equivalent is `loop.run_in_executor(None, func, *args)`.
3. CPU-heavy work → a process pool via `run_in_executor(ProcessPoolExecutor(), ...)`.

```python
import asyncio
import time

async def ticker():
    for _ in range(3):
        print("tick")
        await asyncio.sleep(0.1)

async def bad():
    time.sleep(0.35)                         # blocks — ticker can't run
    print("bad done")

async def good():
    await asyncio.to_thread(time.sleep, 0.35)  # runs in a thread — loop stays free
    print("good done")

async def main():
    print("--- blocking")
    await asyncio.gather(bad(), ticker())
    print("--- non-blocking")
    await asyncio.gather(good(), ticker())

asyncio.run(main())
```

**Output:**
```text
--- blocking
bad done
tick
tick
tick
--- non-blocking
tick
tick
tick
good done
```

**🎤 Say this in the interview:**
> "Since asyncio runs on one thread, a synchronous call like `time.sleep` or `requests.get` inside a coroutine freezes every other task. I avoid it by using async libraries, and when I must call blocking code I wrap it in `asyncio.to_thread` — or `run_in_executor`, the older equivalent — so it runs in a thread pool while the loop keeps serving other tasks."

**Key takeaway:** Inside `async def`: no blocking calls. Use `asyncio.to_thread` for unavoidable ones.

---

### 10.7 `asyncio.Queue` and the Producer–Consumer Pattern

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q95)*

**Definition:** `asyncio.Queue` passes items between **coroutines** in the same event loop. The **producer–consumer** pattern separates generating work (producer) from processing it (one or more consumers/workers).

**Explanation:**
- ⚠️ **Correction to the original notes:** `asyncio.Queue` is **not thread-safe** — it is designed for coroutines within **one** event loop. For threads use `queue.Queue`; for processes `multiprocessing.Queue`.
- `maxsize` creates **backpressure**: `await queue.put()` waits when the queue is full, so a fast producer can't exhaust memory.
- `queue.task_done()` + `await queue.join()` lets you wait until every item is processed.

```python
import asyncio

async def producer(queue, items):
    for item in items:
        await queue.put(item)          # waits if the queue is full (backpressure)

async def consumer(queue, worker_id, results):
    while True:
        item = await queue.get()
        await asyncio.sleep(0.01)      # simulate work
        results.append((worker_id, item))
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=5)   # bounded queue
    results = []
    workers = [asyncio.create_task(consumer(queue, i, results)) for i in range(3)]

    await producer(queue, [f"task_{i}" for i in range(10)])
    await queue.join()                 # wait until every item is processed
    for w in workers:
        w.cancel()                     # stop the idle workers

    print(len(results))
    print(sorted(item for _, item in results)[:3])
    print(len({wid for wid, _ in results}) > 1)   # work was shared by workers

asyncio.run(main())
```

**Output:**
```text
10
['task_0', 'task_1', 'task_2']
True
```

**🎤 Say this in the interview:**
> "`asyncio.Queue` lets coroutines hand work to each other. A producer puts items in and several consumer tasks take them out, which separates generating work from processing it. A bounded queue gives backpressure — the producer waits when it's full, so memory stays under control. It's not thread-safe; for threads I'd use `queue.Queue`."

**Key takeaway:** `asyncio.Queue` (coroutines) ≠ `queue.Queue` (threads). `maxsize` = backpressure.

---

## 11. Performance & Optimization

### 11.1 Profiling Python Code

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q91)*

**Definition:** **Profiling** measures where a program spends time or memory, so you optimize the real bottleneck instead of guessing.

**Explanation:**

| Tool | Measures | Notes |
|---|---|---|
| `cProfile` + `pstats` | Time per function | Built-in. `python -m cProfile -s cumulative script.py` |
| `timeit` | Micro-benchmarks of small snippets | Built-in |
| `line_profiler` | Time per line | `pip install line-profiler`; mark functions with `@profile`, run with `kernprof -l -v script.py` |
| `memory_profiler` / `tracemalloc` | Memory usage | `tracemalloc` is built-in |
| `py-spy` | Sampling profiler for running processes | No code changes; safe for production: `py-spy top --pid <pid>` |

```python
import cProfile
import io
import pstats

def slow_function():
    return sum(i * i for i in range(200_000))

profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
stats.print_stats(5)                         # top 5 functions
print("slow_function" in stream.getvalue())

import timeit
t_join = timeit.timeit('"".join(str(i) for i in range(100))', number=1000)
print(t_join > 0)
```

**Output:**
```text
True
True
```

**🎤 Say this in the interview:**
> "Measure first, optimize second. I start with `cProfile` to find which functions take the most cumulative time, then use `line_profiler` to find the exact slow lines, and `tracemalloc` or `memory_profiler` for memory. For a live production process I use `py-spy`, which needs no code changes."

**Key takeaway:** Never guess — profile (`cProfile` → `line_profiler` → fix → re-measure).

---

### 11.2 Common Performance Anti-Patterns

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q93)*

**Definition:** Coding habits that make Python code needlessly slow or memory-hungry.

**Explanation:**

| Anti-pattern | Better | Why |
|---|---|---|
| `s += word` in a loop | `" ".join(words)` | Strings are immutable; repeated `+=` can copy the string each time (O(n²)); `join` is O(n) |
| `for i in range(len(items)): items[i]` | `for item in items` / `enumerate` | Cleaner, avoids indexing |
| `if x in big_list` repeatedly | Convert to a `set` once | O(n) → O(1) per lookup |
| `list(range(10**6))` just to loop | Iterate `range` / a generator directly | No need to build the list |
| Repeated `module.func` lookups in very hot loops | Bind to a local name: `sqrt = math.sqrt` | Small win; only after profiling |
| Manual loops for sums/max | Built-ins: `sum`, `max`, `any`, `sorted` | Implemented in C |
| Recomputing pure results | `@lru_cache` (2.3) | Memoization |
| Many DB calls in a loop | Batch / eager loading (13.3) | Network round-trips dominate |

```python
words = ["python", "is", "fast", "enough"]

result = ""
for word in words:              # anti-pattern
    result += word + " "
print(repr(result.strip()))

print(repr(" ".join(words)))    # idiomatic O(n)

items = list(range(10_000))
lookup = set(items)             # build once
print(9_999 in lookup)          # O(1) average

import math
data = [1, 4, 9]
sqrt = math.sqrt                # cache the attribute lookup (micro-optimization)
print([sqrt(x) for x in data])
```

**Output:**
```text
'python is fast enough'
'python is fast enough'
True
[1.0, 2.0, 3.0]
```

**🎤 Say this in the interview:**
> "The classic one is building strings with `+=` in a loop — strings are immutable, so it can copy the string every time; `''.join()` is linear. Others are membership tests on lists instead of sets, building lists you only iterate once instead of using generators, not using built-ins, and making database calls inside loops. But I always profile first before micro-optimizing."

**Key takeaway:** `join` for strings, `set` for lookups, generators for one-pass data, profile first.

---
## 12. FastAPI & Web Backend

> The code in Sections 12–15 needs third-party packages (`fastapi`, `pydantic`, `sqlalchemy`, `redis`, `pytest`, …) and often a running database. These examples are **snippets** that show the pattern. Names like `db`, `User`, `UserCreate`, `get_db` refer to objects defined in the earlier examples of the same section.

### 12.1 What is FastAPI and How Does It Compare to Flask?

🔴 **P1** · Level: Easy · Frequency: Very frequent · *(Source: Q39)*

**Definition:** **FastAPI** is a modern Python web framework built on **Starlette** (ASGI) and **Pydantic**. It uses **type hints** to validate requests, serialize responses, and generate **OpenAPI docs** automatically (`/docs`, `/redoc`). **Flask** is a simpler, older micro-framework that is **synchronous (WSGI) by default**.

**Explanation:**

| | FastAPI | Flask |
|---|---|---|
| Server interface | ASGI (async-first) | WSGI (sync; async views added in 2.0, but still a WSGI app) |
| Validation | Built-in via Pydantic + type hints | Manual or extensions (Marshmallow, etc.) |
| API docs | Automatic OpenAPI/Swagger | Extensions needed |
| Dependency injection | Built-in `Depends()` | None built-in |
| Performance | High for I/O-bound async workloads | Good; usually lower throughput under heavy concurrent I/O |
| Best for | APIs, microservices, ML model serving | Simple apps, server-rendered sites, large plugin ecosystem |

> The original notes said "FastAPI is 2–3× faster than Flask". Benchmarks vary a lot with workload and setup, so in an interview say "higher throughput for async I/O-bound workloads" rather than quoting a fixed number.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users", status_code=201)
async def create_user(user: User):          # body is validated automatically
    return {"message": f"Created {user.name}"}

# Run: uvicorn main:app --reload   → interactive docs at /docs and /redoc
```

**🎤 Say this in the interview:**
> "FastAPI is an async-first framework built on Starlette and Pydantic. The big difference from Flask is that type hints drive everything: request validation, serialization and automatic OpenAPI docs. It also has dependency injection built in. Flask is simpler and synchronous by default, with a huge ecosystem. For new JSON APIs, especially I/O-heavy ones, I'd choose FastAPI."

**Key takeaway:** FastAPI = ASGI + Pydantic + type hints → validation and docs for free.

---

### 12.2 Pydantic Validation in FastAPI

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q40)*

**Definition:** **Pydantic** models define the shape and types of data. FastAPI uses them to **validate incoming JSON** (returning a **422** error if it's invalid), **serialize responses**, and build the **OpenAPI schema**.

**Explanation:**
- Pydantic **v2** API: `@field_validator` (replaces v1 `@validator`), `model_dump()` (replaces `.dict()`), `model_config = {...}` (replaces `class Config`).
- Use **separate schemas** for input and output (`UserCreate` with a password vs `UserOut` without) — never leak internal fields.
- `Field(...)` adds constraints: `Field(gt=0, le=150)`, `min_length`, `pattern`.

```python
from pydantic import BaseModel, EmailStr, Field, field_validator   # EmailStr needs: pip install "pydantic[email]"

class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(gt=0, lt=150)
    password: str
    role: str | None = "user"

    @field_validator("name")
    @classmethod
    def name_not_admin(cls, v):
        if v.lower() == "admin":
            raise ValueError("reserved name")
        return v

    model_config = {"str_strip_whitespace": True}

class UserOut(BaseModel):                  # response schema — no password
    id: int
    name: str
    email: EmailStr

@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate):
    data = user.model_dump(exclude={"password"})      # v2: model_dump(), not .dict()
    return {"id": 1, **data}                          # extra fields are filtered out by UserOut
```

**🎤 Say this in the interview:**
> "I define request and response shapes as Pydantic models. FastAPI validates the incoming JSON against them and returns a 422 with details if it's invalid, then uses the response model to serialize the output and filter out fields like passwords. In Pydantic v2 I use `field_validator` for custom rules and `model_dump` instead of `.dict()`. I always keep separate create and output schemas."

**Key takeaway:** Pydantic = runtime validation from type hints; separate in/out schemas.

---

### 12.3 Dependency Injection with `Depends()`

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Source: Q46)*

**Definition:** FastAPI's **dependency injection** system resolves function parameters declared with `Depends(fn)` by calling `fn` automatically for each request (and caching the result within that request). It's used for DB sessions, authentication, configuration and shared logic.

**Explanation:**
- Dependencies can depend on other dependencies (a tree).
- A dependency that **`yield`s** gets cleanup after the response (perfect for DB sessions).
- **Testing:** swap any dependency with `app.dependency_overrides[real] = fake`.

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with AsyncSessionLocal() as session:   # defined in 12.6
        yield session                            # cleanup runs after the response

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    user = await get_user_by_token(db, token)    # your lookup function
    if not user:
        raise HTTPException(401, "Invalid token")
    return user

@app.get("/me")
async def get_me(user=Depends(get_current_user)):
    return user

# In tests:
# app.dependency_overrides[get_db] = lambda: fake_db
```

**🎤 Say this in the interview:**
> "With `Depends`, FastAPI calls the dependency for me on each request and injects the result — I use it for DB sessions, the current user, and settings. Dependencies can chain, and a `yield` dependency gives me cleanup after the response. The big win is testing: I can replace any dependency with `app.dependency_overrides`."

**Key takeaway:** `Depends` = per-request injection + easy test overrides.

---

### 12.4 Exception Handling in FastAPI

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q41)*

**Definition:** Raise `HTTPException` for expected errors (404, 401…). Register **custom exception handlers** with `@app.exception_handler(ExcType)` to turn domain exceptions into consistent JSON error responses across the app.

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404,
                        content={"error": "user_not_found", "user_id": exc.user_id})

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = fake_db.get(user_id)            # placeholder data store
    if not user:
        raise UserNotFoundError(user_id)   # domain error, mapped to a 404 by the handler
    return user

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": 1}
```

**🎤 Say this in the interview:**
> "For simple cases I raise `HTTPException` with a status code. For domain errors I define custom exceptions and register handlers with `@app.exception_handler`, so the business code stays HTTP-agnostic and every error has the same JSON shape. I never expose raw exception messages or stack traces to clients — I log them and return a clean error."

**Key takeaway:** `HTTPException` for simple cases; custom exception + handler for consistent error schemas.

---

### 12.5 Middleware and CORS

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Sources: Q42 + Q79 — merged)*

**Definition:** **Middleware** is code that runs on **every request and response** — used for logging, timing, auth, CORS, compression, rate limiting. **CORS** (Cross-Origin Resource Sharing) is a browser security mechanism; the server sends headers that tell the browser which **other origins** may call the API.

**Explanation:**
- Middleware order: the middleware added **last** is the **outermost**, so it runs **first** on the request (and last on the response).
- CORS is enforced **by browsers** only — it doesn't protect against curl/server-to-server calls.
- `allow_origins=["*"]` together with `allow_credentials=True` is not allowed by the CORS spec — browsers reject a wildcard origin on credentialed requests. List exact origins in production.

```python
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)          # pass to the next layer / route
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "https://staging.myapp.com"],   # explicit, never "*" with credentials
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**🎤 Say this in the interview:**
> "Middleware wraps every request and response, so it's where I put cross-cutting concerns like request timing, logging, CORS and rate limiting. The last middleware added is the outermost and runs first. CORS tells browsers which origins may call my API; in production I list exact origins, because a wildcard combined with credentials is rejected by browsers and is a security risk."

**Key takeaway:** Middleware = per-request cross-cutting logic. CORS = explicit origins in prod.

---

### 12.6 Building a CRUD API with a Database

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Source: Q43)*

**Definition:** A CRUD (Create, Read, Update, Delete) API in FastAPI typically uses **SQLAlchemy** (ORM), an **async engine**, and a **DB session injected via `Depends`**, with models, schemas and data-access code kept in separate modules.

**Explanation — typical project layout:**

```
app/
├── main.py          # FastAPI app, include routers
├── database.py      # engine, session factory, get_db
├── models/          # SQLAlchemy ORM models (DB tables)
├── schemas/         # Pydantic models (API input/output)
├── crud/            # DB access functions
└── routers/         # endpoints grouped by resource
```

```python
# database.py  (SQLAlchemy 2.0 style)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# routers/users.py
from fastapi import Depends, HTTPException

@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.model_dump(exclude={"password"}),
                   hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)              # load DB-generated fields such as id
    return db_user

@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    return user
```

> Updates from the original notes: SQLAlchemy 2.0 uses `async_sessionmaker`, and Pydantic v2 uses `model_dump()` instead of `.dict()`.

**🎤 Say this in the interview:**
> "I use SQLAlchemy with an async engine and inject an `AsyncSession` per request through `Depends(get_db)`. I keep ORM models, Pydantic schemas, CRUD functions and routers in separate modules. Endpoints validate input with a create schema, write through the session, commit, and return through a response model so internal fields like hashed passwords never leak."

**Key takeaway:** routers / models / schemas / crud + session per request via `Depends`.

---

### 12.7 JWT Authentication

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Source: Q75)*

**Definition:** A **JWT** (JSON Web Token) is a signed token (`header.payload.signature`) the server issues after login. The client sends it in `Authorization: Bearer <token>`, and the server **verifies the signature and expiry** without a session lookup (stateless auth).

**Explanation (flow):**
1. User logs in with username and password → server verifies them → issues an **access token** (short-lived, e.g., 15 min) and usually a **refresh token**.
2. Client sends the access token with every request.
3. A dependency decodes and verifies it; if it's invalid or expired → **401**.
4. The payload is only **base64-encoded, not encrypted** → never put secrets in it (store `sub`/user id and roles only).

```python
from datetime import datetime, timedelta, timezone
import jwt                                    # PyJWT: pip install pyjwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "load-me-from-env"               # never hardcode in real code (see 12.13)
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta   # utcnow() is deprecated
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:             # also covers expired tokens
        raise credentials_exception
    username = payload.get("sub")
    if username is None:
        raise credentials_exception
    return username

@app.get("/protected")
async def protected_route(user: str = Depends(get_current_user)):
    return {"user": user}
```

> The original notes used `python-jose` (`from jose import jwt, JWTError`). That works the same way; current FastAPI docs use **PyJWT**, shown above.

**🎤 Say this in the interview:**
> "On login I verify the password hash and issue a signed JWT with the user id in `sub` and a short expiry. Protected routes use a dependency that decodes the token, checks the signature and expiry, and raises 401 if anything is wrong. JWT payloads are only encoded, not encrypted, so I store just the user id and roles. In production I use short-lived access tokens plus refresh tokens, and keep the secret in environment config."

**Follow-ups:**
- **Q: How do you log out / revoke a JWT?** — JWTs are stateless, so use short expiry plus a server-side denylist (e.g., in Redis) or rotate refresh tokens.
- **Q: How are passwords stored?** — Hashed with bcrypt/argon2 (e.g., `passlib`/`pwdlib`), never stored as plain text or encrypted.

**Key takeaway:** Signed, short-lived, no secrets in the payload, verified in a dependency.

---

### 12.8 Rate Limiting

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q76)*

**Definition:** **Rate limiting** caps how many requests a client (IP, user, API key) can make in a time window, returning **429 Too Many Requests** when exceeded. Implement it as middleware or a dependency, usually backed by **Redis** so the limit is shared across all server instances.

**Explanation:**

| Algorithm | Idea | Trade-off |
|---|---|---|
| Fixed window | Count per minute bucket | Simple; allows bursts at window boundaries |
| **Sliding window** (log / counter) | Count requests in the last N seconds | More accurate; a little more storage |
| Token bucket | Tokens refill at a rate; each request uses one | Allows controlled bursts |

```python
import time
import redis.asyncio as redis                   # async client — doesn't block the event loop
from fastapi import Depends, HTTPException, Request

r = redis.Redis(host="localhost", port=6379)

def rate_limit(max_requests: int = 10, window: int = 60):
    async def check(request: Request):
        key = f"rate:{request.client.host}"
        now = time.time()
        pipe = r.pipeline()
        pipe.zremrangebyscore(key, 0, now - window)   # drop entries outside the window
        pipe.zadd(key, {str(now): now})               # record this request
        pipe.zcard(key)                               # count requests in the window
        pipe.expire(key, window)
        _, _, count, _ = await pipe.execute()
        if count > max_requests:
            raise HTTPException(429, "Too many requests")
    return check

@app.get("/api/data", dependencies=[Depends(rate_limit(10, 60))])
async def get_data():
    return {"data": "..."}
```

> The original example used the synchronous `redis.Redis` client inside an async dependency, which blocks the event loop (see 10.6). Use `redis.asyncio`. Libraries like **`slowapi`** provide ready-made limits.

**🎤 Say this in the interview:**
> "I implement rate limiting as a dependency or middleware backed by Redis, so the limit holds across all instances. A sliding window using a sorted set — remove old timestamps, add the current one, count — is more accurate than a fixed window, which allows bursts at the boundary. When the limit is exceeded I return 429. For a quick solution there's `slowapi`."

**Key takeaway:** Redis + sliding window + 429.

---

### 12.9 Background Tasks

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q77)*

**Definition:** FastAPI's `BackgroundTasks` runs a function **after the response is sent**, in the same process — good for light work like sending a welcome email. Heavy or critical jobs belong in a **task queue** like Celery (see 15.3).

| | `BackgroundTasks` | Celery / RQ / Arq + broker |
|---|---|---|
| Runs in | Same web process | Separate worker processes |
| Survives a server restart | ❌ Task lost | ✅ Persisted in the broker |
| Retries, scheduling, monitoring | ❌ | ✅ |
| Use for | Light, non-critical work | Heavy, critical or long-running jobs |

```python
from fastapi import BackgroundTasks

async def send_welcome_email(email: str):
    ...                                        # call email provider

def update_analytics(user_id: int):            # sync functions run in a threadpool
    ...

@app.post("/register")
async def register(user: UserCreate, background_tasks: BackgroundTasks):
    new_user = await create_user_in_db(user)
    background_tasks.add_task(send_welcome_email, user.email)   # runs after the response
    background_tasks.add_task(update_analytics, new_user.id)
    return {"id": new_user.id, "status": "registered"}
```

**🎤 Say this in the interview:**
> "`BackgroundTasks` lets me run work after the response is returned, like sending a confirmation email, so the user doesn't wait. It runs in the same process, so if the server restarts the task is lost and there are no retries. For heavy or must-not-lose jobs I use Celery with Redis or RabbitMQ."

**Key takeaway:** Light → `BackgroundTasks`; reliable/heavy → Celery.

---

### 12.10 File Uploads

🟢 **P3** · Level: Medium · Frequency: Frequent · *(Source: Q78)*

**Definition:** Use `UploadFile` (with `File(...)`) to receive files as multipart form data. `UploadFile` is backed by a spooled temporary file, so large uploads don't have to sit fully in memory.

**Explanation — best practices:**
- Validate **content type** and **size**. Read in chunks rather than calling `await file.read()` on huge files.
- Never trust `file.filename` for paths (path traversal) — generate your own name.
- In production, stream to object storage (S3/GCS) instead of the local disk.

```python
import uuid
import aiofiles                                  # pip install aiofiles
from fastapi import File, HTTPException, UploadFile

MAX_SIZE = 5 * 1024 * 1024                        # 5 MB
ALLOWED = {"image/jpeg", "image/png", "application/pdf"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED:
        raise HTTPException(400, f"File type not allowed: {file.content_type}")

    save_path = f"uploads/{uuid.uuid4().hex}"     # don't trust the client's filename
    size = 0
    async with aiofiles.open(save_path, "wb") as out:
        while chunk := await file.read(1024 * 1024):   # 1 MB chunks
            size += len(chunk)
            if size > MAX_SIZE:
                raise HTTPException(400, "File too large (max 5MB)")
            await out.write(chunk)
    return {"filename": file.filename, "size": size}

@app.post("/upload-many")
async def upload_many(files: list[UploadFile] = File(...)):
    return [{"name": f.filename} for f in files]
```

**🎤 Say this in the interview:**
> "I accept files with `UploadFile`, validate the content type and size, read in chunks so large files don't blow up memory, and generate my own filename to avoid path traversal. In production I stream directly to S3 or GCS rather than saving to local disk."

**Key takeaway:** Validate type + size, stream in chunks, store in object storage.

---

### 12.11 API Versioning

🟢 **P3** · Level: Medium · Frequency: Frequent · *(Source: Q80)*

**Definition:** **API versioning** lets you change an API without breaking existing clients. The common approaches are **URL path** (`/v1/users`), **header** (`Accept: application/vnd.api+json;version=2`) and **query parameter**.

| Approach | Pros | Cons |
|---|---|---|
| URL path `/v1/` | Explicit, easy to test, cache-friendly | URLs change |
| Header | Clean URLs | Harder to debug and test from a browser |

```python
from fastapi import APIRouter, FastAPI

app = FastAPI()
v1 = APIRouter(prefix="/v1")
v2 = APIRouter(prefix="/v2")

@v1.get("/users")
async def get_users_v1():
    return [{"id": 1, "name": "Raj"}]

@v2.get("/users")
async def get_users_v2():                      # extended response
    return [{"id": 1, "name": "Raj", "role": "admin", "created_at": "2024-01-01"}]

app.include_router(v1)
app.include_router(v2)                         # /v1/users and /v2/users both work
```

**🎤 Say this in the interview:**
> "I usually version through the URL path with a separate `APIRouter` per version, because it's explicit and easy to test. I keep old versions running until clients migrate, and only make breaking changes in a new version. Header versioning gives cleaner URLs but is harder to debug."

**Key takeaway:** `/v1`, `/v2` routers; never break existing clients.

---

### 12.12 Pagination (Offset vs Cursor)

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q98)*

**Definition:** **Pagination** returns large result sets in pages. **Offset/limit** pagination skips N rows; **cursor (keyset)** pagination continues from the last seen key (`WHERE id < last_id`).

| | Offset/limit | Cursor (keyset) |
|---|---|---|
| Jump to page N | ✅ | ❌ (next/previous only) |
| Speed on deep pages | Slows down — DB still scans the skipped rows | Fast — uses the index |
| Data changing between requests | Duplicates or skipped items | Stable |
| Best for | Admin tables, small datasets | Feeds, infinite scroll, large tables |

```python
import math
from typing import Generic, TypeVar
from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

@app.get("/users", response_model=Page[UserOut])           # offset pagination
async def list_users(page: int = Query(1, ge=1),
                     size: int = Query(20, ge=1, le=100),
                     db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(User.id)))
    users = (await db.execute(
        select(User).order_by(User.id).offset((page - 1) * size).limit(size)
    )).scalars().all()
    return Page(items=users, total=total, page=page, size=size,
                pages=math.ceil(total / size))

@app.get("/feed")                                          # cursor pagination
async def get_feed(cursor: int | None = Query(None),       # last seen id
                   limit: int = Query(20, le=100),
                   db: AsyncSession = Depends(get_db)):
    query = select(Post).order_by(Post.id.desc()).limit(limit)
    if cursor is not None:
        query = query.where(Post.id < cursor)
    posts = (await db.execute(query)).scalars().all()
    return {"items": posts, "next_cursor": posts[-1].id if posts else None}
```

**🎤 Say this in the interview:**
> "Offset pagination is simple and supports jumping to page N, but it slows down on deep pages because the database still scans the skipped rows, and items can be duplicated or skipped if data changes between requests. Cursor pagination continues from the last seen id using the index, so it's fast and stable — I use it for feeds and large tables. I always cap the page size."

**Key takeaway:** Small/admin → offset. Large/real-time → cursor. Always use a stable `ORDER BY` and a max page size.

---

### 12.13 Configuration and Environment Variables

🔴 **P1** · Level: Medium · Frequency: Frequent · *(Sources: Q47 + Q99 factor 3 — merged)*

**Definition:** Store configuration — especially **secrets** — in **environment variables**, not in code. `pydantic-settings` (`BaseSettings`) reads env vars or a `.env` file into a typed, validated settings object.

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict   # pip install pydantic-settings

class Settings(BaseSettings):
    database_url: str                 # required — startup fails if missing
    secret_key: str
    redis_url: str = "redis://localhost:6379/0"
    debug: bool = False               # "true"/"1" from env → True
    max_connections: int = 10

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache                            # load once, reuse everywhere
def get_settings() -> Settings:
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {"debug": settings.debug}
```

**🎤 Say this in the interview:**
> "I never hardcode config or secrets. I use `pydantic-settings`, which reads environment variables or a `.env` file into a typed Settings class, so a missing or invalid value fails at startup instead of at runtime. I wrap it in an `lru_cache` factory so it's loaded once, and inject it with `Depends` so tests can override it. `.env` stays out of git."

**Key takeaway:** Env vars + typed `BaseSettings` + `@lru_cache` factory.

---

## 13. Databases, SQL & Redis

### 13.1 SQL JOINs (INNER, LEFT, FULL OUTER, CROSS)

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Sources: Q48 + Q83 — merged)*

**Definition:** A **JOIN** combines rows from two tables based on a related column.

**Explanation:** Sample data — `users`: (1, Raj), (2, Priya), (3, Anita) · `orders`: (101, user_id=1), (102, user_id=1), (103, user_id=2)

| JOIN | Returns | Result for the sample |
|---|---|---|
| `INNER JOIN` | Only rows with a match in **both** tables | Raj, Raj, Priya |
| `LEFT JOIN` | **All** left rows + matches (NULL if none) | Raj, Raj, Priya, Anita (NULL order) |
| `RIGHT JOIN` | All right rows + matches | Mirror image of LEFT |
| `FULL OUTER JOIN` | All rows from both sides | Everything, NULLs where unmatched |
| `CROSS JOIN` | Every combination (Cartesian product) | 3 users × N products = 3N rows |

```sql
-- INNER JOIN: only users who have orders
SELECT u.name, o.id
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: all users, even without orders
SELECT u.name, o.id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Classic question: find users with NO orders
SELECT u.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;                       -- returns Anita

-- CROSS JOIN: every combination (dangerous on big tables)
SELECT u.name, p.name
FROM users u
CROSS JOIN products p;
```

**🎤 Say this in the interview:**
> "INNER JOIN returns only matching rows; LEFT JOIN returns every row from the left table with NULLs where there's no match; FULL OUTER returns everything from both; CROSS JOIN is the Cartesian product. A common question is finding users with no orders — that's a LEFT JOIN with `WHERE orders.id IS NULL`. An accidental cross join from a missing ON condition can generate millions of rows."

**Key takeaway:** "Rows without a match" → `LEFT JOIN ... WHERE right.id IS NULL`.

---

### 13.2 Database Indexing

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q49)*

**Definition:** An **index** is a separate data structure — usually a **B-tree** — that lets the database find rows without scanning the whole table. It **speeds up reads** at the cost of **slower writes** and extra storage.

**Explanation:**
- Index columns used in `WHERE`, `JOIN ... ON`, and `ORDER BY`.
- **Composite index** `(user_id, created_at)` follows the **leftmost-prefix rule**: it helps queries filtering on `user_id`, or `user_id` + `created_at`, but **not** `created_at` alone.
- Avoid indexing **low-cardinality** columns (e.g., booleans) and over-indexing write-heavy tables.
- Verify with `EXPLAIN ANALYZE` (Index Scan vs Seq Scan).
- Other types (PostgreSQL): Hash, **GIN** (full-text/JSONB — see 13.8), GiST, partial, and unique indexes.

```sql
CREATE INDEX idx_users_email ON users(email);

-- Composite index: column order matters (leftmost prefix)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Check whether the index is used
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'raj@x.com';

-- PostgreSQL: build without locking writes in production
CREATE INDEX CONCURRENTLY idx_orders_created ON orders(created_at);
```

**🎤 Say this in the interview:**
> "An index, usually a B-tree, lets the database find rows without a full table scan, so reads get much faster, but every insert and update must also maintain the index. I index columns used in WHERE, JOIN and ORDER BY, remember that composite indexes follow the leftmost-prefix rule, avoid low-cardinality columns, and confirm with EXPLAIN ANALYZE."

**Key takeaway:** Index = faster reads, slower writes. Check with `EXPLAIN ANALYZE`.

---

### 13.3 The N+1 Query Problem

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Source: Q50)*

**Definition:** The **N+1 problem** happens when you run **1 query** to fetch N records, then **1 extra query per record** (usually through ORM lazy loading) — N+1 round trips instead of 1 or 2.

**Explanation:** 100 users → 1 query for users + 100 queries for their orders = 101 queries. Each round trip adds latency.

| Fix | Queries | When |
|---|---|---|
| `selectinload` | 2 (`... WHERE user_id IN (...)`) | One-to-many collections (usually the best default) |
| `joinedload` | 1 (JOIN) | Many-to-one / small related sets; duplicates parent rows for collections |
| Hand-written JOIN / aggregate | 1 | Reports, counts |

```python
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload, selectinload

# BAD: lazy loading fires one SELECT per user
# (with AsyncSession, lazy loading actually raises an error, which helps catch this)
users = (await db.execute(select(User))).scalars().all()
for user in users:
    print(user.orders)

# FIX 1: selectinload → 2 queries in total
users = (await db.execute(
    select(User).options(selectinload(User.orders))
)).scalars().all()

# FIX 2: joinedload → 1 query with a JOIN (.unique() removes duplicated parents)
users = (await db.execute(
    select(User).options(joinedload(User.orders))
)).unique().scalars().all()

# FIX 3: a single SQL aggregate for reports
result = await db.execute(text("""
    SELECT u.id, u.name, COUNT(o.id) AS order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.name
"""))
```

**Detecting it:** turn on SQL logging in development — `create_engine(..., echo=True)` or `logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)` — and look for repeated identical queries.

**🎤 Say this in the interview:**
> "N+1 is when I load N parent rows and the ORM then lazily fires one query per row for the related data — 101 round trips instead of 2. I detect it with SQL logging in development and fix it with eager loading: `selectinload` for collections, which gives two queries, or `joinedload` for a single JOIN. In one case fixing an N+1 cut about 99 round trips." *(Only quote numbers from your own experience — the original notes suggest quantifying impact, e.g., "800 ms → 45 ms".)*

**Key takeaway:** Loop + lazy relationship = N+1 → `selectinload`/`joinedload`.

---

### 13.4 Connection Pooling

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Source: Q81)*

**Definition:** **Connection pooling** keeps a set of open database connections and **reuses** them across requests, avoiding the cost of opening a new connection (TCP + auth + TLS) for every request. SQLAlchemy engines pool automatically.

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=10,        # connections kept open
    max_overflow=20,     # extra connections allowed under load (closed afterwards)
    pool_timeout=30,     # seconds to wait for a free connection before erroring
    pool_recycle=1800,   # replace connections older than 30 min
    pool_pre_ping=True,  # check a connection is alive before using it
)
# A session borrows a connection and returns it to the pool when it closes.
```

**Explanation — sizing:** total connections ≈ `(pool_size + max_overflow) × number of app processes/pods`. That must stay below the database's `max_connections`. At scale, add an external pooler like **PgBouncer**.

**🎤 Say this in the interview:**
> "Opening a database connection is expensive, so a pool keeps connections open and lends them to requests. SQLAlchemy does this automatically; I tune `pool_size` and `max_overflow`, and enable `pool_pre_ping` because databases and firewalls drop idle connections. I also make sure pool size × number of workers stays under the database's connection limit, and use PgBouncer at larger scale."

**Key takeaway:** Reuse connections; `pool_pre_ping=True`; mind the total connection count.

---

### 13.5 Database Migrations with Alembic

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q82)*

**Definition:** **Migrations** are version-controlled scripts that change the database **schema** step by step (add a table, add a column). **Alembic** is the migration tool for SQLAlchemy; each migration has an `upgrade()` and a `downgrade()`.

```bash
alembic init migrations                                     # one-time setup
alembic revision --autogenerate -m "add user role column"   # diff models vs DB
alembic upgrade head                                        # apply all pending
alembic downgrade -1                                        # roll back one step
```

```python
# migrations/env.py: point Alembic at your models
from myapp.models import Base
target_metadata = Base.metadata

# migrations/versions/xxxx_add_user_role_column.py (generated, then reviewed)
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("users",
        sa.Column("role", sa.String(50), nullable=False, server_default="user"))

def downgrade():
    op.drop_column("users", "role")
```

**🎤 Say this in the interview:**
> "I manage schema changes with Alembic migrations kept in git. Autogenerate compares my SQLAlchemy models to the database, but I always review the result — it misses things like column renames, which it sees as drop-plus-add, and some constraint changes. When adding a non-nullable column to an existing table I set a `server_default`, and I make sure every migration has a working downgrade."

**Key takeaway:** Schema changes = reviewed, versioned migrations with a downgrade.

---

### 13.6 Transaction Isolation Levels

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q84)*

**Definition:** **Isolation levels** control how much concurrent transactions can see of each other's changes — a trade-off between **consistency** and **performance/concurrency**.

**Explanation — anomalies:**
- **Dirty read** — reading another transaction's **uncommitted** data.
- **Non-repeatable read** — reading the same row twice gives different values (another transaction committed an update in between).
- **Phantom read** — re-running the same query returns **new rows** (another transaction inserted matching rows).

| Level (SQL standard) | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| READ UNCOMMITTED | Possible | Possible | Possible |
| **READ COMMITTED** | ❌ | Possible | Possible |
| REPEATABLE READ | ❌ | ❌ | Possible (standard)* |
| SERIALIZABLE | ❌ | ❌ | ❌ |

\* PostgreSQL's REPEATABLE READ uses snapshots and also prevents phantoms. **Defaults:** PostgreSQL, Oracle and SQL Server → READ COMMITTED; MySQL InnoDB → REPEATABLE READ. *(The original notes said READ COMMITTED is the default "in most DBs" — true for many, but not MySQL.)*

```text
Phantom read example:
T1: SELECT COUNT(*) FROM orders WHERE user_id = 1;   → 5
T2: INSERT INTO orders (user_id) VALUES (1); COMMIT;
T1: SELECT COUNT(*) FROM orders WHERE user_id = 1;   → 6   ← phantom row
```

```python
from sqlalchemy import text

async with db.begin():                       # SQLAlchemy AsyncSession
    await db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
    ...                                      # be ready to retry on serialization failures

# Or per engine: create_async_engine(url, isolation_level="SERIALIZABLE")
```

**🎤 Say this in the interview:**
> "Isolation levels decide which concurrency anomalies are allowed — dirty reads, non-repeatable reads and phantom reads. READ COMMITTED, the PostgreSQL default, is fine for most apps. For things like financial transfers I use SERIALIZABLE or explicit row locks with `SELECT ... FOR UPDATE`, and handle the serialization errors with retries. Higher isolation means more locking or aborts, so lower throughput."

**Key takeaway:** Higher isolation = fewer anomalies, less concurrency. Default to READ COMMITTED.

---

### 13.7 Preventing SQL Injection

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q85)*

**Definition:** **SQL injection** happens when user input is put directly into a SQL string, letting an attacker change the query (e.g., `1; DROP TABLE users; --`). Prevent it with **parameterized queries** — the driver sends the values separately from the SQL text.

```python
# BAD: string formatting puts user input into the SQL text
user_input = "1; DROP TABLE users; --"
query = f"SELECT * FROM users WHERE id = {user_input}"      # NEVER do this

# GOOD: bound parameter with text()
from sqlalchemy import select, text
result = await db.execute(
    text("SELECT * FROM users WHERE id = :user_id"),
    {"user_id": user_id},
)

# GOOD: the ORM / Core builds parameterized SQL for you
user = await db.get(User, user_id)
result = await db.execute(select(User).where(User.email == user_email))

# Plain DB-API (sqlite3, psycopg) uses placeholders the same way
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))   # psycopg style
```

A runnable demonstration with the built-in `sqlite3`:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
conn.execute("INSERT INTO users VALUES (1, 'Raj'), (2, 'Priya')")

evil = "1 OR 1=1"
print(conn.execute(f"SELECT name FROM users WHERE id = {evil}").fetchall())   # injected!
print(conn.execute("SELECT name FROM users WHERE id = ?", (evil,)).fetchall())  # safe
```

**Output:**
```text
[('Raj',), ('Priya',)]
[]
```

**🎤 Say this in the interview:**
> "I never build SQL with string formatting. I use the SQLAlchemy ORM or parameterized queries with bound parameters, so the driver sends the values separately and they can't change the query structure. Injection is one of the OWASP Top 10 risks. Least-privilege database users add another layer of defence."

**Key takeaway:** Parameters, never f-strings, for SQL.

---

### 13.8 Full-Text Search in PostgreSQL

🟢 **P3** · Level: Hard · Frequency: Frequent · *(Source: Q87)*

**Definition:** PostgreSQL has built-in **full-text search**: `tsvector` (pre-processed, stemmed document terms) is matched against `tsquery` (search terms) with the `@@` operator, sped up by a **GIN index**.

```sql
-- Generated search column (PostgreSQL 12+) stays up to date automatically
ALTER TABLE products ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (to_tsvector('english', name || ' ' || coalesce(description, ''))) STORED;

CREATE INDEX idx_products_search ON products USING GIN (search_vector);

SELECT name, ts_rank(search_vector, query) AS rank
FROM products, to_tsquery('english', 'laptop & gaming') AS query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

```python
from sqlalchemy import func, select

result = await db.execute(
    select(Product).where(
        func.to_tsvector("english", Product.name)
            .op("@@")(func.to_tsquery("english", "laptop"))
    )
)
```

| Need | Tool |
|---|---|
| Keyword search inside an existing Postgres app | `tsvector` + GIN |
| Fuzzy / typo-tolerant `LIKE '%x%'` | `pg_trgm` extension + GIN/GiST trigram index |
| Large scale, facets, multi-language, relevance tuning | Elasticsearch / OpenSearch |

> The original notes used a plain `UPDATE` to fill the column, which goes stale when rows change. A generated column (or a trigger) keeps it current.

**🎤 Say this in the interview:**
> "For simple keyword search I use Postgres full-text search — a `tsvector` column with a GIN index, queried with `to_tsquery` and ranked with `ts_rank`. For fuzzy matching I add `pg_trgm`. If I need facets, multi-language analysis or very large scale, I'd move search to Elasticsearch or OpenSearch."

**Key takeaway:** `tsvector` + GIN for built-in search; Elasticsearch for heavy search.

---

### 13.9 Redis and Its Data Structures

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q86)*

**Definition:** **Redis** is an **in-memory** data store used as a cache, message broker, rate limiter and more. It supports rich data structures, not just plain key-value strings.

| Structure | Commands | Use case |
|---|---|---|
| String | `SET`, `GET`, `SETEX`, `INCR` | Caching, counters, distributed locks |
| List | `LPUSH`, `RPOP`, `LTRIM` | Queues, recent-items lists |
| Hash | `HSET`, `HGETALL` | Objects (user profile fields) |
| Set | `SADD`, `SCARD`, `SISMEMBER` | Unique visitors, tags |
| Sorted set | `ZADD`, `ZREVRANGE`, `ZRANGEBYSCORE` | Leaderboards, sliding-window rate limits |
| Stream | `XADD`, `XREADGROUP` | Event logs, consumer groups |
| Pub/Sub | `PUBLISH`, `SUBSCRIBE` | Real-time notifications (fire-and-forget) |

```python
import redis

r = redis.Redis(decode_responses=True)          # return str instead of bytes

r.setex("user:1:name", 300, "Raj")               # string with a 5-minute TTL
print(r.get("user:1:name"))                      # Raj

r.lpush("notifications:1", "Order shipped")      # list: newest first
r.ltrim("notifications:1", 0, 9)                 # keep the last 10

r.hset("user:1", mapping={"name": "Raj", "role": "admin"})
print(r.hgetall("user:1"))                       # {'name': 'Raj', 'role': 'admin'}

r.zadd("leaderboard", {"Raj": 1500, "Priya": 2000, "Anita": 1800})
print(r.zrevrange("leaderboard", 0, 2, withscores=True))
# [('Priya', 2000.0), ('Anita', 1800.0), ('Raj', 1500.0)]

r.sadd("visitors:today", "user:1", "user:2", "user:1")
print(r.scard("visitors:today"))                 # 2 (unique)
```

**Caching pattern (cache-aside):** read from cache → on a miss, read the DB → write to the cache with a TTL → invalidate or update the cache on writes.

**🎤 Say this in the interview:**
> "Redis is an in-memory store with rich data structures. I use strings with TTLs for caching, hashes for objects, sets for uniqueness, sorted sets for leaderboards and sliding-window rate limiting, lists or streams for queues, and Pub/Sub for real-time notifications. My usual pattern is cache-aside with TTLs, plus invalidation when data changes."

**Follow-ups:**
- **Q: Is Redis data persistent?** — Optionally: RDB snapshots and/or an AOF log. Treat a cache as disposable.
- **Q: Cache problems?** — Stale data (TTL + invalidation), cache stampede (locks or randomised TTLs), memory limits (eviction policies like `allkeys-lru`).

**Key takeaway:** Redis = in-memory data structures; cache-aside + TTL.

---

## 14. Testing

### 14.1 Writing Tests with `pytest`

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q44)*

**Definition:** **pytest** is Python's most popular test framework: plain `assert` statements, **fixtures** for setup/teardown, **parametrize** for running one test with many inputs, and a large plugin ecosystem.

**Explanation:**
- Test files `test_*.py`, functions `test_*`.
- **Fixtures** (`@pytest.fixture`) provide reusable setup and are injected by parameter name.
- `@pytest.mark.parametrize` runs one test for each set of inputs.
- `pytest.raises` asserts that an exception is raised.
- **Test pyramid:** many unit tests → fewer integration tests → few end-to-end tests.

```python
# test_users.py   (run: pytest -v)
import pytest
from fastapi.testclient import TestClient
from main import app        # assumes POST /users returns 201 and validates age with Field(gt=0, lt=150)

client = TestClient(app)

@pytest.fixture
def sample_user():
    return {"name": "Raj", "email": "raj@test.com", "age": 25, "password": "s3cret!"}

def test_create_user(sample_user):
    response = client.post("/users", json=sample_user)
    assert response.status_code == 201
    assert response.json()["name"] == "Raj"

@pytest.mark.parametrize("age", [-1, 0, 999])
def test_invalid_age(sample_user, age):
    sample_user["age"] = age
    assert client.post("/users", json=sample_user).status_code == 422

def test_division_error():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

**🎤 Say this in the interview:**
> "I use pytest with plain asserts, fixtures for reusable setup, and parametrize to cover many inputs with one test. For FastAPI I use `TestClient` and override dependencies like the database. I follow the test pyramid — mostly fast unit tests, fewer integration tests, and a few end-to-end tests — and mock external services."

**Key takeaway:** Fixtures + parametrize + `pytest.raises` + `TestClient`.

---

### 14.2 Fixture Scope

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q89)*

**Definition:** A fixture's **scope** controls how often it's created: `function` (default, every test), `class`, `module` (once per file), `package`, `session` (once per test run).

**Explanation:** Use a broad scope for **expensive, read-only** setup (DB engine, app instance) and `function` scope for anything **mutable** (a DB session/transaction rolled back after each test), so tests stay isolated and fast.

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")          # created once per test run
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    yield engine
    engine.dispose()

@pytest.fixture                           # function scope: fresh for every test
def db_session(db_engine):
    conn = db_engine.connect()
    tx = conn.begin()
    session = Session(bind=conn)
    yield session
    session.close()
    tx.rollback()                         # undo everything this test did
    conn.close()

@pytest.fixture(scope="module")           # once per test file
def seeded_users(db_engine):
    with db_engine.begin() as conn:
        conn.execute(insert_users_sql)
    yield
    with db_engine.begin() as conn:
        conn.execute(delete_users_sql)
```

**🎤 Say this in the interview:**
> "Fixture scope controls how often setup runs. I make the database engine session-scoped because it's expensive, and give each test a function-scoped session inside a transaction that's rolled back afterwards. That keeps the suite fast without tests leaking state into each other."

**Key takeaway:** Expensive & immutable → `session` scope. Mutable state → `function` scope + rollback.

---

### 14.3 Mocking with `unittest.mock`

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q88)*

**Definition:** **Mocking** replaces real dependencies (APIs, databases, email, time) with **fake objects** during a test, so you can test code in isolation and **assert how dependencies were called**.

**Explanation:**
- `Mock`/`MagicMock` — fake objects that record calls; set `.return_value` or `.side_effect`.
- `AsyncMock` — for `async` functions.
- `patch("path.to.name")` — temporarily replaces a name (as a decorator or context manager).
- ⚠️ **Patch where the name is used, not where it's defined.** If `myapp/services.py` does `from myapp.utils import send_email`, patch `myapp.services.send_email`.

```python
from unittest.mock import MagicMock, patch

class PaymentGateway:
    def charge(self, amount):
        raise RuntimeError("real network call!")

def checkout(gateway, amount):
    if gateway.charge(amount)["status"] == "ok":
        return "paid"
    return "failed"

fake = MagicMock()
fake.charge.return_value = {"status": "ok"}
print(checkout(fake, 100))
fake.charge.assert_called_once_with(100)

fake.charge.side_effect = TimeoutError("gateway timeout")   # simulate a failure
try:
    checkout(fake, 100)
except TimeoutError as e:
    print("TimeoutError:", e)

import os
with patch("os.getcwd", return_value="/fake/dir"):          # patch a module attribute
    print(os.getcwd())
print(os.getcwd() != "/fake/dir")                           # restored afterwards
```

**Output:**
```text
paid
TimeoutError: gateway timeout
/fake/dir
True
```

Patching in an application test (snippet — `myapp` is a placeholder; async tests need `pytest-asyncio`):

```python
import pytest
from unittest.mock import AsyncMock, patch

@patch("myapp.services.send_email")             # where it is USED
def test_register_sends_email(mock_email):
    mock_email.return_value = True
    register_user("raj@test.com")
    mock_email.assert_called_once_with("raj@test.com")

@pytest.mark.asyncio
async def test_async_service():
    with patch("myapp.services.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": [1, 2, 3]}
        assert await process_data() == [1, 2, 3]
```

**🎤 Say this in the interview:**
> "Mocking replaces external dependencies with fakes so I can test my logic in isolation and assert how those dependencies were called. I use `patch`, `MagicMock` and `AsyncMock`, with `return_value` for normal responses and `side_effect` to simulate errors. The classic gotcha is that you patch the name where it's looked up — the module that imports it — not where it's defined."

**Key takeaway:** Patch where it's used; `return_value` for results, `side_effect` for errors.

---

### 14.4 Code Coverage

🟢 **P3** · Level: Easy · Frequency: Frequent · *(Source: Q90)*

**Definition:** **Code coverage** measures which lines (and branches) your tests execute. In pytest, use the `pytest-cov` plugin (built on `coverage.py`).

```bash
pip install pytest-cov
pytest --cov=myapp --cov-report=term-missing      # show uncovered line numbers
pytest --cov=myapp --cov-report=html              # browsable report in htmlcov/
pytest --cov=myapp --cov-fail-under=80            # fail CI if coverage drops below 80%
pytest --cov=myapp --cov-branch                   # branch coverage too
```

```ini
# .coveragerc
[run]
source = myapp
omit =
    */tests/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    if TYPE_CHECKING:
```

> The original notes used `[coverage:run]` section names — those are for `setup.cfg`/`tox.ini`. In a `.coveragerc` file the sections are `[run]` and `[report]`.

**🎤 Say this in the interview:**
> "I measure coverage with `pytest-cov` and enforce a threshold in CI, usually around 80% on business logic. But coverage only shows a line ran, not that it was checked — a test without meaningful asserts adds coverage but no safety. So I focus on business logic, edge cases and branch coverage rather than chasing 100%."

**Key takeaway:** Coverage is a floor, not proof of correctness.

---

## 15. DevOps, Architecture & System Design

### 15.1 Docker and Containerizing a FastAPI App

🔴 **P1** · Level: Medium · Frequency: Very frequent · *(Source: Q45)*

**Definition:** **Docker** packages an application with its runtime and dependencies into an **image**; a running image is a **container**. A `Dockerfile` defines the image; **Docker Compose** runs multi-container setups (app + DB + Redis).

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   # cached layer: changes only when requirements change
COPY . .
RUN useradd -m appuser
USER appuser                                          # don't run as root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db, redis]
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
  redis:
    image: redis:7
```

**Best practices:** copy `requirements.txt` before the code (layer caching), use **multi-stage builds** for smaller images, add a `.dockerignore` (`__pycache__`, `.env`, `.git`, `venv`), run as a non-root user, and pass secrets through the environment rather than baking them into the image.

**🎤 Say this in the interview:**
> "Docker packages the app and its dependencies into an image so it runs the same everywhere. For a FastAPI service I start from a slim Python image, install requirements before copying the code so the layer is cached, run uvicorn as a non-root user, and use a `.dockerignore`. Locally I use Compose to run the app with Postgres and Redis; in production I use multi-stage builds and pass config through environment variables."

**Key takeaway:** Slim base, cached dependency layer, non-root, `.dockerignore`, multi-stage.

---

### 15.2 The 12-Factor App

🟠 **P2** · Level: Medium · Frequency: Frequent · *(Source: Q99)*

**Definition:** The **12-factor app** is a methodology for building portable, scalable, deployable web services. The factors most relevant to Python backends:

| # | Factor | In Python practice |
|---|---|---|
| 1 | Codebase | One repo, many deploys |
| 2 | Dependencies | Declared explicitly (`requirements.txt` / `pyproject.toml`), isolated in a venv or container |
| **3** | **Config** | **In environment variables** — `pydantic-settings` (12.13) |
| 4 | Backing services | DB, Redis, S3 as attached resources accessed by URL — swappable |
| 5 | Build, release, run | Separate stages (Docker image → release with config → run) |
| **6** | **Processes** | **Stateless** — keep state in DB/Redis, not in memory or local disk |
| 7 | Port binding | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| 8 | Concurrency | Scale out with processes (`--workers 4`, more pods) |
| 9 | Disposability | Fast start-up, graceful shutdown |
| 10 | Dev/prod parity | Same stack everywhere (Docker) |
| **11** | **Logs** | **Write to stdout** as an event stream; the platform collects them |
| 12 | Admin processes | One-off tasks (migrations) run as separate processes |

```python
import logging
logging.basicConfig(level=logging.INFO)          # factor 11: log to stdout/stderr, not files
logging.getLogger(__name__).info("service started")
```

**🎤 Say this in the interview:**
> "12-factor is a set of practices for cloud-ready services. The ones I apply most are: config in environment variables via pydantic-settings, stateless processes with state in Postgres or Redis so I can scale horizontally, backing services as swappable URLs, logs written to stdout for the platform to collect, and dev/prod parity through Docker."

**Key takeaway:** Env config, stateless processes, logs to stdout, Docker parity.

---

### 15.3 Designing a Task Queue (Celery)

🟠 **P2** · Level: Hard · Frequency: Frequent · *(Source: Q97)*

**Definition:** A **task queue** moves slow or unreliable work out of the request cycle. Components: **producer** (the web app enqueues tasks), **broker** (Redis/RabbitMQ holds messages), **workers** (separate processes execute tasks), and an optional **result backend**.

```text
Client → FastAPI ──enqueue──▶ Broker (Redis/RabbitMQ) ──▶ Worker processes ──▶ Result backend
          (returns 202 immediately)
```

```python
from celery import Celery
from celery.utils.log import get_task_logger

celery_app = Celery("tasks",
                    broker="redis://localhost:6379/0",
                    backend="redis://localhost:6379/1")
logger = get_task_logger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60, acks_late=True)
def send_email(self, to: str, subject: str, body: str):
    try:
        smtp_send(to, subject, body)
        logger.info("Email sent to %s", to)
    except ConnectionError as exc:
        # exponential backoff: 60s, 120s, 240s
        raise self.retry(exc=exc, countdown=60 * 2 ** self.request.retries)

@router.post("/send-newsletter", status_code=202)
async def send_newsletter(emails: list[str]):
    for email in emails:
        send_email.delay(email, "Newsletter", "Content...")   # enqueue, don't wait
    return {"queued": len(emails)}

# Start workers: celery -A tasks worker --loglevel=info --concurrency=4
```

**Design points:** make tasks **idempotent** (they may run more than once), pass IDs rather than large objects, use retries with exponential backoff for transient failures, set timeouts, use dead-letter handling for poison messages, and monitor with **Flower**.

**🎤 Say this in the interview:**
> "A task queue decouples slow work from the request: the API enqueues a message to a broker like Redis or RabbitMQ and returns immediately, and separate worker processes do the job. In Celery, `bind=True` gives access to `self` for retries, and I use `max_retries` with exponential backoff for transient errors. Tasks must be idempotent because they can be delivered more than once."

**Key takeaway:** Producer → broker → workers; idempotent tasks, retries with backoff.

---

### 15.4 Designing a URL Shortener

🟠 **P2** · Level: Hard · Frequency: Very frequent · *(Source: Q96)*

**Definition:** A URL shortener maps a short code to a long URL. Core pieces: **code generation**, **storage** (database as the source of truth + Redis cache), and a fast **redirect endpoint**.

**Key design decisions:**

| Decision | Options |
|---|---|
| Code generation | Hash of the URL (MD5/SHA → base62/base64, truncated) **or** auto-increment ID → base62 (no collisions) **or** random code + uniqueness check |
| Collisions | Unique constraint on `code`; on conflict, retry with a salt or a new random code |
| Read path | Cache-aside in Redis (reads ≫ writes) |
| Redirect code | **301** permanent (cached by browsers — fewer hits, but you lose analytics and can't change the target) vs **302** temporary (every click hits your server — analytics, editable) |
| Extras | Custom aliases, expiry (TTL), click analytics (async via a queue), rate limiting |

```python
import base64
import hashlib
import time
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

def generate_short_code(url: str, length: int = 7) -> str:
    digest = hashlib.md5(url.encode()).digest()          # not for security, just spreading
    return base64.urlsafe_b64encode(digest)[:length].decode()

@app.post("/shorten")
async def shorten_url(url: str, db=Depends(get_db)):
    code = generate_short_code(url)
    existing = await db.get(ShortURL, code)
    if existing and existing.original_url != url:        # collision → salt and retry
        code = generate_short_code(url + str(time.time()))
    if not existing or existing.original_url != url:
        db.add(ShortURL(code=code, original_url=url))
        await db.commit()
    await cache.setex(f"url:{code}", 86400, url)          # async Redis client, 24h TTL
    return {"short_url": f"https://short.ly/{code}"}

@app.get("/{code}")
async def redirect(code: str, db=Depends(get_db)):
    if url := await cache.get(f"url:{code}"):             # cache first
        return RedirectResponse(url, status_code=302)
    short = await db.get(ShortURL, code)
    if not short:
        raise HTTPException(404, "URL not found")
    await cache.setex(f"url:{code}", 86400, short.original_url)
    return RedirectResponse(short.original_url, status_code=302)
```

**🎤 Say this in the interview:**
> "I'd generate a short code either from a base62-encoded unique ID or a truncated hash with collision checks backed by a unique constraint. Postgres stores the mapping, and because reads vastly outnumber writes I put a Redis cache-aside layer in front of the redirect endpoint. 301 redirects are cached by browsers, which reduces load but loses analytics, so if we need click tracking or editable links I'd use 302 and record clicks asynchronously through a queue."

**Key takeaway:** Unique code generation + DB + Redis cache; 301 vs 302 trade-off.

---

### 15.5 Debugging a Slow API Endpoint in Production

🔴 **P1** · Level: Hard · Frequency: Very frequent · *(Sources: Q100 + Q50 + Q91 — merged)*

**Definition:** A systematic process: **measure → identify → fix → verify**. Don't guess.

**Step-by-step approach:**

| Step | Action | Tools |
|---|---|---|
| 1. Measure | Confirm which endpoint is slow, how often, and since when (a recent deploy?) | APM (Datadog, New Relic, Sentry), timing middleware, p95/p99 latency |
| 2. Database | Look for slow queries, N+1, missing indexes | SQL logging, `EXPLAIN ANALYZE`, `pg_stat_statements` |
| 3. Application | Find hot code paths | `py-spy` (no code changes), `cProfile` |
| 4. External calls | Slow third-party APIs, missing timeouts | Tracing (OpenTelemetry) |
| 5. Fix | Index (`CREATE INDEX CONCURRENTLY`), eager loading, caching, async I/O, pagination, background jobs | |
| 6. Verify | Compare metrics before and after | Dashboards, load tests |

```python
import logging
import time
from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")                                # Step 1: measure every request
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
    if duration_ms > 500:
        logger.warning("SLOW: %s took %.0fms", request.url.path, duration_ms)
    return response

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)    # Step 2: log SQL (dev/staging)

# Step 2: inspect a slow query plan
#   EXPLAIN ANALYZE SELECT ... ;
# Step 5: add an index without locking writes
#   CREATE INDEX CONCURRENTLY idx_orders_created ON orders(created_at);
# Step 3: profile a live process without code changes
#   py-spy top --pid <pid>
#   py-spy record -o profile.svg --pid <pid>
```

**🎤 Say this in the interview:**
> "I treat it as a process: measure, identify, fix, verify. First I check the APM dashboard and logs to confirm the endpoint, the p95 latency and whether it started after a deploy. Then I check the database — slow queries, N+1 patterns, missing indexes — using SQL logging and EXPLAIN ANALYZE. If it's application code I profile the live process with py-spy. I fix the actual cause — an index, eager loading, caching or moving work to a background job — and verify the improvement with metrics, not intuition."

**Key takeaway:** Measure → DB → code → external calls → fix → verify with metrics.

---
## 16. Interview Strategy & Answer Templates

### 16.1 General Tips

*(From the end of Part 1)*

1. **Quantify everything** — "800 ms → 45 ms", "101 queries → 2 queries". Use numbers from your own work.
2. **Use real examples** — payment systems, user services, APIs you built.
3. **Know the why** — don't just say what you used; say why you chose it.
4. **Mention trade-offs** — every solution has downsides, and knowing them shows seniority.
5. **Practise out loud** — explaining code verbally is a different skill from writing it.

**Answer formula for any technical question:**
> **Definition** (1 line) → **how it works** (2–3 lines) → **example** → **trade-off or gotcha** → **when I use it**.

### 16.2 "Tell me about your most challenging technical problem" (STAR)

*(From the end of Part 2 — replace the numbers with your own)*

```text
Situation: An API endpoint took 3–4 seconds under load.
Task:      Bring it under 200 ms.
Action:    1. Added timing middleware to confirm the bottleneck
           2. Enabled SQL logging — found an N+1 query (101 DB calls per request)
           3. Added selectinload() → 2 queries
           4. Added a Redis cache for repeated user lookups (TTL 5 min)
Result:    Response time dropped from 3400 ms to 85 ms (40× faster)
```

### 16.3 "How do you ensure code quality?"

```text
- Type hints + mypy in CI (catches type bugs before runtime)
- pytest with 80%+ coverage on business logic
- Code review focused on N+1 queries, missing indexes, error handling
- Pre-commit hooks: formatting (black or ruff format), import sorting (isort/ruff), linting (flake8/ruff)
- Structured logging in production — errors reported to Sentry
```

### 16.4 "How do you handle a production incident?"

```text
1. Mitigate first — roll back, use a feature flag, scale up
2. Communicate — update the status page, notify stakeholders
3. Investigate — logs, metrics, recent deployments
4. Fix — a targeted patch, not a rushed rewrite
5. Post-mortem — what happened, why, how to prevent it (blameless)
```

---

## 17. Quick Revision (Last-Minute Preparation)

### 17.1 Key Definitions (One-Liners)

| Term | One-line definition |
|---|---|
| Mutable / immutable | Can / cannot be changed after creation |
| Hashable | Has a fixed hash → can be a dict key or set member |
| `is` / `==` | Same object / same value |
| Shallow copy | New container, shared nested objects |
| Deep copy | New container, recursively copied contents |
| `*args` / `**kwargs` | Extra positional args (tuple) / keyword args (dict) |
| LEGB | Name lookup order: Local → Enclosing → Global → Built-in |
| Closure | Inner function that remembers enclosing variables |
| Decorator | Function that wraps a function to add behaviour; `@d` = `f = d(f)` |
| Iterable | Has `__iter__`; can produce an iterator; re-loopable |
| Iterator | Has `__next__`; keeps state; single-use |
| Generator | Function with `yield`; lazy iterator |
| Context manager | `__enter__`/`__exit__`; `with` guarantees cleanup |
| Dunder method | Special method Python calls for operators and built-ins |
| Descriptor | Class attribute with `__get__`/`__set__`; powers `property` |
| Metaclass | Class of a class (`type`); controls class creation |
| MRO | Method lookup order (C3 linearization); `super()` follows it |
| Duck typing | If it has the method, it works — type doesn't matter |
| Protocol | Structural interface — "looks like" rather than "inherits from" |
| GIL | CPython lock: one thread runs bytecode at a time |
| Coroutine | `async def` function; suspends at `await` |
| Event loop | Scheduler that runs coroutines on one thread |
| Reference counting | Object freed when its reference count hits 0; GC handles cycles |
| `lru_cache` | Memoizes pure functions with hashable arguments |
| Pydantic | Runtime data validation from type hints |
| `Depends` | FastAPI per-request dependency injection |
| N+1 | 1 query + 1 per row; fix with eager loading |
| Index | B-tree that speeds up reads and slows writes |
| Connection pool | Reused set of open DB connections |
| JWT | Signed, stateless token; payload is not encrypted |
| CORS | Browser rule for which origins may call an API |
| Idempotent | Running it twice has the same effect as once |

### 17.2 Important Differences (Side by Side)

| Concept A | Concept B | The difference |
|---|---|---|
| list | tuple | Mutable vs immutable (tuple is hashable, slightly lighter) |
| set | list | Unique + O(1) lookup vs ordered + duplicates |
| `==` | `is` | Value vs identity |
| `=` | `copy` / `deepcopy` | Alias vs new outer object vs fully independent |
| `sorted()` | `.sort()` | New list vs in place (returns `None`) |
| `any()` | `all()` | At least one vs every (`all([])` is True) |
| `__str__` | `__repr__` | User-facing vs developer-facing (always write `__repr__`) |
| `__getattr__` | `__getattribute__` | Missing attributes only vs every access |
| `@classmethod` | `@staticmethod` | Gets `cls` (factories) vs gets nothing (helpers) |
| `property` | `cached_property` | Computed every access vs computed once |
| inheritance | composition | is-a vs has-a (prefer composition) |
| ABC | Protocol | Must inherit (nominal) vs just match (structural) |
| metaclass | `__init_subclass__` | Controls class creation vs simple subclass hook |
| dataclass | NamedTuple | Mutable class vs immutable tuple |
| dataclass | Pydantic | No validation vs runtime validation |
| iterable | iterator | Re-loopable vs single-use with `__next__` |
| generator | list | Lazy, one item in memory vs all in memory |
| `yield` | `return` | Pause and resume vs end the function |
| threading | multiprocessing | Shared memory, GIL-limited vs separate memory, true parallelism |
| threading | asyncio | Pre-emptive OS threads vs cooperative single-thread coroutines |
| concurrency | parallelism | Interleaving vs simultaneous execution |
| `asyncio.Queue` | `queue.Queue` | Coroutines (not thread-safe) vs threads (thread-safe) |
| `executor.map` | `as_completed` | Input order vs completion order |
| `BackgroundTasks` | Celery | Same process, lost on restart vs durable workers with retries |
| offset | cursor pagination | Page jumps, slow deep pages vs fast, stable, next-only |
| INNER JOIN | LEFT JOIN | Matches only vs all left rows + NULLs |
| `selectinload` | `joinedload` | 2 queries (IN) vs 1 query (JOIN) |
| 301 | 302 | Permanent, browser-cached vs temporary, every hit reaches you |
| `Mock` | `AsyncMock` | Sync vs awaitable fakes |

### 17.3 Common Pitfalls (Gotchas)

1. **Mutable default arguments** — `def f(x=[])` shares one list. Use `None`.
2. **`is` for value comparison** — works by accident for small ints (-5..256). Use `==`; `is` only for `None`.
3. **Shallow copy of nested lists** — inner lists are still shared.
4. **`lst = lst.sort()`** — sets `lst` to `None`.
5. **`all([])` is `True`** — vacuous truth.
6. **`x or default`** — replaces valid falsy values like `0` or `""`.
7. **Assigning to a global inside a function** without `global` → `UnboundLocalError`.
8. **Late-binding closures** — `[lambda: i for i in range(3)]` all return 2.
9. **Defining `__eq__` without `__hash__`** → the object becomes unhashable.
10. **Hashing mutable fields** → dict/set lookups break.
11. **Forgetting `@functools.wraps`** → decorated functions lose their name and docstring.
12. **Re-using an exhausted iterator/generator** → silently empty.
13. **`groupby` on unsorted data** → split groups.
14. **`lru_cache` with list arguments** → `TypeError: unhashable`; unbounded caches can grow forever.
15. **Thinking the GIL makes code thread-safe** — `counter += 1` can still race.
16. **Threads for CPU-bound work** — no speed-up; use processes.
17. **Blocking calls inside `async def`** (`time.sleep`, `requests`, sync Redis/DB clients) freeze the event loop.
18. **Missing `if __name__ == "__main__":`** with multiprocessing on Windows/macOS.
19. **Bare `except:` / `except Exception: pass`** — hides bugs.
20. **String concatenation in loops** — use `"".join()`.
21. **f-strings in SQL** → SQL injection. Always use parameters.
22. **`allow_origins=["*"]` with credentials** — rejected by browsers; insecure.
23. **Secrets in JWT payloads or in code** — payloads are readable; use env vars.
24. **Patching where a name is defined instead of where it's used** in `mock.patch`.
25. **Lazy-loading relationships in a loop** → N+1 queries.
26. **Accidental CROSS JOIN** (missing ON) → row explosion.
27. **Offset pagination on huge tables** — slow deep pages, duplicates when data changes.
28. **Non-nullable column added without `server_default`** → migration fails on existing rows.
29. **`BackgroundTasks` for critical jobs** — lost on restart.
30. **Optimizing without profiling** — measure first.

### 17.4 Rapid-Fire FAQ

| Question | Answer |
|---|---|
| Are dicts ordered? | Yes — insertion order guaranteed since Python 3.7 |
| What's cached for `is`? | Small ints -5..256 and some interned strings (CPython detail) |
| Can a tuple be a dict key? | Yes, if all its elements are hashable |
| Is Python pass-by-value or by reference? | Pass by object reference — mutations are visible to the caller; rebinding isn't |
| What does `__init__` return? | `None` — `__new__` creates the object |
| How do you make a class immutable? | `@dataclass(frozen=True)`, `NamedTuple`, or `__slots__` + no setters |
| What's `self`? | The instance the method was called on, passed automatically |
| Is anything truly private in Python? | No — `_x` is convention; `__x` is name-mangled to `_Class__x` |
| What does `super()` call? | The next class in the MRO of the instance's type |
| How to inspect MRO? | `Cls.__mro__` or `Cls.mro()` |
| Generator expression syntax? | `(x for x in data)` |
| What does `yield from` do? | Delegates to a sub-iterator/generator |
| What does a `for` loop call? | `iter()` once, then `next()` until `StopIteration` |
| Why `functools.wraps`? | Keeps `__name__`, `__doc__`, etc. of the wrapped function |
| Decorator stacking order? | Applied bottom-up; the top one runs first when called |
| What frees memory in CPython? | Reference counting + a cyclic generational GC |
| How to break circular imports? | Move shared code to a third module (or defer the import) |
| Does the GIL affect I/O-bound threads? | Barely — the GIL is released during I/O waits |
| Python without a GIL? | 3.13 has an experimental free-threaded build (PEP 703) |
| How to run blocking code from async? | `await asyncio.to_thread(func, ...)` |
| Run coroutines concurrently? | `asyncio.gather(...)` or `asyncio.create_task(...)` |
| `ThreadPoolExecutor` vs `ProcessPoolExecutor`? | I/O-bound vs CPU-bound |
| What is the walrus operator? | `:=` — assign inside an expression (3.8+) |
| `sorted()` algorithm and complexity? | Timsort, O(n log n), stable |
| Fast membership test? | Use a `set` (O(1) average) |
| Validation error status in FastAPI? | 422 Unprocessable Entity |
| Rate-limit exceeded status? | 429 Too Many Requests |
| Pydantic v2 replacements? | `@field_validator`, `model_dump()`, `model_config` |
| How to override dependencies in tests? | `app.dependency_overrides[dep] = fake` |
| Detect N+1? | Enable SQL logging, look for repeated queries |
| Composite index rule? | Leftmost prefix |
| PostgreSQL default isolation? | READ COMMITTED (MySQL InnoDB: REPEATABLE READ) |
| Where do 12-factor apps keep config? | Environment variables |
| Default fixture scope in pytest? | `function` |
| Measure coverage? | `pytest --cov=pkg --cov-report=term-missing` |

### 17.5 Top 25 Must-Know Topics (Study These First)

| # | Topic | Section |
|---|---|---|
| 1 | List vs tuple vs set vs dict | 1.1 |
| 2 | Mutability and hashability | 1.2 |
| 3 | `==` vs `is` | 1.3 |
| 4 | Shallow vs deep copy | 1.4 |
| 5 | `*args` / `**kwargs` | 3.1 |
| 6 | Mutable default argument | 3.2 |
| 7 | Closures | 3.5 |
| 8 | Exception handling | 4.1 |
| 9 | Classes, `__init__`, OOP pillars | 5.1, 5.2 |
| 10 | Composition vs inheritance | 5.4 |
| 11 | classmethod vs staticmethod | 5.5 |
| 12 | Dataclasses | 5.7 |
| 13 | Dunder methods, `__str__` vs `__repr__` | 6.1, 6.2 |
| 14 | Iterators vs iterables | 8.1 |
| 15 | Generators | 8.2 |
| 16 | Decorators | 8.3 |
| 17 | Context managers | 8.5 |
| 18 | GIL | 10.1 |
| 19 | Threading vs multiprocessing vs asyncio | 10.2 |
| 20 | async/await and the event loop | 10.5 |
| 21 | FastAPI, Pydantic, `Depends` | 12.1–12.3 |
| 22 | JWT auth and pagination | 12.7, 12.12 |
| 23 | JOINs, indexing, N+1, SQL injection | 13.1–13.3, 13.7 |
| 24 | pytest and mocking | 14.1, 14.3 |
| 25 | Debugging a slow endpoint | 15.5 |

---

## Appendix: Source Coverage Map

Every question from both source files and where it lives in this guide. Duplicates were merged into one section.

| Source Q | Topic | Section | | Source Q | Topic | Section |
|---|---|---|---|---|---|---|
| Q1 | list/tuple/set/dict | 1.1 | | Q51 | deepcopy vs `=` | 1.4 (merged) |
| Q2 | `is` vs `==` | 1.3 | | Q52 | Dunder methods | 6.1 |
| Q3 | Mutability | 1.2 | | Q53 | `__hash__` | 6.3 |
| Q4 | Shallow vs deep copy | 1.4 | | Q54 | Multiple inheritance, MRO | 5.3 |
| Q5 | Truthy/falsy | 1.5 | | Q55 | Monkey patching | 6.10 |
| Q6 | List comprehension | 1.10 | | Q56 | Metaclasses | 6.7 |
| Q7 | Type hints | 3.6 | | Q57 | `__init_subclass__` | 6.8 |
| Q8 | `is None` | 1.3 (merged) | | Q58 | functools | 2.3 |
| Q9 | Memory management | 9.1 | | Q59 | itertools | 2.2 |
| Q10 | Import system | 9.2 | | Q60 | any/all | 1.6 |
| Q11 | enumerate/zip | 1.11 | | Q61 | Walrus operator | 1.9 |
| Q12 | collections | 2.1 | | Q62 | Sorting | 1.7 |
| Q13 | f-strings | 1.8 | | Q63 | sys.argv/argparse | 2.4 |
| Q14 | Exception handling | 4.1 | | Q64 | concurrent.futures | 10.3 |
| Q15 | `*args`/`**kwargs` | 3.1 | | Q65 | Composition vs inheritance | 5.4 |
| Q16 | Mutable default | 3.2 | | Q66 | Singleton | 7.1 |
| Q17 | lambda/map/filter/reduce | 3.3 | | Q67 | Factory | 7.2 |
| Q18 | Scope | 3.4 | | Q68 | Observer | 7.3 |
| Q19 | Classes, `__init__` | 5.1 | | Q69 | `__call__` | 6.4 |
| Q20 | Inheritance | 5.2.1, 5.3 | | Q70 | Descriptors | 6.6 |
| Q21 | Polymorphism | 5.2.2 | | Q71 | `__getattr__` vs `__getattribute__` | 6.5 |
| Q22 | Encapsulation | 5.2.3 | | Q72 | Custom iterator | 8.1 (merged) |
| Q23 | Abstract base classes | 5.2.4, 6.9 | | Q73 | namedtuple | 2.1 (merged) |
| Q24 | Dataclasses | 5.7 | | Q74 | Protocol | 6.9 |
| Q25 | `__str__` vs `__repr__` | 6.2 | | Q75 | JWT auth | 12.7 |
| Q26 | property | 5.6 | | Q76 | Rate limiting | 12.8 |
| Q27 | staticmethod/classmethod | 5.5 | | Q77 | Background tasks | 12.9 |
| Q28 | `__slots__` | 5.8 | | Q78 | File uploads | 12.10 |
| Q29 | Decorators | 8.3 | | Q79 | CORS | 12.5 (merged) |
| Q30 | Decorators with arguments | 8.4 | | Q80 | API versioning | 12.11 |
| Q31 | Generators | 8.2 | | Q81 | Connection pooling | 13.4 |
| Q32 | Iterator vs iterable | 8.1 | | Q82 | Alembic | 13.5 |
| Q33 | Closures | 3.5 | | Q83 | INNER/LEFT/CROSS JOIN | 13.1 (merged) |
| Q34 | Context managers | 8.5 | | Q84 | Isolation levels | 13.6 |
| Q35 | GIL | 10.1 | | Q85 | SQL injection | 13.7 |
| Q36 | Threading vs MP vs async | 10.2 | | Q86 | Redis | 13.9 |
| Q37 | async/await | 10.5 | | Q87 | Full-text search | 13.8 |
| Q38 | Blocking the event loop | 10.6 | | Q88 | Mocking | 14.3 |
| Q39 | FastAPI vs Flask | 12.1 | | Q89 | Fixture scope | 14.2 |
| Q40 | Pydantic | 12.2 | | Q90 | Coverage | 14.4 |
| Q41 | FastAPI exceptions | 12.4 | | Q91 | Profiling | 11.1 |
| Q42 | Middleware | 12.5 | | Q92 | lru_cache | 2.3 (merged) |
| Q43 | CRUD with DB | 12.6 | | Q93 | Performance anti-patterns | 11.2 |
| Q44 | pytest | 14.1 | | Q94 | Pool vs ProcessPoolExecutor | 10.4 |
| Q45 | Docker | 15.1 | | Q95 | asyncio.Queue | 10.7 |
| Q46 | Dependency injection | 12.3 | | Q96 | URL shortener | 15.4 |
| Q47 | Env vars and config | 12.13 | | Q97 | Task queue | 15.3 |
| Q48 | SQL JOINs | 13.1 | | Q98 | Pagination | 12.12 |
| Q49 | Indexing | 13.2 | | Q99 | 12-factor app | 15.2 (+12.13) |
| Q50 | N+1 problem | 13.3 | | Q100 | Debugging a slow endpoint | 15.5 |

### Corrections Made to the Source Notes

These changes keep the original meaning but fix code that was outdated or would not run as written:

| Where | Original | Fixed to |
|---|---|---|
| Q5 (1.5) | Used an undefined `input_name` | Defined it so the example runs |
| Q54 (5.3) | `B2` example referenced a `C2` class that didn't exist | Complete cooperative `super()` example |
| Q55 (6.10) | Replaced `datetime.datetime` globally | Scoped patching; note that built-in types can't be patched directly |
| Q92 (2.3) | Cached query built SQL with an f-string (injection risk) | Parameterized query |
| Q95 (10.7) | Called `asyncio.Queue` "thread-safe" | It's for coroutines in one event loop; use `queue.Queue` for threads |
| Q84 (13.6) | "READ COMMITTED is the default in most DBs" | Added that MySQL InnoDB defaults to REPEATABLE READ; mixed SQL/Python split into separate blocks |
| Q43 (12.6) | `user.dict()`, `sessionmaker` | Pydantic v2 `model_dump()`, SQLAlchemy 2.0 `async_sessionmaker` |
| Q75 (12.7) | `datetime.utcnow()` (deprecated in 3.12), `python-jose` | `datetime.now(timezone.utc)`, PyJWT (python-jose noted as an alternative) |
| Q76 (12.8) | Sync Redis client inside an async dependency | `redis.asyncio` |
| Q37 (10.5) | `aiohttp` call with a relative URL and no base URL | Added `base_url` |
| Q39 (12.1) | "2–3× faster than Flask" | Benchmarks vary; described qualitatively |
| Q44 (14.1) | Test expected 201 and 422 without the route being set up for it | Stated the assumptions (status code and `Field` constraints) |
| Q64/Q94 (10.3–10.4) | Process pools without a `__main__` guard | Added `if __name__ == "__main__":` |
| Q90 (14.4) | `[coverage:run]` sections in `.coveragerc` | `[run]`/`[report]` (the prefixed form is for `setup.cfg`/`tox.ini`) |
| Q96 (15.4) | Missing `Depends`/`time` imports; sync Redis inside async | Imports added; async cache client; 301 vs 302 trade-off kept |
| Q68 (7.3) | Cited `@app.on_event` | Noted it's deprecated in favour of `lifespan` |

---

*End of guide. Revise Section 17 the night before; practise the 🎤 answers out loud.*
