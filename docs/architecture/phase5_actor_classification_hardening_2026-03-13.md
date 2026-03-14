# Phase 5 Actor Classification Hardening (2026-03-13, Asia/Seoul)

## Objective

Reduce collection rejection volume without introducing fallback guesses.

## Changes

### 1) Collection logic hardening

Updated:
- `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/collect_service.py`

Applied rules:
- Keep hard reject when `entity_id` or `when` is missing.
- Classify events explicitly:
  - `manual`: `context_user_id` present
  - `automation`: automation context/domain or `context_event_type=automation_triggered`
  - `system`: valid event with entity/timestamp but non-manual, non-automation
- Support two event types:
  - `state_change` when `state` exists
  - `event` when only log message exists (`script started`, `automation triggered`, etc.)

### 2) HA client logbook robustness

Updated:
- `/Users/dy/Desktop/HAOS_Control/src/reco_engine/adapters/ha_client.py`

Fixes:
- UTC timestamp conversion for logbook/history calls
- URL-safe encoding for time and entity query parameters

### 3) Idempotent persistence

Updated:
- `/Users/dy/Desktop/HAOS_Control/src/reco_engine/adapters/repository_sqlite.py`
- `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/proposal_service.py`

Additions:
- Event insert dedup check (same timestamp/entity/actor/action/state tuple)
- Candidate insert dedup check (same proposed record payload)

## Measured Result

Before hardening (24h run):
- inserted: `523`
- rejected: `4369`

After hardening (24h run):
- inserted: `4906`
- rejected: `2`

Re-run behavior after dedup:
- additional inserted after immediate rerun: `18` (new events only)

## Integrity Notes

- No silent fallback actor assignment was added.
- Rejection still occurs for structurally invalid records (missing required keys).
- Failure visibility is preserved via `rejected` counter.
