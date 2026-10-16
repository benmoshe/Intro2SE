# 12 — Capstone: build and ship `tasker`

**Goal:** combine everything into one small, complete, well-engineered application.

You'll build `tasker`, a command-line task tracker, as a standalone project
in its own repository. Nothing here is new — the point is doing it all
together, unprompted, on a blank page.

## What it does

```
$ tasker add "Write the capstone"
Added task 1.
$ tasker add "Ship it"
Added task 2.
$ tasker done 1
Completed task 1: Write the capstone
$ tasker list
[ ] 2  Ship it
$ tasker list --all
[x] 1  Write the capstone
[ ] 2  Ship it
$ tasker export --format json
[{"id": 1, "title": "Write the capstone", "done": true}, ...]
$ tasker done 99
tasker: no task with id 99
$ echo $?
1
```

## Requirements

**Behaviour**

- Commands: `add TITLE`, `done ID`, `list [--all]`, `export --format {json,csv}`.
- Tasks persist between runs in SQLite.
- The database path comes from `TASKER_DB` (default `~/.tasker.db`).
- Empty titles and unknown ids produce a one-line message on stderr and exit code 1 — never a traceback.

**Structure** (modules 05–07)

- `src` layout, with separate modules for domain, repository, service, exporters and CLI.
- The service depends on a `TaskRepository` protocol, not on SQLite.
- Export formats plug in through a registry; adding one must not require editing existing code.
- All wiring happens in one place — the CLI's `main`.

**Quality** (modules 02–04, 08)

- Fully type-annotated; `mypy --strict` passes.
- `ruff check` and `ruff format --check` pass.
- Service tested against an in-memory repository; one contract test suite run against both repositories.
- CLI tested by calling `main(argv)` with `capsys` and a `tmp_path` database.
- Custom exception types; configuration loaded once into a frozen dataclass.
- `--verbose` turns on `DEBUG` logging to stderr.

**Delivery** (modules 09–11)

- Installable with `pip install .`, providing a `tasker` command via an entry point.
- A git history of small, well-described commits — not one giant one.
- GitHub Actions workflow running lint, type check and tests on every push and pull request.
- A `Dockerfile` that runs as a non-root user.
- A `README.md` covering what it is, how to install it, how to use it, and how to develop it.

## Suggested order

Work in thin vertical slices. After every step the tests pass and you commit.

1. Skeleton: repository, `pyproject.toml`, an empty package, one passing test, CI green.
   *Get the pipeline working while there's nothing to break.*
2. Domain and in-memory repository, test-first.
3. `TaskService` with `create`, `complete`, `pending`.
4. CLI for `add`, `done`, `list` against the in-memory repository.
5. SQLite repository; turn your repository tests into contract tests; wire it into `main`.
6. Configuration from the environment; error handling and exit codes.
7. Exporters and the `export` command.
8. Logging and `--verbose`.
9. Dockerfile, README, final tidy-up.

You've already written most of these pieces in modules 05, 07, 08 and 10.
Reuse the ideas; retype the code rather than pasting it — you'll improve it.

## Self-assessment

Score each line 0 (missing), 1 (partly) or 2 (solid).

| Area | Question |
|------|----------|
| Correctness | Does every command in the example session behave as shown? |
| Tests | Could you delete any line of logic without a test failing? |
| Tests | Does the whole suite run in under a few seconds, with no real files outside `tmp_path`? |
| Design | Does anything outside the SQLite repository import `sqlite3`? |
| Design | How many existing files change to add a `markdown` export format? (Target: zero.) |
| Readability | Could a stranger find where "empty titles are rejected" lives in under a minute? |
| Types | Is `mypy --strict` clean, without `# type: ignore` or `Any`? |
| Errors | Can any user input produce a traceback? |
| Git | Does `git log --oneline` read like a sensible story of the project? |
| CI | Is `main` protected, and has CI caught at least one real mistake? |
| Packaging | Does `pip install .` in a fresh venv give a working `tasker`? |
| Docs | Could someone install and use it from the README alone? |

20 or more out of 24: you're doing software engineering.

## Going further

- Due dates and priorities — notice which layers the change touches.
- A second interface: a small HTTP API with FastAPI that reuses `TaskService` unchanged.
- Schema migrations for the SQLite database.
- Test coverage with `pytest-cov`, and property-based tests with `hypothesis`.
- Publish to TestPyPI from CI when you push a version tag.

## Where to go next

- *The Pragmatic Programmer* — Hunt and Thomas
- *Refactoring* — Martin Fowler
- *Architecture Patterns with Python* — Percival and Gregory (free online)
- *A Philosophy of Software Design* — John Ousterhout
- The pytest, mypy and Python Packaging User Guide documentation
