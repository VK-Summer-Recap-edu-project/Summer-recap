import json
import logging

from arq.connections import ArqRedis

from adapters.base import DummyPhotoLoader
from ml.model import DummyModel

ml_model = DummyModel()
adapter = DummyPhotoLoader()
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


async def process_task(ctx, task_id: str, photo_ids: list[str]):
    batch_size = 64
    num_processed = 0
    redis: ArqRedis = ctx["redis"]
    results = []
    logging.debug(f"processing job {task_id}")
    for i in range(0, len(photo_ids), batch_size):
        logging.debug(f"starting batch {i}")
        batch_ids = photo_ids[i : i + batch_size]
        photos_batch = await adapter.load_photos(batch_ids)
        batch_results = ml_model(photos_batch)
        num_processed += 1
        await redis.set(
            f"task:{task_id}",
            json.dumps({"status": "processing", "progress": num_processed}),
        )
        results.extend(batch_results)
    logging.debug(f"finishing job {task_id}")
    await redis.set(
        f"task:{task_id}",
        json.dumps({"status": "done", "progress": num_processed, "results": results}),
    )
