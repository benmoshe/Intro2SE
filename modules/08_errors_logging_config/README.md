# 08 — Errors, logging and configuration

**Goal:** build software that fails clearly, tells you what it's doing, and can
be configured without editing code.

These are the things that separate code that works on your laptop from code
you can operate in production.

## Exceptions

**Raise early, catch late.** Detect a problem as soon as it's knowable; handle
it at the level that can actually do something about it — often only at the
top of the program.

```python
class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""
```

- **Define your own exception types** for errors callers may want to handle.
  A caller can catch `ConfigError` precisely; they can't safely catch `Exception`.
- **Never use a bare `except:`** and avoid `except Exception: pass`. Swallowed
  errors resurface later as mysteries.
- **Catch the narrowest type** you know how to handle.
- **Write messages for the person fixing it**: say what was wrong and what
  was expected — `APP_PORT must be an integer between 1 and 65535, got 'abc'`.
- **Preserve the cause** when translating: `raise ConfigError(...) from error`.
- **Use `finally` or `with`** for cleanup that must happen either way.

Exceptions are for things going wrong, not ordinary outcomes. "User not
found" during a lookup is often better as a `None` return (module 04's
`User | None`) than as an exception.

## Logging

`print` is for the program's output. `logging` is for the story of what the
program is doing.

```python
import logging

logger = logging.getLogger(__name__)

logger.info("processed %d orders", count)
logger.warning("attempt %d/%d failed: %s", attempt, attempts, error)
logger.exception("could not charge card")   # inside except: includes the traceback
```

| Level | Use for |
|-------|---------|
| `DEBUG` | detail useful only when diagnosing |
| `INFO` | normal milestones |
| `WARNING` | something odd, but we carried on |
| `ERROR` | an operation failed |
| `CRITICAL` | the program can't continue |

Rules of thumb:

- One logger per module: `logging.getLogger(__name__)`.
- Pass values as arguments (`"x=%s", x`), not f-strings — formatting is then
  skipped when the level is disabled.
- **Libraries log; applications configure.** Call `logging.basicConfig(...)`
  once, in `main`, never at import time in a module others will use.
- Never log secrets: passwords, tokens, full card numbers.

## Configuration

Anything that differs between your laptop, CI and production — database
URLs, ports, feature flags, credentials — is configuration, and belongs in
the **environment**, not the source.

Read it once, at startup, into a typed object, and validate it immediately:

```python
@dataclass(frozen=True)
class Config:
    database_url: str
    port: int = 8000
    debug: bool = False

config = load_config(os.environ)   # fails fast, with a clear message
```

The rest of the program receives `config` and never touches `os.environ`.
Notice `load_config` takes the environment as an argument — so a test can
hand it a plain dict.

**Secrets never go in git.** Not in code, not in a committed `.env`. Once
pushed, a secret must be considered leaked and rotated.

## Retrying

Networks fail transiently. A retry helper is a classic small utility, and a
good exercise in everything above: catch only *expected* errors, log each
failure, back off exponentially, and finally let the last error propagate.

## Exercise

In `exercise.py`:

1. `load_config(env)` — reads `APP_DATABASE_URL` (required), `APP_PORT`
   (optional, 1–65535, default 8000) and `APP_DEBUG` (optional boolean).
   Every problem raises `ConfigError` naming the offending variable.
2. `retry(fn, attempts=3, delay=0.1, exceptions=..., sleep=...)` — calls `fn`
   until it succeeds; logs a warning per failure; sleeps `delay`, `2×delay`,
   `4×delay`… between attempts; re-raises the final error.

`sleep` is injected for the same reason the clock was in module 03.

```bash
pytest modules/08_errors_logging_config
```

## Check yourself

- Why does `retry` take an `exceptions` argument instead of catching everything?
- What's wrong with `logging.basicConfig()` at the top of a library module?
- You find an API key in a commit from last month. Is deleting it in a new commit enough?
