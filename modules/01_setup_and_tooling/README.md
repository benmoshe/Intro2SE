# 01 — Setup and tooling

**Goal:** have a reproducible project environment and a fast edit–test loop.

Writing a script and engineering software differ mostly in what surrounds the
code: isolated dependencies, automated checks, and a single command that tells
you whether things work. Set that up once and every later module gets easier.

## Virtual environments

Never install project dependencies into your system Python. A virtual
environment is a private copy of the interpreter's package directory:

```bash
python3 -m venv .venv          # create
source .venv/bin/activate      # activate (Windows: .venv\Scripts\activate)
pip install -r requirements-dev.txt
```

`.venv/` is disposable and never committed — see `.gitignore`. If it breaks,
delete it and recreate it. That it *can* be recreated from a file is the point.

## `pyproject.toml`

One file configures the project and its tools. Open the one at the repo root:
pytest, ruff, and mypy each read their own `[tool.*]` table from it. In module
10 you'll add a `[project]` table to make code installable.

## The three tools you'll use throughout

| Tool | Answers | Run |
|------|---------|-----|
| **pytest** | Does it behave correctly? | `pytest modules/01_setup_and_tooling` |
| **ruff** | Is it tidy and free of common mistakes? | `ruff check .` / `ruff format .` |
| **mypy** | Do the types line up? | `mypy modules/04_types_and_static_analysis/solution.py` |

Useful pytest flags:

- `-x` stop at the first failure
- `-k name` run only tests whose name matches
- `-vv` show full diffs
- `--lf` re-run only what failed last time

## The loop

1. Run the tests. Read the *first* failure — top to bottom, the assertion line
   and the diff tell you exactly what was expected.
2. Make the smallest change that could fix it.
3. Run again.

Seconds per cycle, not minutes. Fast feedback is the single biggest lever on
how quickly you can work safely.

## Exercise

Implement `slugify` in `exercise.py`. The task is easy on purpose — you're
really testing your setup.

```bash
pytest modules/01_setup_and_tooling
```

Then run `ruff check modules/01_setup_and_tooling` and `ruff format` on your
file and see what, if anything, they change.

## Check yourself

- Why is `.venv/` in `.gitignore` but `requirements-dev.txt` committed?
- What's the difference between a linter and a formatter?
- A teammate says "works on my machine". What in this module addresses that?
