# React & Next.js — Complete Frontend Interview Notes

> **How to use:** Read each section before interviews. Every answer includes a concept description + code example so you can revise quickly.

---

## Table of Contents

1. [React Core Concepts](#section-1-react-core-concepts)
2. [React Hooks](#section-2-react-hooks)
3. [React Routing](#section-3-react-routing)
4. [Performance & Optimization](#section-4-performance--optimization)
5. [Next.js Basics](#section-5-nextjs-basics)
6. [Advanced Next.js](#section-6-advanced-nextjs)
7. [State Management](#section-7-state-management)
8. [TypeScript with React](#section-8-typescript-with-react)
9. [Practical Patterns](#section-9-practical-patterns)
10. [Common Interview Patterns & Tricky Questions](#section-10-common-interview-patterns--tricky-questions)
11. [Performance Optimization](#section-11-performance-optimization)

---

# Section 1: React Core Concepts

## 1. What is React and why use it over vanilla JS?

React is a **JavaScript library** (not a framework) developed by Meta for building user interfaces using a **component-based architecture**.

**Why React over Vanilla JS:**
- **Virtual DOM** — React batches and minimizes real DOM updates, improving performance
- **Reusable Components** — Build once, use anywhere
- **Declarative UI** — Describe *what* the UI looks like, React figures out *how* to update it
- **Ecosystem** — Rich tooling, libraries, and community

---

## 2. What is JSX?

JSX (JavaScript XML) lets you write HTML-like syntax inside JavaScript. It is **not valid JS** — it gets compiled by **Babel** into `React.createElement()` calls.

```jsx
// JSX
const element = <h1>Hello, World</h1>;

// What Babel compiles it to:
const element = React.createElement('h1', null, 'Hello, World');
```

---

## 3. What is the Virtual DOM?

The Virtual DOM (VDOM) is a **lightweight, in-memory copy** of the real DOM. When state changes:

1. React creates a new Virtual DOM tree
2. It **diffs** (compares) it with the previous VDOM (**reconciliation**)
3. Only the changed parts are updated in the **real DOM** (patching)

This avoids expensive full-page re-renders.

---

## 4. What is Reconciliation?

Reconciliation is the process React uses to **compare the new Virtual DOM with the previous one** and determine the **minimum set of DOM operations** needed. React uses a **diffing algorithm** that:
- Compares nodes by **type** first
- Uses **keys** to match list items
- Skips subtrees if parent type hasn't changed

---

## 5. State vs Props

| Feature | State | Props |
|---|---|---|
| Managed by | Component itself | Parent component |
| Mutable? | Yes (via setState/useState) | No (read-only) |
| Triggers re-render? | Yes | Yes (when changed by parent) |

```jsx
// Props — passed from parent
function Child({ name }) {
  return <p>Hello, {name}</p>;
}

// State — managed inside component
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## 6. Class vs Functional Components

| Feature | Class Component | Functional Component |
|---|---|---|
| Syntax | `class MyComp extends React.Component` | `function MyComp()` |
| State | `this.state` | `useState` hook |
| Lifecycle | Lifecycle methods | `useEffect` hook |
| Performance | Slightly heavier | Lighter, preferred today |

Functional components are the **modern standard**. Class components are legacy but still appear in older codebases.

---

## 7. Component Lifecycle (Class Components)

```
Mount  →  Update  →  Unmount
```

| Phase | Method | Description |
|---|---|---|
| Mount | `componentDidMount()` | Runs after component is inserted into DOM |
| Update | `componentDidUpdate()` | Runs after props/state change triggers re-render |
| Unmount | `componentWillUnmount()` | Runs before component is removed from DOM |

**Functional equivalent with hooks:**
```jsx
useEffect(() => {
  // componentDidMount
  return () => {
    // componentWillUnmount
  };
}, []); // [] = run once on mount
```

---

## 8. Keys in Lists

Keys are **unique identifiers** that help React track which list items changed, were added, or removed during reconciliation.

```jsx
{items.map(item => (
  <li key={item.id}>{item.name}</li>  // ✅ Use stable unique IDs
))}

// ❌ Avoid using array index as key (causes bugs on reorder/delete)
{items.map((item, index) => <li key={index}>{item.name}</li>)}
```

---

## 9. Controlled vs Uncontrolled Components

**Controlled** — React state is the single source of truth for the input value.
**Uncontrolled** — The DOM itself holds the value; you access it via a `ref`.

```jsx
// Controlled
const [name, setName] = useState('');
<input value={name} onChange={e => setName(e.target.value)} />

// Uncontrolled
const inputRef = useRef();
<input ref={inputRef} />
// Access value: inputRef.current.value
```

---

## 10. Passing Data: Parent ↔ Child

```jsx
// Parent → Child: via props
<Child message="Hello" />

// Child → Parent: via callback function passed as prop
function Parent() {
  const [msg, setMsg] = useState('');
  return <Child onSend={setMsg} />;
}

function Child({ onSend }) {
  return <button onClick={() => onSend('Hi Parent!')}>Send</button>;
}
```

---

## 11. Lifting State Up

When multiple sibling components need to share state, **move the state to their common parent** and pass it down via props.

```jsx
function Parent() {
  const [value, setValue] = useState('');
  return (
    <>
      <InputChild onChange={setValue} />
      <DisplayChild value={value} />
    </>
  );
}
```

---

## 12. Prop Drilling & How to Avoid It

**Prop drilling** = passing props through many intermediate components that don't need them.

**Solutions:**
- **Context API** — built-in global state
- **Redux / Zustand** — external state libraries
- **Component composition** — restructure components to avoid depth

---

## 13. Fragments

Fragments let you return multiple elements without adding extra DOM nodes.

```jsx
// Short syntax (preferred)
return (
  <>
    <h1>Title</h1>
    <p>Body</p>
  </>
);

// Full syntax (needed when you need to pass a key)
return (
  <React.Fragment key={id}>
    <dt>Term</dt>
    <dd>Definition</dd>
  </React.Fragment>
);
```

---

## 14. React Portals

Portals render a child component **outside the parent component's DOM hierarchy**, while still being part of the React tree. Useful for modals, tooltips, and overlays.

```jsx
import ReactDOM from 'react-dom';

function Modal({ children }) {
  return ReactDOM.createPortal(
    <div className="modal">{children}</div>,
    document.getElementById('modal-root') // renders here in HTML
  );
}
```

---

## 15. Error Boundaries

Error boundaries catch JavaScript errors in **child component trees** and display a fallback UI instead of crashing the whole app.

> ⚠️ Only available as **class components** (no hook equivalent yet).

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  componentDidCatch(error, info) {
    this.setState({ hasError: true });
    console.error(error, info);
  }

  render() {
    if (this.state.hasError) return <h1>Something went wrong.</h1>;
    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <MyComponent />
</ErrorBoundary>
```

---

## 16. Higher-Order Components (HOC)

A HOC is a **function that takes a component and returns a new enhanced component**. It's a pattern for reusing component logic.

```jsx
function withLogger(WrappedComponent) {
  return function EnhancedComponent(props) {
    console.log('Rendering', WrappedComponent.name);
    return <WrappedComponent {...props} />;
  };
}

const LoggedButton = withLogger(Button);
```

---

## 17. React.memo vs PureComponent

Both prevent unnecessary re-renders by doing **shallow prop comparison**.

```jsx
// Functional component
const MyComponent = React.memo(function MyComponent({ value }) {
  return <div>{value}</div>;
});

// With custom comparison
export default React.memo(MyComponent, (prevProps, nextProps) => {
  return prevProps.value === nextProps.value;
});
```

| | React.Component | React.PureComponent | React.memo |
|---|---|---|---|
| Type | Class | Class | Functional |
| Re-render check | Always | Shallow compare | Shallow compare |

---

## 18. Conditional Rendering

```jsx
// Ternary operator
{isLoggedIn ? <Dashboard /> : <Login />}

// Short-circuit (render or nothing)
{isAdmin && <AdminPanel />}

// Null to render nothing
if (!isVisible) return null;
```

---

## 19. Forms in React

```jsx
function Form() {
  const [form, setForm] = useState({ name: '', email: '' });

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault(); // prevent page reload
    console.log(form);
    setForm({ name: '', email: '' }); // clear after submit
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" value={form.name} onChange={handleChange} />
      <input name="email" value={form.email} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## 20. Synthetic Events

React wraps native browser events in **SyntheticEvent** objects for cross-browser compatibility. The API is identical to native events (`e.target`, `e.preventDefault()`, etc.), but React pools and reuses these objects for performance.

---

## 21. React 17 vs React 18

| Feature | React 17 | React 18 |
|---|---|---|
| Concurrent Rendering | ❌ | ✅ |
| Automatic Batching | Partial | ✅ Full (async, timeouts) |
| `useTransition` | ❌ | ✅ |
| `useDeferredValue` | ❌ | ✅ |
| `createRoot` API | ❌ | ✅ |

```jsx
// React 18: createRoot (enables concurrent features)
import { createRoot } from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

---

## 22. Refs (`useRef`)

Refs provide direct access to DOM elements without causing re-renders when changed.

```jsx
const inputRef = useRef(null);

// Focus on mount
useEffect(() => {
  inputRef.current.focus();
}, []);

return <input ref={inputRef} />;
```

**Also used to:** Store mutable values that persist across renders (like timers) without triggering re-renders.

---

## 23. defaultProps and propTypes

```jsx
import PropTypes from 'prop-types';

function Button({ label, color }) {
  return <button style={{ background: color }}>{label}</button>;
}

Button.defaultProps = { color: 'blue' };
Button.propTypes = {
  label: PropTypes.string.isRequired,
  color: PropTypes.string,
};
```

> In TypeScript projects, use **TypeScript interfaces/types** instead of propTypes.

---

# Section 2: React Hooks

> **Rules of Hooks:**
> 1. Only call hooks at the **top level** (not inside loops, conditions, or nested functions)
> 2. Only call hooks from **React function components** or custom hooks
> 3. Hooks do **NOT** work in class components

---

## 1. useState

Adds state to functional components.

```jsx
const [count, setCount] = useState(0);

// Functional update (safe when new state depends on old state)
setCount(prev => prev + 1);

// Object state — spread to avoid losing other fields
const [user, setUser] = useState({ name: '', age: 0 });
setUser(prev => ({ ...prev, name: 'John' }));
```

---

## 2. useEffect

Handles **side effects**: data fetching, subscriptions, DOM manipulation, timers.

```jsx
useEffect(() => {
  // Side effect code here

  return () => {
    // Cleanup (runs on unmount or before next effect)
  };
}, [dependency]); // Dependency array controls when effect runs
```

**Dependency array rules:**
- `[]` — runs **once** on mount (like componentDidMount)
- `[value]` — runs when `value` changes
- *(no array)* — runs on **every render**

---

## 3. useRef

Two main use cases:

```jsx
// 1. DOM access
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();

// 2. Mutable value that persists without re-render (e.g. store timer ID)
const timerRef = useRef(null);
timerRef.current = setInterval(() => console.log('tick'), 1000);
// Later: clearInterval(timerRef.current);
```

---

## 4. useMemo

Memoizes an **expensive computed value** so it's only recalculated when dependencies change.

```jsx
const expensiveResult = useMemo(() => {
  return computeHeavyCalculation(data);
}, [data]); // Only recalculates when `data` changes
```

> Use when a computation is slow — don't use for everything, as memoization itself has overhead.

---

## 5. useCallback

Memoizes a **function** so it isn't recreated on every render. Useful when passing callbacks to memoized child components.

```jsx
const handleClick = useCallback(() => {
  doSomething(value);
}, [value]); // Only recreates when `value` changes
```

> Without `useCallback`, a new function reference is created every render → breaks `React.memo` on child.

---

## 6. useReducer

Alternative to `useState` for **complex state logic** with multiple sub-values or when next state depends on multiple actions.

```jsx
const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 };
    case 'decrement': return { count: state.count - 1 };
    case 'reset':     return initialState;
    default: return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <>
      <p>{state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </>
  );
}
```

| useState | useReducer |
|---|---|
| Simple values | Complex state logic |
| Direct setter | Dispatch + reducer |
| Good for: counters, booleans | Good for: forms, carts, multi-step |

---

## 7. useContext

Reads a value from a Context without prop drilling.

```jsx
// 1. Create context
const ThemeContext = React.createContext('light');

// 2. Provide at the top level
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Page />
    </ThemeContext.Provider>
  );
}

// 3. Consume anywhere in the tree
function Button() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Click me</button>;
}
```

---

## 8. Custom Hooks

Custom hooks are JavaScript functions that **start with `use`** and can call other hooks. They let you extract and reuse stateful logic.

```jsx
// Custom hook for data fetching
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(url)
      .then(res => res.json())
      .then(data => { setData(data); setLoading(false); })
      .catch(err => { setError(err); setLoading(false); });
  }, [url]);

  return { data, loading, error };
}

// Usage
const { data, loading } = useFetch('/api/users');
```

---

## 9. useLayoutEffect

Like `useEffect`, but fires **synchronously after DOM mutations and before the browser paints**. Use for measuring DOM elements or synchronous DOM updates.

```jsx
useLayoutEffect(() => {
  const height = divRef.current.getBoundingClientRect().height;
  setHeight(height); // Won't cause visible flicker
}, []);
```

| useEffect | useLayoutEffect |
|---|---|
| After paint (async) | Before paint (sync) |
| For API calls, subscriptions | For DOM measurements |
| Non-blocking | Can block paint |

---

## 10. useImperativeHandle + forwardRef

Lets a parent component call methods/properties on a child component via a ref.

```jsx
const FancyInput = React.forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current.focus(),
    clear: () => (inputRef.current.value = ''),
  }));

  return <input ref={inputRef} />;
});

// In parent:
const ref = useRef();
<FancyInput ref={ref} />
<button onClick={() => ref.current.focus()}>Focus Input</button>
```

---

## 11. Cleaning up Effects

```jsx
useEffect(() => {
  // Setup
  const id = setInterval(() => setCount(c => c + 1), 1000);

  // Cleanup — runs on unmount or before next effect
  return () => clearInterval(id);
}, []);

// Cancelling fetch with AbortController
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then(res => res.json())
    .then(setData);
  return () => controller.abort();
}, [url]);
```

---

## 12. Debouncing with Hooks

```jsx
function useDebounce(value, delay = 500) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler); // Clear on value change
  }, [value, delay]);

  return debounced;
}

// Usage — only searches 500ms after user stops typing
const debouncedSearch = useDebounce(searchTerm, 500);
useEffect(() => { fetchResults(debouncedSearch); }, [debouncedSearch]);
```

---

## 13. Persisting State to localStorage

```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}
```

---

# Section 3: React Routing

## 1. React Router Basics

React Router enables **client-side navigation** — switching views without a full page reload.

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<NotFound />} /> {/* 404 */}
      </Routes>
    </BrowserRouter>
  );
}
```

---

## 2. BrowserRouter vs HashRouter

| | BrowserRouter | HashRouter |
|---|---|---|
| URL style | `/about` | `/#/about` |
| Requires server config | Yes | No |
| SEO friendly | Yes | No |
| Use case | Production apps | Static hosting / legacy |

---

## 3. Navigation Components

```jsx
import { Link, NavLink } from 'react-router-dom';

// Link — basic navigation
<Link to="/home">Home</Link>

// NavLink — adds active class when route matches
<NavLink to="/home" className={({ isActive }) => isActive ? 'active' : ''}>
  Home
</NavLink>
```

---

## 4. Programmatic Navigation

```jsx
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // after login...
    navigate('/dashboard');        // go to route
    navigate(-1);                  // go back
    navigate('/login', { replace: true }); // replace history entry
  };
}
```

---

## 5. Dynamic Routes & useParams

```jsx
// Route definition
<Route path="/users/:id" element={<UserDetail />} />

// In component
import { useParams } from 'react-router-dom';
function UserDetail() {
  const { id } = useParams(); // id from URL e.g. /users/42
  // fetch user data with id...
}
```

---

## 6. Nested Routes

```jsx
// Parent route uses <Outlet /> to render child routes
<Routes>
  <Route path="/dashboard" element={<Dashboard />}>
    <Route path="profile" element={<Profile />} />
    <Route path="settings" element={<Settings />} />
  </Route>
</Routes>

// Dashboard.jsx
import { Outlet } from 'react-router-dom';
function Dashboard() {
  return (
    <div>
      <Sidebar />
      <Outlet /> {/* Child route renders here */}
    </div>
  );
}
```

---

## 7. Protected Routes (Auth Guard)

```jsx
function ProtectedRoute({ children }) {
  const isAuthenticated = !!localStorage.getItem('token');
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Usage
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

---

## 8. Query Parameters

```jsx
import { useSearchParams } from 'react-router-dom';

function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q'); // /search?q=react → 'react'

  return (
    <input
      value={query || ''}
      onChange={e => setSearchParams({ q: e.target.value })}
    />
  );
}
```

---

## 9. Lazy Loading Routes (Code Splitting)

```jsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Suspense>
  );
}
```

---

## 10. useLocation

```jsx
import { useLocation } from 'react-router-dom';

function Page() {
  const location = useLocation();
  // location.pathname → '/dashboard'
  // location.search → '?tab=overview'
  // location.state → passed via navigate('/page', { state: { from: '/home' } })
}
```

---

# Section 4: Performance & Optimization

## 1. When to Optimize (and when NOT to)

> Don't optimize prematurely. First, **measure** with React DevTools Profiler. Then optimize bottlenecks.

---

## 2. React DevTools Profiler

- Open React DevTools → **Profiler** tab
- Click Record → interact with the app → Stop
- View which components re-rendered, how long they took, and why

---

## 3. React.memo

Prevents re-render if **props haven't changed** (shallow comparison).

```jsx
const ExpensiveList = React.memo(function ExpensiveList({ items }) {
  return <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>;
});
```

---

## 4. useMemo + useCallback Together

```jsx
function Parent({ data }) {
  // Memoize computed value
  const sortedData = useMemo(() => [...data].sort((a, b) => a.name.localeCompare(b.name)), [data]);

  // Memoize callback so MemoChild doesn't re-render
  const handleSelect = useCallback((id) => {
    setSelected(id);
  }, []);

  return <MemoChild data={sortedData} onSelect={handleSelect} />;
}
```

---

## 5. Virtualization (Large Lists)

Render only the **visible items** in a long list instead of all items.

```jsx
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  );

  return (
    <FixedSizeList height={600} itemCount={items.length} itemSize={35} width="100%">
      {Row}
    </FixedSizeList>
  );
}
```

---

## 6. Code Splitting

Split your bundle into smaller chunks so users only download what they need.

```jsx
// Route-based splitting (most common)
const HomePage = lazy(() => import('./pages/Home'));

// Component-based splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));
```

---

## 7. Avoiding Memory Leaks

```jsx
useEffect(() => {
  let isMounted = true;

  fetch('/api/data')
    .then(res => res.json())
    .then(data => {
      if (isMounted) setData(data); // Don't set state if unmounted
    });

  return () => { isMounted = false; };
}, []);
```

---

## 8. Context Performance

Avoid putting frequently changing values in a single large context — every consumer re-renders.

```jsx
// ❌ Bad — everything re-renders on theme or user change
const AppContext = createContext({ theme, user, cart });

// ✅ Good — split into separate contexts
const ThemeContext = createContext(theme);
const UserContext = createContext(user);
const CartContext = createContext(cart);
```

---

## 9. Debounce vs Throttle

| | Debounce | Throttle |
|---|---|---|
| Fires | After user **stops** action for N ms | At most **once per N ms** |
| Use case | Search input, form validation | Scroll, resize events |

```jsx
// Debounce — fire 500ms after last keystroke
const debounced = useDebounce(inputValue, 500);

// Throttle — fire at most once every 200ms
function throttle(fn, limit) {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      fn(...args);
    }
  };
}
```

---

## 10. Image Optimization

```jsx
// Lazy load images natively
<img src="/photo.jpg" loading="lazy" alt="description" />

// Responsive images
<img
  srcSet="/img-300.webp 300w, /img-600.webp 600w"
  sizes="(max-width: 600px) 300px, 600px"
  src="/img-600.webp"
  alt="description"
/>
```

---

# Section 5: Next.js Basics

## 1. What is Next.js?

Next.js is a **React framework** that adds:
- **Server-Side Rendering (SSR)**
- **Static Site Generation (SSG)**
- **Incremental Static Regeneration (ISR)**
- **File-based routing**
- **API routes** (backend in same project)
- **Image optimization**

---

## 2. Rendering Strategies

| Strategy | When HTML generated | Use case |
|---|---|---|
| CSR (React default) | In browser | Dashboards, authenticated apps |
| SSR | On server per request | SEO pages with dynamic data |
| SSG | At build time | Blogs, docs, marketing pages |
| ISR | At build + revalidate | Frequently updated static pages |

---

## 3. SSR — getServerSideProps

Runs on the **server on every request**. Good for pages that need fresh, personalized data.

```jsx
export async function getServerSideProps(context) {
  const { params, query, req, res } = context;
  const data = await fetch(`https://api.example.com/posts/${params.id}`).then(r => r.json());

  return { props: { data } };
}

export default function Page({ data }) {
  return <div>{data.title}</div>;
}
```

---

## 4. SSG — getStaticProps

Runs **at build time**. Data is baked into the HTML. Use for pages that don't change often.

```jsx
export async function getStaticProps() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());

  return {
    props: { posts },
    revalidate: 60, // ISR — regenerate every 60 seconds
  };
}
```

---

## 5. ISR — Incremental Static Regeneration

Best of SSG + SSR: pages are **static by default** but get **regenerated in the background** at a set interval.

```jsx
export async function getStaticProps() {
  const data = await fetchData();
  return {
    props: { data },
    revalidate: 30, // Page will be regenerated at most every 30 seconds
  };
}
```

---

## 6. Dynamic Routes with getStaticPaths

For SSG with dynamic paths, tell Next.js which paths to pre-render.

```jsx
// pages/posts/[id].js

