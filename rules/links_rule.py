import re
from domain.entities.rule import Rule
from domain.entities.rule_result import RuleResult


class LinksRule(Rule):
    """Правило проверки наличия ссылок"""

    def __init__(self, allow_list: list[str] = None, priority: int = 2):
        super().__init__("links", priority)
        self.allow_list = allow_list or []
        self.url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s]*'

    def check(self, text: str) -> RuleResult:
        links = re.findall(self.url_pattern, text)

        if self.allow_list:
            links = [link for link in links
                     if not any(allowed in link for allowed in self.allow_list)]

        passed = len(links) == 0
        message = f"Найдены ссылки: {', '.join(links[:3])}" if links else "Ссылок нет"

        return RuleResult(
            rule_name=self.name,
            passed=passed,
            message=message,
            priority=self.priority
        )