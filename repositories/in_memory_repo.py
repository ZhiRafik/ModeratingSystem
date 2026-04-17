# repositories/in_memory_repo.py
from typing import List, Optional, Dict
from domain.entities.moderation_result import ModerationResult


class InMemoryRepository:
    def __init__(self):
        self._storage: Dict[int, ModerationResult] = {}  # Словарь!
        self._next_id = 1

    def save(self, result: ModerationResult) -> ModerationResult:
        """Сохранить результат и вернуть его с ID"""
        result.id = self._next_id
        self._storage[self._next_id] = result  # O(1)
        self._next_id += 1
        return result

    def get_by_id(self, record_id: int) -> Optional[ModerationResult]:
        """Найти по ID - O(1)"""
        return self._storage.get(record_id)

    def get_all(self) -> List[ModerationResult]:
        """Получить все результаты - O(n)"""
        return list(self._storage.values())

    def get_recent(self, limit: int = 10) -> List[ModerationResult]:
        """Последние N результатов - O(n log n)"""
        # Сортируем по id (чем больше id, тем новее)
        sorted_ids = sorted(self._storage.keys(), reverse=True)
        return [self._storage[id] for id in sorted_ids[:limit]]

    def clear(self):
        """Очистить"""
        self._storage.clear()
        self._next_id = 1