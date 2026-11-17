from pathlib import Path

import pytest

from adapters.photo_loaders import LocalPhotoLoader


@pytest.mark.asyncio
async def test_local_adapter_loads_and_fails_correctly(tmp_path: Path):
    # 1. Setup actual dummy files in the OS temporary directory
    photo1 = tmp_path / "photo1.jpg"
    photo2 = tmp_path / "photo2.jpg"
    photo1.write_bytes(b"foo")
    photo2.write_bytes(b"bar")

    adapter = LocalPhotoLoader(base_dir=tmp_path)
    photo_ids = ["photo1.jpg", "photo2.jpg"]
    loaded_bytes = await adapter.load_photos(photo_ids)
    assert len(loaded_bytes) == 2
    assert loaded_bytes[0] == b"foo"
    assert loaded_bytes[1] == b"bar"
