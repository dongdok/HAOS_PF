from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from reco_engine.core.errors import DataValidationError


@dataclass(frozen=True)
class ApprovalSummary:
    updated: int


@dataclass(frozen=True)
class TestBatchSummary:
    batch_id: int
    linked_candidates: int
    started_at: str
    ends_at: str


@dataclass(frozen=True)
class FinalizeSummary:
    batch_id: int
    updated_candidates: int
    new_batch_status: str


class ApprovalService:
    def __init__(self, db_path: Path):
        self._db_path = db_path

    def approve_candidates(self, candidate_ids: list[int]) -> ApprovalSummary:
        if not candidate_ids:
            raise DataValidationError("candidate_ids must not be empty")
        now = datetime.now().astimezone().isoformat()
        with sqlite3.connect(self._db_path) as conn:
            placeholders = ",".join("?" for _ in candidate_ids)
            cur = conn.execute(
                f"""
                UPDATE recommendation_candidate
                SET status = 'approved',
                    approved_at = ?
                WHERE id IN ({placeholders})
                  AND status = 'proposed'
                """,
                (now, *candidate_ids),
            )
            conn.commit()
            return ApprovalSummary(updated=int(cur.rowcount))

    def start_test_batch(self, candidate_ids: list[int], test_days: int) -> TestBatchSummary:
        if not candidate_ids:
            raise DataValidationError("candidate_ids must not be empty")
        if test_days <= 0:
            raise DataValidationError("test_days must be greater than zero")

        started = datetime.now().astimezone()
        ends = started + timedelta(days=test_days)
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO recommendation_test_batch (status, started_at, ends_at)
                VALUES ('testing', ?, ?)
                """,
                (started.isoformat(), ends.isoformat()),
            )
            batch_id = int(cur.lastrowid)
            placeholders = ",".join("?" for _ in candidate_ids)
            cur2 = conn.execute(
                f"""
                UPDATE recommendation_candidate
                SET status = 'testing',
                    test_batch_id = ?,
                    test_start_at = ?,
                    test_end_at = ?
                WHERE id IN ({placeholders})
                  AND status = 'approved'
                """,
                (batch_id, started.isoformat(), ends.isoformat(), *candidate_ids),
            )
            linked = int(cur2.rowcount)
            if linked == 0:
                conn.execute("DELETE FROM recommendation_test_batch WHERE id = ?", (batch_id,))
                conn.commit()
                raise DataValidationError("No approved candidates were linked to the test batch")
            conn.commit()
            return TestBatchSummary(
                batch_id=batch_id,
                linked_candidates=linked,
                started_at=started.isoformat(),
                ends_at=ends.isoformat(),
            )

    def finalize_test_batch(self, batch_id: int, passed: bool, reason: str | None = None) -> FinalizeSummary:
        status = "passed" if passed else "failed"
        candidate_status = "active" if passed else "rejected"
        now = datetime.now().astimezone().isoformat()

        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                """
                UPDATE recommendation_candidate
                SET status = ?,
                    finalized_at = ?,
                    rejection_reason = CASE WHEN ? = 1 THEN NULL ELSE ? END
                WHERE test_batch_id = ?
                  AND status = 'testing'
                """,
                (candidate_status, now, 1 if passed else 0, reason, batch_id),
            )
            conn.execute(
                """
                UPDATE recommendation_test_batch
                SET status = ?,
                    finalized_at = ?,
                    rollback_reason = CASE WHEN ? = 1 THEN NULL ELSE ? END
                WHERE id = ?
                """,
                (status, now, 1 if passed else 0, reason, batch_id),
            )
            conn.commit()

            return FinalizeSummary(
                batch_id=batch_id,
                updated_candidates=int(cur.rowcount),
                new_batch_status=status,
            )

    def rollback_batch(self, batch_id: int, reason: str) -> FinalizeSummary:
        now = datetime.now().astimezone().isoformat()
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                """
                UPDATE recommendation_candidate
                SET status = 'rolled_back',
                    finalized_at = ?,
                    rejection_reason = ?
                WHERE test_batch_id = ?
                  AND status IN ('testing','active')
                """,
                (now, reason, batch_id),
            )
            conn.execute(
                """
                UPDATE recommendation_test_batch
                SET status = 'rolled_back',
                    finalized_at = ?,
                    rollback_reason = ?
                WHERE id = ?
                """,
                (now, reason, batch_id),
            )
            conn.commit()

            return FinalizeSummary(
                batch_id=batch_id,
                updated_candidates=int(cur.rowcount),
                new_batch_status="rolled_back",
            )
