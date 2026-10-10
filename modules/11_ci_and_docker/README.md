# 11 — Continuous integration and Docker

**Goal:** have every change checked automatically, and package your
application so it runs the same everywhere.

This module has no pytest exercise; you'll write configuration and watch it run.

## Continuous integration

CI means a server runs your checks on every push and pull request. Its job is
to make "it works on my machine" irrelevant: the question becomes "is CI green?"

Open `.github/workflows/ci.yml` at the root of this repository — it's a real,
working pipeline for this course:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: ruff check .
      - run: ruff format --check .
      - run: pytest --solutions
```

Reading it top to bottom:

- **`on`** — when to run: pushes to `main`, and every pull request.
- **`jobs.check.runs-on`** — a fresh virtual machine each time. Nothing
  carries over, so the build can't depend on leftovers.
- **`strategy.matrix`** — run the whole job once per Python version you support.
- **`steps`** — check out the code, install Python, install dependencies, run
  the checks. Any step exiting non-zero fails the build — which is why exit
  codes mattered in module 10.

Principles:

- **CI runs the same commands you run locally.** If it fails in CI, you can
  reproduce it with one line. A `Makefile` or task runner keeps the two in sync.
- **Fast first.** Lint in seconds before tests in minutes; fail early.
- **Keep it under ten minutes.** Slow pipelines get ignored or bypassed.
- **Never merge on red.** Protect `main` so a green build is required.
- **A flaky test is a bug.** Fix or delete it; don't re-run until green.

**Continuous delivery** extends the pipeline: when `main` is green, build the
artifact (a wheel, a container image) and deploy it automatically. Secrets
used for deployment live in the CI system's secret store — never in the
workflow file.

## Docker

A container image packages your application *with* its interpreter and
dependencies. The image you test is, byte for byte, the image you ship.

`Dockerfile` in this folder is a template for a `src`-layout project like the
one from module 10:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

RUN useradd --create-home appuser
USER appuser

ENTRYPOINT ["wordcount"]
```

- **`FROM python:3.12-slim`** — pin the base image version; `latest` changes under you.
- **Layers are cached.** Each instruction is a layer, rebuilt only when its
  inputs change. Copy what changes least first.
- **`--no-cache-dir`** — keeps pip's download cache out of the image.
- **`USER appuser`** — don't run as root inside the container.
- **`ENTRYPOINT`** — the command the container runs; arguments are appended.

```bash
docker build -t wordcount .
docker run --rm -v "$PWD:/data" wordcount /data/README.md
```

Add a `.dockerignore` (`.venv`, `.git`, `__pycache__`, `tests`) so they
aren't sent to the build. Configuration reaches a container through
environment variables (`docker run -e APP_PORT=5000 …`) — exactly what
module 08's `load_config` expects. Never bake secrets into an image.

## Exercise

Using the `src`-layout project from module 10's stretch task (create it now
if you skipped it):

1. **Pipeline.** Put the project in a GitHub repository. Add a workflow that
   runs `ruff check`, `ruff format --check`, `mypy` and `pytest` on every
   push and pull request, across two Python versions.
2. **See it fail.** Open a pull request with a deliberately broken test.
   Read the CI output and find the failing assertion. Fix it; watch it go green.
3. **Protect `main`.** In the repository settings, require the check to pass
   before merging.
4. **Container.** Copy the `Dockerfile` in, add a `.dockerignore`, build the
   image, and run your CLI through it on a file from your machine.
5. **Stretch.** Add a second CI job that builds the Docker image, and runs
   only if the checks job succeeded (`needs: check`).

## Check yourself

- Why does each CI run start from a clean machine?
- What goes wrong if dependencies are installed *after* `COPY src`, and you change one source line?
- Your pipeline takes 25 minutes. Name two ways to shorten it.
