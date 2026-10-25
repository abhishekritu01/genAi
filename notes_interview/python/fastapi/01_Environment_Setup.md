# Chapter 1 — Python Environment Setup

> **Goal:** Have Python, a virtual environment, FastAPI and Uvicorn installed, a clean project folder, and a running development server — on Windows, macOS or Linux.

---

## 1.1 Install Python and Verify the Version

### What & why
FastAPI is a Python library, so you need Python first. Use **Python 3.12 or 3.13** (FastAPI supports 3.8+ officially for older versions, but modern features like `type X = ...` and better error messages make 3.12+ the sensible choice).

### Install

| OS | Recommended way |
|---|---|
| Windows | Download installer from python.org → ✅ tick **"Add python.exe to PATH"**. Or `winget install Python.Python.3.13` |
| macOS | `brew install python@3.13` (Homebrew) or python.org installer |
| Linux (Ubuntu/Debian) | `sudo apt update && sudo apt install python3 python3-venv python3-pip` |
| Any (pro option) | **`uv`** — a fast Rust-based tool that installs Python *and* manages venvs/deps (see 1.8) |

### Verify

```powershell
PS> python --version          # Python 3.13.x
PS> py --list                 # Windows launcher: lists all installed Pythons
PS> py -3.13 --version        # pick a specific version
```

```bash
$ python3 --version           # macOS/Linux usually use "python3"
$ which python3               # where is it installed?
```

💡 On Windows the command is usually `python` (or `py`); on macOS/Linux it is `python3`. Inside an *activated* venv, plain `python` works everywhere.

---

## 1.2 Virtual Environments (`venv`)

### Simple explanation
A **virtual environment** is a private folder that holds a copy of Python plus *only the packages for this project*. Project A can use FastAPI 0.110 and project B FastAPI 0.115 without conflict.

