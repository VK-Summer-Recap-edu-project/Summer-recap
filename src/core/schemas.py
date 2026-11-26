from typing import Literal, Optional

from pydantic import BaseModel


class LoadedPhoto(BaseModel):
    id: str
    bytes: bytes


class FailedPhoto(BaseModel):
    id: str
    reason: str


class TaskState(BaseModel):
    status: Literal["queued", "processing", "done"]
    progress: int
    results: Optional[list] = None
