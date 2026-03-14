from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from reco_engine.adapters.ha_client import HAClient
from reco_engine.adapters.repository_sqlite import SQLiteRepository
from reco_engine.core.entities import ActorType, KpiSnapshot
from reco_engine.core.errors import DataValidationError
from reco_engine.core.kpi import cancel_rate


class KpiService:
    def __init__(self, db_path: Path, repository: SQLiteRepository):
        self._db_path = db_path
        self._repo = repository

    def compute_and_store(self, monthly_energy_kwh: float) -> KpiSnapshot:
        manual_ops, auto_ops, cancelled = self._aggregate()
        snapshot = KpiSnapshot(
            measured_at=datetime.now().astimezone(),
            manual_ops_total=manual_ops,
            automation_cancel_rate=cancel_rate(cancelled=cancelled, total_automation_actions=auto_ops),
            unnecessary_on_minutes=0,
            monthly_energy_kwh=monthly_energy_kwh,
        )
        self._repo.insert_kpi(snapshot)
        return snapshot

    def compute_and_store_auto(self, ha_client: HAClient, canonical_config: dict[str, Any]) -> KpiSnapshot:
        monthly_energy_entity = self.resolve_monthly_energy_entity(canonical_config)
        state = ha_client.fetch_state(monthly_energy_entity)
        monthly_energy_kwh = self._parse_energy_kwh(state=state, entity_id=monthly_energy_entity)
        return self.compute_and_store(monthly_energy_kwh=monthly_energy_kwh)

    def resolve_monthly_energy_entity(self, canonical_config: dict[str, Any]) -> str:
        return self._resolve_monthly_energy_entity(canonical_config)

    def _aggregate(self) -> tuple[int, int, int]:
        with sqlite3.connect(self._db_path) as conn:
            manual_ops = conn.execute(
                "SELECT COUNT(*) FROM event_log WHERE actor_type = ?",
                (ActorType.MANUAL.value,),
            ).fetchone()[0]
            auto_ops = conn.execute(
                "SELECT COUNT(*) FROM event_log WHERE actor_type = ?",
                (ActorType.AUTOMATION.value,),
            ).fetchone()[0]
            cancelled = conn.execute(
                "SELECT COUNT(*) FROM event_log WHERE result = 'cancelled'"
            ).fetchone()[0]
        return int(manual_ops), int(auto_ops), int(cancelled)

    @staticmethod
    def _resolve_monthly_energy_entity(canonical_config: dict[str, Any]) -> str:
        utility = canonical_config.get("required_utility_meter_entities")
        if not isinstance(utility, dict):
            raise DataValidationError("required_utility_meter_entities is missing in canonical config")
        monthly = utility.get("monthly")
        if not isinstance(monthly, list) or not monthly:
            raise DataValidationError("required_utility_meter_entities.monthly must be a non-empty list")
        entity_id = monthly[0]
        if not isinstance(entity_id, str) or not entity_id:
            raise DataValidationError("monthly energy entity_id must be a non-empty string")
        return entity_id

    @staticmethod
    def _parse_energy_kwh(state: dict[str, Any], entity_id: str) -> float:
        raw = state.get("state")
        if raw in {None, "unknown", "unavailable", "none", "None"}:
            raise DataValidationError(f"{entity_id}: invalid state for monthly energy ({raw})")
        try:
            value = float(str(raw))
        except (TypeError, ValueError) as exc:
            raise DataValidationError(f"{entity_id}: non-numeric monthly energy state ({raw})") from exc
        if value < 0:
            raise DataValidationError(f"{entity_id}: monthly energy must be non-negative ({value})")
        return value
