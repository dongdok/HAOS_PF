from __future__ import annotations

from collections import Counter
from datetime import datetime
from dataclasses import dataclass

from reco_engine.adapters.ha_client import HAClient
from reco_engine.adapters.repository_sqlite import SQLiteRepository
from reco_engine.core.entities import ActorType, EventRecord, EventResult
from reco_engine.core.errors import DataValidationError


@dataclass(frozen=True)
class CollectSummary:
    inserted: int
    rejected: int
    rejected_reasons: dict[str, int]


class CollectService:
    def __init__(self, ha_client: HAClient, repository: SQLiteRepository):
        self._ha = ha_client
        self._repo = repository

    def collect_logbook_window(
        self,
        start_time: datetime,
        end_time: datetime,
        measurement_entity_ids: list[str] | None = None,
    ) -> CollectSummary:
        inserted = 0
        rejected = 0
        rejected_reasons: Counter[str] = Counter()

        entries = self._ha.fetch_logbook(start_time=start_time, end_time=end_time)
        for entry in entries:
            entity_id = entry.get("entity_id")
            when = entry.get("when")
            state_value = entry.get("state")
            context_state = entry.get("context_state")

            if not isinstance(entity_id, str) or not entity_id:
                self._reject("missing_entity_id", "logbook", None, str(when) if when else None)
                rejected += 1
                rejected_reasons["missing_entity_id"] += 1
                continue
            if not isinstance(when, str) or not when:
                self._reject("missing_timestamp", "logbook", entity_id, None)
                rejected += 1
                rejected_reasons["missing_timestamp"] += 1
                continue
            if state_value is None:
                self._reject("missing_state", "logbook", entity_id, when)
                rejected += 1
                rejected_reasons["missing_state"] += 1
                continue
            if context_state is None:
                self._reject("missing_context_state", "logbook", entity_id, when)
                rejected += 1
                rejected_reasons["missing_context_state"] += 1
                continue

            try:
                timestamp = datetime.fromisoformat(when.replace("Z", "+00:00"))
            except ValueError:
                self._reject("invalid_timestamp_format", "logbook", entity_id, when)
                rejected += 1
                rejected_reasons["invalid_timestamp_format"] += 1
                continue

            try:
                actor_type = self._actor_type_from_logbook(entry)
            except DataValidationError:
                self._reject("unclassifiable_actor_type", "logbook", entity_id, when)
                rejected += 1
                rejected_reasons["unclassifiable_actor_type"] += 1
                continue

            event = EventRecord(
                timestamp=timestamp,
                entity_id=entity_id,
                actor_type=actor_type,
                action="state_change",
                pre_state=str(context_state),
                post_state=str(state_value),
                source_automation=entry.get("context_entity_id")
                if actor_type == ActorType.AUTOMATION
                else None,
                result=EventResult.SUCCESS,
                reason_code="observed_logbook_state_change",
            )
            if self._repo.insert_event(event):
                inserted += 1

        if measurement_entity_ids:
            history_payload = self._ha.fetch_history(
                start_time=start_time,
                end_time=end_time,
                entity_ids=measurement_entity_ids,
            )
            for per_entity in history_payload:
                if not isinstance(per_entity, list) or len(per_entity) < 2:
                    continue
                prev = per_entity[0]
                for current in per_entity[1:]:
                    if not isinstance(prev, dict) or not isinstance(current, dict):
                        self._reject("invalid_history_row", "history", None, None)
                        rejected += 1
                        rejected_reasons["invalid_history_row"] += 1
                        prev = current
                        continue

                    entity_id = current.get("entity_id")
                    changed_at = current.get("last_changed")
                    pre_state = prev.get("state")
                    post_state = current.get("state")

                    if not isinstance(entity_id, str) or not entity_id:
                        self._reject("history_missing_entity_id", "history", None, str(changed_at))
                        rejected += 1
                        rejected_reasons["history_missing_entity_id"] += 1
                        prev = current
                        continue
                    if not isinstance(changed_at, str) or not changed_at:
                        self._reject("history_missing_timestamp", "history", entity_id, None)
                        rejected += 1
                        rejected_reasons["history_missing_timestamp"] += 1
                        prev = current
                        continue
                    if pre_state is None or post_state is None:
                        self._reject("history_missing_state", "history", entity_id, changed_at)
                        rejected += 1
                        rejected_reasons["history_missing_state"] += 1
                        prev = current
                        continue

                    try:
                        timestamp = datetime.fromisoformat(changed_at.replace("Z", "+00:00"))
                    except ValueError:
                        self._reject("history_invalid_timestamp_format", "history", entity_id, changed_at)
                        rejected += 1
                        rejected_reasons["history_invalid_timestamp_format"] += 1
                        prev = current
                        continue

                    history_event = EventRecord(
                        timestamp=timestamp,
                        entity_id=entity_id,
                        actor_type=ActorType.SYSTEM,
                        action="state_change",
                        pre_state=str(pre_state),
                        post_state=str(post_state),
                        source_automation=None,
                        result=EventResult.SUCCESS,
                        reason_code="observed_history_state_change",
                    )
                    if self._repo.insert_event(history_event):
                        inserted += 1

                    prev = current

        return CollectSummary(
            inserted=inserted,
            rejected=rejected,
            rejected_reasons=dict(rejected_reasons),
        )

    @staticmethod
    def _actor_type_from_logbook(entry: dict) -> ActorType:
        if entry.get("context_user_id"):
            return ActorType.MANUAL
        if entry.get("context_domain") == "automation":
            return ActorType.AUTOMATION
        if entry.get("domain") == "automation":
            return ActorType.AUTOMATION
        if entry.get("context_event_type") == "automation_triggered":
            return ActorType.AUTOMATION
        domain = entry.get("domain")
        if isinstance(domain, str) and domain and domain != "automation":
            return ActorType.SYSTEM
        source = entry.get("source")
        if isinstance(source, str) and source:
            return ActorType.SYSTEM
        raise DataValidationError("Cannot classify actor_type from logbook entry")

    def _reject(
        self,
        reason_code: str,
        source: str,
        entity_id: str | None,
        raw_timestamp: str | None,
    ) -> None:
        self._repo.insert_collect_reject(
            reason_code=reason_code,
            source=source,
            entity_id=entity_id,
            raw_timestamp=raw_timestamp,
        )
