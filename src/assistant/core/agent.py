from __future__ import annotations

from datetime import datetime

from assistant.core.models import Priority, Task
from assistant.core.store import TaskStore


class AssistantCore:
    def __init__(self, db_path: str = "~/.local/share/personal-assistant/assistant.db"):
        from pathlib import Path
        self.store = TaskStore(Path(db_path).expanduser())

    def create_task(
        self,
        title: str,
        *,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        deadline: datetime | None = None,
        estimated_minutes: int = 30,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            estimated_minutes=estimated_minutes,
        )
        return self.store.add(task)
