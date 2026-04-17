# 📅 Day 1 — Core Python (Strong Foundation)

> **Goal:** Clear fundamentals + tricky concepts  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: Data Types — `list`, `tuple`, `set`, `dict`

### 🔹 List
- **Ordered**, **mutable**, **allows duplicates**
- Syntax: `[1, 2, 3]`

```python   
fruits = ["apple", "banana", "apple"]
fruits.append("cherry")      # Add to end
fruits.insert(1, "mango")    # Insert at index
fruits.remove("banana")      # Remove by value
fruits.pop()                 # Remove last element
fruits[0]                    # Access by index
fruits[1:3]                  # Slicing
len(fruits)                  # Length
```

**Common methods:**
| Method | Description |
|--------|-------------|
| `append(x)` | Add to end |
| `insert(i, x)` | Insert at index |
| `remove(x)` | Remove first occurrence |
| `pop(i)` | Remove at index (default last) |
| `sort()` | Sort in place |
| `reverse()` | Reverse in place |
| `count(x)` | Count occurrences |
| `index(x)` | Find index of first occurrence |

---

### 🔹 Tuple
- **Ordered**, **immutable**, **allows duplicates**
- Syntax: `(1, 2, 3)`

```python
coords = (10, 20)
coords[0]           # Access → 10
# coords[0] = 99   # ❌ TypeError: can't modify tuple

# Single element tuple (must have comma!)
single = (5,)       # ✅ This is a tuple
not_tuple = (5)     # ❌ This is just an integer

# Tuple unpacking
x, y = coords
print(x, y)         # 10  20

# Tuple methods
coords.count(10)    # 1
coords.index(20)    # 1

#2nd example of unpacking
tuple1 = (1, 2, 3)
x, y, z = tuple1
print(x)  # Output: 1
print(y)  # Output: 2
print(z)  # Output: 3
```

