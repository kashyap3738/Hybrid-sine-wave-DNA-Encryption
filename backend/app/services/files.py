import shutil
from pathlib import Path

from fastapi import UploadFile

from ..config import MEDIA_DIRS


def init_directories():
    for directory in MEDIA_DIRS.values():
        directory.mkdir(exist_ok=True)


def save_upload(upload: UploadFile, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    return destination
