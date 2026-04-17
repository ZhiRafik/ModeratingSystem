from abc import ABC, abstractmethod
from domain.entities.rule_result import RuleResult


class Rule(ABC):
    """Абстрактный базовый класс для всех правил"""

    def __init__(self, name: str, priority: int = 0, enabled: bool = True):
        self.name = name
        self.priority = priority
        self.enabled = enabled

    @abstractmethod
    def check(self, text: str) -> RuleResult:
        """Проверяет текст и возвращает результат"""
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} priority={self.priority}>"