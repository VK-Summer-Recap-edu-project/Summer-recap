# TODO: broken photos mustn't crash anything
import asyncio
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class FailedPhoto:
    id: str
    reason: str


class BasePhotoLoader:
    async def load_photos(self, photo_ids: list[str]) -> tuple[list, list[FailedPhoto]]:
        """Returns: (bytes_loaded, failed_ids)"""
        ...


class DummyPhotoLoader(BasePhotoLoader):
    async def load_photos(self, photo_ids: list[str]) -> tuple[list, list[FailedPhoto]]:
        num_failed = np.random.randint(1, len(photo_ids))
        failed_ids = np.random.choice(photo_ids, num_failed, replace=False).tolist()
        failed = [FailedPhoto(id, "womp womp") for id in failed_ids]
        return (
            np.random.random((len(photo_ids) - num_failed, 32, 32)).tolist(),
            failed,
        )


class LocalPhotoLoader(BasePhotoLoader):
    def __init__(self, base_dir: os.PathLike):
        self.base_dir = Path(base_dir)

    async def load_photos(self, photo_ids: list[str]) -> tuple[list, list[FailedPhoto]]:
        return await asyncio.to_thread(self._read_files, photo_ids)

    def _read_files(self, photo_ids: list[str]) -> tuple[list, list[FailedPhoto]]:
        photos_bytes = []
        failed_photos = []
        for photo_id in photo_ids:
            photo_path = self.base_dir / photo_id
            try:
                photos_bytes.append(photo_path.read_bytes())
            except Exception as e:
                failed_photos.append(FailedPhoto(photo_id, str(e)))

        return photos_bytes, failed_photos
