# Python Interview Questions — Part 2 (Q51–Q100)
> 50 more advanced questions with full answers, code examples and interviewer tips

---

## Core Python — Advanced

### Q51. What is the difference between `deepcopy` and assignment (`=`)?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
Assignment (`=`) just creates another reference to the same object. `deepcopy` creates a completely independent object with all nested objects also copied.

```python
import copy

a = [[1, 2], [3, 4]]

b = a               # same object — both point to same list
c = copy.deepcopy(a)  # fully independent clone

a[0][0] = 99

print(b[0][0])   # 99 — b is affected (same reference)
print(c[0][0])   # 1  — c is independent
print(a is b)    # True  — same object
print(a is c)    # False — different objects
```

> **Interviewer tip:** This trips up juniors constantly. Say: "Assignment is O(1), deepcopy is O(n) — only use deepcopy when you truly need independence."

---

### Q52. What are Python's dunder (magic) methods?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Dunder methods (double underscore) are special methods Python calls automatically for built-in operations. They let you define how your objects behave with operators, built-in functions, and statements.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):         # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):        # v * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __len__(self):                # len(v)
        return 2

    def __getitem__(self, idx):       # v[0]
        return (self.x, self.y)[idx]

    def __contains__(self, val):      # 3 in v
        return val in (self.x, self.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)    # Vector(4, 6)
print(v1 * 3)     # Vector(3, 6)
print(len(v1))    # 2
print(v1[0])      # 1
```

> **Interviewer tip:** Know at minimum: `__init__`, `__str__`, `__repr__`, `__len__`, `__getitem__`, `__eq__`, `__hash__`, `__enter__`, `__exit__`, `__iter__`, `__next__`.

---

### Q53. What is `__hash__` and when do you implement it?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`__hash__` returns an integer used when the object is used as a dict key or set member. If you define `__eq__`, Python sets `__hash__` to None (making the object unhashable) — you must explicitly define both.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))   # hash a tuple of fields

p1 = Point(1, 2)
p2 = Point(1, 2)

print(p1 == p2)       # True
print(p1 is p2)       # False

# Now usable as dict key and set member
seen = {p1}
print(p2 in seen)     # True  — because __hash__ + __eq__ match
```

> **Interviewer tip:** Rule: objects that compare equal must have the same hash. Use `hash(tuple_of_fields)` — never hash mutable state.

---

### Q54. How does Python handle multiple inheritance and what is MRO?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Python uses C3 linearization (MRO — Method Resolution Order) to determine which parent's method to call when multiple inheritance is used. Use `ClassName.__mro__` to inspect it.

```python
class A:
    def greet(self): return "A"

class B(A):
    def greet(self): return "B"

class C(A):
    def greet(self): return "C"

class D(B, C):   # inherits from B and C
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

print(D().greet())   # "B" — B comes before C in MRO

# super() follows MRO — not just "the parent class"
class B2(A):
    def greet(self):
        return "B2 + " + super().greet()  # calls C2.greet next!
```

> **Interviewer tip:** "Diamond problem" — D inherits from B and C which both inherit from A. MRO ensures A's method is called only once.

---

### Q55. What is monkey patching in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Monkey patching is dynamically modifying a class or module at runtime — replacing or adding methods/attributes without changing the original source code. Common in testing.

```python
import datetime

# Monkey patch datetime.now for testing
class FakeDatetime:
    @staticmethod
    def now():
        return datetime.datetime(2024, 1, 1, 12, 0, 0)

# In a test
datetime.datetime = FakeDatetime
print(datetime.datetime.now())   # always returns 2024-01-01 12:00:00

# Better approach in pytest — use monkeypatch fixture
def test_something(monkeypatch):
    monkeypatch.setattr(datetime, "datetime", FakeDatetime)
    # test logic here
```

> **Interviewer tip:** Use carefully in production — it makes code harder to reason about. In tests, prefer `unittest.mock.patch` or pytest's `monkeypatch` fixture.

---

### Q56. What are metaclasses in Python?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
A metaclass is the class of a class — it defines how classes themselves behave. `type` is the default metaclass. You use metaclasses to customize class creation — add methods, enforce structure, register subclasses automatically.

```python
# type is the metaclass of every class
print(type(int))    # <class 'type'>
print(type(list))   # <class 'type'>

# Custom metaclass — auto-registers subclasses
class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:   # skip the base class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class CSVPlugin(Plugin): pass
class JSONPlugin(Plugin): pass

print(PluginMeta.registry)
# {'CSVPlugin': <class 'CSVPlugin'>, 'JSONPlugin': <class 'JSONPlugin'>}
```

> **Interviewer tip:** Most real-world use cases for metaclasses are now better handled by `__init_subclass__` or class decorators — mention this if asked.

---

### Q57. What is `__init_subclass__` and when is it better than metaclasses?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`__init_subclass__` is called whenever the class is subclassed — a simpler alternative to metaclasses for most class customization needs.

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
# {'csv': <class 'CSVPlugin'>, 'json': <class 'JSONPlugin'>}
```

> **Interviewer tip:** Prefer `__init_subclass__` over metaclasses — simpler, more readable, and works with existing metaclasses without conflicts.

---

### Q58. What is the `functools` module and what are its most useful tools?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`functools` provides higher-order functions and tools for working with functions. Key tools: `lru_cache`, `wraps`, `partial`, `reduce`, `cached_property`.

```python
from functools import lru_cache, partial, cached_property

# lru_cache — memoization
@lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

print(fib(50))   # instant — cached results

# partial — fix some arguments
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)
print(square(5))   # 25
print(cube(3))     # 27

# cached_property — compute once, cache on instance
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def area(self):
        print("computing...")
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)   # computes
print(c.area)   # returns cached value
```

> **Interviewer tip:** `lru_cache` is one of the easiest performance wins in Python — use it for any pure function called repeatedly with the same arguments.

---

### Q59. What is the `itertools` module?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`itertools` provides memory-efficient tools for working with iterators. Key functions: `chain`, `product`, `combinations`, `permutations`, `groupby`, `islice`, `cycle`.

```python
import itertools

