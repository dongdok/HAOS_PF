from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from reco_engine.core.entity_resolution import is_shadow_entity, representative_entity_id


@dataclass(frozen=True)
class OpsSummary:
    review_now: list[dict]
    keep_good: list[dict]
    recommend_new: list[dict]


class OpsSummaryService:
    def __init__(self, db_path: Path):
        self._db_path = db_path

    def build(self) -> OpsSummary:
        with sqlite3.connect(self._db_path) as conn:
            signal_by_entity = self._load_signal_by_entity(conn)
            automation_activity = self._load_automation_activity(conn)
            conflict_feedback = self._load_latest_conflict_feedback(conn)

        review_now: list[dict] = []
        keep_good: list[dict] = []
        recommend_new: list[dict] = []

        entities = sorted(set(signal_by_entity.keys()) | set(automation_activity.keys()))
        for entity_id in entities:
            rule_signals = signal_by_entity.get(entity_id, {})
            auto_count = automation_activity.get(entity_id, 0)
            conflict_feedback_verdict = conflict_feedback.get(entity_id)

            conflict_evidence = int(rule_signals.get("condition_conflict", 0))
            cancel_evidence = int(rule_signals.get("manual_cancel_after_auto", 0))
            should_review = cancel_evidence > 0 or (
                conflict_evidence > 0 and conflict_feedback_verdict != "intended"
            )

            top_behavior_rule, top_behavior_count = self._top_behavior_signal(rule_signals)
            should_recommend_new = top_behavior_count > 0 and auto_count == 0

            if should_review:
                review_now.append(
                    {
                        "entity_id": entity_id,
                        "evidence_count": max(conflict_evidence, cancel_evidence),
                        "reasons": self._review_reasons(
                            rule_signals=rule_signals,
                            conflict_feedback_verdict=conflict_feedback_verdict,
                        ),
                        "recommended_action": "기존 자동화 조건/우선순위/실행 타이밍 점검",
                    }
                )
                continue

            if should_recommend_new:
                recommend_new.append(
                    {
                        "entity_id": entity_id,
                        "evidence_count": top_behavior_count,
                        "reasons": [self._rule_reason(top_behavior_rule)],
                        "recommended_action": "신규 자동화 후보로 등록 후 7일 테스트",
                    }
                )
                continue

            if auto_count > 0:
                keep_good.append(
                    {
                        "entity_id": entity_id,
                        "evidence_count": auto_count,
                        "reasons": ["자동화 실행 로그가 안정적으로 관측됨"],
                        "recommended_action": "현재 정책 유지",
                    }
                )

        return OpsSummary(
            review_now=sorted(
                review_now,
                key=lambda item: (-item["evidence_count"], item["entity_id"]),
            )[:5],
            keep_good=sorted(
                keep_good,
                key=lambda item: (-item["evidence_count"], item["entity_id"]),
            )[:5],
            recommend_new=sorted(
                recommend_new,
                key=lambda item: (-item["evidence_count"], item["entity_id"]),
            )[:5],
        )

    @staticmethod
    def _load_signal_by_entity(conn: sqlite3.Connection) -> dict[str, dict[str, int]]:
        rows = conn.execute(
            """
            SELECT rule_code, entity_id, evidence_count
            FROM recommendation_candidate
            WHERE status IN ('proposed','approved','testing','active')
            """
        ).fetchall()
        by_entity: dict[str, dict[str, int]] = {}
        for rule_code, entity_id, evidence_count in rows:
            if is_shadow_entity(entity_id):
                continue
            resolved = representative_entity_id(entity_id)
            per_rule = by_entity.setdefault(resolved, {})
            per_rule[str(rule_code)] = per_rule.get(str(rule_code), 0) + int(evidence_count)
        return by_entity

    @staticmethod
    def _load_automation_activity(conn: sqlite3.Connection) -> dict[str, int]:
        rows = conn.execute(
            """
            SELECT entity_id, COUNT(*) AS auto_count
            FROM event_log
            WHERE actor_type = 'automation'
              AND entity_id NOT LIKE 'automation.%'
            GROUP BY entity_id
            """
        ).fetchall()
        merged: dict[str, int] = {}
        for entity_id, auto_count in rows:
            if is_shadow_entity(entity_id):
                continue
            resolved = representative_entity_id(entity_id)
            merged[resolved] = merged.get(resolved, 0) + int(auto_count)
        return merged

    @staticmethod
    def _load_latest_conflict_feedback(conn: sqlite3.Connection) -> dict[str, str]:
        rows = conn.execute(
            """
            SELECT cf.entity_id, cf.verdict
            FROM conflict_feedback cf
            JOIN (
              SELECT entity_id, MAX(id) AS max_id
              FROM conflict_feedback
              GROUP BY entity_id
            ) latest
              ON latest.entity_id = cf.entity_id
             AND latest.max_id = cf.id
            """
        ).fetchall()
        feedback: dict[str, str] = {}
        for entity_id, verdict in rows:
            feedback[representative_entity_id(entity_id)] = str(verdict)
        return feedback

    @staticmethod
    def _top_behavior_signal(rule_signals: dict[str, int]) -> tuple[str, int]:
        behavior_rules = (
            "manual_repeat",
            "movement_repeat",
            "env_response_repeat",
            "door_presence_time_repeat",
        )
        top_rule = behavior_rules[0]
        top_count = int(rule_signals.get(top_rule, 0))
        for rule in behavior_rules[1:]:
            count = int(rule_signals.get(rule, 0))
            if count > top_count:
                top_rule = rule
                top_count = count
        return top_rule, top_count

    @classmethod
    def _review_reasons(cls, rule_signals: dict[str, int], conflict_feedback_verdict: str | None) -> list[str]:
        reasons: list[str] = []
        if int(rule_signals.get("condition_conflict", 0)) > 0:
            if conflict_feedback_verdict == "intended":
                reasons.append("의도된 충돌로 기록됨 (참고)")
            else:
                reasons.append("자동화 간 충돌 신호가 반복됨")
        if int(rule_signals.get("manual_cancel_after_auto", 0)) > 0:
            reasons.append("자동화 직후 수동 취소가 반복됨")
        return reasons

    @staticmethod
    def _rule_reason(rule_code: str) -> str:
        mapping = {
            "manual_repeat": "수동 ON/OFF 반복",
            "movement_repeat": "방 간 이동 패턴 반복",
            "env_response_repeat": "환경 변화 후 제어 반복",
            "door_presence_time_repeat": "출입문+재실+시간대 패턴 반복",
        }
        return mapping.get(rule_code, rule_code)
