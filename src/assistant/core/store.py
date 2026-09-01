from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from assistant.core.models import Task, TaskStatus


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL,
    deadline TEXT,
    estimated_minutes INTEGER NOT NULL,
    project_id TEXT
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline);
"""


class TaskStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, task: Task) -> Task:
        with self.connect() as conn:
            conn.execute(
                """INSERT INTO tasks
                (id,title,description,status,priority,created_at,deadline,estimated_minutes,project_id)
                VALUES (?,?,?,?,?,?,?,?,?)""",
                (str(task.id), task.title, task.description, task.status.value,
                 task.priority.value, task.created_at.isoformat(),
                 task.deadline.isoformat() if task.deadline else None,
                 task.estimated_minutes, str(task.project_id) if task.project_id else None),
            )
        return task

    def list_open(self) -> list[Task]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status IN (?, ?) ORDER BY deadline IS NULL, deadline",
                (TaskStatus.TODO.value, TaskStatus.IN_PROGRESS.value),
            ).fetchall()
        return [Task.model_validate(dict(row) | {"id": row["id"]}) for row in rows]

    def complete(self, task_id: str) -> bool:
        with self.connect() as conn:
            cur = conn.execute("UPDATE tasks SET status=? WHERE id=?", (TaskStatus.DONE.value, task_id))
            return cur.rowcount == 1
