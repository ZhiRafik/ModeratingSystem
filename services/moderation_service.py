from typing import List, Optional
from services.rule_engine import RuleEngine
from repositories.in_memory_repo import InMemoryRepository
from domain.entities.moderation_result import ModerationResult
from domain.entities.rule_result import RuleResult
from domain.value_objects.moderation_status import ModerationStatus


class ModerationService:
    """Сервис модерации (бизнес-логика)"""

    def __init__(self, rule_engine: RuleEngine, repository: InMemoryRepository):
        self.rule_engine = rule_engine
        self.repo = repository

    def moderate(self, text: str) -> ModerationResult:
        """Основной метод модерации"""
        if not text or not text.strip():
            result = ModerationResult(
                text=text,
                status=ModerationStatus.REJECTED,
                rule_results=[],
                final_message="❌ Текст пустой"
            )
            return self.repo.save(result)

        # Выполняем правила
        results = self.rule_engine.execute(text)

        # Определяем статус
        status = self._determine_status(results)
        final_message = self._build_message(status, results)

        result = ModerationResult(
            text=text,
            status=status,
            rule_results=results,
            final_message=final_message
        )

        return self.repo.save(result)

    def _determine_status(self, results: List[RuleResult]) -> ModerationStatus:
        """Определить статус по результатам правил"""
        for r in results:
            if not r.passed and r.priority <= 2:
                return ModerationStatus.REJECTED

        for r in results:
            if not r.passed:
                return ModerationStatus.MANUAL_REVIEW

        return ModerationStatus.APPROVED

    def _build_message(self, status: ModerationStatus, results: List[RuleResult]) -> str:
        """Сформировать итоговое сообщение"""
        if status == ModerationStatus.APPROVED:
            return "✅ Текст прошёл модерацию"

        failed = [r for r in results if not r.passed]
        if not failed:
            return "❌ Неизвестная ошибка"

        if status == ModerationStatus.REJECTED:
            return f"❌ Отклонён: {failed[0].message}"
        else:
            return f"⚠️ Требуется ручная проверка: {failed[0].message}"

    def get_history(self, limit: int = 50) -> List[ModerationResult]:
        """Получить историю проверок"""
        return self.repo.get_recent(limit)

    def get_record(self, record_id: int) -> Optional[ModerationResult]:
        """Получить запись по ID"""
        return self.repo.get_by_id(record_id)

    def get_stats(self) -> dict:
        """Получить статистику"""
        all_records = self.repo.get_all()
        total = len(all_records)

        if total == 0:
            return {"total": 0, "approved": 0, "rejected": 0, "manual_review": 0, "approval_rate": 0}

        approved = sum(1 for r in all_records if r.status == ModerationStatus.APPROVED)
        rejected = sum(1 for r in all_records if r.status == ModerationStatus.REJECTED)
        manual = sum(1 for r in all_records if r.status == ModerationStatus.MANUAL_REVIEW)

        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "manual_review": manual,
            "approval_rate": round(approved / total * 100, 2)
        }