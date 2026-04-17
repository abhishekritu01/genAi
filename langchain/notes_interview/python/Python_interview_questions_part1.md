# Python Interview Questions — Crack Any Interview
> 50 most important questions with full answers, code examples and interviewer tips

---

## Core Python

### Q1. What is the difference between a list, tuple, set, and dict?
**Level:** Easy | **Frequency:** Very frequent

**Answer:**
- **List:** ordered, mutable, allows duplicates
- **Tuple:** ordered, immutable, allows duplicates
- **Set:** unordered, mutable, no duplicates
- **Dict:** key-value pairs, ordered (Python 3.7+), keys unique

```python
# List
a = [1, 2, 2]       # mutable, ordered
# Tuple
b = (1, 2, 2)       # immutable, ordered
# Set
c = {1, 2, 2}       # {1, 2} — no duplicates
# Dict
d = {"name": "Raj"} # key-value
```

> **Interviewer tip:** "When would you choose each?" — sets for O(1) lookup, tuples for fixed data like coordinates.

---

### Q2. What is the difference between `is` and `==`?
**Level:** Easy | **Frequency:** Very frequent

**Answer:**
`==` checks value equality. `is` checks identity — whether both variables point to the same object in memory.

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True  (same value)
print(a is b)   # False (different objects)

x = 256
y = 256
print(x is y)   # True (CPython caches small ints)
```

> **Interviewer tip:** Gotcha: CPython caches integers -5 to 256 and interned strings — 'is' can trick you. Always use == for value comparison.

---

### Q3. What is mutability in Python?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
Mutable objects can be changed after creation (list, dict, set). Immutable objects cannot (int, str, tuple, frozenset). Immutability is important for dict keys and set elements.

```python
# Mutable
lst = [1, 2]
lst.append(3)   # OK

# Immutable
tup = (1, 2)
# tup[0] = 9   # TypeError!

# Why it matters for dicts:
d = {[1,2]: "val"}  # TypeError — lists can't be keys
```

> **Interviewer tip:** Say: "Immutable objects are hashable, which is why they can be dict keys or set members."

---

### Q4. Explain shallow copy vs deep copy.
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Shallow copy creates a new object but references the same nested objects. Deep copy creates a fully independent clone, recursively copying all nested objects.

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep    = copy.deepcopy(original)

original[0][0] = 99

print(shallow[0][0])  # 99  — shared reference!
print(deep[0][0])     # 1   — independent copy
```

> **Interviewer tip:** Common follow-up: "When would deep copy cause a problem?" — circular references, very large objects (memory).

---

### Q5. What are Python's truthy and falsy values?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
Falsy: `None`, `False`, `0`, `0.0`, `''`, `[]`, `{}`, `set()`, `()`. Everything else is truthy.

```python
# Falsy
if not []:    print("empty list is falsy")
if not "":    print("empty string is falsy")
if not 0:     print("zero is falsy")
if not None:  print("None is falsy")

# Idiomatic usage
name = input_name or "Guest"
```

> **Interviewer tip:** Say: "I use this for default value patterns and guard clauses to write cleaner code."

---

### Q6. What is list comprehension and when should you use it?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
List comprehension creates a new list in a single readable line. It's faster than a for loop + append because it's optimized at the C level in CPython.

```python
# Basic
squares = [x**2 for x in range(10)]

# With filter
evens = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
word_len = {w: len(w) for w in ["python", "fast", "api"]}

# Set comprehension
unique_lens = {len(w) for w in ["hi", "hello", "hey"]}
```

> **Interviewer tip:** Prefer comprehensions for simple transforms. Use regular loops when logic is complex — readability wins.

---

### Q7. What are type hints and why use them?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
Type hints annotate function parameters and return types. They don't enforce types at runtime but enable static analysis (mypy), better IDE autocomplete, and serve as documentation.

```python
from typing import Optional, List

def find_user(user_id: int) -> Optional[dict]:
    pass

def process(data: list) -> List[str]:
    pass

# Python 3.10+ syntax (cleaner)
def find(uid: int) -> dict | None:
    pass
```

