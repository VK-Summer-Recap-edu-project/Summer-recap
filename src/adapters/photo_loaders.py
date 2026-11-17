# TODO: broken photos mustn't crash anything
import asyncio
import os
from pathlib import Path

import numpy as np


class BasePhotoLoader:
    async def load_photos(self, photo_ids: list[str]) -> list: ...


class DummyPhotoLoader(BasePhotoLoader):
    async def load_photos(self, photo_ids: list[str]) -> list:
        return np.random.random((len(photo_ids), 32, 32)).tolist()


class LocalPhotoLoader(BasePhotoLoader):
    def __init__(self, base_dir: os.PathLike):
        self.base_dir = Path(base_dir)

    async def load_photos(self, photo_ids: list[str]) -> list:
        return await asyncio.to_thread(self._read_files, photo_ids)

    def _read_files(self, photo_ids: list[str]) -> list:
        photo_bytes = []
        for photo_id in photo_ids:
            photo_bytes.append((self.base_dir / photo_id).read_bytes())
        return photo_bytes
