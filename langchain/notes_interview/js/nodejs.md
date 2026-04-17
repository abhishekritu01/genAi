# 🧠 Node.js — Complete Interview & Reference Notes

> A comprehensive, end-to-end reference covering Sections 1–36 plus a Miscellaneous section for advanced concepts.

---

## 📋 Table of Contents

1. [Node.js Basics](#section-1-nodejs-basics)
2. [Event Loop & Async Programming](#section-2-event-loop-and-asynchronous-programming)
3. [Core Modules](#section-3-core-modules)
4. [Asynchronous Programming Patterns](#section-4-asynchronous-programming-patterns)
5. [EventEmitter](#section-5-eventemitter)
6. [Streams and Buffers](#section-6-streams-and-buffers)
7. [File System (fs) Module](#section-7-file-system-fs-module)
8. [Libuv & Thread Pool](#section-8-libuv--thread-pool)
9. [Child Process, Cluster & Worker Threads](#section-9-child-process-cluster-and-worker-threads)
10. [Express.js Framework](#section-10-expressjs-framework)
11. [Security in Node.js](#section-11-security-in-nodejs)
12. [Authentication & Authorization](#section-12-authentication--authorization)
13. [Database Integration](#section-13-database-integration)
14. [API Design Patterns](#section-14-api-design-patterns)
15. [Error & Exception Handling](#section-15-error--exception-handling)
16. [Testing](#section-16-testing)
17. [Performance Optimization](#section-17-performance-optimization)
18. [Debugging & Profiling](#section-18-debugging--profiling)
19. [Deployment, Scaling & DevOps](#section-19-deployment-scaling--devops)
20. [Advanced Topics (Networking, Real-time, Patterns)](#section-20-advanced-topics)
21. [Node.js Internals & Advanced Concepts](#section-21-nodejs-internals--advanced-concepts)
22. [Node.js Design Patterns](#section-22-nodejs-design-patterns)
23. [Real-Time Communication (WebSockets)](#section-23-real-time-communication-websockets)
24. [Message Queues & Background Jobs](#section-24-message-queues--background-jobs)
25. [File Uploads & Handling](#section-25-file-uploads--handling)
26. [Advanced Security in Node.js](#section-26-advanced-security-in-nodejs)
27. [Authentication Deep Dive](#section-27-authentication-deep-dive)
28. [GraphQL with Node.js](#section-28-graphql-with-nodejs)
29. [Advanced Databases](#section-29-advanced-databases)
30. [Microservices Architecture](#section-30-microservices-architecture)
31. [Performance Optimization (Deep Dive)](#section-31-performance-optimization-deep-dive)
32. [Node.js with TypeScript](#section-32-nodejs-with-typescript)
33. [Testing & CI/CD](#section-33-testing--cicd)
34. [Monitoring & Observability](#section-34-monitoring--observability)
35. [Docker & Deployment](#section-35-docker--deployment)
36. [Node.js 20+ Features](#section-36-nodejs-20-features)
37. [Miscellaneous — Important Concepts](#miscellaneous--important-concepts)
38. [REST vs Event-Driven Architecture (Interview Notes)](#rest-vs-event-driven-architecture-interview-notes)

---

## Section 1: Node.js Basics

### 1. What is Node.js?

Node.js is a **runtime environment** that allows you to run JavaScript on the server side, built on Chrome's **V8 engine**. It enables building scalable, non-blocking, event-driven applications.

> Node.js is **not** a programming language or a framework — it is a runtime.

### 2. What makes Node.js fast?

- **V8 engine** compiles JavaScript to native machine code using JIT (Just-In-Time) compilation
- **Non-blocking I/O** via `libuv`
- **Event-driven architecture** avoids thread overhead

#### libuv — The Engine Behind Node.js

`libuv` is a C library used internally by Node.js to handle asynchronous I/O operations (file system, network, timers). It provides the **event loop** and **thread pool**.

| Feature | Description |
|---|---|
| 🕑 Event Loop | Manages async operations and decides what callback runs next |
| 🧵 Thread Pool | Handles expensive/blocking tasks (file I/O, DNS, crypto, compression) |
| 🌐 Cross-platform | Consistent API across Windows, macOS, and Linux |
| 📡 Async I/O | Non-blocking file/socket operations |

### 3. Is Node.js single-threaded?

Yes — Node.js is **single-threaded for JavaScript execution** but can use a **thread pool** (via libuv) for heavy I/O tasks. The event loop runs on one thread; operations like file reads are delegated to worker threads in the pool.

### 4. What is NPM?

**Node Package Manager** — used to install and manage third-party modules and dependencies. Comes bundled with Node.js.

```bash
npm install express          # install a package
npm install --save-dev jest  # install as dev dependency
npm init -y                  # create package.json with defaults
```

### 5. Node.js vs JavaScript

| Node.js | JavaScript |
|---|---|
| Runs on server | Runs in browser |
| Access to file system, OS, network | Access to DOM, BOM |
| Uses CommonJS modules | Uses ES Modules |
| Has `process`, `__dirname`, `__filename` | Has `window`, `document` |

### 6. What are modules in Node.js?

Reusable blocks of code. Three types:

- **Built-in** — `fs`, `http`, `os`, `path`, `events`, `crypto`, `url`
- **Local** — Your own `.js` files
- **Third-party** — Installed via npm (e.g., `express`, `mongoose`)

### 7. What is the CommonJS module system?

Uses `require()` and `module.exports` to import/export.

```javascript
// math.js (export)
module.exports = { add: (a, b) => a + b };

// app.js (import)
const math = require('./math');
console.log(math.add(2, 3)); // 5
```

### 8. Difference between `require()` and `import`

| Feature | `require()` | `import` |
|---|---|---|
| Module system | CommonJS | ES Modules |
| Loading | Synchronous | Asynchronous |
| Usage | `const x = require('x')` | `import x from 'x'` |
| Dynamic loading | Yes | Use `import()` function |
| `__dirname` available | Yes | No (use `import.meta.url`) |

### 9. What is `package.json`?

Metadata file that defines your Node project — name, version, scripts, dependencies, etc.

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

### 10. What is `package-lock.json`?

Locks the **exact versions** of all installed dependencies (including transitive ones) to ensure consistent installs across environments. Always commit this file.

### Performance Measurement

```javascript
console.time("label");
// ... operation
console.timeEnd("label"); // Prints elapsed time

// High-resolution timing
const { performance } = require('perf_hooks');
const start = performance.now();
// ... operation
console.log(performance.now() - start, 'ms');
```

---

## Section 2: Event Loop and Asynchronous Programming

### 11. What is the Event Loop?

The **event loop** is a mechanism that allows Node.js to handle many I/O operations without blocking a single thread. It continuously checks if there are callbacks ready to execute and runs them.

> Think of it as a loop that asks: "Is there anything to do? Run it. Now check again."

### 12. Phases of the Event Loop

```
   ┌──────────────────────────────┐
┌─>│           timers             │  ← setTimeout, setInterval callbacks
│  └─────────────┬────────────────┘
│  ┌─────────────▼────────────────┐
│  │     pending callbacks        │  ← I/O errors from previous iteration
│  └─────────────┬────────────────┘
│  ┌─────────────▼────────────────┐
│  │       idle, prepare          │  ← Internal use only
│  └─────────────┬────────────────┘
│  ┌─────────────▼────────────────┐
│  │           poll               │  ← Fetch new I/O events; execute callbacks
│  └─────────────┬────────────────┘
│  ┌─────────────▼────────────────┐
│  │           check              │  ← setImmediate callbacks
│  └─────────────┬────────────────┘
│  ┌─────────────▼────────────────┐
└──│      close callbacks         │  ← socket.on('close', ...)
   └──────────────────────────────┘
```

Between each phase, Node processes **microtasks** (process.nextTick + Promises).

### 13. `process.nextTick()` vs `setImmediate()`

| Feature | `process.nextTick()` | `setImmediate()` |
|---|---|---|
| Queue | Microtask queue | Macrotask queue (check phase) |
| When it runs | Before the event loop continues | After I/O events in check phase |
| Blocks event loop? | Yes, if called recursively | No |
| Use case | Immediate callback, before I/O | After current event loop cycle |

```javascript
console.log("Start");

process.nextTick(() => console.log("process.nextTick()"));
Promise.resolve().then(() => console.log("Promise then()"));
setImmediate(() => console.log("setImmediate()"));

console.log("End");

// Output:
// Start
// End
// process.nextTick()
// Promise then()
// setImmediate()
```

> ⚠️ `process.nextTick()` runs before promises. Both are microtasks but nextTick has higher priority.

### 14. Microtasks vs Macrotasks

| Type | Examples |
|---|---|
| Microtasks | `process.nextTick`, `Promise.then`, `queueMicrotask` |
| Macrotasks | `setTimeout`, `setImmediate`, `setInterval`, I/O callbacks |

Microtasks are always drained **completely** before moving to the next event loop phase.

### 15. What happens if the Event Loop is blocked?

The application becomes **unresponsive** — no new requests can be handled. To avoid blocking:

- Use async/await or callbacks for I/O
- Move CPU-heavy work to **Worker Threads** or **Child Processes**
- Use streaming for large data

---

## Section 3: Core Modules

### 16. Node.js Core Modules

Prebuilt libraries — no npm install needed:

| Module | Purpose |
|---|---|
| `fs` | File system operations |
| `http` / `https` | HTTP server/client |
| `path` | File path manipulation |
| `os` | Operating system info |
| `events` | EventEmitter |
| `crypto` | Hashing, encryption |
| `url` | URL parsing |
| `stream` | Readable/writable streams |
| `buffer` | Binary data handling |
| `child_process` | Spawn subprocesses |
| `cluster` | Multi-process scaling |
| `worker_threads` | CPU parallel execution |
| `net` | TCP/IPC servers |
| `dns` | DNS lookups |
| `zlib` | Compression |

### 17. The `fs` Module

```javascript
const fs = require('fs');

// Async read
fs.readFile('demo.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// Sync read (blocks event loop)
const data = fs.readFileSync('demo.txt', 'utf8');

// Write file
fs.writeFile('out.txt', 'Hello World', err => {
  if (err) throw err;
});

// Append to file
fs.appendFile('log.txt', 'new entry\n', err => { ... });

// Check if file exists
fs.access('file.txt', fs.constants.F_OK, err => {
  console.log(err ? 'Does not exist' : 'Exists');
});

// Delete file
fs.unlink('file.txt', err => { ... });

// Create directory
fs.mkdir('./newDir', { recursive: true }, err => { ... });

// Read directory
fs.readdir('./', (err, files) => console.log(files));
```

### 18. The `path` Module

```javascript
const path = require('path');

path.basename('/home/user/file.txt');     // 'file.txt'
path.dirname('/home/user/file.txt');      // '/home/user'
path.extname('file.txt');                 // '.txt'
path.join('/home', 'user', 'file.txt');  // '/home/user/file.txt'
path.resolve('src', 'index.js');         // absolute path
path.normalize('/home//user/../user/');  // '/home/user/'
```

### 19. The `os` Module

```javascript
const os = require('os');

os.platform();    // 'linux' / 'win32' / 'darwin'
os.arch();        // 'x64', 'arm'
os.cpus();        // Array of CPU info
os.totalmem();    // Total memory in bytes
os.freemem();     // Free memory in bytes
os.homedir();     // '/home/user'
os.hostname();    // Machine hostname
os.uptime();      // System uptime in seconds
```

### 20. The `http` Module

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ message: 'Hello Node' }));
});

server.listen(3000, () => console.log('Server on port 3000'));
```

### The `url` Module

```javascript
const { URL } = require('url');
const myURL = new URL('https://example.com/path?name=node&version=20');

myURL.hostname;           // 'example.com'
myURL.pathname;           // '/path'
myURL.searchParams.get('name'); // 'node'
```

### The `crypto` Module

```javascript
const crypto = require('crypto');

// Hash
const hash = crypto.createHash('sha256').update('password').digest('hex');

// Random bytes
const token = crypto.randomBytes(32).toString('hex');

// HMAC
const hmac = crypto.createHmac('sha256', 'secret')
  .update('data')
  .digest('hex');
```

---

## Section 4: Asynchronous Programming Patterns

### 21. Callbacks

Functions passed as arguments, executed after an operation completes.

```javascript
function fetchData(callback) {
  setTimeout(() => {
    callback(null, { id: 1, name: 'Node' });
  }, 1000);
}

fetchData((err, data) => {
  if (err) return console.error(err);
  console.log(data);
});
```

### 22. Callback Hell

Deeply nested callbacks create unreadable "pyramid of doom":

```javascript
readFile('a.txt', (err, a) => {
  readFile('b.txt', (err, b) => {
    writeFile('c.txt', a + b, (err) => {
      doSomethingElse((err) => {
        // and so on...
      });
    });
  });
});
```

**Solutions:** Promises, async/await, or named functions.

### 23. Promises

An object representing the **future completion or failure** of an async operation.

```javascript
const fetchUser = (id) => new Promise((resolve, reject) => {
  if (id <= 0) reject(new Error('Invalid ID'));
  else resolve({ id, name: 'Alice' });
});

fetchUser(1)
  .then(user => console.log(user))
  .catch(err => console.error(err))
  .finally(() => console.log('Done'));

// Promise combinators
Promise.all([p1, p2, p3]);       // All must resolve (fail-fast)
Promise.allSettled([p1, p2]);    // Waits for all, returns outcomes
Promise.race([p1, p2]);          // First to resolve/reject wins
Promise.any([p1, p2]);           // First to resolve wins (ignores rejects)
```

### 24. async/await

Syntactic sugar over Promises for synchronous-looking async code.

```javascript
async function getUserData(userId) {
  const user = await fetchUser(userId);       // waits for promise
  const posts = await fetchPosts(user.id);   // sequential
  return { user, posts };
}

// Parallel execution
const [user, posts] = await Promise.all([fetchUser(1), fetchPosts(1)]);
```

### 25. Error Handling in async/await

```javascript
async function getData() {
  try {
    const data = await fetchFromDB();
    return data;
  } catch (err) {
    console.error('DB Error:', err.message);
    throw err; // re-throw if needed
  } finally {
    console.log('Cleanup');
  }
}
```

> Always handle errors in async functions — unhandled rejections can crash the process.

---

## Section 5: EventEmitter

### 26. What is EventEmitter?

The `EventEmitter` class (from the `events` module) is the **core of Node's event-driven architecture**. It allows objects to emit named events and register listener functions.

Key points:
- Multiple listeners can be registered for the same event
- Many built-in modules (`http`, `fs`, `net`, `stream`) are EventEmitters
- Forms the foundation of the Observer pattern in Node.js

### 27. Using EventEmitter

```javascript
const EventEmitter = require('events');
const emitter = new EventEmitter();

// Register a listener
emitter.on('data', (payload) => {
  console.log('Received:', payload);
});

// One-time listener
emitter.once('connect', () => {
  console.log('Connected!');
});

// Emit an event with data
emitter.emit('data', { id: 1, msg: 'Hello' });
emitter.emit('connect');
emitter.emit('connect'); // 'once' listener won't fire again

// Remove a listener
const handler = () => console.log('Handler');
emitter.on('event', handler);
emitter.off('event', handler);        // alias: removeListener

// Remove all listeners for an event
emitter.removeAllListeners('data');

// Check listener count
console.log(emitter.listenerCount('data'));

// Get all listener names
console.log(emitter.eventNames());
```

### 28. Extending EventEmitter

```javascript
const EventEmitter = require('events');

class Logger extends EventEmitter {
  log(msg) {
    console.log(msg);
    this.emit('logged', { message: msg, timestamp: Date.now() });
  }
}

const logger = new Logger();
logger.on('logged', (info) => console.log('Log recorded:', info));
logger.log('User signed in');
```

### 29. `on` vs `once`

| Method | Behavior |
|---|---|
| `emitter.on(event, fn)` | Fires every time the event is emitted |
| `emitter.once(event, fn)` | Fires only the first time, then auto-removes |
| `emitter.off(event, fn)` | Removes a specific listener |
| `emitter.prependListener(event, fn)` | Adds listener to the beginning of the queue |

> ⚠️ Default max listeners is 10. Use `emitter.setMaxListeners(n)` to increase.

---

## Section 6: Streams and Buffers

### 30. What is a Stream?

A **stream** is a sequence of data chunks read or written over time, rather than loading everything into memory at once. Essential for handling large files or network data efficiently.

### 31. Types of Streams

| Type | Description | Example |
|---|---|---|
| Readable | Data can be read from | `fs.createReadStream()` |
| Writable | Data can be written to | `fs.createWriteStream()` |
| Duplex | Both readable and writable | TCP sockets |
| Transform | Duplex that modifies data | `zlib.createGzip()` |

### 32. Stream Examples

```javascript
const fs = require('fs');

// Readable stream
const readStream = fs.createReadStream('input.txt', { encoding: 'utf8' });
readStream.on('data', chunk => process.stdout.write(chunk));
readStream.on('end', () => console.log('Done reading'));
readStream.on('error', err => console.error(err));

// Writable stream
const writeStream = fs.createWriteStream('output.txt');
writeStream.write('Hello ');
writeStream.write('World');
writeStream.end(); // signals no more data

// Pipe: readable → writable
fs.createReadStream('input.txt').pipe(fs.createWriteStream('output.txt'));

// Transform: compress a file
const zlib = require('zlib');
fs.createReadStream('file.txt')
  .pipe(zlib.createGzip())
  .pipe(fs.createWriteStream('file.txt.gz'));
```

### 33. Backpressure in Streams

**Backpressure** occurs when the writable stream cannot handle the incoming data speed from the readable stream. `pipe()` handles this automatically by pausing the readable stream when the writable buffer is full.

```javascript
// Manual backpressure handling
const readable = fs.createReadStream('big.txt');
const writable = fs.createWriteStream('out.txt');

readable.on('data', chunk => {
  const canContinue = writable.write(chunk);
  if (!canContinue) {
    readable.pause(); // pause until drain
    writable.once('drain', () => readable.resume());
  }
});
```

### 34. What is a Buffer?

A `Buffer` is a fixed-size chunk of memory outside the V8 heap, used to handle **binary data** (e.g., images, TCP streams, file I/O).

```javascript
// Create buffers
const buf1 = Buffer.alloc(10);            // zero-filled, 10 bytes
const buf2 = Buffer.from('Hello');        // from string
const buf3 = Buffer.from([0x48, 0x69]);  // from byte array

// Convert
buf2.toString('utf8');   // 'Hello'
buf2.toString('hex');    // '48656c6c6f'
buf2.toString('base64'); // 'SGVsbG8='

// Buffer operations
Buffer.concat([buf1, buf2]);
buf2.length; // 5
buf2.copy(buf1); // copy into another buffer
```

---

## Section 7: File System (fs) Module

### 35. Async vs Sync FS Methods

```javascript
// Async — does NOT block the event loop
fs.readFile('file.txt', 'utf8', (err, data) => { ... });

// Sync — BLOCKS the event loop until complete
const data = fs.readFileSync('file.txt', 'utf8');

// Promise-based (recommended)
const fs = require('fs').promises;
const data = await fs.readFile('file.txt', 'utf8');
```

> Use async methods in production. Sync methods are acceptable in startup scripts.

### 36. File Operations Cheat Sheet

```javascript
const fs = require('fs/promises'); // Promise-based API

// Read
await fs.readFile('file.txt', 'utf8');

// Write (overwrites)
await fs.writeFile('file.txt', 'content');

// Append
await fs.appendFile('file.txt', 'more content');

// Copy
await fs.copyFile('src.txt', 'dest.txt');

// Rename / Move
await fs.rename('old.txt', 'new.txt');

// Delete
await fs.unlink('file.txt');

// Stat (file info)
const stat = await fs.stat('file.txt');
console.log(stat.size, stat.mtime);

// Create directory
await fs.mkdir('./dir', { recursive: true });

// Remove directory
await fs.rmdir('./dir', { recursive: true });

// List directory
const files = await fs.readdir('./');
```

### 37. Watch Files for Changes

```javascript
fs.watch('file.txt', (eventType, filename) => {
  console.log(`Event: ${eventType}, File: ${filename}`);
});

// More reliable with chokidar (npm package)
const chokidar = require('chokidar');
chokidar.watch('./src').on('change', path => console.log(`Changed: ${path}`));
```

---

## Section 8: Libuv & Thread Pool

### 38. What is libuv?

A C library that provides Node.js with:
- The **event loop**
- A **thread pool** (default 4 threads) for blocking operations
- Cross-platform async I/O abstraction

### 39. Default Thread Pool Size

Default: **4 threads**. Can be changed:

```bash
UV_THREADPOOL_SIZE=8 node app.js
# or
process.env.UV_THREADPOOL_SIZE = 8;
```

### 40. Tasks That Use the Thread Pool

| Operation | Uses Thread Pool? |
|---|---|
| File I/O (`fs` module) | ✅ Yes |
| DNS lookups (`dns.lookup`) | ✅ Yes |
| Crypto operations | ✅ Yes |
| Zlib compression | ✅ Yes |
| Network I/O (TCP/UDP) | ❌ No (uses OS async primitives) |
| `child_process` | ❌ No (separate processes) |

---

## Section 9: Child Process, Cluster and Worker Threads

### 41. Child Processes

Used to spawn new OS processes and execute shell commands or other scripts.

```javascript
const { exec, spawn, fork, execFile } = require('child_process');

// exec — runs command in shell, buffers output
exec('ls -la', (err, stdout, stderr) => {
  console.log(stdout);
});

// spawn — streams stdout/stderr (better for large output)
const ls = spawn('ls', ['-la']);
ls.stdout.on('data', data => console.log(data.toString()));
ls.on('close', code => console.log(`Exit code: ${code}`));

// fork — spawns a new Node.js process with IPC channel
const child = fork('./worker.js');
child.send({ task: 'compute' });
child.on('message', result => console.log(result));

// execFile — executes a file directly (no shell)
execFile('node', ['--version'], (err, stdout) => console.log(stdout));
```

### 42. Clustering

Creates multiple Node.js processes (one per CPU core) to scale on multi-core systems. All workers share the same port.

```javascript
const cluster = require('cluster');
const http = require('http');
const os = require('os');

if (cluster.isPrimary) {
  const numCPUs = os.cpus().length;
  console.log(`Primary ${process.pid} spawning ${numCPUs} workers`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code) => {
    console.log(`Worker ${worker.process.pid} died. Restarting...`);
    cluster.fork(); // auto-restart
  });
} else {
  http.createServer((req, res) => {
    res.end(`Handled by worker ${process.pid}`);
  }).listen(3000);
}
```

### 43. Worker Threads

Run JavaScript in **parallel** on multiple threads — ideal for CPU-intensive tasks (image processing, complex calculations).

```javascript
// main.js
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

if (isMainThread) {
  const worker = new Worker(__filename, { workerData: { num: 42 } });
  worker.on('message', result => console.log('Result:', result));
  worker.on('error', err => console.error(err));
} else {
  const result = workerData.num * 2;
  parentPort.postMessage(result); // send back to main thread
}
```

### 44. Cluster vs Worker Threads vs Child Process

| Feature | Cluster | Worker Threads | Child Process |
|---|---|---|---|
| Memory | Separate | Shared (SharedArrayBuffer) | Separate |
| Communication | IPC / socket | MessageChannel | IPC / stdio |
| Best for | HTTP scaling | CPU tasks (same process) | Running external programs |
| Overhead | High (full process) | Low (same process) | High |

---

## Section 10: Express.js Framework

### 45. What is Express.js?

A minimal, unopinionated web framework for Node.js that simplifies routing, middleware, and HTTP handling.

```javascript
const express = require('express');
const app = express();

app.use(express.json());           // parse JSON bodies
app.use(express.urlencoded({ extended: true })); // parse URL-encoded bodies

app.get('/', (req, res) => res.send('Hello Express'));
app.listen(3000, () => console.log('Running on :3000'));
```

### 46. Middleware

Functions that execute in the **request-response cycle**, in order. Must call `next()` to continue.

```javascript
// Application-level middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next(); // pass to next middleware/route
});

// Route-level middleware
const authMiddleware = (req, res, next) => {
  if (!req.headers.authorization) return res.status(401).json({ error: 'Unauthorized' });
  next();
};

app.get('/protected', authMiddleware, (req, res) => res.send('Secret'));
```

### 47. Types of Middleware

| Type | Example |
|---|---|
| Application-level | `app.use(fn)` |
| Router-level | `router.use(fn)` |
| Built-in | `express.json()`, `express.static()` |
| Error-handling | `app.use((err, req, res, next) => {})` |
| Third-party | `morgan`, `cors`, `helmet` |

### 48. `next()` — How It Works

```javascript
app.use((req, res, next) => {
  console.log('Middleware 1');
  next();           // continue to next
});

app.use((req, res, next) => {
  console.log('Middleware 2');
  next(new Error('Something went wrong')); // skip to error handler
});

// Error handling middleware (4 parameters)
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message });
});
```

### 49. Route Parameters and Query Strings

```javascript
// Route parameter
app.get('/user/:id', (req, res) => {
  res.json({ userId: req.params.id });
});

// Multiple params
app.get('/post/:year/:month', (req, res) => {
  const { year, month } = req.params;
  res.json({ year, month });
});

// Query string: GET /search?q=node&page=2
app.get('/search', (req, res) => {
  const { q, page = 1 } = req.query;
  res.json({ query: q, page });
});
```

### 50. Express Router

Groups routes into modular files:

```javascript
// routes/users.js
const router = require('express').Router();

router.get('/', getAllUsers);
router.get('/:id', getUserById);
router.post('/', createUser);
router.put('/:id', updateUser);
router.delete('/:id', deleteUser);

module.exports = router;

// app.js
app.use('/api/users', require('./routes/users'));
```

---

## Section 11: Security in Node.js

### 51. Common Security Risks

- **Injection attacks** (SQL, NoSQL, command injection)
- **XSS** (Cross-Site Scripting)
- **CSRF** (Cross-Site Request Forgery)
- **Insecure cookies**
- **Exposed secrets/tokens** in code
- **Unvalidated/unsanitized inputs**
- **Outdated dependencies** with known CVEs

### 52. Protecting Against XSS

```javascript
// Use DOMPurify (client-side) or sanitize-html (server-side)
const sanitizeHtml = require('sanitize-html');
const clean = sanitizeHtml(userInput, {
  allowedTags: ['b', 'i', 'em'],
  allowedAttributes: {}
});

// Use validator for input validation
const validator = require('validator');
validator.isEmail('test@mail.com'); // true
validator.escape('<script>alert(1)</script>'); // escapes HTML
```

### 53. Preventing SQL Injection

```javascript
// ❌ WRONG — string concatenation
db.query(`SELECT * FROM users WHERE name = '${userInput}'`);

// ✅ CORRECT — parameterized queries
db.query('SELECT * FROM users WHERE name = ?', [userInput]);

// ✅ With ORM (Sequelize)
User.findAll({ where: { name: userInput } });
```

### 54. CSRF Protection

```javascript
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/submit', csrfProtection, (req, res) => {
  res.send('Form submitted');
});
```

### 55. Securing Cookies

```javascript
res.cookie('session', token, {
  httpOnly: true,   // not accessible via JS (prevents XSS)
  secure: true,     // HTTPS only
  sameSite: 'Strict', // prevents CSRF
  maxAge: 3600000   // 1 hour
});
```

### 56. Password Hashing with bcrypt

```javascript
const bcrypt = require('bcryptjs');

// Hash on signup
const hash = await bcrypt.hash(plainPassword, 10); // 10 salt rounds
await User.create({ password: hash });

// Compare on login
const isMatch = await bcrypt.compare(inputPassword, storedHash);
if (!isMatch) return res.status(401).json({ error: 'Invalid credentials' });
```

### 57. Helmet.js

Secures Express apps by setting various HTTP headers:

```javascript
const helmet = require('helmet');
app.use(helmet());
// Sets: Content-Security-Policy, X-Frame-Options, X-XSS-Protection,
//       Strict-Transport-Security, X-Content-Type-Options, etc.
```

### 58. Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                   // max requests per window per IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' }
});

app.use('/api/', limiter);
```

---

## Section 12: Authentication & Authorization

### 59. Authentication vs Authorization

| | Authentication | Authorization |
|---|---|---|
| Question | Who are you? | What can you do? |
| Process | Login / Signup | Role / Permission check |
| Example | JWT, sessions, OAuth | Admin vs User, RBAC |

### 60. What is JWT?

**JSON Web Token** — a compact, self-contained token for stateless authentication.

### 61. JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.    ← Header (Base64)
eyJ1c2VySWQiOjEsInJvbGUiOiJ1c2VyIn0.     ← Payload (Base64)
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQs  ← Signature
```

- **Header** — algorithm & token type
- **Payload** — claims (userId, role, exp)
- **Signature** — HMAC of header + payload using secret key

### 62. Securing JWTs

- Short expiry on access tokens (15 min)
- Store in **HttpOnly cookies** (not localStorage)
- Use **HTTPS** only
- Rotate tokens (refresh token pattern)
- Validate signature on every request

### 63. What is OAuth 2.0?

An open authorization standard. Allows apps to access user data via third-party providers (Google, GitHub) without seeing credentials.

**Flow:** App → Provider (login) → App gets authorization code → Exchange for access token → Use token to access resources

---

## Section 13: Database Integration

### 64. Connecting MongoDB with Mongoose

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

mongoose.connection.on('connected', () => console.log('MongoDB connected'));
mongoose.connection.on('error', err => console.error(err));
```

### 65. Mongoose vs Native MongoDB Driver

| Feature | Mongoose (ODM) | Native Driver |
|---|---|---|
| Schema validation | ✅ Built-in | ❌ Manual |
| Middleware hooks | ✅ pre/post | ❌ No |
| Type casting | ✅ Automatic | ❌ Manual |
| Query builder | ✅ Chainable | Partial |
| Performance | Slight overhead | Faster |
| Use case | Apps with defined data models | Flexible/dynamic data |

### 66. Connection Pooling

```javascript
// Mongoose — pool is managed automatically (default: 5)
mongoose.connect(uri, { maxPoolSize: 10 });

// mysql2 — explicit pool
const mysql = require('mysql2/promise');
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  database: 'mydb',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

const [rows] = await pool.execute('SELECT * FROM users WHERE id = ?', [1]);
```

### 67. Mongoose Schema & Model

```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, minlength: 6 },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// CRUD
const user = await User.create({ name: 'Alice', email: 'alice@mail.com', password: 'hashed' });
const users = await User.find({ role: 'user' }).sort({ name: 1 }).limit(10);
const updated = await User.findByIdAndUpdate(id, { name: 'Bob' }, { new: true });
await User.findByIdAndDelete(id);
```

### 68. Transactions in MongoDB

```javascript
const session = await mongoose.startSession();
session.startTransaction();

try {
  await Account.updateOne({ _id: fromId }, { $inc: { balance: -100 } }, { session });
  await Account.updateOne({ _id: toId }, { $inc: { balance: 100 } }, { session });
  await session.commitTransaction();
} catch (err) {
  await session.abortTransaction();
  throw err;
} finally {
  session.endSession();
}
```

### 69. Indexes in MongoDB

```javascript
// Create indexes in schema
userSchema.index({ email: 1 }, { unique: true });
userSchema.index({ name: 'text' }); // full-text search
userSchema.index({ createdAt: -1 }); // for sorting

// Compound index
userSchema.index({ role: 1, createdAt: -1 });
```

> Indexes **speed up reads** but **slow down writes**. Index fields used frequently in queries.

---

## Section 14: API Design Patterns

### 70. REST API Design

**REST** = Representational State Transfer. Stateless, resource-based API using HTTP methods.

| HTTP Method | Action | Example |
|---|---|---|
| GET | Read | `GET /users` |
| POST | Create | `POST /users` |
| PUT | Replace | `PUT /users/1` |
| PATCH | Update | `PATCH /users/1` |
| DELETE | Delete | `DELETE /users/1` |

```javascript
// RESTful route example
app.get('/api/v1/users', getAllUsers);
app.get('/api/v1/users/:id', getUserById);
app.post('/api/v1/users', createUser);
app.patch('/api/v1/users/:id', updateUser);
app.delete('/api/v1/users/:id', deleteUser);
```

### 71. REST vs GraphQL

| Feature | REST | GraphQL |
|---|---|---|
| Endpoints | Multiple | Single (`/graphql`) |
| Data fetching | Fixed response | Request exactly what you need |
| Over/under-fetching | Common | Eliminated |
| Caching | HTTP caching (simple) | Requires custom cache |
| Versioning | `/v1`, `/v2` | Schema evolution |
| Learning curve | Low | Medium |

### 72. HATEOAS

**Hypermedia As The Engine Of Application State** — API responses include links to related actions.

```json
{
  "id": 1,
  "name": "Alice",
  "_links": {
    "self": { "href": "/users/1" },
    "posts": { "href": "/users/1/posts" },
    "delete": { "href": "/users/1", "method": "DELETE" }
  }
}
```

### 73. gRPC

**gRPC** (Google Remote Procedure Call) — high-performance RPC framework using HTTP/2 + Protocol Buffers.

| Feature | REST | gRPC |
|---|---|---|
| Protocol | HTTP/1.1 | HTTP/2 |
| Data format | JSON (text) | Protobuf (binary) |
| Streaming | Limited (SSE/WS) | Bidirectional streaming |
| Performance | Good | Excellent |
| Use case | Public APIs | Internal microservices |

### 74. Pagination Patterns

```javascript
// Offset-based (simple but slow for large datasets)
const page = parseInt(req.query.page) || 1;
const limit = parseInt(req.query.limit) || 10;
const skip = (page - 1) * limit;

const [users, total] = await Promise.all([
  User.find().skip(skip).limit(limit).lean(),
  User.countDocuments()
]);

res.json({
  data: users,
  pagination: { page, limit, total, pages: Math.ceil(total / limit) }
});

// Cursor-based (efficient for large datasets)
const lastId = req.query.cursor;
const query = lastId ? { _id: { $gt: lastId } } : {};
const users = await User.find(query).limit(limit).sort({ _id: 1 });
const nextCursor = users.length ? users[users.length - 1]._id : null;

res.json({ data: users, nextCursor });
```

### 75. API Versioning

```javascript
// URL versioning (most common)
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Header versioning
app.use((req, res, next) => {
  req.version = req.headers['api-version'] || 'v1';
  next();
});
```

---

## Section 15: Error & Exception Handling

### 76. Operational vs Programmer Errors

| Type | Description | Action |
|---|---|---|
| Operational | Expected errors (DB down, network timeout, 404) | Handle gracefully |
| Programmer | Bugs (undefined is not a function, logic errors) | Fix the code |

### 77. Handling Uncaught Exceptions

```javascript
process.on('uncaughtException', (err) => {
  console.error('UNCAUGHT EXCEPTION:', err);
  // Perform cleanup
  process.exit(1); // always exit — state may be corrupted
});
```

### 78. Handling Unhandled Promise Rejections

```javascript
process.on('unhandledRejection', (reason, promise) => {
  console.error('UNHANDLED REJECTION at:', promise, 'reason:', reason);
  process.exit(1);
});
```

### 79. Custom Error Classes

```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = statusCode >= 400 && statusCode < 500 ? 'fail' : 'error';
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404);
  }
}

class ValidationError extends AppError {
  constructor(message) {
    super(message, 400);
  }
}

// Usage
throw new NotFoundError('User not found');
```

### 80. Centralized Error Handler

```javascript
// errorHandler.js
const errorHandler = (err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.message = err.message || 'Internal Server Error';

  if (process.env.NODE_ENV === 'development') {
    return res.status(err.statusCode).json({
      status: err.status,
      error: err,
      message: err.message,
      stack: err.stack
    });
  }

  // Production: don't leak stack traces
  if (err.isOperational) {
    return res.status(err.statusCode).json({ status: err.status, message: err.message });
  }

  // Unknown errors — don't leak details
  console.error('ERROR:', err);
  res.status(500).json({ status: 'error', message: 'Something went wrong' });
};

// app.js
app.use(errorHandler);
```

### Async Error Wrapper

```javascript
// Wraps async route handlers to catch errors
const catchAsync = (fn) => (req, res, next) => fn(req, res, next).catch(next);

app.get('/users', catchAsync(async (req, res) => {
  const users = await User.find();
  res.json(users);
}));
```

---

## Section 16: Testing

### 81. Testing Frameworks

| Tool | Purpose |
|---|---|
| **Jest** | Full-featured test runner + assertions + mocking |
| **Mocha** | Test runner (flexible) |
| **Chai** | Assertion library for Mocha |
| **Supertest** | HTTP assertions for Express |
| **Sinon** | Spies, stubs, mocks |
| **nock** | HTTP request mocking |

### 82. Unit vs Integration vs E2E Tests

| Type | Scope | Speed | Example |
|---|---|---|---|
| Unit | Single function/module | ⚡ Fastest | Test a `calculateTax()` function |
| Integration | Multiple modules together | 🔶 Medium | Test controller + service + DB |
| E2E | Full user flow | 🐢 Slow | Register → Login → Buy product |

### 83. Jest Examples

```javascript
// math.test.js
const { add, multiply } = require('./math');

describe('Math functions', () => {
  test('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('multiplies numbers', () => {
    expect(multiply(4, 5)).toBe(20);
  });
});

// Async test
test('fetches user', async () => {
  const user = await fetchUser(1);
  expect(user).toHaveProperty('id', 1);
  expect(user.name).toBeTruthy();
});

// Mock a module
jest.mock('./emailService');
const emailService = require('./emailService');
emailService.sendEmail.mockResolvedValue({ success: true });
```

### 84. Supertest for API Testing

```javascript
const request = require('supertest');
const app = require('../app');

describe('GET /api/users', () => {
  it('returns 200 with users array', async () => {
    const res = await request(app)
      .get('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(res.body).toBeInstanceOf(Array);
  });

  it('returns 401 without token', async () => {
    await request(app).get('/api/users').expect(401);
  });
});
```

### 85. Mocking DB Calls

```javascript
// Using jest.mock
jest.mock('../models/User');
const User = require('../models/User');

User.find.mockResolvedValue([{ id: 1, name: 'Alice' }]);
User.findById.mockResolvedValue({ id: 1, name: 'Alice' });
User.create.mockResolvedValue({ id: 2, name: 'Bob' });

// Using in-memory MongoDB (mongoose-memory-server)
const { MongoMemoryServer } = require('mongodb-memory-server');
```

---

## Section 17: Performance Optimization

### 86. Handling Large Data with Streams

```javascript
// ❌ Loads entire file into memory
const data = fs.readFileSync('bigfile.csv');

// ✅ Streams data chunk by chunk
const stream = fs.createReadStream('bigfile.csv');
stream.on('data', processChunk);
stream.on('end', () => console.log('Done'));
```

### 87. Response Compression

```javascript
const compression = require('compression');
app.use(compression({
  level: 6,     // 0-9, tradeoff between speed and compression
  threshold: 1024, // only compress responses > 1KB
  filter: (req, res) => {
    if (req.headers['x-no-compression']) return false;
    return compression.filter(req, res);
  }
}));
```

### 88. Caching Strategies

```javascript
// In-memory cache (node-cache)
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 300 }); // 5 min TTL

app.get('/users', async (req, res) => {
  const cached = cache.get('users');
  if (cached) return res.json(cached);

  const users = await User.find().lean();
  cache.set('users', users);
  res.json(users);
});

// Redis cache
const redis = require('redis');
const client = redis.createClient();

const cacheMiddleware = (ttl) => async (req, res, next) => {
  const key = req.originalUrl;
  const cached = await client.get(key);
  if (cached) return res.json(JSON.parse(cached));

  res.sendResponse = res.json;
  res.json = (body) => {
    client.setEx(key, ttl, JSON.stringify(body));
    res.sendResponse(body);
  };
  next();
};
```

### 89. Clustering for Performance

```javascript
const cluster = require('cluster');
const os = require('os');

if (cluster.isPrimary) {
  os.cpus().forEach(() => cluster.fork());
  cluster.on('exit', () => cluster.fork());
} else {
  require('./app'); // each worker runs the app
}
```

### 90. Performance Profiling Tools

| Tool | Purpose |
|---|---|
| `node --inspect` | Chrome DevTools profiler |
| `clinic.js` | CPU/memory/event loop analysis |
| `perf_hooks` | Built-in performance measurement |
| `0x` | Flame graph profiler |
| `autocannon` | HTTP benchmarking |

### 91. Preventing Memory Leaks

Common causes:
- **Global variables** holding large objects
- **Event listeners** not removed
- **Timers** (setInterval) not cleared
- **Closures** retaining old references
- **Caches** without size limits

```javascript
// ✅ Always remove event listeners
const handler = () => { ... };
emitter.on('event', handler);
// ... later
emitter.off('event', handler);

// ✅ Clear intervals when done
const interval = setInterval(fn, 1000);
// ... later
clearInterval(interval);

// ✅ Use WeakMap/WeakSet for object-keyed caches
const cache = new WeakMap(); // keys are garbage collected when no other references exist
```

### 92. Async Performance Tips

```javascript
// ❌ Sequential — slow
const user = await getUser(1);
const posts = await getPosts(1);

// ✅ Parallel — fast
const [user, posts] = await Promise.all([getUser(1), getPosts(1)]);

// Batch DB writes
const bulkOps = users.map(u => ({ insertOne: { document: u } }));
await User.bulkWrite(bulkOps);
```

---

## Section 18: Debugging & Profiling

### 93. Debugging with Node Inspector

```bash
node --inspect app.js          # attach debugger
node --inspect-brk app.js      # break before first line
```

Open `chrome://inspect` in Chrome → click "Open dedicated DevTools for Node"

### 94. Console Debugging

```javascript
console.log('basic');
console.error('error in red');
console.warn('warning in yellow');
console.table([{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]);
console.group('Section');
  console.log('grouped output');
console.groupEnd();
console.time('operation');
// ... code
console.timeEnd('operation'); // operation: 32.5ms
console.dir(obj, { depth: null }); // deep object inspection
console.trace('How did we get here?');
```

### 95. Heap Snapshot

```bash
# Start with --inspect, then take snapshot in Chrome Memory tab
node --inspect app.js

# Or use heapdump
npm install heapdump
process.kill(process.pid, 'SIGUSR2'); // triggers snapshot on signal
```

### 96. Event Loop Delay Monitoring

```javascript
const { monitorEventLoopDelay } = require('perf_hooks');

const histogram = monitorEventLoopDelay({ resolution: 20 });
histogram.enable();

setInterval(() => {
  console.log('Mean lag:', histogram.mean / 1e6, 'ms');
  console.log('Max lag:', histogram.max / 1e6, 'ms');
  histogram.reset();
}, 5000);
```

---

## Section 19: Deployment, Scaling & DevOps

### 97. Running Node in Production

```bash
# PM2 — Process manager
npm install -g pm2
pm2 start app.js --name "my-api" -i max  # cluster mode on all CPUs
pm2 start ecosystem.config.js            # config file approach
pm2 save                                  # persist process list
pm2 startup                              # auto-start on reboot
```

### 98. Zero-Downtime Deployment

```bash
pm2 reload app-name    # graceful reload (zero downtime)
pm2 restart app-name   # hard restart (brief downtime)
```

### 99. Reverse Proxying with Nginx

```nginx
upstream nodejs_app {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://nodejs_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 100. Horizontal vs Vertical Scaling

| Strategy | Horizontal | Vertical |
|---|---|---|
| Method | Add more instances/servers | Add CPU/RAM to existing server |
| Cost | Scales incrementally | Expensive hardware |
| Complexity | Load balancer needed | Simpler |
| Limits | Practically unlimited | Hardware limit |

### 101. Docker Deployment

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

```bash
docker build -t my-node-app .
docker run -d -p 3000:3000 --env-file .env my-node-app
```

### 102. Environment Variables

```javascript
// .env
DB_URL=mongodb://localhost:27017/mydb
JWT_SECRET=supersecret
PORT=3000
NODE_ENV=production

// app.js
require('dotenv').config();
const port = process.env.PORT || 3000;
const dbUrl = process.env.DB_URL;
```

---

## Section 20: Advanced Topics

### 103. TCP vs UDP vs HTTP

| Protocol | Reliability | Speed | Use Case |
|---|---|---|---|
| TCP | Reliable (ordered, ACK) | Moderate | HTTP, databases, file transfer |
| UDP | Unreliable (no ACK) | Fast | Video streaming, gaming, DNS |
| HTTP | Application layer over TCP | — | Web APIs, browser communication |

### 104. HTTP/2

- **Multiplexing** — multiple requests over a single TCP connection
- **Header compression** (HPACK) — reduces overhead
- **Server push** — server proactively sends resources
- **Binary protocol** — faster to parse than HTTP/1.1 text

```javascript
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt')
});

server.on('stream', (stream, headers) => {
  stream.respond({ ':status': 200, 'content-type': 'text/html' });
  stream.end('<h1>Hello HTTP/2</h1>');
});

server.listen(443);
```

### 105. WebSocket vs SSE

| Feature | WebSocket | Server-Sent Events (SSE) |
|---|---|---|
| Direction | Bidirectional | Server → Client only |
| Protocol | WS/WSS | HTTP |
| Reconnection | Manual | Automatic |
| Use case | Chat, gaming | Live feeds, notifications |
| Browser support | All modern | All modern (except older IE) |

### 106. Keep-Alive

Reuses TCP connections for multiple HTTP requests, reducing handshake overhead:

```javascript
const http = require('http');
const agent = new http.Agent({ keepAlive: true, maxSockets: 10 });
http.get({ hostname: 'api.example.com', agent }, res => { ... });
```

### 107. Real-Time Communication with Socket.IO

```javascript
// Server
const io = require('socket.io')(httpServer, {
  cors: { origin: '*' }
});

io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);

  socket.on('message', (data) => {
    io.emit('message', data); // broadcast to all
    socket.broadcast.emit('message', data); // broadcast except sender
  });

  socket.on('disconnect', () => console.log('User disconnected'));
});

// Client
const socket = io('http://localhost:3000');
socket.emit('message', { text: 'Hello' });
socket.on('message', data => console.log(data));
```

### 108. Scaling Socket.IO with Redis

```javascript
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);
io.adapter(createAdapter(pubClient, subClient));
```

### 109–115. Design Patterns Overview

| Pattern | Description |
|---|---|
| **Dependency Injection** | Inject dependencies via constructor/factory instead of hard-coding |
| **Middleware Chain** | Series of functions executed in sequence (Express model) |
| **Event-Driven** | Components communicate via events (EventEmitter, Kafka) |
| **Observer** | Objects subscribe to events, react when they occur |
| **Strategy** | Define a family of algorithms, select one at runtime |
| **Proxy** | Intercepts requests and forwards to target (middleware, API gateway) |
| **Singleton** | A single instance shared throughout the app (module cache) |

---

## Section 21: Node.js Internals & Advanced Concepts

### 116. How the V8 Engine Works

1. **Parsing** — JS source code → AST (Abstract Syntax Tree)
2. **Bytecode generation** — AST → bytecode (Ignition interpreter)
3. **JIT Compilation** — Hot code paths → native machine code (TurboFan compiler)
4. **Optimization** — Frequently called code is re-optimized

> JIT = code is compiled at runtime, not ahead of time.

### 117. Garbage Collection in V8

V8 uses **generational garbage collection**:

- **Young generation (Minor GC)** — Short-lived objects, collected frequently using Scavenge algorithm
- **Old generation (Major GC)** — Long-lived objects, collected using Mark-Sweep-Compact

```javascript
// Force GC (only in --expose-gc mode)
node --expose-gc -e "global.gc(); console.log(process.memoryUsage());"
```

### 118. Node.js Architecture Components

```
┌─────────────────────────────────────────┐
│           Your JavaScript Code          │
├─────────────────────────────────────────┤
│           Node.js Bindings (C++)        │
├─────────────────────────────────────────┤
│    V8 (JS engine)    │  libuv           │
│    - Executes JS     │  - Event loop    │
│    - GC              │  - Thread pool   │
│                      │  - Async I/O     │
├─────────────────────────────────────────┤
│           Operating System              │
└─────────────────────────────────────────┘
```

### 119. `process.nextTick()` vs `Promise.then()`

Both are microtasks, but **`process.nextTick()` runs before Promise callbacks**.

```javascript
Promise.resolve().then(() => console.log('Promise'));
process.nextTick(() => console.log('nextTick'));
// Output: nextTick → Promise
```

### 120. Detecting Memory Leaks

```bash
# Run with heap inspection
node --inspect --max-old-space-size=512 app.js
```

Tools:
- **Chrome DevTools** — Memory tab, heap snapshots
- **clinic.js** — `clinic doctor -- node app.js`
- **heapdump** — npm package for programmatic snapshots
- **memwatch-next** — detects leaks and diffs

---

## Section 22: Node.js Design Patterns

### 121. Module Pattern

Encapsulates private state, exposes only a public API:

```javascript
const counter = (() => {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    get: () => count,
    reset: () => { count = 0; }
  };
})();

counter.increment();
counter.increment();
console.log(counter.get()); // 2
```

### 122. Singleton Pattern

Node.js module cache ensures modules are singletons:

```javascript
// db.js
const mongoose = require('mongoose');

class Database {
  constructor() {
    if (Database.instance) return Database.instance;
    Database.instance = this;
    this.connection = null;
  }

  async connect(uri) {
    if (!this.connection) {
      this.connection = await mongoose.connect(uri);
    }
    return this.connection;
  }
}

module.exports = new Database(); // always the same instance
```

### 123. Factory Pattern

```javascript
function createUser(type) {
  const users = {
    admin: () => ({ role: 'admin', canDelete: true, canWrite: true }),
    editor: () => ({ role: 'editor', canDelete: false, canWrite: true }),
    viewer: () => ({ role: 'viewer', canDelete: false, canWrite: false })
  };
  return users[type] ? users[type]() : users.viewer();
}

const admin = createUser('admin');
```

### 124. Observer Pattern

```javascript
class EventBus extends require('events') {}
const bus = new EventBus();

// Subscribers
bus.on('user:registered', (user) => sendWelcomeEmail(user));
bus.on('user:registered', (user) => createUserProfile(user));

// Publisher
async function registerUser(userData) {
  const user = await User.create(userData);
  bus.emit('user:registered', user); // notifies all subscribers
  return user;
}
```

### 125. MVC Pattern in Express

```
app/
├── controllers/     ← Handle HTTP requests/responses
│   └── userController.js
├── services/        ← Business logic
│   └── userService.js
├── models/          ← Database schemas
│   └── User.js
├── routes/          ← Route definitions
│   └── userRoutes.js
└── middleware/      ← Cross-cutting concerns
    └── auth.js
```

---

## Section 23: Real-Time Communication (WebSockets)

### 126. WebSockets vs HTTP

| Feature | HTTP | WebSocket |
|---|---|---|
| Connection | Request-Response | Persistent |
| State | Stateless | Stateful |
| Direction | Unidirectional | Bidirectional |
| Overhead | Headers on every request | Single handshake |

### 127. Socket.IO Rooms and Namespaces

```javascript
// Namespaces — logical channels
const chatNS = io.of('/chat');
const newsNS = io.of('/news');

chatNS.on('connection', socket => {
  console.log('Chat user connected');
});

// Rooms — groups within a namespace
io.on('connection', socket => {
  // Join a room
  socket.join('room1');

  // Send to a specific room
  io.to('room1').emit('message', 'Hello room!');

  // Leave a room
  socket.leave('room1');

  // Send to all in room except sender
  socket.to('room1').emit('message', 'Hello others!');
});
```

---

## Section 24: Message Queues & Background Jobs

### 128. Why Use Message Queues?

- Decouple services
- Retry failed jobs
- Control throughput (rate limiting)
- Offload heavy work from request cycle
- Ensure task persistence

### 129. Bull Queue with Redis

```javascript
const Queue = require('bull');

const emailQueue = new Queue('email', { redis: { host: 'localhost', port: 6379 } });

// Producer — add jobs
emailQueue.add({ to: 'user@mail.com', subject: 'Welcome' }, {
  attempts: 3,       // retry up to 3 times
  backoff: 5000,     // wait 5s between retries
  delay: 2000        // start after 2s delay
});

// Consumer — process jobs
emailQueue.process(async (job) => {
  await sendEmail(job.data);
  console.log(`Email sent to ${job.data.to}`);
});

// Events
emailQueue.on('completed', job => console.log(`Job ${job.id} done`));
emailQueue.on('failed', (job, err) => console.error(`Job ${job.id} failed: ${err.message}`));
```

### 130. RabbitMQ

```javascript
const amqp = require('amqplib');

// Producer
const conn = await amqp.connect('amqp://localhost');
const channel = await conn.createChannel();
await channel.assertQueue('tasks', { durable: true });
channel.sendToQueue('tasks', Buffer.from(JSON.stringify({ type: 'email', to: 'user@mail.com' })));

// Consumer
channel.consume('tasks', (msg) => {
  const task = JSON.parse(msg.content.toString());
  processTask(task);
  channel.ack(msg); // acknowledge message
});
```

---

## Section 25: File Uploads & Handling

### 131. File Uploads with Multer

```javascript
const multer = require('multer');

// Memory storage (for small files)
const upload = multer({ storage: multer.memoryStorage() });

// Disk storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => cb(null, `${Date.now()}-${file.originalname}`)
});

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'image/webp'];
    if (allowed.includes(file.mimetype)) cb(null, true);
    else cb(new Error('Invalid file type'));
  }
});

// Single file
app.post('/upload', upload.single('avatar'), (req, res) => {
  res.json({ filename: req.file.filename });
});

// Multiple files
app.post('/uploads', upload.array('photos', 5), (req, res) => {
  res.json({ files: req.files.map(f => f.filename) });
});
```

### 132. Upload to AWS S3

```javascript
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: 'us-east-1' });

app.post('/upload', upload.single('file'), async (req, res) => {
  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: `uploads/${Date.now()}-${req.file.originalname}`,
    Body: req.file.buffer,
    ContentType: req.file.mimetype
  });

  await s3.send(command);
  res.json({ message: 'Uploaded to S3' });
});
```

---

## Section 26: Advanced Security in Node.js

### 133. CORS Configuration

```javascript
const cors = require('cors');

// Allow specific origins
app.use(cors({
  origin: ['https://myapp.com', 'https://admin.myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true, // allow cookies
  maxAge: 86400      // preflight cache: 24h
}));

// Dynamic origin validation
app.use(cors({
  origin: (origin, callback) => {
    const whitelist = ['https://myapp.com'];
    callback(null, whitelist.includes(origin) || !origin);
  }
}));
```

### 134. Input Validation with Joi

```javascript
const Joi = require('joi');

const userSchema = Joi.object({
  name: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(18).max(120),
  role: Joi.string().valid('user', 'admin').default('user')
});

const validateUser = (req, res, next) => {
  const { error, value } = userSchema.validate(req.body);
  if (error) return res.status(400).json({ error: error.details[0].message });
  req.validatedBody = value;
  next();
};

app.post('/users', validateUser, createUser);
```

### 135. Security Best Practices Checklist

- ✅ Validate and sanitize all user inputs
- ✅ Use parameterized queries (no string concatenation)
- ✅ Hash passwords with bcrypt (min 10 rounds)
- ✅ Use HTTPS everywhere
- ✅ Set secure cookie flags (HttpOnly, Secure, SameSite)
- ✅ Use Helmet.js for HTTP headers
- ✅ Implement rate limiting
- ✅ Never expose stack traces in production
- ✅ Store secrets in environment variables (never in code)
- ✅ Keep dependencies updated (`npm audit`)
- ✅ Use CSRF tokens for form submissions
- ✅ Limit payload size (`express.json({ limit: '10kb' })`)
- ✅ Disable X-Powered-By header (`app.disable('x-powered-by')`)

---

## Section 27: Authentication Deep Dive

### 136. Session-Based vs Token-Based Auth

| Feature | Session-Based | Token-Based (JWT) |
|---|---|---|
| State storage | Server (DB/Redis) | Client (token) |
| Scalability | Harder (sticky sessions) | Easier (stateless) |
| Revocation | Easy (delete session) | Hard (until expiry) |
| Best for | Traditional web apps | SPAs, mobile, APIs |

### 137. Complete JWT Authentication Flow

```javascript
const jwt = require('jsonwebtoken');

// Login — generate tokens
app.post('/auth/login', async (req, res) => {
  const user = await User.findOne({ email: req.body.email });
  if (!user || !await bcrypt.compare(req.body.password, user.password)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const accessToken = jwt.sign(
    { userId: user._id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );

  const refreshToken = jwt.sign(
    { userId: user._id },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  // Store refresh token in DB
  await User.findByIdAndUpdate(user._id, { refreshToken });

  res.cookie('refreshToken', refreshToken, { httpOnly: true, secure: true });
  res.json({ accessToken });
});

// Auth middleware — verify access token
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Refresh token route
app.post('/auth/refresh', async (req, res) => {
  const token = req.cookies.refreshToken;
  if (!token) return res.status(401).json({ error: 'No refresh token' });

  const decoded = jwt.verify(token, process.env.REFRESH_SECRET);
  const user = await User.findById(decoded.userId);

  if (!user || user.refreshToken !== token) {
    return res.status(401).json({ error: 'Invalid refresh token' });
  }

  const newAccessToken = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '15m' });
  res.json({ accessToken: newAccessToken });
});
```

---

## Section 28: GraphQL with Node.js

### 138. What is GraphQL?

A query language for APIs where clients request **exactly** the data they need. Reduces over-fetching and under-fetching.

### 139. Apollo Server Setup

```javascript
const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    author: User!
  }

  type Query {
    user(id: ID!): User
    users: [User!]!
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
  }
`;

const resolvers = {
  Query: {
    user: async (_, { id }) => await User.findById(id),
    users: async () => await User.find()
  },
  Mutation: {
    createUser: async (_, args) => await User.create(args)
  },
  User: {
    posts: async (user) => await Post.find({ authorId: user.id })
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({ user: req.user }) // pass auth context
});

server.listen(4000).then(({ url }) => console.log(`GraphQL ready at ${url}`));
```

---

## Section 29: Advanced Databases

### 140. Mongoose Middleware Hooks

```javascript
// Pre-save hook — hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

// Post-save hook
userSchema.post('save', function(doc, next) {
  console.log(`User ${doc.email} saved`);
  next();
});

// Pre-find hook — always exclude password
userSchema.pre(/^find/, function(next) {
  this.select('-password');
  next();
});
```

### 141. Query Optimization

```javascript
// Use lean() for read-only queries (returns plain JS objects, not Mongoose docs)
const users = await User.find().lean(); // much faster

// Use select() to limit fields
const users = await User.find().select('name email -_id');

// Use indexes
userSchema.index({ email: 1 });

// Use explain() to analyze queries
const explanation = await User.find({ email: 'test@mail.com' }).explain('executionStats');

// Avoid N+1 problem — use populate wisely
const posts = await Post.find().populate('author', 'name email');

// Or use aggregation for complex queries
const result = await Order.aggregate([
  { $match: { status: 'completed' } },
  { $group: { _id: '$userId', total: { $sum: '$amount' } } },
  { $sort: { total: -1 } }
]);
```

---

## Section 30: Microservices Architecture

### 142. Monolith vs Microservices

| Aspect | Monolith | Microservices |
|---|---|---|
| Deployment | Single unit | Independent services |
| Scaling | Scale all or nothing | Scale individual services |
| Development | Simpler initially | Complex coordination |
| Database | Shared | Separate per service |
| Failure | One bug can affect all | Isolated failures |
| Tech stack | Uniform | Polyglot possible |

### 143. Microservice Communication Patterns

```javascript
// Synchronous — REST/gRPC (tight coupling)
const axios = require('axios');
const user = await axios.get(`http://user-service:3001/users/${id}`);

// Asynchronous — Message broker (loose coupling)
// Producer
channel.sendToQueue('user.created', Buffer.from(JSON.stringify(user)));

// Consumer
channel.consume('user.created', (msg) => {
  const user = JSON.parse(msg.content.toString());
  createUserProfile(user);
  channel.ack(msg);
});
```

### 144. API Gateway Pattern

```
Client → API Gateway → [User Service]
                     → [Product Service]
                     → [Order Service]
                     → [Payment Service]
```

Responsibilities:
- Authentication / Authorization
- Rate limiting
- Load balancing
- Request routing
- Response aggregation
- SSL termination

---

## Section 31: Performance Optimization Deep Dive

### 145. PM2 Cluster Mode

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api',
    script: 'index.js',
    instances: 'max',       // one per CPU
    exec_mode: 'cluster',
    watch: false,
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    max_memory_restart: '500M',
    log_file: './logs/combined.log',
    error_file: './logs/error.log'
  }]
};
```

```bash
pm2 start ecosystem.config.js --env production
pm2 monit        # real-time monitoring
pm2 logs         # view logs
pm2 reload all   # zero-downtime reload
```

### 146. Redis Caching Pattern

```javascript
const redis = require('redis');
const client = await redis.createClient().connect();

async function getUser(id) {
  const cacheKey = `user:${id}`;

  // Check cache first
  const cached = await client.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Miss — fetch from DB
  const user = await User.findById(id).lean();
  if (!user) return null;

  // Store in cache for 1 hour
  await client.setEx(cacheKey, 3600, JSON.stringify(user));
  return user;
}

// Invalidate cache on update
async function updateUser(id, data) {
  const user = await User.findByIdAndUpdate(id, data, { new: true });
  await client.del(`user:${id}`); // invalidate
  return user;
}
```

---

## Section 32: Node.js with TypeScript

### 147. Why TypeScript with Node.js?

- **Static typing** — catch errors at compile time
- **Better IDE support** — autocompletion, refactoring
- **Self-documenting** — types serve as documentation
- **Safer refactoring** — type errors surface immediately

### 148. Express with TypeScript

```typescript
import express, { Request, Response, NextFunction } from 'express';

interface User {
  id: number;
  name: string;
  email: string;
}

interface AuthRequest extends Request {
  user?: User;
}

const app = express();

app.get('/users/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user: User | null = await getUserById(parseInt(req.params.id));
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json(user);
  } catch (err) {
    next(err);
  }
});
```

### 149. tsconfig.json for Node.js

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

```bash
npm install -D typescript ts-node @types/node @types/express
npx tsc          # compile
ts-node src/app.ts # direct execution
```

---

## Section 33: Testing & CI/CD

### 150. Testing Structure (Jest + Supertest)

```javascript
// tests/user.test.js
const request = require('supertest');
const mongoose = require('mongoose');
const app = require('../app');

beforeAll(async () => {
  await mongoose.connect(process.env.TEST_DB_URL);
});

afterAll(async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.connection.close();
});

afterEach(async () => {
  await User.deleteMany({});
});

describe('POST /api/users', () => {
  it('creates a user', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@test.com', password: 'pass123' })
      .expect(201);

    expect(res.body).toHaveProperty('id');
    expect(res.body.email).toBe('alice@test.com');
    expect(res.body).not.toHaveProperty('password'); // never expose password
  });
});
```

### 151. GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mongodb:
        image: mongo:6
        ports: ['27017:27017']

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci
      - run: npm test
        env:
          TEST_DB_URL: mongodb://localhost:27017/testdb

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Deploy to production"
```

---

## Section 34: Monitoring & Observability

### 152. Health Check Endpoint

```javascript
app.get('/health', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: process.env.npm_package_version
  };

  try {
    await mongoose.connection.db.admin().ping();
    health.db = 'connected';
  } catch {
    health.status = 'degraded';
    health.db = 'disconnected';
  }

  res.status(health.status === 'ok' ? 200 : 503).json(health);
});
```

### 153. Winston Logging

```javascript
const { createLogger, format, transports } = require('winston');

const logger = createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: format.combine(
    format.timestamp(),
    format.errors({ stack: true }),
    format.json()
  ),
  transports: [
    new transports.Console({
      format: format.combine(format.colorize(), format.simple())
    }),
    new transports.File({ filename: 'logs/error.log', level: 'error' }),
    new transports.File({ filename: 'logs/combined.log' })
  ]
});

// Use in code
logger.info('Server started', { port: 3000 });
logger.error('DB connection failed', { error: err.message });
logger.warn('Rate limit exceeded', { ip: req.ip });

module.exports = logger;
```

### 154. Morgan HTTP Logging

```javascript
const morgan = require('morgan');

// Development
app.use(morgan('dev'));

// Production (structured)
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));
```

---

## Section 35: Docker & Deployment

### 155. Production Dockerfile

```dockerfile
# Multi-stage build for smaller image
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER appuser
EXPOSE 3000
CMD ["node", "index.js"]
```

### 156. docker-compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DB_URL=mongodb://mongo:27017/mydb
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - mongo
      - redis
    command: npm run dev

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  mongo_data:
```

```bash
docker-compose up -d       # start all services
docker-compose logs -f app # follow app logs
docker-compose down        # stop all
```

---

## Section 36: Node.js 20+ Features

### 157. Built-in Test Runner

```javascript
// test.mjs
import { test, describe, it, before, after } from 'node:test';
import assert from 'node:assert';

describe('Math', () => {
  it('adds numbers', () => {
    assert.strictEqual(1 + 2, 3);
  });

  it('async test', async () => {
    const result = await Promise.resolve(42);
    assert.strictEqual(result, 42);
  });
});
```

```bash
node --test          # run all test files
node --test --watch  # watch mode
```

### 158. Global fetch() API (Node 18+)

```javascript
// No need for node-fetch anymore
const res = await fetch('https://api.example.com/users');
const users = await res.json();
```

### 159. Web Streams API

```javascript
const { ReadableStream, WritableStream, TransformStream } = require('node:stream/web');

const readable = new ReadableStream({
  start(controller) {
    controller.enqueue('Hello');
    controller.enqueue(' World');
    controller.close();
  }
});
```

### 160. Permission Model (Experimental)

```bash
# Restrict file system access
node --experimental-permission --allow-fs-read=./data --allow-fs-write=./out app.js

# Restrict network access
node --experimental-permission --allow-net=api.example.com app.js
```

### 161. ESM Loader Hooks

```javascript
// hooks.mjs
export async function resolve(specifier, context, nextResolve) {
  // custom resolution logic
  return nextResolve(specifier, context);
}

export async function load(url, context, nextLoad) {
  // custom loading/transformation
  return nextLoad(url, context);
}
```

```bash
node --experimental-loader ./hooks.mjs app.js
```

---

## Miscellaneous — Important Concepts

### M1. `__dirname` vs `process.cwd()`

| | `__dirname` | `process.cwd()` |
|---|---|---|
| What it is | Directory of the current **file** | Directory where Node was **started** |
| Constant? | Yes (always the file's dir) | No (can change with `process.chdir()`) |
| ESM equivalent | Use `import.meta.url` | Same `process.cwd()` |

```javascript
const path = require('path');

// Reliable file path (won't break if run from another dir)
const configPath = path.join(__dirname, 'config.json');

// ESM equivalent
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
```

### M2. Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH
  |      |     |
  |      |     └─ Bug fixes (backward compatible)
  |      └─────── New features (backward compatible)
  └────────────── Breaking changes
```

In `package.json`:
- `"^4.18.2"` — accepts `4.x.x` (same major)
- `"~4.18.2"` — accepts `4.18.x` (same minor)
- `"4.18.2"` — exact version only

### M3. `dependencies` vs `devDependencies` vs `peerDependencies`

| Type | Installed in | Purpose |
|---|---|---|
| `dependencies` | `npm install` | Runtime packages (express, mongoose) |
| `devDependencies` | `npm install` (not in production) | Dev tools (jest, nodemon, eslint) |
| `peerDependencies` | Must be installed by consumer | Plugin expects host package (e.g., React plugin) |
| `optionalDependencies` | Optional | Won't fail if install fails |

### M4. Tree Shaking

Removes unused code from JavaScript bundles (Webpack, Rollup). Only works with **ES Modules** (`import/export`), not CommonJS.

```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;

// app.js — only imports add
import { add } from './math.js';
// subtract is "tree-shaken" out of the bundle
```

### M5. ESM vs CommonJS

| Feature | CommonJS (CJS) | ES Modules (ESM) |
|---|---|---|
| Syntax | `require()` / `module.exports` | `import` / `export` |
| Loading | Synchronous | Asynchronous |
| File extension | `.js`, `.cjs` | `.mjs` or `.js` with `"type": "module"` |
| Tree shaking | ❌ | ✅ |
| Top-level await | ❌ | ✅ |

### M6. Graceful Shutdown

```javascript
const server = app.listen(3000);

const shutdown = async (signal) => {
  console.log(`${signal} received. Shutting down gracefully...`);

  // Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');

    // Close DB connection
    await mongoose.connection.close();
    console.log('MongoDB disconnected');

    process.exit(0);
  });

  // Force exit after 10 seconds
  setTimeout(() => {
    console.error('Forced shutdown');
    process.exit(1);
  }, 10000);
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```

### M7. Loading Config for Different Environments

```javascript
// config/index.js
require('dotenv').config({ path: `.env.${process.env.NODE_ENV}` });

module.exports = {
  port: process.env.PORT || 3000,
  dbUrl: process.env.DB_URL,
  jwtSecret: process.env.JWT_SECRET,
  nodeEnv: process.env.NODE_ENV || 'development',
  isProduction: process.env.NODE_ENV === 'production'
};
```

```bash
NODE_ENV=production node app.js
NODE_ENV=test jest
```

### M8. require() JSON Files

```javascript
const config = require('./config.json');
// Automatically parsed — returns a JavaScript object
console.log(config.database.host);
```

### M9. Process Object

```javascript
process.pid                // Process ID
process.version            // Node.js version
process.platform           // 'linux', 'darwin', 'win32'
process.argv               // Command-line arguments ['node', 'app.js', '--port', '3000']
process.env                // Environment variables
process.cwd()              // Current working directory
process.uptime()           // Process uptime in seconds
process.memoryUsage()      // { rss, heapTotal, heapUsed, external }
process.cpuUsage()         // { user, system } in microseconds
process.exit(0)            // Exit with code 0 (success)
process.exit(1)            // Exit with code 1 (failure)
process.stdout.write()     // Write to stdout
process.stderr.write()     // Write to stderr
process.nextTick(fn)       // Schedule microtask
process.hrtime.bigint()    // High-resolution time in nanoseconds
```

### M10. REPL (Read-Eval-Print Loop)

```bash
node           # start interactive REPL
.help          # list REPL commands
.exit          # exit
.load file.js  # load a file into REPL
.save file.js  # save REPL session to file
_              # last evaluated expression
```

### M11. Scheduling Jobs with node-cron

```javascript
const cron = require('node-cron');

// Run every minute
cron.schedule('* * * * *', () => console.log('Running every minute'));

// Run at 2:30 AM every day
cron.schedule('30 2 * * *', async () => {
  await cleanupOldLogs();
  console.log('Daily cleanup done');
});

// Cron syntax: second(optional) minute hour day month weekday
// Example:   '0 0 * * 1' = every Monday at midnight
```

### M12. Sending Emails with Nodemailer

```javascript
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
});

