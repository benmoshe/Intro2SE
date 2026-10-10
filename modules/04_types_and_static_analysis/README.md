# 04 — Types and static analysis

**Goal:** use type hints and automated checkers to catch whole classes of bugs
before the code ever runs.

## Type hints

Python doesn't enforce annotations at runtime. They're documentation that a
tool — mypy — can verify.

```python
def mean(values: list[float]) -> float:
    return sum(values) / len(values)

def find_user(user_id: int) -> User | None: ...
```

`User | None` is the most valuable hint you'll write: mypy then forces every
caller to handle the `None` case before touching the result.

Common building blocks:

| Hint | Meaning |
|------|---------|
| `list[int]`, `dict[str, float]` | containers and what's in them |
| `X \| None` | might be missing |
| `Iterable[T]`, `Mapping[K, V]`, `Sequence[T]` | accept the *widest* type you actually need (from `collections.abc`) |
| `Callable[[int, str], bool]` | a function taking `(int, str)` and returning `bool` |
| `TypeVar("T")` | "some type, the same one each time it appears" |

Be liberal in what you accept (`Iterable[T]`) and specific in what you return (`list[T]`).

## Generics

```python
T = TypeVar("T")

def first(items: Iterable[T]) -> T | None:
    for item in items:
        return item
    return None
```

mypy now knows `first([1, 2])` is `int | None` and `first(["a"])` is `str | None`.

## Dataclasses and value objects

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

You get `__init__`, `__repr__` and `__eq__` for free. `frozen=True` makes
instances immutable — and hashable. A small immutable type defined by its
value (money, a date range, an email address) is a **value object**. Wrapping
primitives this way stops you adding dollars to euros or passing a user id
where an order id belongs.

## Protocols: typed duck typing

```python
class Exporter(Protocol):
    def export(self, report: Report) -> str: ...
```

Any class with a matching `export` method satisfies `Exporter` — no
inheritance needed. You'll use this heavily from module 05 on.

## The tools

```bash
mypy modules/04_types_and_static_analysis/exercise.py   # type check (strict, per pyproject.toml)
ruff check .                                            # lint
ruff format .                                           # format
```

A formatter ends style arguments for good. A linter catches real bugs —
unused variables, mutable default arguments, shadowed names. A type checker
catches `None` slipping through and arguments in the wrong order. All three
run in milliseconds; let them do the boring part of code review.

## Exercise

In `exercise.py`:

1. `Money` — a frozen dataclass holding integer `cents` and a `currency`
   (default `"USD"`). Storing cents as an `int` avoids float rounding errors.
   - `Money.from_str("12.34")` parses a decimal string.
   - `a + b` returns a new `Money`; mixing currencies raises `CurrencyMismatch`.
   - `str(m)` gives `"12.34 USD"`.
2. `group_by(items, key)` — fully annotated with `TypeVar`s.

```bash
pytest modules/04_types_and_static_analysis
mypy modules/04_types_and_static_analysis/exercise.py
```

Both must be clean. The tests check behaviour; only mypy checks your annotations.

## Check yourself

- Why is `0.1 + 0.2 == 0.3` false, and how does storing cents sidestep it?
- What does `frozen=True` buy you beyond "can't assign"?
- When would you annotate a parameter `Iterable[T]` rather than `list[T]`?
