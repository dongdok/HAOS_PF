from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ActorType(str, Enum):
    MANUAL = "manual"
    AUTOMATION = "automation"
    SYSTEM = "system"


class EventResult(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class EventRecord:
    timestamp: datetime
    entity_id: str
    actor_type: ActorType
    action: str
    pre_state: str
    post_state: str
    source_automation: str | None
    result: EventResult
    reason_code: str


@dataclass(frozen=True)
class RecommendationCandidate:
    rule_code: str
    entity_id: str
    summary: str
    evidence_count: int
    confidence_score: float
    proposed_automation_yaml: str


@dataclass(frozen=True)
class KpiSnapshot:
    measured_at: datetime
    manual_ops_total: int
    automation_cancel_rate: float
    unnecessary_on_minutes: int
    monthly_energy_kwh: float