await transporter.sendMail({
  from: `"My App" <${process.env.EMAIL_USER}>`,
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Thanks for signing up</h1>'
});
```

### M13. URL and Query String Parsing

```javascript
const { URL, URLSearchParams } = require('url');

const url = new URL('https://api.example.com/users?page=2&limit=10&sort=name');
url.hostname;            // 'api.example.com'
url.pathname;            // '/users'
url.search;              // '?page=2&limit=10&sort=name'
url.searchParams.get('page');  // '2'
url.searchParams.getAll('sort'); // ['name']
url.searchParams.has('limit'); // true

// Build query strings
const params = new URLSearchParams({ page: 2, limit: 10 });
params.toString(); // 'page=2&limit=10'
```

### M14. Useful npm Commands

```bash
npm init -y                    # create package.json with defaults
npm install <pkg>              # install and add to dependencies
npm install -D <pkg>           # install as devDependency
npm install -g <pkg>           # global install
npm uninstall <pkg>            # remove package
npm update                     # update all packages
npm outdated                   # list outdated packages
npm audit                      # check for vulnerabilities
npm audit fix                  # auto-fix vulnerabilities
npm list --depth=0             # list installed packages
npm run <script>               # run script from package.json
npm publish                    # publish to npm registry
npx <pkg>                      # run package without installing
```

### M15. Common Node.js Project Structure

```
project/
├── src/
│   ├── config/           ← app config, db config
│   ├── controllers/      ← request handlers
│   ├── services/         ← business logic
│   ├── models/           ← database models
│   ├── routes/           ← route definitions
│   ├── middleware/       ← auth, validation, logging
│   ├── utils/            ← helper functions
│   └── app.js            ← express app setup
├── tests/
│   ├── unit/
│   └── integration/
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── package.json
└── README.md
```

### M16. How `require()` Resolution Works

When you call `require('module')`, Node.js searches in this order:

1. **Core modules** (`fs`, `path`, etc.) — returned immediately
2. **Relative path** (`./file`, `../dir`) — resolved directly
3. **node_modules** — searches upward from current directory
4. **NODE_PATH** — environment variable (legacy)

Module caching: once loaded, the same module object is returned on subsequent `require()` calls (no re-execution).

```javascript
// Force re-load (clear cache)
delete require.cache[require.resolve('./module')];
const fresh = require('./module');
```

### M17. Promisifying Callback APIs

```javascript
const { promisify } = require('util');
const fs = require('fs');

