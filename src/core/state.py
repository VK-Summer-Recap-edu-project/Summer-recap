from arq.connections import ArqRedis

from core.schemas import TaskState


class TaskStateManager:
    def __init__(self, redis: ArqRedis):
        self.redis = redis

    async def get_state(self, task_id: str) -> TaskState | None:
        state = await self.redis.get(f"task:{task_id}")
        if state is not None:
            return TaskState.model_validate_json(state)
        return None

    async def set_state(self, task_id: str, state: TaskState) -> None:
        await self.redis.set(f"task:{task_id}", state.model_dump_json())
