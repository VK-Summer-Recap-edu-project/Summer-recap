import logging
from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI

from api.routers import tasks

logging.basicConfig(
    level=logging.DEBUG,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await create_pool(RedisSettings(host="localhost", port=6379))
    yield
    await app.state.redis.close()


app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)