// Promisify a callback function
const readFileAsync = promisify(fs.readFile);
const data = await readFileAsync('file.txt', 'utf8');

// Or use fs.promises directly
const { readFile } = require('fs').promises;
const data = await readFile('file.txt', 'utf8');
```

### M18. Readable Stream from String/Array

```javascript
const { Readable } = require('stream');

// Create readable stream from string
const readable = Readable.from(['Hello', ' ', 'World']);
readable.pipe(process.stdout); // Hello World

// Create readable stream programmatically
const stream = new Readable({
  read() {
    this.push('chunk1');
    this.push('chunk2');
    this.push(null); // signal end
  }
});
```

### M19. HTTPS Server

```javascript
const https = require('https');
const fs = require('fs');
const express = require('express');
const app = express();

const options = {
  key: fs.readFileSync('./ssl/private.key'),
  cert: fs.readFileSync('./ssl/certificate.crt')
};

https.createServer(options, app).listen(443, () => {
  console.log('HTTPS server running on port 443');
});
```

### M20. Quick Reference — Event Loop Order

```javascript
// Execution order:
// 1. Synchronous code
// 2. process.nextTick callbacks
// 3. Promise microtasks (.then, .catch)
// 4. setImmediate / I/O callbacks
// 5. setTimeout / setInterval