**When to use tuple:**
- Coordinates, RGB values, DB records
- Function returning multiple values
- As dictionary keys (lists can't be keys)

---

### 🔹 Set
- **Unordered**, **mutable**, **NO duplicates**
- Syntax: `{1, 2, 3}`

```python
nums = {1, 2, 3, 3, 2}
print(nums)             # {1, 2, 3} — duplicates removed

nums.add(4)             # Add element
nums.remove(2)          # Remove (KeyError if not found)
nums.discard(99)        # Remove safely (no error)

# Set operations
a = {1, 2, 3}
b = {3, 4, 5}

a | b                   # Union       → {1, 2, 3, 4, 5}          means "in a or b or both"
a & b                   # Intersection → {3}                     means "in both a and b"
a - b                   # Difference  → {1, 2}                   means "in a but not in b"
a ^ b                   # Symmetric difference → {1, 2, 4, 5}    means "in a or b but not both"
```

**Common use case:** Remove duplicates from a list
```python
my_list = [1, 2, 2, 3, 3, 3]
unique = list(set(my_list))   # [1, 2, 3]
```

⚠️ **Note:** Sets don't preserve order!

---

### 🔹 Dict
- **Ordered** (Python 3.7+), **mutable**, **key-value pairs**, **keys must be unique**
- Syntax: `{"key": "value"}`

```python
person = {"name": "Alice", "age": 25, "city": "Delhi"}

# Access
person["name"]              # "Alice"
person.get("salary", 0)     # 0 (default if key missing)


# if key exists, get value; else return "Not Available"
print(person.get("salary", "Not Available"))

# Modify
person["age"] = 26          # Update
person["email"] = "a@b.com" # Add new key

# Delete
del person["city"]
person.pop("age")           # Returns value before deleting

# Iterate
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(key, value)

# Useful methods
person.keys()               # dict_keys(['name', 'email'])
person.values()             # dict_values(['Alice', 'a@b.com'])
person.items()              # dict_items([...])
person.update({"age": 27})  # Merge/update
```

---

### 📊 Quick Comparison Table

| Feature | List | Tuple | Set | Dict |
|---------|------|-------|-----|------|
| Ordered | ✅ | ✅ | ❌ | ✅ (3.7+) |
| Mutable | ✅ | ❌ | ✅ | ✅ |
| Duplicates | ✅ | ✅ | ❌ | Keys: ❌ |
| Indexed | ✅ | ✅ | ❌ | By key |
| Syntax | `[]` | `()` | `{}` | `{k:v}` |

---

## 📌 Topic 2: Mutability vs Immutability

### 🔹 What is Mutability?
- **Mutable** = Can be changed after creation (list, dict, set)
- **Immutable** = Cannot be changed after creation (int, float, str, tuple, bool)

```python
# Mutable example — list
my_list = [1, 2, 3]
my_list[0] = 99
print(my_list)      # [99, 2, 3] ✅ Changed in place

# Immutable example — string
my_str = "hello"
# my_str[0] = "H"  # ❌ TypeError

# Strings create new objects
my_str = my_str + " world"   # New string created
```

### 🔹 Why Does It Matter?

```python
# Mutable objects passed to functions CAN be modified
def add_item(lst):
    lst.append(4)

nums = [1, 2, 3]
add_item(nums)
print(nums)          # [1, 2, 3, 4] ← original changed!

# Immutable objects passed to functions CANNOT be modified
def change_num(n):
    n = 99

x = 5
change_num(x)
print(x)             # 5 ← original unchanged
```

### 🔹 Mutable Default Argument Bug (Common Interview Trap!)

```python
# ❌ WRONG — mutable default argument
def append_to(element, lst=[]):
    lst.append(element)
    return lst

print(append_to(1))   # [1]
print(append_to(2))   # [1, 2] ← Bug! Reuses same list

# ✅ CORRECT — use None as default
def append_to(element, lst=None):
    if lst is None:
        lst = []
    lst.append(element)
    return lst
```

---

## 📌 Topic 3: `is` vs `==`

### 🔹 The Difference

| Operator | Checks |
|----------|--------|
| `==` | **Value equality** — are the values the same? |
| `is` | **Identity equality** — are they the same object in memory? |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True  — same values
print(a is b)    # False — different objects in memory
print(a is c)    # True  — c points to same object as a

    

```

### 🔹 The Integer Caching Trick (Interview Favorite!)

```python
# Python caches small integers (-5 to 256)
x = 100
y = 100
print(x is y)    # True ← cached, same object

x = 1000
y = 1000
print(x is y)    # False ← not cached, different objects

                 # python caches small integers -5 to 256, so `is` returns True for them. For larger numbers, a new object is created each time.

                 # Python caches small integers, but is should never be used for value comparison because object identity is implementation-dependent and can lead to confusing bugs.

```

### 🔹 String Interning

```python
a = "hello"
b = "hello"
print(a is b)    # True — Python interns short strings

a = "hello world"
b = "hello world"
print(a is b)    # May be False — longer strings may not be interned
```

### ✅ Rule of Thumb
- Use `==` for comparing values (almost always)
- Use `is` only for `None`, `True`, `False` checks

```python
# ✅ Correct way to check None
if result is None:
    print("No result")

# ❌ Avoid
if result == None:   # Works but not Pythonic
```

---

## 📌 Topic 4: Shallow vs Deep Copy

### 🔹 Assignment (Not a copy at all!)

```python
a = [1, 2, [3, 4]]
b = a              # b points to SAME object

b[0] = 99
print(a)           # [99, 2, [3, 4]] ← a also changed!
```

### 🔹 Shallow Copy
- Copies the **outer object**, but **nested objects are still shared**

```python
import copy

a = [1, 2, [3, 4]]
b = copy.copy(a)       # Shallow copy
# Also: b = a[:]  or  b = list(a)

b[0] = 99              # Changes b only
print(a)               # [1, 2, [3, 4]] ✅ outer unchanged

b[2][0] = 999          # Changes nested list
print(a)               # [1, 2, [999, 4]] ⚠️ a's nested list changed!
```

### 🔹 Deep Copy
- Copies **everything** — outer and all nested objects

```python
import copy

a = [1, 2, [3, 4]]
b = copy.deepcopy(a)   # Deep copy

b[2][0] = 999
print(a)               # [1, 2, [3, 4]] ✅ completely independent
print(b)               # [1, 2, [999, 4]]
```

### 📊 Visual Summary

```
Original:   a → [1, 2, → [3, 4]]
                          ↑
Assignment: b ────────────────── (same object)

Shallow:    b → [1, 2, → [3, 4]]  (new list, same nested ref)
                          ↑ shared

Deep:       b → [1, 2, → [3, 4]]  (completely new everything)
```

### 🔹 Shallow Copy Methods

```python
a = [1, 2, 3]

b = a[:]           # Slicing
b = list(a)        # list() constructor
b = a.copy()       # .copy() method

import copy
b = copy.copy(a)   # copy module
```

---

## 📌 Topic 5: Truthy vs Falsy

### 🔹 Falsy Values (evaluate to `False` in boolean context)

```python
# All of these are Falsy:
bool(None)      # False
bool(0)         # False
bool(0.0)       # False
bool("")        # False — empty string
bool([])        # False — empty list
bool(())        # False — empty tuple
bool({})        # False — empty dict
bool(set())     # False — empty set
bool(False)     # False
```

### 🔹 Truthy Values (everything else)

```python
bool(1)         # True
bool(-1)        # True (any non-zero number)
bool("hello")   # True (non-empty string)
bool([0])       # True (non-empty list, even if it contains falsy values)
bool({"a": 1})  # True
```

### 🔹 Practical Usage

```python
# ✅ Pythonic way — check if list is not empty
my_list = [1, 2, 3]
if my_list:
    print("List has items")

# ❌ Less Pythonic
if len(my_list) > 0:
    print("List has items")

# Check for None
name = None
print(name or "Guest")    # "Guest" — uses default

# Short-circuit evaluation
x = 0
y = x or 10
print(y)                  # 10 — x is falsy, so y = 10

x = 5
y = x or 10
print(y)                  # 5 — x is truthy, so y = x
```

### 🔹 `and` / `or` Return Values (not just True/False!)

```python
# `or` returns first truthy value, or last value
0 or "" or "hello"    # "hello"
0 or [] or {}         # {} (all falsy, returns last)

# `and` returns first falsy value, or last value
1 and 2 and 3         # 3 (all truthy, returns last)
1 and 0 and 3         # 0 (first falsy)
```

---

## 🛠️ Practice Problems

### ✅ Problem 1: Remove Duplicates from List

```python
# Method 1: Using set (doesn't preserve order)
def remove_duplicates_set(lst):
    return list(set(lst))

# Method 2: Preserve order using dict.fromkeys
def remove_duplicates_ordered(lst):
    return list(dict.fromkeys(lst))

# Method 3: Manual loop
def remove_duplicates_loop(lst):
    seen = []
    for item in lst:
        if item not in seen:
            seen.append(item)
    return seen

# Method 4: List comprehension
def remove_duplicates_comp(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# Test
nums = [1, 2, 2, 3, 3, 3, 4]
print(remove_duplicates_set(nums))      # [1, 2, 3, 4]
print(remove_duplicates_ordered(nums))  # [1, 2, 3, 4] (order preserved)
```

---

### ✅ Problem 2: Find Frequency of Elements

```python
# Method 1: Using dict
def frequency_dict(lst):
    freq = {}
    for item in lst:
        freq[item] = freq.get(item, 0) + 1
    return freq

# Method 2: Using Counter (most Pythonic)
from collections import Counter

def frequency_counter(lst):
    return dict(Counter(lst))

# Method 3: Dict comprehension
def frequency_comp(lst):
    return {item: lst.count(item) for item in set(lst)}

# Test
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print(frequency_dict(words))     # {'apple': 3, 'banana': 2, 'cherry': 1}
print(frequency_counter(words))  # same result

# Bonus: Most common
c = Counter(words)
print(c.most_common(2))          # [('apple', 3), ('banana', 2)]
```

---

### ✅ Problem 3: Reverse a List (Multiple Ways)

```python
my_list = [1, 2, 3, 4, 5]

# Method 1: Slicing (creates new list)
reversed_list = my_list[::-1]
print(reversed_list)     # [5, 4, 3, 2, 1]

# Method 2: reversed() built-in (returns iterator)
reversed_list = list(reversed(my_list))
print(reversed_list)     # [5, 4, 3, 2, 1]

# Method 3: .reverse() in place (mutates original)
my_list.reverse()
print(my_list)           # [5, 4, 3, 2, 1]

# Method 4: Manual loop
def reverse_manual(lst):
    result = []
    for i in range(len(lst) - 1, -1, -1):
        result.append(lst[i])
    return result

# Method 5: Two-pointer swap
def reverse_inplace(lst):
    left, right = 0, len(lst) - 1
    while left < right:
        lst[left], lst[right] = lst[right], lst[left]
        left += 1
        right -= 1
    return lst
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What's the difference between list and tuple?**  
A: List is mutable (can change), tuple is immutable (cannot change). Tuples are faster and can be used as dict keys.

**Q: Can a set contain a list?**  
A: No. Sets require hashable (immutable) elements. Lists are unhashable, so they can't be in a set.

**Q: What is `a is b` checking?**  
A: It checks if `a` and `b` point to the **same object in memory**, not just equal values.

**Q: What happens with small integers and `is`?**  
A: Python caches integers from -5 to 256, so `is` returns `True` for them. For larger numbers, a new object is created each time.

**Q: What is a shallow copy?**  
A: A new outer object is created, but nested objects are still shared references.

**Q: Name 3 falsy values.**  
A: `None`, `0`, `""`, `[]`, `{}`, `False` — pick any 3.

**Q: How do you remove duplicates while preserving order?**  
A: `list(dict.fromkeys(my_list))` — since Python 3.7+, dicts maintain insertion order.

---

## 📝 Key Takeaways

1. **list = mutable, ordered** | **tuple = immutable, ordered** | **set = mutable, unordered, no dups** | **dict = key-value, ordered**
2. **Mutability** matters when passing objects to functions — lists get modified, integers don't
3. **`is`** checks identity (memory address), **`==`** checks value — use `is` only for `None`/`True`/`False`
4. **Shallow copy** shares nested references — use `copy.deepcopy()` for truly independent copies
5. **Falsy**: `None`, `0`, `""`, `[]`, `{}`, `()`, `set()`, `False` — everything else is truthy

---

*Day 1 Complete ✅ → Move to Day 2: Functions + Python Behavior*


---
---
---
---
---
---






# 📅 Day 2 — Functions + Python Behavior

> **Goal:** Write clean, Pythonic code  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: Functions — The Basics First

Before diving into `*args` and `**kwargs`, let's make sure the foundation is rock solid.

### 🔹 What is a Function?

A function is a **reusable block of code** that performs a specific task.  
**Why use functions?**
- Avoid repetition (DRY — Don't Repeat Yourself)
- Make code readable and testable
- Break big problems into small pieces

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))    # Hello, Alice!
```

### 🔹 Function Anatomy  - means the structure of a function, including its definition, name, parameters, body, and return value.

```python
def function_name(parameter1, parameter2):
    """Docstring — explains what this function does."""
    # function body
    result = parameter1 + parameter2
    return result          # return is optional

# Calling the function
output = function_name(10, 20)
print(output)    # 30
```

### 🔹 Return Values

```python
# Return nothing → returns None implicitly
def say_hi():
    print("Hi!")

result = say_hi()
print(result)       # None

# Return multiple values (actually returns a tuple)
def min_max(lst):
    return min(lst), max(lst)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(low, high)    # 1 9


def return_multiple_values(list):
    
    return min(list), max(list), sum(list)

numbers = [3, 1, 4, 1, 5]
min_value, max_value, total = return_multiple_values(numbers)
print(f"Min: {min_value}, Max: {max_value}, Sum: {total}")            # Min: 1, Max: 5, Sum: 14
```

---

## 📌 Topic 2: `*args` and `**kwargs`

### 🔹 Why Do We Need Them?

Sometimes you don't know in advance how many arguments a function will receive.  
That's where `*args` and `**kwargs` come in.

---

### 🔹 `*args` — Variable Positional Arguments

- `*args` collects **extra positional arguments** into a **tuple**
- The `*` is the magic — `args` is just a convention (could be `*numbers`, `*items`)

```python
def add_all(*args):
    print(type(args))   # <class 'tuple'>
    print(args)         # (1, 2, 3, 4, 5)
    return sum(args)

print(add_all(1, 2, 3))        # 6
print(add_all(1, 2, 3, 4, 5))  # 15
print(add_all(10))              # 10
```

**Mixing regular and `*args`:**

```python
def greet_many(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet_many("Hello", "Alice", "Bob", "Charlie")
# Hello, Alice!
# Hello, Bob!
# Hello, Charlie!
```

**Unpacking with `*` when calling:**

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))    # 6 — unpacks list into positional args
```

---

### 🔹 `**kwargs` — Variable Keyword Arguments

- `**kwargs` collects **extra keyword arguments** into a **dict**
- The `**` is the magic — `kwargs` is just a convention

```python
def display_info(**kwargs):
    print(type(kwargs))   # <class 'dict'>
    for key, value in kwargs.items():
        print(f"{key}: {value}")

display_info(name="Alice", age=25, city="Delhi")
# name: Alice
# age: 25
# city: Delhi
```

**Mixing regular args, `*args`, and `**kwargs`:**

```python
def full_function(a, b, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

full_function(1, 2, 3, 4, 5, name="Alice", city="Delhi")
# a=1, b=2
# args=(3, 4, 5)
# kwargs={'name': 'Alice', 'city': 'Delhi'}
```

**Unpacking with `**` when calling:**

```python
def create_user(name, age, city):
    print(f"Creating user: {name}, {age}, {city}")

user_data = {"name": "Bob", "age": 30, "city": "Mumbai"}
create_user(**user_data)    # unpacks dict into keyword args
```

---

### 🔹 Order of Parameters — CRITICAL RULE

```
def func(positional, *args, keyword_only, **kwargs)
          ↑            ↑         ↑              ↑
        normal      extra     after *args    extra
        params    positional  = keyword      keyword
                               only!
```

```python
# Correct order
def correct(a, b, *args, **kwargs):
    pass

# ❌ SyntaxError — *args must come before **kwargs
# def wrong(a, **kwargs, *args): pass

# Keyword-only arguments (after *)
def keyword_only(a, b, *, must_name_me):
    print(a, b, must_name_me)

keyword_only(1, 2, must_name_me=99)    # ✅
# keyword_only(1, 2, 99)               # ❌ TypeError
```

---

## 📌 Topic 3: Default Arguments + The Mutable Default Bug

### 🔹 Default Arguments

```python
def power(base, exponent=2):
    return base ** exponent

print(power(3))      # 9  — uses default exponent=2
print(power(3, 3))   # 27 — overrides default
```

**Multiple defaults:**

```python
def connect(host="localhost", port=5432, debug=False):
    print(f"Connecting to {host}:{port}, debug={debug}")

connect()                           # localhost:5432, debug=False
connect("production.db")            # production.db:5432, debug=False
connect("production.db", 3306)      # production.db:3306, debug=False
connect(debug=True)                 # localhost:5432, debug=True
```

---

### 🔹 ⚠️ The Mutable Default Argument Bug — Most Common Interview Trap!

**Why does this happen?**

Default argument values are **evaluated ONCE when the function is defined**, not every time it's called.  
If the default is a mutable object (list, dict, set), it gets **shared across all calls**.

```python
# ❌ BUG — mutable default argument
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item("apple"))     # ['apple']
print(add_item("banana"))    # ['apple', 'banana'] ← BUG! Expected ['banana']
print(add_item("cherry"))    # ['apple', 'banana', 'cherry'] ← still growing!

# Why? The [] is created ONCE. The same list is reused every call.
```

**The Fix — Always use `None` as default:**

```python
# ✅ CORRECT
def add_item(item, lst=None):
    if lst is None:
        lst = []           # New list created each time
    lst.append(item)
    return lst

print(add_item("apple"))     # ['apple']
print(add_item("banana"))    # ['banana'] ✅ Fresh list!
```

**Same bug with dict:**

```python
# ❌ BUG
def add_key(key, value, data={}):
    data[key] = value
    return data

# ✅ FIX
def add_key(key, value, data=None):
    if data is None:
        data = {}
    data[key] = value
    return data
```

**Intentional use of mutable defaults (rare, advanced):**

```python
# Sometimes used for caching (memoization) — intentional shared state
def cached_fibonacci(n, cache={0: 0, 1: 1}):
    if n not in cache:
        cache[n] = cached_fibonacci(n-1) + cached_fibonacci(n-2)
    return cache[n]
```

---

## 📌 Topic 4: Lambda Functions

### 🔹 What is a Lambda?

A **lambda** is a small, anonymous, one-line function.  
**Why use it?** For short throwaway functions, especially as arguments to `map`, `filter`, `sorted`.

```python
# Regular function
def square(x):
    return x ** 2

# Equivalent lambda
square = lambda x: x ** 2

print(square(5))    # 25
```

**Syntax:**
```
lambda arguments : expression
       ↑                ↑
  one or more       single expression
  parameters        (auto-returned)
```

### 🔹 Lambda Examples

```python
# No arguments
greet = lambda: "Hello!"
print(greet())           # Hello!

# One argument
double = lambda x: x * 2
print(double(7))         # 14

# Multiple arguments
add = lambda x, y: x + y
print(add(3, 4))         # 7

# With condition (ternary)
is_even = lambda x: "even" if x % 2 == 0 else "odd"
print(is_even(4))        # even
print(is_even(7))        # odd
```

### 🔹 Lambda with `sorted()` — Very Common Interview Pattern

```python
# Sort list of tuples by second element
pairs = [(1, 3), (4, 1), (2, 2)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print(sorted_pairs)    # [(4, 1), (2, 2), (1, 3)]

# Sort list of dicts by a field
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print([s["name"] for s in by_grade])    # ['Bob', 'Alice', 'Charlie']

# Sort strings by length
words = ["banana", "apple", "kiwi", "cherry"]
print(sorted(words, key=lambda w: len(w)))   # ['kiwi', 'apple', 'banana', 'cherry']
```

### 🔹 Lambda Limitations

```python
# ❌ Can't use statements (if/else blocks, loops, assignments)
# lambda x: if x > 0: return x   # SyntaxError

# ❌ Can't span multiple lines

# ✅ Use regular function when logic is complex
def process(x):
    if x > 0:
        return x * 2
    elif x == 0:
        return 0
    else:
        return -x
```

> **Interview tip:** Lambda is great for simple key functions. For anything complex, use a regular `def`.

---

## 📌 Topic 5: `map`, `filter`, `reduce`

These are **higher-order functions** — they take a function as an argument.

### 🔹 `map()` — Transform Every Element

**How it works:** Apply a function to every item in an iterable. Returns a **map object** (lazy iterator).

```
map(function, iterable)
```

```python
# Double every number
nums = [1, 2, 3, 4, 5]
doubled = map(lambda x: x * 2, nums)
print(list(doubled))    # [2, 4, 6, 8, 10]

# Convert strings to integers
str_nums = ["1", "2", "3", "4"]
int_nums = list(map(int, str_nums))
print(int_nums)    # [1, 2, 3, 4]

# Apply to multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
result = list(map(lambda x, y: x + y, a, b))
print(result)      # [11, 22, 33]

# Using a regular function with map
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temps_c = [0, 20, 37, 100]
temps_f = list(map(celsius_to_fahrenheit, temps_c))
print(temps_f)    # [32.0, 68.0, 98.6, 212.0]
```

**map vs list comprehension:**

```python
# map way
result = list(map(lambda x: x**2, nums))

# List comprehension way (more Pythonic, preferred)
result = [x**2 for x in nums]
```

---

### 🔹 `filter()` — Keep Elements That Match a Condition

**How it works:** Apply a function that returns True/False. Keeps elements where function returns `True`.

```
filter(function, iterable)
```

```python
# Keep only even numbers
nums = [1, 2, 3, 4, 5, 6, 7, 8]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)    # [2, 4, 6, 8]

# Filter out None/falsy values
mixed = [0, 1, None, 2, "", 3, False, 4]
truthy = list(filter(None, mixed))   # None means use truthiness
print(truthy)    # [1, 2, 3, 4]

# Filter strings by condition
names = ["Alice", "Bob", "Alexander", "Charlie", "Aaron"]
long_names = list(filter(lambda name: len(name) > 4, names))
print(long_names)    # ['Alice', 'Alexander', 'Charlie']

# Filter dicts
employees = [
    {"name": "Alice", "salary": 50000},
    {"name": "Bob", "salary": 80000},
    {"name": "Charlie", "salary": 65000}
]
high_earners = list(filter(lambda e: e["salary"] > 60000, employees))
print([e["name"] for e in high_earners])    # ['Bob', 'Charlie']
```

---

### 🔹 `reduce()` — Combine All Elements Into One

**How it works:** Apply a function cumulatively to reduce the iterable to a single value.  
**Note:** Must import from `functools`.


from functools import reduce


list1 = [1, 2, 3, 4, 5]
#map filter and reducer

#map
def square(x):
    return x * x    
squared_list = list(map(square, list1))
print(squared_list)

#filter
def is_even(x):
    return x % 2 == 0
even_list = list(filter(is_even, list1))
print(even_list)



#reducefrom functools import reduce
def add(x, y):
    return x + y
sum_of_list = reduce(add, list1)
print(sum_of_list)

```
reduce(function, iterable, initial_value)
```

```python
from functools import reduce

# Sum all numbers (how it works step by step)
nums = [1, 2, 3, 4, 5]
#  Step 1: f(1, 2) → 3
#  Step 2: f(3, 3) → 6
#  Step 3: f(6, 4) → 10
#  Step 4: f(10, 5) → 15
result = reduce(lambda x, y: x + y, nums)
print(result)    # 15

# Product of all elements
product = reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
print(product)    # 120

# Find maximum manually
nums = [3, 1, 4, 1, 5, 9, 2, 6]
maximum = reduce(lambda x, y: x if x > y else y, nums)
print(maximum)    # 9

# Flatten a list of lists
lists = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda x, y: x + y, lists)
print(flat)    # [1, 2, 3, 4, 5, 6]

# With initial value
result = reduce(lambda x, y: x + y, [1, 2, 3], 100)
print(result)    # 106 (starts from 100)
```

---

### 🔹 Combining `map`, `filter`, `reduce` — Transformation Pipeline

```python
from functools import reduce

# Problem: Given a list of numbers,
# keep only evens, square them, then sum them all

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Step 1: filter evens
evens = filter(lambda x: x % 2 == 0, nums)

# Step 2: square them
squared = map(lambda x: x ** 2, evens)

# Step 3: sum them all
total = reduce(lambda x, y: x + y, squared)

print(total)    # 220  (4 + 16 + 36 + 64 + 100)

# One-liner version
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x**2,
        filter(lambda x: x % 2 == 0, nums))
)
print(result)    # 220
```

---

### 📊 `map` vs `filter` vs `reduce` Summary

| Function | Input | Output | Purpose |
|----------|-------|--------|---------|
| `map(f, lst)` | iterable | iterator (same size) | Transform every element |
| `filter(f, lst)` | iterable | iterator (≤ original size) | Keep matching elements |
| `reduce(f, lst)` | iterable | single value | Combine all into one |

---

## 📌 Topic 6: Variable Scope — Local, Global, `nonlocal`

### 🔹 What is Scope?

**Scope** = where a variable is accessible/visible.  
Python follows the **LEGB Rule** to look up variables:

```
L → Local       (inside current function)
E → Enclosing   (enclosing function, for nested functions)
G → Global      (module level)
B → Built-in    (Python's built-ins: len, print, range...)
```

Python searches in this order: **L → E → G → B**

---

### 🔹 Local Scope

Variables defined **inside a function** — only visible inside that function.

```python
def my_func():
    x = 10          # local variable
    print(x)        # 10 ✅

my_func()
# print(x)          # ❌ NameError: x is not defined
```

---

### 🔹 Global Scope

Variables defined **at the module level** — visible everywhere.

```python
x = 100    # global variable

def my_func():
    print(x)    # ✅ can READ global variable

my_func()       # 100
print(x)        # 100 ✅
```

**Trying to MODIFY a global variable from inside a function:**

```python
x = 100

def my_func():
    x = 200         # This creates a NEW local variable!
    print(x)        # 200 (local)

my_func()
print(x)            # 100 (global unchanged!)
```

**Using `global` keyword to modify:**

```python
x = 100

def my_func():
    global x        # tell Python: use the global x
    x = 200         # now modifies the global
    print(x)        # 200

my_func()
print(x)            # 200 (global changed!)
```

> **Best practice:** Avoid using `global`. Pass values as arguments and return them instead. `global` makes code hard to debug and test.

---

### 🔹 Enclosing Scope (Closures)

When you have a **function inside a function**, the inner function can access variables from the outer function.

```python
def outer():
    message = "Hello"      # enclosing scope variable

    def inner():
        print(message)     # ✅ accesses enclosing variable

    inner()

outer()    # Hello
```

---

### 🔹 `nonlocal` — Modify Enclosing Scope Variable

`nonlocal` lets an inner function **modify** a variable in its enclosing function.

```python
def counter():
    count = 0              # enclosing variable

    def increment():
        nonlocal count     # tell Python: use enclosing 'count'
        count += 1
        print(count)

    increment()    # 1
    increment()    # 2
    increment()    # 3

counter()
```

**Without `nonlocal` — it fails:**

```python
def counter():
    count = 0

    def increment():
        count += 1         # ❌ UnboundLocalError!
        # Python sees assignment → treats count as local
        # But local count doesn't exist yet!

    increment()
```

---

### 🔹 The LEGB Rule in Action

```python
x = "global"          # G — Global

def outer():
    x = "enclosing"   # E — Enclosing

    def inner():
        x = "local"   # L — Local
        print(x)      # local (L wins)

    inner()
    print(x)          # enclosing (E, since inner's L is gone)

outer()
print(x)              # global (G)
print(len)            # <built-in function len> (B — Built-in)
```

---

### 🔹 Scope Pitfall — Variable Shadowing

```python
# Accidentally shadowing built-ins
list = [1, 2, 3]         # ❌ You just shadowed the built-in `list`!
new_list = list([4, 5])  # ❌ TypeError: 'list' object is not callable

# ✅ Don't use built-in names as variable names:
# list, dict, set, str, int, float, type, id, input, print, etc.
```

---

### 🔹 `global` vs `nonlocal` — Comparison

```python
x = 0    # global

def outer():
    x = 10    # enclosing

    def modify_global():
        global x      # refers to module-level x = 0
        x = 999
        print("inside modify_global:", x)   # 999

    def modify_enclosing():
        nonlocal x    # refers to outer()'s x = 10
        x = 888
        print("inside modify_enclosing:", x)  # 888

    modify_global()
    print("after modify_global, outer x:", x)      # still 10

    modify_enclosing()
    print("after modify_enclosing, outer x:", x)   # now 888

outer()
print("global x:", x)    # 999
```

---

## 🛠️ Practice Problems

### ✅ Practice 1: Build Reusable Utility Functions

```python
# --- Utility Function Library ---

def clamp(value, min_val, max_val):
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))

print(clamp(15, 0, 10))    # 10
print(clamp(-5, 0, 10))    # 0
print(clamp(7, 0, 10))     # 7


def flatten(nested_list):
    """Flatten one level of nesting."""
    return [item for sublist in nested_list for item in sublist]

print(flatten([[1, 2], [3, 4], [5]]))    # [1, 2, 3, 4, 5]


def chunk(lst, size):
    """Split list into chunks of given size."""
    return [lst[i:i+size] for i in range(0, len(lst), size)]

print(chunk([1,2,3,4,5,6,7], 3))    # [[1,2,3], [4,5,6], [7]]


def safe_divide(a, b, default=0):
    """Divide a by b, return default if division by zero."""
    return a / b if b != 0 else default

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # 0


def merge_dicts(*dicts):
    """Merge multiple dicts. Later dicts override earlier ones."""
    result = {}
    for d in dicts:
        result.update(d)
    return result

print(merge_dicts({"a": 1}, {"b": 2}, {"a": 99}))   # {'a': 99, 'b': 2}


def count_if(lst, condition):
    """Count elements matching a condition function."""
    return sum(1 for item in lst if condition(item))

nums = [1, 2, 3, 4, 5, 6]
print(count_if(nums, lambda x: x % 2 == 0))    # 3 (evens)
print(count_if(nums, lambda x: x > 3))          # 3
```

---

### ✅ Practice 2: Transformation Pipelines

```python
from functools import reduce

# --- Pipeline 1: Process employee data ---

employees = [
    {"name": "Alice", "dept": "Engineering", "salary": 90000},
    {"name": "Bob", "dept": "Marketing", "salary": 55000},
    {"name": "Charlie", "dept": "Engineering", "salary": 75000},
    {"name": "Diana", "dept": "HR", "salary": 60000},
    {"name": "Eve", "dept": "Engineering", "salary": 105000},
]

# Get total salary of Engineering department
engineering_total = reduce(
    lambda acc, emp: acc + emp["salary"],
    filter(lambda e: e["dept"] == "Engineering", employees),
    0
)
print(f"Engineering total salary: {engineering_total}")    # 270000

# Get names of employees earning > 70000
high_earner_names = list(map(
    lambda e: e["name"],
    filter(lambda e: e["salary"] > 70000, employees)
))
print(f"High earners: {high_earner_names}")    # ['Alice', 'Charlie', 'Eve']

# Apply 10% raise to all Engineering employees
def apply_raise(employee, raise_pct=0.1):
    return {**employee, "salary": employee["salary"] * (1 + raise_pct)}

engineering_raised = list(map(
    lambda e: apply_raise(e) if e["dept"] == "Engineering" else e,
    employees
))
for emp in engineering_raised:
    print(f"{emp['name']}: {emp['salary']}")


# --- Pipeline 2: Text Processing Pipeline ---

text = "  Hello World   this IS a TEST   "

# Clean → split → filter → lowercase → sort
pipeline_result = sorted(
    filter(
        lambda w: len(w) > 3,
        map(
            lambda w: w.lower(),
            text.strip().split()
        )
    )
)
print(pipeline_result)    # ['hello', 'test', 'this', 'world']


# --- Pipeline 3: Number processing ---
# Given raw data: strings with possible spaces and non-numbers
# Keep valid numbers, convert to int, square them, sum if > 10

raw_data = ["3", " 7 ", "abc", "5", "2", " 9", "xyz", "4"]

result = reduce(
    lambda acc, x: acc + x,
    filter(
        lambda x: x > 10,
        map(
            lambda x: x**2,
            map(int,
                filter(
                    lambda x: x.strip().isdigit(),
                    raw_data
                )
            )
        )
    ),
    0
)
print(f"Sum of squares > 10: {result}")    # 49+25+81+16 = 171 (5²=25, 7²=49, 9²=81, 4²=16... filter >10)
```

---

### ✅ Practice 3: Demonstrating Scope

```python
# Counter using closure + nonlocal
def make_counter(start=0, step=1):
    """Factory function — creates a customizable counter."""
    count = start

    def counter():
        nonlocal count
        current = count
        count += step
        return current

    return counter

# Create independent counters
by_ones = make_counter()
by_fives = make_counter(0, 5)

print(by_ones())     # 0
print(by_ones())     # 1
print(by_ones())     # 2
print(by_fives())    # 0
print(by_fives())    # 5


# Logger using *args, **kwargs
def make_logger(prefix):
    def log(*args, level="INFO", **kwargs):
        message = " ".join(str(a) for a in args)
        extras = " ".join(f"{k}={v}" for k, v in kwargs.items())
        print(f"[{level}] [{prefix}] {message} {extras}".strip())
    return log

app_log = make_logger("APP")
db_log = make_logger("DB")

app_log("Server started", "on port 8000", level="INFO")
db_log("Query executed", duration="12ms", rows=42, level="DEBUG")
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What is `*args`?**  
A: It collects any number of extra positional arguments into a **tuple** inside the function. The `*` is what does the magic — `args` is just a name convention.

**Q: What is `**kwargs`?**  
A: It collects any number of extra keyword arguments into a **dict** inside the function.

**Q: What is the correct order of parameters?**  
A: `def func(regular, *args, keyword_only, **kwargs)` — positional first, then `*args`, then keyword-only, then `**kwargs`.

**Q: What is the mutable default argument bug?**  
A: Default values are evaluated once when the function is defined. Using a mutable object (like `[]` or `{}`) as a default means all calls share the same object. Fix: use `None` as default and create a new object inside the function.

**Q: What's the difference between `map` and list comprehension?**  
A: Both transform an iterable. List comprehensions are generally more Pythonic and readable. `map` is slightly faster in some cases and pairs well with existing functions (e.g., `map(int, strings)`).

**Q: What does `reduce` do?**  
A: It applies a function cumulatively to reduce an iterable to a single value. Example: `reduce(lambda x,y: x+y, [1,2,3,4])` → 10.

**Q: What is the LEGB rule?**  
A: Python looks up variables in this order: **Local → Enclosing → Global → Built-in**.

**Q: What's the difference between `global` and `nonlocal`?**  
A: `global` refers to the module-level (top-level) variable. `nonlocal` refers to the nearest enclosing function's variable (not global). Both allow modification of variables outside the current local scope.

**Q: Can a lambda have multiple lines?**  
A: No. Lambdas are restricted to a single expression. For multi-line logic, use a regular `def` function.

**Q: When should you NOT use lambda?**  
A: When the logic is complex, when you need statements (loops, try/except), or when a named function makes the code more readable.

---

## 📝 Key Takeaways

1. **`*args`** = extra positional args → collected as a **tuple**
2. **`**kwargs`** = extra keyword args → collected as a **dict**
3. **Mutable defaults are shared across calls** — always use `None` and create inside the function
4. **Lambda** = anonymous one-liner function — great for `map`, `filter`, `sorted` key
5. **`map(f, lst)`** = transform every element | **`filter(f, lst)`** = keep matching elements | **`reduce(f, lst)`** = combine into one
6. **LEGB rule**: Python searches Local → Enclosing → Global → Built-in
7. **`global`** = access/modify module-level variable from inside a function
8. **`nonlocal`** = access/modify enclosing function's variable from inner function
9. **Avoid `global`** in real code — pass values as arguments and return them
10. **Closures** let inner functions remember the enclosing function's variables even after it returns

---

*Day 2 Complete ✅ → Move to Day 3: OOP — Classes, Inheritance, Magic Methods*


----
----
----
----
----



# 📅 Day 3 — OOP: Object-Oriented Programming (High Priority)

> **Goal:** Master real-world object design  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: Classes & Objects

### 🔹 What is OOP? Why Use It?

**OOP (Object-Oriented Programming)** is a way of organizing code around **real-world entities** (objects) rather than just functions and logic.

**Why OOP?**
- Models real-world things naturally (User, BankAccount, Payment)
- Groups related data + behavior together
- Makes code reusable, maintainable, and scalable
- Easier to work in teams — each class is a self-contained unit

**The 4 Pillars of OOP:**
```
1. Encapsulation   → Bundle data + methods, hide internals
2. Inheritance     → Child class reuses parent class code
3. Polymorphism    → Same method name, different behavior
4. Abstraction     → Hide complexity, show only what's needed
```

---

### 🔹 Class vs Object

| Concept | What It Is | Real-World Analogy |
|---------|-----------|-------------------|
| **Class** | Blueprint / Template | Cookie cutter |
| **Object** | Instance of a class | Actual cookie |

```python
# Class = Blueprint
class Dog:
    # class body

# Object = Instance created from blueprint
my_dog = Dog()
your_dog = Dog()
# my_dog and your_dog are two separate objects from same blueprint
```

---

### 🔹 Creating a Class

```python
class Person:
    # Class variable — shared by ALL instances
    species = "Homo sapiens"

    # Constructor — called when object is created
    def __init__(self, name, age):
        # Instance variables — unique to each object
        self.name = name
        self.age = age

    # Instance method — works on the object
    def greet(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

    def have_birthday(self):
        self.age += 1
        return f"Happy birthday {self.name}! Now {self.age}."


# Creating objects (instances)
alice = Person("Alice", 25)
bob = Person("Bob", 30)

# Accessing attributes
print(alice.name)       # Alice
print(bob.age)          # 30

# Calling methods
print(alice.greet())    # Hi, I'm Alice and I'm 25 years old.
print(bob.have_birthday())  # Happy birthday Bob! Now 31.

# Class variable access
print(alice.species)    # Homo sapiens
print(Person.species)   # Homo sapiens (access via class too)
```

---

### 🔹 `self` — What Is It?

`self` refers to **the current object** calling the method.  
It's how the object talks to itself.

```python
class Counter:
    def __init__(self):
        self.count = 0      # self.count belongs to THIS object

    def increment(self):
        self.count += 1     # THIS object's count goes up

    def reset(self):
        self.count = 0

c1 = Counter()
c2 = Counter()

c1.increment()
c1.increment()
c2.increment()

print(c1.count)    # 2
print(c2.count)    # 1 — completely independent
```

> `self` is not a keyword — it's a convention. You could write `def greet(this)` and it would work. But always use `self`.

---

### 🔹 Class Variables vs Instance Variables

```python
class Employee:
    company = "TechCorp"       # Class variable — shared by all
    employee_count = 0         # Class variable — tracks total

    def __init__(self, name, salary):
        self.name = name           # Instance variable — unique
        self.salary = salary       # Instance variable — unique
        Employee.employee_count += 1  # Modify class variable

    def get_info(self):
        return f"{self.name} at {self.company}, salary: {self.salary}"


e1 = Employee("Alice", 90000)
e2 = Employee("Bob", 75000)
e3 = Employee("Charlie", 85000)

print(e1.get_info())         # Alice at TechCorp, salary: 90000
print(Employee.employee_count)  # 3

# Changing class variable via instance — creates instance variable!
e1.company = "StartupXYZ"    # Creates instance variable, doesn't affect class
print(e1.company)            # StartupXYZ
print(e2.company)            # TechCorp (unaffected)
print(Employee.company)      # TechCorp (unaffected)
```

---

### 🔹 Class Methods and Static Methods

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    # Regular instance method — needs self
    def to_fahrenheit(self):
        return (self.celsius * 9/5) + 32

    # Class method — works on the class, not instance
    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        celsius = (fahrenheit - 32) * 5/9
        return cls(celsius)    # cls = Temperature

    # Static method — no self, no cls — just a utility function
    @staticmethod
    def is_freezing(celsius):
        return celsius <= 0


# Instance method
t1 = Temperature(100)
print(t1.to_fahrenheit())       # 212.0

# Class method — alternative constructor
t2 = Temperature.from_fahrenheit(32)
print(t2.celsius)               # 0.0

# Static method — utility, no object needed
print(Temperature.is_freezing(-5))   # True
print(Temperature.is_freezing(25))   # False
```

---

## 📌 Topic 2: Inheritance (Single & Multiple)

### 🔹 What is Inheritance?

**Inheritance** allows a class (child) to **reuse** code from another class (parent).  
The child gets all the parent's attributes and methods automatically.

**Why?** Avoid code duplication. Model "is-a" relationships.

```
Animal (parent/base/super class)
  ├── Dog (child/derived/sub class)
  └── Cat (child/derived/sub class)

Dog "is-a" Animal ✅
```

---

### 🔹 Single Inheritance

```python
# Parent class
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

    def eat(self):
        return f"{self.name} is eating."

    def __str__(self):
        return f"{self.name} ({self.species})"


# Child class — inherits from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        # Call parent's __init__ to set up name and species
        super().__init__(name, species="Canis familiaris")
        self.breed = breed       # Dog-specific attribute

    # Override parent's method
    def speak(self):
        return f"{self.name} says: Woof!"

    # Dog-specific method
    def fetch(self):
        return f"{self.name} fetches the ball!"


class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, species="Felis catus")
        self.indoor = indoor

    def speak(self):
        return f"{self.name} says: Meow!"

    def purr(self):
        return f"{self.name} purrs..."


# Using them
dog = Dog("Rex", "Labrador")
cat = Cat("Whiskers")

print(dog.speak())    # Rex says: Woof!
print(cat.speak())    # Whiskers says: Meow!
print(dog.eat())      # Rex is eating. (inherited from Animal)
print(dog.fetch())    # Rex fetches the ball!
print(dog)            # Rex (Canis familiaris) (from __str__)

# Check relationships
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — dog is also an Animal
print(issubclass(Dog, Animal))  # True
```

---

### 🔹 `super()` — How and Why

`super()` gives you access to the **parent class** so you can call its methods.


```
class Parent:
    def show(self):
        print("This is Parent class")


class Child(Parent):
    def show(self):
        super().show()   # call Parent method
        print("This is Child class")


c = Child()
c.show()

# Output:
This is Parent class
This is Child class
```

```python
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def info(self):
        return f"{self.year} {self.make} {self.model}"

    def start(self):
        return "Vehicle starting..."


class ElectricCar(Vehicle):
    def __init__(self, make, model, year, battery_kwh):
        super().__init__(make, model, year)   # Call Vehicle's __init__
        self.battery_kwh = battery_kwh         # Electric-specific

    def info(self):
        # Extend parent's method, don't rewrite it
        base_info = super().info()
        return f"{base_info} (Electric, {self.battery_kwh}kWh)"

    def start(self):
        parent_start = super().start()
        return f"{parent_start} Silently. ⚡"


tesla = ElectricCar("Tesla", "Model 3", 2024, 75)
print(tesla.info())     # 2024 Tesla Model 3 (Electric, 75kWh)
print(tesla.start())    # Vehicle starting... Silently. ⚡
```

---

### 🔹 Multiple Inheritance

A class can inherit from **more than one parent**.

```python
class Flyable:
    def fly(self):
        return f"{self.__class__.__name__} is flying! 🛫"

    def describe(self):
        return "I can fly"


class Swimmable:
    def swim(self):
        return f"{self.__class__.__name__} is swimming! 🏊"

    def describe(self):
        return "I can swim"


# Duck inherits from BOTH
class Duck(Flyable, Swimmable):
    def __init__(self, name):
        self.name = name

    def quack(self):
        return f"{self.name} says: Quack!"


duck = Duck("Donald")
print(duck.fly())      # Duck is flying! 🛫
print(duck.swim())     # Duck is swimming! 🏊
print(duck.quack())    # Donald says: Quack!

# Which describe() is called?
print(duck.describe())  # "I can fly" — Flyable wins (listed first)
```

---

### 🔹 MRO — Method Resolution Order

When multiple parents have the same method, Python uses **MRO** to decide which one to call.  
MRO follows the **C3 linearization algorithm** — left to right, depth first.

```python
class A:
    def hello(self):
        return "Hello from A"

class B(A):
    def hello(self):
        return "Hello from B"

class C(A):
    def hello(self):
        return "Hello from C"

class D(B, C):
    pass


d = D()
print(d.hello())    # Hello from B — B comes before C in D(B, C)

# See the MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Or more readable
print([cls.__name__ for cls in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']










🔹 Why MRO is Needed

When multiple parent classes have the same method, Python needs to decide:
👉 which method to execute

🔹 Example
class A:
    def hello(self):
        return "Hello from A"

class B(A):
    def hello(self):
        return "Hello from B"

class C(A):
    def hello(self):
        return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.hello())   # Output: Hello from B
🔹 MRO Order
print(D.__mro__)

👉 Output:

(D, B, C, A, object)

👉 Readable:

print([cls.__name__ for cls in D.__mro__])
['D', 'B', 'C', 'A', 'object']
```

> **Rule:** Python checks left to right in the class definition `D(B, C)` → B checked first.

---

## 📌 Topic 3: Polymorphism

### 🔹 What is Polymorphism?

**Polymorphism** = "many forms"  
The same method name works **differently** depending on the object calling it.

**Why?** Write generic code that works with many types. No need to check `if type is Dog do this, if type is Cat do that`.

```
speak() on Dog → "Woof!"
speak() on Cat → "Meow!"
speak() on Duck → "Quack!"

Same method name → different behavior → Polymorphism
```

---

### 🔹 Method Overriding (Runtime Polymorphism)

```python
class Shape:
    def __init__(self, color="red"):
        self.color = color

    def area(self):
        raise NotImplementedError("Subclass must implement area()")

    def describe(self):
        return f"I am a {self.__class__.__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius, color="red"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height, color="blue"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base, height, color="green"):
        super().__init__(color)
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


# Polymorphism in action — same interface, different behavior
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

for shape in shapes:
    print(shape.describe())
# I am a Circle with area 78.54
# I am a Rectangle with area 24.00
# I am a Triangle with area 12.00

# Generic function — works with ANY shape
def total_area(shape_list):
    return sum(shape.area() for shape in shape_list)

print(f"Total area: {total_area(shapes):.2f}")   # Total area: 114.54
```

---

### 🔹 Duck Typing — Python's Natural Polymorphism

> "If it walks like a duck and quacks like a duck, it's a duck."

Python doesn't check the type — it checks if the object **has the method**.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Robot:
    def speak(self):
        return "BEEP BOOP"

class Person:
    def speak(self):
        return "Hello!"

# This function works with ANY object that has speak()
def make_speak(entity):
    print(entity.speak())

# No inheritance needed! Just needs speak()
animals = [Dog(), Cat(), Robot(), Person()]
for a in animals:
    make_speak(a)
# Woof!
# Meow!
# BEEP BOOP
# Hello!
```

---

### 🔹 Operator Overloading (Polymorphism on Operators)

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)      # Vector(4, 6)  — calls __add__
print(v1 * 3)       # Vector(3, 6)  — calls __mul__
```

---

## 📌 Topic 4: Encapsulation

### 🔹 What is Encapsulation?

**Encapsulation** = Bundling data (attributes) and methods together, and **controlling access** to them.

**Why?** 
- Protect data from accidental modification
- Hide internal implementation details
- Provide a clean public interface

**Three levels of access in Python:**

| Convention | Syntax | Meaning |
|-----------|--------|---------|
| Public | `self.name` | Anyone can access |
| Protected | `self._name` | "Please don't touch" (convention only) |
| Private | `self.__name` | Name-mangled, harder to access |

---

### 🔹 Public, Protected, Private

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner           # Public — anyone can access
        self._bank_name = "MyBank"   # Protected — internal use (convention)
        self.__balance = balance      # Private — name-mangled

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited {amount}. New balance: {self.__balance}"
        return "Invalid amount"

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrawn {amount}. New balance: {self.__balance}"
        return "Insufficient funds or invalid amount"

    def get_balance(self):          # Public method to safely read balance
        return self.__balance


acc = BankAccount("Alice", 1000)

print(acc.owner)              # Alice ✅ public
print(acc._bank_name)         # MyBank ✅ accessible but convention says don't
# print(acc.__balance)        # ❌ AttributeError

# Name mangling — Python renames __balance to _BankAccount__balance
print(acc._BankAccount__balance)  # 1000 (accessible but bad practice)

print(acc.deposit(500))       # Deposited 500. New balance: 1500
print(acc.withdraw(200))      # Withdrawn 200. New balance: 1300
print(acc.get_balance())      # 1300
```

---

### 🔹 `@property` — The Pythonic Way to Encapsulate

`@property` lets you define **getters, setters, and deleters** cleanly.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius    # protected

    @property
    def radius(self):
        """Getter — called when you access obj.radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter — called when you do obj.radius = value"""
        if value < 0:
            raise ValueError("Radius cannot be negative!")
        self._radius = value

    @radius.deleter
    def radius(self):
        """Deleter — called when you do del obj.radius"""
        print("Deleting radius...")
        del self._radius

    @property
    def area(self):
        """Read-only computed property"""
        import math
        return math.pi * self._radius ** 2

    @property
    def diameter(self):
        return self._radius * 2


c = Circle(5)

# Access like an attribute, but goes through getter
print(c.radius)     # 5
print(c.area)       # 78.53...
print(c.diameter)   # 10

# Set like an attribute, but goes through setter (with validation!)
c.radius = 10
print(c.radius)     # 10

# Validation works
try:
    c.radius = -5   # ❌ ValueError: Radius cannot be negative!
except ValueError as e:
    print(e)

# area is read-only — no setter defined
try:
    c.area = 100    # ❌ AttributeError: can't set attribute
except AttributeError as e:
    print(e)
```

---

### 🔹 Real-world Encapsulation Example

```python
class User:
    def __init__(self, username, email, password):
        self.username = username         # Public
        self.__email = email             # Private
        self.__password_hash = self.__hash_password(password)   # Private

    def __hash_password(self, password):
        """Private method — internal only."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        if "@" not in new_email:
            raise ValueError("Invalid email address!")
        self.__email = new_email

    def check_password(self, password):
        """Public interface to verify password — never expose hash."""
        return self.__hash_password(password) == self.__password_hash

    def change_password(self, old_password, new_password):
        if not self.check_password(old_password):
            raise PermissionError("Old password is wrong!")
        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters!")
        self.__password_hash = self.__hash_password(new_password)
        return "Password changed successfully!"

    def __str__(self):
        return f"User({self.username}, {self.__email})"


user = User("alice", "alice@example.com", "secret123")

print(user.username)              # alice ✅
print(user.email)                 # alice@example.com ✅ (via property)
# print(user.__email)             # ❌ AttributeError

print(user.check_password("secret123"))   # True
print(user.check_password("wrong"))       # False

print(user.change_password("secret123", "newsecret456"))
```

---

## 📌 Topic 5: Magic Methods (Dunder Methods)

### 🔹 What are Magic Methods?

Magic methods (also called **dunder methods** — double underscore) are special methods Python calls **automatically** in certain situations.

You don't call `obj.__str__()` — Python calls it when you do `print(obj)` or `str(obj)`.

---

### 🔹 `__init__` — Constructor

Called automatically when an object is **created**.

```python
class Book:
    def __init__(self, title, author, pages):
        print(f"Creating book: {title}")  # Called automatically
        self.title = title
        self.author = author
        self.pages = pages
        self.current_page = 0


b = Book("Python Crash Course", "Eric Matthes", 560)
# Output: Creating book: Python Crash Course
# Object is now ready to use
```

---

### 🔹 `__str__` vs `__repr__`

| Method | Called By | Purpose | Audience |
|--------|-----------|---------|----------|
| `__str__` | `print(obj)`, `str(obj)` | Human-readable string | End users |
| `__repr__` | `repr(obj)`, in REPL | Unambiguous representation | Developers |

```python
class Product:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

    def __str__(self):
        """For end users — pretty and readable."""
        return f"{self.name} — ₹{self.price:.2f} (Stock: {self.qty})"

    def __repr__(self):
        """For developers — shows how to recreate the object."""
        return f"Product(name={self.name!r}, price={self.price}, qty={self.qty})"


p = Product("Laptop", 75000, 10)

print(p)          # Laptop — ₹75000.00 (Stock: 10)    [__str__]
print(str(p))     # Laptop — ₹75000.00 (Stock: 10)    [__str__]
print(repr(p))    # Product(name='Laptop', price=75000, qty=10)  [__repr__]

# In a list — uses __repr__
products = [p]
print(products)   # [Product(name='Laptop', price=75000, qty=10)]
```

> **Rule:** Always define `__repr__`. Define `__str__` when you want a different user-facing format.

---

### 🔹 Comparison Magic Methods

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):    # ==
        return self.celsius == other.celsius

    def __lt__(self, other):    # <
        return self.celsius < other.celsius

    def __le__(self, other):    # <=
        return self.celsius <= other.celsius

    def __gt__(self, other):    # >
        return self.celsius > other.celsius

    def __str__(self):
        return f"{self.celsius}°C"


t1 = Temperature(100)
t2 = Temperature(50)
t3 = Temperature(100)

print(t1 == t3)    # True
print(t1 > t2)     # True
print(t2 < t1)     # True

# Now sortable!
temps = [Temperature(30), Temperature(10), Temperature(20)]
print(sorted(temps))    # [10°C, 20°C, 30°C]
```

---

### 🔹 Arithmetic Magic Methods

```python
class Money:
    def __init__(self, amount, currency="INR"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch!")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)

    def __str__(self):
        return f"{self.currency} {self.amount:,.2f}"

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"


m1 = Money(1000)
m2 = Money(500)

print(m1 + m2)     # INR 1,500.00
print(m1 - m2)     # INR 500.00
print(m1 * 1.1)    # INR 1,100.00
```

---

### 🔹 Container Magic Methods

```python
class ShoppingCart:
    def __init__(self):
        self.__items = []

    def add(self, item):
        self.__items.append(item)

    def __len__(self):          # len(cart)
        return len(self.__items)

    def __getitem__(self, index):   # cart[0]
        return self.__items[index]

    def __contains__(self, item):   # "apple" in cart
        return item in self.__items

    def __iter__(self):         # for item in cart
        return iter(self.__items)

    def __str__(self):
        return f"Cart({self.__items})"


cart = ShoppingCart()
cart.add("apple")
cart.add("banana")
cart.add("cherry")

print(len(cart))            # 3
print(cart[0])              # apple
print("banana" in cart)     # True
print("mango" in cart)      # False

for item in cart:
    print(item)             # apple, banana, cherry

print(cart)                 # Cart(['apple', 'banana', 'cherry'])
```

---

### 🔹 `__del__` — Destructor

Called when the object is about to be **garbage collected**.

```python
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        print(f"Connected to {db_name}")

    def __del__(self):
        print(f"Connection to {self.db_name} closed.")


conn = DatabaseConnection("users_db")    # Connected to users_db
del conn                                  # Connection to users_db closed.
```

---

### 🔹 `__call__` — Make Objects Callable

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor


double = Multiplier(2)
triple = Multiplier(3)

print(double(5))    # 10 — object called like a function!
print(triple(4))    # 12

print(callable(double))    # True
```

---

### 🔹 Complete Magic Methods Reference

| Method | Triggered By | Description |
|--------|-------------|-------------|
| `__init__` | `MyClass()` | Constructor |
| `__str__` | `print(obj)`, `str(obj)` | User-friendly string |
| `__repr__` | `repr(obj)`, REPL | Dev-friendly string |
| `__len__` | `len(obj)` | Length |
| `__getitem__` | `obj[key]` | Index/key access |
| `__setitem__` | `obj[key] = val` | Index/key assignment |
| `__contains__` | `x in obj` | Membership test |
| `__iter__` | `for x in obj` | Iteration |
| `__eq__` | `==` | Equality |
| `__lt__` | `<` | Less than |
| `__add__` | `+` | Addition |
| `__sub__` | `-` | Subtraction |
| `__mul__` | `*` | Multiplication |
| `__call__` | `obj()` | Callable object |
| `__del__` | `del obj` | Destructor |
| `__enter__` | `with obj:` | Context manager enter |
| `__exit__` | end of `with` block | Context manager exit |

---

## 🛠️ Practice 1: Design a Payment System

```python
from abc import ABC, abstractmethod
from datetime import datetime
import uuid


# ─── Base Payment Class ───────────────────────────────────────────────────────
class Payment(ABC):
    """Abstract base class for all payment types."""

    def __init__(self, amount, currency="INR"):
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        self.__amount = amount
        self.currency = currency
        self.transaction_id = str(uuid.uuid4())[:8].upper()
        self.timestamp = datetime.now()
        self.status = "PENDING"

    @property
    def amount(self):
        return self.__amount

    @abstractmethod
    def process(self):
        """Each payment type must implement this."""
        pass

    @abstractmethod
    def refund(self):
        """Each payment type must implement refund."""
        pass

    def get_receipt(self):
        return (
            f"─── Receipt ───────────────────\n"
            f"  TXN ID   : {self.transaction_id}\n"
            f"  Amount   : {self.currency} {self.amount:,.2f}\n"
            f"  Status   : {self.status}\n"
            f"  Time     : {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  Type     : {self.__class__.__name__}\n"
            f"───────────────────────────────"
        )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.transaction_id}, amount={self.amount}, status={self.status})"

    def __repr__(self):
        return f"{self.__class__.__name__}(amount={self.amount!r}, currency={self.currency!r})"


# ─── Credit Card Payment ─────────────────────────────────────────────────────
class CreditCardPayment(Payment):
    def __init__(self, amount, card_number, card_holder):
        super().__init__(amount)
        self.__card_number = card_number   # Private
        self.card_holder = card_holder
        self.__masked_card = f"****-****-****-{card_number[-4:]}"

    def process(self):
        # Simulate validation + processing
        if len(self.__card_number) != 16:
            self.status = "FAILED"
            return f"Payment FAILED: Invalid card number."
        print(f"Processing card {self.__masked_card}...")
        self.status = "SUCCESS"
        return f"✅ Card payment of {self.currency} {self.amount:,.2f} successful!"

    def refund(self):
        if self.status != "SUCCESS":
            return "Cannot refund — payment not successful."
        self.status = "REFUNDED"
        return f"♻️  Refund of {self.currency} {self.amount:,.2f} to {self.__masked_card} initiated."

    def __str__(self):
        return f"CreditCardPayment({self.__masked_card}, {self.currency} {self.amount:,.2f})"


# ─── UPI Payment ─────────────────────────────────────────────────────────────
class UPIPayment(Payment):
    def __init__(self, amount, upi_id):
        super().__init__(amount)
        self.upi_id = upi_id

    def process(self):
        if "@" not in self.upi_id:
            self.status = "FAILED"
            return "Payment FAILED: Invalid UPI ID."
        print(f"Sending payment request to {self.upi_id}...")
        self.status = "SUCCESS"
        return f"✅ UPI payment of {self.currency} {self.amount:,.2f} to {self.upi_id} successful!"

    def refund(self):
        if self.status != "SUCCESS":
            return "Cannot refund — payment not successful."
        self.status = "REFUNDED"
        return f"♻️  Refund of {self.currency} {self.amount:,.2f} to {self.upi_id} initiated."


# ─── Wallet Payment ───────────────────────────────────────────────────────────
class WalletPayment(Payment):
    def __init__(self, amount, wallet_balance):
        super().__init__(amount)
        self.__wallet_balance = wallet_balance

    def process(self):
        if self.__wallet_balance < self.amount:
            self.status = "FAILED"
            return f"Payment FAILED: Insufficient wallet balance ({self.__wallet_balance} available)."
        self.__wallet_balance -= self.amount
        self.status = "SUCCESS"
        return f"✅ Wallet payment of {self.currency} {self.amount:,.2f} successful! Remaining: {self.__wallet_balance:,.2f}"

    def refund(self):
        if self.status != "SUCCESS":
            return "Cannot refund — payment not successful."
        self.__wallet_balance += self.amount
        self.status = "REFUNDED"
        return f"♻️  Refund of {self.currency} {self.amount:,.2f} added back to wallet."


# ─── Payment Gateway (Orchestrator) ──────────────────────────────────────────
class PaymentGateway:
    def __init__(self):
        self.__transactions = []

    def pay(self, payment: Payment):
        """Polymorphism — same interface for all payment types."""
        result = payment.process()
        self.__transactions.append(payment)
        print(result)
        print(payment.get_receipt())
        return payment

    def get_history(self):
        print("\n─── Transaction History ──────────────")
        for txn in self.__transactions:
            print(f"  {txn}")
        print("──────────────────────────────────────")

    def total_collected(self):
        return sum(p.amount for p in self.__transactions if p.status == "SUCCESS")


# ─── Usage ────────────────────────────────────────────────────────────────────
gateway = PaymentGateway()

# Different payment methods — same process() interface (Polymorphism)
card = CreditCardPayment(5000, "1234567890123456", "Alice")
upi = UPIPayment(1500, "alice@upi")
wallet = WalletPayment(800, 2000)

gateway.pay(card)
gateway.pay(upi)
gateway.pay(wallet)

# Refund one
print(upi.refund())

gateway.get_history()
print(f"\nTotal collected: INR {gateway.total_collected():,.2f}")
```

---

## 🛠️ Practice 2: Design a User Service

```python
from datetime import datetime
from enum import Enum
import hashlib


# ─── Enums ────────────────────────────────────────────────────────────────────
class Role(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


# ─── Address (Value Object) ───────────────────────────────────────────────────
class Address:
    def __init__(self, street, city, state, pincode):
        self.street = street
        self.city = city
        self.state = state
        self.pincode = pincode

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} - {self.pincode}"

    def __repr__(self):
        return f"Address({self.city!r}, {self.state!r})"

    def __eq__(self, other):
        return (self.city == other.city and
                self.state == other.state and
                self.pincode == other.pincode)


# ─── Base User ────────────────────────────────────────────────────────────────
class BaseUser:
    _user_count = 0

    def __init__(self, username, email, password):
        self._validate_email(email)
        self._validate_password(password)

        BaseUser._user_count += 1
        self.id = BaseUser._user_count
        self.username = username
        self.__email = email
        self.__password_hash = self._hash(password)
        self.status = UserStatus.ACTIVE
        self.created_at = datetime.now()
        self.address = None
        self.login_count = 0

    @staticmethod
    def _hash(text):
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def _validate_email(email):
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError(f"Invalid email: {email}")

    @staticmethod
    def _validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters!")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        self._validate_email(new_email)
        self.__email = new_email

    def verify_password(self, password):
        return self._hash(password) == self.__password_hash

    def change_password(self, old_pass, new_pass):
        if not self.verify_password(old_pass):
            raise PermissionError("Incorrect current password!")
        self._validate_password(new_pass)
        self.__password_hash = self._hash(new_pass)
        return "Password updated successfully."

    def login(self, password):
        if self.status == UserStatus.BANNED:
            raise PermissionError("Account is banned!")
        if self.status == UserStatus.INACTIVE:
            raise PermissionError("Account is inactive!")
        if not self.verify_password(password):
            raise PermissionError("Invalid credentials!")
        self.login_count += 1
        return f"Welcome back, {self.username}! (Login #{self.login_count})"

    def set_address(self, street, city, state, pincode):
        self.address = Address(street, city, state, pincode)

    def deactivate(self):
        self.status = UserStatus.INACTIVE
        return f"User {self.username} deactivated."

    @classmethod
    def get_user_count(cls):
        return cls._user_count

    def __str__(self):
        return f"User(#{self.id} {self.username}, {self.__email}, {self.status.value})"

    def __repr__(self):
        return f"BaseUser(username={self.username!r}, email={self.__email!r})"

    def __eq__(self, other):
        return isinstance(other, BaseUser) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


# ─── Admin User ───────────────────────────────────────────────────────────────
class AdminUser(BaseUser):
    def __init__(self, username, email, password, department):
        super().__init__(username, email, password)
        self.role = Role.ADMIN
        self.department = department
        self.__managed_users = []

    def ban_user(self, user: BaseUser):
        if user == self:
            raise PermissionError("Admin cannot ban themselves!")
        user.status = UserStatus.BANNED
        return f"⛔ {user.username} has been banned by {self.username}."

    def unban_user(self, user: BaseUser):
        user.status = UserStatus.ACTIVE
        return f"✅ {user.username} has been unbanned."

    def add_managed_user(self, user: BaseUser):
        self.__managed_users.append(user)

    def get_managed_users(self):
        return self.__managed_users.copy()

    def __str__(self):
        return f"AdminUser(#{self.id} {self.username}, dept={self.department})"


# ─── Editor User ──────────────────────────────────────────────────────────────
class EditorUser(BaseUser):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self.role = Role.EDITOR
        self.__posts = []

    def create_post(self, title, content):
        post = {"title": title, "content": content, "created_at": datetime.now()}
        self.__posts.append(post)
        return f"📝 Post '{title}' created by {self.username}."

    def get_posts(self):
        return self.__posts.copy()

    def __str__(self):
        return f"EditorUser(#{self.id} {self.username}, posts={len(self.__posts)})"


# ─── User Service ─────────────────────────────────────────────────────────────
class UserService:
    """Manages all users — create, find, delete, report."""

    def __init__(self):
        self.__users = {}

    def register(self, user: BaseUser):
        if user.username in self.__users:
            raise ValueError(f"Username '{user.username}' already taken!")
        self.__users[user.username] = user
        print(f"✅ Registered: {user}")
        return user

    def find_by_username(self, username):
        user = self.__users.get(username)
        if not user:
            raise LookupError(f"User '{username}' not found.")
        return user

    def delete_user(self, username):
        if username not in self.__users:
            raise LookupError(f"User '{username}' not found.")
        del self.__users[username]
        return f"🗑️  User '{username}' deleted."

    def list_users(self):
        print("\n─── All Users ──────────────────────")
        for user in self.__users.values():
            print(f"  {user}")
        print(f"  Total: {len(self.__users)} users")
        print("────────────────────────────────────")

    def get_active_users(self):
        return [u for u in self.__users.values() if u.status == UserStatus.ACTIVE]

    def __len__(self):
        return len(self.__users)

    def __contains__(self, username):
        return username in self.__users


# ─── Usage ────────────────────────────────────────────────────────────────────
service = UserService()

# Create users
admin = AdminUser("superadmin", "admin@app.com", "admin1234", "Engineering")
alice = EditorUser("alice99", "alice@app.com", "alicepass")
bob = BaseUser("bob_viewer", "bob@app.com", "bobpass99")

# Register all
service.register(admin)
service.register(alice)
service.register(bob)

# Login
print(alice.login("alicepass"))
print(bob.login("bobpass99"))

# Create post
print(alice.create_post("OOP in Python", "OOP stands for..."))

# Set address
alice.set_address("123 MG Road", "Bengaluru", "Karnataka", "560001")
print(f"Alice's address: {alice.address}")

# Admin actions
print(admin.ban_user(bob))
try:
    bob.login("bobpass99")
except PermissionError as e:
    print(f"❌ {e}")

print(admin.unban_user(bob))

# Service features
service.list_users()
print(f"alice99 in service: {'alice99' in service}")  # __contains__
print(f"Total users: {len(service)}")                  # __len__
print(f"Total ever created: {BaseUser.get_user_count()}")

# Find and update
found = service.find_by_username("alice99")
found.email = "newalice@app.com"
print(f"Updated email: {found.email}")
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What are the 4 pillars of OOP?**  
A: **Encapsulation** (bundle + hide data), **Inheritance** (reuse parent code), **Polymorphism** (same interface, different behavior), **Abstraction** (hide complexity, show only essentials).

**Q: What is the difference between a class and an object?**  
A: A class is a **blueprint** (template). An object is a **concrete instance** created from that blueprint. A class defines structure; an object holds actual data.

**Q: What does `super()` do?**  
A: It gives access to the **parent class**, allowing you to call its methods from the child class — most commonly in `__init__` to initialize the parent part of the object.

**Q: What is MRO and why does it matter?**  
A: Method Resolution Order — the order Python searches for a method in multiple inheritance. It follows C3 linearization (left to right, then up). Check it with `ClassName.__mro__`.

**Q: What is the difference between `__str__` and `__repr__`?**  
A: `__str__` is for **end users** — human-readable output for `print()`. `__repr__` is for **developers** — unambiguous, ideally showing how to recreate the object. If only one is defined, `__repr__` is used as fallback.

**Q: What is encapsulation?**  
A: Bundling data and methods together and controlling access. In Python, `_name` = protected (convention), `__name` = private (name-mangled). Use `@property` for clean getter/setter with validation.

**Q: What is polymorphism?**  
A: Same method name, different behavior depending on the object. Achieved through method overriding. Python also supports duck typing — if it has the method, it can be used, regardless of type.

**Q: What is duck typing?**  
A: Python doesn't check the type of an object — it checks if the object has the method or attribute needed. "If it walks like a duck and quacks like a duck, it's a duck."

**Q: When would you use `@classmethod` vs `@staticmethod`?**  
A: `@classmethod` receives `cls` and is used for alternative constructors or class-level operations. `@staticmethod` receives neither `self` nor `cls` — it's just a utility function that logically belongs in the class.

**Q: What is name mangling?**  
A: When you use `__attr` (double underscore prefix), Python renames it to `_ClassName__attr`. This makes it harder (but not impossible) to access from outside the class.

---

## 📝 Key Takeaways

1. **Class = blueprint, Object = instance** — use `self` to refer to the current object
2. **`__init__`** is the constructor — runs automatically when object is created
3. **Inheritance** uses `super()` to call the parent — always call `super().__init__()` in child
4. **MRO** controls method lookup in multiple inheritance — left to right (`Class.__mro__` to debug)
5. **Polymorphism** = same method name, different behavior — enables generic code
6. **Duck typing** = Python cares about behavior (methods), not types
7. **Encapsulation** — use `_protected`, `__private`, and `@property` for controlled access
8. **`__str__`** = pretty for users | **`__repr__`** = precise for developers — always define `__repr__`
9. **Magic methods** let your objects behave like built-in types (`+`, `len()`, `in`, `[]`)
10. **`@classmethod`** = alternative constructor | **`@staticmethod`** = utility in the class namespace

---

*Day 3 Complete ✅ → Move to Day 4: Advanced Python — Decorators, Generators, Closures*





---
---
---
---
---
---
---
---



# 📅 Day 4 — Advanced Python
> **Goal:** Stand out from other candidates  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: Closures

> Closures come BEFORE decorators because decorators are built ON TOP of closures. Understanding closures first makes decorators obvious.

### 🔹 What is a Closure?

A **closure** is a function that **remembers the variables from its enclosing scope** even after that scope has finished executing.

Three conditions for a closure:
1. There must be a **nested function** (function inside a function)
2. The inner function must **refer to a variable** from the outer function
3. The outer function must **return the inner function**

```python
# Simple closure example
def outer(message):
    # 'message' is a free variable — lives in enclosing scope
    def inner():
        print(message)   # inner remembers 'message'
    return inner         # return the function, not the result

# outer() has finished executing...
# but inner still remembers 'message'
say_hello = outer("Hello, World!")
say_bye   = outer("Goodbye!")

say_hello()    # Hello, World!
say_bye()      # Goodbye!

# Proof it remembers
print(say_hello.__closure__)                        # (<cell at 0x...>,)
print(say_hello.__closure__[0].cell_contents)       # Hello, World!
```

---

### 🔹 Why Closures Matter — The Real Use Cases

```python
# Use Case 1: Function factories — generate customized functions
def make_multiplier(factor):
    def multiply(number):
        return number * factor    # 'factor' is remembered
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
times10 = make_multiplier(10)

print(double(5))    # 10
print(triple(5))    # 15
print(times10(5))   # 50

# Each function is independent with its own 'factor'
print(double.__closure__[0].cell_contents)   # 2
print(triple.__closure__[0].cell_contents)   # 3
```

```python
# Use Case 2: Maintaining state without a class
def make_counter(start=0):
    count = [start]   # mutable list so we can modify it

    def increment(step=1):
        count[0] += step
        return count[0]

    def decrement(step=1):
        count[0] -= step
        return count[0]

    def reset():
        count[0] = start
        return count[0]

    def get():
        return count[0]

    return increment, decrement, reset, get

inc, dec, rst, get = make_counter(10)

print(inc())      # 11
print(inc())      # 12
print(inc(5))     # 17
print(dec(3))     # 14
print(rst())      # 10
print(get())      # 10
```

```python
# Use Case 3: Partial application — pre-fill some arguments
def make_power(exponent):
    def power(base):
        return base ** exponent
    return power

square = make_power(2)
cube   = make_power(3)

print(square(4))    # 16
print(cube(3))      # 27
print(list(map(square, [1, 2, 3, 4, 5])))  # [1, 4, 9, 16, 25]
```

---

### 🔹 Closure with `nonlocal`

```python
def make_accumulator():
    total = 0

    def add(value):
        nonlocal total      # modify the enclosing variable
        total += value
        return total

    return add

acc = make_accumulator()
print(acc(10))    # 10
print(acc(20))    # 30
print(acc(5))     # 35
```

---

### 🔹 Common Closure Gotcha — Loop Variables

```python
# ❌ BUG — all closures capture the SAME variable 'i'
funcs = []
for i in range(5):
    funcs.append(lambda: i)   # all capture 'i', not its current value

print([f() for f in funcs])   # [4, 4, 4, 4, 4] ← all see final i=4

# ✅ FIX 1 — use default argument to capture current value
funcs = []
for i in range(5):
    funcs.append(lambda x=i: x)   # x=i captures value at creation time

print([f() for f in funcs])   # [0, 1, 2, 3, 4] ✅

# ✅ FIX 2 — use a factory function
def make_func(i):
    def func():
        return i
    return func

funcs = [make_func(i) for i in range(5)]
print([f() for f in funcs])   # [0, 1, 2, 3, 4] ✅
```

---

## 📌 Topic 2: Decorators

### 🔹 What is a Decorator?

A **decorator** is a function that **wraps another function** to extend or modify its behavior — without changing its source code.

**Why?**
- Add logging, timing, authentication, caching to any function
- Separation of concerns — keep business logic clean
- DRY — apply same behavior to many functions with one line

**Core idea:** A decorator is just a closure that takes a function as input.

```
@decorator
def my_func():
    ...

# This is EXACTLY the same as:
def my_func():
    ...
my_func = decorator(my_func)
```

---

### 🔹 Building a Decorator Step by Step

```python
# Step 1: A normal function
def greet():
    print("Hello!")

# Step 2: A function that wraps another
def my_decorator(func):
    def wrapper():
        print("Before the function")
        func()
        print("After the function")
    return wrapper

# Step 3: Apply manually
greet = my_decorator(greet)
greet()
# Before the function
# Hello!
# After the function

# Step 4: Use @syntax (syntactic sugar for the same thing)
@my_decorator
def greet():
    print("Hello!")

greet()
# Same output!
```

---

### 🔹 Decorator with Arguments — Using `*args, **kwargs`

```python
# This decorator works on ANY function regardless of its parameters
def my_decorator(func):
    def wrapper(*args, **kwargs):      # accept any arguments
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)  # pass them through
        print(f"Done with {func.__name__}")
        return result                   # return the result!
    return wrapper


@my_decorator
def add(a, b):
    return a + b

@my_decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(add(3, 4))              # Calling add → 7 → Done
print(greet("Alice"))         # Calling greet → Hello, Alice! → Done
```

---

### 🔹 `functools.wraps` — Preserve Function Identity

```python
import functools

# ❌ Without @wraps — function loses its identity
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """This is my function."""
    pass

print(my_func.__name__)    # wrapper  ← WRONG!
print(my_func.__doc__)     # None     ← WRONG!


# ✅ With @wraps — identity preserved
def good_decorator(func):
    @functools.wraps(func)          # copies __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_func():
    """This is my function."""
    pass

print(my_func.__name__)    # my_func  ✅
print(my_func.__doc__)     # This is my function. ✅
```

> **Always use `@functools.wraps(func)` inside your decorators.** It's a best practice.

---

### 🔹 Decorators with Parameters

What if the decorator itself needs arguments? You need **one more layer of nesting**.

```python
import functools

# Decorator factory — returns a decorator
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)
def say(message):
    print(message)

say("Hello!")
# Hello!
# Hello!
# Hello!


# Another example — access control
def require_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(f"Requires role: {role}. Got: {user.get('role')}")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_role("admin")
def delete_user(user, target_id):
    return f"User {target_id} deleted by {user['name']}"


admin = {"name": "Alice", "role": "admin"}
guest = {"name": "Bob",   "role": "viewer"}

print(delete_user(admin, 42))    # User 42 deleted by Alice
try:
    delete_user(guest, 42)       # PermissionError: Requires role: admin
except PermissionError as e:
    print(e)
```

---

### 🔹 Stacking Multiple Decorators


```

# @functools.wraps(func) — Simple Explanation

## 🧠 What is it?

`@functools.wraps(func)` is used inside decorators to **preserve the original function’s identity** when it is wrapped by another function.

---

## ❗ Problem without `wraps`

When we use a decorator, the original function is replaced by an inner wrapper function.

### Example:
```python
def decorator(func):
    def wrapper():
        return func()
    return wrapper

@decorator
def greet():
    """Say hello"""
    return "Hello"

print(greet.__name__)  # wrapper ❌
print(greet.__doc__)   # None ❌



=============== sol=====================

import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper():
        return func()
    return wrapper

@decorator
def greet():
    """Say hello"""
    return "Hello"

print(greet.__name__)  # greet ✅
print(greet.__doc__)   # Say hello ✅

```




```python
import functools

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

def underline(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper


@bold
@italic
@underline
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
# <b><i><u>Hello, Alice!</u></i></b>

# Decorators apply BOTTOM UP:
# underline(greet) first → italic(that) → bold(that)
# But execution is TOP DOWN:
# bold's wrapper runs → calls italic's wrapper → calls underline's wrapper → calls greet
```

---

### 🔹 Class-Based Decorators

```python
import functools

class CountCalls:
    """Decorator that counts how many times a function is called."""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} time(s)")
        return self.func(*args, **kwargs)


@CountCalls
def say_hello():
    print("Hello!")

say_hello()    # say_hello called 1 time(s) → Hello!
say_hello()    # say_hello called 2 time(s) → Hello!
say_hello()    # say_hello called 3 time(s) → Hello!
print(say_hello.count)    # 3
```

---

## 📌 Topic 3: Iterators vs Iterables

### 🔹 What is an Iterable?

An **iterable** is any object you can loop over with `for`.  
It implements `__iter__()` which returns an **iterator**.

```python
# These are all iterables:
for x in [1, 2, 3]:     pass   # list
for x in (1, 2, 3):     pass   # tuple
for x in {1, 2, 3}:     pass   # set
for x in {"a": 1}:      pass   # dict (iterates keys)
for x in "hello":        pass   # string
for x in range(5):       pass   # range
```

---

### 🔹 What is an Iterator?

An **iterator** is an object that:
1. Implements `__iter__()` — returns itself
2. Implements `__next__()` — returns the next value, raises `StopIteration` when done

```python
# Get an iterator from an iterable
my_list = [1, 2, 3]
my_iter = iter(my_list)    # calls my_list.__iter__()

print(next(my_iter))    # 1   — calls my_iter.__next__()
print(next(my_iter))    # 2
print(next(my_iter))    # 3
print(next(my_iter))    # StopIteration! ← exhausted

# for loop does this automatically:
# 1. calls iter() to get iterator
# 2. calls next() repeatedly
# 3. catches StopIteration to stop
```

---

### 🔹 Iterable vs Iterator — The Difference

| | Iterable | Iterator |
|---|----------|----------|
| Has `__iter__` | ✅ returns iterator | ✅ returns self |
| Has `__next__` | ❌ | ✅ |
| Can loop multiple times | ✅ fresh each time | ❌ one-time use |
| Examples | list, tuple, str, dict | `iter(list)`, `map()`, `filter()`, `zip()` |

```python
my_list = [1, 2, 3]

# Iterable — can loop multiple times
for x in my_list: pass
for x in my_list: pass   # works fine

# Iterator — one-time use
my_iter = iter(my_list)
for x in my_iter: pass
for x in my_iter: pass   # prints nothing — already exhausted!

# An iterator is also an iterable (has both __iter__ and __next__)
print(hasattr(my_list, '__iter__'))    # True
print(hasattr(my_list, '__next__'))    # False ← list is NOT an iterator

print(hasattr(my_iter, '__iter__'))    # True
print(hasattr(my_iter, '__next__'))    # True ← iterator has both
```

---

### 🔹 Building a Custom Iterator

```python
class CountUp:
    """Iterator that counts from start to end."""

    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self     # iterator returns itself

    def __next__(self):
        if self.current > self.end:
            raise StopIteration   # signal: we're done
        value = self.current
        self.current += 1
        return value


counter = CountUp(1, 5)
for num in counter:
    print(num, end=" ")    # 1 2 3 4 5

# Also works with next()
counter2 = CountUp(10, 12)
print(next(counter2))    # 10
print(next(counter2))    # 11
print(next(counter2))    # 12
# print(next(counter2))  # StopIteration


# Infinite iterator
class InfiniteCounter:
    def __init__(self, start=0):
        self.n = start

    def __iter__(self):
        return self

    def __next__(self):
        value = self.n
        self.n += 1
        return value

counter = InfiniteCounter()
# Take only first 5
import itertools
print(list(itertools.islice(counter, 5)))   # [0, 1, 2, 3, 4]
```

---

## 📌 Topic 4: Generators

### 🔹 What is a Generator?

A **generator** is a special function that **yields values one at a time** instead of returning all values at once.

- Uses `yield` instead of `return`
- **Lazy evaluation** — values are produced only when needed
- **Memory efficient** — doesn't store all values in memory
- Returns a **generator object** (which is an iterator)

```python
# Regular function — creates entire list in memory
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result    # all 1 million values in memory at once!

# Generator function — produces one value at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2   # produces one, pauses, resumes next call

# Memory difference
import sys
lst = get_squares_list(1_000_000)
gen = get_squares_gen(1_000_000)

print(sys.getsizeof(lst))   # ~8.5 MB
print(sys.getsizeof(gen))   # ~120 bytes ← virtually nothing!
```

---

### 🔹 How `yield` Works Internally

```python
def step_by_step():
    print("Step 1: before first yield")
    yield 1
    print("Step 2: between yields")
    yield 2
    print("Step 3: before last yield")
    yield 3
    print("Step 4: after last yield — function ends")


gen = step_by_step()
print("Generator created, nothing runs yet.")

print(next(gen))
# Step 1: before first yield
# 1

print(next(gen))
# Step 2: between yields
# 2

print(next(gen))
# Step 3: before last yield
# 3

# print(next(gen))
# Step 4: after last yield — function ends
# StopIteration!
```

> **Key insight:** When `yield` is hit, the function **pauses** and saves its entire state (local variables, where it stopped). The next `next()` call **resumes from where it left off**.

---

### 🔹 Generator Expressions

Like list comprehensions but with `()` — lazy, memory efficient.

```python
# List comprehension — creates full list in memory
squares_list = [x**2 for x in range(10)]

# Generator expression — lazy, creates one at a time
squares_gen = (x**2 for x in range(10))

print(type(squares_list))   # <class 'list'>
print(type(squares_gen))    # <class 'generator'>

# Use in a for loop
for sq in squares_gen:
    print(sq, end=" ")      # 0 1 4 9 16 25 36 49 64 81

# Use in functions that accept iterables
total = sum(x**2 for x in range(10))    # no extra () needed inside sum()
print(total)    # 285

# Filter with condition
evens = list(x for x in range(20) if x % 2 == 0)
print(evens)    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

---

### 🔹 `yield from` — Delegating to Sub-generators

```python
# Without yield from
def chain_manual(*iterables):
    for iterable in iterables:
        for item in iterable:
            yield item

# With yield from (cleaner)
def chain(*iterables):
    for iterable in iterables:
        yield from iterable    # delegate to sub-iterable

result = list(chain([1, 2], [3, 4], [5, 6]))
print(result)    # [1, 2, 3, 4, 5, 6]


# Recursive generator with yield from
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # recurse into nested list
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(data)))    # [1, 2, 3, 4, 5, 6, 7]
```

---

### 🔹 Sending Values to a Generator

```python
# Generators can also RECEIVE values via send()
def accumulator():
    total = 0
    while True:
        value = yield total    # yield sends 'total' out, receives 'value' in
        if value is None:
            break
        total += value


