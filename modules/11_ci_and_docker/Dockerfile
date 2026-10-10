# Template for a src-layout project with a [project.scripts] entry point
# named "wordcount" (see module 10). Copy it to that project's root.

FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

RUN useradd --create-home appuser
USER appuser

ENTRYPOINT ["wordcount"]
