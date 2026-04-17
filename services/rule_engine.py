from typing import List, Optional
from domain.entities.rule import Rule
from domain.entities.rule_result import RuleResult


class RuleEngine:
    """Движок для выполнения правил"""

    def __init__(self):
        self.rules: List[Rule] = []

    def add_rule(self, rule: Rule) -> None:
        """Добавить правило"""
        self.rules.append(rule)
        self._sort_by_priority()

    def remove_rule(self, rule_name: str) -> bool:
        """Удалить правило по имени"""
        for rule in self.rules:
            if rule.name == rule_name:
                self.rules.remove(rule)
                return True
        return False

    def get_rule(self, rule_name: str) -> Optional[Rule]:
        """Получить правило по имени"""
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None

    def _sort_by_priority(self):
        self.rules.sort(key=lambda r: r.priority)

    def execute(self, text: str) -> List[RuleResult]:
        """Выполнить все включённые правила"""
        results = []
        for rule in self.rules:
            if rule.enabled:
                results.append(rule.check(text))
        return results