# chain — combine multiple iterables
for x in itertools.chain([1,2], [3,4], [5,6]):
    print(x)   # 1 2 3 4 5 6

# product — cartesian product (like nested loops)
for combo in itertools.product("AB", [1, 2]):
    print(combo)   # ('A',1) ('A',2) ('B',1) ('B',2)

# combinations and permutations
print(list(itertools.combinations([1,2,3], 2)))
# [(1,2), (1,3), (2,3)]

# groupby — group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))

# islice — slice any iterator (including infinite ones)
gen = itertools.count(1)   # infinite counter
print(list(itertools.islice(gen, 5)))   # [1, 2, 3, 4, 5]
```

> **Interviewer tip:** `groupby` requires the data to be sorted by the key first — a common gotcha.

---

### Q60. What is the difference between `any()` and `all()`?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`any()` returns True if at least one element is truthy. `all()` returns True if every element is truthy. Both short-circuit — they stop as soon as the result is determined.

```python
scores = [85, 92, 78, 95, 60]

# any — did anyone score above 90?
print(any(s > 90 for s in scores))   # True

# all — did everyone pass (score >= 60)?
print(all(s >= 60 for s in scores))  # True

# all on empty iterable returns True (vacuous truth)
print(all(x > 0 for x in []))        # True ← gotcha!

# any on empty iterable returns False
print(any(x > 0 for x in []))        # False

# Short-circuit — generator stops at first match
def check(x):
    print(f"checking {x}")
    return x > 3

print(any(check(x) for x in [1, 2, 5, 6]))
# checking 1, checking 2, checking 5 — stops here!
```

> **Interviewer tip:** Always pass a generator expression to `any()`/`all()` — not a list — to benefit from short-circuiting.

---

### Q61. What is `walrus operator` (`:=`)?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
The walrus operator (`:=`) assigns a value to a variable as part of an expression — introduced in Python 3.8. Avoids computing a value twice.

```python
import re

# Without walrus — compute twice
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if len(data) > 5:
    print(f"Long list: {len(data)} items")   # len() called twice

# With walrus — compute once
if (n := len(data)) > 5:
    print(f"Long list: {n} items")

# Great in while loops
import random
while (val := random.randint(1, 10)) != 7:
    print(f"Got {val}, trying again...")
print("Got 7!")

# Useful with regex
text = "Order ID: 12345"
if m := re.search(r"\d+", text):
    print(f"Found number: {m.group()}")   # no need to check m again
```

> **Interviewer tip:** Don't overuse it — only use walrus when it genuinely avoids a repeated computation or makes the code cleaner.

---

### Q62. What are Python's built-in sorting options?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`sorted()` returns a new list. `list.sort()` sorts in place. Both use Timsort (O(n log n)). Use `key` parameter for custom sorting, `reverse=True` for descending.

```python
users = [
    {"name": "Priya", "age": 28},
    {"name": "Raj",   "age": 25},
    {"name": "Anita", "age": 31},
]

# Sort by age
by_age = sorted(users, key=lambda u: u["age"])

# Sort by name descending
by_name_desc = sorted(users, key=lambda u: u["name"], reverse=True)

# Multi-key sort — primary: age, secondary: name
from operator import itemgetter
multi = sorted(users, key=itemgetter("age", "name"))

# Sort strings case-insensitively
words = ["Banana", "apple", "Cherry"]
print(sorted(words, key=str.lower))  # ['apple', 'Banana', 'Cherry']

# Timsort is stable — equal elements keep original order
```

> **Interviewer tip:** Timsort is stable — this matters when sorting by multiple criteria in steps. Use `operator.itemgetter` or `attrgetter` instead of lambda for small speed gains.

---

### Q63. What is `sys.argv` and how do you parse CLI arguments?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`sys.argv` is a list of command-line arguments. For real CLI tools use `argparse` (stdlib) or `click` (third-party).

```python
# sys.argv — raw
import sys
print(sys.argv)   # ['script.py', 'arg1', 'arg2']

# argparse — proper CLI
import argparse

parser = argparse.ArgumentParser(description="Process data")
parser.add_argument("--input",  required=True, help="Input file path")
parser.add_argument("--output", default="out.csv", help="Output file")
parser.add_argument("--verbose", action="store_true")

args = parser.parse_args()
print(args.input, args.output, args.verbose)

# Run: python script.py --input data.csv --verbose
```

> **Interviewer tip:** For complex CLIs with subcommands, use `click` — it's cleaner. For simple scripts, `argparse` is fine since it's in stdlib.

---

### Q64. What is the GIL workaround using `concurrent.futures`?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`concurrent.futures` provides a high-level interface for both threading and multiprocessing. `ThreadPoolExecutor` for I/O-bound, `ProcessPoolExecutor` for CPU-bound tasks.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests

urls = ["https://api.example.com/1", "https://api.example.com/2"]

# I/O bound — ThreadPoolExecutor
def fetch(url):
    return requests.get(url).json()

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch, urls))

# CPU bound — ProcessPoolExecutor (bypasses GIL)
def crunch(n):
    return sum(i*i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(crunch, 10_000_000) for _ in range(4)]
    results = [f.result() for f in futures]
```

> **Interviewer tip:** `executor.map()` preserves order. `executor.submit()` gives you `Future` objects for more control — use `.result()` to get the value, `.exception()` to check for errors.

---

## OOP — Advanced

### Q65. What is the difference between composition and inheritance?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Inheritance models "is-a" relationships. Composition models "has-a" relationships. Composition is often preferred — it's more flexible, avoids deep inheritance hierarchies, and makes testing easier.

