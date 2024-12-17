import os
import shutil
from collections.abc import Generator
from pathlib import Path

from flask import current_app

from configs import dify_config
from extensions.storage.base_storage import BaseStorage
from patch.extensions import storage_utils

class LocalFsStorage(BaseStorage):
    """Implementation for local filesystem storage."""

    def __init__(self):
        super().__init__()
        folder = dify_config.STORAGE_LOCAL_PATH
        if not os.path.isabs(folder):
            folder = os.path.join(current_app.root_path, folder)
        self.folder = folder

    def _build_filepath(self, filename: str) -> str:
        """Build the full file path based on the folder and filename."""
        if not self.folder or self.folder.endswith("/"):
            return self.folder + filename
        else:
            return self.folder + "/" + filename

    def save(self, filename, data):
        filepath = self._build_filepath(filename)
        folder = os.path.dirname(filepath)
        os.makedirs(folder, exist_ok=True)
        storage_utils.ls_save(filepath, data)  

    def load_once(self, filename: str) -> bytes:
        filepath = self._build_filepath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError("File not found")
        return storage_utils.ls_load_once(filepath)

    def load_stream(self, filename: str) -> Generator:
        filepath = self._build_filepath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError("File not found")
        yield storage_utils.ls_load_stream(filename)

    def download(self, filename, target_filepath):
        filepath = self._build_filepath(filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError("File not found")
        storage_utils.ls_download(filepath, target_filepath)

    def exists(self, filename):
        filepath = self._build_filepath(filename)
        return os.path.exists(filepath)

    def delete(self, filename):
        filepath = self._build_filepath(filename)
        if os.path.exists(filepath):
            os.remove(filepath)
