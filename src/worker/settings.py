from worker.worker import process_task
from arq.connections import RedisSettings


class WorkerSettings:
    functions = [process_task]
    redis_settings = RedisSettings(host="localhost", port=6379)