> **Interviewer tip:** Say: "I use mypy in CI to catch type errors before runtime. FastAPI's whole validation system is powered by type hints."

---

### Q8. What is the difference between `==` and `is` for None checks?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
Always use `is None` or `is not None` — never `== None`. None is a singleton in Python.

```python
x = None

# Correct
if x is None:
    print("x is None")

# Wrong — a custom class could override __eq__
class Weird:
    def __eq__(self, other): return True

w = Weird()
print(w == None)   # True  ← dangerous!
print(w is None)   # False ← correct
```

> **Interviewer tip:** PEP 8 explicitly states: comparisons to singletons like None should use 'is' and 'is not'.

---

### Q9. How does Python's memory management work?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Python uses reference counting as the primary mechanism — objects are freed when their reference count hits 0. A cyclic garbage collector handles circular references.

```python
import sys
import gc

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount arg)

b = a
print(sys.getrefcount(a))  # 3

del b
print(sys.getrefcount(a))  # 2

# Circular reference — GC handles this
class Node:
    def __init__(self): self.ref = None
n1, n2 = Node(), Node()
n1.ref, n2.ref = n2, n1   # cycle
del n1, n2
gc.collect()               # cleans up cycle
```

> **Interviewer tip:** Mention: `__slots__` reduces memory per instance by replacing instance `__dict__` with a fixed-size array.

---

### Q10. How does Python's import system work?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
When you import a module, Python checks `sys.modules` cache first. If not found, it searches `sys.path`. The module is executed once and cached. Circular imports happen when two modules import each other.

```python
import sys

# Check if already imported
print("os" in sys.modules)   # True

# See where Python looks
print(sys.path)

# Fix circular imports with deferred imports
def get_thing():
    from module_b import Thing  # import inside function
    return Thing()
```

> **Interviewer tip:** Circular imports are a design smell — fix by restructuring (extract shared code to a third module).

---

### Q11. How do you use `enumerate` and `zip`?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`enumerate()` gives both index and value. `zip()` pairs items from multiple iterables. Both are lazy iterators.

```python
fruits = ["apple", "banana", "cherry"]

# enumerate — avoid range(len(lst))
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip — pair two lists
prices = [1.5, 2.0, 3.5]
for fruit, price in zip(fruits, prices):
    print(f"{fruit}: ₹{price}")
```

> **Interviewer tip:** Common fix in code review: `for i in range(len(lst)): print(i, lst[i])` → replace with enumerate.

---

### Q12. What is the `collections` module?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Provides specialized containers: `Counter`, `defaultdict`, `deque`, `namedtuple`, `OrderedDict`.

```python
from collections import Counter, defaultdict, deque

# Counter
words = ["hi", "hello", "hi", "world", "hi"]
print(Counter(words).most_common(2))

# defaultdict — no KeyError
graph = defaultdict(list)
graph["a"].append("b")

# deque — O(1) append/pop from both ends
q = deque([1, 2, 3])
q.appendleft(0)
q.append(4)
```

> **Interviewer tip:** Counter is great for frequency problems. defaultdict eliminates the 'if key not in dict' pattern.

---

### Q13. What are f-strings?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
f-strings (Python 3.6+) are the fastest and most readable way to format strings.

```python
name = "Raj"
score = 95.678

print(f"Hello, {name}! Score: {score:.2f}")
print(f"2 + 2 = {2 + 2}")
print(f"{name=}")           # name='Raj' (debug format, 3.8+)

# Formatting specs
value = 1234567
print(f"{value:,}")         # 1,234,567
print(f"{score:.1f}")       # 95.7
```

> **Interviewer tip:** f-strings support format specs: `{value:.2f}`, `{value:,}`, `{value:>10}` for alignment.

---

### Q14. What is exception handling best practice?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Catch specific exceptions, not bare `except`. Use `finally` for cleanup. Create custom exception classes for domain errors.

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
        return balance - amount
    except InsufficientFundsError:
        raise   # re-raise — don't swallow
    finally:
        print("Transaction attempt logged")
