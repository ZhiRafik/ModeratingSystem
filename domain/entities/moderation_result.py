from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from domain.entities.rule_result import RuleResult
from domain.value_objects.moderation_status import ModerationStatus

@dataclass
class ModerationResult:
    """Полный результат модерации"""
    text: str
    status: ModerationStatus
    rule_results: List[RuleResult]
    final_message: str
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None  # Для репозитория