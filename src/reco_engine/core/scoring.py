from __future__ import annotations


def confidence_from_evidence(evidence_count: int, penalty_count: int) -> float:
    if evidence_count < 0 or penalty_count < 0:
        raise ValueError("evidence_count and penalty_count must be non-negative")
    if evidence_count == 0:
        raise ValueError("evidence_count must be greater than zero")
    raw = (evidence_count - penalty_count) / evidence_count
    return max(0.0, min(1.0, round(raw, 4)))