```python
# Inheritance — "is-a" (Dog IS AN Animal)
class Animal:
    def breathe(self): print("breathing")

class Dog(Animal):
    def bark(self): print("woof")

# Composition — "has-a" (Car HAS AN Engine)
class Engine:
    def start(self): print("vroom")
    def stop(self):  print("silence")

class Car:
    def __init__(self):
        self.engine = Engine()   # composed, not inherited

    def drive(self):
        self.engine.start()
        print("driving...")

# Composition advantage: swap Engine easily
class ElectricEngine:
    def start(self): print("whoosh")
    def stop(self):  print("silence")

car = Car()
car.engine = ElectricEngine()   # swap without changing Car class
```

> **Interviewer tip:** "Favour composition over inheritance" — Gang of Four. Say: "I use inheritance for true is-a relationships like Exception subclasses, and composition for everything else."

---

### Q66. What is the Singleton pattern in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Singleton ensures a class has only one instance. In Python, implemented via metaclass, `__new__`, or module-level variable (simplest).

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
print(s1 is s2)   # True

# Method 2 — module level (Pythonic — modules are singletons)
# config.py
class _Config:
    debug = False
    db_url = "postgresql://..."

config = _Config()   # import this instance, not the class

# Method 3 — using decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
```

> **Interviewer tip:** In Python, module-level objects are the most Pythonic singleton — Python caches module imports, so the object is created once.

---

### Q67. What is the Factory pattern in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Factory pattern creates objects without specifying the exact class. Use when the type of object to create depends on a condition or configuration.

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str): pass

class EmailNotification(Notification):
    def send(self, message):
        print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS: {message}")

class PushNotification(Notification):
    def send(self, message):
        print(f"Push: {message}")

# Factory — returns the right class based on type
class NotificationFactory:
    _types = {
        "email": EmailNotification,
        "sms":   SMSNotification,
        "push":  PushNotification,
    }

    @classmethod
    def create(cls, ntype: str) -> Notification:
        if ntype not in cls._types:
            raise ValueError(f"Unknown type: {ntype}")
        return cls._types[ntype]()

notif = NotificationFactory.create("email")
notif.send("Your order shipped!")
```

> **Interviewer tip:** Using a dict map instead of if-elif chains is more Pythonic and extensible — adding new types doesn't require touching the factory logic.

---

### Q68. What is the Observer pattern in Python?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Observer pattern lets objects subscribe to events and be notified automatically when something changes. Core of event-driven systems.

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
        print(f"Order placed: {order}")
        self.emit("order_placed", order)

service = OrderService()
service.on("order_placed", lambda o: print(f"Send email for {o}"))
service.on("order_placed", lambda o: print(f"Update inventory for {o}"))
service.on("order_placed", lambda o: print(f"Notify warehouse for {o}"))

service.place_order({"id": 42, "item": "Laptop"})
```

> **Interviewer tip:** Python's `signal` library and FastAPI's event system (`@app.on_event`) are real-world implementations of this pattern.

---

## Advanced Python — Deeper

### Q69. What is `__call__` and callable objects?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`__call__` makes an instance callable like a function. Useful for creating stateful functions, decorators as classes, and function-like objects.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))    # 10
print(triple(5))    # 15
print(callable(double))  # True

# Useful as class-based decorator
class CountCalls:
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

greet("Raj")   # Call #1, Hello, Raj!
greet("Priya") # Call #2, Hello, Priya!
print(greet.count)  # 2
```

> **Interviewer tip:** Class-based decorators using `__call__` are more powerful than function-based ones — they can hold state across calls.

---

### Q70. What are descriptors in Python?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
A descriptor is an object that defines `__get__`, `__set__`, or `__delete__` — it controls attribute access on another class. `property`, `classmethod`, `staticmethod` are all descriptors.

```python
class Validator:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{self.name} must be a non-negative int")
        obj.__dict__[self.name] = value

class Product:
    price    = Validator()
    quantity = Validator()

    def __init__(self, price, quantity):
        self.price    = price
        self.quantity = quantity

p = Product(100, 5)
print(p.price)       # 100
# p.price = -10      # ValueError!
```

> **Interviewer tip:** Descriptors are how `@property` works under the hood. Say: "I'd use a descriptor when the same validation logic needs to apply to multiple attributes across multiple classes."

---

### Q71. What is `__getattr__` vs `__getattribute__`?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`__getattr__` is called only when normal attribute lookup fails. `__getattribute__` is called for every attribute access — override with extreme care to avoid infinite recursion.

```python
class DynamicConfig:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        # Only called when attribute not found normally
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No config key: {name}")

cfg = DynamicConfig({"debug": True, "db_url": "postgresql://..."})
print(cfg.debug)    # True  — via __getattr__
print(cfg.db_url)   # postgresql://...
# print(cfg.missing) # AttributeError

# __getattribute__ — called for EVERY access
class Logged:
    def __getattribute__(self, name):
        print(f"Accessing: {name}")
        return super().__getattribute__(name)   # must call super!
```

> **Interviewer tip:** Never override `__getattribute__` unless you have a very specific reason — it's called for every access including internal ones and is easy to break.

---

### Q72. How do you implement a custom iterator class?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
A custom iterator implements `__iter__` (returns self) and `__next__` (returns next value or raises StopIteration).

```python
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self     # iterator returns itself

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for n in CountDown(5):
    print(n)   # 5 4 3 2 1

# Range-like class — iterable (not iterator)
class Range:
    def __init__(self, start, stop):
        self.start, self.stop = start, stop

    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current     # generator makes this simple
            current += 1

for x in Range(1, 6):
    print(x)   # 1 2 3 4 5
```

> **Interviewer tip:** The key distinction — an iterable creates a new iterator each time (can loop multiple times), an iterator is consumed (can only loop once).

---

### Q73. What is `namedtuple` and when do you use it?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
`namedtuple` creates tuple subclasses with named fields — lightweight immutable data structures. More readable than plain tuples, less overhead than full classes.

