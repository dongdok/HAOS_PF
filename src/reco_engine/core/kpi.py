from __future__ import annotations


def reduction_rate(before_count: int, after_count: int) -> float:
    if before_count <= 0:
        raise ValueError("before_count must be greater than zero")
    if after_count < 0:
        raise ValueError("after_count must be non-negative")
    return round((before_count - after_count) / before_count, 4)


def cancel_rate(cancelled: int, total_automation_actions: int) -> float:
    if total_automation_actions <= 0:
        raise ValueError("total_automation_actions must be greater than zero")
    if cancelled < 0:
        raise ValueError("cancelled must be non-negative")
    return round(cancelled / total_automation_actions, 4)

