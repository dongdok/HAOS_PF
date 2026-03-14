# Phase 9 Feedback Buttons + Engine Reflection (2026-03-13, Asia/Seoul)

## Objective

Implement user-driven conflict labeling:

1. dashboard buttons for `의도됨` / `문제`,
2. ingestion into engine DB,
3. apply labels to conflict recommendation ranking/proposal generation.

## Implemented Code

- Feedback ingestion service:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/feedback_service.py`
- DB schema extension:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/adapters/repository_sqlite.py`
- Proposal filtering:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/proposal_service.py`
- Conflict summary filtering:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/ops_summary_service.py`
- CLI command wiring:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/interfaces/cli.py`

## New Command

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli ingest-conflict-feedback \
  --db data/reco_engine.db
```

## Home Assistant UI Changes

- Added 10 feedback scripts (`script.reco_feedback_*`) for compatibility.
- Added 5 `input_select` helpers for stable feedback logging:
  - `input_select.cuceonpideubaeg_1beon_sangtae`
  - `input_select.cuceonpideubaeg_2beon_sangtae`
  - `input_select.cuceonpideubaeg_3beon_sangtae`
  - `input_select.cuceonpideubaeg_4beon_sangtae`
  - `input_select.cuceonpideubaeg_5beon_sangtae`
- Added dashboard card section `충돌 피드백 버튼` with per-item buttons:
  - `의도됨` -> helper option `의도됨`
  - `문제` -> helper option `문제`

## Reflection Behavior

- `condition_conflict` proposals are skipped when latest verdict is `intended`.
- `ops-summary` conflict top5 excludes entities with latest verdict `intended`.

## Verification

- Feedback ingestion command returns non-empty `latest_verdict_map`.
- Current reflected intended labels:
  - `light.geosil_keoteun_rain_jomyeong_rokeol`
  - `light.geosil_stand_lighting`
  - `switch.jubang_ceiling_light`