gen = accumulator()
next(gen)           # Prime the generator (advance to first yield)
print(gen.send(10))   # 10
print(gen.send(20))   # 30
print(gen.send(5))    # 35
```

---

### 🔹 Generators for Large Datasets — Real Use Cases

```python
import os

# Use Case 1: Read large file line by line (no loading entire file)
def read_large_file(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

# Use Case 2: Generate infinite Fibonacci sequence
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)    # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# Use Case 3: Paginated API data
def fetch_users_paginated(total_users, page_size=100):
    """Simulate fetching users page by page."""
    for offset in range(0, total_users, page_size):
        # In reality: response = requests.get(f"/users?offset={offset}&limit={page_size}")
        batch = [f"user_{i}" for i in range(offset, min(offset + page_size, total_users))]
        print(f"Fetched page: offset={offset}")
        yield from batch

# Process 1000 users without loading all into memory
for user in fetch_users_paginated(250, page_size=100):
    pass   # process user
    # Only 100 users in memory at a time


# Use Case 4: Data pipeline
def read_csv_rows(filename):
    """Read CSV rows lazily."""
    with open(filename) as f:
        headers = next(f).strip().split(",")
        for line in f:
            values = line.strip().split(",")
            yield dict(zip(headers, values))

def filter_rows(rows, key, value):
    for row in rows:
        if row.get(key) == value:
            yield row