console.log('1 - sync');

setTimeout(() => console.log('5 - setTimeout'), 0);
setImmediate(() => console.log('4b - setImmediate'));

Promise.resolve().then(() => console.log('3 - promise'));
process.nextTick(() => console.log('2 - nextTick'));

fs.readFile(__filename, () => {
  setTimeout(() => console.log('7 - setTimeout inside I/O'), 0);
  setImmediate(() => console.log('6 - setImmediate inside I/O')); // guaranteed before setTimeout
  console.log('4a - I/O callback');
});

console.log('1b - sync');
```

> Inside an I/O callback, `setImmediate` is **always guaranteed** to run before `setTimeout`.

---

*These notes cover Sections 1–36 of Node.js fundamentals through advanced topics, plus the Miscellaneous section. Last updated March 2026.*




# 🧠 Node.js — Complete Interview Preparation Notes
> **150+ Questions | All Topics | Code Examples | Cheat Sheets**
> Master these 4 topics → Clear 70% of interviews: **Event Loop | Async | Middleware | Indexing**

---

## 📚 Table of Contents

1. [Node.js Basics](#section-1-nodejs-basics)
2. [Event Loop ★★★](#section-2-event-loop)
3. [Async Programming ★★★](#section-3-async-programming)
4. [Core Modules](#section-4-core-modules)
5. [Streams & Buffers](#section-5-streams--buffers)
6. [libuv, Child Process, Cluster & Worker Threads](#section-6-libuv-child-process-cluster--worker-threads)
7. [Express.js & Middleware ★★★](#section-7-expressjs--middleware)
8. [Databases, MongoDB & Indexing ★★★](#section-8-databases-mongodb--indexing)
9. [Security & Authentication](#section-9-security--authentication)
10. [API Design & REST](#section-10-api-design--rest)
11. [Error Handling, Testing & Debugging](#section-11-error-handling-testing--debugging)
12. [Performance, Scaling & Deployment](#section-12-performance-scaling--deployment)
13. [Real-Time, Message Queues & Microservices](#section-13-real-time-message-queues--microservices)
14. [System Design & Advanced Scenarios](#section-14-system-design--advanced-scenarios)
15. [Quick Reference Cheat Sheets](#quick-reference-cheat-sheets)

---

## Section 1: Node.js Basics

### Q1. What is Node.js?

Node.js is an open-source, cross-platform **runtime environment** that executes JavaScript on the server side. Built on Google Chrome's **V8 JavaScript engine**.

- **Runtime** — Not a language or framework. It runs JS outside the browser.
- **V8 Engine** — Compiles JS directly to native machine code. Extremely fast.
- **Event-driven** — Non-blocking I/O + event loop. Handles thousands of concurrent connections with minimal resources.
- **Use cases** — REST APIs, real-time apps (chat, games), streaming, microservices, CLI tools.

> 📌 **Memory Trick:** `Node = V8 (JS execution) + libuv (async I/O) + C++ bindings (OS calls)`

---

### Q2. What makes Node.js fast?

- **V8 JIT Compilation** — JS compiled to native machine code at runtime, not interpreted line by line.
- **Non-blocking I/O** — Instead of waiting for file/DB/network ops, Node registers a callback and moves on.
- **Single-threaded event loop** — No overhead from thread context switching.
- **libuv thread pool** — Heavy tasks (file I/O, crypto) run in background threads. Main JS thread stays free.

---

### Q3. Is Node.js single-threaded?

**Yes and No.**

- JS execution → **single-threaded**
- Network I/O → handled by **OS kernel** (no extra threads)
- File I/O / Crypto → **libuv thread pool** (4 threads by default)
- Heavy CPU work → **Worker Threads** (you create them manually)

---

### Q4. Node.js vs Browser JavaScript

| Feature | Node.js | Browser JS |
|---|---|---|
| Runs on | Server (V8 + libuv) | Browser (V8 / SpiderMonkey) |
| Access to | File system, OS, network | DOM, BOM, window |
| Module system | CommonJS (require) + ESM | ES Modules (import) |
| Global object | `global`, `process` | `window`, `document` |
| Built-in APIs | fs, http, path, os, crypto | fetch, localStorage, navigator |

---

### Q5. package.json vs package-lock.json

| File | Purpose |
|---|---|
| `package.json` | Metadata: name, version, scripts, dependencies (version ranges like `^1.2.0`) |
| `package-lock.json` | Locks **EXACT** versions of every nested dependency — ensures identical installs across machines |

> **Tip:** Always commit `package-lock.json`. Run `npm ci` (not `npm install`) in CI/CD for reproducible builds.

---

### Q6. Modules — require() vs import

| Feature | CommonJS (require) | ES Modules (import) |
|---|---|---|
| Syntax | `const x = require('x')` | `import x from 'x'` |
| Loading | Synchronous | Asynchronous |
| Exports | `module.exports = {...}` | `export default / export const` |
| File extension | `.js` (default in Node) | Need `.mjs` or `"type":"module"` in package.json |
| When to use | Older Node projects | Modern projects, TypeScript |

**Module types:**
- **Built-in** — `fs`, `http`, `path`, `os`, `events`, `crypto` — no npm install needed
- **Local** — Your own files: `const helper = require('./helper.js')`
- **Third-party** — npm packages: `express`, `mongoose`, `axios`

---

### Q7. Semantic Versioning (SemVer)

Format: **MAJOR.MINOR.PATCH** e.g. `2.4.1`

- **MAJOR (2)** — Breaking changes. Existing code may break.
- **MINOR (4)** — New features, backward compatible.
- **PATCH (1)** — Bug fixes only.
- **^ (caret)** — `^1.2.0` = accept any `1.x.x`
- **~ (tilde)** — `~1.2.0` = accept only `1.2.x`

---

## Section 2: Event Loop ★★★

> ⚡ **MOST IMPORTANT — Appears in 90% of Node.js interviews**

### Q8. What is the Event Loop?

The Event Loop is the mechanism that allows Node.js to perform **non-blocking operations** despite JavaScript being single-threaded. It continuously checks if the call stack is empty, then picks the next callback from the appropriate queue.

**How it works:**
1. Your JS code runs synchronously on the call stack.
2. When an async operation (`setTimeout`, `fs.readFile`) is encountered, it is handed off to libuv / OS.
3. Node continues executing the rest of the synchronous code without waiting.
4. When the async operation completes, its callback goes into the appropriate queue.
5. When the call stack is empty, the event loop picks the next callback and runs it.

---

### Q8a. The 6 Phases of the Event Loop — Memorise This!

| Phase | Name | What Executes |
|---|---|---|
| 1 | **Timers** | `setTimeout()` and `setInterval()` callbacks whose delay has expired |
| 2 | **Pending Callbacks** | I/O callbacks deferred from previous loop iteration |
| 3 | **Idle / Prepare** | Internal Node.js use only |
| 4 | **Poll** | Retrieves new I/O events. Executes I/O callbacks. Most code runs here |
| 5 | **Check** | `setImmediate()` callbacks execute here |
| 6 | **Close Callbacks** | Cleanup: `socket.on('close')`, `server.on('close')` |

---

### Q9. Microtasks vs Macrotasks ★★★

| Priority | Queue Type | Contents | When It Runs |
|---|---|---|---|
| 1st (highest) | Microtask | `process.nextTick()` | Before everything else — even before Promise |
| 2nd | Microtask | `Promise.then() / .catch()` | After nextTick, before next loop phase |
| 3rd | Macrotask (Timers) | `setTimeout()`, `setInterval()` | Phase 1 of event loop |
| 4th | Macrotask (Check) | `setImmediate()` | Phase 5 of event loop |
| 5th | Macrotask (Poll) | I/O callbacks | Phase 4 of event loop |

---

### Q9a. Classic Interview Question — Predict the Output

```js
console.log('A');

