from __future__ import annotations

from reco_engine.adapters.repository_sqlite import SQLiteRepository
from reco_engine.core.entities import RecommendationCandidate
from reco_engine.core.entity_resolution import is_shadow_entity, representative_entity_id
from reco_engine.core.policy import EnginePolicy
from reco_engine.core.scoring import confidence_from_evidence


class ProposalService:
    def __init__(self, repository: SQLiteRepository, policy: EnginePolicy):
        self._repo = repository
        self._policy = policy

    def persist_proposals(self, findings: dict[str, dict[str, int]]) -> int:
        inserted = 0
        feedback_map = self._repo.latest_conflict_feedback()
        normalized_findings = self._normalize_findings(findings)
        for rule_code, per_entity in normalized_findings.items():
            for entity_id, evidence_count in per_entity.items():
                if (
                    rule_code == "condition_conflict"
                    and feedback_map.get(entity_id) == "intended"
                ):
                    continue
                confidence = confidence_from_evidence(evidence_count=evidence_count, penalty_count=0)
                if confidence < self._policy.min_confidence_to_propose:
                    continue

                candidate = RecommendationCandidate(
                    rule_code=rule_code,
                    entity_id=entity_id,
                    summary=f"{rule_code} detected for {entity_id} ({evidence_count} events)",
                    evidence_count=evidence_count,
                    confidence_score=confidence,
                    proposed_automation_yaml=_proposal_stub(rule_code, entity_id),
                )
                if self._repo.insert_candidate(candidate):
                    inserted += 1
        return inserted

    @staticmethod
    def _normalize_findings(findings: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
        normalized: dict[str, dict[str, int]] = {}
        for rule_code, per_entity in findings.items():
            merged: dict[str, int] = {}
            for entity_id, evidence_count in per_entity.items():
                if is_shadow_entity(entity_id):
                    continue
                representative = representative_entity_id(entity_id)
                merged[representative] = merged.get(representative, 0) + evidence_count
            normalized[rule_code] = merged
        return normalized


def _proposal_stub(rule_code: str, entity_id: str) -> str:
    # Proposal only. It is never auto-applied.
    return (
        "alias: \"[추천] 자동화 제안\"\n"
        f"description: \"rule={rule_code}, entity={entity_id}\"\n"
        "mode: restart\n"
        "trigger: []\n"
        "action: []\n"
    )
