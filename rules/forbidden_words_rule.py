from domain.entities.rule import Rule
from domain.entities.rule_result import RuleResult


class ForbiddenWordsRule(Rule):
    """Правило проверки запрещённых слов"""

    def __init__(self, forbidden_words: list[str] = None, priority: int = 1):
        super().__init__("forbidden_words", priority)
        self.forbidden_words = forbidden_words or [
            "spam", "порно", "наркотики", "кровь", "насилие",
            "убийство", "оружие", "экстремизм", "фейк",
            "instagram", "facebook", "twitter",
            "инстаграм", "фейсбук", "твиттер",
            "vpn", "впн",
            "telegram", "телеграм", "tg", "тг"
        ]

    def check(self, text: str) -> RuleResult:
        lower_text = text.lower()
        found = [word for word in self.forbidden_words if word in lower_text]
        passed = len(found) == 0
        message = f"Найдены запрещённые слова: {', '.join(found)}" if found else "Запрещённых слов нет"

        return RuleResult(
            rule_name=self.name,
            passed=passed,
            message=message,
            priority=self.priority
        )

    def add_word(self, word: str):
        if word.lower() not in self.forbidden_words:
            self.forbidden_words.append(word.lower())

    def remove_word(self, word: str):
        word_lower = word.lower()
        if word_lower in self.forbidden_words:
            self.forbidden_words.remove(word_lower)