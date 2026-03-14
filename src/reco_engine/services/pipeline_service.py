from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from reco_engine.adapters.ha_client import HAClient
from reco_engine.adapters.repository_sqlite import SQLiteRepository
from reco_engine.core.errors import DataValidationError
from reco_engine.core.policy import EnginePolicy
from reco_engine.services.collect_service import CollectService
from reco_engine.services.detection_service import DetectionService
from reco_engine.services.feedback_service import FeedbackService
from reco_engine.services.intervention_service import InterventionService
from reco_engine.services.kpi_service import KpiService
from reco_engine.services.proposal_service import ProposalService


@dataclass(frozen=True)
class PipelineSummary:
    collected_inserted: int
    collected_rejected: int
    collected_rejected_reasons: dict[str, int]
    interventions_updated: int
    feedback_ingested: int
    proposals_inserted: int
    findings: dict[str, dict[str, int]]
    monthly_energy_entity_id: str
    monthly_energy_kwh: float
    kpi_measured_at: str


class PipelineService:
    def __init__(
        self,
        db_path: Path,
        ha_client: HAClient,
        repository: SQLiteRepository,
        policy: EnginePolicy,
        canonical_config: dict[str, Any],
    ):
        self._db_path = db_path
        self._ha = ha_client
        self._repo = repository
        self._policy = policy
        self._canonical = canonical_config

    def run_daily_cycle(self, collect_hours: int, intervention_window_minutes: int) -> PipelineSummary:
        if collect_hours <= 0:
            raise DataValidationError("collect_hours must be greater than zero")
        if intervention_window_minutes <= 0:
            raise DataValidationError("intervention_window_minutes must be greater than zero")
        now = datetime.now().astimezone()
        start = now - timedelta(hours=collect_hours)

        collect_summary = CollectService(
            ha_client=self._ha,
            repository=self._repo,
        ).collect_logbook_window(
            start_time=start,
            end_time=now,
            measurement_entity_ids=self._measurement_entity_ids(),
        )

        intervention_summary = InterventionService(
            db_path=self._db_path,
            repository=self._repo,
        ).apply_manual_override_rule(window_minutes=intervention_window_minutes)

        feedback_summary = FeedbackService(
            db_path=self._db_path,
            repository=self._repo,
        ).ingest_from_event_log()

        findings = DetectionService(
            db_path=self._db_path,
            policy=self._policy,
        ).run()

        proposals_inserted = ProposalService(
            repository=self._repo,
            policy=self._policy,
        ).persist_proposals(findings)

        kpi_service = KpiService(
            db_path=self._db_path,
            repository=self._repo,
        )
        monthly_entity = kpi_service.resolve_monthly_energy_entity(self._canonical)
        snapshot = kpi_service.compute_and_store_auto(
            ha_client=self._ha,
            canonical_config=self._canonical,
        )

        return PipelineSummary(
            collected_inserted=collect_summary.inserted,
            collected_rejected=collect_summary.rejected,
            collected_rejected_reasons=collect_summary.rejected_reasons,
            interventions_updated=intervention_summary.updated_events,
            feedback_ingested=feedback_summary.inserted,
            proposals_inserted=proposals_inserted,
            findings=findings,
            monthly_energy_entity_id=monthly_entity,
            monthly_energy_kwh=snapshot.monthly_energy_kwh,
            kpi_measured_at=snapshot.measured_at.isoformat(),
        )

    def _measurement_entity_ids(self) -> list[str]:
        specs = self._canonical.get("required_measurement_entities", [])
        if not isinstance(specs, list):
            return []
        entity_ids: list[str] = []
        for spec in specs:
            if not isinstance(spec, dict):
                continue
            entity_id = spec.get("entity_id")
            if isinstance(entity_id, str) and entity_id:
                entity_ids.append(entity_id)
        # Preserve order while deduplicating
        return list(dict.fromkeys(entity_ids))
