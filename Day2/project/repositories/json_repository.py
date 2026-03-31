import json
import os
from datetime import datetime


class JSONRepository:
    def __init__(self, file_path: str, root_key: str):
        self.file_path = file_path
        self.root_key = root_key
        self._ensure_file()

    def _ensure_file(self):
        """Ensure the JSON file exists; if not, create it."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({self.root_key: []}, f)

    def _read(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_all(self, filters=None):
        items = self._read()[self.root_key]
        if not filters:
            return items

        filtered = []
        for item in items:
            match = True
            for k, v in filters.items():
                if v is not None and item.get(k) != v:
                    match = False
                    break
            if match:
                filtered.append(item)

        return filtered

    def get_by_id(self, item_id):
        items = self._read()[self.root_key]
        return next((i for i in items if i["id"] == item_id), None)

    def create(self, data):
        db = self._read()
        items = db[self.root_key]

        next_id = max([i["id"] for i in items], default=0) + 1

        new_item = {
            **data,
            "id": next_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        items.append(new_item)
        self._write(db)
        return new_item

    def update(self, item_id, new_data):
        db = self._read()
        items = db[self.root_key]

        for item in items:
            if item["id"] == item_id:
                item.update(new_data)
                item["updated_at"] = datetime.utcnow().isoformat()
                self._write(db)
                return item

        return None

    def delete(self, item_id):
        db = self._read()
        items = db[self.root_key]

        db[self.root_key] = [i for i in items if i["id"] != item_id]
        self._write(db)