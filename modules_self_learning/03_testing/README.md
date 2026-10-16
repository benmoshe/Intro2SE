# 03 — Testing

**Goal:** write tests that give you confidence to change code, and design code
so it's easy to test.

## Anatomy of a test

Arrange, act, assert — one behaviour per test, named for that behaviour:

```python
def test_withdraw_reduces_balance():
    account = Account(balance=100)   # arrange
    account.withdraw(30)             # act
    assert account.balance == 70     # assert
```

pytest finds files named `test_*.py` and functions named `test_*`, and
rewrites plain `assert` so failures show both sides of the comparison.

## Parametrize: one test, many cases

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [("45s", 45), ("2m", 120), ("1h30m", 5400)],
)
def test_parse_duration(text, expected):
    assert parse_duration(text) == expected
```

Each row is reported separately, so one bad case doesn't hide the others.

## Testing errors

```python
with pytest.raises(ValueError, match="invalid duration"):
    parse_duration("soon")
```

Failure paths are behaviour too. Untested error handling is usually broken.

## Fixtures

A fixture is a named piece of setup that a test requests by argument name:

```python
@pytest.fixture
def account():
    return Account(balance=100)

def test_withdraw(account):
    ...
```

Built-in ones worth knowing: `tmp_path` (a fresh directory), `capsys`
(captured stdout/stderr), `caplog` (captured log records), `monkeypatch`.
The `impl` fixture this course uses lives in the root `conftest.py`.

## Test doubles and dependency injection

Code that reads the clock, the network, or a database is slow and
non-deterministic to test. Don't reach for those things directly — **accept
them as parameters**:

```python
class RateLimiter:
    def __init__(self, max_calls, period, clock=time.monotonic):
        self._clock = clock
```

Production code uses the default. Tests pass a *fake* they fully control:

```python
class FakeClock:
    def __init__(self): self.now = 0.0
    def __call__(self): return self.now
```

No `sleep`, no patching, no flakiness. Prefer hand-written fakes like this to
`unittest.mock` where you can; mocks couple tests to *how* code calls its
collaborators rather than to what it achieves.

## Test-driven development

1. **Red** — write a small failing test for the next bit of behaviour.
2. **Green** — write the simplest code that passes.
3. **Refactor** — clean up with the tests as a safety net.

The value isn't the ritual; it's that you never write code without knowing
how you'll check it, and you design the interface from the caller's side.

## What makes a good test

- **Fast** — milliseconds, so you run them constantly.
- **Deterministic** — same result every run, in any order.
- **Tests behaviour, not implementation** — survives a refactor.
- **Fails for one reason** — and the name tells you which.

Most tests should be small unit tests; fewer integration tests check that the
pieces connect; a handful of end-to-end tests cover critical paths.

## Exercise

Two pieces in `exercise.py`:

1. `parse_duration("1h30m") -> 5400`. Work through the tests one at a time,
   TDD-style: `pytest modules/03_testing -x -k duration`.
2. `RateLimiter` — a sliding-window limiter with an injected clock. Read
   `FakeClock` in the tests first to see how time is controlled.

**Stretch:** create `test_mine.py` and add three cases the provided tests
don't cover. What should `parse_duration("0s")` return? `" 5m "`? Decide,
write the test, then make it pass.

## Check yourself

- Why does `RateLimiter` take `clock` as an argument instead of calling `time.monotonic()` inside `allow`?
- A test passes alone but fails when the whole suite runs. What's the likely cause?