```python
from collections import namedtuple
from typing import NamedTuple

# Old style
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)    # 3 4
print(p[0], p[1])  # 3 4 — still a tuple
print(p._asdict()) # {'x': 3, 'y': 4}

# New style with types (preferred)
class Coordinate(NamedTuple):
    latitude:  float
    longitude: float
    altitude:  float = 0.0

loc = Coordinate(12.9716, 77.5946)
print(loc.latitude)    # 12.9716
print(loc)             # Coordinate(latitude=12.9716, ...)

# Use case: returning multiple values cleanly
def get_user_stats(uid):
    return Coordinate(12.9716, 77.5946, 900.0)
```

> **Interviewer tip:** Use `NamedTuple` (typed) over `namedtuple` — better IDE support, type checking, and cleaner syntax. Use `@dataclass` when you need mutability.

---

### Q74. What is `typing.Protocol` and structural subtyping?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`Protocol` defines structural subtyping (duck typing with type checking). A class satisfies a Protocol if it has the required methods — no explicit inheritance needed.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...
    def area(self) -> float: ...

class Circle:
    def draw(self):  print("Drawing circle")
    def area(self):  return 3.14 * 5 ** 2

class Square:
    def draw(self):  print("Drawing square")
    def area(self):  return 4 * 4

# No explicit inheritance — structural match is enough
def render(shape: Drawable):
    shape.draw()
    print(f"Area: {shape.area()}")

render(Circle())   # works!
render(Square())   # works!

# isinstance check works with @runtime_checkable
print(isinstance(Circle(), Drawable))  # True
```

> **Interviewer tip:** `Protocol` is better than ABCs for defining interfaces between loosely coupled code — the implementer doesn't need to know about your interface at all.

---

## FastAPI — Advanced

### Q75. How do you implement JWT authentication in FastAPI?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
Use `python-jose` for JWT creation/validation and FastAPI's dependency injection for protecting routes.

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your-secret-key"
ALGORITHM  = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"user": user}
```

> **Interviewer tip:** Always store only non-sensitive data in JWT (user_id, roles). Never store passwords. Use short expiry (15 min) + refresh tokens for production.

---

### Q76. How do you implement rate limiting in FastAPI?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Use Redis with a sliding window counter, or `slowapi` library (Limits-based). Rate limiting belongs in middleware or as a dependency.

```python
import redis
import time
from fastapi import HTTPException, Request

r = redis.Redis(host="localhost", port=6379)

def rate_limit(max_requests: int = 10, window: int = 60):
    async def check(request: Request):
        client_ip = request.client.host
        key = f"rate:{client_ip}"

        pipe = r.pipeline()
        now  = time.time()
        pipe.zremrangebyscore(key, 0, now - window)  # remove old
        pipe.zadd(key, {str(now): now})              # add current
        pipe.zcard(key)                              # count
        pipe.expire(key, window)
        _, _, count, _ = pipe.execute()

        if count > max_requests:
            raise HTTPException(429, "Too many requests")
    return check

@app.get("/api/data", dependencies=[Depends(rate_limit(10, 60))])
async def get_data():
    return {"data": "..."}
```

> **Interviewer tip:** Sliding window is more accurate than fixed window (no burst at boundary). For distributed systems, Redis is the standard backend for rate limiting.

---

### Q77. How do you implement background tasks in FastAPI?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
FastAPI has built-in `BackgroundTasks` for simple post-response tasks. For heavy jobs use Celery + Redis/RabbitMQ.

```python
from fastapi import BackgroundTasks
import asyncio

async def send_welcome_email(email: str):
    await asyncio.sleep(2)   # simulate slow email
    print(f"Email sent to {email}")

async def update_analytics(user_id: int):
    print(f"Analytics updated for {user_id}")

@app.post("/register")
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks
):
    # Save user to DB
    new_user = await create_user_in_db(user)

    # These run AFTER the response is sent
    background_tasks.add_task(send_welcome_email, user.email)
    background_tasks.add_task(update_analytics, new_user.id)

    return {"id": new_user.id, "status": "registered"}

# For heavy tasks — use Celery
# @celery.task
# def send_email_celery(email):
#     ...
```

> **Interviewer tip:** `BackgroundTasks` runs in the same process — if the server restarts, tasks are lost. For reliability, use Celery with a message broker.

---

### Q78. How do you handle file uploads in FastAPI?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Use `UploadFile` for file uploads. Validate file type and size. For large files, stream to avoid loading into memory.

```python
from fastapi import UploadFile, File, HTTPException
import aiofiles
import os

MAX_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED  = {"image/jpeg", "image/png", "application/pdf"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate content type
    if file.content_type not in ALLOWED:
        raise HTTPException(400, f"File type not allowed: {file.content_type}")

    # Read and validate size
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(400, "File too large (max 5MB)")

    # Save to disk asynchronously
    save_path = f"uploads/{file.filename}"
    async with aiofiles.open(save_path, "wb") as f:
        await f.write(contents)

    return {"filename": file.filename, "size": len(contents)}

# Multiple files
@app.post("/upload-many")
async def upload_many(files: list[UploadFile] = File(...)):
    return [{"name": f.filename} for f in files]
```

> **Interviewer tip:** In production, stream files directly to S3/GCS using `aiobotocore` — don't save to local disk.

---

### Q79. What is CORS and how do you configure it in FastAPI?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
CORS (Cross-Origin Resource Sharing) controls which domains can call your API from a browser. Configure with `CORSMiddleware`.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myapp.com",
        "https://staging.myapp.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Development only — allow all origins
# allow_origins=["*"]  ← NEVER use in production with credentials!
```

> **Interviewer tip:** `allow_origins=["*"]` with `allow_credentials=True` is a security error — browsers will reject it. Always be explicit with origins in production.

---

### Q80. How do you version a FastAPI API?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Use URL path versioning (`/v1/`, `/v2/`) or header versioning. Mount separate routers per version. Keep old versions alive until clients migrate.

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# V1 router
v1 = APIRouter(prefix="/v1")

@v1.get("/users")
async def get_users_v1():
    return [{"id": 1, "name": "Raj"}]

# V2 router — extended response
v2 = APIRouter(prefix="/v2")

@v2.get("/users")
async def get_users_v2():
    return [{"id": 1, "name": "Raj", "role": "admin", "created_at": "2024-01-01"}]

app.include_router(v1)
app.include_router(v2)

# /v1/users  and  /v2/users  both work
```

