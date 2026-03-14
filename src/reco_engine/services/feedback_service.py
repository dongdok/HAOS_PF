from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from reco_engine.adapters.repository_sqlite import SQLiteRepository


@dataclass(frozen=True)
class FeedbackIngestSummary:
    inserted: int
    skipped: int


INPUT_SELECT_ENTITY_MAP = {
    "input_select.cuceonpideubaeg_1beon_sangtae": "script.apply_solar_color_temp",
    "input_select.cuceonpideubaeg_2beon_sangtae": "light.geosil_keoteun_rain_jomyeong_rokeol",
    "input_select.cuceonpideubaeg_3beon_sangtae": "light.geosil_stand_lighting",
    "input_select.cuceonpideubaeg_4beon_sangtae": "switch.jubang_ceiling_light",
    "input_select.cuceonpideubaeg_5beon_sangtae": "input_boolean.gasang_hwajangsil",
}

INPUT_SELECT_VERDICT_MAP = {
    "의도됨": "intended",
    "문제": "unintended",
}


class FeedbackService:
    def __init__(self, db_path: Path, repository: SQLiteRepository):
        self._db_path = db_path
        self._repo = repository

    def ingest_from_event_log(self) -> FeedbackIngestSummary:
        rows = self._load_candidate_rows()
        inserted = 0
        skipped = 0
        for event_id, ts, entity_id, post_state in rows:
            decoded = self._decode_feedback(source_entity_id=entity_id, post_state=post_state)
            if decoded is None:
                skipped += 1
                continue
            target_entity_id, verdict = decoded
            ok = self._repo.insert_conflict_feedback(
                event_log_id=event_id,
                entity_id=target_entity_id,
                verdict=verdict,
                recorded_at=ts,
                source_script=entity_id,
            )
            if ok:
                inserted += 1
            else:
                skipped += 1
        return FeedbackIngestSummary(inserted=inserted, skipped=skipped)

    def latest_verdict_map(self) -> dict[str, str]:
        return self._repo.latest_conflict_feedback()

    def _load_candidate_rows(self) -> list[tuple[int, str, str, str]]:
        with sqlite3.connect(self._db_path) as conn:
            return conn.execute(
                """
                SELECT id, timestamp, entity_id, post_state
                FROM event_log
                WHERE entity_id LIKE 'input_select.cuceonpideubaeg_%_sangtae'
                ORDER BY id
                """
            ).fetchall()

    @staticmethod
    def _decode_feedback(source_entity_id: str, post_state: str) -> tuple[str, str] | None:
        if source_entity_id in INPUT_SELECT_ENTITY_MAP:
            verdict = INPUT_SELECT_VERDICT_MAP.get(post_state)
            if verdict is None:
                return None
            return INPUT_SELECT_ENTITY_MAP[source_entity_id], verdict
        return None