```

> **Interviewer tip:** Never: `except Exception: pass` — this hides bugs. Always log or re-raise in except blocks.

---

## Functions

### Q15. What are `*args` and `**kwargs`?
**Level:** Easy | **Frequency:** Very frequent

**Answer:**
`*args` collects extra positional arguments as a tuple. `**kwargs` collects extra keyword arguments as a dict.

```python
def greet(*args, **kwargs):
    for name in args:
        print(f"Hello, {name}")
    for key, val in kwargs.items():
        print(f"{key}: {val}")

greet("Raj", "Priya", role="Dev", city="Bengaluru")
```

> **Interviewer tip:** Ordering matters — regular args → *args → keyword-only args → **kwargs.

---

### Q16. What is the mutable default argument trap?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Default argument values are evaluated once when the function is defined, not on each call. Using a mutable default like `[]` causes all calls to share the same object.

```python
# BAD
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item(1))   # [1]
print(add_item(2))   # [1, 2]  ← Bug!

# GOOD — use None sentinel
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

> **Interviewer tip:** This is one of the most commonly asked Python gotcha questions. Know the None sentinel pattern by heart.

---

### Q17. Explain lambda, map, filter, and reduce.
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`lambda` creates anonymous functions. `map` applies a function to each item. `filter` keeps items where function returns True. `reduce` folds a sequence into a single value.

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

squared  = list(map(lambda x: x**2, nums))
evens    = list(filter(lambda x: x % 2 == 0, nums))
total    = reduce(lambda a, b: a + b, nums)

print(squared)  # [1, 4, 9, 16, 25]
print(evens)    # [2, 4]
print(total)    # 15
```

> **Interviewer tip:** Say: "In real projects I prefer list comprehensions for readability, but map/filter shine in functional pipelines."

---

### Q18. What is variable scope — local, global, nonlocal?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Local: inside the function. Global: module level. Nonlocal: from an enclosing function.

```python
x = 10  # global

def outer():
    y = 20  # enclosing
    def inner():
        nonlocal y
        global x
        x = 99   # modifies global x
        y = 88   # modifies enclosing y
    inner()
    print(y)   # 88

outer()
print(x)       # 99
```

> **Interviewer tip:** Test: "What happens if you read a global vs assign to it?" — assignment without `global` keyword makes it local.

---

## OOP

### Q19. What are classes, objects, and `__init__`?
**Level:** Easy | **Frequency:** Very frequent

**Answer:**
A class is a blueprint. An object is an instance. `__init__` is the constructor — runs when you create an object.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def __str__(self):
        return f"{self.owner}: ₹{self.balance}"

acc = BankAccount("Raj", 5000)
acc.deposit(1000)
print(acc)   # Raj: ₹6000
```

> **Interviewer tip:** Always define `__str__` and `__repr__` — shows depth. `__str__` for users, `__repr__` for debugging.

---

### Q20. Explain inheritance and method overriding.
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Inheritance lets a child class reuse and extend a parent class. `super()` calls the parent's version.

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):           # override
        return "Woof!"

class GuideDog(Dog):
    def speak(self):
        return super().speak() + " (trained)"

print(GuideDog().speak())  # Woof! (trained)
```

> **Interviewer tip:** Follow-up: MRO (Method Resolution Order) — Python uses C3 linearization. Use `ClassName.__mro__` to inspect.

---

### Q21. What is polymorphism in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Different classes can be used through the same interface. Python uses duck typing — if an object has the right methods, it works regardless of type.

```python
class Circle:
    def area(self): return 3.14 * 5 ** 2

class Rectangle:
    def area(self): return 4 * 6

shapes = [Circle(), Rectangle()]
for s in shapes:
    print(s.area())   # works for both!
```

> **Interviewer tip:** Say: "Python's duck typing makes polymorphism natural — I don't need interfaces like in Java."

---

### Q22. What is encapsulation in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Python uses naming conventions: `_single_underscore` (protected) and `__double_underscore` (name-mangled, harder to access externally).

```python
class User:
    def __init__(self, name, password):
        self.name = name
        self.__password = password   # private

    def check_password(self, pwd):
        return self.__password == pwd