def transform_rows(rows, transform_fn):
    for row in rows:
        yield transform_fn(row)

# Pipeline: read → filter → transform (all lazy)
# rows = read_csv_rows("data.csv")
# active = filter_rows(rows, "status", "active")
# processed = transform_rows(active, lambda r: {**r, "name": r["name"].upper()})
# for row in processed: save_to_db(row)
```

---

## 📌 Topic 5: Context Managers (`with` statement)

### 🔹 What is a Context Manager?

A **context manager** manages resources — ensuring setup and teardown happen correctly even if an error occurs.

**Why?** Resources like files, DB connections, locks — must always be closed/released, even when exceptions occur.

```python
# Without context manager — risky!
f = open("data.txt", "w")
f.write("hello")
# If an exception happens here, f.close() never runs → resource leak!
f.close()

# With context manager — safe!
with open("data.txt", "w") as f:
    f.write("hello")
    # Even if exception here, file is ALWAYS closed
# File is automatically closed here
```

---

### 🔹 How `with` Works Internally

The `with` statement calls two magic methods:
- `__enter__()` — setup, runs when entering the `with` block
- `__exit__()` — teardown, runs when exiting (even on exception)

```python
# What Python does with "with obj as x:"
# 1. calls obj.__enter__() → assigns result to x
# 2. runs the with block
# 3. calls obj.__exit__() → no matter what (exception or not)
```

---

### 🔹 Building a Context Manager with a Class

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file      # this is what 'as f' gets

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()

        # exc_type, exc_value, traceback are filled if exception occurred
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        return False   # False = don't suppress the exception
                       # True  = suppress it (rarely do this)


with FileManager("test.txt", "w") as f:
    f.write("Hello, context manager!")
    print("Writing complete")
# Opening test.txt
# Writing complete
# Closing test.txt


# Exception handling
with FileManager("test.txt", "r") as f:
    content = f.read()
    raise ValueError("Something went wrong!")
# Opening test.txt
# Closing test.txt          ← still closes!
# Exception occurred: Something went wrong!
# ValueError: Something went wrong!  ← still raised (return False)
```

---

### 🔹 Building a Context Manager with `contextlib`

`contextlib.contextmanager` lets you write a context manager as a generator — much simpler.

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label=""):
    """Context manager that times a block of code."""
    start = time.perf_counter()
    try:
        yield           # code inside the with block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] Elapsed: {elapsed:.4f}s")


with timer("sorting"):
    data = list(range(1_000_000, 0, -1))
    data.sort()
# [sorting] Elapsed: 0.0821s


@contextmanager
def managed_db_connection(db_url):
    """Simulate DB connection management."""
    print(f"Connecting to {db_url}...")
    connection = {"url": db_url, "open": True}  # simulate connection
    try:
        yield connection
    except Exception as e:
        print(f"Rolling back transaction: {e}")
        connection["open"] = False
        raise
    finally:
        print(f"Closing connection to {db_url}")
        connection["open"] = False


with managed_db_connection("postgresql://localhost/mydb") as conn:
    print(f"Connection open: {conn['open']}")
    # do database work here
# Connecting to postgresql://localhost/mydb
# Connection open: True
# Closing connection to postgresql://localhost/mydb
```

---

### 🔹 Context Manager Rules — `__exit__` Parameters

```python
class ErrorHandler:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # exc_type  → the exception class (e.g., ValueError)
        # exc_value → the exception instance
        # traceback → the traceback object
        # All three are None if no exception occurred

        if exc_type is None:
            print("No exception — all good!")
            return False

        if exc_type is ValueError:
            print(f"Caught ValueError: {exc_value} — suppressing it")
            return True   # ← suppress the exception!

        print(f"Unknown exception {exc_type.__name__} — re-raising")
        return False      # ← re-raise it


with ErrorHandler():
    print("doing work")
    raise ValueError("bad value")    # suppressed!
# doing work
# Caught ValueError: bad value — suppressing it
# (no exception raised)

with ErrorHandler():
    print("no problem here")
# no problem here
# No exception — all good!
```

---

### 🔹 Nested Context Managers

```python
# Multiple context managers on one line
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        outfile.write(line.upper())

# Reentrant context managers
from contextlib import contextmanager

@contextmanager
def indent(level=1):
    prefix = "  " * level
    print(f"{prefix}Enter")
    yield prefix
    print(f"{prefix}Exit")

with indent(1) as p1:
    print(f"{p1}Working at level 1")
    with indent(2) as p2:
        print(f"{p2}Working at level 2")
```

---

### 🔹 `contextlib` Utilities

```python
from contextlib import suppress, nullcontext

# suppress — silently ignore specific exceptions
with suppress(FileNotFoundError):
    open("nonexistent_file.txt")
    # No exception raised — FileNotFoundError is suppressed

# nullcontext — no-op context manager (useful in conditionals)
def process(data, lock=None):
    context = lock if lock is not None else nullcontext()
    with context:
        # process data — works with or without a lock
        return [x * 2 for x in data]
```

---

## 🛠️ Practice 1: Custom Decorators — Logging & Timing

```python
import functools
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
logger = logging.getLogger(__name__)


# ─── 1. Timing Decorator ─────────────────────────────────────────────────────
def timer(func):
    """Measures execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        print(f"⏱  {func.__name__}() took {elapsed:.3f}ms")
        return result
    return wrapper


# ─── 2. Logger Decorator ─────────────────────────────────────────────────────
def log_calls(func):
    """Logs function calls with arguments and return value."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args = ", ".join(args_repr + kwargs_repr)
        logger.info(f"→ Calling {func.__name__}({all_args})")
        try:
            result = func(*args, **kwargs)
            logger.info(f"← {func.__name__} returned {result!r}")
            return result
        except Exception as e:
            logger.error(f"✗ {func.__name__} raised {type(e).__name__}: {e}")
            raise
    return wrapper


# ─── 3. Retry Decorator ──────────────────────────────────────────────────────
def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Retries a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"⚠  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            print(f"✗ All {max_attempts} attempts failed.")
            raise last_exception
        return wrapper
    return decorator


# ─── 4. Cache Decorator (memoization) ────────────────────────────────────────
def memoize(func):
    """Cache function results — avoid recomputing same inputs."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    wrapper.cache = cache    # expose cache for inspection
    return wrapper


# ─── 5. Validate Types Decorator ─────────────────────────────────────────────
def validate_types(**expected_types):
    """Validate argument types at runtime."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for param_name, value in bound.arguments.items():
                if param_name in expected_types:
                    expected = expected_types[param_name]
                    if not isinstance(value, expected):
                        raise TypeError(
                            f"Argument '{param_name}' must be {expected.__name__}, "
                            f"got {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ─── Using the decorators ─────────────────────────────────────────────────────

@timer
@log_calls
def compute_sum(n):
    """Sum of first n numbers."""
    return sum(range(n))

print(compute_sum(1_000_000))


@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))    # 12586269025 — fast because of memoization
print(fibonacci.cache)  # see the cache


attempt_count = 0

@retry(max_attempts=3, delay=0, exceptions=(ValueError,))
def unreliable_function():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ValueError(f"Simulated failure #{attempt_count}")
    return "Success on attempt 3!"

print(unreliable_function())


@validate_types(name=str, age=int, salary=float)
def create_employee(name, age, salary):
    return f"Employee: {name}, {age}, {salary}"

print(create_employee("Alice", 30, 75000.0))   # works
try:
    create_employee("Bob", "thirty", 75000.0)  # TypeError!
except TypeError as e:
    print(e)
```

---

## 🛠️ Practice 2: Generators for Large Datasets

```python
import random
import time
from typing import Generator, Iterator


# ─── 1. Large Dataset Generator ──────────────────────────────────────────────
def generate_transactions(count: int) -> Generator:
    """Generate transaction records lazily — no memory buildup."""
    categories = ["food", "transport", "shopping", "utilities", "entertainment"]
    for i in range(count):
        yield {
            "id": f"TXN{i:08d}",
            "amount": round(random.uniform(10, 10000), 2),
            "category": random.choice(categories),
            "timestamp": time.time() - random.randint(0, 86400 * 30),
        }


# ─── 2. Pipeline of Generators ───────────────────────────────────────────────
def filter_by_category(transactions, category):
    for txn in transactions:
        if txn["category"] == category:
            yield txn

def filter_by_amount(transactions, min_amount=0, max_amount=float("inf")):
    for txn in transactions:
        if min_amount <= txn["amount"] <= max_amount:
            yield txn

def enrich_transaction(transactions):
    """Add computed fields lazily."""
    for txn in transactions:
        yield {
            **txn,
            "tax": round(txn["amount"] * 0.18, 2),
            "total": round(txn["amount"] * 1.18, 2),
            "is_large": txn["amount"] > 5000,
        }

def batch_transactions(transactions, batch_size=100):
    """Group into batches for bulk processing."""
    batch = []
    for txn in transactions:
        batch.append(txn)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch   # yield remaining


# ─── Build the pipeline ───────────────────────────────────────────────────────
print("Building lazy pipeline...")
raw              = generate_transactions(1_000_000)      # 1 million rows — lazy!
food_txns        = filter_by_category(raw, "food")
big_food         = filter_by_amount(food_txns, min_amount=1000)
enriched         = enrich_transaction(big_food)
batches          = batch_transactions(enriched, batch_size=50)

# Process — only pulls data as needed
total_amount = 0
total_tax    = 0
count        = 0

for batch in batches:
    for txn in batch:
        total_amount += txn["amount"]
        total_tax    += txn["tax"]
        count        += 1
    if count > 500:   # stop early for demo
        break

print(f"Processed {count} large food transactions")
print(f"Total amount : ₹{total_amount:,.2f}")
print(f"Total tax    : ₹{total_tax:,.2f}")


# ─── 3. Infinite Sequence Generators ─────────────────────────────────────────
def primes() -> Iterator[int]:
    """Infinite prime number generator using Sieve."""
    yield 2
    found = [2]
    candidate = 3
    while True:
        if all(candidate % p != 0 for p in found):
            found.append(candidate)
            yield candidate
        candidate += 2

prime_gen = primes()
first_20_primes = [next(prime_gen) for _ in range(20)]
print(f"First 20 primes: {first_20_primes}")


# ─── 4. Generator with Context Manager ───────────────────────────────────────
from contextlib import contextmanager

@contextmanager
def track_performance(name):
    """Track memory and time for a generator pipeline."""
    import tracemalloc
    tracemalloc.start()
    start_time = time.perf_counter()
    print(f"\n[{name}] Starting...")
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"[{name}] Done in {elapsed:.3f}s")
        print(f"[{name}] Peak memory: {peak / 1024:.1f} KB")

with track_performance("generator pipeline"):
    result = sum(x**2 for x in range(1_000_000) if x % 2 == 0)
    print(f"Result: {result}")
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What is a closure?**  
A: A closure is an inner function that **remembers variables from its enclosing scope** even after the outer function has returned. It requires: a nested function, a free variable from the outer scope, and the outer function returning the inner function.

**Q: What is a decorator?**  
A: A decorator is a function that **wraps another function** to add behavior before/after it runs, without modifying the original function. Under the hood it's a closure — `@decorator` is syntactic sugar for `func = decorator(func)`.

**Q: Why use `@functools.wraps`?**  
A: Without it, the decorated function loses its `__name__`, `__doc__`, and other metadata. `@functools.wraps(func)` copies those attributes from the original function to the wrapper — always include it.

**Q: What is the difference between an iterable and an iterator?**  
A: An **iterable** has `__iter__()` and can be looped multiple times (list, tuple, string). An **iterator** has both `__iter__()` and `__next__()`, is one-time use, and raises `StopIteration` when exhausted. All iterators are iterables, but not all iterables are iterators.

**Q: What is a generator?**  
A: A generator is a function that uses `yield` to produce values one at a time. It's lazy (computes on demand), memory-efficient (doesn't store all values), and returns a generator object which is an iterator.

**Q: What is the difference between `return` and `yield`?**  
A: `return` exits the function and returns a value. `yield` **pauses** the function, saves its state, produces a value, and **resumes** from where it left off on the next `next()` call. A function with `yield` becomes a generator function.

**Q: When would you use a generator over a list?**  
A: When working with **large or infinite datasets** where you don't need all values in memory at once — reading large files line by line, paginated API calls, data pipelines, infinite sequences.

**Q: What does a context manager do?**  
A: It manages resources — ensuring setup (`__enter__`) and teardown (`__exit__`) happen correctly, even if an exception occurs. The `with` statement is the syntax. Common uses: file handling, DB connections, locks, timing.

**Q: How do you create a context manager without a class?**  
A: Use `@contextlib.contextmanager` decorator on a generator function. Everything before `yield` is `__enter__`, everything after is `__exit__`. Wrap in `try/finally` to ensure cleanup on exceptions.

**Q: What is the closure loop gotcha?**  
A: When creating closures in a loop, all closures capture the same variable (not its value at creation time). Fix: use a default argument `lambda x=i: x` or a factory function to capture the current value.

**Q: What is `yield from`?**  
A: `yield from iterable` delegates to a sub-generator or iterable, yielding each of its values. It's cleaner than a loop with `yield` and also passes `.send()` and `.throw()` through.

---

## 📝 Key Takeaways

1. **Closure** = inner function that remembers outer function's variables — foundation of decorators
2. **Decorator** = closure that wraps a function — always use `@functools.wraps(func)` inside
3. **Decorator with args** = needs 3 levels of nesting: factory → decorator → wrapper
4. **Stacked decorators** apply bottom-up but execute top-down
5. **Iterable** = has `__iter__` (loopable many times) | **Iterator** = has `__iter__` + `__next__` (one-time use)
6. **Generator** = function with `yield` — lazy, memory efficient, pauses and resumes
7. **`yield`** pauses function and saves state | **`return`** ends function completely
8. **Generator expressions** `(x for x in ...)` are lazy — use instead of list comprehensions for large data
9. **Context manager** = `__enter__` (setup) + `__exit__` (teardown, always runs) — use `with` statement
10. **`@contextmanager`** + generator = easiest way to build context managers without a class

---

*Day 4 Complete ✅ → Move to Day 5: Concurrency — GIL, Threading, Multiprocessing, Async*

















---
---
---
---
---


# 📅 Day 5 — Concurrency + Internals
> **Goal:** Senior-level understanding  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: GIL — Global Interpreter Lock

### 🔹 What is the GIL?

The **Global Interpreter Lock (GIL)** is a **mutex (lock)** in CPython (the standard Python interpreter) that allows only **one thread to execute Python bytecode at a time** — even on a multi-core machine.

**In simple terms:**  
Even if you have 8 CPU cores and 8 threads, only ONE thread runs Python code at any given moment.

```
Without GIL (ideal):
Core 1: Thread 1 ████████████
Core 2: Thread 2 ████████████
Core 3: Thread 3 ████████████
← True parallelism

With GIL (reality in CPython):
Core 1: Thread 1 ██ __ ██ __ ██
Core 2: Thread 2 __ ██ __ ██ __
Core 3: (idle)
← Concurrency, NOT parallelism (threads take turns)
```

---

### 🔹 Why Does the GIL Exist?

Python's memory management (reference counting) is **not thread-safe**.

```python
# Every object has a reference count
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))   # 2 (x + getrefcount's arg)

y = x                        # reference count goes to 3
del y                        # reference count back to 2
del x                        # reference count hits 0 → garbage collected
```

Without the GIL, two threads could simultaneously modify reference counts → **race conditions → memory corruption → crashes**.  
The GIL was the simplest solution to make CPython thread-safe.

---

### 🔹 What Does the GIL Block? What Doesn't It?

```
GIL BLOCKS:
  ✗ CPU-bound Python code (math, loops, string processing)
  ✗ Any pure Python computation

GIL RELEASES:
  ✓ I/O operations (file read/write, network calls, DB queries)
  ✓ time.sleep()
  ✓ C extensions that explicitly release the GIL (NumPy, Pandas)
  ✓ subprocess calls
```

```python
import threading
import time
import requests   # I/O bound — GIL is released during network call

# GIL is released during requests.get() → threading actually helps here!
def fetch_url(url):
    response = requests.get(url)
    print(f"Got {len(response.content)} bytes from {url}")

# Threading helps for I/O bound work
urls = ["https://httpbin.org/delay/1"] * 5

# Sequential: 5 seconds
# Threaded: ~1 second (all waiting on network simultaneously)
```

---

### 🔹 The GIL and CPU-Bound Work

```python
import threading
import time

def cpu_task(n):
    """Pure CPU work — GIL prevents true parallelism."""
    count = 0
    for i in range(n):
        count += i
    return count

# Single thread
start = time.perf_counter()
cpu_task(50_000_000)
cpu_task(50_000_000)
single_time = time.perf_counter() - start
print(f"Single thread: {single_time:.2f}s")

# Two threads — NOT faster (GIL!)
start = time.perf_counter()
t1 = threading.Thread(target=cpu_task, args=(50_000_000,))
t2 = threading.Thread(target=cpu_task, args=(50_000_000,))
t1.start(); t2.start()
t1.join();  t2.join()
two_thread_time = time.perf_counter() - start
print(f"Two threads: {two_thread_time:.2f}s")  # ≈ same or SLOWER than single!
# Slower because of GIL contention + thread switching overhead
```

