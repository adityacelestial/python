from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRepository(ABC):
    """Abstract base repository defining the data-access contract.

    Services depend on this abstraction (DIP), and any concrete
    implementation (JSONRepository, DBRepository, …) can replace
    another without affecting the service layer (LSP).
    """

    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        """Return every record in the store."""

    @abstractmethod
    def find_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Return a single record by its id, or None if absent."""

    @abstractmethod
    def save(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Persist a new record and return it with its generated id."""

    @abstractmethod
    def update(self, record_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing record and return the updated version."""

    @abstractmethod
    def delete(self, record_id: int) -> bool:
        """Delete a record by id. Returns True if found and removed."""