setTimeout(() => console.log('B - setTimeout'), 0);
setImmediate(() => console.log('C - setImmediate'));
Promise.resolve().then(() => console.log('D - Promise'));
process.nextTick(() => console.log('E - nextTick'));

console.log('F');

// ─── OUTPUT ───────────────────────────────────────
// A   ← synchronous
// F   ← synchronous
// E   ← microtask: nextTick runs first
// D   ← microtask: Promise.then
// B   ← macrotask: setTimeout (timers phase)
// C   ← macrotask: setImmediate (check phase)
//
// NOTE: Inside an I/O callback → C always runs before B
```

> ⚠️ **Warning:** Never call `process.nextTick()` recursively — it will **starve the event loop** and prevent all I/O callbacks from running.

---

### Q10. process.nextTick() vs setImmediate()

| Feature | `process.nextTick()` | `setImmediate()` |
|---|---|---|
| Queue type | Microtask queue | Macrotask queue (check phase) |
| When runs | Before next event loop phase | After current I/O events (phase 5) |
| Priority | Highest of all async | Lower than nextTick and Promises |
| Use case | Ensure async behaviour, emit events after setup | Execute after I/O completes |
| Risk | Can starve event loop if recursive | Safe — allows loop to continue |

---

### Q11. What happens when the Event Loop is blocked?

When you run CPU-heavy synchronous code (complex loop, `JSON.parse` on huge payload), the event loop **cannot process any other callbacks**. The entire app freezes.

**Solutions:**
- **Worker Threads** — for CPU-heavy JS (crypto, ML, image processing)
- **Child Processes** — run work in a separate process (`spawn`, `fork`)
- **Break work into chunks** — use `setImmediate()` between chunks

```js
// ❌ BLOCKS event loop — no requests handled during this
for (let i = 0; i < 10_000_000_000; i++) { /* CPU maxed */ }

