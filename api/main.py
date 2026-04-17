from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from services.rule_engine import RuleEngine
from services.moderation_service import ModerationService
from repositories.in_memory_repo import InMemoryRepository
from rules import ForbiddenWordsRule, LinksRule, RepetitionsRule, LengthRule

# Инициализация
engine = RuleEngine()
engine.add_rule(ForbiddenWordsRule())
engine.add_rule(LinksRule())
engine.add_rule(RepetitionsRule())
engine.add_rule(LengthRule())

repo = InMemoryRepository()
service = ModerationService(engine, repo)

app = FastAPI(title="Moderation System", version="1.0.0")

# DTO для API
class ModerateRequest(BaseModel):
    text: str

class ModerateResponse(BaseModel):
    id: int
    status: str
    final_message: str
    rule_results: List[dict]

class HistoryRecordResponse(BaseModel):
    id: int
    text: str
    status: str
    created_at: str
    final_message: str

# Эндпоинты
@app.post("/moderate", response_model=ModerateResponse)
async def moderate(request: ModerateRequest):
    result = service.moderate(request.text)
    return ModerateResponse(
        id=result.id,
        status=result.status.value,
        final_message=result.final_message,
        rule_results=[
            {"rule_name": r.rule_name, "passed": r.passed, "message": r.message}
            for r in result.rule_results
        ]
    )

@app.get("/history")
async def get_history(limit: int = 50):
    history = service.get_history(limit)
    return [
        HistoryRecordResponse(
            id=r.id,
            text=r.text[:100],
            status=r.status.value,
            created_at=r.created_at.isoformat(),
            final_message=r.final_message
        )
        for r in history
    ]

@app.get("/history/{record_id}")
async def get_record(record_id: int):
    record = service.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.get("/stats")
async def get_stats():
    return service.get_stats()

@app.get("/rules")
async def get_rules():
    return {
        "rules": [
            {"name": r.name, "priority": r.priority, "enabled": r.enabled}
            for r in engine.rules
        ]
    }

@app.post("/rules/{rule_name}/toggle")
async def toggle_rule(rule_name: str, enabled: bool):
    rule = engine.get_rule(rule_name)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    rule.enabled = enabled
    return {"rule": rule_name, "enabled": enabled}