---

### 🔹 GIL Workarounds

```
Problem                      → Solution
─────────────────────────────────────────────────────
CPU-bound Python code        → multiprocessing (separate processes, each has own GIL)
CPU-bound numerical work     → NumPy / Pandas (C extensions, release GIL)
I/O-bound work               → threading or asyncio (GIL released during I/O)
CPU + I/O mixed              → concurrent.futures (ThreadPoolExecutor or ProcessPoolExecutor)
```

---

### 🔹 GIL in Python 3.13+ (New!)

Python 3.13 introduced **experimental free-threaded mode** (no GIL):
```bash
python3.13t your_script.py    # 't' = free-threaded build
```
This is experimental — real-world adoption is still early.

---

## 📌 Topic 2: Multithreading vs Multiprocessing

### 🔹 Core Concepts

| | Threading | Multiprocessing |
|---|-----------|----------------|
| **What** | Multiple threads in ONE process | Multiple independent processes |
| **Memory** | Shared memory space | Separate memory per process |
| **GIL** | Limited by GIL | Each process has its OWN GIL |
| **Best for** | I/O-bound tasks | CPU-bound tasks |
| **Overhead** | Low (cheap to create) | High (expensive to create) |
| **Communication** | Easy (shared variables) | Hard (Queue, Pipe, Manager) |
| **Crash isolation** | One crash affects all | Crashes are isolated |

---

### 🔹 Threading — Deep Dive

```python
import threading
import time
import queue

# ─── Basic Thread Creation ────────────────────────────────────────────────────

def worker(name, delay):
    print(f"[{name}] Starting — will sleep {delay}s")
    time.sleep(delay)   # GIL released during sleep!
    print(f"[{name}] Done")

# Method 1: threading.Thread
t1 = threading.Thread(target=worker, args=("Thread-1", 2))
t2 = threading.Thread(target=worker, args=("Thread-2", 1))

t1.start()   # start thread
t2.start()

t1.join()    # wait for t1 to finish
t2.join()    # wait for t2 to finish

print("All threads done")
# Thread-1 Starting — will sleep 2s
# Thread-2 Starting — will sleep 1s
# Thread-2 Done        ← finishes first (only 1s)
# Thread-1 Done


# ─── Daemon Threads ───────────────────────────────────────────────────────────
# Daemon thread: dies automatically when main program exits
# Non-daemon (default): main program waits for them to finish

t = threading.Thread(target=worker, args=("Daemon", 10), daemon=True)
t.start()
print("Main program done — daemon thread auto-killed")
# Main exits, daemon killed immediately (didn't wait 10s)
```

---

### 🔹 Thread Synchronization — Race Conditions & Locks

```python
import threading

# ─── Race Condition Example ───────────────────────────────────────────────────
counter = 0

def increment_unsafe():
    global counter
    for _ in range(100_000):
        counter += 1   # NOT atomic! Read → modify → write (3 steps)

threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Expected: 500000, Got: {counter}")
# Expected: 500000, Got: 378234  ← WRONG due to race condition!


# ─── Fix with Lock ────────────────────────────────────────────────────────────
counter = 0
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(100_000):
        with lock:          # acquire lock, release after block
            counter += 1   # only ONE thread at a time

threads = [threading.Thread(target=increment_safe) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Expected: 500000, Got: {counter}")
# Expected: 500000, Got: 500000 ✅


# ─── RLock — Reentrant Lock (same thread can acquire multiple times) ──────────
rlock = threading.RLock()

def recursive_work(depth):
    with rlock:   # same thread can re-acquire RLock
        print(f"Depth {depth}")
        if depth > 0:
            recursive_work(depth - 1)

recursive_work(3)


# ─── Semaphore — limit concurrent access ─────────────────────────────────────
sem = threading.Semaphore(3)   # max 3 threads at once

def limited_resource(name):
    with sem:
        print(f"{name} using resource")
        time.sleep(1)
        print(f"{name} releasing resource")

threads = [threading.Thread(target=limited_resource, args=(f"T{i}",)) for i in range(7)]
for t in threads: t.start()
for t in threads: t.join()
# Only 3 threads run at a time
```

---

### 🔹 Thread Communication — Queue

```python
import threading
import queue
import time
import random

# Producer-Consumer Pattern — thread-safe via Queue
def producer(q, items):
    for item in items:
        time.sleep(random.uniform(0.1, 0.3))
        q.put(item)
        print(f"Produced: {item}")
    q.put(None)   # sentinel value to signal done

def consumer(q, name):
    while True:
        item = q.get()    # blocks until item available
        if item is None:
            q.put(None)   # pass sentinel to next consumer
            break
        print(f"[{name}] Consumed: {item}")
        q.task_done()
        time.sleep(0.1)

task_queue = queue.Queue(maxsize=5)   # buffer of max 5 items

prod_thread = threading.Thread(target=producer, args=(task_queue, range(1, 11)))
cons1 = threading.Thread(target=consumer, args=(task_queue, "Consumer-1"))
cons2 = threading.Thread(target=consumer, args=(task_queue, "Consumer-2"))

prod_thread.start()
cons1.start()
cons2.start()

prod_thread.join()
cons1.join()
cons2.join()
```

---

### 🔹 Multiprocessing — Deep Dive

```python
import multiprocessing
import time
import os

# ─── Basic Process Creation ───────────────────────────────────────────────────
def cpu_heavy(n, result_queue):
    pid = os.getpid()
    print(f"Process {pid} computing...")
    result = sum(i * i for i in range(n))
    result_queue.put(result)
    print(f"Process {pid} done: {result}")

if __name__ == "__main__":   # ALWAYS needed for multiprocessing on Windows/macOS
    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=cpu_heavy, args=(5_000_000, q))
    p2 = multiprocessing.Process(target=cpu_heavy, args=(5_000_000, q))

    start = time.perf_counter()
    p1.start(); p2.start()
    p1.join();  p2.join()
    elapsed = time.perf_counter() - start

    results = [q.get() for _ in range(2)]
    print(f"Results: {results}, Time: {elapsed:.2f}s")
    # True parallelism! Both processes run on separate cores simultaneously


# ─── Shared Memory ────────────────────────────────────────────────────────────
from multiprocessing import Value, Array

def increment_shared(counter, lock):
    for _ in range(100_000):
        with lock:
            counter.value += 1

if __name__ == "__main__":
    counter = Value('i', 0)   # shared integer
    lock = multiprocessing.Lock()

    procs = [multiprocessing.Process(target=increment_shared, args=(counter, lock))
             for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()

    print(f"Shared counter: {counter.value}")   # 400000


# ─── Process Pool ─────────────────────────────────────────────────────────────
def square(n):
    return n * n

if __name__ == "__main__":
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(square, range(1, 11))
        print(results)    # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

        # map_async — non-blocking
        async_result = pool.map_async(square, range(100))
        # do other work here...
        print(async_result.get())   # wait and get results
```

---

### 🔹 Threading vs Multiprocessing — When to Use Which

```python
import time
import threading
import multiprocessing
import requests

# ─── I/O Bound — Threading WINS ───────────────────────────────────────────────
def download(url):
    time.sleep(1)   # simulate network call
    return f"Downloaded {url}"

urls = [f"http://example.com/{i}" for i in range(10)]

# Sequential: 10 seconds
start = time.perf_counter()
results = [download(url) for url in urls]
print(f"Sequential I/O: {time.perf_counter() - start:.1f}s")   # ~10.0s

# Threaded: ~1 second (all sleeping concurrently)
start = time.perf_counter()
threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()
print(f"Threaded I/O: {time.perf_counter() - start:.1f}s")     # ~1.0s ✅


# ─── CPU Bound — Multiprocessing WINS ────────────────────────────────────────
def cpu_work(n):
    return sum(i * i for i in range(n))

tasks = [5_000_000] * 4

# Sequential: ~4x single time
start = time.perf_counter()
[cpu_work(n) for n in tasks]
print(f"Sequential CPU: {time.perf_counter() - start:.2f}s")

# Multiprocessing: ~1x single time (4 cores working together)
if __name__ == "__main__":
    start = time.perf_counter()
    with multiprocessing.Pool(4) as pool:
        pool.map(cpu_work, tasks)
    print(f"Multiprocessing CPU: {time.perf_counter() - start:.2f}s")  # ~4x faster!
```

---

## 📌 Topic 3: `concurrent.futures` — High-Level Interface

### 🔹 Why `concurrent.futures`?

`concurrent.futures` gives a **clean, consistent interface** for both threading and multiprocessing — no need to manually manage threads/processes.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import urllib.request

# ─── ThreadPoolExecutor — for I/O bound ──────────────────────────────────────
def fetch_data(url):
    time.sleep(1)   # simulate I/O
    return f"Data from {url}"

urls = [f"http://example.com/page/{i}" for i in range(10)]

# submit() — returns a Future object
with ThreadPoolExecutor(max_workers=5) as executor:
    # submit tasks
    futures = [executor.submit(fetch_data, url) for url in urls]

    # as_completed — process results as they finish (not in order)
    for future in as_completed(futures):
        try:
            result = future.result()
            print(result)
        except Exception as e:
            print(f"Error: {e}")


# map() — simpler, preserves order
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_data, urls))
    print(results)   # in same order as input


# ─── ProcessPoolExecutor — for CPU bound ─────────────────────────────────────
def cpu_intensive(n):
    return sum(i ** 2 for i in range(n))

tasks = [2_000_000] * 8

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_intensive, tasks))
        print(f"Sum of results: {sum(results)}")
```

---

### 🔹 Future Objects — Check Status, Cancel, Callbacks

```python
from concurrent.futures import ThreadPoolExecutor
import time

def slow_task(n):
    time.sleep(n)
    if n == 3:
        raise ValueError("Task with n=3 always fails!")
    return f"Result after {n}s"

with ThreadPoolExecutor(max_workers=3) as executor:
    f1 = executor.submit(slow_task, 1)
    f2 = executor.submit(slow_task, 2)
    f3 = executor.submit(slow_task, 3)

    # Check status
    print(f"f1 done? {f1.done()}")     # False (still running)
    time.sleep(1.5)
    print(f"f1 done? {f1.done()}")     # True

    # Get result (blocks until done)
    print(f1.result())                 # Result after 1s

    # Handle exceptions
    try:
        print(f3.result())
    except ValueError as e:
        print(f"Caught: {e}")          # Caught: Task with n=3 always fails!

    # Add callback — runs when future completes
    def on_done(future):
        try:
            print(f"Callback: {future.result()}")
        except Exception as e:
            print(f"Callback error: {e}")

    f2.add_done_callback(on_done)


# ─── wait() — wait for specific futures ──────────────────────────────────────
from concurrent.futures import wait, FIRST_COMPLETED, ALL_COMPLETED

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(slow_task, i) for i in [2, 1, 3, 1]]

    # Wait for first to complete
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)
    print(f"First done: {len(done)}, Still running: {len(not_done)}")

    # Wait for all
    wait(futures, return_when=ALL_COMPLETED)
    print("All done!")
```

---

### 🔹 Choosing the Right Executor

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

# Rule of thumb:
# ThreadPoolExecutor  → I/O bound  (network, file, DB)
# ProcessPoolExecutor → CPU bound  (math, image processing, ML)

# Good max_workers values:
# ThreadPool   → 5 to 20+ (threads are cheap, I/O spends most time waiting)
# ProcessPool  → os.cpu_count() (one process per core)

print(f"CPU cores: {os.cpu_count()}")   # e.g., 8

# Context manager ensures proper cleanup
with ThreadPoolExecutor(max_workers=10) as pool:
    pass  # executor.shutdown(wait=True) called automatically

# Without context manager — must shutdown manually
pool = ThreadPoolExecutor(max_workers=5)
# ... do work ...
pool.shutdown(wait=True)   # wait=False returns immediately
```

---

## 📌 Topic 4: Async Programming (`async`/`await`)

### 🔹 What is Async Programming?

**Async programming** is a form of **cooperative concurrency** — instead of using threads or processes, a single thread handles multiple tasks by **switching between them when one is waiting** (for I/O, network, etc.).

**Key idea:** While one task waits for a network response, instead of blocking, control returns to the event loop which runs another task.

```
Synchronous:
  Task 1: ████████▓▓▓▓▓▓████████  (▓ = waiting for I/O, CPU idle)
  Task 2: ──────────────────────────████████▓▓▓▓████████  (waits for Task 1)

Async (single thread):
  Task 1: ████████........████████   (. = event loop runs Task 2)
  Task 2:         ████████........████████
  All on ONE thread — no GIL issues, very lightweight!
```

---

### 🔹 Key Terms

| Term | Meaning |
|------|---------|
| `async def` | Defines a **coroutine function** |
| `await` | Pause this coroutine, let event loop run others |
| `coroutine` | A function that can be paused and resumed |
| `event loop` | The engine that manages and switches between coroutines |
| `asyncio` | Python's built-in async library |
| `Task` | A scheduled coroutine running in the event loop |

---

### 🔹 Basic Async Syntax

```python
import asyncio
import time

# ─── Regular function vs Coroutine ───────────────────────────────────────────
def regular_sleep(n):
    time.sleep(n)              # BLOCKS everything
    return f"Regular slept {n}s"

async def async_sleep(n):
    await asyncio.sleep(n)     # yields control during wait
    return f"Async slept {n}s"


# ─── Running a coroutine ──────────────────────────────────────────────────────
async def main():
    result = await async_sleep(1)
    print(result)   # Async slept 1s

asyncio.run(main())   # starts the event loop


# ─── Sequential vs Concurrent ─────────────────────────────────────────────────
async def task(name, delay):
    print(f"[{name}] Starting")
    await asyncio.sleep(delay)
    print(f"[{name}] Done after {delay}s")
    return name

# Sequential — 3 seconds total
async def sequential():
    start = time.perf_counter()
    await task("A", 1)
    await task("B", 1)
    await task("C", 1)
    print(f"Sequential: {time.perf_counter() - start:.1f}s")   # 3.0s

# Concurrent — ~1 second total
async def concurrent():
    start = time.perf_counter()
    results = await asyncio.gather(
        task("A", 1),
        task("B", 1),
        task("C", 1),
    )
    print(f"Concurrent: {time.perf_counter() - start:.1f}s")   # ~1.0s
    print(f"Results: {results}")   # ['A', 'B', 'C']

asyncio.run(sequential())
asyncio.run(concurrent())
```

---

### 🔹 `asyncio.gather` vs `asyncio.create_task`

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} result"

# ─── gather — run multiple coroutines concurrently, wait for ALL ──────────────
async def use_gather():
    results = await asyncio.gather(
        fetch("A", 2),
        fetch("B", 1),
        fetch("C", 3),
    )
    # Waits for ALL to complete (~3s total, not 6s)
    print(results)   # ['A result', 'B result', 'C result'] — in order of input!


# ─── create_task — schedule and run in background ────────────────────────────
async def use_tasks():
    # Schedule tasks immediately — they start running
    task_a = asyncio.create_task(fetch("A", 2))
    task_b = asyncio.create_task(fetch("B", 1))
    task_c = asyncio.create_task(fetch("C", 3))

    # Do other work while tasks run in background
    print("Tasks are running in background...")
    await asyncio.sleep(0)   # yield to let tasks start

    # Wait for them individually
    result_b = await task_b   # B finishes first (1s)
    result_a = await task_a   # A next (2s)
    result_c = await task_c   # C last (3s)
    print(result_b, result_a, result_c)


# ─── as_completed — process results as they arrive ───────────────────────────
async def use_as_completed():
    tasks = [
        asyncio.create_task(fetch("A", 3)),
        asyncio.create_task(fetch("B", 1)),
        asyncio.create_task(fetch("C", 2)),
    ]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"Got: {result}")   # B first, then C, then A (by completion order)


asyncio.run(use_gather())
asyncio.run(use_tasks())
asyncio.run(use_as_completed())
```

---

### 🔹 Error Handling in Async

```python
import asyncio

async def risky_task(name, should_fail=False):
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError(f"{name} failed!")
    return f"{name} success"


# ─── try/except in coroutine ──────────────────────────────────────────────────
async def handle_errors():
    try:
        result = await risky_task("Task-A", should_fail=True)
    except ValueError as e:
        print(f"Caught: {e}")

    # gather — by default, first exception cancels all
    try:
        results = await asyncio.gather(
            risky_task("T1"),
            risky_task("T2", should_fail=True),
            risky_task("T3"),
        )
    except ValueError as e:
        print(f"Gather failed: {e}")

    # return_exceptions=True — collects all results AND exceptions
    results = await asyncio.gather(
        risky_task("T1"),
        risky_task("T2", should_fail=True),
        risky_task("T3"),
        return_exceptions=True,   # exceptions returned as values, not raised
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"Exception: {r}")
        else:
            print(f"Success: {r}")


asyncio.run(handle_errors())
```

---

### 🔹 Async Context Managers and Iterators

```python
import asyncio

# ─── Async context manager ────────────────────────────────────────────────────
class AsyncDBConnection:
    async def __aenter__(self):
        print("Connecting to DB...")
        await asyncio.sleep(0.1)   # simulate connection time
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing DB connection")
        await asyncio.sleep(0.05)

    async def query(self, sql):
        await asyncio.sleep(0.1)   # simulate query
        return [{"id": 1, "name": "Alice"}]


async def use_db():
    async with AsyncDBConnection() as db:
        results = await db.query("SELECT * FROM users")
        print(results)


# ─── Async generator / iterator ───────────────────────────────────────────────
async def async_range(start, stop, delay=0.1):
    for i in range(start, stop):
        await asyncio.sleep(delay)   # async operation per item
        yield i

async def use_async_gen():
    async for num in async_range(0, 5):
        print(num, end=" ")   # 0 1 2 3 4

asyncio.run(use_db())
asyncio.run(use_async_gen())
```

---

### 🔹 Async vs Threading vs Multiprocessing — Full Comparison

```
┌─────────────────┬──────────────────────┬────────────────────┬─────────────────────┐
│                 │  Threading           │  Multiprocessing   │  Async (asyncio)    │
├─────────────────┼──────────────────────┼────────────────────┼─────────────────────┤
│ Best for        │ I/O bound            │ CPU bound          │ I/O bound (many)    │
│ GIL affected    │ Yes                  │ No                 │ No (single thread)  │
│ Memory          │ Shared               │ Separate           │ Shared              │
│ Threads/Procs   │ Multiple threads     │ Multiple processes │ Single thread       │
│ Overhead        │ Low-Medium           │ High               │ Very low            │
│ Complexity      │ Medium               │ High               │ Medium              │
│ Scale           │ 100s of threads      │ CPU count          │ 10,000s of tasks    │
│ Python support  │ threading module     │ multiprocessing    │ asyncio             │
└─────────────────┴──────────────────────┴────────────────────┴─────────────────────┘

Decision flowchart:
  Is the task CPU-bound?
    YES → multiprocessing / ProcessPoolExecutor
    NO  → Is there a lot of concurrency (1000s)?
            YES → asyncio
            NO  → threading / ThreadPoolExecutor
```

---

## 🛠️ Practice 1: Threading Examples

```python
import threading
import time
import queue
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── Example 1: Web Scraper Simulation ───────────────────────────────────────
def scrape_page(url, results, lock):
    """Simulate scraping a web page."""
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)  # simulate network I/O
    data = {"url": url, "content_length": random.randint(1000, 50000), "time": delay}

    with lock:
        results.append(data)

    logger.info(f"Scraped {url} in {delay:.2f}s")


def run_scraper(urls):
    results = []
    lock = threading.Lock()

    threads = [
        threading.Thread(
            target=scrape_page,
            args=(url, results, lock),
            name=f"Scraper-{i}"
        )
        for i, url in enumerate(urls)
    ]

    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.perf_counter() - start

    logger.info(f"Scraped {len(results)} pages in {elapsed:.2f}s")
    return results


urls = [f"https://example.com/page/{i}" for i in range(8)]
results = run_scraper(urls)
print(f"\nTotal pages scraped: {len(results)}")


# ─── Example 2: Thread Pool with concurrent.futures ──────────────────────────
def download_file(file_id):
    """Simulate file download."""
    delay = random.uniform(0.3, 1.5)
    time.sleep(delay)
    if file_id % 7 == 0:   # simulate occasional failure
        raise ConnectionError(f"Failed to download file_{file_id}")
    return {"file_id": file_id, "size_kb": random.randint(100, 5000)}


def download_all(file_ids, max_workers=5):
    success = []
    failed = []

    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="Downloader") as executor:
        future_to_id = {executor.submit(download_file, fid): fid for fid in file_ids}

        for future in as_completed(future_to_id):
            file_id = future_to_id[future]
            try:
                result = future.result()
                success.append(result)
                logger.info(f"✅ Downloaded file_{file_id}: {result['size_kb']}KB")
            except ConnectionError as e:
                failed.append(file_id)
                logger.warning(f"❌ {e}")

    return success, failed


print("\n─── File Download Simulation ───")
start = time.perf_counter()
success, failed = download_all(range(1, 21), max_workers=5)
elapsed = time.perf_counter() - start

print(f"Downloaded: {len(success)}, Failed: {len(failed)}")
print(f"Time: {elapsed:.2f}s (sequential would take ~{len(range(1,21)) * 0.9:.1f}s)")


# ─── Example 3: Producer-Consumer with Thread Pool ───────────────────────────
def process_item(item):
    """Worker function — process one item."""
    time.sleep(random.uniform(0.1, 0.5))
    return item * item


print("\n─── Producer-Consumer Pattern ───")
items = list(range(1, 16))

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_item, items))

print(f"Processed {len(results)} items: {results[:5]}...")
```

---

## 🛠️ Practice 2: Async API Call Examples

```python
import asyncio
import time
import random
import json
from typing import List, Dict, Any


# ─── Simulate async HTTP calls (no external library needed) ──────────────────
async def fake_http_get(url: str, timeout: float = 5.0) -> Dict:
    """Simulate an async HTTP GET request."""
    delay = random.uniform(0.2, 1.5)
    await asyncio.sleep(delay)   # GIL released here

    if "error" in url:
        raise ConnectionError(f"HTTP 500 from {url}")
    if delay > 1.3:
        raise asyncio.TimeoutError(f"Timeout fetching {url}")

    return {
        "url": url,
        "status": 200,
        "data": {"id": hash(url) % 1000, "value": random.randint(1, 100)},
        "response_time": round(delay, 3),
    }


# ─── Example 1: Fetch multiple APIs concurrently ─────────────────────────────
async def fetch_all_concurrent(urls: List[str]) -> List[Dict]:
    """Fetch all URLs concurrently — total time ≈ slowest single request."""
    print(f"\nFetching {len(urls)} URLs concurrently...")
    start = time.perf_counter()

    results = await asyncio.gather(
        *[fake_http_get(url) for url in urls],
        return_exceptions=True,
    )

    elapsed = time.perf_counter() - start
    successful = [r for r in results if isinstance(r, dict)]
    failed = [r for r in results if isinstance(r, Exception)]

    print(f"✅ Success: {len(successful)}, ❌ Failed: {len(failed)}")
    print(f"⏱  Total time: {elapsed:.2f}s (sequential would be ~{len(urls) * 0.85:.1f}s)")
    return successful


urls = [
    "https://api.example.com/users/1",
    "https://api.example.com/users/2",
    "https://api.example.com/error/3",   # will fail
    "https://api.example.com/products/1",
    "https://api.example.com/products/2",
    "https://api.example.com/orders/1",
]

asyncio.run(fetch_all_concurrent(urls))


# ─── Example 2: Rate-Limited API Fetcher ──────────────────────────────────────
async def rate_limited_fetch(url: str, semaphore: asyncio.Semaphore) -> Dict:
    """Fetch with rate limiting — max N concurrent requests."""
    async with semaphore:   # acquire slot, release after done
        print(f"→ Fetching {url}")
        result = await fake_http_get(url)
        print(f"← Done {url} in {result['response_time']}s")
        return result


async def fetch_with_rate_limit(urls: List[str], max_concurrent: int = 3):
    """Fetch URLs but limit to max_concurrent at a time."""
    print(f"\nFetching {len(urls)} URLs (max {max_concurrent} concurrent)...")
    semaphore = asyncio.Semaphore(max_concurrent)

    tasks = [rate_limited_fetch(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, dict)]


all_urls = [f"https://api.example.com/item/{i}" for i in range(1, 10)]
asyncio.run(fetch_with_rate_limit(all_urls, max_concurrent=3))


