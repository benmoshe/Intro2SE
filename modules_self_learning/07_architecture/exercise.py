from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Protocol

# --- Domain ---


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TaskNotFound(LookupError):
    """Raised when a task id doesn't exist."""


# --- Port ---


class TaskRepository(Protocol):
    def add(self, title: str) -> Task:
        """Store a new, not-done task and return it. Ids start at 1 and increase."""
        ...

    def get(self, task_id: int) -> Task | None: ...

    def all(self) -> list[Task]:
        """Return every task, ordered by id."""
        ...

    def save(self, task: Task) -> None:
        """Persist changes made to an existing task."""
        ...


# --- Adapters ---


class InMemoryTaskRepository:
    """Keeps tasks in a dict. Returns copies, so changes only stick via save()."""

    def __init__(self) -> None:
        raise NotImplementedError("TODO")

    def add(self, title: str) -> Task:
        raise NotImplementedError("TODO")

    def get(self, task_id: int) -> Task | None:
        raise NotImplementedError("TODO")

    def all(self) -> list[Task]:
        raise NotImplementedError("TODO")

    def save(self, task: Task) -> None:
        raise NotImplementedError("TODO")


class SqliteTaskRepository:
    """Keeps tasks in a SQLite table, which it creates if missing."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        raise NotImplementedError("TODO")

    def add(self, title: str) -> Task:
        raise NotImplementedError("TODO")

    def get(self, task_id: int) -> Task | None:
        raise NotImplementedError("TODO")

    def all(self) -> list[Task]:
        raise NotImplementedError("TODO")

    def save(self, task: Task) -> None:
        raise NotImplementedError("TODO")


# --- Service ---


class TaskService:
    """Use cases. Knows the rules; knows nothing about how tasks are stored."""

    def __init__(self, repository: TaskRepository) -> None:
        raise NotImplementedError("TODO")

    def create(self, title: str) -> Task:
        """Create a task. Strip surrounding whitespace; reject an empty title with ValueError."""
        raise NotImplementedError("TODO")

    def complete(self, task_id: int) -> Task:
        """Mark a task done and return it. Raise TaskNotFound for an unknown id."""
        raise NotImplementedError("TODO")

    def pending(self) -> list[Task]:
        """Return the tasks that aren't done, ordered by id."""
        raise NotImplementedError("TODO")
