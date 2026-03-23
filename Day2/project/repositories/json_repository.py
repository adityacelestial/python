import json
import os
from datetime import datetime
from .base_repository import BaseRepository

class JSONRepository(BaseRepository):
    def __init__(self, file_path, root_key):
        self.file_path = file_path
        self.root_key = root_key
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({self.root_key: []}, f)

    def _read(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4, default=str)

    def get_all(self):
        return self._read()[self.root_key]

    def get_by_id(self, item_id):
        items = self.get_all()
        for item in items:
            if item["id"] == item_id:
                return item
        return None

    def create(self, data):
        db = self._read()
        items = db[self.root_key]

        data["id"] = len(items) + 1
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()

        items.append(data)
        self._write(db)
        return data

    def update(self, item_id, new_data):
        db = self._read()
        items = db[self.root_key]

        for item in items:
            if item["id"] == item_id:
                item.update(new_data)
                item["updated_at"] = datetime.utcnow()
                self._write(db)
                return item
        return None

    def delete(self, item_id):
        db = self._read()
        items = db[self.root_key]

        db[self.root_key] = [i for i in items if i["id"] != item_id]
        self._write(db)