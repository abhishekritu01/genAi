# 📘 Complete JavaScript Interview Notes
> **Target: 3–5 Years Experience | Full-Stack / Frontend Roles**
> Covers everything from fundamentals to advanced internals — no topic skipped.

---

## 📑 Table of Contents

1. [JavaScript Fundamentals](#1-javascript-fundamentals)
2. [Data Types & Type System](#2-data-types--type-system)
3. [Scope, Hoisting & Closures](#3-scope-hoisting--closures)
4. [Functions (All Forms)](#4-functions-all-forms)
5. [Objects & Prototypes](#5-objects--prototypes)
6. [Arrays & Iteration](#6-arrays--iteration)
7. [ES6+ Modern JavaScript](#7-es6-modern-javascript)
8. [Asynchronous JavaScript](#8-asynchronous-javascript)
9. [The Event Loop & Runtime](#9-the-event-loop--runtime)
10. [DOM & Browser APIs](#10-dom--browser-apis)
11. [Error Handling](#11-error-handling)
12. [Memory Management & Performance](#12-memory-management--performance)
13. [Design Patterns](#13-design-patterns)
14. [Functional Programming](#14-functional-programming)
15. [Classes & OOP](#15-classes--oop)
16. [Modules (CJS & ESM)](#16-modules-cjs--esm)
17. [Regular Expressions](#17-regular-expressions)
18. [Web APIs & Storage](#18-web-apis--storage)
19. [Security in JavaScript](#19-security-in-javascript)
20. [JavaScript Internals & V8 Engine](#20-javascript-internals--v8-engine)
21. [Node.js Specific Concepts](#21-nodejs-specific-concepts)
22. [Miscellaneous & Tricky Concepts](#22-miscellaneous--tricky-concepts)
23. [Top Interview Questions with Answers](#23-top-interview-questions-with-answers)

---

## 1. JavaScript Fundamentals

### What is JavaScript?

JavaScript is a **high-level, interpreted, single-threaded, dynamically typed, garbage-collected** programming language. It runs in browsers and on servers (via Node.js).

- **Paradigms supported:** Object-Oriented, Functional, Event-driven, Imperative
- **Execution model:** Single-threaded, non-blocking via event loop
- **Typing:** Dynamic (types resolved at runtime), weakly typed (implicit coercion)

### How JS Code Runs

```
Source Code → Parser → AST (Abstract Syntax Tree) → Bytecode → JIT Compiled
```

The **V8 engine** (Chrome/Node.js) compiles JS to native machine code using JIT (Just-In-Time) compilation.

---

## 2. Data Types & Type System

### Primitive Types (7 total — immutable, stored by value)

| Type | Example | `typeof` result |
|------|---------|----------------|
| `String` | `"hello"` | `"string"` |
| `Number` | `42`, `3.14`, `NaN`, `Infinity` | `"number"` |
| `Boolean` | `true`, `false` | `"boolean"` |
| `Undefined` | `let x;` | `"undefined"` |
| `Null` | `let x = null` | `"object"` ⚠️ (JS bug) |
| `BigInt` | `9007199254740991n` | `"bigint"` |
| `Symbol` | `Symbol("id")` | `"symbol"` |

### Non-Primitive Types (stored by reference)

| Type | Example | `typeof` result |
|------|---------|----------------|
| `Object` | `{}`, `[]`, `new Map()` | `"object"` |
| `Function` | `function(){}` | `"function"` |
| `Array` | `[1,2,3]` | `"object"` |

### typeof Gotchas

```js
typeof null         // "object"  ← historical bug, not fixed for backwards compat
typeof []           // "object"  ← use Array.isArray([]) → true
typeof NaN          // "number"  ← Not a Number is of type number
typeof function(){} // "function"
typeof undefined    // "undefined"
typeof undeclared   // "undefined" ← does NOT throw error
```

### null vs undefined

| | `null` | `undefined` |
|-|--------|-------------|
| Meaning | Intentionally empty | Not yet assigned |
| Set by | Developer | JavaScript engine |
| typeof | `"object"` | `"undefined"` |
| Equality | `null == undefined` → `true` | `null === undefined` → `false` |

```js
let a;           // undefined — declared, no value
let b = null;    // null — explicitly set to "nothing"

null == undefined   // true  (loose)
null === undefined  // false (strict)
```

### Type Coercion

JS automatically converts types in certain operations.

```js
// String + Number → String concatenation
"5" + 2       // "52"
"5" + 2 + 1   // "521"
2 + 1 + "5"   // "35" (left to right)

// Math operators → Number conversion
"5" - 2       // 3
"5" * "2"     // 10
true + 1      // 2
false + 1     // 1
null + 1      // 1
undefined + 1 // NaN

// Comparison coercion
0 == false    // true
"" == false   // true
null == 0     // false
null == false // false
NaN == NaN    // false ← NaN is never equal to itself
```

### == vs ===

| Operator | Description | Use |
|----------|-------------|-----|
| `==` | Loose equality — does type coercion | Avoid |
| `===` | Strict equality — no coercion | Always prefer |

```js
"5" == 5    // true  (coercion: "5" → 5)
"5" === 5   // false (different types)
null == undefined  // true
null === undefined // false
```

### Checking types reliably

```js
Array.isArray([])                    // true
x === null                           // null check
x !== null && typeof x === "object"  // real object
Number.isNaN(NaN)                    // true (better than isNaN())
Number.isFinite(Infinity)            // false
Object.prototype.toString.call([])   // "[object Array]"
```

### Falsy Values (8 total)

```js
false, 0, -0, 0n, "", '', ``, null, undefined, NaN
```

Everything else is **truthy**, including `[]`, `{}`, `"0"`, `" "`.

```js
Boolean([])   // true  ← empty array is truthy!
Boolean({})   // true  ← empty object is truthy!
Boolean("0")  // true  ← non-empty string is truthy
```

### Pass by Value vs Pass by Reference

**Primitives → Pass by Value** (a copy is made):

```js
let a = 10;
let b = a;
b = 20;
console.log(a); // 10 — unaffected
```

**Objects/Arrays → Pass by Reference** (reference/pointer is shared):

```js
let obj1 = { name: "Abhi" };
let obj2 = obj1;        // same reference
obj2.name = "Sunny";
console.log(obj1.name); // "Sunny" — affected!
```

> **Interview tip:** JS is technically "pass by value" — but for objects, the value IS the reference (memory address). So mutating properties affects the original.

**Copying to avoid shared references:**

```js
// Shallow copy
const copy1 = { ...original };
const copy2 = Object.assign({}, original);
const copy3 = [...arr];

// Deep copy
const deep = JSON.parse(JSON.stringify(obj)); // loses functions, dates
const deep2 = structuredClone(obj);           // ES2023, handles more types
```

---

## 3. Scope, Hoisting & Closures

### Scope Types

| Scope | Description | Keywords |
|-------|-------------|---------|
| **Global** | Accessible everywhere | `var` at top level |
| **Function** | Inside function body | `var`, `let`, `const` |
| **Block** | Inside `{}` (if, for, etc.) | `let`, `const` only |
| **Module** | Per-file scope in ESM | All declarations |
| **Lexical** | Defined by code position at author time | Closures |

```js
var globalVar = "I'm global";

function outer() {
  var funcVar = "function scope";

  if (true) {
    let blockVar = "block scope";  // only accessible here
    var hoisted = "function scope"; // var ignores block!
  }

  console.log(hoisted);    // "function scope" — var leaked out
  console.log(blockVar);   // ReferenceError
}
```

### var vs let vs const

| Feature | `var` | `let` | `const` |
|---------|-------|-------|---------|
| Scope | Function | Block | Block |
| Hoisted | ✅ (as `undefined`) | ✅ (TDZ) | ✅ (TDZ) |
| Reassignable | ✅ | ✅ | ❌ |
| Redeclarable | ✅ | ❌ | ❌ |
| Global property | ✅ (`window.x`) | ❌ | ❌ |

> **`const` doesn't mean immutable** — the binding can't be reassigned, but object properties CAN be changed.

```js
const user = { name: "Abhi" };
user.name = "Sunny";   // ✅ works — mutating property
user = {};             // ❌ TypeError — reassigning binding

const arr = [1, 2, 3];
arr.push(4);           // ✅ works
arr = [];              // ❌ TypeError
```

### Hoisting

Declarations are moved to the top of their scope during the **creation phase** of the Execution Context.

**`var` hoisting:**

```js
console.log(x); // undefined (not ReferenceError!)
var x = 5;
// JS sees it as:
// var x;          ← hoisted
// console.log(x); ← undefined
// x = 5;
```

**Function declaration hoisting (fully hoisted with body):**

```js
sayHello(); // "Hello!" — works before declaration
function sayHello() { console.log("Hello!"); }
```

**`let`/`const` — Temporal Dead Zone (TDZ):**

```js
console.log(y); // ReferenceError: Cannot access 'y' before initialization
let y = 10;
// y is hoisted but NOT initialized — it's in the "TDZ"
```

**Function expressions are NOT hoisted:**

```js
sayBye(); // TypeError: sayBye is not a function
var sayBye = function() { console.log("Bye!"); };
// var sayBye is hoisted as undefined, then called → error
```

### Scope Chain

When JS looks up a variable, it searches:
1. Current scope
2. Parent scope
3. Parent's parent
4. ... up to global scope
5. `ReferenceError` if not found

```js
let x = "global";

function outer() {
  let x = "outer";
  function inner() {
    // no x here → looks up chain → finds "outer"
    console.log(x); // "outer"
  }
  inner();
}
```

### Closures

A **closure** is a function that "remembers" the variables from its outer scope even after the outer function has finished executing.

```js
function makeCounter(start = 0) {
  let count = start;          // this variable is "closed over"
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount()  { return count; }
  };
}

const counter = makeCounter(5);
counter.increment(); // 6
counter.increment(); // 7
counter.getCount();  // 7
// 'count' is private — inaccessible from outside
```

**Classic closure trap in loops (var):**

```js
// Problem
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
// Prints: 3 3 3 — all closures share same 'i'

// Fix 1: use let
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
// Prints: 0 1 2 — each iteration has its own 'i'

// Fix 2: IIFE to capture value
for (var i = 0; i < 3; i++) {
  ((j) => setTimeout(() => console.log(j), 0))(i);
}
```

**Closure use cases:**
- Data encapsulation / private variables
- Memoization / caching
- Partial application & currying
- Event handlers / callbacks maintaining state
- Module pattern

---

## 4. Functions (All Forms)

### Function Declaration

```js
function add(a, b) {
  return a + b;
}
// Fully hoisted — can be called before definition
```

### Function Expression

```js
const add = function(a, b) {
  return a + b;
};
// Not hoisted — variable is hoisted as undefined
```

### Arrow Functions

```js
const add = (a, b) => a + b;         // implicit return
const square = x => x * x;           // single param, no parens needed
const noOp = () => {};                // no params
const getObj = () => ({ key: "val" });// return object — wrap in ()
```

**Arrow function differences from regular functions:**

| Feature | Regular Function | Arrow Function |
|---------|-----------------|----------------|
| `this` binding | Own `this` (dynamic) | Lexical (inherits from parent) |
| `arguments` object | ✅ Has it | ❌ No `arguments` |
| Used as constructor | ✅ `new Fn()` | ❌ Cannot use `new` |
| `prototype` property | ✅ Has it | ❌ No `prototype` |
| Method definition | ✅ Good | ❌ Avoid (`this` wrong) |

```js
const obj = {
  value: 42,
  regular: function() { return this.value; },  // this = obj → 42
  arrow: () => this.value                       // this = outer/window → undefined
};
```

### Default Parameters

```js
function greet(name = "Guest", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
greet();              // "Hello, Guest!"
greet("Abhi");        // "Hello, Abhi!"
greet(undefined, "Hi"); // "Hi, Guest!" — only undefined triggers default
greet(null, "Hi");    // "Hi, null"  — null does NOT trigger default
```

### Rest Parameters

```js
function sum(first, ...rest) {
  return rest.reduce((acc, n) => acc + n, first);
}
sum(1, 2, 3, 4); // 10

// rest must be the last parameter
function invalid(a, ...b, c) {} // SyntaxError
```

### Spread Operator

```js
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];  // [1,2,3,4,5]

const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 }; // { a:1, b:2, c:3 }

Math.max(...arr1); // 3
```

### The `arguments` Object

```js
function sum() {
  // arguments = array-like object (NOT a real array)
  return Array.from(arguments).reduce((a, b) => a + b, 0);
}
sum(1, 2, 3); // 6

// Arrow functions do NOT have their own arguments
const fn = () => console.log(arguments); // ReferenceError
```

### IIFE (Immediately Invoked Function Expression)

```js
// Classic IIFE
(function() {
  const privateVar = "hidden";
  console.log("Runs immediately");
})();

// Arrow IIFE
(() => {
  console.log("Arrow IIFE");
})();

// IIFE with return value
const result = (function(x) { return x * 2; })(5); // 10
```

**Use cases:** Creating private scope, avoiding global pollution, one-time initialization.

### `this` Keyword

`this` is determined by **how** a function is called (not where it's defined).

| Calling Pattern | `this` value |
|-----------------|-------------|
| Global scope (non-strict) | `window` |
| Global scope (strict) | `undefined` |
| Object method | The object |
| Constructor (`new`) | New instance |
| Arrow function | Lexical outer scope |
| `call/apply/bind` | Explicitly set |
| DOM event handler | The element |
| Class method | The instance |

```js
const obj = {
  name: "Abhi",
  greet() {
    console.log(this.name); // "Abhi"
    const inner = () => console.log(this.name); // "Abhi" — lexical this
    inner();
  }
};

// Losing 'this'
const fn = obj.greet;
fn(); // undefined (or window.name) — 'this' lost when method extracted
```

### call, apply, bind

All three allow you to **explicitly set `this`**.

```js
function introduce(lang1, lang2) {
  console.log(`${this.name} knows ${lang1} and ${lang2}`);
}
const user = { name: "Abhi" };

// call — invoke immediately, args separated by commas
introduce.call(user, "JS", "Python");

// apply — invoke immediately, args as an array
introduce.apply(user, ["JS", "Python"]);

// bind — returns a NEW function, doesn't invoke
const boundFn = introduce.bind(user, "JS");
boundFn("Python"); // called later
```

| Method | Invokes? | Args format |
|--------|----------|-------------|
| `call` | ✅ Immediately | Comma-separated |
| `apply` | ✅ Immediately | Array |
| `bind` | ❌ Returns bound fn | Comma-separated (partial) |

### Pure vs Impure Functions

```js
// Pure — same input, always same output, no side effects
function add(a, b) { return a + b; }

// Impure — depends on/modifies external state
let count = 0;
function increment() { return ++count; } // side effect: modifies external state

// Impure — same input, different output
function random() { return Math.random(); }
```

### Higher-Order Functions

Functions that accept functions as arguments or return functions.

```js
// Takes function
function apply(fn, value) { return fn(value); }
apply(x => x * 2, 5); // 10

// Returns function
function multiplier(factor) {
  return (n) => n * factor;
}
const double = multiplier(2);
double(5); // 10
```

---

## 5. Objects & Prototypes

### Object Creation Methods

```js
// 1. Object literal
const obj = { name: "Abhi", age: 27 };

// 2. Constructor function
function Person(name) { this.name = name; }
const p = new Person("Abhi");

// 3. Object.create() — explicit prototype linking
const proto = { greet() { return `Hi ${this.name}`; } };
const user = Object.create(proto);
user.name = "Abhi";
user.greet(); // "Hi Abhi"

// 4. ES6 Class
class User { constructor(name) { this.name = name; } }
const u = new User("Abhi");

// 5. Factory function
function createUser(name) { return { name, greet() { return `Hi ${this.name}`; } }; }
```

### Object Methods

```js
const obj = { a: 1, b: 2, c: 3 };

Object.keys(obj)    // ["a", "b", "c"]
Object.values(obj)  // [1, 2, 3]
Object.entries(obj) // [["a",1], ["b",2], ["c",3]]

// Convert entries back to object
Object.fromEntries([["a", 1], ["b", 2]]); // { a:1, b:2 }

// Merge objects
Object.assign({}, obj1, obj2); // shallow merge

// Freeze — no modifications allowed
Object.freeze(obj); // can't add/modify/delete

// Seal — can modify values, can't add/delete
Object.seal(obj);

// Check property
"a" in obj                // true (checks prototype chain too)
obj.hasOwnProperty("a")   // true (own properties only)
Object.hasOwn(obj, "a")   // true (ES2022 — better alternative)
```

### Property Descriptors

```js
const obj = {};
Object.defineProperty(obj, "name", {
  value: "Abhi",
  writable: false,    // cannot change value
  enumerable: true,   // shows in for...in loops
  configurable: false // cannot delete or redefine
});

// Read descriptor
Object.getOwnPropertyDescriptor(obj, "name");
```

### Getters & Setters

```js
const user = {
  _firstName: "Abhi",
  _lastName: "K",
  get fullName() {
    return `${this._firstName} ${this._lastName}`;
  },
  set fullName(name) {
    [this._firstName, this._lastName] = name.split(" ");
  }
};

user.fullName;          // "Abhi K"
user.fullName = "John Doe";
user._firstName;        // "John"
```

### Prototype Chain

Every object has a hidden `[[Prototype]]` link. When accessing a property:
1. Look on the object itself
2. Look on its prototype
3. Continue up chain until `Object.prototype`
4. Return `undefined` if not found

```js
const animal = { breathes: true };
const dog = Object.create(animal);
dog.barks = true;

dog.barks;    // true   — own property
dog.breathes; // true   — inherited from animal
dog.toString; // function — inherited from Object.prototype

Object.getPrototypeOf(dog) === animal; // true
```

### `prototype` vs `__proto__`

| | `prototype` | `__proto__` |
|-|-------------|-------------|
| Belongs to | Constructor functions | All objects |
| Purpose | Template for instances | Points to actual prototype |
| When used | `Fn.prototype.method = ...` | Checking inheritance |

```js
function Car(brand) { this.brand = brand; }
Car.prototype.drive = function() { return `${this.brand} drives`; };

const c = new Car("BMW");
c.__proto__ === Car.prototype;              // true
Car.prototype.__proto__ === Object.prototype; // true
Object.prototype.__proto__ === null;        // true (end of chain)
```

### What `new` Does Internally

```js
function User(name) { this.name = name; }
const user = new User("Abhi");

// Internally, new does:
// 1. Creates empty object: obj = {}
// 2. Links prototype: obj.__proto__ = User.prototype
// 3. Executes constructor: User.call(obj, "Abhi")
// 4. Returns obj (if constructor returns primitive/nothing)
```

### Shallow vs Deep Copy

```js
const obj = { a: 1, b: { c: 2 } };

// Shallow — nested reference is shared
const shallow = { ...obj };
shallow.b.c = 99;
obj.b.c; // 99 — affected!

// Deep copy options:
const deep1 = JSON.parse(JSON.stringify(obj));  // ❌ loses functions, Dates, undefined
const deep2 = structuredClone(obj);             // ✅ ES2022 — handles most types
```

---

## 6. Arrays & Iteration

### Array Methods Cheatsheet

**Mutating (modify original):**

```js
arr.push(x)        // add to end, returns new length
arr.pop()          // remove from end, returns element
arr.unshift(x)     // add to start, returns new length
arr.shift()        // remove from start, returns element
arr.splice(i,n,x)  // remove/insert at index
arr.sort(fn)       // sort in place
arr.reverse()      // reverse in place
arr.fill(v,s,e)    // fill values
```

**Non-mutating (return new array/value):**

```js
arr.map(fn)         // transform each → new array, same length
arr.filter(fn)      // keep matching → new array, same/shorter
arr.reduce(fn, init)// aggregate → single value
arr.find(fn)        // first match or undefined
arr.findIndex(fn)   // first match index or -1
arr.every(fn)       // all match? → boolean
arr.some(fn)        // any match? → boolean
arr.includes(v)     // contains value? → boolean
arr.indexOf(v)      // first index of value, or -1
arr.flat(depth)     // flatten nested arrays
arr.flatMap(fn)     // map + flatten one level
arr.slice(s,e)      // copy portion
arr.concat(arr2)    // join arrays
arr.join(sep)       // array → string
Array.from(x)       // convert iterable to array
Array.isArray(x)    // check if array
```

### map vs filter vs reduce

```js
const nums = [1, 2, 3, 4, 5];

// map — transform each element (same length output)
nums.map(x => x * 2);          // [2, 4, 6, 8, 10]

// filter — select elements (same/shorter output)
nums.filter(x => x % 2 === 0); // [2, 4]

// reduce — fold to single value
nums.reduce((acc, x) => acc + x, 0); // 15

// Chaining
nums
  .filter(x => x > 2)
  .map(x => x * 10)
  .reduce((a, b) => a + b, 0); // 120
```

### slice vs splice

```js
const arr = [1, 2, 3, 4, 5];

// slice — non-destructive, returns copy
arr.slice(1, 3);    // [2, 3] — original unchanged
arr.slice(-2);      // [4, 5] — negative from end

// splice — DESTRUCTIVE, modifies original
arr.splice(1, 2);       // removes 2 items at index 1, returns [2,3]
arr.splice(1, 0, 99);   // inserts 99 at index 1, removes 0
arr.splice(1, 1, 99);   // replaces item at index 1 with 99
```

### for...in vs for...of

```js
const arr = [10, 20, 30];
const obj = { a: 1, b: 2 };

// for...in — iterates over KEYS (indices for arrays, keys for objects)
for (let key in arr) { console.log(key); }  // "0", "1", "2" (strings!)
for (let key in obj) { console.log(key); }  // "a", "b"

// for...of — iterates over VALUES (works on iterables: array, string, Map, Set)
for (let val of arr) { console.log(val); }  // 10, 20, 30
// for (let val of obj) {} // ❌ TypeError — objects are not iterable
for (let [k, v] of Object.entries(obj)) {} // ✅ iterate object entries
```

### Destructuring

```js
// Array destructuring
const [a, b, c = 3] = [1, 2];
const [first, ...rest] = [1, 2, 3, 4]; // rest = [2,3,4]
const [, second] = [1, 2];              // skip first element

// Object destructuring
const { name, age = 25 } = { name: "Abhi" };
const { name: n } = { name: "Abhi" };   // rename to n
const { a: { b: deepVal } } = { a: { b: 99 } }; // nested

// Function parameter destructuring
function greet({ name, role = "user" }) {
  return `${name} is a ${role}`;
}
greet({ name: "Abhi", role: "admin" });
```

---

## 7. ES6+ Modern JavaScript

### Template Literals

```js
const name = "Abhi";
const age = 27;

// Multi-line
const msg = `Hello ${name},
you are ${age} years old.`;

// Expression evaluation
`${2 + 2}`         // "4"
`${age > 18 ? "adult" : "minor"}`

// Tagged templates
function highlight(strings, ...vals) {
  return strings.reduce((acc, str, i) =>
    acc + str + (vals[i] ? `<b>${vals[i]}</b>` : ""), "");
}
highlight`Hello ${name}, you are ${age}`;
```

### Optional Chaining (?.)

```js
const user = { profile: { address: { city: "Bangalore" } } };

// Without optional chaining (verbose)
user && user.profile && user.profile.address && user.profile.address.city;

// With optional chaining
user?.profile?.address?.city;         // "Bangalore" or undefined
user?.settings?.theme;                // undefined (no error)
user?.greet?.();                      // call method if exists
arr?.[0];                             // safe array access
```

### Nullish Coalescing (??)

```js

Nullish Coalescing Operator (??)

👉 Introduced in modern JavaScript (ES2020)
👉 Used to provide a default value only when the value is null or undefined
// ?? returns right side only if left is null or undefined
null ?? "default"      // "default"
undefined ?? "default" // "default"
0 ?? "default"         // 0    ← 0 is not null/undefined!
"" ?? "default"        // ""   ← empty string is not null/undefined!
false ?? "default"     // false

// vs || which returns right side for any falsy value
0 || "default"         // "default"  ← 0 is falsy
"" || "default"        // "default"  ← "" is falsy
```

### Logical Assignment Operators (ES2021)

```js
let a = null;
let b = 0;
let c = "hello";

a ??= "default";  // a = "default"  (assigns if null/undefined)
b ||= "fallback"; // b = "fallback" (assigns if falsy)
c &&= "world";    // c = "world"    (assigns if truthy)
```

### Symbols

```js
const id = Symbol("id");          // unique identifier
const id2 = Symbol("id");
id === id2; // false — every Symbol is unique

// As object keys (hidden from Object.keys)
const obj = { [id]: 123, name: "Abhi" };
Object.keys(obj);   // ["name"] — Symbol not included
obj[id];            // 123

// Global symbol registry
const s1 = Symbol.for("shared");
const s2 = Symbol.for("shared");
s1 === s2; // true — shared registry

// Well-known symbols
class MyArray {
  [Symbol.iterator]() { /* custom iteration */ }
}
```

### Map & Set

```js
// Map — key-value pairs, any type as key
const map = new Map();
map.set("name", "Abhi");
map.set(42, "number key");
map.set(obj, "object key");

map.get("name");    // "Abhi"
map.has("name");    // true
map.size;           // 3
map.delete("name");
map.clear();

for (let [key, val] of map) {}

// Set — unique values only
const set = new Set([1, 2, 2, 3, 3]); // Set {1, 2, 3}
set.add(4);
set.has(2);     // true
set.delete(2);
set.size;       // 3

// Array deduplication using Set
const unique = [...new Set([1,1,2,2,3])]; // [1,2,3]
```

### WeakMap & WeakSet

```js
// WeakMap — object keys only, weakly held (allows GC)
const wm = new WeakMap();
let obj = {};
wm.set(obj, "data");
obj = null; // 'data' can now be garbage collected

// WeakSet — object values only, weakly held
const ws = new WeakSet();
ws.add(obj);

// Key differences from Map/Set:
// - Keys/values must be objects
// - NOT iterable (no .size, no forEach)
// - Keys are weakly referenced → GC can collect them
// Use case: tracking DOM nodes, private data per object
```

### Generators

```js
function* counter(start = 0) {
  while (true) {
    yield start++;
  }
}

const gen = counter(1);
gen.next(); // { value: 1, done: false }
gen.next(); // { value: 2, done: false }
gen.next(); // { value: 3, done: false }

// Finite generator
function* range(start, end) {
  for (let i = start; i < end; i++) yield i;
}
[...range(1, 5)]; // [1, 2, 3, 4]

// Generator with return
function* withReturn() {
  yield 1;
  return "done";
  yield 2; // never reached
}
const g = withReturn();
g.next(); // { value: 1, done: false }
g.next(); // { value: "done", done: true }
g.next(); // { value: undefined, done: true }
```

### Iterators & Iteration Protocol

```js
// Custom iterable object
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        return current <= last
          ? { value: current++, done: false }
          : { value: undefined, done: true };
      }
    };
  }
};

for (let num of range) { console.log(num); } // 1 2 3 4 5
[...range]; // [1, 2, 3, 4, 5]
```

### Proxy & Reflect

```js
// Proxy — intercept object operations
const user = { name: "Abhi", age: 27 };
const proxy = new Proxy(user, {
  get(target, prop) {
    console.log(`Getting ${prop}`);
    return Reflect.get(target, prop);
  },
  set(target, prop, value) {
    if (prop === "age" && typeof value !== "number")
      throw new TypeError("Age must be a number");
    return Reflect.set(target, prop, value);
  },
  has(target, prop) {
    return prop in target;
  }
});

proxy.name;        // "Getting name" → "Abhi"
proxy.age = "old"; // TypeError!

// Reflect — standardized way to perform object operations
Reflect.get(obj, "name");
Reflect.set(obj, "name", "Sunny");
Reflect.deleteProperty(obj, "name");
Reflect.ownKeys(obj); // includes symbols
```

---

## 8. Asynchronous JavaScript

### Callbacks

A function passed to another function to be executed later.

```js
function fetchData(id, callback) {
  setTimeout(() => {
    if (id > 0) callback(null, { id, name: "Abhi" });
    else callback(new Error("Invalid ID"), null);
  }, 1000);
}

fetchData(1, (err, data) => {
  if (err) return console.error(err);
  console.log(data);
});
```

**Callback Hell (Pyramid of Doom):**

```js
getUser(id, (user) => {
  getPosts(user.id, (posts) => {
    getComments(posts[0].id, (comments) => {
      getAuthor(comments[0].authorId, (author) => {
        console.log(author); // deeply nested, hard to handle errors
      });
    });
  });
});
```

### Promises

An object representing a **future value** — either resolved or rejected.

```js
const promise = new Promise((resolve, reject) => {
  const success = true;
  if (success) resolve("Data!");
  else reject(new Error("Failed!"));
});

promise
  .then(data => console.log(data))
  .catch(err => console.error(err))
  .finally(() => console.log("Always runs"));
```

**Promise states:**

| State | Description |
|-------|-------------|
| `pending` | Initial — operation in progress |
| `fulfilled` | `resolve()` was called |
| `rejected` | `reject()` was called |
| `settled` | Either fulfilled or rejected (terminal state) |

**Promise chaining:**

```js
fetch("/api/user")
  .then(res => {
    if (!res.ok) throw new Error("HTTP Error: " + res.status);
    return res.json();
  })
  .then(user => fetch(`/api/posts?userId=${user.id}`))
  .then(res => res.json())
  .then(posts => console.log(posts))
  .catch(err => console.error("Error:", err)); // catches ALL errors above
```

### Promise Combinators

```js
const p1 = fetch("/api/a");
const p2 = fetch("/api/b");
const p3 = fetch("/api/c");

// Promise.all — all must succeed; rejects if any fails
Promise.all([p1, p2, p3])
  .then(([a, b, c]) => {})
  .catch(err => {}); // first rejection triggers catch

// Promise.allSettled — waits for all, never rejects
Promise.allSettled([p1, p2, p3])
  .then(results => {
    results.forEach(r => {
      if (r.status === "fulfilled") console.log(r.value);
      else console.error(r.reason);
    });
  });

// Promise.race — first settled (fulfilled OR rejected) wins
Promise.race([p1, p2, p3]).then(first => {});

// Promise.any — first FULFILLED wins; rejects only if ALL fail
Promise.any([p1, p2, p3])
  .then(first => {})
  .catch(aggregateError => {}); // AggregateError if all fail
```

### Async / Await

Syntactic sugar over Promises — makes async code look synchronous.

```js
async function fetchUserData(userId) {
  try {
    const res = await fetch(`/api/users/${userId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const user = await res.json();
    return user;
  } catch (err) {
    console.error("Failed:", err);
    throw err; // re-throw if needed
  } finally {
    console.log("Request complete");
  }
}
```

**Sequential vs Parallel:**

```js
// Sequential — each awaits before starting next (slower)
const user  = await fetchUser();
const posts = await fetchPosts();  // only starts after user fetches

// Parallel — both start simultaneously (faster)
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
```

**Async with loops:**

```js
// forEach doesn't work with async — it doesn't await
arr.forEach(async (item) => {
  await doSomething(item); // NOT awaited!
});

// Use for...of instead
for (const item of arr) {
  await doSomething(item); // properly sequential
}

// Or map + Promise.all for parallel
const results = await Promise.all(arr.map(item => doSomething(item)));
```

### Async Iterators

```js
async function* fetchPages(url) {
  let page = 1;
  while (true) {
    const res = await fetch(`${url}?page=${page}`);
    const data = await res.json();
    if (!data.length) return;
    yield data;
    page++;
  }
}

for await (const page of fetchPages("/api/data")) {
  console.log(page);
}
```

---

## 9. The Event Loop & Runtime

### Core Components

```
┌────────────────────────────────┐
│         Call Stack             │ ← Executes code (LIFO)
├────────────────────────────────┤
│         Heap                   │ ← Memory allocation
├───────────────┬────────────────┤
│   Web APIs    │   Node.js APIs │ ← Handle async ops
│  (browser)    │   (libuv)      │
├───────────────┴────────────────┤
│      Microtask Queue           │ ← Promises, queueMicrotask
│      Macrotask Queue           │ ← setTimeout, setInterval, I/O
├────────────────────────────────┤
│         Event Loop             │ ← Coordinates everything
└────────────────────────────────┘
```

### Execution Order

```
1. Synchronous code (call stack)
2. Microtasks (Promises .then, queueMicrotask, process.nextTick)
3. Macrotasks (setTimeout, setInterval, I/O callbacks)
4. Back to step 2 (empty microtask queue before next macrotask)
```

```js
console.log("1");                         // sync

setTimeout(() => console.log("2"), 0);   // macrotask

Promise.resolve()
  .then(() => console.log("3"))          // microtask
  .then(() => console.log("4"));         // microtask

queueMicrotask(() => console.log("5"));  // microtask

console.log("6");                         // sync

// Output: 1, 6, 3, 5, 4, 2
```

### Microtasks vs Macrotasks

| Type | Examples | Priority |
|------|---------|----------|
| **Microtask** | `Promise.then`, `queueMicrotask`, `MutationObserver`, `process.nextTick` | Higher — runs before any macrotask |
| **Macrotask** | `setTimeout`, `setInterval`, `setImmediate`, I/O, `requestAnimationFrame` | Lower |

> **Key rule:** After each macrotask, ALL pending microtasks run before the next macrotask starts.

### setTimeout Accuracy

```js
// setTimeout(fn, 0) doesn't mean 0ms delay
// It means "as soon as possible after current code and microtasks"
setTimeout(() => {}, 0); // minimum delay ~1-4ms in browsers

// HTML spec sets minimum timeout to 4ms for nested timeouts
```

### Node.js Event Loop Phases

```
   ┌──────────────────────────┐
┌─ │       timers             │ ← setTimeout, setInterval
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │    pending callbacks     │ ← I/O errors
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
│  │    idle, prepare         │ ← internal
│  └─────────────┬────────────┘
│  ┌─────────────┴────────────┐
└─ │         poll             │ ← fetch I/O events, run callbacks
   └─────────────┬────────────┘
   ┌─────────────┴────────────┐
   │         check            │ ← setImmediate
   └─────────────┬────────────┘
   ┌─────────────┴────────────┐
   │    close callbacks       │ ← socket.close etc.
   └──────────────────────────┘
```

### process.nextTick vs setImmediate

```js
setTimeout(() => console.log("timeout"), 0);
setImmediate(() => console.log("immediate"));
process.nextTick(() => console.log("nextTick"));
console.log("sync");

// Output: sync → nextTick → timeout → immediate
// (setImmediate order vs setTimeout is non-deterministic outside I/O)
```

| Function | When runs |
|----------|-----------|
| `process.nextTick` | Before microtasks, before event loop continues |
| `Promise.then` | After current operation, before next I/O |
| `setImmediate` | After I/O events, in check phase |
| `setTimeout(fn,0)` | In timers phase |

---

## 10. DOM & Browser APIs

### DOM Selection

```js
document.getElementById("id")
document.querySelector(".class")        // first match
document.querySelectorAll("div.item")   // all matches (NodeList)
document.getElementsByClassName("cls") // live HTMLCollection
document.getElementsByTagName("div")
```

### DOM Manipulation

```js
// Create & append
const div = document.createElement("div");
div.textContent = "Hello";
div.className = "container";
document.body.appendChild(div);

// Efficient batch insert
const frag = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const item = document.createElement("li");
  item.textContent = `Item ${i}`;
  frag.appendChild(item);
}
list.appendChild(frag); // single DOM operation

// Remove
element.remove();
parent.removeChild(child);

// Clone
const clone = element.cloneNode(true); // deep clone
```

### Events

```js
// Add listener
element.addEventListener("click", handler, { once: true, capture: false });

// Remove listener
element.removeEventListener("click", handler); // must be same function reference

// Event object
element.addEventListener("click", (e) => {
  e.target;           // element that triggered event
  e.currentTarget;    // element listener is attached to
  e.preventDefault(); // prevent default behavior (form submit, link nav)
  e.stopPropagation();// stop bubbling up the DOM
  e.stopImmediatePropagation(); // also stop other listeners on same element
});
```

### Event Bubbling & Capturing

```
Capture phase: Window → Document → body → parent → element
Bubble phase:  element → parent → body → Document → Window
```

```js
// capture: true = listener fires during capture phase
parent.addEventListener("click", handler, true);  // capture
child.addEventListener("click", handler, false);  // bubble (default)
```

### Event Delegation

Attach one listener to a parent to handle events on many children:

```js
// Instead of: items.forEach(item => item.addEventListener(...))
document.querySelector("#list").addEventListener("click", (e) => {
  const item = e.target.closest("li"); // handle even dynamically added items
  if (!item) return;
  console.log("Clicked:", item.dataset.id);
});
```

**Benefits:** Performance, works for dynamically added elements, less memory.

### Debounce & Throttle

```js
// Debounce — executes after delay of silence
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
// Use: search input, resize handler
const search = debounce((query) => fetchResults(query), 300);
input.addEventListener("input", e => search(e.target.value));

// Throttle — executes at most once per interval
function throttle(fn, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
// Use: scroll events, button clicks
window.addEventListener("scroll", throttle(updateScrollbar, 100));
```

---

## 11. Error Handling

### try / catch / finally

```js
try {
  const data = JSON.parse(invalidJSON);  // throws SyntaxError
  undeclaredFn();                        // throws ReferenceError
} catch (err) {
  console.error(err.name);    // "SyntaxError"
  console.error(err.message); // "Unexpected token..."
  console.error(err.stack);   // stack trace

  if (err instanceof SyntaxError) {
    // handle specifically
  }
} finally {
  // Always runs — cleanup code, even if no error
}
```

### Error Types

| Error | Cause |
|-------|-------|
| `SyntaxError` | Invalid JavaScript syntax |
| `ReferenceError` | Accessing undeclared variable |
| `TypeError` | Wrong type operation (null.property) |
| `RangeError` | Value out of range (array length -1) |
| `URIError` | Invalid URI encoding |
| `EvalError` | Deprecated eval usage |

### Custom Errors

```js
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
    // Fix prototype chain in transpiled code:
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}

class NetworkError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = "NetworkError";
    this.statusCode = statusCode;
  }
}

try {
  throw new ValidationError("Invalid email", "email");
} catch (err) {
  if (err instanceof ValidationError) {
    console.log(err.field); // "email"
  }
}
```

### Async Error Handling

```js
// Promises
fetchData()
  .then(process)
  .catch(err => console.error(err)); // handles all above

// Async/Await
async function run() {
  try {
    const data = await fetchData();
  } catch (err) {
    console.error(err);
  }
}

// Global unhandled rejection handler (Node.js)
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection:", reason);
});

// Browser
window.addEventListener("unhandledrejection", event => {
  console.error(event.reason);
});
```

---

## 12. Memory Management & Performance

### Garbage Collection

JavaScript uses **Mark-and-Sweep** algorithm:
1. Start from "roots" (global, stack variables)
2. Mark all reachable objects
3. Collect (free) all unmarked objects

```js
function createHeavyData() {
  let bigArray = new Array(1000000).fill("*");
  return bigArray; // returned reference keeps it alive
}

// When no references remain → eligible for GC
let data = createHeavyData();
data = null; // removes reference → GC can collect
```

### Memory Leak Patterns

```js
// 1. Forgotten timers
const interval = setInterval(() => { /* uses closured data */ }, 1000);
// Fix: clearInterval(interval) when no longer needed

// 2. Detached DOM nodes
let button = document.getElementById("btn");
button.addEventListener("click", heavyHandler);
button = null; // reference gone but listener still holds button in memory
// Fix: removeEventListener before removing from DOM

// 3. Closures holding large objects
function process() {
  const bigData = new Array(1000000).fill("*");
  return function() {
    return bigData[0]; // bigData held for lifetime of returned fn
  };
}

// 4. Global variable accumulation
function leaky() {
  leakyVar = "I'm now global!"; // missing var/let/const
}

// 5. Event listeners not removed
element.addEventListener("click", handler);
element.remove(); // element removed from DOM but listener persists
// Fix: element.removeEventListener("click", handler);
```

### WeakMap/WeakSet for Memory-Safe Patterns

```js
// DOM node metadata without preventing GC
const metadata = new WeakMap();
function setMeta(node, data) { metadata.set(node, data); }
// When node is GC'd, its entry in WeakMap is auto-removed

// Private data per instance
const _private = new WeakMap();
class Person {
  constructor(name, secret) {
    _private.set(this, { secret });
    this.name = name;
  }
  getSecret() { return _private.get(this).secret; }
}
```

### Performance Optimization Techniques

```js
// Memoization — cache expensive function results
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const expensiveFib = memoize(function fib(n) {
  return n <= 1 ? n : expensiveFib(n-1) + expensiveFib(n-2);
});

// Lazy initialization
class Config {
  get heavyData() {
    if (!this._heavyData) {
      this._heavyData = computeHeavyData(); // computed once on first access
    }
    return this._heavyData;
  }
}

// Web Workers for CPU-intensive tasks
const worker = new Worker("worker.js");
worker.postMessage({ data: largeArray });
worker.onmessage = (e) => console.log("Result:", e.data);
```

### DOM Performance

```js
// Batch reads before writes to avoid forced layout/reflow
// Bad: alternating read/write triggers reflow each time
element.style.height = element.offsetHeight + 10 + "px";
element.style.width = element.offsetWidth + 10 + "px";

// Good: batch reads, then batch writes
const h = element.offsetHeight;
const w = element.offsetWidth;
element.style.height = h + 10 + "px";
element.style.width = w + 10 + "px";

// Use requestAnimationFrame for visual updates
function animate() {
  element.style.left = (++x) + "px";
  if (x < 100) requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

---

## 13. Design Patterns

### Module Pattern

```js
const BankAccount = (function() {
  let _balance = 0;          // private
  let _transactions = [];    // private

  return {
    deposit(amount) {
      _balance += amount;
      _transactions.push({ type: "deposit", amount });
    },
    withdraw(amount) {
      if (amount > _balance) throw new Error("Insufficient funds");
      _balance -= amount;
    },
    getBalance() { return _balance; },
    getHistory() { return [..._transactions]; }
  };
})();

BankAccount.deposit(100);
BankAccount.getBalance(); // 100
// _balance is not accessible from outside
```

### Singleton Pattern

```js
class Database {
  static #instance = null;

  constructor(url) {
    if (Database.#instance) return Database.#instance;
    this.url = url;
    this.connection = null;
    Database.#instance = this;
  }

  static getInstance(url) {
    if (!Database.#instance) new Database(url);
    return Database.#instance;
  }

  connect() { /* ... */ }
}

const db1 = Database.getInstance("mongodb://...");
const db2 = Database.getInstance("mongodb://...");
db1 === db2; // true — same instance
```

### Observer / PubSub Pattern

```js
class EventEmitter {
  #events = {};

  on(event, listener) {
    if (!this.#events[event]) this.#events[event] = [];
    this.#events[event].push(listener);
    return this; // chainable
  }

  off(event, listener) {
    this.#events[event] = (this.#events[event] || [])
      .filter(l => l !== listener);
    return this;
  }

  emit(event, ...args) {
    (this.#events[event] || []).forEach(l => l(...args));
    return this;
  }

  once(event, listener) {
    const wrapper = (...args) => {
      listener(...args);
      this.off(event, wrapper);
    };
    return this.on(event, wrapper);
  }
}

const emitter = new EventEmitter();
emitter.on("data", d => console.log(d));
emitter.emit("data", { id: 1 }); // { id: 1 }
```

### Factory Pattern

```js
class Shape {
  area() { throw new Error("Not implemented"); }
}

class Circle extends Shape {
  constructor(r) { super(); this.r = r; }
  area() { return Math.PI * this.r ** 2; }
}

class Rectangle extends Shape {
  constructor(w, h) { super(); this.w = w; this.h = h; }
  area() { return this.w * this.h; }
}

// Factory
function createShape(type, ...args) {
  const shapes = { circle: Circle, rectangle: Rectangle };
  if (!shapes[type]) throw new Error(`Unknown shape: ${type}`);
  return new shapes[type](...args);
}

createShape("circle", 5).area();       // 78.54
createShape("rectangle", 4, 6).area(); // 24
```

### Strategy Pattern

```js
const sorters = {
  bubble: (arr) => { /* bubble sort implementation */ },
  quick:  (arr) => { /* quicksort implementation */ },
  merge:  (arr) => { /* merge sort implementation */ }
};

class Sorter {
  constructor(strategy = "quick") {
    this.strategy = sorters[strategy];
  }
  setStrategy(strategy) {
    this.strategy = sorters[strategy];
  }
  sort(arr) {
    return this.strategy([...arr]);
  }
}
```

### Proxy Pattern (Validation, Logging)

```js
function createValidatedUser(userData) {
  return new Proxy(userData, {
    set(target, prop, value) {
      if (prop === "age" && (typeof value !== "number" || value < 0))
        throw new TypeError("Age must be a positive number");
      if (prop === "email" && !value.includes("@"))
        throw new TypeError("Invalid email");
      target[prop] = value;
      return true;
    }
  });
}
```

---

## 14. Functional Programming

### Core Principles

1. **Pure Functions** — same input → same output, no side effects
2. **Immutability** — never modify data, always return new data
3. **Function Composition** — combine small functions to build complex ones
4. **Higher-Order Functions** — functions that take/return functions
5. **Declarative** — describe WHAT not HOW

### Currying

Transform a multi-argument function into a chain of single-argument functions.

```js
// Manual currying
const add = a => b => a + b;
add(2)(3); // 5

const multiply = a => b => c => a * b * c;
multiply(2)(3)(4); // 24

// Generic curry utility
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) return fn(...args);
    return (...more) => curried(...args, ...more);
  };
}

const curriedAdd = curry((a, b, c) => a + b + c);
curriedAdd(1)(2)(3); // 6
curriedAdd(1, 2)(3); // 6
curriedAdd(1)(2, 3); // 6
```

### Partial Application

```js
function partial(fn, ...preArgs) {
  return function(...laterArgs) {
    return fn(...preArgs, ...laterArgs);
  };
}

const multiply = (a, b, c) => a * b * c;
const double = partial(multiply, 2);
const triple = partial(multiply, 3);
double(4, 5);  // 40  (2 * 4 * 5)
triple(4, 5);  // 60  (3 * 4 * 5)
```

### Function Composition

```js
// compose — right to left
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

// pipe — left to right (more readable)
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

const double = x => x * 2;
const addOne = x => x + 1;
const square = x => x * x;

const transform = pipe(double, addOne, square);
transform(3); // square(addOne(double(3))) = square(7) = 49
```

### Memoization

```js
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize(n => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

fibonacci(40); // fast with memoization
```

---

## 15. Classes & OOP

### ES6 Class Syntax

```js
class Animal {
  #name;          // private field (ES2022)
  #sound;

  constructor(name, sound) {
    this.#name = name;
    this.#sound = sound;
    this.species = "Unknown"; // public
  }

  speak() {
    return `${this.#name} says ${this.#sound}`;
  }

  get name() { return this.#name; }
  set name(v) {
    if (typeof v !== "string") throw new TypeError("Name must be string");
    this.#name = v;
  }

  static create(name, sound) {
    return new Animal(name, sound);
  }

  toString() { return `Animal(${this.#name})`; }
}

const cat = new Animal("Tom", "meow");
cat.speak(); // "Tom says meow"
Animal.create("Jerry", "squeak").speak();
```

### Inheritance

```js
class Dog extends Animal {
  #tricks = [];

  constructor(name) {
    super(name, "woof"); // must call super() first
  }

  learn(trick) {
    this.#tricks.push(trick);
    return this;
  }

  perform() {
    return this.#tricks.map(t => `${this.name} performs ${t}`);
  }

  speak() {
    return super.speak() + "!"; // call parent method
  }
}

const rex = new Dog("Rex");
rex.learn("sit").learn("fetch");
rex.perform(); // ["Rex performs sit", "Rex performs fetch"]
rex instanceof Dog;    // true
rex instanceof Animal; // true
```

### Class Features Summary

```js
class MyClass {
  // Public instance field
  publicField = "public";

  // Private instance field
  #privateField = "private";

  // Static public field
  static staticField = "static";

  // Static private field
  static #staticPrivate = "private static";

  constructor(value) {
    this.value = value;
  }

  // Instance method
  instanceMethod() { return this.value; }

  // Static method
  static staticMethod() { return MyClass.staticField; }

  // Getters/Setters
  get doubled() { return this.value * 2; }
  set doubled(v) { this.value = v / 2; }

  // Private method
  #privateMethod() { return this.#privateField; }

  // Static initializer block (ES2022)
  static {
    this.staticField = "initialized";
  }
}
```

### Mixins (Multiple Inheritance workaround)

```js
const Serializable = (Base) => class extends Base {
  serialize() { return JSON.stringify(this); }
  static deserialize(json) { return Object.assign(new this(), JSON.parse(json)); }
};

const Timestamped = (Base) => class extends Base {
  constructor(...args) {
    super(...args);
    this.createdAt = new Date();
  }
};

class User extends Timestamped(Serializable(class {})) {
  constructor(name) { super(); this.name = name; }
}

const u = new User("Abhi");
u.createdAt;   // Date object
u.serialize(); // JSON string
```

---

## 16. Modules (CJS & ESM)

### CommonJS (Node.js default)

```js
// Export
module.exports = { add, subtract }; // named
module.exports = function() {};      // default
exports.add = function() {};         // shorthand

// Import
const { add } = require("./math");
const math = require("./math");
const _ = require("lodash");         // node_modules
```

### ES Modules (ESM)

```js
// Named exports
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export class User {}

// Default export (one per module)
export default function main() {}

// Combined
export { add, PI };
export default class App {}

// Import
import { add, PI } from "./math.js";
import App from "./app.js";
import * as math from "./math.js"; // namespace import
import { add as sum } from "./math.js"; // rename

// Dynamic import (code splitting)
const module = await import("./heavy.js");
if (condition) {
  const { fn } = await import("./optional.js");
}
```

### CJS vs ESM

| Feature | CommonJS | ESM |
|---------|----------|-----|
| Syntax | `require`/`exports` | `import`/`export` |
| Loading | Synchronous | Asynchronous |
| Binding | Value copy | Live binding |
| Tree-shaking | ❌ Hard | ✅ Easy |
| Top-level await | ❌ No | ✅ Yes |
| File extension | `.js` | `.mjs` or `"type":"module"` |

---

## 17. Regular Expressions

```js
// Literal syntax
const re = /pattern/flags;

// Constructor (for dynamic patterns)
const re = new RegExp("pattern", "flags");

// Flags
// g — global (find all matches)
// i — case insensitive
// m — multiline (^ and $ match line boundaries)
// s — dotAll (. matches \n)
// u — unicode
// y — sticky (match at lastIndex only)

// Test
/^\d+$/.test("123");  // true
/^\d+$/.test("abc");  // false

// Match
"hello world".match(/\w+/g);    // ["hello", "world"]
"hello world".matchAll(/\w+/g); // iterator of all matches with groups

// Replace
"hello".replace(/l/g, "r");         // "herro"
"2024-01-15".replace(/(\d{4})-(\d{2})-(\d{2})/, "$3/$2/$1"); // "15/01/2024"

// Split
"a,b,,c".split(/,+/); // ["a", "b", "c"]

// Named capture groups
const { year, month, day } = "2024-01-15".match(
  /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/
).groups;
```

---

## 18. Web APIs & Storage

### LocalStorage vs SessionStorage vs Cookies

| Feature | localStorage | sessionStorage | Cookies |
|---------|-------------|----------------|---------|
| Expiry | Never (manual) | Tab close | Set expiry |
| Capacity | ~5MB | ~5MB | ~4KB |
| Accessible | Same origin | Same tab | Server + client |
| Sent to server | ❌ | ❌ | ✅ |

```js
// localStorage
localStorage.setItem("user", JSON.stringify({ name: "Abhi" }));
const user = JSON.parse(localStorage.getItem("user"));
localStorage.removeItem("user");
localStorage.clear();

// sessionStorage — same API, tab-scoped
sessionStorage.setItem("token", "abc123");
```

### Fetch API

```js
// GET
const data = await fetch("/api/users")
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  });

// POST
const res = await fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Abhi" })
});

// With timeout using AbortController
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const res = await fetch("/api/data", { signal: controller.signal });
  clearTimeout(timeout);
} catch (err) {
  if (err.name === "AbortError") console.log("Request timed out");
}
```

### IndexedDB (large structured storage)

```js
const request = indexedDB.open("MyDB", 1);
request.onupgradeneeded = e => {
  const db = e.target.result;
  db.createObjectStore("users", { keyPath: "id" });
};
```

### Service Workers (offline support, caching)

```js
// Register
navigator.serviceWorker.register("/sw.js");

// In sw.js
self.addEventListener("install", e => {
  e.waitUntil(
    caches.open("v1").then(cache => cache.addAll(["/", "/app.js"]))
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
```

---

## 19. Security in JavaScript

### XSS (Cross-Site Scripting)

```js
// Vulnerable
element.innerHTML = userInput; // ❌ can inject <script>

// Safe alternatives
element.textContent = userInput;          // ✅ treats as text
element.innerHTML = DOMPurify.sanitize(userInput); // ✅ sanitize library
```

### CSRF (Cross-Site Request Forgery)

- Include CSRF tokens in state-changing requests
- Use `SameSite` cookie attribute
- Verify `Origin`/`Referer` headers server-side

### Content Security Policy (CSP)

```html
<!-- Restrict script sources -->
<meta http-equiv="Content-Security-Policy" content="script-src 'self' https://trusted.com">
```

### Prototype Pollution

```js
// Dangerous — attacker controls key
const key = "__proto__";
obj[key]["isAdmin"] = true; // pollutes Object.prototype!

// Safe check
if (key === "__proto__" || key === "constructor") return;
// Or use: Object.create(null) for data storage
```

### eval() and new Function() Risks

```js
eval(userInput);           // ❌ arbitrary code execution
new Function(userInput)(); // ❌ same risk

// Alternatives: JSON.parse for data, template literals for templates
```

---

## 20. JavaScript Internals & V8 Engine

### How V8 Works

```
JS Source → Parser → AST → Ignition (bytecode) → TurboFan (machine code)
```

1. **Parsing** — Source code → tokens → AST (Abstract Syntax Tree)
2. **Ignition** — AST → bytecode (interpreted)
3. **TurboFan** — Hot bytecode → optimized machine code (JIT)
4. **Deoptimization** — If assumptions break (type change) → back to bytecode

### Hidden Classes & Inline Caching

V8 creates **hidden classes** (shapes) to track object structure for optimization.

```js
// Good — consistent shape
function Point(x, y) {
  this.x = x; // always in same order
  this.y = y;
}
const p1 = new Point(1, 2);
const p2 = new Point(3, 4); // same hidden class → fast!

// Bad — inconsistent shape
const a = { x: 1 };
const b = { x: 1 };
a.y = 2;    // different hidden class → slower
delete b.x; // deletes → shape change → deoptimize
```

### Stack & Heap Memory

```
Stack: primitive values, function call frames, references (pointers)
Heap:  objects, arrays, closures, functions (actual data)
```

### JIT Compilation Optimization Tips

```js
// Consistent types (monomorphic > polymorphic)
function add(a, b) { return a + b; }
add(1, 2);         // always numbers → V8 optimizes
add("a", "b");     // now string too → less optimal

// Avoid arguments object (use rest params instead)
// Avoid dynamic property additions after object creation
// Keep functions small and predictable
```

---

## 21. Node.js Specific Concepts

### CommonJS Module System

```js
const fs = require("fs");
const path = require("path");
const { EventEmitter } = require("events");

module.exports = { myFunction };
// __dirname  → current file's directory
// __filename → current file's full path
```

### Built-in Modules

```js
// fs — file system
const fs = require("fs");
fs.readFile("file.txt", "utf8", (err, data) => {});
const data = fs.readFileSync("file.txt", "utf8"); // sync
fs.promises.readFile("file.txt", "utf8");         // promise

// path
path.join(__dirname, "files", "data.txt");
path.resolve("./relative");
path.extname("file.txt");    // ".txt"
path.basename("dir/file.txt"); // "file.txt"

// http
const http = require("http");
const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Hello World");
});
server.listen(3000);
```

### Streams

```js
const { Readable, Writable, Transform } = require("stream");

// Pipe streams
const readStream = fs.createReadStream("large-file.txt");
const writeStream = fs.createWriteStream("output.txt");
readStream.pipe(writeStream);

// Transform stream
const { Transform } = require("stream");
const upper = new Transform({
  transform(chunk, encoding, callback) {
    callback(null, chunk.toString().toUpperCase());
  }
});

readStream.pipe(upper).pipe(writeStream);
```

### EventEmitter

```js
const EventEmitter = require("events");
class Logger extends EventEmitter {
  log(msg) {
    this.emit("log", { message: msg, timestamp: new Date() });
  }
}

const logger = new Logger();
logger.on("log", ({ message, timestamp }) => {
  console.log(`[${timestamp}] ${message}`);
});
logger.log("Server started");
```

### process Object

```js
process.env.NODE_ENV       // environment variable
process.argv               // command line arguments
process.cwd()              // current working directory
process.exit(0)            // exit with code
process.memoryUsage()      // memory stats
process.nextTick(fn)       // schedule microtask
process.on("uncaughtException", handler)
process.on("unhandledRejection", handler)
```

---

## 22. Miscellaneous & Tricky Concepts

### Strict Mode

```js
"use strict"; // file level
// or inside function
function fn() { "use strict"; }

// Changes in strict mode:
// - undeclared variables → ReferenceError (not silently global)
// - this in functions → undefined (not window)
// - duplicate parameter names → SyntaxError
// - with statement → SyntaxError
// - delete variable/function → SyntaxError
// - octal literals → SyntaxError

"use strict";
x = 5; // ReferenceError: x is not defined
```

### Optional Catch Binding (ES2019)

```js
// Before
try {} catch (err) { /* must accept err even if unused */ }

// Now — can omit if not needed
try {
  JSON.parse(text);
} catch {
  console.log("Invalid JSON");
}
```

### Numeric Separators (ES2021)

```js
const million = 1_000_000;
const hex = 0xFF_EC_D8;
const binary = 0b1010_0001;
```

### BigInt

```js
const max = Number.MAX_SAFE_INTEGER; // 9007199254740991
const big = 9007199254740991n + 1n;  // 9007199254740992n — accurate!

// Cannot mix BigInt and Number
1n + 1; // TypeError
1n + BigInt(1); // 2n

typeof 1n; // "bigint"
```

### Object.create(null) — Dictionary Objects

```js
// Regular object has prototype chain (toString, hasOwnProperty, etc.)
const obj = {};
"toString" in obj; // true — from prototype!

// Truly empty object — no prototype
const dict = Object.create(null);
"toString" in dict; // false
// Safe for user-controlled keys (no prototype pollution risk)
```

### Array-like Objects

```js
// Has length and indexed access, but not Array methods
const arrayLike = { 0: "a", 1: "b", length: 2 };

// Convert to real array
Array.from(arrayLike);     // ["a", "b"]
[...arrayLike];            // ❌ TypeError (not iterable)
Array.prototype.slice.call(arrayLike); // ["a", "b"]

// Common array-likes: arguments, NodeList, HTMLCollection, strings
```

### Short-Circuit Evaluation

```js
// && returns first falsy or last value
false && console.log("never"); // false
true && "result";               // "result"
null && fn();                   // null (fn not called)

// || returns first truthy or last value
null || "default";              // "default"
"value" || "default";           // "value"

// Practical use
const value = input || "default";
user && user.isAdmin && showAdminPanel();
```

### Computed Property Names

```js
const key = "name";
const obj = { [key]: "Abhi" }; // { name: "Abhi" }

const prefix = "get";
const obj2 = {
  [`${prefix}Name`]() { return this.name; },
  [`${prefix}Age`]() { return this.age; }
};
```

### JSON Methods

```js
// Stringify with replacer & spacing
JSON.stringify({ name: "Abhi", fn: function(){} });
// {"name":"Abhi"} — functions omitted

JSON.stringify(obj, ["name", "age"]); // only include these keys
JSON.stringify(obj, null, 2);         // pretty print with 2-space indent

// Custom serialization
class User {
  toJSON() { return { id: this.id, name: this.name }; }
}

// Parse with reviver
JSON.parse(jsonStr, (key, value) => {
  if (key === "date") return new Date(value);
  return value;
});
```

### Number Precision

```js
0.1 + 0.2 === 0.3; // false ← floating point!
0.1 + 0.2;          // 0.30000000000000004

// Fix:
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON; // true
(0.1 + 0.2).toFixed(2); // "0.30" (string)
Math.round((0.1 + 0.2) * 10) / 10; // 0.3

Number.MAX_SAFE_INTEGER; // 9007199254740991
Number.MIN_SAFE_INTEGER; // -9007199254740991
Number.isInteger(5.0);   // true
Number.isFinite(Infinity); // false
Number.isNaN(NaN);         // true (better than global isNaN)
```

### Iterables & Spread

```js
// Anything with [Symbol.iterator] is iterable
// String, Array, Map, Set, arguments, NodeList, generators...

[..."hello"]; // ["h","e","l","l","o"]
new Set([..."hello"]); // Set {"h","e","l","o"}

// Custom iterable
const range = (from, to) => ({
  [Symbol.iterator]() {
    let i = from;
    return { next: () => i <= to ? { value: i++, done: false } : { done: true } };
  }
});

[...range(1, 5)]; // [1,2,3,4,5]
```

### toString and valueOf

```js
class Money {
  constructor(amount, currency) {
    this.amount = amount;
    this.currency = currency;
  }
  toString() { return `${this.amount} ${this.currency}`; }
  valueOf() { return this.amount; }
}

const m = new Money(100, "USD");
`${m}`;    // "100 USD" — uses toString
m + 50;    // 150       — uses valueOf
m > 50;    // true      — uses valueOf
```

### Prototype Pollution Prevention

```js
function safeSet(obj, key, value) {
  if (key === "__proto__" || key === "constructor" || key === "prototype") {
    throw new Error("Prototype pollution attempt");
  }
  obj[key] = value;
}

// Or use Map instead of plain object for user data
const data = new Map();
data.set("__proto__", "safe"); // completely fine in Map
```

---

## 23. Top Interview Questions with Answers

### Q1: What is the output?

```js
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
console.log(4);
```

**Answer:** `1, 4, 3, 2`
Sync → microtasks (Promise) → macrotasks (setTimeout)

---

### Q2: What is the output?

```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
```

**Answer:** `3, 3, 3`
`var` is function-scoped, shared across iterations. Fix: use `let` or IIFE.

---

### Q3: Implement `Promise.all` from scratch

```js
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;

    if (promises.length === 0) return resolve([]);

    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(value => {
          results[index] = value;
          if (++completed === promises.length) resolve(results);
        })
        .catch(reject);
    });
  });
}
```

---

### Q4: Implement debounce

```js
function debounce(fn, delay) {
  let timerId;
  return function(...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
```

---

### Q5: Flatten a nested array

```js
// Built-in
[1, [2, [3, [4]]]].flat(Infinity); // [1,2,3,4]

// Recursive
function flatten(arr) {
  return arr.reduce((acc, item) =>
    Array.isArray(item) ? acc.concat(flatten(item)) : [...acc, item], []);
}

// Stack-based (iterative)
function flatten(arr) {
  const stack = [...arr];
  const result = [];
  while (stack.length) {
    const item = stack.pop();
    if (Array.isArray(item)) stack.push(...item);
    else result.unshift(item);
  }
  return result;
}
```

---

### Q6: Implement memoization

```js
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
```

---

### Q7: What is closure? Give a real-world example

```js
// Closure = function + its lexical environment
function createMultiplier(multiplier) {
  return (n) => n * multiplier; // 'multiplier' is closed over
}
const double = createMultiplier(2);
const triple = createMultiplier(3);
double(5); // 10
triple(5); // 15
```

---

### Q8: Implement `bind` from scratch

```js
Function.prototype.myBind = function(context, ...preArgs) {
  const fn = this;
  return function(...laterArgs) {
    return fn.apply(context, [...preArgs, ...laterArgs]);
  };
};
```

---

### Q9: Deep clone without JSON

```js
function deepClone(obj) {
  if (obj === null || typeof obj !== "object") return obj;
  if (obj instanceof Date) return new Date(obj.getTime());
  if (obj instanceof Array) return obj.map(item => deepClone(item));
  if (obj instanceof Map) return new Map([...obj].map(([k,v]) => [deepClone(k), deepClone(v)]));
  if (obj instanceof Set) return new Set([...obj].map(v => deepClone(v)));

  const cloned = Object.create(Object.getPrototypeOf(obj));
  for (const key of Reflect.ownKeys(obj)) {
    cloned[key] = deepClone(obj[key]);
  }
  return cloned;
}
```

---

### Q10: What is the difference between `==` and `===`?

`==` performs **type coercion** before comparing. `===` checks both value AND type without coercion. Always prefer `===`.

```js
0 == false  // true  (false coerced to 0)
0 === false // false (different types)
null == undefined  // true  (special case)
null === undefined // false
NaN == NaN  // false (NaN is never equal to anything)
```

---

### Q11: Explain the prototype chain

```js
function Animal(name) { this.name = name; }
Animal.prototype.breathe = function() { return "breathing"; };

const dog = new Animal("Rex");
dog.breathe();      // found on Animal.prototype
dog.toString();     // found on Object.prototype
dog.nonExistent;    // undefined (end of chain: null)
```

---

### Q12: Difference between `null` and `undefined`

- `undefined` = variable declared but not assigned (set by JS)
- `null` = intentionally empty value (set by developer)
- `typeof null === "object"` (historical bug)
- `null == undefined` is `true`, `null === undefined` is `false`

---

### Q13: What is event delegation and why use it?

```js
// Instead of attaching listeners to each item:
document.querySelector("#list").addEventListener("click", e => {
  if (e.target.matches("li.item")) {
    console.log(e.target.textContent);
  }
});
// Benefits: fewer listeners, works for dynamic elements, less memory
```

---

### Q14: Implement curry function

```js
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...moreArgs) {
      return curried.apply(this, args.concat(moreArgs));
    };
  };
}
```

---

### Q15: What are WeakMap and WeakSet? When to use them?

- WeakMap/WeakSet hold **weak references** — keys/values can be GC'd when no other references exist
- Keys must be **objects** (not primitives)
- NOT iterable, no `.size`

**Use cases:**
- Storing metadata about DOM nodes (auto-cleaned when node is removed)
- Private class data
- Caching without preventing GC

---

## Quick Reference: Interview Cheatsheet

### Most Important Concepts to Master

| Topic | Key Points |
|-------|------------|
| Closures | Lexical scope, data privacy, memoization |
| Prototype chain | `__proto__`, `prototype`, inheritance |
| Event loop | Call stack, microtask queue, macrotask queue |
| `this` keyword | 6 different binding rules |
| Async patterns | Callbacks → Promises → async/await |
| Currying | Partial application, function composition |
| Immutability | Spread, Object.assign, structuredClone |
| Hoisting | var (undefined), let/const (TDZ), functions (full) |
| Type coercion | == vs ===, falsy values, Number() rules |
| Memory leaks | Timers, event listeners, closures, globals |

### Quick Output Predictions

```js
// Hoisting
console.log(typeof foo); // "function" (function declaration hoisted)
console.log(typeof bar); // "undefined" (var hoisted as undefined)
function foo() {}
var bar = function() {};

// Closure + var
var fns = [];
for (var i = 0; i < 3; i++) fns.push(() => i);
fns.map(f => f()); // [3, 3, 3]

// Promise + async
async function main() {
  console.log("A");
  await null;
  console.log("B");
}
main();
console.log("C");
// Output: A, C, B

// typeof chain
console.log(typeof typeof 1); // "string" (typeof 1 = "number", typeof "number" = "string")

// Short circuit
console.log(null || undefined || 0 || "" || "found!"); // "found!"
console.log(1 && 2 && 3);  // 3
console.log(1 && 0 && 3);  // 0
```

---

*This document covers the complete JavaScript landscape for interviews at the 3–5 year experience level. Review sections on Event Loop, Closures, Prototypes, and Async Patterns most carefully — they appear in nearly every interview.*