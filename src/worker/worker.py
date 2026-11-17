import asyncio
import logging

from arq.connections import ArqRedis

from adapters.photo_loaders import DummyPhotoLoader
from core.schemas import TaskState
from core.state import TaskStateManager
from ml.model import DummyModel

ml_model = DummyModel()
adapter = DummyPhotoLoader()
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


async def process_task(ctx, task_id: str, photo_ids: list[str]):
    batch_size = 64
    num_processed = 0
    redis: ArqRedis = ctx["redis"]
    state_manager = TaskStateManager(redis)
    results = []
    logging.debug(f"processing job {task_id}")
    for i in range(0, len(photo_ids), batch_size):
        logging.debug(f"starting batch {i}")
        await state_manager.set_state(
            task_id,
            TaskState(status="processing", progress=num_processed),
        )
        batch_ids = photo_ids[i : i + batch_size]
        photos_batch = await adapter.load_photos(batch_ids)
        batch_results = await asyncio.to_thread(ml_model, photos_batch)
        num_processed += len(batch_ids)
        results.extend(batch_results)
    logging.debug(f"finishing job {task_id}")
    await state_manager.set_state(
        task_id,
        TaskState(status="done", progress=num_processed, results=results),
    )