export async function getStaticPaths() {
  const posts = await fetchAllPosts();
  const paths = posts.map(post => ({ params: { id: String(post.id) } }));

  return {
    paths,
    fallback: false,      // 404 for ungenerated paths
    // fallback: true     // Show loading state, then generate
    // fallback: 'blocking' // SSR for new paths, then cache
  };
}

export async function getStaticProps({ params }) {
  const post = await fetchPost(params.id);
  return { props: { post } };
}
```

---

## 7. API Routes

Create **backend API endpoints** inside `pages/api/`. No extra server needed.

```jsx
// pages/api/hello.js
export default function handler(req, res) {
  if (req.method === 'GET') {
    res.status(200).json({ message: 'Hello World' });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}

// Dynamic: pages/api/users/[id].js
export default function handler(req, res) {
  const { id } = req.query;
  res.json({ userId: id });
}
```

---

## 8. next/link and next/image

```jsx
import Link from 'next/link';
import Image from 'next/image';

// Link — client-side navigation with prefetching
<Link href="/about">About</Link>

// Image — automatic optimization (resize, WebP, lazy load)
<Image
  src="/profile.jpg"
  width={300}
  height={300}
  alt="Profile"
  priority // skip lazy load for above-the-fold images
/>
```

---

## 9. Environment Variables

```bash
# .env.local
DATABASE_URL=postgres://...          # Server only
NEXT_PUBLIC_API_URL=https://api.com  # Client + Server (prefix with NEXT_PUBLIC_)
```

```jsx
// Server-side
const dbUrl = process.env.DATABASE_URL;

// Client-side (only NEXT_PUBLIC_ prefix works)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

---

## 10. Custom _app.js and _document.js

```jsx
// pages/_app.js — Wraps all pages, persists layout/state
import '../styles/globals.css';

export default function MyApp({ Component, pageProps }) {
  return (
    <ThemeProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </ThemeProvider>
  );
}

// pages/_document.js — Custom HTML shell (SSR only)
import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

---

## 11. Redirects and Rewrites

```js
// next.config.js
module.exports = {
  async redirects() {
    return [
      { source: '/old-page', destination: '/new-page', permanent: true },
    ];
  },
  async rewrites() {
    return [
      { source: '/api/:path*', destination: 'https://external-api.com/:path*' },
    ];
  },
};
```

---

## 12. next/head for SEO

```jsx
import Head from 'next/head';

export default function Page() {
  return (
    <>
      <Head>
        <title>My Page Title</title>
        <meta name="description" content="Page description for SEO" />
        <meta property="og:title" content="My Page" />
      </Head>
      <main>Content...</main>
    </>
  );
}
```

---

# Section 6: Advanced Next.js

## 1. App Router vs Pages Router (Next.js 13+)

| | Pages Router (`/pages`) | App Router (`/app`) |
|---|---|---|
| Introduced | Next.js original | Next.js 13 |
| Components | Client by default | Server by default |
| Data fetching | `getServerSideProps`, `getStaticProps` | `async` server components |
| Layouts | `_app.js` | Nested `layout.js` files |
| Streaming | ❌ | ✅ |

---

## 2. Server vs Client Components (App Router)

```jsx
// app/page.js — Server Component (default)
// Can use async/await directly, no hooks allowed
async function Page() {
  const data = await fetch('https://api.example.com/data').then(r => r.json());
  return <div>{data.title}</div>;
}

// Client Component — must add 'use client' directive
'use client';
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

**Rule of thumb:**
- Use **Server Components** by default (better performance, less JS sent to browser)
- Switch to **Client Components** only when you need: hooks, event handlers, browser APIs

---

## 3. Layouts in App Router

```
app/
├── layout.js          ← Root layout (wraps everything)
├── page.js            ← Home page
└── dashboard/
    ├── layout.js      ← Dashboard layout (wraps dashboard pages)
    └── page.js        ← /dashboard page
```

```jsx
// app/layout.js
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  );
}
```

---

## 4. Middleware

Runs **before every request** — use for auth, redirects, A/B testing, logging.

```tsx
// middleware.ts (at project root)
import { NextResponse } from 'next/server';

export function middleware(req) {
  const token = req.cookies.get('auth-token');

  if (!token && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'], // Apply only to matched paths
};
```

---

## 5. Streaming with Suspense (App Router)

Stream parts of the page progressively instead of waiting for all data.

```jsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<p>Loading chart...</p>}>
        <SlowChart /> {/* Streams in when ready */}
      </Suspense>
    </div>
  );
}
```

---

## 6. Authentication Pattern in Next.js

**Common approach — JWT + httpOnly cookies:**

```jsx
// pages/api/login.js
export default async function handler(req, res) {
  const { email, password } = req.body;
  const user = await validateUser(email, password);
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });

  const token = generateJWT(user);
  res.setHeader('Set-Cookie', `token=${token}; HttpOnly; Path=/; SameSite=Strict`);
  res.json({ success: true });
}

// middleware.ts — protect routes
const token = req.cookies.get('token');
if (!token) return NextResponse.redirect('/login');
```

**Alternative:** Use **next-auth** library for OAuth, JWT, and session management.

---

## 7. Internationalization (i18n)

```js
// next.config.js
module.exports = {
  i18n: {
    locales: ['en', 'fr', 'de'],
    defaultLocale: 'en',
  },
};

// In component
import { useRouter } from 'next/router';
const { locale } = useRouter(); // 'en', 'fr', etc.
```

---

# Section 7: State Management

## 1. Choosing the Right Tool

| Scenario | Best Tool |
|---|---|
| Local UI state | `useState` / `useReducer` |
| Shared state across a few components | Context API |
| Complex global state | Redux Toolkit |
| Server/async data | React Query / SWR |
| Lightweight global state | Zustand |

---

## 2. Context API (Full Pattern)

```jsx
// 1. Create Context + Provider
const CartContext = React.createContext(null);

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);

  const addItem = (item) => setCart(prev => [...prev, item]);
  const removeItem = (id) => setCart(prev => prev.filter(i => i.id !== id));

  return (
    <CartContext.Provider value={{ cart, addItem, removeItem }}>
      {children}
    </CartContext.Provider>
  );
}

// 2. Custom hook for cleaner usage
export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
}

// 3. Use in component
function ProductCard({ product }) {
  const { addItem } = useCart();
  return <button onClick={() => addItem(product)}>Add to Cart</button>;
}
```

---

## 3. Redux Toolkit (Modern Redux)

```jsx
// store/counterSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async action
export const fetchUsers = createAsyncThunk('users/fetch', async () => {
  const res = await fetch('/api/users');
  return res.json();
});

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0, users: [], loading: false },
  reducers: {
    increment: state => { state.value += 1; },
    decrement: state => { state.value -= 1; },
  },
  extraReducers: builder => {
    builder
      .addCase(fetchUsers.pending, state => { state.loading = true; })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.users = action.payload;
      });
  },
});

export const { increment, decrement } = counterSlice.actions;
export default counterSlice.reducer;

// store/store.js
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: { counter: counterReducer },
});

// In component
import { useSelector, useDispatch } from 'react-redux';
const count = useSelector(state => state.counter.value);
const dispatch = useDispatch();
<button onClick={() => dispatch(increment())}>+</button>
```

---

## 4. Zustand (Lightweight Alternative)

```jsx
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set(state => ({ count: state.count + 1 })),
  reset: () => set({ count: 0 }),
}));

// In component — no Provider needed!
function Counter() {
  const { count, increment } = useStore();
  return <button onClick={increment}>{count}</button>;
}
```

---

## 5. React Query (Server State)

```jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function Users() {
  // Fetch with caching, background refresh, error handling
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
  });

  // Mutation with optimistic update
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: (newUser) => fetch('/api/users', { method: 'POST', body: JSON.stringify(newUser) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

---

## 6. Redux Persist (Persisting State)

```jsx
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = { key: 'root', storage };
const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({ reducer: persistedReducer });
export const persistor = persistStore(store);

// Wrap app
<PersistGate loading={null} persistor={persistor}>
  <App />
</PersistGate>
```

---

# Section 8: TypeScript with React

## 1. Typing Props

```tsx
// Interface for props
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean; // optional prop
  children?: React.ReactNode; // anything React can render
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
}
```

---

## 2. Typing useState

```tsx
const [count, setCount] = useState<number>(0);
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);
```

---

## 3. Typing useRef

```tsx
const inputRef = useRef<HTMLInputElement>(null);
// inputRef.current is HTMLInputElement | null

