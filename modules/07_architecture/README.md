# 07 — Architecture

**Goal:** organise a whole application so business rules stay independent of
databases, frameworks and user interfaces.

Module 05 was about classes. Architecture is the same thinking one level up:
which *parts of the system* know about which others.

## Layers

A workable default for most applications:

```
┌─────────────────────────────────────┐
│ Interface    CLI, HTTP handlers     │  parses input, formats output
├─────────────────────────────────────┤
│ Service      use cases              │  "create a task", "complete a task"
├─────────────────────────────────────┤
│ Domain       entities and rules     │  Task, what a valid title is
└─────────────────────────────────────┘
        ▲
        │ implements an interface the service defines
┌─────────────────────────────────────┐
│ Infrastructure  SQLite, files, APIs │
└─────────────────────────────────────┘
```

**The one rule:** dependencies point inward. The domain imports nothing from
the outer layers. The service layer never imports `sqlite3` or `argparse`.

## Ports and adapters

How can the service save tasks without knowing about the database? It
declares what it *needs* as an interface — a **port**:

```python
class TaskRepository(Protocol):
    def add(self, title: str) -> Task: ...
    def get(self, task_id: int) -> Task | None: ...
    def all(self) -> list[Task]: ...
    def save(self, task: Task) -> None: ...
```

Each storage technology supplies an **adapter** that satisfies it:
`InMemoryTaskRepository`, `SqliteTaskRepository`. This is dependency
inversion (module 05) applied to a whole subsystem, and it's known as the
**repository pattern**.

What you gain:

- **Fast tests.** The service is tested against the in-memory adapter — no I/O.
- **Deferred decisions.** Start in memory, add SQLite later, swap to Postgres
  after that. The service doesn't change.
- **A clear place for every piece of code.** "Is this a business rule or a
  storage detail?" has an answer.

## Contract tests

If two adapters claim to implement the same port, they must behave the same.
So run *one* set of tests against *both*:

```python
@pytest.fixture(params=["memory", "sqlite"])
def repo(request): ...
```

Look at how `test_exercise.py` does this. A subtle bug this catches: an
in-memory repository that hands out its internal objects lets callers mutate
stored state without calling `save` — so code that forgets to save works in
tests and fails against a real database. A good in-memory adapter returns
copies.

## Wiring it together

Something has to build the concrete objects and connect them. Do it in one
place, at the edge of the program — the **composition root**:

```python
def main() -> None:
    repo = SqliteTaskRepository(sqlite3.connect("tasks.db"))
    service = TaskService(repo)
    run_cli(service)
```

Everything below `main` receives its dependencies; nothing reaches out for them.

## Keep it proportionate

A 200-line script needs none of this. Layers earn their keep when the
application has real business rules, more than one way in (CLI *and* API), or
storage you want to fake in tests. Add structure when the code asks for it.

## Exercise

Build the core of a task tracker in `exercise.py`. `Task`, `TaskRepository`
and `TaskNotFound` are provided.

- `InMemoryTaskRepository` — dict-backed; hands out copies.
- `SqliteTaskRepository` — takes a `sqlite3.Connection`, creates its own table.
- `TaskService` — `create(title)`, `complete(task_id)`, `pending()`.

Every test runs against both repositories.

```bash
pytest modules/07_architecture
```

## Check yourself

- `TaskService` never mentions SQL. Which principle is that, and what does it buy you?
- Why should the in-memory repository return copies?
- Where would validation of "title must not be empty" go, and why not in the repository?
