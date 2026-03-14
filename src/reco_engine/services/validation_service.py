from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from reco_engine.adapters.ha_client import HAClient
from reco_engine.core.errors import DataValidationError


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]
    warnings: list[str]


class ValidationService:
    def __init__(self, ha_client: HAClient):
        self._ha = ha_client

    def validate_canonical_entities(self, config: dict[str, Any]) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        states = self._ha.fetch_states()
        by_id = {item["entity_id"]: item for item in states if "entity_id" in item}

        for entity_id in config.get("required_core_entities", []):
            if entity_id not in by_id:
                errors.append(f"missing core entity: {entity_id}")

        for spec in config.get("required_measurement_entities", []):
            entity_id = spec["entity_id"]
            state = by_id.get(entity_id)
            if state is None:
                errors.append(f"missing measurement entity: {entity_id}")
                continue

            attrs = state.get("attributes", {})
            required_device_class = spec.get("required_device_class")
            if required_device_class and attrs.get("device_class") != required_device_class:
                errors.append(
                    f"{entity_id}: device_class={attrs.get('device_class')} expected={required_device_class}"
                )

            required_state_class = spec.get("required_state_class")
            if required_state_class and attrs.get("state_class") != required_state_class:
                errors.append(
                    f"{entity_id}: state_class={attrs.get('state_class')} expected={required_state_class}"
                )

        return ValidationResult(ok=not errors, errors=errors, warnings=warnings)

    def validate_utility_meter_health(self, config: dict[str, Any]) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        states = self._ha.fetch_states()
        by_id = {item["entity_id"]: item for item in states if "entity_id" in item}
        utility_config = config.get("required_utility_meter_entities", {})

        for group, entities in utility_config.items():
            for entity_id in entities:
                state = by_id.get(entity_id)
                if state is None:
                    errors.append(f"missing utility_meter entity ({group}): {entity_id}")
                    continue

                value = str(state.get("state"))
                attrs = state.get("attributes", {})
                if value in {"unknown", "unavailable", "none", "None"}:
                    errors.append(f"{entity_id}: invalid state={value}")

                if attrs.get("state_class") != "total_increasing":
                    errors.append(f"{entity_id}: state_class must be total_increasing")

                if group == "monthly":
                    if attrs.get("unit_of_measurement") != "kWh":
                        errors.append(f"{entity_id}: monthly unit must be kWh")
                    if attrs.get("device_class") != "energy":
                        errors.append(f"{entity_id}: monthly device_class must be energy")
                if group == "daily":
                    if attrs.get("unit_of_measurement") != "kWh":
                        warnings.append(f"{entity_id}: daily unit_of_measurement is missing or not kWh")
                    if attrs.get("device_class") != "energy":
                        warnings.append(f"{entity_id}: daily device_class is missing or not energy")

        return ValidationResult(ok=not errors, errors=errors, warnings=warnings)

    @staticmethod
    def assert_ok(result: ValidationResult) -> None:
        if not result.ok:
            joined = "\n".join(result.errors)
            raise DataValidationError(joined)