const valueRef = useRef<number>(0); // mutable value, not null
```

---

## 4. Typing Events

```tsx
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget);
};
```

---

## 5. Typing useReducer

```tsx
type State = { count: number; loading: boolean };
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setLoading'; payload: boolean };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + 1 };
    case 'setLoading': return { ...state, loading: action.payload };
    default: return state;
  }
}
```

---

## 6. Generic Components

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map((item, i) => <li key={i}>{renderItem(item)}</li>)}</ul>;
}

// Usage
<List items={users} renderItem={(u) => <span>{u.name}</span>} />
```

---

# Section 9: Practical Patterns

## 1. Compound Components

Components that work together sharing implicit state.

```jsx
function Tabs({ children }) {
  const [activeTab, setActiveTab] = useState(0);
  return React.Children.map(children, (child, index) =>
    React.cloneElement(child, { isActive: index === activeTab, onSelect: () => setActiveTab(index) })
  );
}
```

---

## 2. Render Props Pattern

```jsx
function MouseTracker({ render }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  return (
    <div onMouseMove={e => setPos({ x: e.clientX, y: e.clientY })}>
      {render(pos)}
    </div>
  );
}

// Usage
<MouseTracker render={({ x, y }) => <p>{x}, {y}</p>} />
```

---

## 3. Skeleton Loader Pattern

