from __future__ import annotations

import sqlite3
from dataclasses import dataclass, replace
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
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self._tasks[task.id] = task
        self._next_id += 1
        return replace(task)

    def get(self, task_id: int) -> Task | None:
        task = self._tasks.get(task_id)
        return replace(task) if task else None

    def all(self) -> list[Task]:
        return [replace(self._tasks[task_id]) for task_id in sorted(self._tasks)]

    def save(self, task: Task) -> None:
        self._tasks[task.id] = replace(task)


class SqliteTaskRepository:
    """Keeps tasks in a SQLite table, which it creates if missing."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, "
            "done INTEGER NOT NULL DEFAULT 0)"
        )
        self._connection.commit()

    def add(self, title: str) -> Task:
        cursor = self._connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        self._connection.commit()
        assert cursor.lastrowid is not None
        return Task(id=cursor.lastrowid, title=title)

    def get(self, task_id: int) -> Task | None:
        row = self._connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return self._to_task(row) if row else None

    def all(self) -> list[Task]:
        rows = self._connection.execute("SELECT id, title, done FROM tasks ORDER BY id")
        return [self._to_task(row) for row in rows]

    def save(self, task: Task) -> None:
        self._connection.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (task.title, int(task.done), task.id),
        )
        self._connection.commit()

    @staticmethod
    def _to_task(row: tuple[int, str, int]) -> Task:
        task_id, title, done = row
        return Task(id=task_id, title=title, done=bool(done))


# --- Service ---


class TaskService:
    """Use cases. Knows the rules; knows nothing about how tasks are stored."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        return self._repository.add(title)

    def complete(self, task_id: int) -> Task:
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFound(f"no task with id {task_id}")
        task.done = True
        self._repository.save(task)
        return task

    def pending(self) -> list[Task]:
        return [task for task in self._repository.all() if not task.done]