# ─── Example 3: Retry with Exponential Backoff ────────────────────────────────
async def fetch_with_retry(url: str, max_retries: int = 3) -> Dict:
    """Fetch with automatic retry on failure."""
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            result = await fake_http_get(url)
            if attempt > 1:
                print(f"✅ {url} succeeded on attempt {attempt}")
            return result
        except (ConnectionError, asyncio.TimeoutError) as e:
            last_error = e
            if attempt < max_retries:
                wait = 2 ** (attempt - 1)   # exponential backoff: 1s, 2s, 4s
                print(f"⚠  Attempt {attempt} failed: {e}. Retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                print(f"✗ {url} failed after {max_retries} attempts")

    raise last_error


async def resilient_fetch_all(urls: List[str]) -> List[Dict]:
    """Fetch all with retry logic."""
    print(f"\nResilient fetch of {len(urls)} URLs with retry...")
    tasks = [fetch_with_retry(url, max_retries=3) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    success = [r for r in results if isinstance(r, dict)]
    print(f"Final: {len(success)}/{len(urls)} succeeded")
    return success


retry_urls = [
    "https://api.example.com/stable/1",
    "https://api.example.com/error/fail",
    "https://api.example.com/stable/2",
]
asyncio.run(resilient_fetch_all(retry_urls))


# ─── Example 4: Async Pipeline ────────────────────────────────────────────────
async def fetch_user(user_id: int) -> Dict:
    await asyncio.sleep(random.uniform(0.1, 0.4))
    return {"id": user_id, "name": f"User_{user_id}", "dept_id": user_id % 3 + 1}

async def fetch_department(dept_id: int) -> Dict:
    await asyncio.sleep(random.uniform(0.1, 0.3))
    depts = {1: "Engineering", 2: "Marketing", 3: "HR"}
    return {"id": dept_id, "name": depts.get(dept_id, "Unknown")}

async def enrich_user(user: Dict) -> Dict:
    """Fetch related data for a user concurrently."""
    dept = await fetch_department(user["dept_id"])
    return {**user, "department": dept["name"]}

async def process_users_pipeline(user_ids: List[int]) -> List[Dict]:
    """Full async pipeline: fetch users → enrich with dept → return."""
    print(f"\nProcessing {len(user_ids)} users through async pipeline...")
    start = time.perf_counter()

    # Step 1: Fetch all users concurrently
    users = await asyncio.gather(*[fetch_user(uid) for uid in user_ids])

    # Step 2: Enrich each user concurrently
    enriched = await asyncio.gather(*[enrich_user(u) for u in users])

    elapsed = time.perf_counter() - start
    print(f"Pipeline done in {elapsed:.2f}s")
    for u in enriched:
        print(f"  {u['name']} → {u['department']}")
    return list(enriched)


asyncio.run(process_users_pipeline(list(range(1, 8))))
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What is the GIL?**  
A: The Global Interpreter Lock is a mutex in CPython that allows only **one thread to execute Python bytecode at a time**, even on multi-core machines. It exists to protect Python's reference-counting memory management from race conditions.

**Q: Does the GIL mean Python can't be concurrent?**  
A: No. The GIL is released during I/O operations (network, file, DB). Threading still helps for I/O-bound tasks. For CPU-bound tasks, use `multiprocessing` (separate processes, each with their own GIL).

**Q: When do you use threading vs multiprocessing?**  
A: **Threading** for I/O-bound tasks (network requests, file ops, DB queries) — threads wait on I/O, GIL released. **Multiprocessing** for CPU-bound tasks (heavy computation, data processing) — bypasses GIL by using separate processes.

**Q: When do you use asyncio instead of threading?**  
A: When you have **many concurrent I/O operations** (hundreds or thousands). Asyncio is a single thread switching between tasks cooperatively — much lower overhead than creating many OS threads. Perfect for APIs, web servers, microservices.

**Q: What is a coroutine?**  
A: A coroutine is a function defined with `async def` that can be paused with `await` and resumed later. It doesn't block — it yields control to the event loop while waiting, allowing other coroutines to run.

**Q: What's the difference between `asyncio.gather` and `asyncio.create_task`?**  
A: `gather` runs coroutines concurrently and waits for ALL to finish, returning results in input order. `create_task` schedules a coroutine immediately and returns a Task — you can await it later, giving you more control over individual tasks.

**Q: What is a race condition?**  
A: When two threads access and modify shared data simultaneously, and the result depends on the order of execution — causing unpredictable bugs. Fixed using `Lock`, `RLock`, or `Queue`.

**Q: What is a deadlock?**  
A: When two or more threads are waiting for each other to release a lock, so none can proceed. Prevented by always acquiring locks in the same order, using timeouts, or using `asyncio` instead.

**Q: What does `concurrent.futures` provide?**  
A: A high-level interface for async execution using `ThreadPoolExecutor` (threading) and `ProcessPoolExecutor` (multiprocessing). Provides `submit()` (returns Future), `map()`, `as_completed()`, and `wait()`.

**Q: What is a Future object?**  
A: An object representing the result of an asynchronous computation. You can check `.done()`, call `.result()` (blocks), add `.add_done_callback()`, or cancel with `.cancel()`.

**Q: What's the difference between concurrency and parallelism?**  
A: **Concurrency** = dealing with many things at once (structure) — tasks take turns. **Parallelism** = doing many things at the same time (execution) — tasks run simultaneously. Python threading gives concurrency. Multiprocessing gives true parallelism.

---

## 📝 Key Takeaways

1. **GIL** = one thread executes Python bytecode at a time — limits CPU parallelism, NOT I/O concurrency
2. **GIL releases during I/O** — threading still useful for network/file/DB operations
3. **Threading** = shared memory, best for I/O-bound, limited by GIL for CPU work
4. **Multiprocessing** = separate processes/memory, best for CPU-bound, true parallelism
5. **asyncio** = single thread, event loop, cooperative — best for massive I/O concurrency (10,000s of connections)
6. **`concurrent.futures`** = clean high-level API — `ThreadPoolExecutor` for I/O, `ProcessPoolExecutor` for CPU
7. **Race condition** → use `Lock` | **Deadlock** → careful lock ordering | **Limit concurrency** → `Semaphore`
8. **`await`** pauses the coroutine and yields to event loop — never blocks the thread
9. **`asyncio.gather`** = run many coroutines concurrently, wait for all | **`create_task`** = schedule and run in background
10. **Choose your model:** CPU-bound → multiprocessing | I/O-bound few → threading | I/O-bound many → asyncio

---

*Day 5 Complete ✅ → Move to Day 6: FastAPI — Build Real Backend APIs*



---
---
---


# 📅 Day 6 — FastAPI (Real Backend)
> **Goal:** Show real-world backend skills  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: FastAPI Basics

### 🔹 What is FastAPI?

**FastAPI** is a modern, high-performance Python web framework for building APIs. It is built on top of **Starlette** (ASGI framework) and **Pydantic** (data validation).

**Why FastAPI over Flask/Django REST?**

| Feature | FastAPI | Flask | Django REST |
|---------|---------|-------|-------------|
| Performance | ⚡ Very High (async) | Medium | Medium |
| Auto docs | ✅ Built-in (Swagger + ReDoc) | ❌ Manual | ❌ Manual |
| Type hints | ✅ First-class | ❌ Optional | ❌ Optional |
| Validation | ✅ Pydantic (auto) | ❌ Manual | ⚠️ Serializers |
| Async support | ✅ Native | ⚠️ Limited | ⚠️ Limited |
| Learning curve | Low | Very Low | High |

---

### 🔹 Installation & Setup

```bash
# Install FastAPI and server
pip install fastapi uvicorn[standard]

# Optional but recommended
pip install pydantic[email]    # email validation
pip install python-multipart   # form data
pip install httpx              # async HTTP client (for testing)

# Run the server
uvicorn main:app --reload
#         ↑    ↑    ↑
#       file  var  auto-restart on file change
#       name  name

# Custom host/port
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

---

### 🔹 Your First FastAPI App

```python
# main.py
from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI(
    title="My API",
    description="A sample FastAPI application",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI  → http://localhost:8000/docs
    redoc_url="/redoc",      # ReDoc UI    → http://localhost:8000/redoc
    openapi_url="/openapi.json"
)


# ─── Route / Endpoint ─────────────────────────────────────────────────────────
@app.get("/")                       # HTTP method + path
async def root():                   # async function = coroutine
    return {"message": "Hello, FastAPI!"}   # auto-converted to JSON


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


# ─── Path Parameters ──────────────────────────────────────────────────────────
@app.get("/users/{user_id}")
async def get_user(user_id: int):   # type hint → auto validation + conversion
    return {"user_id": user_id, "name": f"User {user_id}"}

# user_id declared as int → FastAPI:
# - validates it's an integer
# - converts "123" (string from URL) to 123 (int)
# - returns 422 Unprocessable Entity if "abc" is passed


# ─── Query Parameters ─────────────────────────────────────────────────────────
@app.get("/items/")
async def list_items(
    skip: int = 0,          # optional, default 0
    limit: int = 10,        # optional, default 10
    search: str | None = None,  # optional, can be None
    active: bool = True,    # bool: ?active=true or ?active=1 or ?active=yes
):
    return {
        "skip": skip,
        "limit": limit,
        "search": search,
        "active": active
    }
# GET /items/?skip=20&limit=5&search=laptop&active=false
```

---

### 🔹 HTTP Methods

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")        # READ
async def read_item(item_id: int):
    pass

@app.post("/items/")               # CREATE
async def create_item():
    pass

@app.put("/items/{item_id}")       # FULL UPDATE (replace entire resource)
async def update_item(item_id: int):
    pass

@app.patch("/items/{item_id}")     # PARTIAL UPDATE (update specific fields)
async def partial_update(item_id: int):
    pass

@app.delete("/items/{item_id}")    # DELETE
async def delete_item(item_id: int):
    pass

@app.head("/items/")               # like GET but no body (check existence)
async def head_items():
    pass

@app.options("/items/")            # returns allowed HTTP methods
async def options_items():
    pass
```

---

### 🔹 Response Models and Status Codes

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    message: str = "success"


# response_model → filters response, only includes declared fields
# status_code    → HTTP status code returned on success
@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,   # 201 Created
)
async def create_item(item: Item):
    # Even if we return extra fields, response_model filters them out
    return {"id": 1, "name": item.name, "price": item.price, "secret": "hidden"}
    # "secret" will NOT appear in response — filtered by response_model
```

---

## 📌 Topic 2: Request/Response Lifecycle

### 🔹 How a Request Flows Through FastAPI

```
Client Request
      ↓
  Uvicorn (ASGI server) — receives HTTP, converts to ASGI scope
      ↓
  Middleware Stack (outermost first)
      ↓
  Router — matches URL + method to handler function
      ↓
  Dependency Injection — resolves all Depends()
      ↓
  Request Parsing — path params, query params, body parsed + validated
      ↓
  Handler Function (your code)
      ↓
  Response Serialization — return value → JSON
      ↓
  Middleware Stack (in reverse for response)
      ↓
  Uvicorn — sends HTTP response to client
```

---

### 🔹 Request Object — Access Everything

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/inspect")
async def inspect_request(request: Request):
    return {
        "method":      request.method,            # GET, POST, etc.
        "url":         str(request.url),           # full URL
        "path":        request.url.path,           # /inspect
        "query":       dict(request.query_params), # ?key=val
        "headers":     dict(request.headers),      # all headers
        "client_ip":   request.client.host,        # client IP
        "cookies":     dict(request.cookies),      # cookies
    }

@app.post("/body-raw")
async def read_raw_body(request: Request):
    body = await request.body()    # raw bytes
    text = await request.json()    # parsed JSON (only once — stream)
    return {"body_length": len(body)}
```

---

### 🔹 Request Body — Multiple Ways to Receive Data

```python
from fastapi import FastAPI, Body, Query, Path, Header, Cookie
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


# ─── Body from Pydantic model ─────────────────────────────────────────────────
class Product(BaseModel):
    name: str
    price: float
    quantity: int = 1

@app.post("/products/")
async def create_product(product: Product):
    # FastAPI reads JSON body, validates against Product, raises 422 if invalid
    return product


# ─── Multiple body parameters ─────────────────────────────────────────────────
class User(BaseModel):
    name: str

class Order(BaseModel):
    items: list[str]

@app.post("/checkout/")
async def checkout(user: User, order: Order):
    # Expected JSON: {"user": {"name": "Alice"}, "order": {"items": ["a", "b"]}}
    return {"user": user.name, "items": order.items}


# ─── Body + Path + Query + Header together ───────────────────────────────────
@app.put("/products/{product_id}")
async def update_product(
    product_id: int,                              # path param
    product: Product,                             # body
    notify: bool = Query(False),                  # query param with metadata
    x_api_key: str | None = Header(None),         # request header
    session: str | None = Cookie(None),           # cookie
):
    return {
        "id": product_id,
        "product": product,
        "notify": notify,
        "api_key": x_api_key,
        "session": session,
    }
```

---

### 🔹 Response Object — Customize Responses

```python
from fastapi import FastAPI
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse,
)

app = FastAPI()


# Custom JSON response with headers and cookies
@app.get("/custom-response")
async def custom_response():
    content = {"message": "Custom response"}
    headers = {"X-Custom-Header": "my-value", "X-Request-Id": "abc123"}
    response = JSONResponse(content=content, status_code=200, headers=headers)
    response.set_cookie(key="session_id", value="xyz789", httponly=True)
    return response


# HTML response
@app.get("/page", response_class=HTMLResponse)
async def html_page():
    return "<html><body><h1>Hello!</h1></body></html>"


# Redirect
@app.get("/old-path")
async def redirect():
    return RedirectResponse(url="/new-path", status_code=301)


# Streaming — for large responses
async def generate_data():
    for i in range(10):
        yield f"data: chunk {i}\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(generate_data(), media_type="text/event-stream")
```

---

## 📌 Topic 3: Pydantic Validation

### 🔹 What is Pydantic?

**Pydantic** is a data validation library that uses Python type hints to validate, parse, and serialize data. FastAPI uses Pydantic models for request bodies, response models, and settings.

```python
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
```

---

### 🔹 Basic Pydantic Model

```python
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str                       # required
    email: str                      # required
    age: int                        # required
    bio: Optional[str] = None       # optional, defaults to None
    is_active: bool = True          # optional, defaults to True

# Pydantic automatically:
# - Validates types ("25" → 25 for int)
# - Raises ValidationError for wrong types
# - Generates JSON schema (used by FastAPI for docs)

# Create an instance
user = UserCreate(name="Alice", email="alice@example.com", age=25)
print(user.name)          # Alice
print(user.is_active)     # True
print(user.model_dump())  # {'name': 'Alice', 'email': 'alice@...', ...}
print(user.model_json())  # JSON string
```

---

### 🔹 Field — Add Validation Constraints

```python
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str = Field(
        ...,                        # ... = required (no default)
        min_length=2,
        max_length=100,
        description="Product name",
        examples=["Laptop", "Phone"],
    )
    price: float = Field(
        ...,
        gt=0,                       # greater than 0
        lt=1_000_000,               # less than 1,000,000
        description="Price in INR",
    )
    discount: float = Field(
        default=0.0,
        ge=0.0,                     # greater than or equal to 0
        le=100.0,                   # less than or equal to 100
    )
    quantity: int = Field(default=1, ge=1)
    sku: str = Field(
        ...,
        pattern=r"^[A-Z]{2}-\d{4}$",   # regex pattern: AB-1234
        description="Stock Keeping Unit",
    )
    tags: list[str] = Field(default=[], max_length=5)

# Valid
p = Product(name="Laptop", price=75000.0, sku="LA-1234")

# Invalid — raises ValidationError
try:
    p = Product(name="X", price=-100, sku="invalid")
except Exception as e:
    print(e)
```

---

### 🔹 Custom Validators

```python
from pydantic import BaseModel, field_validator, model_validator, EmailStr
from typing import Optional
import re

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    age: int
    phone: Optional[str] = None

    # ─── Field Validator — validate single field ───────────────────────────
    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v.lower()   # transform: always store lowercase

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email address")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 13:
            raise ValueError("Must be at least 13 years old")
        if v > 120:
            raise ValueError("Invalid age")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not cleaned.startswith("+") and not cleaned.isdigit():
            raise ValueError("Invalid phone number")
        return cleaned

    # ─── Model Validator — cross-field validation ───────────────────────────
    @model_validator(mode="after")
    def passwords_must_match(self) -> "UserRegister":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


# Test
try:
    user = UserRegister(
        username="Alice_99",
        email="ALICE@EXAMPLE.COM",
        password="Secret123",
        confirm_password="Secret123",
        age=25,
        phone="+91 98765-43210"
    )
    print(user.username)   # alice_99 (lowercased)
    print(user.email)      # alice@example.com (lowercased)
    print(user.phone)      # +919876543210 (cleaned)
except Exception as e:
    print(e)
```

---

### 🔹 Nested Models, Enums, and Schema Patterns

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class Address(BaseModel):
    street: str
    city: str
    state: str
    pincode: str = Field(..., pattern=r"^\d{6}$")
    country: str = "India"

class UserBase(BaseModel):
    username: str
    email: str
    role: Role = Role.VIEWER

class UserCreate(UserBase):
    password: str           # only on creation
    address: Optional[Address] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None     # all optional for PATCH
    email: Optional[str] = None
    role: Optional[Role] = None
    address: Optional[Address] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    address: Optional[Address] = None

    model_config = {"from_attributes": True}  # allow ORM model → Pydantic

# Nested model usage
user_data = {
    "username": "alice",
    "email": "alice@example.com",
    "password": "secret",
    "role": "admin",
    "address": {
        "street": "123 MG Road",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560001"
    }
}
user = UserCreate(**user_data)
print(user.role)            # Role.ADMIN
print(user.address.city)    # Bengaluru
print(user.model_dump())    # full nested dict
```

---

## 📌 Topic 4: Dependency Injection

### 🔹 What is Dependency Injection in FastAPI?

**Dependency Injection (DI)** lets you declare shared logic (auth, DB sessions, pagination) as **dependencies** and FastAPI injects them automatically into your route handlers.

```python
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

app = FastAPI()

# ─── Simple dependency ────────────────────────────────────────────────────────
def get_pagination(skip: int = 0, limit: int = 10):
    """Reusable pagination params — available to any route."""
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    return {"skip": skip, "limit": limit}

# Inject using Depends
@app.get("/users/")
async def list_users(pagination: Annotated[dict, Depends(get_pagination)]):
    return {"pagination": pagination, "users": []}

@app.get("/products/")
async def list_products(pagination: Annotated[dict, Depends(get_pagination)]):
    return {"pagination": pagination, "products": []}


# ─── Authentication dependency ────────────────────────────────────────────────
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # In real app: decode JWT, look up user in DB
    if token != "valid-token-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user_id": 1, "username": "alice", "role": "admin"}

@app.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


# ─── Database session dependency (SQLAlchemy pattern) ────────────────────────
# from database import SessionLocal
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db           # provide db session to route
#     finally:
#         db.close()         # always close, even on exception
#
# @app.get("/users/{id}")
# async def get_user(id: int, db: Session = Depends(get_db)):
#     return db.query(User).filter(User.id == id).first()


# ─── Chained / nested dependencies ───────────────────────────────────────────
def get_settings():
    return {"debug": False, "max_connections": 10}

def get_db_connection(settings: dict = Depends(get_settings)):
    # Use settings to configure DB
    return {"connected": True, "max_conn": settings["max_connections"]}

@app.get("/status")
async def app_status(db: dict = Depends(get_db_connection)):
    return db
```

---

## 📌 Topic 5: Middleware

### 🔹 What is Middleware?

**Middleware** is a function that runs **before every request** and **after every response**. It wraps the entire request/response cycle.

**Use cases:** Logging, authentication, CORS, rate limiting, request timing, error tracking.

```
Request → [Middleware 1] → [Middleware 2] → Route Handler
Response ← [Middleware 1] ← [Middleware 2] ← Route Handler
```

---

### 🔹 Custom Middleware

```python
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI()


# ─── Method 1: @app.middleware decorator ─────────────────────────────────────
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add a unique request ID to every request."""
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id      # attach to request state

    response = await call_next(request)        # call actual route handler

    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing."""
    start = time.perf_counter()

    response = await call_next(request)

    elapsed = (time.perf_counter() - start) * 1000
    print(
        f"[{request.method}] {request.url.path} "
        f"→ {response.status_code} "
        f"({elapsed:.1f}ms)"
    )
    response.headers["X-Process-Time"] = f"{elapsed:.1f}ms"
    return response


# ─── Method 2: Class-based middleware ────────────────────────────────────────
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict = {}   # {ip: [timestamps]}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Clean old timestamps
        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if now - t < self.window_seconds
            ]
        else:
            self.requests[client_ip] = []

        # Check limit
        if len(self.requests[client_ip]) >= self.max_requests:
            return Response(
                content='{"detail": "Rate limit exceeded"}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(self.window_seconds)},
            )

        self.requests[client_ip].append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(
            self.max_requests - len(self.requests[client_ip])
        )
        return response


app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)


# ─── Built-in Middleware ──────────────────────────────────────────────────────
# CORS — allow cross-origin requests (browser to API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myfrontend.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# GZip — compress responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted host — prevent host header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["myapi.com", "localhost"])
```

---

## 📌 Topic 6: Exception Handling

### 🔹 HTTPException — Standard API Errors

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

fake_db = {1: {"name": "Alice"}, 2: {"name": "Bob"}}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
            headers={"X-Error": "UserNotFound"},  # optional custom headers
        )
    return fake_db[user_id]

# Response on error:
# HTTP 404
# {
#   "detail": "User with id 99 not found"
# }
```

---

### 🔹 Custom Exception Classes + Handlers

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()


# ─── Custom exception classes ─────────────────────────────────────────────────
class AppException(Exception):
    """Base exception for all app errors."""
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id):
        super().__init__(
            message=f"{resource} with id '{resource_id}' not found",
            status_code=404,
            error_code="NOT_FOUND",
        )

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=401, error_code="UNAUTHORIZED")

class ForbiddenException(AppException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message=message, status_code=403, error_code="FORBIDDEN")

class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=409, error_code="CONFLICT")

class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=422, error_code="VALIDATION_ERROR")


# ─── Register exception handlers ─────────────────────────────────────────────
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "path": str(request.url.path),
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Override default 422 response for better error messages."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors,
            }
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected exceptions."""
    print(f"Unexpected error: {exc}")   # log it
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            }
        }
    )


# ─── Using custom exceptions in routes ───────────────────────────────────────
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = fake_db.get(user_id)
    if not user:
        raise NotFoundException("User", user_id)   # clean, readable
    return user
```

---

## 🛠️ Practice: Complete User CRUD API

```python
# ─── Project Structure ────────────────────────────────────────────────────────
# user_api/
# ├── main.py          ← FastAPI app + routes
# ├── models.py        ← Pydantic schemas
# ├── database.py      ← In-memory "database"
# ├── exceptions.py    ← Custom exceptions
# └── dependencies.py  ← Shared dependencies
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════
# models.py — Pydantic Schemas
# ══════════════════════════════════════════════════════════

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(..., description="Valid email address")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.VIEWER
    is_active: bool = True

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("username")
    @classmethod
    def lowercase_username(cls, v: str) -> str:
        return v.lower()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="At least 8 characters")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """All fields optional — for PATCH requests."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v and ("@" not in v or "." not in v.split("@")[-1]):
            raise ValueError("Invalid email format")
        return v.lower() if v else v


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    users: list[UserResponse]


class MessageResponse(BaseModel):
    success: bool
    message: str


# ══════════════════════════════════════════════════════════
# database.py — In-memory Database
# ══════════════════════════════════════════════════════════

from datetime import datetime
from typing import Optional
import hashlib


class InMemoryDB:
    """Simulates a database with an in-memory dict."""

    def __init__(self):
        self._users: dict[int, dict] = {}
        self._next_id: int = 1
        self._seed()   # add sample data

    def _seed(self):
        """Add initial data."""
        import hashlib
        sample_users = [
            {"username": "admin", "email": "admin@app.com", "full_name": "Admin User",
             "role": "admin", "password": "Admin@123"},
            {"username": "alice", "email": "alice@app.com", "full_name": "Alice Smith",
             "role": "editor", "password": "Alice@123"},
        ]
        for u in sample_users:
            self.create_user(u)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, data: dict) -> dict:
        now = datetime.now()
        user = {
            "id": self._next_id,
            "username": data["username"],
            "email": data["email"],
            "full_name": data["full_name"],
            "role": data.get("role", "viewer"),
            "is_active": data.get("is_active", True),
            "password_hash": self._hash_password(data["password"]),
            "created_at": now,
            "updated_at": now,
        }
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        return self._users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return next((u for u in self._users.values() if u["email"] == email), None)

    def get_user_by_username(self, username: str) -> Optional[dict]:
        return next((u for u in self._users.values() if u["username"] == username), None)

    def get_all_users(
        self,
        skip: int = 0,
        limit: int = 10,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        users = list(self._users.values())

        if role:
            users = [u for u in users if u["role"] == role]
        if is_active is not None:
            users = [u for u in users if u["is_active"] == is_active]
        if search:
            s = search.lower()
            users = [u for u in users if s in u["username"] or s in u["email"] or s in u["full_name"]]

        total = len(users)
        return users[skip: skip + limit], total

    def update_user(self, user_id: int, updates: dict) -> Optional[dict]:
        user = self._users.get(user_id)
        if not user:
            return None
        updates = {k: v for k, v in updates.items() if v is not None}
        user.update(updates)
        user["updated_at"] = datetime.now()
        return user

    def delete_user(self, user_id: int) -> bool:
        if user_id not in self._users:
            return False
        del self._users[user_id]
        return True

    def verify_password(self, user_id: int, password: str) -> bool:
        user = self._users.get(user_id)
        if not user:
            return False
        return user["password_hash"] == self._hash_password(password)

    @property
    def count(self) -> int:
        return len(self._users)


# Singleton instance
db = InMemoryDB()


# ══════════════════════════════════════════════════════════
# exceptions.py — Custom Exceptions
# ══════════════════════════════════════════════════════════

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, resource: str, identifier):
        super().__init__(f"{resource} '{identifier}' not found", 404, "NOT_FOUND")

class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(message, 409, "CONFLICT")

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, 401, "UNAUTHORIZED")

class ForbiddenException(AppException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403, "FORBIDDEN")


# ══════════════════════════════════════════════════════════
# dependencies.py — Shared Dependencies
# ══════════════════════════════════════════════════════════

from fastapi import Depends, Header, Query
from typing import Annotated, Optional


def get_db_instance():
    """Returns the database instance."""
    return db


def get_pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
):
    return {"skip": skip, "limit": limit}


def get_api_key(x_api_key: Optional[str] = Header(None)):
    """Simple API key authentication."""
    VALID_API_KEYS = {"dev-key-123", "prod-key-xyz"}
    if not x_api_key or x_api_key not in VALID_API_KEYS:
        raise UnauthorizedException("Invalid or missing API key")
    return x_api_key


DBDep = Annotated[InMemoryDB, Depends(get_db_instance)]
PaginationDep = Annotated[dict, Depends(get_pagination)]
AuthDep = Annotated[str, Depends(get_api_key)]


# ══════════════════════════════════════════════════════════
# main.py — Full FastAPI Application
# ══════════════════════════════════════════════════════════

import time
import uuid
from fastapi import FastAPI, Request, status, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional


# ─── App Setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="User Management API",
    description="""
## User CRUD API

A complete User Management system with:
- ✅ Create, Read, Update, Delete users
- ✅ Input validation via Pydantic
- ✅ Custom error responses
- ✅ Pagination and filtering
- ✅ API key authentication
    """,
    version="1.0.0",
    contact={"name": "API Support", "email": "support@example.com"},
)


# ─── Middleware ────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_request_metadata(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8].upper()
    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed_ms:.1f}ms"

    print(f"[{request_id}] {request.method} {request.url.path} → {response.status_code} ({elapsed_ms:.1f}ms)")
    return response


# ─── Exception Handlers ───────────────────────────────────────────────────────
@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"code": exc.error_code, "message": exc.message},
        },
    )