u = User("Raj", "secret123")
print(u.check_password("secret123"))  # True
# print(u.__password)  # AttributeError
```

> **Interviewer tip:** Key point: Python doesn't truly enforce private — it's convention and name mangling, not hard access control.

---

### Q23. What are abstract base classes?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Abstract classes define a contract — they list methods subclasses must implement. You can't instantiate an abstract class directly.

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): pass

class UPI(Payment):
    def pay(self, amount):
        print(f"Paying ₹{amount} via UPI")

class Card(Payment):
    def pay(self, amount):
        print(f"Paying ₹{amount} via card")

# Payment()  # TypeError — can't instantiate
UPI().pay(500)
```

> **Interviewer tip:** Great for design questions — "I use ABCs to enforce contracts in payment systems, notification services, etc."

---

### Q24. What are dataclasses?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from class fields. Reduces boilerplate for data-holding classes.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    tags: list = field(default_factory=list)

u = User("Raj", "raj@example.com")
print(u)       # User(name='Raj', email='raj@example.com', tags=[])
print(u == User("Raj", "raj@example.com"))  # True
```

> **Interviewer tip:** Mention `frozen=True` for immutable dataclasses — useful for dict keys or thread-safe value objects.

---

### Q25. What is the difference between `__str__` and `__repr__`?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`__str__` is for end users — called by `print()`. `__repr__` is for developers — called in the REPL and should ideally return a string that recreates the object.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Point at ({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(str(p))    # Point at (3, 4)
print(repr(p))   # Point(x=3, y=4)
print([p])       # uses __repr__
```

> **Interviewer tip:** Rule: always implement `__repr__`. Implement `__str__` only when you want a user-friendly display.

---

### Q26. What is a property in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`@property` lets you define a method accessed like an attribute — enables getters, setters, and deleters with a clean API.

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

t = Temperature(25)
print(t.fahrenheit)   # 77.0
```

> **Interviewer tip:** Properties are better than public attributes for validation, and better than get/set methods for Pythonic API design.

---

### Q27. What is the difference between `staticmethod` and `classmethod`?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`@staticmethod`: no access to class or instance — just a namespaced function. `@classmethod`: receives `cls` — used for alternative constructors or class-level logic.

```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_string(cls, s):        # alternative constructor
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_valid(s):                # utility — no class needed
        return len(s.split("-")) == 3

d = Date.from_string("2024-03-15")
print(Date.is_valid("2024-03-15"))  # True
```

> **Interviewer tip:** `from_string`, `from_json`, `from_env` as class methods are common factory patterns in production code.

---

### Q28. What is `__slots__` and when do you use it?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`__slots__` replaces the instance `__dict__` with a fixed-size array, reducing memory usage per instance significantly.

```python
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x, self.y = x, y

import sys
p1 = Point(1, 2)
# No __dict__ means much lower memory per instance
# Useful when creating millions of instances
```

> **Interviewer tip:** Downside: can't add arbitrary attributes, and inheritance gets tricky. Use only when memory profiling shows a real problem.

---

## Advanced Python

### Q29. What are decorators and how do they work?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
A decorator is a function that wraps another function to add behavior. Uses `@syntax` as syntactic sugar for `func = decorator(func)`.

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_task():
    time.sleep(0.1)

slow_task()   # slow_task took 0.100xs
```

> **Interviewer tip:** Always use `@functools.wraps(func)` inside wrapper to preserve the original function's metadata.

---

### Q30. What is a decorator with arguments?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Needs three levels of nesting: outermost takes arguments, returns the actual decorator, which wraps the function.

```python
import functools

def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    print(f"Retry {attempt+1}...")
        return wrapper
    return decorator

@retry(times=3)
def call_api():
    pass
```

> **Interviewer tip:** Always use `@functools.wraps(func)` — preserves `__name__`, `__doc__`, helps with debugging.

---

