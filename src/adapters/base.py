import numpy as np


class BasePhotoLoader:
    async def load_photos(self, photo_ids: list[str]) -> list: ...


class DummyPhotoLoader(BasePhotoLoader):
    async def load_photos(self, photo_ids: list[str]) -> list:
        return np.random.random((len(photo_ids), 32, 32)).tolist()