```jsx
function UserCard({ isLoading, user }) {
  if (isLoading) {
    return (
      <div className="skeleton">
        <div className="skeleton-avatar" />
        <div className="skeleton-text" />
      </div>
    );
  }
  return <div>{user.name}</div>;
}
```

---

## 4. Pagination

```jsx
function Pagination({ total, pageSize, currentPage, onPageChange }) {
  const pages = Math.ceil(total / pageSize);
  return (
    <div>
      <button onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 1}>
        Prev
      </button>
      {Array.from({ length: pages }, (_, i) => (
        <button key={i + 1} onClick={() => onPageChange(i + 1)}
          className={currentPage === i + 1 ? 'active' : ''}>
          {i + 1}
        </button>
      ))}
      <button onClick={() => onPageChange(currentPage + 1)} disabled={currentPage === pages}>
        Next
      </button>
    </div>
  );
}
```

---

## 5. Infinite Scroll with Intersection Observer

```jsx
function useInfiniteScroll(callback) {
  const observerRef = useRef();

  const lastItemRef = useCallback(node => {
    if (observerRef.current) observerRef.current.disconnect();
    observerRef.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) callback();
    });
    if (node) observerRef.current.observe(node);
  }, [callback]);

  return lastItemRef;
}
```

---

## 6. Dark Mode Toggle

