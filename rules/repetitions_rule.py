import re
from collections import Counter
from domain.entities.rule import Rule
from domain.entities.rule_result import RuleResult


class RepetitionsRule(Rule):
    """Правило проверки повторений символов и слов"""

    def __init__(self, max_repetitions: int = 5, priority: int = 3):
        super().__init__("repetitions", priority)
        self.max_repetitions = max_repetitions

    def check(self, text: str) -> RuleResult:
        if not text.strip():
            return RuleResult(
                rule_name=self.name,
                passed=True,
                message="Пустой текст",
                priority=self.priority
            )

        violations = []

        # Проверка повторяющихся символов (ааааа)
        repeated_chars = re.findall(r'(.)\1{4,}', text)
        if repeated_chars:
            violations.append(f"повторяющиеся символы: {', '.join(set(repeated_chars[:3]))}")

        # Проверка повторяющихся слов
        words = text.lower().split()
        word_counts = Counter(words)
        repeated_words = [word for word, count in word_counts.items() if count > self.max_repetitions]
        if repeated_words:
            violations.append(f"повторяющиеся слова: {', '.join(repeated_words[:3])}")

        passed = len(violations) == 0
        message = "Повторений нет" if passed else f"Обнаружены: {'; '.join(violations)}"

        return RuleResult(
            rule_name=self.name,
            passed=passed,
            message=message,
            priority=self.priority
        )