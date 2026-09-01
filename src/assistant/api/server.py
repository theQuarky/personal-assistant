from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from assistant.core.agent import AssistantCore
from assistant.core.models import Priority
from assistant.core.workload import build_report

app = FastAPI(title="Personal Assistant", version="0.1.0")
core = AssistantCore()


class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    deadline: datetime | None = None
    estimated_minutes: int = 30


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks")
def create_task(request: CreateTaskRequest):
    return core.create_task(**request.model_dump())


@app.get("/tasks")
def list_tasks():
    return core.store.list_open()


@app.get("/workload")
def workload(available_minutes: int = 480):
    return build_report(core.store.list_open(), available_minutes)