### Q31. What are generators and when do you use them?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Generators use `yield` to produce values lazily — one at a time, on demand. Memory-efficient for large data.

```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()   # one line at a time

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
print([next(gen) for _ in range(8)])  # [0,1,1,2,3,5,8,13]
```

> **Interviewer tip:** Say: "I use generators for ETL pipelines and streaming large datasets where loading everything would OOM."

---

### Q32. What is the difference between an iterator and an iterable?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
An iterable has `__iter__` and can produce an iterator. An iterator has both `__iter__` and `__next__` and maintains state.

```python
lst = [1, 2, 3]          # iterable
it  = iter(lst)          # iterator

print(next(it))  # 1
print(next(it))  # 2
# A generator is both an iterable AND an iterator
gen = (x**2 for x in range(3))
print(next(gen))   # 0
```

> **Interviewer tip:** Key test: can you reset it? An iterable can be iterated again. An exhausted iterator cannot.

---

### Q33. What are closures in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
A closure is a nested function that captures and remembers variables from its enclosing scope even after that scope has finished.

```python
def make_multiplier(n):
    def multiply(x):
        return x * n     # 'n' is captured from outer scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

> **Interviewer tip:** Closures are the foundation of decorators. "Where does the decorator store the original function?" — in a closure.

---

### Q34. Explain context managers and the `with` statement.
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Context managers handle setup and teardown. They implement `__enter__` and `__exit__`. The `with` statement guarantees cleanup even on exception.

```python
# Class-based
class DBConnection:
    def __enter__(self):
        print("Connecting...")
        return self
    def __exit__(self, exc_type, exc_val, tb):
        print("Closing connection")
        return False

# contextlib approach (simpler)
from contextlib import contextmanager

@contextmanager
def db_conn():
    print("Connecting...")
    try:
        yield
    finally:
        print("Closing connection")

with db_conn():
    print("Doing work")
```

> **Interviewer tip:** Prefer `contextlib` for simple cases, class-based when you need more control like suppressing specific exceptions.

---

## Concurrency

### Q35. What is the GIL and how does it affect Python?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
The Global Interpreter Lock is a mutex in CPython that allows only one thread to execute Python bytecode at a time. It limits CPU parallelism in threads but doesn't affect I/O-bound tasks. Multiprocessing bypasses it.

```python
# Threads — good for I/O bound (file, network)
import threading
t = threading.Thread(target=fetch_url, args=(url,))

# Processes — good for CPU bound (computation)
import multiprocessing
p = multiprocessing.Process(target=crunch_numbers)

# GIL doesn't affect:
# - C extensions (NumPy releases the GIL)
# - I/O operations (file read, network)
```

> **Interviewer tip:** "The GIL protects CPython's memory management. NumPy and IO both work around it — that's why data science and web servers still perform well."

---

### Q36. Threading vs Multiprocessing vs Async — when to use each?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
- **Threading:** I/O-bound tasks, shared memory, GIL limits CPU
- **Multiprocessing:** CPU-bound tasks, true parallelism, separate memory
- **Async:** many concurrent I/O tasks with a single thread — most efficient for network-heavy apps

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)   # non-blocking
    return f"data from {url}"

async def main():
    results = await asyncio.gather(
        fetch("url1"), fetch("url2"), fetch("url3")
    )
    print(results)

asyncio.run(main())
```

> **Interviewer tip:** Decision rule: I/O-bound + few tasks = threads, I/O-bound + many tasks = async, CPU-bound = multiprocessing.

---

### Q37. What is async/await and how does the event loop work?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
`async def` defines a coroutine. `await` suspends it and returns control to the event loop, which runs other coroutines while waiting.

```python
import asyncio
import aiohttp

async def fetch_user(session, user_id):
    async with session.get(f"/users/{user_id}") as r:
        return await r.json()

async def main():
    async with aiohttp.ClientSession() as session:
        users = await asyncio.gather(
            fetch_user(session, 1),
            fetch_user(session, 2),
            fetch_user(session, 3),
        )
    return users
```