> **Interviewer tip:** URL versioning is most explicit and easiest to test. Header versioning (`Accept: application/vnd.api+json;version=2`) is cleaner but harder to debug.

---

## Database — Advanced

### Q81. What is database connection pooling?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
Connection pooling maintains a cache of open DB connections and reuses them — avoids the overhead of creating a new connection per request. SQLAlchemy manages this automatically.

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=10,          # number of connections to keep open
    max_overflow=20,       # extra connections allowed under load
    pool_timeout=30,       # seconds to wait for a connection
    pool_recycle=1800,     # recycle connections every 30 min
    pool_pre_ping=True,    # test connection before use (handles dropped connections)
)

# Each request gets a connection from the pool
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        # connection returns to pool here automatically
```

> **Interviewer tip:** `pool_pre_ping=True` is important for long-running services — database servers drop idle connections, and this detects and replaces them automatically.

---

### Q82. What is database migration and how does Alembic work?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Migrations track schema changes (adding columns, tables) in version-controlled files. Alembic is the standard migration tool for SQLAlchemy.

```python
# alembic.ini — configure database URL

# env.py — point to your models
from myapp.models import Base
target_metadata = Base.metadata

# Generate a migration after model change
# alembic revision --autogenerate -m "add user role column"

# Generated migration file
def upgrade():
    op.add_column("users",
        sa.Column("role", sa.String(50), nullable=False, server_default="user")
    )

def downgrade():
    op.drop_column("users", "role")

# Apply migrations
# alembic upgrade head

# Rollback one step
# alembic downgrade -1
```

> **Interviewer tip:** Always review autogenerated migrations — Alembic misses some changes like column renames and constraint updates. Add `server_default` when adding non-nullable columns to existing tables.

---

### Q83. What is the difference between `INNER JOIN`, `LEFT JOIN`, and `CROSS JOIN`?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
INNER JOIN: only matching rows. LEFT JOIN: all left rows + matching right (NULL for no match). CROSS JOIN: cartesian product — every row from left combined with every row from right.

```sql
-- Setup
-- users: (1, Raj), (2, Priya), (3, Anita)
-- orders: (1, user_id=1), (2, user_id=1), (3, user_id=2)

-- INNER JOIN — only users with orders
SELECT u.name, o.id FROM users u
INNER JOIN orders o ON u.id = o.user_id;
-- Raj, Raj, Priya (Anita excluded)

