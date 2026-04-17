from domain.entities.rule import Rule
from domain.entities.rule_result import RuleResult


class LengthRule(Rule):
    """Правило проверки длины текста"""

    def __init__(self, min_length: int = 10, max_length: int = 500, priority: int = 4):
        super().__init__("length", priority)
        self.min_length = min_length
        self.max_length = max_length

    def check(self, text: str) -> RuleResult:
        length = len(text)
        passed = self.min_length <= length <= self.max_length

        if length < self.min_length:
            message = f"Текст слишком короткий: {length} (минимум {self.min_length})"
        elif length > self.max_length:
            message = f"Текст слишком длинный: {length} (максимум {self.max_length})"
        else:
            message = f"Длина текста в норме: {length}"

        return RuleResult(
            rule_name=self.name,
            passed=passed,
            message=message,
            priority=self.priority
        )

    def update_bounds(self, min_length: int = None, max_length: int = None):
        if min_length is not None:
            self.min_length = min_length
        if max_length is not None:
            self.max_length = max_length