> **Interviewer tip:** Common mistake: calling blocking code (`time.sleep`, `requests.get`) inside async — it blocks the entire event loop. Use `asyncio.sleep` and `aiohttp` instead.

---

### Q38. What is blocking the event loop and how do you avoid it?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Blocking the event loop means running synchronous code inside async that doesn't yield control. Use `asyncio.to_thread()` to run blocking code in a thread pool.

```python
import asyncio
import time

# BAD — blocks event loop
async def bad():
    time.sleep(2)   # freezes everything!

# GOOD — runs in thread pool, doesn't block
async def good():
    await asyncio.to_thread(time.sleep, 2)

# GOOD — use async-native libraries
async def fetch():
    await asyncio.sleep(2)   # non-blocking
```

> **Interviewer tip:** `asyncio.run_in_executor()` is the older equivalent of `asyncio.to_thread()`.

---

## FastAPI

### Q39. What is FastAPI and how does it compare to Flask?
**Level:** Easy | **Frequency:** Very frequent

**Answer:**
FastAPI is a modern async web framework with automatic OpenAPI docs, Pydantic validation, and async support built in. Flask is simpler but synchronous by default.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
async def create_user(user: User):
    return {"message": f"Created {user.name}"}

# Auto-generated docs at /docs and /redoc
```

> **Interviewer tip:** Key differentiators: type hints drive validation and docs automatically. FastAPI is 2-3x faster than Flask for I/O-bound workloads.

---

### Q40. How does Pydantic validation work in FastAPI?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Pydantic models define the shape and types of request/response data. FastAPI uses them to validate incoming JSON, serialize responses, and generate OpenAPI schema.

```python
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    role: Optional[str] = "user"

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Age must be positive")
        return v

    model_config = {"str_strip_whitespace": True}
```

> **Interviewer tip:** Pydantic v2 uses `@field_validator` instead of `@validator`. Always use separate request and response schemas.

---

### Q41. How do you handle exceptions in FastAPI?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Use `HTTPException` for expected errors. Use custom exception handlers for app-wide error handling. Always return consistent error response schemas.

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UserNotFoundError(Exception):
    pass

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(req: Request, exc):
    return JSONResponse(status_code=404,
        content={"error": "User not found"})

@app.get("/users/{id}")
async def get_user(id: int):
    user = db.get(id)
    if not user:
        raise UserNotFoundError()
    return user
```

> **Interviewer tip:** Best practice: never expose raw exception messages to clients — wrap them in a consistent error schema.

---

### Q42. What is middleware in FastAPI?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Middleware runs on every request/response cycle. Used for logging, auth, CORS, request timing, rate limiting.

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

> **Interviewer tip:** Order matters: middleware added last runs first. Use Starlette's `BaseHTTPMiddleware` for class-based middleware.

---

### Q43. How do you write a FastAPI CRUD API with a database?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
Use SQLAlchemy for ORM, dependency injection for DB sessions. Separate models, schemas, and CRUD operations into different files.

```python
# database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://...")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# routes.py
@app.post("/users", response_model=UserOut)
async def create_user(user: UserCreate,
                      db: AsyncSession = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    return db_user
```

> **Interviewer tip:** Structure: `routers/ models/ schemas/ crud/` — shows you know real project layout.

---

### Q44. How do you write tests with pytest?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Use fixtures for setup/teardown, parametrize for multiple inputs, and mock for faking dependencies.

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_user():
    return {"name": "Raj", "email": "raj@test.com", "age": 25}

def test_create_user(sample_user):
    response = client.post("/users", json=sample_user)
    assert response.status_code == 201
    assert response.json()["name"] == "Raj"

@pytest.mark.parametrize("age", [-1, 0, 999])
def test_invalid_age(sample_user, age):
    sample_user["age"] = age
    r = client.post("/users", json=sample_user)
    assert r.status_code == 422
```

> **Interviewer tip:** Test pyramid — unit > integration > e2e. Mock external calls with `unittest.mock.patch`.

---

### Q45. What is Docker and how do you containerize a FastAPI app?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Docker packages your app and dependencies into a portable container. A Dockerfile defines the image. docker-compose runs multi-container apps.

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["8000:8000"]
    depends_on: [db, redis]
  db:
    image: postgres:16
  redis:
    image: redis:7
```

