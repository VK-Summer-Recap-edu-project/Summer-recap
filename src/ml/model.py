import random
import time


class BaseModel:
    def __call__(self, images: list) -> list: ...


class DummyModel(BaseModel):
    def __call__(self, images: list) -> list:
        print("processing images...")
        time.sleep(random.random())
        return [
            {"foo": random.randint(1, 5), "bar": random.random()}
            for _ in range(len(images))
        ]
