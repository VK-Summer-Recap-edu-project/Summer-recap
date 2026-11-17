import random
import time


class BaseModel:
    def __call__(self, images: list) -> list: ...


class DummyModel(BaseModel):
    def __call__(self, images: list) -> list:
        print("processing images...")
        time.sleep(random.randint(0, 4))
        return [
            {"foo": random.randint(1, 5), "bar": random.random()}
            for _ in range(len(images))
        ]