// ✅ Worker Thread — CPU work without blocking main thread
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
  const worker = new Worker(__filename);
  worker.on('message', result => console.log('Result:', result));
} else {
  let sum = 0;
  for (let i = 0; i < 10_000_000_000; i++) sum += i;
  parentPort.postMessage(sum);
}
```

---

## Section 3: Async Programming ★★★

### Q12. Callbacks and Callback Hell

A **callback** is a function passed as an argument, invoked when the async operation completes.

```js
// Simple callback — fine for one level
fs.readFile('data.txt', 'utf8', (err, data) => {
  if (err) return console.error(err);
  console.log(data);
});

// ❌ CALLBACK HELL — unreadable, unmanageable
getUser(id, (err, user) => {
  getOrders(user.id, (err, orders) => {
    getDetails(orders[0].id, (err, details) => {
      getPrice(details.productId, (err, price) => {
        // 4 levels deep — impossible to maintain!
      });
    });
  });
});
```

> **Fix callback hell with:** Promises (flatten the chain) or `async/await` (reads like sync code)

---

### Q13. Promises — 3 States ★★★

A **Promise** represents the eventual completion or failure of an async operation.

| State | Meaning | What happens |
|---|---|---|
| **Pending** | Operation in progress | Neither fulfilled nor rejected yet |
| **Fulfilled** | Operation succeeded | `.then(value => ...)` is called |
| **Rejected** | Operation failed | `.catch(err => ...)` is called |

```js
// Creating a Promise
function fetchUser(id) {
  return new Promise((resolve, reject) => {
    db.find(id, (err, user) => {
      if (err) reject(new Error('DB error: ' + err.message));
      else     resolve(user);
    });
  });
}

// Consuming — clean chain, no nesting
fetchUser(1)
  .then(user   => getOrders(user.id))
  .then(orders => processOrders(orders))
  .catch(err   => console.error(err))   // catches ANY error above
  .finally(()  => db.close());          // always runs
```

---

### Q14. async/await ★★★

`async/await` is **syntactic sugar built on top of Promises**. Makes async code look and read like synchronous code.

```js
async function getUserData(userId) {
  try {
    // await pauses THIS function only — not the whole thread!
    const user   = await fetchUser(userId);
    const orders = await getOrders(user.id);  // sequential (depends on user)
    return orders;
  } catch (err) {
    // Catches errors from ANY awaited Promise above
    console.error('Failed:', err.message);
    throw err;  // re-throw so caller knows it failed
  } finally {
    closeConnection();  // always runs
  }
}
```

| Feature | Promises (.then) | async/await |
|---|---|---|
| Readability | Chained .then() calls | Linear, reads like sync code |
| Error handling | .catch() at chain end | try/catch — familiar |
| Debugging | Stack traces can be unclear | Clear stack traces with line numbers |
| Parallel tasks | `Promise.all([...])` | `await Promise.all([...])` |

---

### Q15. Promise.all() vs Promise.race() vs Promise.allSettled() ★★★

| Method | Resolves When | Rejects When | Best Use Case |
|---|---|---|---|
| `Promise.all()` | ALL fulfill | ANY one rejects (fail-fast) | Parallel independent tasks — all must succeed |
| `Promise.race()` | FIRST one settles | FIRST one rejects | Timeout pattern, first-response wins |
| `Promise.allSettled()` | ALL settle (any result) | Never rejects | Run all, collect all outcomes regardless of failure |
| `Promise.any()` | FIRST one fulfills | ALL reject | Race to first success, ignore failures |

```js
// ✅ Parallel fetch — 3x faster than sequential
const [users, products, orders] = await Promise.all([
  db.getUsers(),
  db.getProducts(),
  db.getOrders()
]);

// ✅ Timeout pattern
const result = await Promise.race([
  fetch('/api/data'),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout after 5s')), 5000))
]);

// ✅ Run all, collect results (even failures)
const results = await Promise.allSettled([task1(), task2(), task3()]);
results.forEach(r => {
  if (r.status === 'fulfilled') console.log('OK:', r.value);
  else                          console.log('FAIL:', r.reason);
});
```

> **Performance Rule:** Never use sequential awaits for **independent** async operations. Always use `Promise.all()` — runs them in parallel.

---

### Q16. How to measure async execution time

```js
// Method 1: console.time (quick and easy)
console.time('dbQuery');
const users = await User.find({});
console.timeEnd('dbQuery');  // "dbQuery: 47.231ms"

// Method 2: performance.now() — precise
const { performance } = require('perf_hooks');
const t0 = performance.now();
await expensiveOperation();
console.log(`Took ${(performance.now() - t0).toFixed(2)}ms`);

// Method 3: Monitor event loop lag (detect blocking)
const { monitorEventLoopDelay } = require('perf_hooks');
const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();
setInterval(() => {
  console.log('EL delay mean:', (h.mean / 1e6).toFixed(2), 'ms');
}, 5000);
```

---

## Section 4: Core Modules

### Q17. Important Core Modules

| Module | Purpose | Key Methods |
|---|---|---|
| `fs` | File system operations | readFile, writeFile, createReadStream, watch |
| `path` | File path manipulation | join, resolve, basename, dirname, extname |
| `os` | Operating system info | platform, cpus, freemem, totalmem, homedir |
| `http / https` | Create HTTP servers | createServer, request |
| `events` | EventEmitter pattern | on, emit, once, removeListener |
| `url` | Parse / format URLs | new URL(), URLSearchParams |
| `crypto` | Hashing, encryption | createHash, randomBytes, pbkdf2 |
| `stream` | Streaming data | Readable, Writable, Transform, pipeline |
| `child_process` | Spawn processes | spawn, exec, fork |
| `cluster` | Multi-core scaling | fork, isMaster, isWorker |
| `worker_threads` | CPU parallelism | Worker, parentPort, workerData |
| `util` | Utility helpers | promisify, inspect, format |

---

### Q18. fs module — sync vs async

```js
const fs  = require('fs');
const fsp = require('fs/promises');  // Promise-based (Node 14+)

// ❌ Sync — BLOCKS event loop
const data = fs.readFileSync('config.json', 'utf8');

// ✅ Async callback — non-blocking
fs.readFile('config.json', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(JSON.parse(data));
});

// ✅ Promise-based (best for modern code)
const content = await fsp.readFile('config.json', 'utf8');
await fsp.writeFile('output.json', JSON.stringify(data, null, 2));
await fsp.appendFile('log.txt', 'New log entry\n');

// Watch for changes
fs.watch('config.json', (event, filename) => {
  console.log(`File ${filename} changed: ${event}`);
});
```

---

### Q19. EventEmitter

`EventEmitter` is the core of Node's event-driven architecture. Most built-in modules (`fs`, `http`, `net`, `stream`) extend it.

```js
const EventEmitter = require('events');

class UserService extends EventEmitter {
  createUser(data) {
    const user = { id: 1, ...data };
    this.emit('userCreated', user);  // emit with data
    return user;
  }
}

const svc = new UserService();

svc.on('userCreated', (user) => {     // runs every time
  sendWelcomeEmail(user.email);
});

svc.once('userCreated', (user) => {  // runs ONCE only
  console.log('First user:', user.id);
});

// ALWAYS handle 'error' event — unhandled error crashes process!
svc.on('error', (err) => console.error('Service error:', err));

// Clean up to prevent memory leaks
const handler = (user) => console.log(user);
svc.on('userCreated', handler);
svc.off('userCreated', handler);  // remove when done
```

> ⚠️ **Always handle the `error` event on EventEmitter instances.** An unhandled `error` event throws and crashes the process.

---

## Section 5: Streams & Buffers

### Q20. What are Streams?

Streams process data **chunk by chunk** instead of loading it all into memory at once.

| Without Streams | With Streams |
|---|---|
| Load entire 2GB file into RAM | Process in small chunks (64KB each) |
| App may crash (out of memory) | Works with any file size |
| Slow — waits for full read | Starts processing immediately |

| Stream Type | Direction | Real Examples |
|---|---|---|
| **Readable** | Source — you read FROM it | `fs.createReadStream`, HTTP request |
| **Writable** | Destination — you write TO it | `fs.createWriteStream`, HTTP response |
| **Duplex** | Both read and write simultaneously | `net.Socket`, TCP connections |
| **Transform** | Read, modify, then write | `zlib` (gzip/gunzip), crypto cipher |

```js
const fs   = require('fs');
const zlib = require('zlib');

// ✅ Stream a large file and gzip it — no RAM spike
fs.createReadStream('large-video.mp4')
  .pipe(zlib.createGzip())
  .pipe(fs.createWriteStream('large-video.mp4.gz'))
  .on('finish', () => console.log('Done!'));

// ✅ Modern: stream.pipeline (handles errors + cleanup automatically)
const { pipeline } = require('stream/promises');
await pipeline(
  fs.createReadStream('input.csv'),
  csvParser(),
  fs.createWriteStream('output.json')
);
```

> 📌 **Backpressure:** When the writable stream cannot consume data as fast as the readable produces it. `pipe()` and `pipeline()` handle this automatically by pausing the source.

---

### Q21. What is a Buffer?

A **Buffer** is a fixed-size raw memory allocation **outside V8's heap**. Stores binary data as bytes.

```js
const buf1 = Buffer.from('Hello Node.js', 'utf8');
console.log(buf1);              // <Buffer 48 65 6c 6c 6f ...>
console.log(buf1.toString());   // "Hello Node.js"
console.log(buf1.length);       // 13

const buf2 = Buffer.alloc(10);  // 10 zero bytes

// Convert image to base64 (common for APIs)
const img    = fs.readFileSync('photo.jpg');
const base64 = img.toString('base64');
```

---

## Section 6: libuv, Child Process, Cluster & Worker Threads

### Q22. What is libuv?

libuv is a **C library** that gives Node.js cross-platform async I/O capabilities.

| libuv Feature | What it does |
|---|---|
| **Event Loop** | Manages all async operations. Picks callbacks from queues when call stack is empty. |
| **Thread Pool** (default 4) | Handles blocking ops: file I/O, DNS, crypto, compression |
| **Cross-platform** | Same API on Windows (IOCP), Linux (epoll), macOS (kqueue) |
| **Network I/O** | TCP/UDP via OS kernel directly — no thread pool needed |

> **Tip:** Change thread pool size: `UV_THREADPOOL_SIZE=16 node app.js`

---

### Q23. Child Process vs Cluster vs Worker Threads

| Option | What it creates | Best For |
|---|---|---|
| `child_process.exec/spawn` | New OS process | Run shell commands, scripts |
| `child_process.fork` | New Node.js process | CPU-heavy tasks as separate Node app |
| `cluster` | Multiple Node workers on same port | Scale HTTP server across CPU cores |
| `Worker Threads` | JS thread inside same process | CPU work while sharing memory |

```js
// ── CLUSTER — Scale HTTP server across all CPU cores
const cluster = require('cluster');
const os      = require('os');

if (cluster.isPrimary) {
  const cores = os.cpus().length;
  for (let i = 0; i < cores; i++) cluster.fork();
  cluster.on('exit', (worker) => cluster.fork()); // auto-restart
} else {
  require('./app').listen(3000);
}

// ── WORKER THREAD — CPU work without blocking main thread
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

if (isMainThread) {
  const w = new Worker(__filename, { workerData: { n: 40 } });
  w.on('message', result => console.log('Fibonacci:', result));
} else {
  function fib(n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
  parentPort.postMessage(fib(workerData.n));
}
```

---

## Section 7: Express.js & Middleware ★★★

### Q24. What is Express.js?

Express.js is a **minimal, unopinionated web framework** for Node.js. Wraps Node's `http` module and adds routing, middleware, and a clean API.

- **Routing** — `app.get('/users', handler)`
- **Middleware pipeline** — Process requests through sequential functions
- **Error handling** — Centralized error middleware
- **Ecosystem** — `cors`, `helmet`, `multer`, `passport`, etc.

---

### Q25. Middleware — How Request Flow Works ★★★

Middleware is any function with the signature `(req, res, next)`. Express processes every request through a chain of middleware in the order they are defined.

> **Request Flow:** `Client → middleware 1 → middleware 2 → route handler → response`

```js
const express = require('express');
const app = express();

// APPLICATION-LEVEL — runs for every request
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();  // MUST call next() or request hangs forever
});

// BUILT-IN MIDDLEWARE
app.use(express.json());           // parse JSON request bodies
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public')); // serve static files

// THIRD-PARTY MIDDLEWARE
app.use(require('cors')({ origin: 'https://myapp.com' }));
app.use(require('helmet')());

// ROUTE-LEVEL — only for specific routes
app.get('/dashboard', authenticate, authorize('admin'), (req, res) => {
  res.json({ data: 'secret' });
});

// ERROR HANDLER — 4 params, always LAST
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({ message: err.message });
});
```

| Middleware Type | How Applied | Common Examples |
|---|---|---|
| Application-level | `app.use()` — every request | Logging, body parsing, cors, helmet |
| Router-level | `router.use()` — scoped routes | Admin route auth checks |
| Built-in | `express.json()`, `express.static()` | Parse body, serve static files |
| Third-party | npm install then `app.use()` | morgan, multer, passport, compression |
| Error-handling | `(err,req,res,next)` — 4 params, last | Centralized error responses |

---

### Q26. What does next() do? ★★★

`next()` passes control to the **NEXT middleware** in the stack. Without it, the request hangs — client gets no response and connection times out.

```js
// 1. Call next() — pass to next middleware
app.use((req, res, next) => {
  req.startTime = Date.now();
  next();
});

// 2. Send a response — ends the cycle
app.use((req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(401).json({ error: 'Unauthorized' });
    // 'return' prevents next() from also being called accidentally
  }
  next();
});

// 3. Call next(err) — jump directly to error handler
app.use(async (req, res, next) => {
  try {
    req.user = await verifyToken(req.headers.authorization);
    next();
  } catch (err) {
    next(err);  // skips all regular middleware, goes to (err,req,res,next)
  }
});
```

---

### Q27. Global Error Handling in Express

```js
// Step 1: Custom error class
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

// Step 2: Throw from anywhere
app.get('/user/:id', async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) throw new AppError('User not found', 404);
    res.json(user);
  } catch (err) {
    next(err);  // always pass to error handler
  }
});

// Step 3: catchAsync wrapper (avoid try/catch everywhere)
const catchAsync = (fn) => (req, res, next) => fn(req, res, next).catch(next);
app.get('/products', catchAsync(async (req, res) => {
  const products = await Product.find();
  res.json(products);
}));

