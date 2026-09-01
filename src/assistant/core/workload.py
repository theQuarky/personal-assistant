from __future__ import annotations

from datetime import datetime, timezone

from assistant.core.models import Priority, Task, WorkloadItem, WorkloadReport

_PRIORITY = {
    Priority.LOW: 1.0,
    Priority.MEDIUM: 2.0,
    Priority.HIGH: 3.5,
    Priority.CRITICAL: 5.0,
}


def workload_score(task: Task, now: datetime | None = None) -> tuple[float, float]:
    """Return (score, deadline pressure).

    This intentionally stays deterministic. The LLM may suggest priorities, but
    the application remains responsible for the final scheduling calculation.
    """
    now = now or datetime.now(timezone.utc)
    base = _PRIORITY[task.priority]

    if not task.deadline:
        return base, 0.0

    deadline = task.deadline
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    hours = (deadline - now).total_seconds() / 3600

    if hours <= 0:
        pressure = 5.0
    elif hours <= 6:
        pressure = 4.5
    elif hours <= 24:
        pressure = 3.5
    elif hours <= 72:
        pressure = 2.0
    elif hours <= 168:
        pressure = 1.0
    else:
        pressure = 0.25

    return base + pressure, pressure


def build_report(tasks: list[Task], available_minutes: int, now: datetime | None = None) -> WorkloadReport:
    now = now or datetime.now(timezone.utc)
    items = []
    for task in tasks:
        score, pressure = workload_score(task, now)
        items.append(WorkloadItem(task=task, priority_score=score, deadline_pressure=pressure))

    items.sort(key=lambda item: (-item.priority_score, item.task.deadline is None, item.task.deadline or now))
    planned = sum(item.task.estimated_minutes for item in items)

    return WorkloadReport(
        available_minutes=available_minutes,
        planned_minutes=planned,
        overload_minutes=max(0, planned - available_minutes),
        items=items,
    )
