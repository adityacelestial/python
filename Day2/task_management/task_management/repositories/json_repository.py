import json
import logging
import os
from typing import Any, Dict, List, Optional

from filelock import FileLock

from repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class JSONRepository(BaseRepository):
    """Concrete repository that persists data in a JSON file.

    Satisfies LSP: can replace BaseRepository anywhere in the service
    layer without breaking existing behaviour.
    """

    def __init__(self, file_path: str, collection_key: str) -> None:
        self._file_path = file_path
        self._collection_key = collection_key
        self._lock_path = f"{file_path}.lock"
        self._ensure_file()

    # ──────────────── private helpers ────────────────

    def _ensure_file(self) -> None:
        """Create the JSON file with an empty collection if missing or corrupt."""
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        if not os.path.exists(self._file_path):
            self._write({self._collection_key: []})
            logger.info("Created data file: %s", self._file_path)
            return
        try:
            self._read()
        except (json.JSONDecodeError, KeyError):
            logger.error("Corrupt data file %s – recreating.", self._file_path)
            self._write({self._collection_key: []})

    def _read(self) -> Dict[str, Any]:
        with open(self._file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if self._collection_key not in data:
            raise KeyError(self._collection_key)
        return data

    def _write(self, data: Dict[str, Any]) -> None:
        with FileLock(self._lock_path):
            tmp = self._file_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, default=str)
            os.replace(tmp, self._file_path)

    def _next_id(self, records: List[Dict[str, Any]]) -> int:
        return max((r["id"] for r in records), default=0) + 1

    # ──────────────── BaseRepository interface ────────────────

    def find_all(self) -> List[Dict[str, Any]]:
        return self._read()[self._collection_key]

    def find_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        return next(
            (r for r in self.find_all() if r["id"] == record_id), None
        )

    def save(self, record: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        records = data[self._collection_key]
        record["id"] = self._next_id(records)
        records.append(record)
        self._write(data)
        return record

    def update(self, record_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = self._read()
        records = data[self._collection_key]
        for i, rec in enumerate(records):
            if rec["id"] == record_id:
                records[i] = {**rec, **updates}
                self._write(data)
                return records[i]
        return None

    def delete(self, record_id: int) -> bool:
        data = self._read()
        records = data[self._collection_key]
        new_records = [r for r in records if r["id"] != record_id]
        if len(new_records) == len(records):
            return False
        data[self._collection_key] = new_records
        self._write(data)
        return True
