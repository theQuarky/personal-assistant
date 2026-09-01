from datetime import datetime, timedelta, timezone

from assistant.core.models import Priority, Task
from assistant.core.workload import build_report


def test_overload_is_detected():
    now = datetime.now(timezone.utc)
    tasks = [
        Task(title="A", estimated_minutes=120, priority=Priority.HIGH, deadline=now + timedelta(hours=2)),
        Task(title="B", estimated_minutes=120, priority=Priority.MEDIUM),
    ]
    report = build_report(tasks, available_minutes=180, now=now)
    assert report.planned_minutes == 240
    assert report.overload_minutes == 60
    assert report.items[0].task.title == "A"


def test_no_deadline_has_no_deadline_pressure():
    task = Task(title="A")
    report = build_report([task], available_minutes=60)
    assert report.items[0].deadline_pressure == 0
