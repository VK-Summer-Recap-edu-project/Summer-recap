from pathlib import Path

import pytest

from adapters.photo_loaders import LocalPhotoLoader


@pytest.mark.asyncio
async def test_local_adapter_loads_and_fails_correctly(tmp_path: Path):
    # 1. Setup actual dummy files in the OS temporary directory
    photo1 = tmp_path / "photo1.jpg"
    photo1.write_bytes(b"foo")

    adapter = LocalPhotoLoader(base_dir=tmp_path)
    photo_ids = ["photo1.jpg", "photo2.jpg"]
    loaded_bytes, failed_ids = await adapter.load_photos(photo_ids)
    assert len(loaded_bytes) == 1
    assert loaded_bytes[0].bytes == b"foo"
    assert len(failed_ids) == 1
    assert failed_ids[0].id == "photo2.jpg"
