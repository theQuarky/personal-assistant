from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1, max_length=500)
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deadline: Optional[datetime] = None
    estimated_minutes: int = Field(default=30, ge=1)
    project_id: Optional[UUID] = None


class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=200)
    description: str = ""
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Reminder(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    trigger_at: datetime
    message: str
    delivered: bool = False


class WorkloadItem(BaseModel):
    task: Task
    priority_score: float
    deadline_pressure: float


class WorkloadReport(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    available_minutes: int
    planned_minutes: int
    overload_minutes: int
    items: list[WorkloadItem]
