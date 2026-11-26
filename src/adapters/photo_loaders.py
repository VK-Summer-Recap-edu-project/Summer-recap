import asyncio
import os
from pathlib import Path

import numpy as np

from core.schemas import FailedPhoto, LoadedPhoto


class BasePhotoLoader:
    async def load_photos(
        self, photo_ids: list[str]
    ) -> tuple[list[LoadedPhoto], list[FailedPhoto]]: ...


class DummyPhotoLoader(BasePhotoLoader):
    async def load_photos(
        self, photo_ids: list[str]
    ) -> tuple[list[LoadedPhoto], list[FailedPhoto]]:
        num_failed = np.random.randint(1, len(photo_ids))
        failed_ids = np.random.choice(photo_ids, num_failed, replace=False).tolist()
        failed = [FailedPhoto(id=id, reason="womp womp") for id in failed_ids]
        loaded = [
            LoadedPhoto(id=str(id), bytes=data.tobytes())
            for id, data in enumerate(
                np.random.random((len(photo_ids) - num_failed, 32, 32))
            )
        ]
        return (
            loaded,
            failed,
        )


class LocalPhotoLoader(BasePhotoLoader):
    def __init__(self, base_dir: os.PathLike):
        self.base_dir = Path(base_dir)

    async def load_photos(
        self, photo_ids: list[str]
    ) -> tuple[list[LoadedPhoto], list[FailedPhoto]]:
        return await asyncio.to_thread(self._read_files, photo_ids)

    def _read_files(
        self, photo_ids: list[str]
    ) -> tuple[list[LoadedPhoto], list[FailedPhoto]]:
        photos_bytes = []
        failed_photos = []
        for photo_id in photo_ids:
            photo_path = self.base_dir / photo_id
            try:
                photos_bytes.append(
                    LoadedPhoto(id=photo_id, bytes=photo_path.read_bytes())
                )
            except Exception as e:
                failed_photos.append(FailedPhoto(id=photo_id, reason=str(e)))

        return photos_bytes, failed_photos