> **Interviewer tip:** Use multi-stage builds in production to keep image size small. Use `.dockerignore` to exclude `__pycache__`, `.env`, `.git`.

---

### Q46. What is dependency injection in FastAPI?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
FastAPI's `Depends()` system automatically resolves dependencies. Used for DB sessions, auth, config, and shared logic.

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme),
                           db = Depends(get_db)):
    user = await db.get_user_by_token(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    return user

@app.get("/me")
async def get_me(user = Depends(get_current_user)):
    return user
```

> **Interviewer tip:** Testing is easy — override deps: `app.dependency_overrides[get_db] = mock_db`.

---

### Q47. How do you handle environment variables and config in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Use `pydantic-settings` (BaseSettings) to parse and validate config with type safety. Never hardcode secrets.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    max_connections: int = 10

    model_config = {"env_file": ".env"}

settings = Settings()
print(settings.database_url)   # loaded from .env
```

> **Interviewer tip:** Use `@lru_cache` on the settings factory so config is loaded once: `@lru_cache def get_settings(): return Settings()`

---

## Database

### Q48. Explain SQL JOINs with examples.
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
- **INNER JOIN:** only matching rows from both tables
- **LEFT JOIN:** all from left + matching from right (NULL if no match)
- **FULL OUTER JOIN:** all rows from both

```sql
-- INNER JOIN — only users who have orders
SELECT u.name, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN — all users, even without orders
SELECT u.name, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Find users with NO orders
SELECT u.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

> **Interviewer tip:** "Write a query to find users with NO orders" — LEFT JOIN WHERE `orders.id IS NULL`.

---

### Q49. What is database indexing and when should you use it?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
An index is a data structure (usually B-tree) that speeds up reads at the cost of slower writes. Index columns used in WHERE, JOIN ON, and ORDER BY.

```sql
-- Create an index
CREATE INDEX idx_users_email ON users(email);

-- Composite index — order matters!
CREATE INDEX idx_orders_user_date
ON orders(user_id, created_at);

-- Check if index is being used
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'raj@x.com';
```

> **Interviewer tip:** Too many indexes slow down writes. Avoid indexing columns with low cardinality (e.g., boolean columns).

---

### Q50. What is the N+1 query problem and how do you fix it?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
N+1 happens when you fetch N records then make one extra DB query per record in a loop — totalling N+1 round trips instead of 2.

```python
# BAD — lazy loading triggers N queries
users = (await db.execute(select(User))).scalars().all()
for user in users:
    print(user.orders)   # each access fires a new SELECT!

# FIX 1 — selectinload (2 queries total)
from sqlalchemy.orm import selectinload
users = (await db.execute(
    select(User).options(selectinload(User.orders))
)).scalars().all()

# FIX 2 — joinedload (1 query with JOIN)
from sqlalchemy.orm import joinedload
users = (await db.execute(
    select(User).options(joinedload(User.orders))
)).unique().scalars().all()

# FIX 3 — raw SQL JOIN for complex queries
result = await db.execute(text("""
    SELECT u.*, COUNT(o.id) AS order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
"""))
```

> **Interviewer tip:** Quantify it — "Fixing an N+1 dropped our endpoint from 800ms to 45ms by cutting 99 round trips." Enable SQL logging in dev to catch N+1 early: `logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)`

---

## Final Interview Tips

1. **Quantify everything** — "800ms → 45ms", "101 queries → 2 queries"
2. **Use real examples** — payment systems, user services, APIs you built
3. **Know the why** — don't just say what, say why you chose it
4. **Mention trade-offs** — every solution has downsides, knowing them shows seniority
5. **Practice out loud** — explaining code verbally is a different skill from writing it

---

*Items marked ← NEW were added based on common interview gaps: abstract classes, dataclasses, asyncio.gather, pytest, Docker, Redis, async SQLAlchemy.*











