from ml.model import DummyModel
from adapters.base import DummyPhotoLoader
from arq.connections import ArqRedis
import json

ml_model = DummyModel()
adapter = DummyPhotoLoader()


async def process_task(ctx, task_id: str, photo_ids: list[str]):
    batch_size = 64
    num_processed = 0
    redis: ArqRedis = ctx["redis"]
    results = []
    for i in range(0, len(photo_ids), batch_size):
        batch_ids = photo_ids[i : i + batch_size]
        photos_batch = await adapter.load_photos(batch_ids)
        batch_results = ml_model(photos_batch)
        num_processed += 1
        redis.set(
            f"task:{task_id}",
            json.dumps({"status": "processing", "progress": num_processed}),
        )
        results.extend(batch_results)
    return results
