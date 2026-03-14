from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from reco_engine.core.entities import ActorType, EventRecord, EventResult
from reco_engine.core.policy import EnginePolicy
from reco_engine.core.rules import (
    detect_condition_conflicts,
    detect_door_presence_time_patterns,
    detect_env_response_patterns,
    detect_manual_cancels_after_automation,
    detect_presence_transition_patterns,
    detect_repeated_manual_toggles,
)


class DetectionService:
    def __init__(self, db_path: Path, policy: EnginePolicy):
        self._db_path = db_path
        self._policy = policy

    def run(self) -> dict[str, dict[str, int]]:
        events = self._load_events()
        return {
            "manual_repeat": detect_repeated_manual_toggles(
                events=events,
                min_count=self._policy.manual_repeat_min_count,
            ),
            "manual_cancel_after_auto": detect_manual_cancels_after_automation(
                events=events,
                window_minutes=self._policy.cancel_window_minutes,
            ),
            "condition_conflict": detect_condition_conflicts(
                events=events,
                window_minutes=self._policy.conflict_window_minutes,
            ),
            "movement_repeat": detect_presence_transition_patterns(
                events=events,
                min_count=self._policy.movement_repeat_min_count,
                window_minutes=self._policy.movement_window_minutes,
            ),
            "env_response_repeat": detect_env_response_patterns(
                events=events,
                min_count=self._policy.env_pattern_min_count,
                window_minutes=self._policy.env_response_window_minutes,
            ),
            "door_presence_time_repeat": detect_door_presence_time_patterns(
                events=events,
                min_count=self._policy.door_pattern_min_count,
                window_minutes=self._policy.door_pattern_window_minutes,
            ),
        }

    def _load_events(self) -> list[EventRecord]:
        rows: list[tuple] = []
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT timestamp, entity_id, actor_type, action, pre_state, post_state,
                       source_automation, result, reason_code
                FROM event_log
                """
            ).fetchall()

        events: list[EventRecord] = []
        for row in rows:
            events.append(
                EventRecord(
                    timestamp=datetime.fromisoformat(row[0]),
                    entity_id=row[1],
                    actor_type=ActorType(row[2]),
                    action=row[3],
                    pre_state=row[4],
                    post_state=row[5],
                    source_automation=row[6],
                    result=EventResult(row[7]),
                    reason_code=row[8],
                )
            )
        return events