```jsx
function useTheme() {
  const [theme, setTheme] = useState(() =>
    localStorage.getItem('theme') || 'light'
  );

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggle = () => setTheme(t => t === 'light' ? 'dark' : 'light');
  return { theme, toggle };
}
```

---

# Section 10: Common Interview Patterns & Tricky Questions

## 1. Why does my useEffect run twice in development?

React 18 + Strict Mode **intentionally mounts → unmounts → remounts** components in development to help detect side effects that don't clean up properly. This only happens in dev, not production.

---

## 2. Stale Closure in useEffect

```jsx
// ❌ Bug — count is always 0 inside the effect (stale closure)
useEffect(() => {
  const id = setInterval(() => {
    console.log(count); // Always 0!
    setCount(count + 1); // Adds 1 to stale 0 forever
  }, 1000);
  return () => clearInterval(id);
}, []); // Empty dep array = count captured at mount time

// ✅ Fix — use functional updater
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1); // Uses latest state
  }, 1000);
  return () => clearInterval(id);
}, []);
```

---

## 3. Object/Array in Dependency Array

```jsx
// ❌ Problem — new object created every render
const options = { color: 'red' }; // New reference each time!
useEffect(() => { /* runs every render */ }, [options]);

// ✅ Fix — memoize the object
const options = useMemo(() => ({ color: 'red' }), []);
useEffect(() => { /* runs once */ }, [options]);
```

---

## 4. Batching in React 18

React 18 automatically batches **all** state updates (even in setTimeout, fetch callbacks, etc.) into a single re-render.

```jsx
// React 17: 2 re-renders
// React 18: 1 re-render (batched)
setTimeout(() => {
  setCount(c => c + 1);
  setName('John');
}, 1000);
```

---

## 5. useTransition (React 18)

Mark state updates as non-urgent so they don't block UI interactions.

```jsx
const [isPending, startTransition] = useTransition();

function handleSearch(query) {
  // Urgent: update input immediately
  setInputValue(query);

  // Non-urgent: can be interrupted
  startTransition(() => {
    setSearchResults(filterItems(query));
  });
}
```

---

## 6. Key Trick for Resetting State

Changing the `key` prop **unmounts and remounts** the component, resetting all internal state.

```jsx
function Parent() {
  const [userId, setUserId] = useState(1);

  return (
    // Profile fully resets when userId changes
    <Profile key={userId} userId={userId} />
  );
}
```

---

## 7. Difference: null vs undefined vs false in JSX

```jsx
{null}       // Renders nothing
{undefined}  // Renders nothing
{false}      // Renders nothing
{0}          // ⚠️ Renders "0" — common bug!

// Fix for 0 issue:
{count > 0 && <Badge count={count} />}  // Use explicit boolean
{!!count && <Badge count={count} />}    // Or double negation
```

---

## 8. Common Performance Checklist

- [ ] Are expensive calculations memoized with `useMemo`?
- [ ] Are callbacks memoized with `useCallback` when passed to `React.memo` children?
- [ ] Are large lists virtualized?
- [ ] Are routes code-split with `React.lazy`?
- [ ] Are images optimized (WebP, lazy load, proper sizing)?
- [ ] Are contexts split to avoid unnecessary re-renders?
- [ ] Are API calls debounced/throttled where appropriate?
- [ ] Are effects cleaned up to prevent memory leaks?

---

## 9. Quick Revision: Hook Summary Table

| Hook | Purpose |
|---|---|
| `useState` | Local state |
| `useEffect` | Side effects (fetch, subscriptions, DOM) |
| `useRef` | DOM access, mutable values without re-render |
| `useMemo` | Memoize computed value |
| `useCallback` | Memoize function |
| `useReducer` | Complex state with reducer pattern |
| `useContext` | Consume context without prop drilling |
| `useLayoutEffect` | Sync DOM measurements before paint |
| `useImperativeHandle` | Expose child methods to parent via ref |
| `useTransition` | Mark non-urgent state updates (React 18) |
| `useDeferredValue` | Defer re-rendering non-urgent values (React 18) |

