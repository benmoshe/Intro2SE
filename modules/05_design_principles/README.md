# 05 — Design principles

**Goal:** structure code so that the changes you'll likely need are cheap.

Design is about managing change. Good design doesn't mean more classes — it
means that when a requirement moves, you edit one place, not ten.

## Cohesion and coupling

- **Cohesion** — how strongly the things inside a module belong together. High is good.
- **Coupling** — how much one module must know about another. Low is good.

A quick test: describe what a module does in one sentence. If you can't, cohesion
is low. Then ask what would have to change if you rewrote the module next
door. If the answer is "lots", coupling is high.

## SOLID, in plain terms

| Principle | In practice |
|-----------|-------------|
| **S**ingle responsibility | A class has one reason to change. Parsing, business rules and output formatting change for different reasons — separate them. |
| **O**pen/closed | Add behaviour by adding code, not editing existing code. A new export format shouldn't mean touching an `if/elif` chain. |
| **L**iskov substitution | Anything that claims to be an `Exporter` must work wherever an `Exporter` is expected — no surprises. |
| **I**nterface segregation | Depend on small interfaces. A function that only reads shouldn't demand an object that can also write and delete. |
| **D**ependency inversion | High-level policy depends on abstractions, not concrete details. Your business logic shouldn't import `sqlite3`. |

These are heuristics for spotting pain, not laws. Apply them when you feel the
friction they describe, not pre-emptively.

## Before and after

```python
def export(report, fmt):
    if fmt == "json":
        ...
    elif fmt == "csv":
        ...
    # every new format edits this function, and every edit risks the others
```

Open/closed version — each format is its own small object behind a shared interface:

```python
class Exporter(Protocol):
    def export(self, report: Report) -> str: ...

registry.register("json", JsonExporter())
registry.register("yaml", YamlExporter())   # new code only; nothing existing changed
```

## Dependency injection

Pass collaborators in rather than creating them inside:

```python
class ReportService:
    def __init__(self, exporters: ExporterRegistry) -> None:
        self._exporters = exporters
```

You met this in module 03 with the clock. It's the same idea at every scale,
and it's what makes code both testable and reconfigurable. No framework needed.

## Composition over inheritance

Inheritance is the tightest coupling Python offers: a subclass depends on
every detail of its parent. Reach for it when there's a genuine *is-a*
relationship and you need substitutability. Otherwise, hold a reference to a
collaborator (*has-a*) and delegate.

## Two counterweights

- **YAGNI** — "you aren't gonna need it." Don't build flexibility for
  requirements that don't exist.
- **Rule of three** — tolerate duplication twice; abstract on the third
  occurrence, when you can see the real pattern.

Over-engineering is as costly as under-engineering. It just takes longer to notice.

## Exercise

Build a pluggable export system in `exercise.py`. `Report`, the `Exporter`
protocol and `UnknownFormatError` are provided.

- `JsonExporter` and `CsvExporter` — each turns a `Report` into a string.
- `ExporterRegistry` — `register(fmt, exporter)`, `export(report, fmt)`, `formats()`.

One test registers a brand-new exporter defined in the test file. If your
registry needs no changes to support it, you've satisfied open/closed.

```bash
pytest modules/05_design_principles
```

## Check yourself

- Which SOLID principle does an `if fmt == ...` chain violate, and what's the practical cost?
- When is an `if/elif` chain perfectly fine?
- `CsvExporter` doesn't inherit from `Exporter`. Why is it still one?
