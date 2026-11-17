from typing import Literal, Optional

from pydantic import BaseModel


class TaskState(BaseModel):
    status: Literal["queued", "processing", "done"]
    progress: int
    results: Optional[list] = None
