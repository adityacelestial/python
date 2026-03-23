from abc import ABC, abstractmethod
from typing import List, Dict

class BaseRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Dict]:
        pass

    @abstractmethod
    def save(self, data: Dict):
        pass

    @abstractmethod
    def find_by_id(self, item_id: int) -> Dict:
        pass

    @abstractmethod
    def delete(self, item_id: int):
        pass