// Step 4: Global error handler — LAST middleware, 4 params
app.use((err, req, res, next) => {
  const status  = err.statusCode || 500;
  const message = err.isOperational ? err.message : 'Internal Server Error';
  if (!err.isOperational) console.error('BUG:', err);
  res.status(status).json({
    success: false,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});
```

---

### Q28. Large Express Project Structure

```
project/
├── src/
│   ├── routes/         ← define endpoints, plug in controllers
│   ├── controllers/    ← handle req/res, call services, return response
│   ├── services/       ← business logic (no Express knowledge here)
│   ├── repositories/   ← DB queries only (no business logic)
│   ├── models/         ← Mongoose/Sequelize schemas
│   ├── middleware/     ← auth, validation, rate-limit
│   ├── config/         ← DB, env, constants
│   └── app.js          ← Express setup, register routes
├── .env
├── package.json
└── server.js           ← start HTTP server
```

> 📌 **Rule:** Controllers → Services → Repositories → DB. No layer skips another. Makes each layer independently testable.

---

### Q29. Request Validation with Joi

```js
const Joi = require('joi');

const registerSchema = Joi.object({
  email:    Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  age:      Joi.number().min(18).max(120),
});

function validate(schema) {
  return (req, res, next) => {
    const { error } = schema.validate(req.body, { abortEarly: false });
    if (error) {
      const errors = error.details.map(d => d.message);
      return res.status(400).json({ errors });
    }
    next();
  };
}

app.post('/register', validate(registerSchema), userController.register);
```

---

## Section 8: Databases, MongoDB & Indexing ★★★

### Q30. Indexing — Why It's Critical ★★★

An **index** is a sorted B-tree structure that allows the DB to find documents without scanning every record.

| Scenario | No Index (Collection Scan) | With Index (Index Scan) |
|---|---|---|
| Search 10M users by email | Scans ALL 10M documents | Jumps directly to matches |
| Time complexity | O(n) — linear | O(log n) — binary search |
| 10M record lookup | ~10 seconds | < 1 millisecond |
| Write speed | Fast (no extra structure) | Slightly slower (index also updates) |

```js
// Create indexes in MongoDB
db.users.createIndex({ email: 1 });                    // single field
db.users.createIndex({ email: 1, createdAt: -1 });     // compound

// Mongoose — define on schema
const UserSchema = new mongoose.Schema({
  email: { type: String, unique: true, index: true },
});
UserSchema.index({ username: 1, createdAt: -1 });      // compound

// ✅ ALWAYS verify your query uses the index!
db.users.find({ email: 'test@test.com' }).explain('executionStats');
// Look for: "IXSCAN" (good) vs "COLLSCAN" (bad — no index!)
```

> ⚠️ **Do NOT index every field.** Every index: (1) slows INSERT/UPDATE/DELETE, (2) uses RAM. Only index fields you frequently query, sort, or filter by.

**Index types:**

| Index Type | When to Use | Example |
|---|---|---|
| Single field | Query/sort on one field | `{ email: 1 }` |
| Compound | Query on multiple fields together | `{ country: 1, city: 1 }` |
| Unique | Enforce uniqueness | `{ email: 1 }, { unique: true }` |
| Text | Full-text search | `{ description: 'text' }` |
| TTL | Auto-delete after time (sessions) | `{ expiresAt: 1 }, { expireAfterSeconds: 0 }` |
| Sparse | Only index docs where field exists | `{ phone: 1 }, { sparse: true }` |

---

### Q31. SQL vs NoSQL

| Feature | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB) |
|---|---|---|
| Data model | Tables, rows, columns — rigid schema | Documents — flexible schema |
| Relationships | JOINs — powerful multi-table queries | Embedding or $lookup |
| Transactions | Full ACID by default | Added in MongoDB 4.0 |
| Horizontal scaling | Hard — requires sharding setup | Built-in sharding |
| Best for | Banking, ERP, complex relationships | Catalogs, CMS, real-time |

---

### Q32. Transactions & ACID Properties

A **transaction** groups multiple DB operations into one atomic unit — ALL succeed or ALL fail (rollback).

| ACID | Meaning | Example |
|---|---|---|
| **Atomicity** | All or nothing | Bank transfer: both debit AND credit succeed or neither does |
| **Consistency** | DB moves from one valid state to another | Balance cannot go negative |
| **Isolation** | Concurrent transactions don't interfere | Two transfers don't corrupt same balance |
| **Durability** | Committed data survives crashes | Written to disk, not just RAM |

```js
// MongoDB Transaction with Mongoose
const session = await mongoose.startSession();
session.startTransaction();

try {
  await Account.updateOne(
    { _id: senderId },
    { $inc: { balance: -amount } },
    { session }  // pass session to ALL operations
  );
  await Account.updateOne(
    { _id: receiverId },
    { $inc: { balance: +amount } },
    { session }
  );
  await session.commitTransaction();  // both succeed: save permanently
} catch (err) {
  await session.abortTransaction();   // either failed: undo everything
  throw err;
} finally {
  session.endSession();               // always release session
}
```

---

### Q33. Pagination — Offset vs Cursor

| Feature | Offset / Skip | Cursor-based |
|---|---|---|
| Mechanism | `SKIP n LIMIT m` | `WHERE _id > lastSeenId LIMIT m` |
| Performance on large pages | Gets slower as page grows | Constant O(log n) |
| Consistency | Can skip/duplicate on data changes | Stable — no gaps |
| Use case | Small datasets, admin UIs | Infinite scroll, feeds, large datasets |

```js
// Offset pagination (simple)
const page = 3, limit = 20;
const users = await User.find()
  .skip((page - 1) * limit)  // slow for page 1000+
  .limit(limit);

// Cursor pagination (scalable — always fast)
const users = await User.find({ _id: { $lt: lastSeenId } })
  .limit(20)
  .sort({ _id: -1 });
// Return: users + nextCursor = users[users.length-1]._id
```

---

### Q34. Connection Pooling

Connection pooling maintains **pre-established DB connections** that are reused — instead of opening/closing per request.

| Without Pooling | With Pooling |
|---|---|
| Open new connection per request (~20ms overhead) | Reuse existing connection (< 1ms) |
| DB overwhelmed by thousands of connections | Fixed pool size protects DB server |
| High latency under load | Consistent low latency |

```js
// Mongoose — pooling configured automatically
mongoose.connect(process.env.MONGO_URI, {
  maxPoolSize: 10,   // default 5; increase for high-traffic
  minPoolSize: 2,    // keep 2 connections warm always
  serverSelectionTimeoutMS: 5000,
});

// PostgreSQL (pg) — explicit pool
const { Pool } = require('pg');
const pool = new Pool({ max: 20, idleTimeoutMillis: 30000 });
const { rows } = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
```

---

### Q35. MongoDB Aggregation Pipeline

```js
// Total revenue per category — top 5
db.orders.aggregate([
  { $match:   { status: 'completed' } },
  { $group:   { _id: '$category', revenue: { $sum: '$amount' }, count: { $sum: 1 } } },
  { $sort:    { revenue: -1 } },
  { $limit:   5 },
  { $project: { _id: 0, category: '$_id', revenue: 1, count: 1 } }
]);

// $lookup — like SQL JOIN
db.orders.aggregate([
  { $lookup: {
      from: 'users', localField: 'userId', foreignField: '_id', as: 'user'
  }},
  { $unwind: '$user' },
  { $project: { orderTotal: 1, 'user.name': 1, 'user.email': 1 } }
]);
```

---

### Q36. Mongoose — Schemas, Hooks, Query Optimization

```js
const UserSchema = new mongoose.Schema({
  name:     { type: String, required: true, trim: true },
  email:    { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, select: false },  // never returned by default
  role:     { type: String, enum: ['user','admin'], default: 'user' }
}, { timestamps: true });

// Pre-save hook — hash password before saving
UserSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Instance method
UserSchema.methods.comparePassword = async function(candidate) {
  return bcrypt.compare(candidate, this.password);
};

// ── QUERY OPTIMIZATION ──
// lean() — plain JS objects, ~50% faster than full Mongoose docs
const users = await User.find({ role: 'admin' }).lean();

// select() — only fetch needed fields
const users = await User.find().select('name email -password');

// populate() — join related documents
const orders = await Order.find().populate('userId', 'name email');
```

---

## Section 9: Security & Authentication

### Q37. Common Security Vulnerabilities

| Attack | How It Works | Prevention |
|---|---|---|
| SQL/NoSQL Injection | Malicious input manipulates query logic | Parameterised queries, Mongoose ODM, input validation |
| XSS | Inject scripts via user input | Escape output, CSP headers (helmet), sanitize-html |
| CSRF | Forge requests using user cookies | CSRF tokens (csurf), SameSite=Strict cookies |
| Brute Force | Try millions of passwords | Rate limiting, account lockouts, bcrypt slow hash |
| Exposed Secrets | API keys/passwords in code | dotenv, .gitignore, secrets manager |
| Insecure Headers | Missing security HTTP headers | helmet.js — sets 11 headers automatically |
| Dependency Vulns | Outdated packages with CVEs | `npm audit`, Snyk, dependabot |

```js
app.use(require('helmet')());   // Secure HTTP headers
app.use(require('cors')({ origin: 'https://myapp.com' }));
app.use(require('express-rate-limit')({
  windowMs: 15 * 60 * 1000,   // 15 min window
  max:      100,               // 100 requests per IP
}));
// Stricter for auth routes
app.use('/api/auth/', require('express-rate-limit')({ windowMs: 15*60*1000, max: 5 }));
```

---

### Q38. Authentication vs Authorization

| Concept | Authentication | Authorization |
|---|---|---|
| Question | Who are you? | What are you allowed to do? |
| When | First — login/signup | After authentication confirmed |
| Failure response | **401 Unauthorized** | **403 Forbidden** |
| Example | Verify email + password | Check if user has 'admin' role |

---

### Q39. JWT Authentication — Full Flow ★★★

**Structure:** `Header.Payload.Signature` (3 parts, Base64URL encoded)
- **Header** — Algorithm (HS256) + type (JWT)
- **Payload** — Claims: userId, role, exp. **NOT encrypted — just encoded!**
- **Signature** — HMAC(Header + Payload, secretKey) — proves not tampered with

```js
const jwt    = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

// 1. REGISTER — hash password
app.post('/auth/register', async (req, res) => {
  const hash = await bcrypt.hash(req.body.password, 12);
  const user = await User.create({ email: req.body.email, password: hash });
  res.status(201).json({ message: 'Registered' });
});

// 2. LOGIN — verify + issue tokens
app.post('/auth/login', async (req, res) => {
  const user  = await User.findOne({ email: req.body.email }).select('+password');
  const valid = user && await bcrypt.compare(req.body.password, user.password);
  if (!valid) return res.status(401).json({ error: 'Invalid credentials' });

  // Short-lived access token (15 min)
  const accessToken = jwt.sign(
    { userId: user._id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );
  // Long-lived refresh token (7 days)
  const refreshToken = jwt.sign(
    { userId: user._id },
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  // Refresh token in httpOnly cookie (safe from XSS)
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true, secure: true, sameSite: 'Strict', maxAge: 7*24*3600*1000
  });
  res.json({ accessToken });
});

// 3. AUTH MIDDLEWARE — verify on protected routes
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]; // "Bearer <token>"
  if (!token) return res.status(401).json({ error: 'No token provided' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch (err) {
    res.status(403).json({ error: 'Invalid or expired token' });
  }
};

app.get('/profile', authenticate, (req, res) => res.json(req.user));
```

> ⚠️ **NEVER store JWTs in `localStorage`** — vulnerable to XSS. Store access tokens in memory and refresh tokens in `httpOnly` cookies.

---

### Q40. Session-based vs Token-based Authentication

| Feature | Session-based | Token-based (JWT) |
|---|---|---|
| Storage | Server stores session | Client stores token |
| State | Stateful | Stateless |
| Scaling | Hard — need sticky sessions or shared store | Easy — any server can verify |
| Revocation | Easy — delete session from DB | Hard — need token blacklist (Redis) |
| Best for | Traditional web apps | APIs, microservices, mobile apps |

---

## Section 10: API Design & REST

### Q41. REST API — Core Principles

| Principle | Meaning |
|---|---|
| **Stateless** | Each request contains ALL info. Server stores NO session between requests. |
| **Resource-based** | Everything is a resource: `/users/123` not `/getUser?id=123` |
| **Uniform Interface** | Standard HTTP methods and status codes |
| **Cacheable** | Responses declare if they can be cached |

| Method | Action | Example | Idempotent? |
|---|---|---|---|
| GET | Retrieve | `GET /users` or `GET /users/1` | Yes |
| POST | Create | `POST /users` | No |
| PUT | Replace entirely | `PUT /users/1` | Yes |
| PATCH | Partial update | `PATCH /users/1` | Yes |
| DELETE | Delete | `DELETE /users/1` | Yes |

---

### Q42. REST vs GraphQL

| Feature | REST | GraphQL |
|---|---|---|
| Endpoints | Multiple (`/users`, `/posts`) | Single `/graphql` |
| Data fetching | Over-fetch or under-fetch | Exact fields client requests |
| Versioning | URL versioning (`/v1`, `/v2`) | Schema evolution |
| Caching | Simple HTTP caching | Requires custom caching |
| Best for | Simple CRUD, public APIs | Complex data, mobile apps |

---

### Q43. API Versioning

```js
// URL versioning (recommended — simple, explicit)
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Header versioning
// Accept: application/vnd.myapi.v2+json
```

---

### Q44. gRPC vs REST

| Feature | REST | gRPC |
|---|---|---|
| Protocol | HTTP/1.1 | HTTP/2 (multiplexing, streaming) |
| Payload | JSON (text, larger) | Protobuf (binary, 5-10x smaller) |
| Streaming | Not native | Native bi-directional |
| Best for | Public APIs, CRUD | Microservice-to-microservice, low latency |

---

## Section 11: Error Handling, Testing & Debugging

### Q45. Operational vs Programmer Errors

| Type | Definition | Examples | How to Handle |
|---|---|---|---|
| **Operational** | Expected runtime errors | DB down, network timeout, invalid input | Catch, log, return HTTP error response |
| **Programmer** | Bugs in code | TypeError, undefined.property | Fix the bug — crash in dev, log + alert in prod |

---

### Q46. Handle Uncaught Exceptions in Production

```js
// Catch ALL uncaught synchronous errors
process.on('uncaughtException', (err) => {
  logger.error('UNCAUGHT EXCEPTION:', { error: err.message, stack: err.stack });
  process.exit(1);  // MUST exit — process is in unknown state. PM2 restarts.
});

// Catch ALL unhandled Promise rejections
process.on('unhandledRejection', (reason, promise) => {
  logger.error('UNHANDLED REJECTION:', { reason });
  process.exit(1);  // Node 15+ exits automatically
});

// Graceful shutdown (SIGTERM from Docker/Kubernetes)
process.on('SIGTERM', async () => {
  server.close(async () => {
    await mongoose.connection.close();
    await redis.quit();
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 30_000);  // force exit after 30s
});
```

---

### Q47. Testing in Node.js

| Tool | Purpose | When to Use |
|---|---|---|
| Jest | All-in-one: runner, assertions, mocking, coverage | Most popular — great for unit and integration |
| Supertest | HTTP assertions for Express APIs | Integration testing of HTTP endpoints |
| Mocha + Chai | Test runner + assertion library | When you want flexible setup |
| Sinon | Spies, stubs, mocks | Complex mocking scenarios |

```js
// ── UNIT TEST with Jest ──
const { createUser } = require('./user.service');
const UserRepo       = require('./user.repo');

jest.mock('./user.repo');

describe('UserService', () => {
  test('creates user', async () => {
    UserRepo.create.mockResolvedValue({ id: 1, email: 'test@test.com' });
    const result = await createUser({ email: 'test@test.com', password: 'pass' });
    expect(result).toHaveProperty('id');
    expect(UserRepo.create).toHaveBeenCalledTimes(1);
  });
});

// ── INTEGRATION TEST with Supertest ──
const request = require('supertest');
const app     = require('./app');

test('returns 401 for missing token', async () => {
  const res = await request(app).get('/api/profile');
  expect(res.statusCode).toBe(401);
});
```

---

### Q48. Debugging Node.js

```bash
# Chrome DevTools
node --inspect-brk app.js
# Open chrome://inspect → "Open dedicated DevTools for Node"

# VS Code — .vscode/launch.json
{
  "type": "node",
  "request": "launch",
  "name": "Debug App",
  "program": "${workspaceFolder}/src/app.js"
}
```

```js
// Console helpers
console.table([{ name: 'Alice', age: 30 }, { name: 'Bob', age: 25 }]);
console.time('op');  /* code */  console.timeEnd('op');
console.group('Auth'); console.log('checking...'); console.groupEnd();

// Deep inspect
const util = require('util');
console.log(util.inspect(complexObject, { depth: null, colors: true }));
```

---

## Section 12: Performance, Scaling & Deployment

### Q49. Performance Optimization Techniques

| Technique | Impact | How to Implement |
|---|---|---|
| Database indexes | **Huge** — queries 1000x faster | `createIndex` on every queried field |
| Redis caching | **High** — skip DB for hot data | Cache DB results for 5-60 min |
| `Promise.all()` (parallel) | **High** — cut sequential await chains | Run independent async ops together |
| Stream large data | **High** — no RAM spike | `fs.createReadStream`, `res.write` |
| Response compression | **Medium** — 70% smaller payloads | `app.use(require('compression')())` |
| Connection pooling | **Medium** — no reconnect overhead | `maxPoolSize` in Mongoose/pg config |
| `lean()` queries | **Medium** — 50% faster Mongoose | `User.find().lean()` |
| Projection | **Medium** — less data transferred | `User.find().select('name email')` |
| Worker Threads | **High** for CPU tasks | Offload crypto/ML from main thread |

---

### Q50. Redis Caching — Cache-Aside Pattern

```js
const redis = require('ioredis');
const client = new redis(process.env.REDIS_URL);

async function getUser(id) {
  const key = `user:${id}`;

  // 1. Try cache first (fast path)
  const cached = await client.get(key);
  if (cached) return JSON.parse(cached);

  // 2. Cache miss — query DB
  const user = await User.findById(id).lean();
  if (!user) return null;

  // 3. Store in cache for 5 minutes
  await client.setex(key, 300, JSON.stringify(user));
  return user;
}

// Invalidate cache on update
async function updateUser(id, data) {
  const user = await User.findByIdAndUpdate(id, data, { new: true });
  await client.del(`user:${id}`);  // remove stale cache
  return user;
}
```

---

### Q51. Horizontal vs Vertical Scaling

| Feature | Vertical (Scale Up) | Horizontal (Scale Out) |
|---|---|---|
| What it means | Add more CPU/RAM to ONE server | Add MORE server instances |
| Limit | Hardware ceiling | Theoretically unlimited |
| Downtime | Needs restart | No downtime |
| Cost | Expensive premium hardware | Cheaper commodity servers |
| Failure risk | Single point of failure | Distributed — one server failing is ok |

---

### Q52. PM2 — Production Process Manager

```bash
# Start with clustering (use all CPU cores)
pm2 start app.js -i max --name "myapi"

# Zero-downtime reload (for deployments)
pm2 reload myapi

# Auto-restart on crash + server reboot
pm2 startup && pm2 save

# Monitor
pm2 monit          # CPU, RAM, logs live
pm2 logs myapi     # view logs
```

```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name:    'myapi',
    script:  'src/app.js',
    instances: 'max',         // one per CPU core
    exec_mode: 'cluster',
    max_memory_restart: '500M',
    env_production: { NODE_ENV: 'production', PORT: 3000 }
  }]
};
```

---

### Q53. Docker — Containerising Node.js

```dockerfile
# Dockerfile (production-optimised)
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json .
RUN npm ci --only=production

