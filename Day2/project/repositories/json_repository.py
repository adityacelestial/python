import json
import os
from .base_repository import BaseRepository

class JSONRepository(BaseRepository):

    def __init__(self, file_path: str, key: str):
        self.file_path = file_path
        self.key = key
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({self.key: []}, f)

    def _read(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_all(self):
        return self._read()[self.key]

    def save(self, item):
        data = self._read()
        data[self.key].append(item)
        self._write(data)

    def find_by_id(self, item_id):
        items = self.get_all()
        return next((i for i in items if i["id"] == item_id), None)

    def delete(self, item_id):
        data = self._read()
        data[self.key] = [i for i in data[self.key] if i["id"] != item_id]
        self._write(data)