@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    errors = [
        {"field": " → ".join(str(l) for l in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": {"code": "VALIDATION_ERROR", "details": errors}},
    )

@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception):
    print(f"Unexpected: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Something went wrong"}},
    )


# ─── Lifespan (startup/shutdown events) ──────────────────────────────────────
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting User API...")
    print(f"   Database initialized with {db.count} users")
    yield
    print("🛑 Shutting down User API...")

app.router.lifespan_context = lifespan


# ─── Health & Info ────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "name": "User Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "total_users": db.count,
        "timestamp": datetime.now().isoformat(),
    }


# ─── CREATE User — POST /users ────────────────────────────────────────────────
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create a new user",
    description="Register a new user. Username and email must be unique.",
)
async def create_user(user_data: UserCreate, database: DBDep):
    # Check for duplicate email
    if database.get_user_by_email(user_data.email):
        raise ConflictException(f"Email '{user_data.email}' is already registered")

    # Check for duplicate username
    if database.get_user_by_username(user_data.username):
        raise ConflictException(f"Username '{user_data.username}' is already taken")

    # Create user
    created = database.create_user(user_data.model_dump())
    return created


# ─── GET All Users — GET /users ───────────────────────────────────────────────
@app.get(
    "/users",
    response_model=UserListResponse,
    tags=["Users"],
    summary="List all users",
)
async def list_users(
    database: DBDep,
    pagination: PaginationDep,
    role: Optional[UserRole] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, min_length=2, description="Search username/email/name"),
):
    users, total = database.get_all_users(
        skip=pagination["skip"],
        limit=pagination["limit"],
        role=role.value if role else None,
        is_active=is_active,
        search=search,
    )
    return {
        "total": total,
        "skip": pagination["skip"],
        "limit": pagination["limit"],
        "users": users,
    }


# ─── GET Single User — GET /users/{user_id} ───────────────────────────────────
@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Get user by ID",
)
async def get_user(user_id: int, database: DBDep):
    user = database.get_user_by_id(user_id)
    if not user:
        raise NotFoundException("User", user_id)
    return user


# ─── FULL UPDATE — PUT /users/{user_id} ──────────────────────────────────────
@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Fully update a user",
)
async def replace_user(user_id: int, user_data: UserCreate, database: DBDep):
    existing = database.get_user_by_id(user_id)
    if not existing:
        raise NotFoundException("User", user_id)

    # Check email conflict (exclude current user)
    email_owner = database.get_user_by_email(user_data.email)
    if email_owner and email_owner["id"] != user_id:
        raise ConflictException(f"Email '{user_data.email}' is used by another account")

    updated = database.update_user(user_id, user_data.model_dump())
    return updated


# ─── PARTIAL UPDATE — PATCH /users/{user_id} ─────────────────────────────────
@app.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Partially update a user",
    description="Update only the provided fields. Other fields remain unchanged.",
)
async def update_user(user_id: int, user_data: UserUpdate, database: DBDep):
    existing = database.get_user_by_id(user_id)
    if not existing:
        raise NotFoundException("User", user_id)

    if user_data.email:
        email_owner = database.get_user_by_email(user_data.email)
        if email_owner and email_owner["id"] != user_id:
            raise ConflictException(f"Email '{user_data.email}' is used by another account")

    updates = user_data.model_dump(exclude_none=True)   # only provided fields
    updated = database.update_user(user_id, updates)
    return updated


# ─── DELETE User — DELETE /users/{user_id} ───────────────────────────────────
@app.delete(
    "/users/{user_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Delete a user",
)
async def delete_user(user_id: int, database: DBDep):
    existing = database.get_user_by_id(user_id)
    if not existing:
        raise NotFoundException("User", user_id)

    database.delete_user(user_id)
    return {"success": True, "message": f"User '{existing['username']}' deleted successfully"}


# ─── ACTIVATE / DEACTIVATE ────────────────────────────────────────────────────
@app.patch(
    "/users/{user_id}/activate",
    response_model=UserResponse,
    tags=["Users"],
    summary="Activate a user account",
)
async def activate_user(user_id: int, database: DBDep):
    user = database.get_user_by_id(user_id)
    if not user:
        raise NotFoundException("User", user_id)
    updated = database.update_user(user_id, {"is_active": True})
    return updated

@app.patch(
    "/users/{user_id}/deactivate",
    response_model=UserResponse,
    tags=["Users"],
    summary="Deactivate a user account",
)
async def deactivate_user(user_id: int, database: DBDep):
    user = database.get_user_by_id(user_id)
    if not user:
        raise NotFoundException("User", user_id)
    updated = database.update_user(user_id, {"is_active": False})
    return updated


# ─── Run directly ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## 📋 API Reference Summary

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `GET` | `/` | API info | 200 |
| `GET` | `/health` | Health check | 200 |
| `POST` | `/users` | Create user | 201 |
| `GET` | `/users` | List all users (paginate, filter, search) | 200 |
| `GET` | `/users/{id}` | Get user by ID | 200 |
| `PUT` | `/users/{id}` | Full replace user | 200 |
| `PATCH` | `/users/{id}` | Partial update user | 200 |
| `DELETE` | `/users/{id}` | Delete user | 200 |
| `PATCH` | `/users/{id}/activate` | Activate account | 200 |
| `PATCH` | `/users/{id}/deactivate` | Deactivate account | 200 |

---

## 🧪 Testing the API

```bash
# Run the server
uvicorn main:app --reload

# ─── Create a user ───────────────────────────────────────
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john99",
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "Secret@123",
    "role": "viewer"
  }'

# ─── List all users ───────────────────────────────────────
curl http://localhost:8000/users
curl "http://localhost:8000/users?skip=0&limit=5&role=admin"
curl "http://localhost:8000/users?search=alice"

# ─── Get user by ID ──────────────────────────────────────
curl http://localhost:8000/users/1

# ─── Partial update ───────────────────────────────────────
curl -X PATCH http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Alice Updated", "role": "admin"}'

# ─── Delete user ──────────────────────────────────────────
curl -X DELETE http://localhost:8000/users/1

# ─── Trigger validation error ─────────────────────────────
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "a", "email": "invalid", "password": "weak"}'
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What is FastAPI and why use it over Flask?**  
A: FastAPI is an async Python web framework with built-in Pydantic validation, automatic Swagger/ReDoc docs, type-hint driven routing, and near-Go performance. Flask needs manual validation, has no auto docs, and limited async support.

**Q: What is Pydantic and what does it do?**  
A: Pydantic is a data validation library using Python type hints. It validates and parses incoming data, raises detailed errors on invalid input, and serializes Python objects to JSON. FastAPI uses it for request bodies and response models.

**Q: What is the difference between PUT and PATCH?**  
A: `PUT` is a full replacement — you send the complete resource. `PATCH` is partial update — you send only the fields to change. In practice, use `UserUpdate` model with all Optional fields for PATCH.

**Q: What is Dependency Injection in FastAPI?**  
A: `Depends()` lets you declare reusable logic (auth, DB sessions, pagination) as dependencies. FastAPI automatically resolves and injects them into route handlers. Dependencies can depend on other dependencies (chaining).

**Q: What is middleware in FastAPI?**  
A: Code that runs before every request and after every response. Used for logging, CORS, rate limiting, auth checks, request timing. Added via `@app.middleware("http")` or `app.add_middleware()`.

**Q: How do you handle errors in FastAPI?**  
A: Three ways: `HTTPException` for quick HTTP errors, custom exception classes + `@app.exception_handler()` for structured error responses, and overriding `RequestValidationError` handler for custom 422 messages.

**Q: What is `response_model` in FastAPI?**  
A: It tells FastAPI to filter and validate the response through a Pydantic model. Extra fields are removed. It also generates the response schema in docs. Without it, whatever you return is sent as-is.

**Q: What does `model_dump(exclude_none=True)` do?**  
A: It converts a Pydantic model to a dict, but excludes fields that are `None`. Essential for PATCH endpoints — only apply updates for fields the client actually provided.

**Q: What is Uvicorn?**  
A: Uvicorn is an ASGI server that runs FastAPI apps. ASGI (Async Server Gateway Interface) is the async successor to WSGI. `uvicorn main:app --reload` starts the server with hot-reload.

**Q: How do you add authentication to FastAPI?**  
A: Use `Depends()` with a function that checks API keys (from headers) or JWT tokens (via `python-jose` library). The dependency raises `401 Unauthorized` if invalid. Apply to individual routes or use `dependencies=[]` on routers.

---

## 📝 Key Takeaways

1. **FastAPI** = async + Pydantic + auto docs — fastest Python API framework
2. **Path params** `{id}` → declared in function signature with type hint → auto validated
3. **Query params** → function args with defaults → `?skip=0&limit=10`
4. **Request body** → Pydantic model as function parameter → auto parsed + validated
5. **Pydantic `Field()`** → add constraints (`gt`, `lt`, `min_length`, `pattern`, `regex`)
6. **`@field_validator`** → single field validation | **`@model_validator`** → cross-field validation
7. **`Depends()`** → inject reusable logic (auth, DB, pagination) into any route
8. **Middleware** → wraps every request/response — CORS, logging, rate-limiting
9. **Custom exception handler** → consistent structured error responses across the API
10. **`response_model`** → controls what goes OUT | **`status_code`** → HTTP code on success
11. **PUT** = full replace (all fields required) | **PATCH** = partial update (all fields optional)
12. **Auto docs** at `/docs` (Swagger) and `/redoc` (ReDoc) — zero configuration needed

---

*Day 6 Complete ✅ → Move to Day 7: Database + SQL + SQLAlchemy + Final Prep*

---
---
---
---
---

# 📅 Day 8 — Missing Topics (Must Know)
> **Goal:** Fill all gaps — stand out in every round  
> **Time:** 2 hrs Concepts → 2 hrs Coding → 1 hr Revision

---

## 📌 Topic 1: List / Dict / Set Comprehensions

### 🔹 Why Comprehensions?

Comprehensions are the most **Pythonic** way to create collections. Every interviewer expects you to write them fluently. They are faster than loops and more readable.

```python
# ❌ Non-Pythonic — loop approach
squares = []
for x in range(10):
    squares.append(x ** 2)

# ✅ Pythonic — comprehension
squares = [x ** 2 for x in range(10)]
```

---

### 🔹 List Comprehension

```python
# Basic syntax
# [expression for item in iterable if condition]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Simple transform
squares = [x ** 2 for x in numbers]
print(squares)   # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# With condition (filter)
evens = [x for x in numbers if x % 2 == 0]
print(evens)     # [2, 4, 6, 8, 10]

# Transform + filter
even_squares = [x ** 2 for x in numbers if x % 2 == 0]
print(even_squares)   # [4, 16, 36, 64, 100]

# If-else inside (ternary — goes BEFORE for)
labels = ["even" if x % 2 == 0 else "odd" for x in numbers]
print(labels)    # ['odd', 'even', 'odd', 'even', ...]

# Nested loops
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)      # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# String processing
words = ["hello", "world", "python"]
upper_long = [w.upper() for w in words if len(w) > 4]
print(upper_long)   # ['HELLO', 'WORLD', 'PYTHON']

# Nested list comprehension (create matrix)
grid = [[row * col for col in range(1, 4)] for row in range(1, 4)]
print(grid)
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

---

### 🔹 Dict Comprehension

```python
# Basic syntax
# {key_expr: value_expr for item in iterable if condition}

# Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)    # {1: 'a', 2: 'b', 3: 'c'}

# Transform values
prices = {"apple": 100, "banana": 50, "cherry": 200}
discounted = {k: v * 0.9 for k, v in prices.items()}
print(discounted)  # {'apple': 90.0, 'banana': 45.0, 'cherry': 180.0}

# Filter + transform
expensive = {k: v for k, v in prices.items() if v > 75}
print(expensive)   # {'apple': 100, 'cherry': 200}

# From two lists using zip
keys = ["name", "age", "city"]
vals = ["Alice", 25, "Delhi"]
user = {k: v for k, v in zip(keys, vals)}
print(user)        # {'name': 'Alice', 'age': 25, 'city': 'Delhi'}

# Word frequency
sentence = "the quick brown fox jumps over the lazy dog the"
freq = {word: sentence.split().count(word) for word in set(sentence.split())}
print(freq)        # {'the': 3, 'quick': 1, 'brown': 1, ...}

# Index map
words = ["apple", "banana", "cherry"]
index_map = {word: i for i, word in enumerate(words)}
print(index_map)   # {'apple': 0, 'banana': 1, 'cherry': 2}
```

---

### 🔹 Set Comprehension

```python
# Basic syntax
# {expression for item in iterable if condition}

numbers = [1, 2, 2, 3, 3, 3, 4, 5, 5]

# Unique squares
unique_squares = {x ** 2 for x in numbers}
print(unique_squares)    # {1, 4, 9, 16, 25} — no duplicates

# Unique first letters
words = ["apple", "ant", "banana", "berry", "cherry"]
first_letters = {w[0] for w in words}
print(first_letters)     # {'a', 'b', 'c'}

# Unique lengths
lengths = {len(w) for w in ["hello", "hi", "hey", "world", "python"]}
print(lengths)           # {2, 3, 5, 6}
```

---

### 🔹 Generator Expression

```python
# Same as list comprehension but LAZY — uses () not []
# Doesn't compute all values at once — memory efficient

import sys

# List comprehension — all in memory
lc = [x ** 2 for x in range(1_000_000)]
print(sys.getsizeof(lc))    # ~8.5 MB

# Generator expression — lazy
ge = (x ** 2 for x in range(1_000_000))
print(sys.getsizeof(ge))    # ~104 bytes

# Use when you only need to iterate once or pass to a function
total = sum(x ** 2 for x in range(1000))      # no extra list created
maximum = max(len(w) for w in ["hi", "hello", "hey"])
filtered = list(x for x in range(20) if x % 3 == 0)
print(filtered)    # [0, 3, 6, 9, 12, 15, 18]
```

---

### 📊 All 4 Comprehension Types

```python
data = [1, 2, 3, 4, 5]

list_comp  = [x * 2 for x in data]          # list  → [2, 4, 6, 8, 10]
set_comp   = {x * 2 for x in data}          # set   → {2, 4, 6, 8, 10}
dict_comp  = {x: x * 2 for x in data}       # dict  → {1:2, 2:4, 3:6, 4:8, 5:10}
gen_expr   = (x * 2 for x in data)          # generator (lazy)

print(type(list_comp))    # <class 'list'>
print(type(set_comp))     # <class 'set'>
print(type(dict_comp))    # <class 'dict'>
print(type(gen_expr))     # <class 'generator'>
```

---

## 📌 Topic 2: String Methods (Must Know)

### 🔹 The Most Important String Methods

```python
s = "  Hello, World! Python is awesome.  "

# ─── Whitespace & Case ────────────────────────────────────────────────────────
s.strip()           # "Hello, World! Python is awesome."  (both sides)
s.lstrip()          # "Hello, World! Python is awesome.  " (left only)
s.rstrip()          # "  Hello, World! Python is awesome." (right only)

s.upper()           # "  HELLO, WORLD! PYTHON IS AWESOME.  "
s.lower()           # "  hello, world! python is awesome.  "
s.title()           # "  Hello, World! Python Is Awesome.  "
s.capitalize()      # "  hello, world! python is awesome.  " (first char upper)
s.swapcase()        # "  hELLO, wORLD! pYTHON IS AWESOME.  "

# ─── Search & Check ───────────────────────────────────────────────────────────
s = "Hello, World!"
s.find("World")         # 7  (index of first match, -1 if not found)
s.rfind("l")            # 10 (rightmost match)
s.index("World")        # 7  (like find but raises ValueError if not found)
s.count("l")            # 3  (count occurrences)

s.startswith("Hello")   # True
s.endswith("!")         # True
s.startswith(("Hi", "Hello"))  # True — tuple of options

"hello123".isalnum()    # True  (all alphanumeric)
"hello".isalpha()       # True  (all letters)
"12345".isdigit()       # True  (all digits)
"   ".isspace()         # True  (all whitespace)
"Hello World".istitle() # True  (title case)
"hello".islower()       # True
"HELLO".isupper()       # True

# ─── Replace & Split ──────────────────────────────────────────────────────────
s = "Hello, World! Hello!"
s.replace("Hello", "Hi")          # "Hi, World! Hi!"
s.replace("Hello", "Hi", 1)       # "Hi, World! Hello!" (max 1 replacement)

# split
"a,b,c,d".split(",")              # ['a', 'b', 'c', 'd']
"a,b,c,d".split(",", 2)           # ['a', 'b', 'c,d'] (max 2 splits)
"hello world".split()             # ['hello', 'world'] (split on whitespace)
"line1\nline2\nline3".splitlines() # ['line1', 'line2', 'line3']

# join — opposite of split
",".join(["a", "b", "c"])         # "a,b,c"
" ".join(["Hello", "World"])      # "Hello World"
"".join(["P", "y", "t", "h", "o", "n"])  # "Python"
"\n".join(["line1", "line2"])     # "line1\nline2"

# ─── Formatting ───────────────────────────────────────────────────────────────
name, age, score = "Alice", 25, 98.567

# f-strings (preferred — Python 3.6+)
f"Name: {name}, Age: {age}"              # "Name: Alice, Age: 25"
f"Score: {score:.2f}"                    # "Score: 98.57" (2 decimal places)
f"Age: {age:05d}"                        # "Age: 00025" (zero-padded)
f"{'left':<10}"                          # "left      " (left align, width 10)
f"{'right':>10}"                         # "     right" (right align)
f"{'center':^10}"                        # "  center  " (center align)
f"{1_000_000:,}"                         # "1,000,000" (thousand separator)
f"{0.1234:.1%}"                          # "12.3%" (percentage)
f"{name!r}"                              # "'Alice'" (repr)
f"{name!u}"                              # debugging: f"{name=}" → "name='Alice'"

# .format() method
"Hello, {}! You are {} years old.".format(name, age)
"Hello, {name}! Age: {age}".format(name="Alice", age=25)
"{0} {1} {0}".format("ha", "ho")       # "ha ho ha"

# ─── Slicing ─────────────────────────────────────────────────────────────────
s = "Python"
s[0]       # 'P'
s[-1]      # 'n'
s[1:4]     # 'yth'
s[:3]      # 'Pyt'
s[3:]      # 'hon'
s[::2]     # 'Pto'  (every 2nd)
s[::-1]    # 'nohtyP' (reversed)

# ─── Padding ──────────────────────────────────────────────────────────────────
"42".zfill(5)          # "00042" (zero-fill to width 5)
"hi".ljust(10)         # "hi        " (left justify)
"hi".rjust(10)         # "        hi" (right justify)
"hi".center(10)        # "    hi    " (center)
"hi".center(10, "*")   # "****hi****" (center with fill char)
```

---

## 📌 Topic 3: `collections` Module

### 🔹 Why `collections`?

The `collections` module provides **specialized container types** that are faster, cleaner, and more expressive than plain dicts/lists for specific use cases. Asked in almost every Python interview.

---

### 🔹 `Counter` — Count Frequencies

```python
from collections import Counter

# Count elements
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c)                     # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(c["apple"])            # 3
print(c["mango"])            # 0 (no KeyError for missing keys!)

# From string
letter_count = Counter("mississippi")
print(letter_count)         # Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})

# Most common
print(c.most_common(2))     # [('apple', 3), ('banana', 2)]
print(c.most_common()[:-3:-1])  # least common 2

# Arithmetic
c1 = Counter(["a", "b", "a", "c"])
c2 = Counter(["a", "b", "b", "d"])

print(c1 + c2)    # Counter({'a': 3, 'b': 3, 'c': 1, 'd': 1})
print(c1 - c2)    # Counter({'a': 1, 'c': 1}) — subtract, drop negatives
print(c1 & c2)    # Counter({'a': 1, 'b': 1}) — intersection (min)
print(c1 | c2)    # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1}) — union (max)

# Update
c.update(["apple", "mango"])
print(c["apple"])   # 4
print(c["mango"])   # 1

# elements() — iterate with repetition
print(list(Counter("aab").elements()))   # ['a', 'a', 'b']

# Real-world use: find most frequent character
def most_frequent_char(s):
    return Counter(s).most_common(1)[0][0]

print(most_frequent_char("aabbcccdd"))   # 'c'

# Check if anagram
def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

print(is_anagram("listen", "silent"))    # True
print(is_anagram("hello", "world"))      # False
```

---

### 🔹 `defaultdict` — Dict with Default Values

```python
from collections import defaultdict

# Regular dict — KeyError on missing key
d = {}
# d["missing_key"]   # ❌ KeyError

# defaultdict — creates default value automatically
d = defaultdict(int)        # default value: int() = 0
d["count"] += 1
d["count"] += 1
d["new_key"] += 5
print(d)    # defaultdict(<class 'int'>, {'count': 2, 'new_key': 5})

# defaultdict with list — group items
d = defaultdict(list)
data = [("fruit", "apple"), ("veggie", "carrot"), ("fruit", "banana"), ("veggie", "potato")]

for category, item in data:
    d[category].append(item)

print(dict(d))   # {'fruit': ['apple', 'banana'], 'veggie': ['carrot', 'potato']}

# defaultdict with set
d = defaultdict(set)
pairs = [("a", 1), ("b", 2), ("a", 3), ("b", 2), ("a", 1)]
for k, v in pairs:
    d[k].add(v)
print(dict(d))   # {'a': {1, 3}, 'b': {2}}

# defaultdict with custom default
d = defaultdict(lambda: "N/A")
d["name"] = "Alice"
print(d["name"])     # Alice
print(d["age"])      # N/A (default)

# Word grouping — group words by first letter
words = ["apple", "ant", "banana", "berry", "cherry", "avocado"]
grouped = defaultdict(list)
for w in words:
    grouped[w[0]].append(w)
print(dict(grouped))
# {'a': ['apple', 'ant', 'avocado'], 'b': ['banana', 'berry'], 'c': ['cherry']}

# Graph adjacency list
graph = defaultdict(list)
edges = [(1, 2), (1, 3), (2, 4), (3, 4)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
print(dict(graph))  # {1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]}
```

---

### 🔹 `deque` — Double-Ended Queue

```python
from collections import deque

# deque = double-ended queue
# O(1) append/pop from BOTH ends (list pop(0) is O(n))

d = deque([1, 2, 3, 4, 5])

# Append / pop
d.append(6)         # add to right → deque([1,2,3,4,5,6])
d.appendleft(0)     # add to left  → deque([0,1,2,3,4,5,6])
d.pop()             # remove right → 6
d.popleft()         # remove left  → 0

# Extend
d.extend([7, 8])          # add multiple to right
d.extendleft([-1, -2])    # add multiple to left (each one by one, reversed!)
print(d)                  # deque([-2, -1, 1, 2, 3, 4, 5, 7, 8])

# Rotate
d = deque([1, 2, 3, 4, 5])
d.rotate(2)    # rotate right by 2
print(d)       # deque([4, 5, 1, 2, 3])
d.rotate(-2)   # rotate left by 2
print(d)       # deque([1, 2, 3, 4, 5])

# maxlen — fixed size, auto-discards old items (sliding window!)
recent = deque(maxlen=3)
for i in range(6):
    recent.append(i)
    print(list(recent))
# [0]
# [0, 1]
# [0, 1, 2]
# [1, 2, 3]  ← 0 discarded
# [2, 3, 4]  ← 1 discarded
# [3, 4, 5]  ← 2 discarded

# Use case: BFS queue
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []

    while queue:
        node = queue.popleft()   # O(1) — faster than list.pop(0)
        result.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result

graph = {1: [2, 3], 2: [4], 3: [4], 4: []}
print(bfs(graph, 1))   # [1, 2, 3, 4]
```

---

### 🔹 `namedtuple` — Tuple with Named Fields

```python
from collections import namedtuple

# Regular tuple — hard to read
point = (3, 4)
print(point[0], point[1])   # 3 4 — what does each mean?

# namedtuple — self-documenting
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)     # 3 4 — clear!
print(p[0], p[1])   # 3 4 — still works as a tuple
print(p)            # Point(x=3, y=4)

# Immutable like tuples
# p.x = 10   # ❌ AttributeError

# Can unpack
x, y = p
print(x, y)         # 3 4

# More examples
Person = namedtuple("Person", ["name", "age", "email"])
alice = Person("Alice", 25, "alice@example.com")
print(alice.name)    # Alice
print(alice._asdict())  # {'name': 'Alice', 'age': 25, 'email': 'alice@example.com'}

# _replace — create new instance with changes (immutable pattern)
older_alice = alice._replace(age=26)
print(older_alice)   # Person(name='Alice', age=26, email='alice@example.com')

# Default values
Config = namedtuple("Config", ["host", "port", "debug"], defaults=["localhost", 8000, False])
cfg = Config()
print(cfg)    # Config(host='localhost', port=8000, debug=False)

# CSV → namedtuples
import csv
Employee = namedtuple("Employee", ["name", "dept", "salary"])
# with open("employees.csv") as f:
#     reader = csv.reader(f)
#     employees = [Employee(*row) for row in reader]
```

---

### 🔹 `OrderedDict` — Dict That Remembers Order

```python
from collections import OrderedDict

# In Python 3.7+ regular dicts maintain insertion order
# OrderedDict has extra features

od = OrderedDict()
od["b"] = 2
od["a"] = 1
od["c"] = 3
print(od)   # OrderedDict([('b', 2), ('a', 1), ('c', 3)])

# move_to_end
od.move_to_end("b")         # move 'b' to end
od.move_to_end("c", last=False)  # move 'c' to front
print(od)   # OrderedDict([('c', 3), ('a', 1), ('b', 2)])

# popitem — LIFO (last) or FIFO (first)
od.popitem(last=True)    # remove last item
od.popitem(last=False)   # remove first item

# Order matters for equality (unlike regular dict)
d1 = OrderedDict([("a", 1), ("b", 2)])
d2 = OrderedDict([("b", 2), ("a", 1)])
print(d1 == d2)   # False — order matters!

# LRU Cache implementation using OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # remove least recently used

lru = LRUCache(3)
lru.put(1, "a"); lru.put(2, "b"); lru.put(3, "c")
print(lru.get(1))   # 'a' — 1 is now most recent
lru.put(4, "d")     # evicts 2 (least recently used)
print(lru.get(2))   # -1 — evicted!
```

---

## 📌 Topic 4: `itertools` Module

### 🔹 Why `itertools`?

`itertools` provides **memory-efficient** tools for working with iterables. These come up in interviews for data processing, combinations, and pipeline problems.