---

## 10. Quick Revision: Next.js Data Fetching

| Method | Runs | Use when |
|---|---|---|
| `getStaticProps` | Build time | Data doesn't change often |
| `getServerSideProps` | Every request | Fresh data, user-specific |
| `getStaticPaths` | Build time | Define dynamic SSG paths |
| ISR (`revalidate`) | Build + interval | Mostly static, updates periodically |
| Server Components | Per request | App Router default |
| `useEffect` fetch | Client side | After page load, interactive |

---




# ⚡ React + Next.js Performance Optimization — Interview Notes

> 📌 **How to use:** Read the explanation, study the example, then close and recall it. These notes are designed to help you crack frontend performance interviews.

---

## 🚀 Section 1: Core React Performance

---

### 1. `React.memo` — Prevent Unnecessary Re-renders

**What it is:** A Higher-Order Component (HOC) that wraps a component and prevents it from re-rendering if its **props haven't changed**.

**When to use:** Pure/display components that receive the same props often (e.g., list items, cards).

```jsx
const UserCard = React.memo(({ name, age }) => {
  console.log("Rendered!");
  return <div>{name} - {age}</div>;
});

// Parent re-renders → UserCard does NOT re-render if name & age are the same
```

> ⚠️ Avoid using it everywhere. It adds overhead for comparison. Use only when re-render is actually expensive.

---

### 2. `useMemo` vs `useCallback`

| Hook | Caches | Use When |
|------|--------|----------|
| `useMemo` | **Value/result** of a function | Expensive calculations |
| `useCallback` | **The function itself** | Passing callbacks to memoized child components |

```jsx
// useMemo — caches computed value
const sortedList = useMemo(() => {
  return items.sort((a, b) => a.price - b.price);
}, [items]); // Only recalculates when `items` changes

// useCallback — caches the function reference
const handleClick = useCallback(() => {
  console.log("clicked", id);
}, [id]); // New function only if `id` changes

// Without useCallback, handleClick gets a new reference on every render
// → causes child component (even React.memo'd) to re-render
```

---

### 3. What Causes Re-renders?

Three main triggers:
1. **State change** — `setState` is called
2. **Props change** — parent passes new value
3. **Context change** — any consumer re-renders when context value changes

```jsx
const [count, setCount] = useState(0);

// This causes ALL children to re-render (even those not using count)
// unless they are wrapped in React.memo
```

> 💡 **Interview tip:** Also mention that calling `setState` with the same value skips re-render in React 18 (Object.is comparison).

---

### 4. Reconciliation — React's Diffing Algorithm

**What it is:** React's process of comparing the **old virtual DOM** with the **new virtual DOM** and updating only the changed parts in the real DOM.

**Rules:**
- Two elements of different types → destroy and rebuild entire subtree
- Same type → update attributes/props only
- Lists → use `key` prop to match old and new elements

```jsx
// Without key — React re-renders all list items on change
{items.map(item => <li>{item.name}</li>)}

// With key — React knows exactly which item changed
{items.map(item => <li key={item.id}>{item.name}</li>)}
```

---

### 5. React Fiber — The Rendering Engine

**What it is:** A complete rewrite of React's core algorithm (introduced in React 16). It breaks rendering work into **small units (fibers)** that can be paused, resumed, or aborted.

**Before Fiber:** Rendering was synchronous and couldn't be interrupted → UI could freeze.

**After Fiber:** Rendering is async/incremental → React can yield to the browser between frames.

```
Old React:  [Render entire tree at once] → Browser blocked → Janky UI
React Fiber: [Render chunk] → [Yield to browser] → [Continue render] → Smooth UI
```

> 💡 Fiber is what enables **Concurrent Mode**, `useTransition`, `Suspense`, etc.

---

## ⚡ Section 2: Rendering Optimization

---

### 1. Virtualization for Large Lists

**Problem:** Rendering 10,000 rows = 10,000 DOM nodes → slow scroll, high memory.

**Solution:** Only render what's **visible in the viewport**.

```jsx
import { FixedSizeList } from 'react-window';

const Row = ({ index, style }) => (
  <div style={style}>Row {index}</div>
);

<FixedSizeList
  height={500}        // Visible container height
  itemCount={10000}   // Total items
  itemSize={35}       // Each row height
  width="100%"
>
  {Row}
</FixedSizeList>

// Only ~15 rows are in the DOM at any time, not 10,000!
```

---

### 2. Lazy Loading Components

**What it is:** Load a component's JS bundle **only when it's needed**, not on initial page load.

```jsx
import React, { lazy, Suspense } from 'react';

// ❌ Normal import — always loaded upfront
// import HeavyChart from './HeavyChart';

// ✅ Lazy import — loaded only when rendered
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<div>Loading chart...</div>}>
      <HeavyChart />
    </Suspense>
  );
}
```

---

### 3. Code Splitting

**What it is:** Break one large JS bundle into **smaller chunks** loaded on demand.

```
Without splitting:  bundle.js = 2MB → User downloads all 2MB upfront

With splitting:
  main.js      = 300KB (loads first)
  dashboard.js = 500KB (loads when user visits /dashboard)
  admin.js     = 700KB (loads only for admin users)
```

In Next.js, **every page is automatically code split**. In React, use `React.lazy` + dynamic `import()`.

---

### 4. `Suspense` — Async UI Placeholder

**What it is:** Displays a fallback UI while a lazy component or async data is loading.

```jsx
<Suspense fallback={<Spinner />}>
  <UserProfile />   {/* Might fetch data or be lazy loaded */}
</Suspense>
```

> In React 18, Suspense also works with data fetching libraries (React Query, Relay).

---

### 5. Why `key` Prop Matters

```jsx
// ❌ Using index as key — causes bugs when list reorders/deletes
{users.map((user, index) => <User key={index} user={user} />)}

// ✅ Using stable unique ID
{users.map(user => <User key={user.id} user={user} />)}
```

With `index` as key: if item at index 0 is deleted, React thinks item at index 0 just changed (not deleted) → wrong component gets updated → bugs.

---

### 6. Avoid Inline Functions in JSX

```jsx
// ❌ Bad — new function reference created on every render
<Button onClick={() => handleDelete(id)} />

// ✅ Good — stable reference with useCallback
const onDelete = useCallback(() => handleDelete(id), [id]);
<Button onClick={onDelete} />
```

Even if `Button` is wrapped in `React.memo`, the inline function gives it a new prop reference each time → memo is bypassed → re-render happens.

---

## ⚡ Section 3: React 18 Advanced Features

---

### 1. Concurrent Rendering

React 18 can **interrupt, pause, and resume** rendering. It prioritizes user interactions (typing, clicking) over less critical renders.

```
Old: [Heavy render running] → User clicks → User waits (blocked)
React 18: [Heavy render running] → User clicks → Click handled immediately → Render resumes
```

---

### 2. `useTransition` — Mark Low-Priority Updates

```jsx
const [isPending, startTransition] = useTransition();

function handleSearch(query) {
  // Urgent: update the input immediately
  setInputValue(query);

  // Non-urgent: filtering a large list can wait
  startTransition(() => {
    setFilteredResults(heavyFilter(data, query));
  });
}

// Show spinner while transition is pending
{isPending && <Spinner />}
```

> 💡 Use when you want the input to feel instant, but a slower result can lag slightly.

---

### 3. `useDeferredValue` — Defer a Non-Critical Value

