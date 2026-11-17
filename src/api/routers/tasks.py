import json
import logging
from uuid import uuid4

from arq.connections import ArqRedis
from fastapi import HTTPException, Request
from fastapi.routing import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/tasks")
logger = logging.getLogger(__name__)


class TaskRequest(BaseModel):
    photo_ids: list[str]


@router.post("")
async def init_task(payload: TaskRequest, request: Request):
    redis: ArqRedis = request.app.state.redis
    task_id = uuid4()
    initial_state = {"status": "queued", "progress": 0}
    await redis.set(f"task:{task_id}", json.dumps(initial_state))
    logger.debug(f"Started task {task_id}")
    await redis.enqueue_job("process_task", task_id, payload.photo_ids)
    return {"task_id": task_id}


@router.get("/{task_id}")
async def progress(task_id: str, request: Request):
    redis: ArqRedis = request.app.state.redis
    state = await redis.get(f"task:{task_id}")
    if not state:
        raise HTTPException(status_code=404, detail="Task not found")

    return json.loads(state)
