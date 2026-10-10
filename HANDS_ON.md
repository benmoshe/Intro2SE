# Software Engineering in Python

A hands-on course for people who can already write Python and want to learn to
*engineer* it: code that is tested, readable, well-structured, and shippable.

You learn by doing. Every module has a short lesson, an exercise with failing
tests, and a reference solution.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Requires Python 3.10+.

## How each module works

```
modules/03_testing/
├── README.md          the lesson — read this first
├── exercise.py        your workspace; fill in the TODOs
├── test_exercise.py   the tests that define "done"
└── solution.py        a reference answer — look only after you've tried
```

1. Read the module's `README.md`.
2. Run its tests and watch them fail:
   ```bash
   pytest modules/03_testing
   ```
3. Edit `exercise.py` until they pass.
4. Compare with `solution.py`. Yours doesn't need to match — ask *why* they differ.

To run the tests against the reference solutions instead of your work:

```bash
pytest --solutions
```

## Syllabus

| #  | Module | You will learn | Exercise |
|----|--------|----------------|----------|
| 01 | [Setup and tooling](modules/01_setup_and_tooling/README.md) | venvs, `pyproject.toml`, the edit–test loop | `slugify` warm-up |
| 02 | [Clean code](modules/02_clean_code/README.md) | naming, small functions, refactoring under test | untangle an order calculator |
| 03 | [Testing](modules/03_testing/README.md) | pytest, parametrize, fixtures, TDD, fakes | duration parser, rate limiter |
| 04 | [Types and static analysis](modules/04_types_and_static_analysis/README.md) | type hints, dataclasses, generics, mypy, ruff | `Money` value object, `group_by` |
| 05 | [Design principles](modules/05_design_principles/README.md) | SOLID, coupling/cohesion, dependency injection | pluggable report exporters |
| 06 | [Design patterns](modules/06_design_patterns/README.md) | strategy, observer, factory — the Pythonic way | pricing strategies, event bus |
| 07 | [Architecture](modules/07_architecture/README.md) | layers, repository pattern, ports and adapters | task tracker with swappable storage |
| 08 | [Errors, logging, config](modules/08_errors_logging_config/README.md) | exception design, `logging`, 12-factor config | config loader, retry helper |
| 09 | [Git and code review](modules/09_git_and_code_review/README.md) | branching, commits, pull requests, reviewing | review a flawed file |
| 10 | [Packaging and CLIs](modules/10_packaging_and_cli/README.md) | `src` layout, entry points, `argparse` | a `wordcount` command |
| 11 | [CI and Docker](modules/11_ci_and_docker/README.md) | GitHub Actions, containers, reproducible builds | pipeline + image for your CLI |
| 12 | [Capstone](modules/12_capstone/README.md) | putting it all together | build and ship `tasker` |

Modules build on each other; do them in order. Budget roughly 2–4 hours each,
and a weekend for the capstone.

## Quality checks

The same commands CI runs (see `.github/workflows/ci.yml`):

```bash
ruff check .          # lint
ruff format --check . # formatting
pytest --solutions    # reference solutions must stay green
```
