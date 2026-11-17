from arq.connections import RedisSettings

from worker.worker import process_task


class WorkerSettings:
    functions = [process_task]
    redis_settings = RedisSettings(host="localhost", port=6379)