```jsx
const [query, setQuery] = useState('');
const deferredQuery = useDeferredValue(query);

// query updates immediately (input is responsive)
// deferredQuery updates with a slight delay (search results can lag)

const results = useMemo(
  () => search(data, deferredQuery),
  [deferredQuery]
);
```

> **Difference from useTransition:** `useTransition` wraps a setter. `useDeferredValue` wraps a value (useful when you don't control the state setter).

---

## ⚡ Section 4: State & Hooks Optimization

---

### 1. Avoid Large State Objects

```jsx
// ❌ Bad — any field change re-renders everything using this state
const [form, setForm] = useState({ name: '', email: '', address: '', phone: '' });

// ✅ Better — split into separate state or use useReducer
const [name, setName] = useState('');
const [email, setEmail] = useState('');
```

---

### 2. Batching — Group Multiple Updates

**React 18** automatically batches state updates even in async code (timeouts, promises).

```jsx
// React 18 — both updates are batched → only ONE re-render
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Before React 18: 2 renders. React 18: 1 render ✅
}, 1000);
```

---

### 3. `useRef` — Mutable Value Without Re-render

```jsx
// Use case 1: Store a value that shouldn't trigger re-render
const renderCount = useRef(0);
renderCount.current += 1; // No re-render!

// Use case 2: Access DOM element
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus(); // Direct DOM access
```

---

### 4. Controlled vs Uncontrolled Components

```jsx
// Controlled — state drives the value (React is in control)
const [value, setValue] = useState('');
<input value={value} onChange={e => setValue(e.target.value)} />

// Uncontrolled — DOM drives the value (ref to read on submit)
const ref = useRef();
<input ref={ref} defaultValue="Hello" />
// Read: ref.current.value on form submit
```

**When to use uncontrolled:** Large forms where you only need the value on submit (avoids re-render on every keystroke).

---

### 5. Avoid Unnecessary `useEffect`

```jsx
// ❌ Unnecessary effect — this is just a derived value!
const [doubled, setDoubled] = useState(0);
useEffect(() => {
  setDoubled(count * 2); // Extra render cycle!
}, [count]);

// ✅ Just compute it during render
const doubled = count * 2; // No effect needed
```

> Rule of thumb: If you can compute a value from existing state/props, don't put it in state or useEffect.

---

## ⚡ Section 5: Next.js Optimization

---

### 1. SSR vs SSG vs ISR

| Mode | When HTML is Generated | Best For |
|------|----------------------|----------|
| **SSR** (Server-Side Rendering) | On every request | Dynamic data per user (dashboards, auth pages) |
| **SSG** (Static Site Generation) | At build time | Rarely changing content (blogs, docs) |
| **ISR** (Incremental Static Regeneration) | At build, then updated in background | Semi-dynamic (product pages, news) |

```jsx
// SSG
export async function getStaticProps() {
  const data = await fetchData();
  return { props: { data } };
}

// SSR
export async function getServerSideProps(context) {
  const user = await getUser(context.req);
  return { props: { user } };
}

// ISR — regenerate every 60 seconds
export async function getStaticProps() {
  const data = await fetchData();
  return { props: { data }, revalidate: 60 };
}
```

---

### 2. `next/image` — Automatic Image Optimization

```jsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  width={1200}
  height={600}
  alt="Hero"
  priority          // Preload LCP image
  placeholder="blur" // Show blur while loading
/>
```

**What it does automatically:** Resizes to correct size, converts to WebP/AVIF, lazy loads by default, prevents CLS with fixed dimensions.

---

### 3. `next/dynamic` — Lazy Load in Next.js

```jsx
import dynamic from 'next/dynamic';

const HeavyMap = dynamic(() => import('./HeavyMap'), {
  loading: () => <p>Loading map...</p>,
  ssr: false, // Don't render on server (useful for browser-only libs)
});
```

---

### 4. App Router vs Pages Router

| Feature | Pages Router | App Router (Next.js 13+) |
|---------|-------------|--------------------------|
| Server Components | ❌ | ✅ |
| Streaming | ❌ | ✅ |
| Nested Layouts | Manual | Built-in |
| Data Fetching | `getServerSideProps` | `async/await` in component |

---

### 5. Server Components (RSC)

**What they are:** Components that run **only on the server**. They send HTML to the client — no JS bundle shipped.

```jsx
// app/page.tsx — This is a Server Component by default
async function ProductPage() {
  const product = await db.getProduct(1); // DB call on server!
  return <div>{product.name}</div>;
  // Zero JS for this component is sent to client ✅
}

// 'use client' — opt into client-side JS
'use client';
function AddToCartButton() {
  const [added, setAdded] = useState(false);
  return <button onClick={() => setAdded(true)}>Add to Cart</button>;
}
```

---

### 6. Streaming SSR

Instead of waiting for the entire page to render on the server, **send HTML in chunks** as they become ready.

```
Without streaming: [Server renders ALL] → [Sends all HTML] → [Browser shows page]
With streaming:    [Send header] → [Send nav] → [Send hero] → [Send data-heavy section]
                   → Browser progressively shows content!
```

In Next.js App Router, `<Suspense>` boundaries become streaming boundaries automatically.

---

### 7. Edge Rendering

**What it is:** Run server code at **CDN edge nodes** closest to the user (not a central server).

```jsx
// pages/api/hello.js
export const config = { runtime: 'edge' }; // Runs at Vercel Edge

export default function handler(req) {
  return new Response('Hello from the edge!');
}
```

> Mumbai user → Edge node in Mumbai (~5ms) vs Central server in US (~200ms).

---

## ⚡ Section 6: Network & API Optimization

---

### 1. Optimize API Calls

- **Caching:** Don't re-fetch data that hasn't changed
- **Pagination:** Fetch 20 items at a time, not 1000
- **Deduplication:** If 3 components request same data simultaneously, make only 1 API call

---

### 2. React Query / SWR

```jsx
import { useQuery } from '@tanstack/react-query';

function Profile({ userId }) {
  const { data, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
    staleTime: 5 * 60 * 1000, // Data is "fresh" for 5 minutes
  });

  if (isLoading) return <Spinner />;
  return <div>{data.name}</div>;
}
// Bonus: Automatically deduplicates, caches, and refetches on focus!
```

---

### 3. Stale-While-Revalidate (SWR)

**Strategy:** Show **cached (stale) data immediately**, then fetch fresh data in the background and update.

```
User visits page → Show cached data (instant!) → Fetch fresh data → Update silently
```

> Result: Page feels instant, but data is always eventually fresh. Used by SWR library and HTTP `Cache-Control` header.

---

## ⚡ Section 7: Browser Performance Metrics

---

### 1. Critical Rendering Path

Steps the browser takes to show a page:

```
1. Download HTML
2. Build DOM tree
3. Download + parse CSS → CSSOM
4. DOM + CSSOM = Render Tree
5. Layout (calculate positions)
6. Paint (draw pixels)
```

**Optimization:** Minimize render-blocking resources (CSS in `<head>`, defer JS).

---

### 2. CLS — Cumulative Layout Shift

**What it is:** Measures how much elements **jump around** during page load (e.g., image loads and pushes text down).

**Score:** 0 is perfect, < 0.1 is good.

```jsx
// ❌ Bad — image has no size, causes layout shift
<img src="banner.jpg" />

// ✅ Good — reserve space before image loads
<img src="banner.jpg" width="1200" height="600" />
// Or use next/image which handles this automatically
```

---

### 3. LCP — Largest Contentful Paint

**What it is:** Time until the **largest visible element** (hero image, headline) is fully rendered.

**Target:** Under 2.5 seconds.

```jsx
// Optimize LCP image with priority preload
<Image src="/hero.jpg" priority />
```

---

### 4. Preload vs Prefetch

```html
<!-- Preload: "I need this VERY SOON" — loads immediately with high priority -->
<link rel="preload" href="/fonts/inter.woff2" as="font" />

<!-- Prefetch: "I might need this later" — loads in browser idle time -->
<link rel="prefetch" href="/about-page.js" />
```

> In Next.js, `<Link>` automatically prefetches the linked page when it enters the viewport.

---

## ⚡ Section 8: Memory & DOM Optimization

---

### 1. Memory Leaks in React

Common causes and fixes:

```jsx
// ❌ Memory leak — setInterval not cleared
useEffect(() => {
  const id = setInterval(() => console.log('tick'), 1000);
  // Component unmounts → interval keeps running!
}, []);

// ✅ Clean up on unmount
useEffect(() => {
  const id = setInterval(() => console.log('tick'), 1000);
  return () => clearInterval(id); // Cleanup!
}, []);

// ❌ Memory leak — event listener not removed
useEffect(() => {
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler); // ✅ Fix
}, []);
```

---

### 2. Event Delegation

Instead of attaching listeners to 1000 list items, attach **one listener to the parent**.

```jsx
// ❌ 1000 event listeners
{items.map(item => (
  <li key={item.id} onClick={() => handleClick(item.id)}>{item.name}</li>
))}

// ✅ One event listener on parent (native JS pattern)
<ul onClick={(e) => {
  const id = e.target.dataset.id;
  if (id) handleClick(id);
}}>
  {items.map(item => (
    <li key={item.id} data-id={item.id}>{item.name}</li>
  ))}
</ul>
```

---

### 3. Reduce DOM Nodes

```jsx
// ❌ Extra wrapper div adds unnecessary node
function List() {
  return (
    <div>
      <Item />
      <Item />
    </div>
  );
}

// ✅ Use Fragment — renders no extra DOM node
function List() {
  return (
    <>
      <Item />
      <Item />
    </>
  );
}
```

> Each extra DOM node costs memory and slows down traversal. Fragments help keep the tree lean.

---

## ⚡ Section 9: Build & Bundle Optimization

---

### 1. Tree Shaking

**What it is:** Remove unused code from the final bundle during build.

```jsx
// ❌ Imports entire lodash library (~70KB)
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Imports only debounce (~2KB) — tree shakeable
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

> Works automatically with ES modules (`import/export`). Doesn't work with CommonJS (`require`).

---

### 2. Bundle Analyzer

Visualize what's inside your JS bundle.

```bash
# Next.js
npm install @next/bundle-analyzer

# Run
ANALYZE=true next build
# Opens a visual treemap showing every module's size
```

> Use it to spot: accidentally imported large libraries, duplicate packages, unoptimized images.

---

### 3. Minification & Compression

```
Source file:  const myVariable = "hello world"; → 30 chars
Minified:     const a="hello world";             → 20 chars (variable renamed)
Gzip:         [binary compressed]                → ~10 chars
```

- **Minification:** Done by bundler (Webpack, Turbopack) at build time
- **Gzip/Brotli:** Done by the server when sending files. Brotli is ~20% smaller than Gzip.

> Enable in Next.js: `compress: true` in `next.config.js` (enabled by default).

---

## ⚡ Section 10: Misc High-Impact Concepts

---

### 1. Debouncing vs Throttling

```jsx
// Debouncing — wait until user STOPS typing, then call
// Use for: search inputs, form validation
const debouncedSearch = useMemo(
  () => debounce((query) => fetchResults(query), 300),
  []
);
<input onChange={e => debouncedSearch(e.target.value)} />
// User types "react" fast → only 1 API call after they stop

// Throttling — call at MOST once every X milliseconds
// Use for: scroll events, resize handlers, mouse move
const throttledScroll = useMemo(
  () => throttle(() => updateScrollPosition(), 100),
  []
);
window.addEventListener('scroll', throttledScroll);
// Scroll fires 100 times/sec → throttle limits to 10 times/sec
```

---

### 2. CDN — Content Delivery Network

**What it is:** A network of servers distributed globally that serves your static assets (images, JS, CSS) from the **nearest location** to the user.

```
Without CDN: Mumbai user → Fetch JS from server in US → ~200ms latency
With CDN:    Mumbai user → Fetch JS from CDN node in Mumbai → ~10ms latency
```

Next.js on Vercel automatically uses a CDN for all static assets.

---

### 3. Avoid Prop Drilling

**Prop drilling:** Passing props through many layers just to reach a deeply nested component.

```jsx
// ❌ Prop drilling
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserAvatar user={user} /> {/* Only this needs it! */}
    </Sidebar>
  </Layout>
</App>

// ✅ Context API — provide at top, consume anywhere
const UserContext = createContext();

// Wrap top-level
<UserContext.Provider value={user}>
  <App />
</UserContext.Provider>

// Consume directly where needed
function UserAvatar() {
  const user = useContext(UserContext);
  return <img src={user.avatar} />;
}
```

> For complex global state (cart, auth, theme), prefer **Zustand** or **Redux Toolkit** over Context (Context can cause unnecessary re-renders when not memoized properly).

---

## 🎯 Quick Interview Cheat Sheet

| Question | 1-Line Answer |
|----------|---------------|
| What is React.memo? | HOC that skips re-render if props are same |
| useMemo vs useCallback? | useMemo = cached value, useCallback = cached function |
| What is Fiber? | Async rendering engine enabling interruptible work |
| What is reconciliation? | Diffing old vs new VDOM to minimize real DOM updates |
| SSR vs SSG vs ISR? | Runtime vs build-time vs incremental HTML generation |
| What is tree shaking? | Remove unused exports from final bundle |
| What is LCP? | Time to largest visible element — target < 2.5s |
| What is CLS? | Layout shift score — target < 0.1 |
| Debounce vs Throttle? | Debounce = wait for pause, Throttle = limit frequency |
| What are Server Components? | Components that run on server only — zero client JS |
| What is streaming SSR? | Send HTML progressively in chunks |
| How to prevent memory leaks? | Clean up effects: clear timers, remove listeners |

---




## Debouncing and throttling are common techniques to optimize performance by limiting how often a function can run.

# Debounce vs Throttle (Simple Examples)

---

## 🔹 Debounce (Wait until stop)

```javascript
function debounce(fn, delay) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
}

const sayHello = debounce(() => console.log("Hello"), 1000);

// Call multiple times quickly
sayHello();
sayHello();
sayHello();


🧠 Output:

Only one "Hello" will print after 1 second.

📌 Explanation:
Previous calls are cancelled
Only the last call executes



// Throttle (Limit execution)
function throttle(fn, limit) {
  let last = 0;
  return () => {
    let now = Date.now();
    if (now - last >= limit) {
      last = now;
      fn();
    }
  };
}

const sayHi = throttle(() => console.log("Hi"), 1000);

// Call repeatedly
setInterval(sayHi, 200);


🧠 Output:

"Hi" prints every 1 second (even though called every 200ms)

📌 Explanation:
Function runs at fixed intervals
Extra calls are ignored


| Feature   | Debounce       | Throttle           |
| --------- | -------------- | ------------------ |
| Execution | After stopping | At intervals       |
| Calls     | One (last)     | Multiple (limited) |
| Use Case  | Search input   | Scroll, resize     |









*Good luck with your interviews! Focus on understanding the **why** behind each concept, not just the syntax. Interviewers love candidates who can explain trade-offs.*