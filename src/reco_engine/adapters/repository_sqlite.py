from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from reco_engine.core.entities import EventRecord, KpiSnapshot, RecommendationCandidate


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS event_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  actor_type TEXT NOT NULL CHECK(actor_type IN ('manual','automation','system')),
  action TEXT NOT NULL,
  pre_state TEXT NOT NULL,
  post_state TEXT NOT NULL,
  source_automation TEXT,
  result TEXT NOT NULL CHECK(result IN ('success','failed','cancelled')),
  reason_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recommendation_candidate (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  rule_code TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  summary TEXT NOT NULL,
  evidence_count INTEGER NOT NULL,
  confidence_score REAL NOT NULL,
  proposed_automation_yaml TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'proposed',
  approved_at TEXT,
  test_batch_id INTEGER,
  test_start_at TEXT,
  test_end_at TEXT,
  finalized_at TEXT,
  rejection_reason TEXT
);

CREATE TABLE IF NOT EXISTS kpi_snapshot (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  measured_at TEXT NOT NULL,
  manual_ops_total INTEGER NOT NULL,
  automation_cancel_rate REAL NOT NULL,
  unnecessary_on_minutes INTEGER NOT NULL,
  monthly_energy_kwh REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS recommendation_test_batch (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  status TEXT NOT NULL CHECK(status IN ('testing','passed','failed','rolled_back')),
  started_at TEXT NOT NULL,
  ends_at TEXT NOT NULL,
  finalized_at TEXT,
  rollback_reason TEXT
);

CREATE TABLE IF NOT EXISTS conflict_feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_log_id INTEGER NOT NULL UNIQUE,
  entity_id TEXT NOT NULL,
  verdict TEXT NOT NULL CHECK(verdict IN ('intended','unintended')),
  recorded_at TEXT NOT NULL,
  source_script TEXT NOT NULL,
  FOREIGN KEY(event_log_id) REFERENCES event_log(id)
);

CREATE TABLE IF NOT EXISTS collect_reject_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recorded_at TEXT NOT NULL DEFAULT (datetime('now')),
  reason_code TEXT NOT NULL,
  source TEXT NOT NULL CHECK(source IN ('logbook','history')),
  entity_id TEXT,
  raw_timestamp TEXT
);
"""


@dataclass(frozen=True)
class SQLiteRepository:
    db_path: Path

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)
            self._apply_migrations(conn)
            conn.commit()

    def insert_event(self, event: EventRecord) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            exists = conn.execute(
                """
                SELECT 1
                FROM event_log
                WHERE timestamp = ?
                  AND entity_id = ?
                  AND actor_type = ?
                  AND action = ?
                  AND pre_state = ?
                  AND post_state = ?
                  AND COALESCE(source_automation, '') = COALESCE(?, '')
                  AND result = ?
                  AND reason_code = ?
                LIMIT 1
                """,
                (
                    event.timestamp.isoformat(),
                    event.entity_id,
                    event.actor_type.value,
                    event.action,
                    event.pre_state,
                    event.post_state,
                    event.source_automation,
                    event.result.value,
                    event.reason_code,
                ),
            ).fetchone()
            if exists:
                return False

            conn.execute(
                """
                INSERT INTO event_log (
                  timestamp, entity_id, actor_type, action, pre_state, post_state,
                  source_automation, result, reason_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.timestamp.isoformat(),
                    event.entity_id,
                    event.actor_type.value,
                    event.action,
                    event.pre_state,
                    event.post_state,
                    event.source_automation,
                    event.result.value,
                    event.reason_code,
                ),
            )
            conn.commit()
            return True

    def insert_candidate(self, candidate: RecommendationCandidate) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            exists = conn.execute(
                """
                SELECT 1
                FROM recommendation_candidate
                WHERE rule_code = ?
                  AND entity_id = ?
                  AND summary = ?
                  AND evidence_count = ?
                  AND confidence_score = ?
                  AND proposed_automation_yaml = ?
                  AND status = 'proposed'
                LIMIT 1
                """,
                (
                    candidate.rule_code,
                    candidate.entity_id,
                    candidate.summary,
                    candidate.evidence_count,
                    candidate.confidence_score,
                    candidate.proposed_automation_yaml,
                ),
            ).fetchone()
            if exists:
                return False

            conn.execute(
                """
                INSERT INTO recommendation_candidate (
                  rule_code, entity_id, summary, evidence_count, confidence_score, proposed_automation_yaml
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate.rule_code,
                    candidate.entity_id,
                    candidate.summary,
                    candidate.evidence_count,
                    candidate.confidence_score,
                    candidate.proposed_automation_yaml,
                ),
            )
            conn.commit()
            return True

    def insert_kpi(self, snapshot: KpiSnapshot) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO kpi_snapshot (
                  measured_at, manual_ops_total, automation_cancel_rate,
                  unnecessary_on_minutes, monthly_energy_kwh
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    snapshot.measured_at.isoformat(),
                    snapshot.manual_ops_total,
                    snapshot.automation_cancel_rate,
                    snapshot.unnecessary_on_minutes,
                    snapshot.monthly_energy_kwh,
                ),
            )
            conn.commit()

    @staticmethod
    def _apply_migrations(conn: sqlite3.Connection) -> None:
        cols = {
            row[1]
            for row in conn.execute("PRAGMA table_info(recommendation_candidate)").fetchall()
        }
        migrations = [
            ("approved_at", "ALTER TABLE recommendation_candidate ADD COLUMN approved_at TEXT"),
            ("test_batch_id", "ALTER TABLE recommendation_candidate ADD COLUMN test_batch_id INTEGER"),
            ("test_start_at", "ALTER TABLE recommendation_candidate ADD COLUMN test_start_at TEXT"),
            ("test_end_at", "ALTER TABLE recommendation_candidate ADD COLUMN test_end_at TEXT"),
            ("finalized_at", "ALTER TABLE recommendation_candidate ADD COLUMN finalized_at TEXT"),
            ("rejection_reason", "ALTER TABLE recommendation_candidate ADD COLUMN rejection_reason TEXT"),
        ]
        for col, stmt in migrations:
            if col not in cols:
                conn.execute(stmt)

    def mark_event_cancelled(self, event_id: int, reason_code: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                """
                UPDATE event_log
                SET result = 'cancelled',
                    reason_code = ?
                WHERE id = ?
                  AND result != 'cancelled'
                """,
                (reason_code, event_id),
            )
            conn.commit()
            return int(cur.rowcount)

    def insert_conflict_feedback(
        self,
        event_log_id: int,
        entity_id: str,
        verdict: str,
        recorded_at: str,
        source_script: str,
    ) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            exists = conn.execute(
                "SELECT 1 FROM conflict_feedback WHERE event_log_id = ? LIMIT 1",
                (event_log_id,),
            ).fetchone()
            if exists:
                return False
            conn.execute(
                """
                INSERT INTO conflict_feedback (
                  event_log_id, entity_id, verdict, recorded_at, source_script
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (event_log_id, entity_id, verdict, recorded_at, source_script),
            )
            conn.commit()
            return True

    def latest_conflict_feedback(self) -> dict[str, str]:
        with sqlite3.connect(self.db_path) as conn:
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
        return {str(row[0]): str(row[1]) for row in rows}

    def insert_collect_reject(
        self,
        reason_code: str,
        source: str,
        entity_id: str | None,
        raw_timestamp: str | None,
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO collect_reject_log (reason_code, source, entity_id, raw_timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (reason_code, source, entity_id, raw_timestamp),
            )
            conn.commit()
