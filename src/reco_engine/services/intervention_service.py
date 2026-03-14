from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from reco_engine.adapters.repository_sqlite import SQLiteRepository


@dataclass(frozen=True)
class InterventionSummary:
    updated_events: int


class InterventionService:
    """Promote automation events to cancelled when manual reversal is observed."""

    def __init__(self, db_path: Path, repository: SQLiteRepository):
        self._db_path = db_path
        self._repo = repository

    def apply_manual_override_rule(self, window_minutes: int) -> InterventionSummary:
        if window_minutes <= 0:
            raise ValueError("window_minutes must be greater than zero")

        window = timedelta(minutes=window_minutes)
        rows = self._load_candidates()
        updated = 0

        for i, base in enumerate(rows):
            if base["actor_type"] != "automation":
                continue
            if base["post_state"] not in {"on", "off"}:
                continue

            base_time = datetime.fromisoformat(base["timestamp"])
            for candidate in rows[i + 1 :]:
                candidate_time = datetime.fromisoformat(candidate["timestamp"])
                if candidate_time - base_time > window:
                    break
                if candidate["entity_id"] != base["entity_id"]:
                    continue
                if candidate["actor_type"] != "manual":
                    continue
                if candidate["post_state"] not in {"on", "off"}:
                    continue
                if candidate["post_state"] == base["post_state"]:
                    continue

                changed = self._repo.mark_event_cancelled(
                    event_id=base["id"],
                    reason_code="manual_override_after_automation",
                )
                updated += changed
                break

        return InterventionSummary(updated_events=updated)

    def _load_candidates(self) -> list[dict]:
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, timestamp, entity_id, actor_type, post_state
                FROM event_log
                WHERE post_state IN ('on', 'off')
                ORDER BY timestamp ASC, id ASC
                """
            ).fetchall()

        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "entity_id": row[2],
                "actor_type": row[3],
                "post_state": row[4],
            }
            for row in rows
        ]
