# 06 — Design patterns

**Goal:** recognise recurring design problems and solve them idiomatically in Python.

A pattern is a named solution to a problem that keeps coming up. The names
matter more than the diagrams: "use a strategy here" communicates a whole
design in four words.

Many classic patterns were written for languages without first-class
functions. In Python they often collapse into something much smaller. Learn
the *problem* each one solves; then use the lightest tool that solves it.

## Strategy — swap an algorithm

**Problem:** one step of a process varies (pricing, sorting, validation) and
you don't want `if` branches for every variant.

In Python a strategy is usually just a function:

```python
PricingStrategy = Callable[[float], float]

def percentage_off(percent: float) -> PricingStrategy:
    def apply(amount: float) -> float:
        return amount * (1 - percent / 100)
    return apply

checkout = Checkout(pricing=percentage_off(10))
```

`percentage_off` is a **factory**: a function that builds and returns another
object — here, a closure that remembers `percent`. You've been using
strategies all along: the `key=` argument to `sorted` is one.

## Observer — react without coupling

**Problem:** when something happens (an order is paid), several unrelated
things must follow (send a receipt, update stock, log analytics). The code
that takes payment shouldn't know about any of them.

```python
bus.subscribe("order_paid", send_receipt)
bus.subscribe("order_paid", update_stock)
...
bus.publish("order_paid", {"amount": 90.0})
```

The publisher knows only the event name. Adding a new reaction is one
`subscribe` call — open/closed again.

The cost: control flow becomes implicit. You can't see what happens after
`publish` by reading the code around it. Use events at boundaries between
subsystems, not for ordinary function calls.

## Others worth knowing

| Pattern | Problem | Pythonic form |
|---------|---------|---------------|
| **Factory** | Creation logic is complex or varies | a function, or a `@classmethod` like `Money.from_str` |
| **Adapter** | You have interface A, callers need B | a thin wrapper class around A |
| **Decorator** | Add behaviour around a function | `@decorator` syntax — built in |
| **Iterator** | Traverse without exposing internals | generators and `yield` — built in |
| **Context manager** | Guarantee cleanup | `with` and `contextlib.contextmanager` — built in |
| **Repository** | Hide how data is stored | next module |
| **Singleton** | Exactly one instance | a module-level object. Usually a smell — prefer passing it in |

## When not to use a pattern

If a plain function or a three-line `if` does the job, a pattern is overhead.
Introduce one when you feel the specific pain it removes — typically the
second or third time you edit the same branching code.

## Exercise

In `exercise.py`:

1. **Strategies** — `no_discount`, and the factories `percentage_off(percent)`,
   `fixed_off(amount)` (never below zero) and `best_of(*strategies)`, which
   composes strategies into one that picks the lowest price.
2. **`EventBus`** — `subscribe(event, handler)` returns a function that
   unsubscribes; `publish(event, payload)` calls handlers in subscription
   order and returns how many ran.
3. **`Checkout`** — ties them together: `pay(amount)` applies the pricing
   strategy and publishes `"order_paid"`.

```bash
pytest modules/06_design_patterns
```

## Check yourself

- `best_of` takes strategies and returns a strategy. Why is that powerful?
- What's the downside of routing everything through an event bus?
- Name a strategy and a decorator from the standard library.
