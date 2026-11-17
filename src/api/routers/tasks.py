from fastapi.routing import APIRouter
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter(prefix="/api/tasks")


class TaskRequest(BaseModel):
    photo_ids: list[str]


@router.post("")
async def init_task(payload: TaskRequest):
    return {"task_id": uuid4()}


@router.get("/{task_id}")
async def progress(task_id: str):
    return {"status": "todo"}
