import asyncio
from unittest.mock import AsyncMock

import pytest
from fakeredis import FakeAsyncRedis
from httpx import ASGITransport, AsyncClient

from api.main import app
from core.state import TaskStateManager
from worker.worker import process_task


@pytest.fixture
async def fake_redis():
    redis = FakeAsyncRedis()

    # Mock ARQ's custom enqueue method
    redis.enqueue_job = AsyncMock(return_value=None)  # pyright: ignore[reportAttributeAccessIssue]

    yield redis
    await redis.aclose()


# 2. Setup the FastAPI test client with the mocked Redis
@pytest.fixture
async def client(fake_redis):
    # Override the app state so routers use the fake Redis
    app.state.redis = fake_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# --- TESTS ---


@pytest.mark.asyncio
async def test_api_task_creation_and_polling(client, fake_redis):
    # 1. Test initiator
    post_response = await client.post(
        "/api/tasks", json={"photo_ids": ["img1.jpg", "img2.jpg"]}
    )
    assert post_response.status_code == 200

    task_id = post_response.json()["task_id"]
    assert task_id is not None

    # 2. Test progress polling
    get_response = await client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 200

    state = get_response.json()
    assert state["status"] == "queued"
    assert state["progress"] == 0


@pytest.mark.asyncio
async def test_worker_fsm_transitions(fake_redis):
    task_id = "test-uuid-123"
    num_images = 10
    photo_ids = [f"img{i}.jpg" for i in range(num_images)]

    ctx = {"redis": fake_redis}
    manager = TaskStateManager(fake_redis)

    # Start the worker in the background
    worker_task = asyncio.create_task(process_task(ctx, task_id, photo_ids))

    # Wait for the first "processing" state
    await asyncio.sleep(0.1)

    # Assert the intermediate state
    mid_state = await manager.get_state(task_id)
    assert mid_state is not None
    assert mid_state.status == "processing"

    # Wait for the worker to finish, enforcing a strict timeout
    try:
        await asyncio.wait_for(worker_task, timeout=5.0)
    except asyncio.TimeoutError:
        pytest.fail("Worker timed out")

    # Assert the final state
    final_state = await manager.get_state(task_id)
    assert final_state is not None
    assert final_state.status == "done"
    assert final_state.progress == num_images