### Why it matters
- No "it works on my machine" problems from global packages.
- Reproducible installs (`requirements.txt` matches exactly what's in the venv).
- You never need `sudo pip install` (which can break your OS Python).

### Create and activate

| Step | Windows PowerShell | macOS / Linux |
|---|---|---|
| Create | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Check | `(Get-Command python).Source` | `which python` |
| Deactivate | `deactivate` | `deactivate` |
| Delete | `Remove-Item -Recurse -Force .venv` | `rm -rf .venv` |

After activation your prompt shows `(.venv)`.

```powershell
PS C:\code\todo> python -m venv .venv
PS C:\code\todo> .\.venv\Scripts\Activate.ps1
(.venv) PS C:\code\todo> python -c "import sys; print(sys.prefix)"
C:\code\todo\.venv
```

🐞 **PowerShell error: "running scripts is disabled on this system"**
```powershell
PS> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
(Allows local scripts like `Activate.ps1`; only needed once.) In cmd.exe use `.venv\Scripts\activate.bat` instead.

💡 Name it `.venv` — VS Code / PyCharm auto-detect it, and it's a common `.gitignore` entry.

---

## 1.3 Install FastAPI and Uvicorn

```bash
(.venv) $ python -m pip install --upgrade pip
(.venv) $ pip install "fastapi[standard]"
```

`fastapi[standard]` installs:

| Package | Role |
|---|---|
| `fastapi` | The framework |
| `uvicorn[standard]` | ASGI server that actually runs your app (with `uvloop`, `httptools` on Linux/macOS) |
| `fastapi-cli` | The `fastapi dev` / `fastapi run` commands |
| `pydantic` (v2) | Data validation |
| `httpx` | HTTP client (also used by `TestClient`) |
| `jinja2`, `python-multipart`, `email-validator` | Templates, form/file uploads, `EmailStr` |

Minimal alternative: `pip install fastapi uvicorn` (you then add `python-multipart` etc. yourself).

💡 Always quote `"fastapi[standard]"` — zsh treats `[ ]` as a glob pattern otherwise.

Verify:
```bash
(.venv) $ pip show fastapi
(.venv) $ python -c "import fastapi, pydantic; print(fastapi.__version__, pydantic.VERSION)"
```

---

## 1.4 Create a Project and First App

```
todo-api/
├── .venv/                 # virtual env (NOT committed)
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── __init__.py
├── .env                   # secrets (NOT committed)
├── .env.example           # template of required env vars (committed)
├── .gitignore
├── requirements.txt       # or pyproject.toml
└── README.md
```

**`app/main.py`**
```python
from fastapi import FastAPI

app = FastAPI(title="Todo API", version="0.1.0")   # 1. create the application object


@app.get("/")                                        # 2. register a GET route at "/"
def read_root():                                     # 3. the "path operation function"
    return {"message": "Hello, FastAPI!"}            # 4. dict -> JSON automatically
```

Line by line:
1. `FastAPI(...)` creates the ASGI app. `title`/`version` appear in the docs.
2. The decorator says: when an HTTP **GET** request hits `/`, call the function below.
3. Any name works; FastAPI uses the function's signature to know what inputs to read.
4. Returning a dict → FastAPI serializes to JSON with status 200.

**`.gitignore`**
```
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.coverage
htmlcov/
*.db
```

---

## 1.5 Run, Stop and Restart the Development Server

### Option A — FastAPI CLI (modern, recommended)
```bash
(.venv) $ fastapi dev app/main.py      # dev: auto-reload, binds 127.0.0.1:8000
(.venv) $ fastapi run app/main.py      # prod-style: no reload, binds 0.0.0.0:8000
```

### Option B — Uvicorn directly (classic, still everywhere)
```bash
(.venv) $ uvicorn app.main:app --reload --port 8000
#                 └──────┘ └─┘
#            module path   variable name of the FastAPI object
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Application startup complete.
```

| Action | How |
|---|---|
| Open the API | http://127.0.0.1:8000 → `{"message":"Hello, FastAPI!"}` |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |
| **Stop** | `Ctrl + C` in the terminal |
| **Restart** | With `--reload` it restarts automatically on file save; otherwise Ctrl+C then run again |
| Different port | `--port 8001` |
| Reachable from LAN / Docker | `--host 0.0.0.0` |

Test from the terminal:
```powershell
PS> Invoke-RestMethod http://127.0.0.1:8000/       # PowerShell
PS> curl.exe http://127.0.0.1:8000/                 # real curl on Windows 10+
```
```bash
$ curl http://127.0.0.1:8000/
{"message":"Hello, FastAPI!"}
```

⚠️ Never use `--reload` in production — it watches files and is slow/unsafe.

### Running from code (useful for debuggers)
```python
# app/main.py (bottom)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
```
`reload=True` requires the **import string** (`"app.main:app"`), not the object.

---

## 1.6 `requirements.txt` vs `pyproject.toml`

### `requirements.txt` (simple, universal)
```bash
(.venv) $ pip freeze > requirements.txt     # snapshot EVERYTHING installed (pinned)
(.venv) $ pip install -r requirements.txt   # recreate on another machine
```
Professional pattern — separate top-level deps from the lock:
```
# requirements.in       (what YOU asked for)
fastapi[standard]>=0.115
sqlalchemy>=2.0
alembic
psycopg[binary]
pydantic-settings
```
```bash
$ pip install pip-tools
$ pip-compile requirements.in -o requirements.txt   # generates fully pinned lock file
$ pip-sync requirements.txt                         # make venv exactly match
```
Dev-only tools go in `requirements-dev.txt` (`-r requirements.txt` + pytest, ruff, mypy).

### `pyproject.toml` (modern standard, PEP 621)
```toml
[project]
name = "todo-api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi[standard]>=0.115",
    "sqlalchemy>=2.0",
    "alembic>=1.13",
    "psycopg[binary]>=3.2",
    "pydantic-settings>=2.4",
]

[dependency-groups]          # PEP 735 (uv supports it); or [project.optional-dependencies] dev = [...]
dev = ["pytest>=8", "pytest-cov", "ruff", "mypy", "httpx"]

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

