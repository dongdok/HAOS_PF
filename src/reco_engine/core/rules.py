from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
import re

from .entities import EventRecord

PRESENCE_TO_PRIMARY_CONTROL = {
    "binary_sensor.geosil_presence": "switch.geosil_ceiling_light",
    "binary_sensor.jubang_presence": "switch.jubang_ceiling_light",
    "binary_sensor.anbang_presence": "switch.anbang_ceiling_light",
    "binary_sensor.osbang_presence": "switch.osbang_ceiling_light",
    "binary_sensor.hwajangsil_presence": "switch.hwajangsil_ceiling_light",
}

ENV_RESPONSE_RULES = [
    {
        "sensor_entity_id": "sensor.osbang_seubdo_rokeol",
        "operator": ">=",
        "threshold": 60.0,
        "target_entity_id": "humidifier.osbang_jeseubgi_rokeol_naebuseubdo",
        "expected_target_states": {"on"},
    },
    {
        "sensor_entity_id": "sensor.anbang_temperature",
        "operator": "<=",
        "threshold": 19.0,
        "target_entity_id": "climate.anbang_hiteo",
        "expected_target_states": {"heat", "heating", "on"},
    },
    {
        "sensor_entity_id": "sensor.anbang_temperature",
        "operator": ">=",
        "threshold": 24.0,
        "target_entity_id": "climate.anbang_hiteo",
        "expected_target_states": {"off"},
    },
]

DOOR_ENTITY_ID = "binary_sensor.hyeongwan_door"
OUTING_TARGET_ENTITY_ID = "input_boolean.gasang_hyeongwan_oecul_1"
HOMECOMING_TARGET_ENTITY_ID = "input_boolean.gasang_hyeongwan_doeo"
HOME_PRESENCE_ENTITIES = {
    "binary_sensor.geosil_presence",
    "binary_sensor.jubang_presence",
    "binary_sensor.anbang_presence",
    "binary_sensor.osbang_presence",
    "binary_sensor.hwajangsil_presence",
}


def detect_repeated_manual_toggles(
    events: list[EventRecord],
    min_count: int,
) -> dict[str, int]:
    """Detect entities repeatedly toggled manually in similar time bands."""
    counts: dict[str, int] = defaultdict(int)
    for event in events:
        if event.actor_type.value == "manual" and event.post_state in {"on", "off"}:
            counts[event.entity_id] += 1
    return {entity_id: count for entity_id, count in counts.items() if count >= min_count}


def detect_manual_cancels_after_automation(
    events: list[EventRecord],
    window_minutes: int,
) -> dict[str, int]:
    """Detect manual reversals shortly after automation actions."""
    window = timedelta(minutes=window_minutes)
    hits: dict[str, int] = defaultdict(int)
    ordered = sorted(events, key=lambda item: item.timestamp)

    for i, base in enumerate(ordered):
        if base.actor_type.value != "automation" or base.post_state not in {"on", "off"}:
            continue
        for candidate in ordered[i + 1 :]:
            if candidate.timestamp - base.timestamp > window:
                break
            if (
                candidate.entity_id == base.entity_id
                and candidate.actor_type.value == "manual"
                and candidate.post_state in {"on", "off"}
                and candidate.post_state != base.post_state
            ):
                hits[base.entity_id] += 1
                break

    return dict(hits)


def detect_condition_conflicts(events: list[EventRecord], window_minutes: int) -> dict[str, int]:
    """Detect rapid opposite actions from different automations on the same entity."""
    window = timedelta(minutes=window_minutes)
    hits: dict[str, int] = defaultdict(int)
    ordered = sorted(events, key=lambda item: item.timestamp)

    for i, left in enumerate(ordered):
        if left.actor_type.value != "automation" or not left.source_automation:
            continue
        for right in ordered[i + 1 :]:
            if right.timestamp - left.timestamp > window:
                break
            if (
                right.entity_id == left.entity_id
                and right.actor_type.value == "automation"
                and right.source_automation
                and right.source_automation != left.source_automation
                and right.post_state in {"on", "off"}
                and left.post_state in {"on", "off"}
                and right.post_state != left.post_state
            ):
                hits[left.entity_id] += 1
                break

    return dict(hits)


