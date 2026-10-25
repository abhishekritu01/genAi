# Chapter 7 — Authentication and Authorization

> **Goal:** Securely register and log in users, issue and verify JWT access/refresh tokens, protect endpoints with dependencies, implement roles, permissions and ownership, API keys, password reset and email verification.

---

## 7.1 Authentication vs Authorization

| | Authentication (AuthN) | Authorization (AuthZ) |
|---|---|---|
| Question | **Who are you?** | **What are you allowed to do?** |
| Mechanism | Password, token, API key, OAuth login, mTLS | Roles, permissions, ownership, policies |
| Failure status | **401 Unauthorized** (+ `WWW-Authenticate` header) | **403 Forbidden** (or 404 to hide existence) |
| Example | Valid JWT for user 7 | User 7 may edit project 12 only if owner |

---

## 7.2 Password Hashing

**Rule:** Never store passwords. Store a **slow, salted hash**.

| Algorithm | Status |
|---|---|
| Plain text, MD5, SHA-1, SHA-256 (unsalted/fast) | ⚠️ **Never** — fast hashes are brute-forced at billions/sec |
| **Argon2id** | ✅ Recommended (memory-hard, OWASP #1) |
| bcrypt | ✅ Fine (72-byte input limit) |
| scrypt / PBKDF2 | ✅ Acceptable |

Library: **`pwdlib`** (modern; used in current FastAPI docs). ⚠️ `passlib` is unmaintained and breaks with newer `bcrypt` versions — avoid for new code.

```bash
$ pip install "pwdlib[argon2]"
```

**`app/core/security.py` (part 1)**
```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()        # Argon2id with sane parameters


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)              # salt is generated & embedded automatically


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)    # constant-time comparison


# Example output: $argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>
```

💡 Timing-attack defense at login: if the user doesn't exist, still run a dummy `verify_password` so response time doesn't reveal which emails exist.

---

## 7.3 How OAuth2 Password Flow + JWT Works

```
Client                                   API
  │ POST /auth/token  (form: username, password)
  │ ───────────────────────────────────────────►  verify password hash
  │                                              create JWT {sub: user_id, exp, ...} signed with SECRET
  │ ◄─────────────────────────────────────────── {"access_token": "eyJ...", "token_type": "bearer"}
  │
  │ GET /users/me   Authorization: Bearer eyJ...
  │ ───────────────────────────────────────────►  verify signature + exp → load user
  │ ◄─────────────────────────────────────────── 200 {user}
```

**JWT (JSON Web Token)** = `base64url(header).base64url(payload).signature`
```json
// header
{"alg": "HS256", "typ": "JWT"}
// payload (claims) — readable by ANYONE, only signed, not encrypted!
{"sub": "42", "role": "admin", "type": "access", "exp": 1767225600, "iat": 1767224700, "jti": "uuid"}
```
- **Stateless:** server verifies the signature; no DB lookup needed to trust the claims.
- ⚠️ Never put secrets/PII in the payload.
- `HS256` = shared secret (one service). `RS256`/`ES256` = private key signs, public key verifies (many services verify; only the auth service signs) — use for microservices.

---

## 7.4 Full Implementation: Register, Login, Me

```bash
$ pip install pyjwt "pwdlib[argon2]" python-multipart "pydantic[email]"
```
⚠️ `python-jose` is effectively unmaintained → use **PyJWT** (current FastAPI docs do).

**`app/core/security.py` (part 2)**
```python
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from app.core.config import settings


def _create_token(subject: str, token_type: str, expires: timedelta, extra: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,               # who (always a string)
        "type": token_type,           # "access" | "refresh" — prevents using refresh as access
        "iat": now,
        "exp": now + expires,
        "jti": uuid4().hex,           # unique token id (for revocation)
        **(extra or {}),
    }
    return jwt.encode(payload, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int, role: str) -> str:
    return _create_token(str(user_id), "access",
                         timedelta(minutes=settings.access_token_expire_minutes), {"role": role})


def create_refresh_token(user_id: int) -> str:
    return _create_token(str(user_id), "refresh", timedelta(days=settings.refresh_token_expire_days))


def decode_token(token: str, expected_type: str) -> dict:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],      # ★ explicit allow-list (prevents alg=none attacks)
        options={"require": ["exp", "sub", "type"]},
    )
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("Wrong token type")
    return payload
```

**`app/schemas/auth.py`**
```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=120)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str | None
    role: str
    is_active: bool


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
```

**`app/api/deps.py`**
```python
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")   # enables "Authorize" button in Swagger

DbSession = Annotated[Session, Depends(get_db)]

CREDENTIALS_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbSession) -> User:
    try:
        payload = decode_token(token, expected_type="access")
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):   # ExpiredSignatureError is a subclass
        raise CREDENTIALS_EXC
    user = db.get(User, user_id)
    if user is None:
        raise CREDENTIALS_EXC
    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]
```

**`app/api/v1/auth.py`**
```python
from typing import Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.api.deps import CurrentUser, DbSession
from app.core.security import (create_access_token, create_refresh_token, decode_token,
                               hash_password, verify_password)
from app.models.user import User
from app.schemas.auth import RefreshRequest, TokenPair, UserOut, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])
DUMMY_HASH = hash_password("dummy-password-for-timing")


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: DbSession):
    email = data.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email, full_name=data.full_name, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token", response_model=TokenPair)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    """OAuth2 spec: form fields `username` + `password` (we treat username as email)."""
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if user is None:
        verify_password(form.password, DUMMY_HASH)          # equalize timing
        raise HTTPException(401, "Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    return TokenPair(access_token=create_access_token(user.id, user.role),
                     refresh_token=create_refresh_token(user.id))


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, db: DbSession):
    try:
        payload = decode_token(body.refresh_token, expected_type="refresh")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid refresh token")
    user = db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(401, "Invalid refresh token")
    # production: check jti not revoked + rotate (see 7.5)
    return TokenPair(access_token=create_access_token(user.id, user.role),
                     refresh_token=create_refresh_token(user.id))


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user
```

Try it:
```bash
$ curl -X POST localhost:8000/api/v1/auth/register -H "Content-Type: application/json" \
       -d '{"email":"a@b.com","password":"S3cure-pass!"}'
$ curl -X POST localhost:8000/api/v1/auth/token -d "username=a@b.com&password=S3cure-pass!"
{"access_token":"eyJhbGciOi...","refresh_token":"eyJ...","token_type":"bearer"}
$ curl localhost:8000/api/v1/auth/me -H "Authorization: Bearer eyJhbGciOi..."
```
In Swagger: click **Authorize 🔒** → enter email/password → all protected calls send the token.

---

## 7.5 Access Tokens vs Refresh Tokens

| | Access token | Refresh token |
|---|---|---|
| Purpose | Call APIs | Get new access tokens |
| Lifetime | Short (5–15 min) | Long (days–weeks) |
| Sent to | Every API request | Only `/auth/refresh` |
| Storage (browser) | Memory | `HttpOnly; Secure; SameSite` cookie |
| Revocation | Hard (stateless) — rely on short expiry | **Stored server-side** → revocable |

### Refresh token rotation + reuse detection (🟡 professional)
```
1. Login → store refresh token record {jti, user_id, family_id, expires_at, revoked=False}
2. /refresh with token R1:
     - R1 unknown/expired/revoked  → 401
     - R1 already USED → 🚨 token theft! revoke whole family, force re-login
     - else mark R1 used, issue R2 (same family)
3. Logout → revoke family
```
```python
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    jti: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    family_id: Mapped[str] = mapped_column(String(64), index=True)
    expires_at: Mapped[datetime]
    used_at: Mapped[datetime | None]
    revoked: Mapped[bool] = mapped_column(default=False)
```
(Store a **hash** of opaque refresh tokens if you use random strings instead of JWTs.)

### Logout with stateless access tokens
- Short access TTL (accept up to N minutes of validity), **or**
- Denylist `jti` in Redis until `exp`, **or**
- `token_version` column on user; include in JWT; bump to invalidate all tokens.

---

## 7.6 Role-Based Access Control (RBAC)

```python
# app/models/user.py
class Role(str, enum.Enum):
    user = "user"
    manager = "manager"
    admin = "admin"
# column: role: Mapped[str] = mapped_column(String(20), default=Role.user.value)
```

```python
# app/api/deps.py
from collections.abc import Callable

def require_roles(*allowed: str) -> Callable[[User], User]:
    def checker(user: CurrentUser) -> User:
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker

AdminUser = Annotated[User, Depends(require_roles("admin"))]


@router.get("/admin/stats")
def stats(admin: AdminUser): ...

@router.delete("/users/{id}", dependencies=[Depends(require_roles("admin", "manager"))])
def delete_user(id: int): ...
```

### Permissions (finer-grained than roles)
```python
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "user":    {"project:read", "project:create"},
    "manager": {"project:read", "project:create", "project:update", "member:invite"},
    "admin":   {"*"},
}

def require_permission(perm: str):
    def checker(user: CurrentUser) -> User:
        perms = ROLE_PERMISSIONS.get(user.role, set())
        if "*" not in perms and perm not in perms:
            raise HTTPException(403, f"Missing permission: {perm}")
        return user
    return Depends(checker)

@router.patch("/projects/{id}", dependencies=[require_permission("project:update")])
def update_project(...): ...
```

OAuth2 **scopes** (FastAPI `Security` + `SecurityScopes`) are the standards-based variant: token carries `"scope": "items:read items:write"`.

### Resource ownership (ABAC-lite)
RBAC alone isn't enough: a "user" can update projects — but **only their own**.
```python
def get_owned_project(project_id: int, user: CurrentUser, db: DbSession) -> Project:
    project = db.get(Project, project_id)
    if project is None or (project.owner_id != user.id and user.role != "admin"):
        raise HTTPException(404, "Project not found")      # 404 hides existence from non-owners
    return project

OwnedProject = Annotated[Project, Depends(get_owned_project)]

@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project: OwnedProject, db: DbSession):
    db.delete(project); db.commit()
```
🐞 **IDOR (Insecure Direct Object Reference)** — the #1 API vulnerability (OWASP API1: Broken Object Level Authorization): checking "is logged in" but not "owns this object". Always scope queries: `WHERE id = :id AND owner_id = :uid`.

For complex policies (org membership, sharing, hierarchies), use a policy engine: OPA, Casbin, Cerbos, Oso, or relationship-based (Zanzibar-style: SpiceDB, OpenFGA).

---

## 7.7 API Keys and Bearer Tokens

**Use for:** machine-to-machine clients, partner integrations, webhooks.

```python
import hashlib, hmac, secrets
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def generate_api_key() -> tuple[str, str]:
    raw = "sk_live_" + secrets.token_urlsafe(32)          # show ONCE to the client
    return raw, hashlib.sha256(raw.encode()).hexdigest()   # store only the hash


def get_api_client(key: Annotated[str | None, Depends(api_key_header)], db: DbSession) -> ApiClient:
    if not key:
        raise HTTPException(401, "Missing API key")
    digest = hashlib.sha256(key.encode()).hexdigest()
    client = db.scalar(select(ApiClient).where(ApiClient.key_hash == digest, ApiClient.revoked.is_(False)))
    if client is None:
        raise HTTPException(401, "Invalid API key")
    return client
```
- Store **hashes** (SHA-256 is fine here because keys are long random strings, not human passwords).
- Prefix keys (`sk_live_`, `sk_test_`) → easy identification + secret scanners detect leaks.
- Support multiple active keys per client → zero-downtime rotation; track `last_used_at`; scopes per key.
- Compare secrets with `hmac.compare_digest` when comparing raw values.

`HTTPBearer` — when you want a generic `Authorization: Bearer <token>` without the OAuth2 password flow:
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
bearer = HTTPBearer()
def token_dep(creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> str:
    return creds.credentials
```

---

## 7.8 Password Reset & Email Verification

### Password reset flow
```
1. POST /auth/forgot-password {email}
     → ALWAYS return 202 "If the account exists, an email was sent"  (no user enumeration)
     → if user exists: token = secrets.token_urlsafe(32); store SHA-256(token), user_id, expires (15–60 min)
     → email link https://app.com/reset?token=<raw>   (background task / queue)
2. POST /auth/reset-password {token, new_password}
     → hash token, look up, check not expired/used
     → set new password hash, mark token used
     → revoke all refresh tokens / bump token_version (log out other sessions)
     → notify user by email "your password was changed"
```
```python
@router.post("/forgot-password", status_code=202)
def forgot_password(body: ForgotPassword, db: DbSession, tasks: BackgroundTasks):
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if user:
        raw = secrets.token_urlsafe(32)
        db.add(PasswordResetToken(token_hash=sha256(raw), user_id=user.id,
                                  expires_at=utcnow() + timedelta(minutes=30)))
        db.commit()
        tasks.add_task(send_reset_email, user.email, raw)
    return {"message": "If that email exists, a reset link has been sent."}
```

### Email verification
- On register: `is_verified=False`; send link with signed token (JWT with `type="verify_email"`, short expiry, or DB-stored random token).
- `GET /auth/verify?token=...` → mark verified.
- Restrict sensitive actions until verified (dependency `require_verified_user`).

---

## 7.9 Where to Store Tokens (browser clients)

| Option | XSS risk | CSRF risk | Notes |
|---|---|---|---|
| `localStorage` | ❌ High (any injected script reads it) | ✅ none | Simple but risky |
| Memory (JS variable) + refresh in HttpOnly cookie | ✅ Lower | refresh endpoint needs CSRF protection | ✅ Common SPA best practice |
| HttpOnly `Secure` `SameSite=Lax/Strict` cookie for everything | ✅ JS can't read | Needs CSRF tokens for state-changing requests (or SameSite=Strict) | Classic web apps, BFF pattern |

Mobile/server clients: Authorization header with token from secure storage.

---

## 7.10 Common Auth Vulnerabilities & Best Practices

| Vulnerability | Prevention |
|---|---|
| Weak password storage | Argon2id/bcrypt via pwdlib |
| Brute force / credential stuffing | Rate-limit login per IP + per account, lockout/backoff, CAPTCHA, MFA, breached-password check (HIBP k-anonymity) |
| User enumeration | Same message & timing for "no user" and "wrong password"; generic forgot-password response |
| JWT `alg=none` / algorithm confusion | `algorithms=["HS256"]` explicit; separate keys per alg |
| Weak JWT secret | ≥ 256-bit random; from secret manager; rotate (support `kid` header) |
| Long-lived access tokens | 5–15 min; refresh rotation |
| Missing `exp` / type checks | `options={"require": [...]}`, check `type` claim |
| IDOR / BOLA | Ownership checks on every object access |
| Mass assignment (`is_admin` in body) | Separate input schemas; never `User(**request.json())` |
| Tokens in URLs | Never — URLs end up in logs/referrers (except one-time email links, short expiry) |
| Logging secrets | Redact `Authorization`, passwords, tokens |
| Session fixation after password change | Revoke all sessions / bump token version |
| Missing HTTPS | Tokens sniffed — always TLS |

🟡 **Don't roll your own if you don't need to:** managed identity (Auth0, Cognito, Entra ID, Keycloak, Clerk, Supabase Auth) with OIDC. Your API then only **verifies** RS256 JWTs using the provider's JWKS public keys:
```python
from jwt import PyJWKClient
jwks = PyJWKClient("https://YOUR_DOMAIN/.well-known/jwks.json")
signing_key = jwks.get_signing_key_from_jwt(token)
payload = jwt.decode(token, signing_key.key, algorithms=["RS256"], audience="my-api",
                     issuer="https://YOUR_DOMAIN/")
```

---

## ✅ Quick Revision — Chapter 7

- AuthN = who (401); AuthZ = what (403/404).
- Hash with Argon2id (`pwdlib`) — ⚠️ not passlib/MD5/SHA.
- JWT = signed, not encrypted; verify with explicit `algorithms`, check `exp`, `type`.
- ⚠️ python-jose → use **PyJWT**.
- `OAuth2PasswordBearer(tokenUrl=...)` + `get_current_user` dependency → `CurrentUser` alias.
- Access short, refresh long + stored + rotated + reuse detection.
- RBAC via dependency factories; permissions map; **ownership checks always** (IDOR).
- API keys: random, prefixed, hashed at rest, rotatable, scoped.
- Reset/verification: random token, hashed, short expiry, single use, no enumeration.
- Rate-limit login; never log tokens.

🎤 *"Login verifies an Argon2 hash and issues a short-lived access JWT plus a rotating refresh token stored server-side so it can be revoked. Every protected route depends on `get_current_user`, which validates signature, expiry and token type. Authorization is layered: role/permission dependencies for coarse access, and ownership checks scoped in the query to prevent IDOR."*
