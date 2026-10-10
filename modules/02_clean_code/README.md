# 02 — Clean code

**Goal:** write code a stranger can read, and improve existing code without
breaking it.

Code is read far more often than it is written. "Clean" isn't about taste — it
means the next person (often you, in six months) can change it confidently.

## Names

A name should answer *what is this?* without the reader looking elsewhere.

```python
d = 86400                      # what is d?
SECONDS_PER_DAY = 86_400       # ah

def calc(x, y): ...            # calc what?
def monthly_payment(principal, annual_rate): ...
```

- Variables and functions: `snake_case`. Classes: `PascalCase`. Constants: `UPPER_CASE`.
- Functions do things, so use verbs (`send_invoice`); values are things, so use nouns (`invoice`).
- Booleans read as questions: `is_valid`, `has_expired`.
- Length should match scope: `i` is fine in a three-line loop, not in a module.

## Magic numbers

A bare `0.08` in the middle of a function carries no meaning and gets duplicated.
Give it a name at module level: `TAX_RATE = 0.08`.

## Functions

- **Do one thing.** If you describe a function with "and", it's two functions.
- **Stay at one level of abstraction.** A function that reads
  `total = subtotal(items) - discount + shipping` shouldn't also contain a
  `for` loop multiplying prices.
- **Prefer returning values to mutating arguments.** Pure functions are trivially testable.
- **Guard clauses over nesting.** Handle the odd cases first and return early.

```python
def shipping_cost(amount):
    if amount > FREE_SHIPPING_THRESHOLD:
        return 0.0
    return STANDARD_SHIPPING
```

## Comments

Comment *why*, not *what*. If you need a comment to explain what a block does,
extract it into a function whose name says so.

## Refactoring

Refactoring is changing structure **without changing behaviour**. The safe way:

1. Make sure tests cover the current behaviour (write *characterization tests*
   if none exist — tests that pin down what the code does today).
2. Make one small change: rename, extract a function, replace a literal.
3. Run the tests. Green? Commit. Red? Undo — don't debug.
4. Repeat.

Never refactor and change behaviour in the same step.

## Exercise

`exercise.py` contains `order_total`. It works, and it's unpleasant.

```bash
pytest modules/02_clean_code
```

The behaviour tests **already pass** — they're your safety net. The other
tests fail because they expect well-named helpers to exist:

- `subtotal(items)` — sum of price × quantity
- `discount_rate(tier)` — `0.2` for `"gold"`, `0.1` for `"silver"`, otherwise `0.0`
- `shipping_cost(amount)` — free above 100, otherwise `5.99`

Extract them one at a time, running the tests after each step. Finish by
giving every magic number a name and making `order_total` read like a sentence.

## Check yourself

- You're mid-refactor and a test goes red. What do you do, and why not debug?
- Find one comment in code you've written that could be replaced by a better name.