FROM base AS production
COPY . .
EXPOSE 3000
USER node        # Never run as root!
CMD ["node", "src/app.js"]
```

```yaml
# docker-compose.yml — local dev with DB + Redis
version: '3.8'
services:
  api:
    build: .
    ports: ["3000:3000"]
    env_file: .env
    depends_on: [mongo, redis]
  mongo:
    image: mongo:7
    volumes: [mongo_data:/data/db]
  redis:
    image: redis:7-alpine
volumes:
  mongo_data:
```

---

### Q54. Logging — Winston + Morgan

```js
const winston = require('winston');
const morgan  = require('morgan');

const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'warn' : 'debug',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()    // structured JSON logs
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log',    level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ]
});

// HTTP request logging
app.use(morgan('combined', { stream: { write: msg => logger.http(msg.trim()) } }));

// Usage
logger.info('Server started', { port: 3000 });
logger.error('DB failed', { error: err.message });
```

---

## Section 13: Real-Time, Message Queues & Microservices

### Q55. WebSockets vs HTTP vs SSE

| Feature | HTTP | WebSocket | Server-Sent Events (SSE) |
|---|---|---|---|
| Connection | New per request | Single persistent | Single persistent |
| Direction | Client → Server → Response | Full-duplex (both ways) | Server → Client only |
| Use case | APIs, CRUD | Chat, games, collaboration | Notifications, live feeds |

```js
// Socket.IO Server
const io = require('socket.io')(server, {
  cors: { origin: 'https://myapp.com' }
});

io.on('connection', (socket) => {
  socket.on('joinRoom', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('userJoined', { userId: socket.id });
  });

  socket.on('message', ({ roomId, text }) => {
    io.to(roomId).emit('message', { from: socket.id, text });
  });
});

// Scale Socket.IO across multiple servers with Redis
const { createAdapter } = require('@socket.io/redis-adapter');
io.adapter(createAdapter(pubClient, subClient));
```

---

### Q56. Message Queues — Bull + Redis

```js
const Queue = require('bull');

// Producer (web server) — add job, don't wait
const emailQueue = new Queue('email', { redis: process.env.REDIS_URL });

app.post('/register', async (req, res) => {
  const user = await User.create(req.body);
  await emailQueue.add({ to: user.email }, {
    attempts: 3,    // retry 3 times on failure
    backoff:  5000, // wait 5s between retries
  });
  res.status(201).json({ message: 'Registered' });
});

// Consumer (separate worker process)
emailQueue.process(async (job) => {
  await sendEmail({ to: job.data.to, subject: 'Welcome!' });
});

emailQueue.on('completed', (job) => console.log('Email sent:', job.id));
emailQueue.on('failed',    (job, err) => console.error('Failed:', err));
```

---

### Q57. Microservices vs Monolith

| Feature | Monolithic | Microservices |
|---|---|---|
| Structure | Single deployable app | Multiple independent services |
| Deployment | Deploy entire app for any change | Deploy only changed service |
| Scaling | Scale entire app | Scale individual services |
| Database | Shared database | Each service has its own DB |
| Failure | One bug can crash everything | Isolated failures |
| Complexity | Simple to start | Complex — needs API gateway, service discovery |

**Communication patterns:**
- **REST APIs** — Simple, synchronous. Good for simple reads.
- **gRPC** — Fast binary. Great for internal microservice calls.
- **Message Brokers (Kafka/RabbitMQ)** — Async, decoupled. Best for events.
- **API Gateway** — Single entry point (NGINX, AWS API Gateway) that routes to the right service.

---

## Section 14: System Design & Advanced Scenarios

### Q58. Designing a Scalable REST API — Checklist

- **Stateless** — No server sessions. Use Redis or JWT. Enables horizontal scaling.
- **Layered architecture** — Routes → Controllers → Services → Repositories → DB.
- **Database indexes** — Index every queried field. Verify with `explain()`.
- **Caching** — Redis for hot data. Cache-aside pattern.
- **Cursor-based pagination** — Never return unbounded results.
- **Rate limiting** — Per-IP and per-user. Stricter on auth routes.
- **Async processing** — Push heavy work (email, reports) to message queues.
- **Load balancing** — PM2 cluster + NGINX, or managed LB (AWS ELB).
- **Health checks** — `GET /health` for load balancers.
- **Monitoring** — Prometheus metrics, Winston logs, Sentry for errors.

---

### Q59. Real-Time Chat App — Architecture

```js
// Architecture:
// Client ──WebSocket──> Node.js (Socket.IO)
//                          ──Redis Pub/Sub──>
//                                  Node.js ──WebSocket──> Client
// (Redis allows horizontal scaling across multiple Node servers)

io.on('connection', async (socket) => {
  const user = await verifySocketToken(socket.handshake.auth.token);

  socket.on('joinChat', async (chatId) => {
    socket.join(`chat:${chatId}`);
    const messages = await Message.find({ chatId }).sort('-createdAt').limit(50).lean();
    socket.emit('chatHistory', messages.reverse());
  });

  socket.on('sendMessage', async ({ chatId, text }) => {
    const message = await Message.create({ chatId, from: user._id, text });
    io.to(`chat:${chatId}`).emit('newMessage', message);
  });

  socket.on('typing', ({ chatId }) => {
    socket.to(`chat:${chatId}`).emit('userTyping', { userId: user._id });
  });
});
```

---

### Q60. Serverless vs Server-based

| Factor | Server-based (Express + EC2) | Serverless (Lambda, Vercel) |
|---|---|---|
| Cost | Pay always — even at 0 traffic | Pay per invocation — 0 at 0 traffic |
| Cold starts | None — always warm | 50ms–2s delay after inactivity |
| Scaling | Manual / auto-scaling config | Automatic — instant to millions |
| Execution limit | No limit | Max 15 min (Lambda) |
| WebSockets | Native support | Not supported by most |
| Choose when | Long-running, WebSockets, CPU-heavy | APIs, webhooks, event handlers |

---

### Q61. File Uploads — Secure Multer Setup

```js
const multer = require('multer');
const crypto = require('crypto');
const path   = require('path');

const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => cb(null, '/tmp/uploads/'),
    filename: (req, file, cb) => {
      // Use random name — NEVER trust original filename
      const ext  = path.extname(file.originalname).toLowerCase();
      const name = crypto.randomBytes(16).toString('hex');
      cb(null, `${name}${ext}`);
    }
  }),
  limits: { fileSize: 10 * 1024 * 1024 },  // 10MB max
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
    if (allowed.includes(file.mimetype)) cb(null, true);
    else cb(new AppError('File type not allowed', 400));
  }
});

app.post('/upload', authenticate, upload.single('file'), async (req, res) => {
  const url = await uploadToS3(req.file);  // upload to cloud storage
  fs.unlink(req.file.path, () => {});       // clean up temp file
  res.json({ url });
});
```

---

### Q62. Environment Variables — Best Practices

```bash
# .env — NEVER commit to git (add to .gitignore)
NODE_ENV=development
PORT=3000
MONGO_URI=mongodb://localhost:27017/mydb
JWT_SECRET=superSecretKeyChangeInProduction
REDIS_URL=redis://localhost:6379
```

```js
// Load BEFORE any other imports
require('dotenv').config();

// Validate required env vars at startup
const required = ['MONGO_URI', 'JWT_SECRET', 'REDIS_URL'];
required.forEach(key => {
  if (!process.env[key]) throw new Error(`Missing required env var: ${key}`);
});

// Multiple environments
require('dotenv').config({ path: `.env.${process.env.NODE_ENV}` });
```

---

## Quick Reference Cheat Sheets

---

### ⚡ Event Loop — Say This in Every Interview

```
Execution Order:
Sync Code → process.nextTick() → Promise.then() → setTimeout(fn,0) → setImmediate() → I/O Callbacks

6 Phases:
Timers → Pending Callbacks → Idle/Prepare → Poll (I/O) → Check (setImmediate) → Close Callbacks
```

---

### 🎯 The 4 Topics That Cover 70% of Interviews

| Topic | One-Line Answer | Key Code |
|---|---|---|
| **Event Loop** | 6 phases; microtasks (nextTick, Promise) run between phases | Predict any async output question |
| **Async** | async/await = Promise sugar; Promise.all() for parallel; try/catch for errors | `const [a,b] = await Promise.all([x(), y()])` |
| **Middleware** | (req,res,next) pipeline; call next() or send response; error handler = 4 params | `app.use((err,req,res,next) => ...)` |
| **Indexing** | B-tree; O(log n) reads; slows writes; use explain() to verify | `db.col.createIndex({field:1})` |

---

### 📊 HTTP Status Codes — Know These Cold

| Code | Meaning | When to Return |
|---|---|---|
| 200 | OK | GET, PUT, PATCH success |
| 201 | Created | POST that creates a resource |
| 204 | No Content | DELETE success |
| 400 | Bad Request | Validation errors, missing fields |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Valid token but wrong role/permission |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource (email already registered) |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Programmer errors, unhandled exceptions |
| 503 | Service Unavailable | DB connection lost, server overloaded |

---

### 📦 npm Package Reference — Must Know

| Package | Purpose | Key Usage |
|---|---|---|
| `express` | Web framework | `app.use()`, `app.get()`, `app.listen()` |
| `mongoose` | MongoDB ODM | `Schema`, `Model.find().lean()`, `.save()` |
| `jsonwebtoken` | JWT sign/verify | `jwt.sign({},secret,{expiresIn:'15m'})` |
| `bcryptjs` | Password hashing | `bcrypt.hash(pw,12)`, `bcrypt.compare(pw,hash)` |
| `dotenv` | Env variables | `require('dotenv').config()` |
| `cors` | CORS headers | `app.use(cors({ origin: 'https://x.com' }))` |
| `helmet` | Security headers | `app.use(helmet())` |
| `express-rate-limit` | Rate limiting | `rateLimit({ windowMs, max })` |
| `joi` / `zod` | Request validation | `Joi.object({email: Joi.string().email()})` |
| `multer` | File uploads | `upload.single('field')` |
| `compression` | Gzip responses | `app.use(compression())` |
| `socket.io` | WebSockets | `io.on('connection', socket => {})` |
| `winston` | Structured logging | `logger.error('msg', { meta })` |
| `morgan` | HTTP request logs | `app.use(morgan('combined'))` |
| `ioredis` | Redis client | `client.get(key)`, `client.setex(key,ttl,val)` |
| `bull` | Job queues | `new Queue('email').add(data)` |
| `node-cron` | Cron jobs | `cron.schedule('0 2 * * *', fn)` |
| `pm2` | Process manager | `pm2 start app.js -i max` |
| `nodemon` | Dev auto-restart | `nodemon app.js` |
| `supertest` | API testing | `request(app).get('/').expect(200)` |
| `jest` | Unit testing | `test('desc', () => expect(x).toBe(y))` |

---

### 💻 5 Must-Memorise Code Snippets

#### 1. Predict Output (Event Loop)
```js
console.log('1');
setTimeout(() => console.log('4'), 0);
Promise.resolve().then(() => console.log('3'));
process.nextTick(() => console.log('2'));
console.log('5');
// Output: 1, 5, 2, 3, 4
```

#### 2. Parallel vs Sequential Async
```js
// ❌ Sequential — 3 seconds
const a = await delay(1000);
const b = await delay(1000);
const c = await delay(1000);

// ✅ Parallel — 1 second
const [a, b, c] = await Promise.all([delay(1000), delay(1000), delay(1000)]);
```

#### 3. Express Global Error Handler
```js
app.use((err, req, res, next) => {
  res.status(err.statusCode || 500).json({ message: err.message });
});
```

#### 4. JWT Auth Middleware
```js
const auth = (req, res, next) => {
  try {
    req.user = jwt.verify(
      req.headers.authorization?.split(' ')[1],
      process.env.JWT_SECRET
    );
    next();
  } catch {
    res.status(403).json({ error: 'Invalid token' });
  }
};
```

#### 5. MongoDB Transaction
```js
const session = await mongoose.startSession();
session.startTransaction();
try {
  await ModelA.updateOne({ _id: id1 }, { $inc: { balance: -100 } }, { session });
  await ModelB.updateOne({ _id: id2 }, { $inc: { balance: +100 } }, { session });
  await session.commitTransaction();
} catch (err) {
  await session.abortTransaction();
  throw err;
} finally {
  session.endSession();
}
```

---

## 🎯 Final Interview Formula

> ✅ **Event Loop** — Know 6 phases + predict any async output
>
> ✅ **Async** — `Promise.all()` for parallel, `try/catch` for errors, explain async/await vs Promise
>
> ✅ **Middleware** — `(req,res,next)` pipeline, always `next()` or send response, 4-param error handler last
>
> ✅ **Indexing** — B-tree speeds reads to O(log n), slows writes, verify with `explain()`







# REST vs Event-Driven Architecture (Interview Notes)

## 🔹 REST

- **Architecture**: Request–Response  
- **Type**: Synchronous  
- **Working**: Client sends request → Server responds immediately  
- **Protocol**: HTTP (GET, POST, PUT, DELETE)  
- **Coupling**: Tight (client must know API endpoints)  
- **Use Cases**:
  - CRUD applications
  - Frontend ↔ Backend communication
  - Simple APIs

**Example:**
GET /users/1 → returns user data

---

## 🔹 Event-Driven Architecture

- **Architecture**: Publish–Subscribe (Event-based)  
- **Type**: Asynchronous  
- **Working**: Service emits event → Other services listen & react  
- **Coupling**: Loose (services don’t directly depend on each other)  
- **Tools**: Kafka, RabbitMQ  
- **Use Cases**:
  - Microservices architecture
  - Real-time systems
  - Notifications, logging, analytics

**Example:**
OrderPlaced → triggers Payment Service & Notification Service

---

## 🔥 Key Differences

| Feature        | REST                     | Event-Driven              |
|---------------|--------------------------|---------------------------|
| Communication | Request–Response         | Events (Pub/Sub)          |
| Type          | Synchronous              | Asynchronous              |
| Coupling      | Tight                    | Loose                     |
| Scalability   | Moderate                 | High                      |

---

## 💡 One-Line Answer

REST is synchronous and tightly coupled, whereas event-driven architecture is asynchronous and loosely coupled, making it more scalable for distributed systems.



# AWS Lambda vs AWS Fargate

## 1. AWS Lambda
- **Type:** Serverless, event-driven compute service  
- **Usage:** Run small pieces of code (functions) in response to events  
- **Scaling:** Automatic, per request/event  
- **Server Management:** Fully managed, no server provisioning needed  
- **Billing:** Pay only for execution time (per millisecond) and number of requests  
- **Best For:**  
  - Processing files in S3  
  - Triggering actions from API Gateway  
  - Handling DynamoDB streams  
  - Scheduled jobs (cron)  
- **Limitations:**  
  - Max execution time 15 minutes  
  - Limited control over runtime environment  

---

## 2. AWS Fargate
- **Type:** Serverless container compute service  
- **Usage:** Run Docker containers without managing EC2 instances  
- **Scaling:** Automatic per task/service (configurable)  
- **Server Management:** No servers, but you manage containers and tasks  
- **Billing:** Pay for vCPU and memory allocated per container per second  
- **Best For:**  
  - Microservices  
  - Web applications  
  - APIs running in containers  
  - Long-running background services  
- **Advantages:**  
  - Can run long-running containers  
  - Full control over container environment  

---

## 3. Key Differences

| Feature             | AWS Lambda                  | AWS Fargate                         |
|--------------------|----------------------------|-----------------------------------|
| Compute Model       | Function (serverless)       | Container (serverless)             |
| Language Support    | Node.js, Python, Java, etc. | Any language in container          |
| Event Handling      | Event-driven                | Runs continuously or on schedule   |
| Duration            | Short-lived (<15 mins)      | Can run long-running containers    |
| Scaling             | Automatic per event         | Automatic per task/service         |
| Control             | Minimal (managed runtime)   | More control over environment      |

---

## 4. Summary
- **Lambda:** Best for quick, event-driven tasks  
- **Fargate:** Best for containerized applications, microservices, or long-running workloads  