def detect_presence_transition_patterns(
    events: list[EventRecord],
    min_count: int,
    window_minutes: int,
) -> dict[str, int]:
    """Detect repeated room-to-room movement arrivals from presence sensor transitions."""
    window = timedelta(minutes=window_minutes)
    arrivals = [
        event
        for event in sorted(events, key=lambda item: item.timestamp)
        if event.entity_id in PRESENCE_TO_PRIMARY_CONTROL and event.post_state == "on"
    ]

    hits: dict[str, int] = defaultdict(int)
    for idx, current in enumerate(arrivals):
        for previous in reversed(arrivals[:idx]):
            if current.timestamp - previous.timestamp > window:
                break
            if previous.entity_id == current.entity_id:
                continue
            target_entity = PRESENCE_TO_PRIMARY_CONTROL[current.entity_id]
            hits[target_entity] += 1
            break

    return {
        entity_id: count
        for entity_id, count in hits.items()
        if count >= min_count
    }


def detect_env_response_patterns(
    events: list[EventRecord],
    min_count: int,
    window_minutes: int,
) -> dict[str, int]:
    """Detect repeated manual/device responses after humidity/temperature threshold events."""
    window = timedelta(minutes=window_minutes)
    ordered = sorted(events, key=lambda item: item.timestamp)
    hits: dict[str, int] = defaultdict(int)

    for idx, base in enumerate(ordered):
        value = _parse_numeric(base.post_state)
        if value is None:
            continue

        matched_rule = None
        for rule in ENV_RESPONSE_RULES:
            if base.entity_id != rule["sensor_entity_id"]:
                continue
            if _compare_numeric(value, rule["operator"], float(rule["threshold"])):
                matched_rule = rule
                break
        if matched_rule is None:
            continue

        for candidate in ordered[idx + 1 :]:
            if candidate.timestamp - base.timestamp > window:
                break
            if candidate.entity_id != matched_rule["target_entity_id"]:
                continue
            expected_states = {
                str(item).strip().lower()
                for item in matched_rule["expected_target_states"]
            }
            candidate_state = str(candidate.post_state).strip().lower()
            if candidate_state not in expected_states:
                continue
            hits[candidate.entity_id] += 1
            break

    return {
        entity_id: count
        for entity_id, count in hits.items()
        if count >= min_count
    }


def detect_door_presence_time_patterns(
    events: list[EventRecord],
    min_count: int,
    window_minutes: int,
) -> dict[str, int]:
    """Detect repeated outing/homecoming scenarios from door + presence changes in similar hours."""
    window = timedelta(minutes=window_minutes)
    ordered = sorted(events, key=lambda item: item.timestamp)
    bucket_hits: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))

    for idx, base in enumerate(ordered):
        if base.entity_id != DOOR_ENTITY_ID or base.post_state != "on":
            continue
        hour_bucket = base.timestamp.hour

        saw_presence_off = False
        saw_presence_on = False
        for candidate in ordered[idx + 1 :]:
            if candidate.timestamp - base.timestamp > window:
                break
            if candidate.entity_id not in HOME_PRESENCE_ENTITIES:
                continue
            if candidate.post_state == "off":
                saw_presence_off = True
            elif candidate.post_state == "on":
                saw_presence_on = True

        if saw_presence_off:
            bucket_hits[OUTING_TARGET_ENTITY_ID][hour_bucket] += 1
        if saw_presence_on:
            bucket_hits[HOMECOMING_TARGET_ENTITY_ID][hour_bucket] += 1

    results: dict[str, int] = {}
    for target_entity_id, by_hour in bucket_hits.items():
        evidence = max(by_hour.values(), default=0)
        if evidence >= min_count:
            results[target_entity_id] = evidence
    return results


def _parse_numeric(raw: str) -> float | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    match = re.search(r"[-+]?[0-9]*\.?[0-9]+", text)
    if not match:
        return None
    return float(match.group(0))


def _compare_numeric(value: float, operator: str, threshold: float) -> bool:
    if operator == ">=":
        return value >= threshold
    if operator == ">":
        return value > threshold
    if operator == "<=":
        return value <= threshold
    if operator == "<":
        return value < threshold
    if operator == "==":
        return value == threshold
    raise ValueError(f"unsupported operator: {operator}")
