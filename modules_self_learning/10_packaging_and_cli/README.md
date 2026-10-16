# 10 — Packaging and command-line interfaces

**Goal:** turn a folder of Python files into something another person can
install and run with one command.

## Project layout

The `src` layout is the standard for installable projects:

```
wordcount/
├── pyproject.toml
├── README.md
├── src/
│   └── wordcount/
│       ├── __init__.py
│       ├── cli.py          argument parsing, printing, exit codes
│       └── counting.py     the actual logic — no I/O
└── tests/
    └── test_counting.py
```

Putting the package under `src/` means tests can only import it once it's
*installed*, so they exercise the same thing your users get — not whatever
happens to be lying in the current directory.

Note the split inside the package: `cli.py` is the interface layer,
`counting.py` is the logic. Module 07 again, in miniature.

## `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "wordcount"
version = "1.0.0"
description = "Count lines, words and characters in files."
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8", "ruff", "mypy"]

[project.scripts]
wordcount = "wordcount.cli:main"
```

- `dependencies` — what the package needs to *run*. Give lower bounds
  (`requests>=2.31`), not exact pins: a library must coexist with others.
- `optional-dependencies.dev` — what you need to *work on* it.
- `[project.scripts]` — creates a `wordcount` command that calls `main()` in
  `wordcount/cli.py`. This is an **entry point**.

```bash
pip install -e ".[dev]"   # editable install: code changes take effect immediately
wordcount README.md       # the command now exists
python -m build           # produce a wheel and sdist in dist/ (pip install build)
```

**Libraries** declare loose ranges. **Applications** you deploy should also
commit a *lock file* of exact versions (`pip-compile`, `uv lock`, `poetry lock`)
so every environment installs precisely the same thing.

## Versioning

Semantic versioning — `MAJOR.MINOR.PATCH`:

- **PATCH** — bug fixes; safe to upgrade.
- **MINOR** — new features, backwards compatible.
- **MAJOR** — something existing callers rely on has changed or gone.

## Writing a CLI with `argparse`

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wordcount", description="...")
    parser.add_argument("files", nargs="+", help="files to count")
    parser.add_argument("-l", "--lines", action="store_true", help="print the line count")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ...
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Three conventions that make a CLI testable and well-behaved:

1. **`main` takes `argv` and returns an exit code.** Tests call
   `main(["file.txt", "--lines"])` directly — no subprocess needed.
2. **Results go to stdout, errors go to stderr.** So `wordcount f.txt > out`
   doesn't mix diagnostics into the data.
3. **Exit code `0` means success, non-zero means failure.** Shell scripts and
   CI depend on it.

`argparse` gives you `--help` for free and exits with code 2 on bad usage.
For larger CLIs, look at `click` or `typer`.

## Exercise

Implement a small `wc` clone in `exercise.py`:

```
$ wordcount notes.txt
2 3 16 notes.txt
$ wordcount --words a.txt b.txt
3 a.txt
1 b.txt
```

- Columns are always in the order lines, words, characters, then the file name.
- With no flags, print all three. With flags, print only those requested.
- A file that can't be read: message on stderr, carry on with the rest, exit code 1.

Keep the counting in `count(text)` and the I/O in `main` — the tests check both.

```bash
pytest modules/10_packaging_and_cli
```

**Stretch:** copy your solution into a real `src`-layout project with the
`pyproject.toml` above, `pip install -e .`, and run `wordcount` from your shell.

## Check yourself

- Why does `main` accept `argv` instead of reading `sys.argv` itself?
- Why would a library pin `requests>=2.31` but an application lock `requests==2.32.3`?
- You renamed a public function. Which version number changes?
