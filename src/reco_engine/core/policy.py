from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnginePolicy:
    manual_repeat_min_count: int
    cancel_window_minutes: int
    conflict_window_minutes: int
    movement_repeat_min_count: int
    movement_window_minutes: int
    env_pattern_min_count: int
    env_response_window_minutes: int
    door_pattern_min_count: int
    door_pattern_window_minutes: int
    test_window_days: int
    min_confidence_to_propose: float