```python
import itertools
```

---

### 🔹 Infinite Iterators

```python
import itertools

# count — infinite counter
for i in itertools.count(10, 5):    # start=10, step=5
    if i > 30: break
    print(i, end=" ")   # 10 15 20 25 30

# cycle — repeat iterable infinitely
status = itertools.cycle(["active", "idle", "sleeping"])
for _ in range(6):
    print(next(status), end=" ")   # active idle sleeping active idle sleeping

# repeat — repeat a value N times (or infinitely)
print(list(itertools.repeat("ha", 3)))   # ['ha', 'ha', 'ha']
```

---

### 🔹 Combination & Permutation

```python
import itertools

items = ["A", "B", "C"]

# permutations — ordered arrangements
print(list(itertools.permutations(items)))
# [('A','B','C'), ('A','C','B'), ('B','A','C'), ('B','C','A'), ('C','A','B'), ('C','B','A')]

print(list(itertools.permutations(items, 2)))   # length-2 permutations
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

# combinations — unordered selections (no repetition)
print(list(itertools.combinations(items, 2)))
# [('A','B'), ('A','C'), ('B','C')]

# combinations_with_replacement — can repeat
print(list(itertools.combinations_with_replacement(items, 2)))
# [('A','A'), ('A','B'), ('A','C'), ('B','B'), ('B','C'), ('C','C')]

# product — cartesian product (like nested loops)
print(list(itertools.product([1, 2], ["a", "b"])))
# [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

print(list(itertools.product([0, 1], repeat=3)))   # all 3-bit binary numbers
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
```

---

### 🔹 Slicing & Chaining

```python
import itertools

# chain — combine multiple iterables
combined = list(itertools.chain([1, 2], [3, 4], [5, 6]))
print(combined)    # [1, 2, 3, 4, 5, 6]

# chain.from_iterable — flatten one level
nested = [[1, 2], [3, 4], [5, 6]]
flat = list(itertools.chain.from_iterable(nested))
print(flat)        # [1, 2, 3, 4, 5, 6]

# islice — lazy slicing of any iterator
gen = (x ** 2 for x in itertools.count())   # infinite generator
first_5 = list(itertools.islice(gen, 5))
print(first_5)     # [0, 1, 4, 9, 16]

# islice(iterable, start, stop, step)
data = range(100)
every_10th = list(itertools.islice(data, 0, 50, 10))
print(every_10th)  # [0, 10, 20, 30, 40]

# takewhile — take while condition is True
nums = [1, 3, 5, 2, 7, 4, 6]
taken = list(itertools.takewhile(lambda x: x % 2 != 0, nums))
print(taken)       # [1, 3, 5] — stops at first even number

# dropwhile — drop while condition is True
dropped = list(itertools.dropwhile(lambda x: x % 2 != 0, nums))
print(dropped)     # [2, 7, 4, 6] — drops until first even, keeps rest

# compress — filter with boolean mask
data = ["a", "b", "c", "d", "e"]
mask = [1, 0, 1, 0, 1]
print(list(itertools.compress(data, mask)))   # ['a', 'c', 'e']
```

---

### 🔹 `groupby` — Group Consecutive Elements

```python
import itertools

# IMPORTANT: data must be sorted by the key first!
data = [
    {"name": "Alice", "dept": "Engineering"},
    {"name": "Bob", "dept": "Engineering"},
    {"name": "Charlie", "dept": "HR"},
    {"name": "Diana", "dept": "HR"},
    {"name": "Eve", "dept": "Marketing"},
]

# Sort first (groupby only groups CONSECUTIVE same-key items)
data.sort(key=lambda x: x["dept"])

for dept, employees in itertools.groupby(data, key=lambda x: x["dept"]):
    emp_list = [e["name"] for e in employees]
    print(f"{dept}: {emp_list}")
# Engineering: ['Alice', 'Bob']
# HR: ['Charlie', 'Diana']
# Marketing: ['Eve']

# Group numbers by even/odd
nums = sorted([1, 2, 3, 4, 5, 6], key=lambda x: x % 2)
for key, group in itertools.groupby(nums, key=lambda x: x % 2):
    label = "odd" if key else "even"
    print(f"{label}: {list(group)}")
# even: [2, 4, 6]
# odd: [1, 3, 5]
```

---

## 📌 Topic 5: `try` / `except` / `else` / `finally` — Full Syntax

### 🔹 Complete Exception Handling

```python
# Full syntax — all 4 clauses
try:
    result = 10 / 2          # code that might raise exception
except ZeroDivisionError as e:
    print(f"Math error: {e}")  # runs ONLY if ZeroDivisionError occurs
except (TypeError, ValueError) as e:
    print(f"Type/Value error: {e}")  # multiple exceptions in one handler
except Exception as e:
    print(f"Unexpected error: {e}")  # catches all other exceptions
else:
    print(f"Success! Result: {result}")  # runs ONLY if NO exception occurred
finally:
    print("This ALWAYS runs")  # runs no matter what (cleanup here)

# Clause execution rules:
# try succeeds      → try, else, finally
# try raises        → try, except (matching), finally (no else!)
# except raises     → try, except, finally (new exception propagates)
```

---

### 🔹 Exception Hierarchy

```python
# Python exception hierarchy (most common):
BaseException
├── SystemExit                  # sys.exit()
├── KeyboardInterrupt           # Ctrl+C
└── Exception                  # All regular exceptions
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── AttributeError          # obj.missing_attr
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError          # list[99]
    │   └── KeyError            # dict["missing"]
    ├── NameError               # undefined variable
    │   └── UnboundLocalError
    ├── OSError / IOError
    │   └── FileNotFoundError
    ├── RuntimeError
    │   └── RecursionError
    ├── StopIteration           # iterator exhausted
    ├── TypeError               # wrong type
    ├── ValueError              # right type, wrong value
    └── UnicodeError
        └── UnicodeDecodeError

# Always catch specific exceptions, not bare except:
# ❌ except:              # catches EVERYTHING including KeyboardInterrupt
# ✅ except Exception:    # catches all normal exceptions
# ✅ except ValueError:   # specific — best practice
```

---

### 🔹 Raising Exceptions

```python
# raise — raise an exception
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed!")
    return a / b

# raise with context (exception chaining)
def read_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Config file missing: {path}") from e
        #                                                   ↑
        # preserves original exception as __cause__

try:
    read_config("/nonexistent/config.json")
except RuntimeError as e:
    print(e)           # Config file missing: /nonexistent/config.json
    print(e.__cause__) # [Errno 2] No such file or directory

# re-raise current exception
def process(data):
    try:
        result = risky_operation(data)
    except Exception as e:
        print(f"Logging error: {e}")
        raise    # ← re-raise same exception without losing traceback


# raise from None — suppress context
def clean_raise():
    try:
        int("abc")
    except ValueError:
        raise ValueError("Expected a number") from None  # hides original

# Custom exception with extra info
class APIError(Exception):
    def __init__(self, message, status_code, endpoint):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint = endpoint

try:
    raise APIError("Not found", 404, "/users/99")
except APIError as e:
    print(e)              # Not found
    print(e.status_code)  # 404
    print(e.endpoint)     # /users/99
```

---

### 🔹 `else` and `finally` Deep Dive

```python
# ─── else — runs only when NO exception occurs ────────────────────────────────
def safe_open(filename):
    try:
        f = open(filename)
    except FileNotFoundError:
        print("File not found!")
        return None
    else:
        content = f.read()   # safe to do here — file opened successfully
        f.close()
        return content
    # else is preferred over putting code in try block
    # because it isolates "expected" errors from "unexpected" ones


# ─── finally — ALWAYS runs, even with return/break/continue ──────────────────
def with_return():
    try:
        print("try")
        return "from try"          # return won't skip finally!
    finally:
        print("finally runs!")     # this prints BEFORE the return

result = with_return()
# try
# finally runs!
print(result)   # "from try"

# Real use: resource cleanup
import sqlite3

def query_db(sql):
    conn = None
    try:
        conn = sqlite3.connect("mydb.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return []
    finally:
        if conn:
            conn.close()   # ALWAYS close connection
```

---

## 📌 Topic 6: Dataclasses

### 🔹 What is a Dataclass?

A **dataclass** automatically generates boilerplate code (`__init__`, `__repr__`, `__eq__`) for classes that primarily hold data.

```python
from dataclasses import dataclass, field, asdict, astuple
from typing import Optional, List
from datetime import datetime
```

---

### 🔹 Basic Dataclass vs Regular Class

```python
# Regular class — lots of boilerplate
class PersonManual:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r}, email={self.email!r})"

    def __eq__(self, other):
        return (self.name, self.age, self.email) == (other.name, other.age, other.email)


# Dataclass — same result, no boilerplate!
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str

p1 = Person("Alice", 25, "alice@example.com")
p2 = Person("Alice", 25, "alice@example.com")

print(p1)           # Person(name='Alice', age=25, email='alice@example.com')
print(p1 == p2)     # True (compares all fields)
print(repr(p1))     # Person(name='Alice', age=25, email='alice@example.com')
```

---

### 🔹 Dataclass Features

```python
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class Product:
    # Required fields (no default)
    name: str
    price: float

    # Optional with default
    category: str = "General"
    in_stock: bool = True
    discount: float = 0.0

    # ⚠️ Mutable defaults MUST use field(default_factory=...)
    tags: List[str] = field(default_factory=list)      # NOT tags: List = []
    metadata: dict = field(default_factory=dict)

    # Field with init=False — not in __init__, set in __post_init__
    created_at: datetime = field(default_factory=datetime.now, init=False)
    product_id: int = field(default=0, init=False)

    # repr=False — exclude from __repr__
    internal_code: str = field(default="", repr=False)

    # compare=False — exclude from __eq__ and __lt__
    last_updated: Optional[datetime] = field(default=None, compare=False)

    def __post_init__(self):
        """Runs after __init__ — for validation and computed fields."""
        if self.price < 0:
            raise ValueError(f"Price cannot be negative: {self.price}")
        if self.discount < 0 or self.discount > 100:
            raise ValueError("Discount must be 0–100")
        self.price = round(self.price, 2)

    @property
    def final_price(self):
        return self.price * (1 - self.discount / 100)

    def apply_discount(self, percent: float) -> "Product":
        """Return new product with discount applied (immutable style)."""
        from dataclasses import replace
        return replace(self, discount=percent)


# Usage
p = Product(name="Laptop", price=75000.50, tags=["electronics", "computer"])
print(p)
# Product(name='Laptop', price=75000.5, category='General', ...)
print(p.final_price)   # 75000.5

p2 = p.apply_discount(10)
print(p2.discount)     # 10
print(p2.final_price)  # 67500.45
```

---

### 🔹 Frozen, Ordered, Slots

```python
from dataclasses import dataclass

# frozen=True — immutable (hashable, can be dict key or set member)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(3, 4)
# p.x = 10   # ❌ FrozenInstanceError — cannot modify frozen instance

# Can use as dict key because it's hashable
distances = {Point(0, 0): 0, Point(3, 4): 5}
print(distances[Point(3, 4)])   # 5

# order=True — enables < > <= >= comparisons
@dataclass(order=True)
class Student:
    grade: int    # compared first
    name: str     # compared second (if grades are equal)

students = [Student(90, "Charlie"), Student(95, "Alice"), Student(90, "Bob")]
print(sorted(students))
# [Student(grade=90, name='Bob'), Student(grade=90, name='Charlie'), Student(grade=95, name='Alice')]

# slots=True (Python 3.10+) — uses __slots__ for memory efficiency
@dataclass(slots=True)
class Coordinate:
    x: float
    y: float
    z: float = 0.0
```

---

### 🔹 `asdict` and `astuple`

```python
from dataclasses import dataclass, asdict, astuple

@dataclass
class Address:
    street: str
    city: str
    country: str = "India"

@dataclass
class User:
    name: str
    age: int
    address: Address

u = User("Alice", 25, Address("123 MG Road", "Bengaluru"))

# Convert to dict (nested too!)
print(asdict(u))
# {'name': 'Alice', 'age': 25, 'address': {'street': '123 MG Road', 'city': 'Bengaluru', 'country': 'India'}}

# Convert to tuple
print(astuple(u))
# ('Alice', 25, ('123 MG Road', 'Bengaluru', 'India'))

# Great for JSON serialization
import json
print(json.dumps(asdict(u), indent=2))
```

---

## 📌 Topic 7: `functools` — `lru_cache` and `partial`

### 🔹 `lru_cache` — Built-in Memoization

```python
from functools import lru_cache
import time

# ─── Without cache — exponential time ────────────────────────────────────────
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# ─── With lru_cache — O(n) time ──────────────────────────────────────────────
@lru_cache(maxsize=None)   # maxsize=None → unlimited cache (functools.cache in 3.9+)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Speed difference
start = time.perf_counter()
print(fib_slow(35))   # 9227465 — takes ~3 seconds
print(f"Without cache: {time.perf_counter() - start:.3f}s")

start = time.perf_counter()
print(fib(35))        # 9227465 — instant
print(f"With cache: {time.perf_counter() - start:.6f}s")

# Cache info and clearing
print(fib.cache_info())    # CacheInfo(hits=..., misses=..., maxsize=None, currsize=...)
fib.cache_clear()          # clear the cache

# maxsize — LRU eviction (Least Recently Used)
@lru_cache(maxsize=128)    # keep last 128 unique calls
def expensive_api_call(user_id: int):
    time.sleep(0.1)   # simulate API call
    return {"id": user_id, "name": f"User {user_id}"}

# First call — miss (actual computation)
result1 = expensive_api_call(1)
# Second call — hit (returns cached result instantly)
result2 = expensive_api_call(1)

# Python 3.9+ — functools.cache (simpler, no maxsize)
from functools import cache

@cache
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

print(factorial(10))   # 3628800
print(factorial.cache_info())

# ⚠️ lru_cache requires hashable arguments
# @lru_cache
# def process(data: list): pass   # ❌ TypeError — list is not hashable
# Fix: use tuple instead of list
@lru_cache(maxsize=128)
def process(data: tuple):
    return sum(data)

print(process((1, 2, 3)))    # works!
```

---

### 🔹 `functools.partial` — Pre-fill Arguments

```python
from functools import partial

# partial — create new function with some args pre-filled
def power(base, exponent):
    return base ** exponent

# Pre-fill exponent
square = partial(power, exponent=2)
cube   = partial(power, exponent=3)

print(square(4))    # 16
print(cube(3))      # 27

# With built-in functions
from functools import partial

# int() with base argument
hex_to_int = partial(int, base=16)
bin_to_int = partial(int, base=2)

print(hex_to_int("ff"))      # 255
print(bin_to_int("1010"))    # 10

# With print
print_error = partial(print, "ERROR:", sep=" ", end="\n")
print_info  = partial(print, "INFO:", sep=" ", end="\n")

print_error("Something went wrong")    # ERROR: Something went wrong
print_info("Server started")           # INFO: Server started

# Real-world: configuring functions for map()
def multiply(x, factor):
    return x * factor

double = partial(multiply, factor=2)
triple = partial(multiply, factor=3)

data = [1, 2, 3, 4, 5]
print(list(map(double, data)))   # [2, 4, 6, 8, 10]
print(list(map(triple, data)))   # [3, 6, 9, 12, 15]
```

---

## 📌 Topic 8: Recursion

### 🔹 What is Recursion?

A function that **calls itself** to solve a smaller version of the same problem. Must have a **base case** (stop condition) to avoid infinite recursion.

```python
# Structure of every recursive function:
def recursive(problem):
    # 1. Base case — simplest version, return directly
    if problem is simple enough:
        return simple_answer

    # 2. Recursive case — break down and call self
    smaller = make_smaller(problem)
    return combine(recursive(smaller))
```

---

### 🔹 Classic Recursion Examples

```python
import sys
sys.setrecursionlimit(10000)   # default is 1000

# ─── Factorial ────────────────────────────────────────────────────────────────
def factorial(n):
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))   # 120
# factorial(5)
# = 5 * factorial(4)
# = 5 * 4 * factorial(3)
# = 5 * 4 * 3 * factorial(2)
# = 5 * 4 * 3 * 2 * factorial(1)
# = 5 * 4 * 3 * 2 * 1 = 120


# ─── Fibonacci ────────────────────────────────────────────────────────────────
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Optimized with memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)


# ─── Sum of list ──────────────────────────────────────────────────────────────
def recursive_sum(lst):
    if not lst:          # empty list → base case
        return 0
    return lst[0] + recursive_sum(lst[1:])

print(recursive_sum([1, 2, 3, 4, 5]))   # 15


# ─── Binary search ────────────────────────────────────────────────────────────
def binary_search(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left > right:     # base case: not found
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)

arr = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(arr, 7))    # 3 (index)
print(binary_search(arr, 4))    # -1 (not found)


# ─── Flatten nested list ──────────────────────────────────────────────────────
def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))   # recurse into nested
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], [5, 6], 7]))   # [1, 2, 3, 4, 5, 6, 7]


# ─── Power — fast exponentiation O(log n) ────────────────────────────────────
def fast_power(base, exp):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)
        return half * half          # square instead of multiplying exp times
    return base * fast_power(base, exp - 1)

print(fast_power(2, 10))    # 1024
```

---

## 📌 Topic 9: FastAPI — JWT Auth + `APIRouter`

### 🔹 JWT Authentication

```python
# pip install python-jose[cryptography] passlib[bcrypt]
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# ─── Config ───────────────────────────────────────────────────────────────────
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ─── Password hashing ─────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ─── JWT token ────────────────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ─── OAuth2 scheme ────────────────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ─── Fake user DB ─────────────────────────────────────────────────────────────
fake_users_db = {
    "alice": {"username": "alice", "hashed_password": hash_password("alice123"), "role": "admin"},
    "bob":   {"username": "bob",   "hashed_password": hash_password("bob123"),   "role": "viewer"},
}

# ─── Schemas ──────────────────────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserOut(BaseModel):
    username: str
    role: str

# ─── Dependencies ─────────────────────────────────────────────────────────────
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token)
    username = payload.get("sub")
    if not username or username not in fake_users_db:
        raise HTTPException(status_code=401, detail="User not found")
    return fake_users_db[username]

def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# ─── App and routes ───────────────────────────────────────────────────────────
app = FastAPI()

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
async def get_me(user: dict = Depends(get_current_user)):
    return user

@app.delete("/admin/users/{username}")
async def admin_delete_user(username: str, admin: dict = Depends(require_admin)):
    return {"message": f"User {username} deleted by {admin['username']}"}
```

---

### 🔹 `APIRouter` — Split Routes Across Files

```python
# ─── Real-world FastAPI project structure ─────────────────────────────────────
# app/
# ├── main.py
# ├── routers/
# │   ├── __init__.py
# │   ├── users.py
# │   ├── products.py
# │   └── auth.py
# └── dependencies.py

# ─── routers/users.py ────────────────────────────────────────────────────────
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/users",          # all routes prefixed with /users
    tags=["Users"],           # grouped in Swagger docs
    dependencies=[],          # apply to all routes in this router
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}

@router.post("/")
async def create_user():
    return {"id": 2, "name": "New User"}


# ─── routers/products.py ──────────────────────────────────────────────────────
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products():
    return [{"id": 1, "name": "Laptop"}]


# ─── routers/auth.py ──────────────────────────────────────────────────────────
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login():
    return {"token": "abc123"}

@router.post("/logout")
async def logout():
    return {"message": "Logged out"}


# ─── main.py — include all routers ───────────────────────────────────────────
from fastapi import FastAPI
# from routers import users, products, auth   # real import

app = FastAPI(title="My API", version="1.0.0")

# Include routers — each adds its routes to the app
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)

# Router with auth dependency applied to ALL its routes
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["Admin"],
#     dependencies=[Depends(require_admin)],   # all admin routes need auth
# )

@app.get("/")
async def root():
    return {"message": "API is running"}

# Final routes:
# GET  /users/
# GET  /users/{user_id}
# POST /users/
# GET  /products/
# POST /auth/login
# POST /auth/logout
```

---

## 📌 Topic 10: Abstract Base Classes (ABC)

### 🔹 What is ABC?

**Abstract Base Class (ABC)** defines a **contract** — a set of methods that ALL subclasses MUST implement. You cannot instantiate an ABC directly.

```python
from abc import ABC, abstractmethod

class Shape(ABC):   # inherit from ABC
    @abstractmethod
    def area(self) -> float:
        """All shapes MUST implement area()."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    # Non-abstract method — shared by all subclasses
    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


# Cannot instantiate ABC directly
try:
    s = Shape()   # ❌ TypeError: Can't instantiate abstract class
except TypeError as e:
    print(e)

# Must implement ALL abstract methods
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

# Concrete classes can be instantiated
c = Circle(5)
r = Rectangle(4, 6)

shapes = [c, r]
for shape in shapes:
    print(shape.describe())
# Circle: area=78.54, perimeter=31.42
# Rectangle: area=24.00, perimeter=20.00

# ABC + abstractmethod ensures the contract is enforced at class definition
class BadShape(Shape):
    def area(self):       # implements area but NOT perimeter
        return 0
    # ❌ TypeError when instantiated: Can't instantiate — perimeter not defined

# Abstract properties
class Vehicle(ABC):
    @property
    @abstractmethod
    def fuel_type(self) -> str:
        pass

    @abstractmethod
    def start(self) -> str:
        pass

class ElectricCar(Vehicle):
    @property
    def fuel_type(self):
        return "Electric"

    def start(self):
        return "Starting silently..."

ev = ElectricCar()
print(ev.fuel_type)   # Electric
print(ev.start())     # Starting silently...
```

---

## 🧠 Quick Revision — Interview Q&A

**Q: What are the 4 types of comprehensions in Python?**  
A: List `[x for x in ...]`, Set `{x for x in ...}`, Dict `{k: v for k, v in ...}`, Generator `(x for x in ...)`. Generator is lazy; the others build the collection immediately.

**Q: When would you use a generator expression over a list comprehension?**  
A: When you only need to iterate once and don't need to store all values in memory — like passing to `sum()`, `max()`, or processing large datasets.

**Q: What is `Counter` and when do you use it?**  
A: `Counter` is a dict subclass for counting hashable objects. Use it for frequency counts, finding most common elements, anagram checking. `Counter("hello").most_common(1)` → `[('l', 2)]`.

**Q: What is `defaultdict`?**  
A: A dict that auto-creates a default value for missing keys using a factory function. `defaultdict(list)` creates an empty list for any missing key — perfect for grouping.

**Q: What is the difference between `deque` and `list` for queue operations?**  
A: `list.pop(0)` is O(n) — shifts all elements. `deque.popleft()` is O(1). Use `deque` when you need to add/remove from both ends frequently.

**Q: What does the `else` clause in try/except do?**  
A: It runs ONLY when NO exception occurred in the try block. It's used to separate "expected failure" code from "post-success" code, keeping the try block minimal.

**Q: What does `finally` always do?**  
A: It ALWAYS runs — even if there's a `return`, `break`, or `continue` in the try/except. Use it for cleanup: closing files, releasing locks, closing DB connections.

**Q: What is a dataclass?**  
A: A decorator (`@dataclass`) that auto-generates `__init__`, `__repr__`, and `__eq__` for classes that mainly hold data. Use `field(default_factory=list)` for mutable defaults. `frozen=True` makes it immutable.

**Q: What is `lru_cache`?**  
A: A decorator from `functools` that caches function return values based on arguments. Implements the LRU (Least Recently Used) eviction policy. Requires hashable arguments. Massively speeds up recursive functions with overlapping subproblems.

**Q: What is an ABC and why use it?**  
A: Abstract Base Class — defines a contract that all subclasses must fulfill by implementing all `@abstractmethod` methods. Prevents instantiation of the base class and enforces the interface at class definition time, not at runtime.

**Q: What is the difference between `raise` and `raise X from Y`?**  
A: `raise` re-raises the current exception. `raise X from Y` chains exceptions — `Y` is stored as `__cause__` on `X`, making the traceback show the original cause. `raise X from None` suppresses the original exception.

**Q: What does `partial` do?**  
A: `functools.partial(func, *args, **kwargs)` creates a new function with some arguments pre-filled. `double = partial(multiply, factor=2)` — now `double(5)` calls `multiply(5, factor=2)`.

---

## 📝 Key Takeaways

1. **List comp** `[expr for x in it if cond]` — transform + filter in one line
2. **Dict comp** `{k: v for k, v in items}` — build or transform dicts cleanly
3. **Generator expr** `(expr for x in it)` — lazy, memory-efficient, use for large data
4. **`Counter`** — frequency counts, most common, anagram check, arithmetic on counts
5. **`defaultdict`** — auto-creates defaults, perfect for grouping (list) and graphs (list/set)
6. **`deque`** — O(1) append/pop from both ends, `maxlen` for sliding window, BFS queue
7. **`namedtuple`** — immutable, self-documenting tuple with named fields
8. **`try/except/else/finally`** — `else` runs on success, `finally` ALWAYS runs
9. **`@dataclass`** — eliminates boilerplate, use `field(default_factory=...)` for mutables
10. **`@lru_cache`** — memoize expensive/recursive functions, requires hashable args
11. **`partial`** — pre-fill arguments to create specialized functions
12. **Recursion** = base case + recursive case — always need a termination condition
13. **ABC** — enforces interface contract, prevents instantiation, use `@abstractmethod`
14. **`APIRouter`** — split FastAPI routes into multiple files, include with prefix and tags
15. **JWT auth** — `create_access_token` → `OAuth2PasswordBearer` → `Depends(get_current_user)`

---

*Day 8 Complete ✅ — All gaps filled. You are now fully interview-ready!*

---

## 📋 Master Checklist — Everything Covered Across All Days

```
Day 1  ✅  Data types, mutability, is vs ==, shallow/deep copy, truthy/falsy
Day 2  ✅  Functions, *args/**kwargs, mutable defaults, lambda, map/filter/reduce, scope
Day 3  ✅  OOP — classes, inheritance, polymorphism, encapsulation, magic methods
Day 4  ✅  Closures, decorators, iterators, generators, context managers
Day 5  ✅  GIL, threading, multiprocessing, asyncio, concurrent.futures
Day 6  ✅  FastAPI — basics, pydantic, middleware, exception handling, CRUD API
Day 8  ✅  Comprehensions, strings, collections, itertools, try/except, dataclasses,
           lru_cache, partial, recursion, ABC, JWT auth, APIRouter
```