-- LEFT JOIN — all users including those without orders
SELECT u.name, o.id FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- Raj, Raj, Priya, Anita (NULL for Anita's order)

-- CROSS JOIN — every combination (dangerous on large tables!)
SELECT u.name, p.name FROM users u
CROSS JOIN products p;
-- 3 users × N products = 3N rows
```

> **Interviewer tip:** Accidental CROSS JOIN (forgetting the ON clause) is a common bug that generates millions of rows and kills DB performance.

---

### Q84. What is a database transaction isolation level?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Isolation levels control how concurrent transactions see each other's uncommitted data. Trade-off between consistency and performance.

```sql
-- READ UNCOMMITTED: sees uncommitted data from other transactions (dirty reads)
-- READ COMMITTED:   only sees committed data (default in most DBs)
-- REPEATABLE READ:  same query returns same results within transaction
-- SERIALIZABLE:     highest isolation — transactions appear sequential

-- Set in SQLAlchemy
from sqlalchemy import text

async with db.begin():
    await db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
    # your operations here

-- Common problem: phantom reads
-- Transaction 1: SELECT COUNT(*) FROM orders WHERE user_id = 1 → 5
-- Transaction 2: INSERT INTO orders (user_id) VALUES (1) → commits
-- Transaction 1: SELECT COUNT(*) FROM orders WHERE user_id = 1 → 6 ← phantom!
-- SERIALIZABLE prevents this
```

> **Interviewer tip:** Most apps work fine with READ COMMITTED (PostgreSQL default). Use SERIALIZABLE only for financial transactions where phantom reads would cause money errors.

---

### Q85. How do you prevent SQL injection in Python?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Always use parameterized queries — never string-format user input into SQL. SQLAlchemy's ORM and `text()` with bound parameters handle this automatically.

```python
# BAD — SQL injection vulnerability
user_input = "1; DROP TABLE users; --"
query = f"SELECT * FROM users WHERE id = {user_input}"   # NEVER!

# GOOD — parameterized query (SQLAlchemy text)
from sqlalchemy import text

result = await db.execute(
    text("SELECT * FROM users WHERE id = :user_id"),
    {"user_id": user_id}   # safely bound
)

# GOOD — ORM (always safe)
user = await db.get(User, user_id)

# GOOD — select with filter
result = await db.execute(
    select(User).where(User.email == user_email)
)
```

> **Interviewer tip:** OWASP ranks SQL injection as a top web vulnerability. Always say: "I use SQLAlchemy ORM or parameterized queries — never string formatting for SQL."

---

### Q86. What is Redis and what are its main data structures?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Redis supports multiple data structures beyond simple key-value: Strings, Lists, Hashes, Sets, Sorted Sets, Streams, and Pub/Sub channels.

```python
import redis
r = redis.Redis()

# String — simple cache
r.setex("user:1:name", 300, "Raj")      # TTL 5 min
print(r.get("user:1:name"))              # b'Raj'

# List — queue / recent items
r.lpush("notifications:1", "Order shipped")
r.ltrim("notifications:1", 0, 9)         # keep last 10

# Hash — structured object
r.hset("user:1", mapping={"name": "Raj", "role": "admin"})
print(r.hgetall("user:1"))

# Sorted Set — leaderboard
r.zadd("leaderboard", {"Raj": 1500, "Priya": 2000, "Anita": 1800})
print(r.zrevrange("leaderboard", 0, 2, withscores=True))  # top 3

# Set — unique visitors
r.sadd("visitors:today", "user:1", "user:2", "user:1")
print(r.scard("visitors:today"))   # 2 — unique count
```

> **Interviewer tip:** Sorted Set is perfect for leaderboards and rate limiting. Pub/Sub is used for real-time notifications. Streams are used for event sourcing.

---

### Q87. How do you implement full-text search in PostgreSQL?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
PostgreSQL has built-in full-text search using `tsvector` and `tsquery`. For production-scale search, use Elasticsearch or PostgreSQL's `pg_trgm` extension.

```sql
-- Add a search vector column
ALTER TABLE products ADD COLUMN search_vector tsvector;

UPDATE products SET search_vector =
    to_tsvector('english', name || ' ' || description);

-- Create GIN index for fast search
CREATE INDEX idx_products_search ON products USING GIN(search_vector);

-- Search query
SELECT name, ts_rank(search_vector, query) AS rank
FROM products, to_tsquery('english', 'laptop & gaming') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

```python
# SQLAlchemy with full-text search
from sqlalchemy import func, cast
from sqlalchemy.dialects.postgresql import TSVECTOR

result = await db.execute(
    select(Product)
    .where(
        func.to_tsvector("english", Product.name)
        .op("@@")(func.to_tsquery("english", "laptop"))
    )
)
```

> **Interviewer tip:** For multi-language apps or complex search (fuzzy, facets), use Elasticsearch. For simple keyword search within PostgreSQL, `tsvector` + GIN index is excellent.

---

## Testing & DevOps

### Q88. What is mocking and how do you use `unittest.mock`?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Mocking replaces real objects with fake ones during testing — lets you test code in isolation without hitting real databases, APIs, or external services.

```python
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# Mock a function
with patch("myapp.services.send_email") as mock_email:
    mock_email.return_value = True
    result = register_user("raj@test.com")
    mock_email.assert_called_once_with("raj@test.com")

# Mock in pytest with decorator
@patch("myapp.db.get_user")
def test_get_profile(mock_get_user):
    mock_get_user.return_value = {"id": 1, "name": "Raj"}
    result = get_user_profile(1)
    assert result["name"] == "Raj"

# Mock async functions
@pytest.mark.asyncio
async def test_async_service():
    with patch("myapp.services.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": [1, 2, 3]}
        result = await process_data()
        assert result == [1, 2, 3]
```

> **Interviewer tip:** `patch` path must be where the name is USED, not where it's defined. If `services.py` imports `send_email` from `utils.py`, patch `myapp.services.send_email`, not `myapp.utils.send_email`.

---

### Q89. What is `pytest` fixture scope and how does it affect performance?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Fixture scope controls how often a fixture is created: `function` (every test), `class`, `module`, `session` (once per test run). Use higher scope for expensive setup like DB connections.

```python
import pytest

# function scope (default) — created/destroyed per test
@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()

# session scope — created once for entire test run
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    yield engine
    engine.dispose()

# module scope — created once per test file
@pytest.fixture(scope="module")
def sample_users(db_engine):
    # seed test data once per module
    with db_engine.connect() as conn:
        conn.execute(insert_users_sql)
    yield
    with db_engine.connect() as conn:
        conn.execute(delete_users_sql)
```

> **Interviewer tip:** Use `session` scope for DB engine, `function` scope for transactions (rollback after each test keeps tests isolated). This pattern makes the test suite fast without sacrificing isolation.

---

### Q90. How do you measure code coverage in Python?
**Level:** Easy | **Frequency:** Frequent

**Answer:**
Use `pytest-cov` to measure which lines of code are executed during tests. Aim for 80%+ coverage on business logic.

```bash
# Install
pip install pytest-cov

# Run tests with coverage
pytest --cov=myapp --cov-report=html tests/

# Coverage report in terminal
pytest --cov=myapp --cov-report=term-missing

# Set minimum coverage threshold (fails if below 80%)
pytest --cov=myapp --cov-fail-under=80
```

```python
# .coveragerc — configure what to include/exclude
[coverage:run]
source = myapp
omit =
    */tests/*
    */migrations/*
    */config.py

[coverage:report]
exclude_lines =
    pragma: no cover
    if TYPE_CHECKING:
```

> **Interviewer tip:** 100% coverage doesn't mean bug-free. Focus coverage on business logic and edge cases, not boilerplate. A test that executes a line but doesn't assert anything is worse than no test.

---

## Performance & Best Practices

### Q91. How do you profile Python code?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Use `cProfile` for function-level profiling, `line_profiler` for line-by-line, and `memory_profiler` for memory usage. Always profile before optimizing.

```python
# cProfile — built-in, function level
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(10)   # top 10 functions

# In terminal
# python -m cProfile -s cumulative script.py

# line_profiler — line by line (pip install line-profiler)
@profile   # decorator added by line_profiler
def process_data(data):
    result = []
    for item in data:        # which line is slow?
        result.append(item * 2)
    return result

# memory_profiler (pip install memory-profiler)
@profile
def load_data():
    data = [i for i in range(1_000_000)]
    return data
```

> **Interviewer tip:** "Measure first, optimize second." — Don't guess. `cProfile` shows cumulative time per function. `line_profiler` shows exactly which line is the bottleneck.

---

### Q92. What is `lru_cache` and when should you use it?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
`lru_cache` (Least Recently Used cache) memoizes function results — if called with the same arguments again, returns the cached result instead of recomputing. Only works with pure functions (same input → same output, no side effects).

```python
from functools import lru_cache
import time

# Without cache — very slow for overlapping subproblems
def fib_slow(n):
    if n < 2: return n
    return fib_slow(n-1) + fib_slow(n-2)

# With cache — O(n) instead of O(2^n)
@lru_cache(maxsize=None)
def fib_fast(n):
    if n < 2: return n
    return fib_fast(n-1) + fib_fast(n-2)

# Real use case — caching DB lookup
@lru_cache(maxsize=256)
def get_country_code(country_name: str) -> str:
    return db.query_sync(f"SELECT code FROM countries WHERE name='{country_name}'")

# Cache info
print(fib_fast.cache_info())
# CacheInfo(hits=..., misses=..., maxsize=None, currsize=...)

# Clear cache when data changes
get_country_code.cache_clear()
```

> **Interviewer tip:** `maxsize=None` = unlimited cache (watch memory). `maxsize=128` = LRU eviction. Arguments must be hashable — can't cache calls with list/dict arguments.

---

### Q93. What are Python's common performance anti-patterns?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
Common anti-patterns: string concatenation in loops, unnecessary list creation, repeated attribute lookups, not using built-ins, global variable lookups.

```python
# BAD — string concatenation in loop (O(n²) copies)
result = ""
for word in words:
    result += word + " "

# GOOD — join (O(n))
result = " ".join(words)

# BAD — range(len(x)) + indexing
for i in range(len(items)):
    process(items[i])

# GOOD — direct iteration
for item in items:
    process(item)

# BAD — repeated attribute lookup in loop
import math
for x in data:
    y = math.sqrt(x)   # Python looks up 'math', then 'sqrt' each time

# GOOD — cache the reference
sqrt = math.sqrt
for x in data:
    y = sqrt(x)

# BAD — building list you only iterate once
for x in list(range(1_000_000)):
    process(x)

# GOOD — use generator
for x in range(1_000_000):
    process(x)
```

> **Interviewer tip:** `"".join(list)` vs `+=` in loops is a classic interview question. The join approach is O(n) — each concatenation in a loop copies the entire string.

---

### Q94. What is the difference between `multiprocessing.Pool` and `ProcessPoolExecutor`?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Both run tasks in separate processes to bypass the GIL. `ProcessPoolExecutor` (from `concurrent.futures`) has a cleaner API with `Future` objects. `Pool` from `multiprocessing` is older but has more fine-grained control.

```python
# ProcessPoolExecutor — preferred (cleaner API)
from concurrent.futures import ProcessPoolExecutor, as_completed

def cpu_task(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(cpu_task, n): n for n in range(10)}
    for future in as_completed(futures):
        result = future.result()
        print(f"Done: {result}")

# multiprocessing.Pool — older but has chunksize for better batching
from multiprocessing import Pool

with Pool(processes=4) as pool:
    results = pool.map(cpu_task, range(10), chunksize=3)
    # chunksize batches tasks — reduces IPC overhead for many small tasks
```

> **Interviewer tip:** `as_completed()` processes results as they finish — not in submission order. Use it when results can be processed independently as soon as they're ready.

---

### Q95. What is the `asyncio.Queue` and how do you build a producer-consumer pattern?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
`asyncio.Queue` is a thread-safe async queue for passing data between coroutines. The producer-consumer pattern separates data generation from data processing.

```python
import asyncio

async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
        print(f"Produced: {item}")
        await asyncio.sleep(0.1)
    await queue.put(None)   # sentinel to signal done

async def consumer(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)   # pass sentinel to next worker
            break
        print(f"Worker {worker_id} processing: {item}")
        await asyncio.sleep(0.3)   # simulate work
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=5)   # bounded queue — backpressure

    items = [f"task_{i}" for i in range(10)]
    prod  = asyncio.create_task(producer(queue, items))
    workers = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    await asyncio.gather(prod, *workers)

asyncio.run(main())
```

> **Interviewer tip:** `maxsize` on the queue creates backpressure — producer blocks when queue is full, preventing memory overflow when consumers are slow.

---

## System Design & Architecture

### Q96. How do you design a URL shortener backend in Python?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
Core components: ID generation, storage (DB + Redis cache), redirect endpoint. Key decisions: collision handling, custom slugs, analytics.

```python
import hashlib
import base64
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

def generate_short_code(url: str, length: int = 7) -> str:
    hash_bytes = hashlib.md5(url.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes)[:length].decode()

@app.post("/shorten")
async def shorten_url(url: str, db=Depends(get_db)):
    code = generate_short_code(url)

    # Handle collisions
    existing = await db.get(ShortURL, code)
    if existing and existing.original_url != url:
        code = generate_short_code(url + str(time.time()))

    short = ShortURL(code=code, original_url=url)
    db.add(short)
    await db.commit()

    # Cache in Redis
    r.setex(f"url:{code}", 86400, url)   # 24 hour TTL

    return {"short_url": f"https://short.ly/{code}"}

@app.get("/{code}")
async def redirect(code: str, db=Depends(get_db)):
    # Check Redis cache first
    url = r.get(f"url:{code}")
    if url:
        return RedirectResponse(url.decode(), status_code=301)

    short = await db.get(ShortURL, code)
    if not short:
        raise HTTPException(404, "URL not found")

    r.setex(f"url:{code}", 86400, short.original_url)
    return RedirectResponse(short.original_url, status_code=301)
```

> **Interviewer tip:** 301 (permanent redirect) is cached by browsers — great for performance but means you can't update the destination. Use 302 (temporary) if you need analytics or want to be able to change the destination.

---

### Q97. How do you design a task queue system?
**Level:** Hard | **Frequency:** Frequent

**Answer:**
Task queues decouple slow/async work from request handling. Components: task producer, message broker (Redis/RabbitMQ), worker processes, result backend.

```python
# Celery setup
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery("tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

logger = get_task_logger(__name__)

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, to: str, subject: str, body: str):
    try:
        smtp_send(to, subject, body)
        logger.info(f"Email sent to {to}")
    except Exception as exc:
        logger.error(f"Failed: {exc}")
        raise self.retry(exc=exc)

@app.task
def process_image(image_id: int):
    image = load_image(image_id)
    resized = resize(image, 800, 600)
    save_image(resized, image_id)

# FastAPI endpoint — enqueue task
@router.post("/send-newsletter")
async def send_newsletter(emails: list[str]):
    for email in emails:
        send_email.delay(email, "Newsletter", "Content...")
    return {"queued": len(emails)}

# Run workers
# celery -A tasks worker --loglevel=info --concurrency=4
```

> **Interviewer tip:** `bind=True` gives access to `self` (the task instance) for retries. `max_retries` with exponential backoff is essential for transient failures like network errors.

---

### Q98. How do you implement pagination in FastAPI?
**Level:** Medium | **Frequency:** Very frequent

**Answer:**
Two common strategies: offset/limit (simple, works for most cases) and cursor-based (better for large datasets and real-time data).

```python
from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

# Offset pagination — simple
@app.get("/users", response_model=Page[UserOut])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * size

    total = await db.scalar(select(func.count(User.id)))
    users = (await db.execute(
        select(User).offset(offset).limit(size)
    )).scalars().all()

    return Page(
        items=users, total=total,
        page=page, size=size,
        pages=math.ceil(total / size)
    )

# Cursor pagination — better for real-time data
@app.get("/feed")
async def get_feed(
    cursor: int = Query(None),   # last seen ID
    limit: int = Query(20)
):
    query = select(Post).order_by(Post.id.desc()).limit(limit)
    if cursor:
        query = query.where(Post.id < cursor)
    posts = (await db.execute(query)).scalars().all()
    next_cursor = posts[-1].id if posts else None
    return {"items": posts, "next_cursor": next_cursor}
```

> **Interviewer tip:** Offset pagination has a problem — if items are added/removed between pages, users see duplicates or miss items. Cursor pagination solves this and also performs better on large tables (no OFFSET scan).

---

### Q99. What is the 12-factor app methodology and how does Python follow it?
**Level:** Medium | **Frequency:** Frequent

**Answer:**
12-factor is a methodology for building scalable, maintainable web apps. Key factors most relevant to Python backends:

```python
# Factor 3: Config in environment — not hardcoded
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str          # from environment
    redis_url:    str
    secret_key:   str
    debug:        bool = False
    model_config = {"env_file": ".env"}

# Factor 4: Backing services as attached resources
# DB, Redis, S3 — accessed via URL, swappable

# Factor 6: Stateless processes
# No local state between requests — store in DB/Redis

# Factor 7: Port binding
# uvicorn main:app --host 0.0.0.0 --port 8000

# Factor 8: Concurrency — scale via processes
# uvicorn --workers 4  (multiple processes)

# Factor 11: Logs as event streams
import logging
logging.basicConfig(level=logging.INFO)   # write to stdout
# Let the platform (Docker, Kubernetes) collect and route logs

# Factor 12: Dev/prod parity
# Docker ensures same environment in dev and prod
```

> **Interviewer tip:** Knowing 12-factor shows you think beyond just writing code — you understand deployment and operations. "I follow factor 3 by never hardcoding config — everything goes through environment variables and pydantic-settings."

---

### Q100. How do you approach debugging a slow API endpoint in production?
**Level:** Hard | **Frequency:** Very frequent

**Answer:**
Systematic approach: measure → identify → fix → verify. Use logging, APM tools, and database query analysis.

```python
# Step 1 — Add timing middleware to identify slow endpoints
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    response.headers["X-Response-Time"] = f"{duration:.2f}ms"
    if duration > 500:
        logger.warning(f"SLOW: {request.url.path} took {duration:.0f}ms")
    return response

# Step 2 — Log slow DB queries
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Step 3 — Use EXPLAIN ANALYZE on slow queries
result = await db.execute(text("EXPLAIN ANALYZE " + your_query))

# Step 4 — Add indexes for slow WHERE / JOIN columns
# CREATE INDEX CONCURRENTLY idx_orders_created ON orders(created_at);
# CONCURRENTLY avoids locking the table in production

# Step 5 — Add caching for repeated expensive queries
@lru_cache(maxsize=128)
def get_static_config(key: str) -> str:
    return db.query_sync(...)

# Step 6 — Profile with py-spy (no code changes needed)
# py-spy top --pid <your_process_pid>
# py-spy record -o profile.svg --pid <pid>
```

> **Interviewer tip:** Structure your answer as a process: "First I'd check the logs and APM dashboard, then identify if it's a slow query (EXPLAIN ANALYZE), a missing index, an N+1, or application-level code. Then fix and verify the improvement with metrics — not just intuition."

---

## Final Interview Answer Templates

### "Tell me about your most challenging technical problem"
```
Situation: We had an API endpoint returning in 3-4 seconds under load.
Task:      Reduce it to under 200ms.
Action:    1. Added timing middleware to confirm the bottleneck
           2. Enabled SQL logging — found N+1 query (101 DB calls per request)
           3. Added selectinload() → 2 queries
           4. Added Redis cache for repeated user lookups (TTL 5 min)
Result:    Response time dropped from 3400ms to 85ms (40x improvement)
```

### "How do you ensure code quality?"
```
- Type hints + mypy in CI (catches type bugs before runtime)
- pytest with 80%+ coverage on business logic
- Code review with focus on: N+1 queries, missing indexes, error handling
- Pre-commit hooks: black (formatting), isort (imports), flake8 (linting)
- Structured logging in production — all errors go to Sentry
```

### "How do you handle a production incident?"
```
1. Mitigate first — rollback, feature flag, scale up
2. Communicate — update status page, notify stakeholders
3. Investigate — check logs, metrics, recent deployments
4. Fix — targeted patch, not a rush rewrite
5. Post-mortem — what happened, why, how to prevent
```

---

*This is Part 2 (Q51–Q100). See Part 1 for Q1–Q50 covering Core Python, OOP, Functions, Advanced, Concurrency, FastAPI, and Database basics.*