| | requirements.txt | pyproject.toml |
|---|---|---|
| Simplicity | ✅ simplest | needs a tool that reads it |
| Metadata, tool config in one file | ❌ | ✅ |
| Lock file | is itself the lock (when pinned) | separate lock (`uv.lock`, `poetry.lock`) |
| Used by | pip, Docker, everyone | uv, Poetry, PDM, Hatch, pip (`pip install .`) |

---

## 1.7 Configure the Editor (VS Code / PyCharm)
- **VS Code:** `Ctrl+Shift+P` → *Python: Select Interpreter* → pick `.venv`. Install extensions: *Python*, *Pylance*, *Ruff*.
- **PyCharm:** Settings → Project → Python Interpreter → Add → *Existing* → `.venv`.
- Debug config (VS Code `launch.json`):
```json
{
  "name": "FastAPI",
  "type": "debugpy",
  "request": "launch",
  "module": "uvicorn",
  "args": ["app.main:app", "--reload"],
  "jinja": true
}
```

---

## 1.8 🟡 Professional Option — `uv`

`uv` (by Astral) replaces `pip`, `venv`, `pip-tools`, and `pyenv` — 10–100× faster.

```powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```
```bash
$ uv init todo-api && cd todo-api      # creates pyproject.toml
$ uv python install 3.13               # installs Python itself
$ uv add "fastapi[standard]" sqlalchemy alembic
$ uv add --dev pytest ruff mypy
$ uv run fastapi dev app/main.py       # runs inside the project venv automatically
$ uv sync                              # install exactly what uv.lock says
```

---

## 1.9 🐞 Troubleshooting Common Errors

| Error | Cause | Fix |
|---|---|---|
| `'python' is not recognized` (Windows) | Not on PATH | Re-run installer with "Add to PATH", or use `py` |
| Windows opens Microsoft Store when typing `python` | App execution alias | Settings → Apps → Advanced app settings → App execution aliases → turn off python.exe aliases |
| `Activate.ps1 cannot be loaded` | Execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: No module named 'fastapi'` | venv not activated / wrong interpreter | Activate venv; check `python -m pip show fastapi`; select interpreter in IDE |
| `fastapi: command not found` | Installed without `[standard]` or venv inactive | `pip install "fastapi[standard]"` or use `uvicorn` |
| `Error loading ASGI app. Could not import module "main"` | Wrong module path / running from wrong dir | Run from project root: `uvicorn app.main:app`; ensure `app/__init__.py` |
| `Attribute "app" not found in module` | Variable isn't named `app` | Use `module:your_variable_name` |
| `[Errno 10048] / address already in use` | Port 8000 busy | Use `--port 8001` or kill: `netstat -ano \| findstr :8000` then `taskkill /PID <pid> /F` (Win), `lsof -i :8000` then `kill <pid>` (mac/Linux) |
| `externally-managed-environment` (Linux/macOS pip) | PEP 668 protects system Python | Use a venv — never `--break-system-packages` |
| `Form data requires "python-multipart"` | Missing dep | `pip install python-multipart` |
| `email-validator is not installed` | Using `EmailStr` | `pip install "pydantic[email]"` |
| `psycopg2` build fails | No C compiler/libpq | Use `psycopg[binary]` (v3) or `psycopg2-binary` |
| Code changes not picked up | No `--reload` / file outside watched dir | Use `fastapi dev` or `--reload --reload-dir app` |
| `pip` installs into wrong Python | Multiple Pythons | Always use `python -m pip ...` |

---

## ✅ Quick Revision — Chapter 1

- `python -m venv .venv` → activate (`.\.venv\Scripts\Activate.ps1` / `source .venv/bin/activate`).
- `pip install "fastapi[standard]"` gives FastAPI + Uvicorn + CLI + extras.
- Run: `fastapi dev app/main.py` (dev) or `uvicorn app.main:app --reload`.
- Docs at `/docs` (Swagger) and `/redoc`.
- Pin deps: `pip freeze > requirements.txt` or `pyproject.toml` + lock (uv/poetry).
- Never commit `.venv` or `.env`; commit `.env.example`.
- **Key takeaway:** *One project = one venv = one pinned dependency file.*
