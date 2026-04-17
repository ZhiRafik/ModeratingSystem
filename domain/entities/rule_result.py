from dataclasses import dataclass

@dataclass
class RuleResult:
    """Результат проверки одного правила"""
    rule_name: str
    passed: bool
    message: str
    priority: int = 0