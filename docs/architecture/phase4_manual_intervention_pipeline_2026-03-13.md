# Phase 4 Manual Intervention Pipeline (2026-03-13, Asia/Seoul)

## Objective

Implement a maintainable pipeline that:

1. collects observed HA logbook events,
2. classifies actor (`manual|automation|system`),
3. enriches automation runs with manual override cancellation,
4. generates recommendation candidates from rule-based detections.

## Implemented Code

- Collection summary model and rejection accounting:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/collect_service.py`
- Manual override enrichment service:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/intervention_service.py`
- Event result update support:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/adapters/repository_sqlite.py`
- CLI command wiring:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/interfaces/cli.py`

## New/Updated Commands

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli collect-logbook \
  --db data/reco_engine.db --ha-url "<HA_URL>" --ha-token "<HA_TOKEN>" --hours 24

PYTHONPATH=src python3 -m reco_engine.interfaces.cli enrich-interventions \
  --db data/reco_engine.db --window-minutes 3

PYTHONPATH=src python3 -m reco_engine.interfaces.cli detect \
  --db data/reco_engine.db --policy config/policy.toml

PYTHONPATH=src python3 -m reco_engine.interfaces.cli propose \
  --db data/reco_engine.db --policy config/policy.toml
```

## Runtime Result Snapshot

- `collect-logbook`:
  - inserted: `523`
  - rejected: `4369`
- `enrich-interventions`:
  - updated_events: `0` (no matching reversal pair in sampled window)
- `detect`:
  - non-empty detections produced for:
    - `manual_repeat`
    - `manual_cancel_after_auto`
    - `condition_conflict`
- `propose`:
  - candidate insertions observed (`13` per run at current threshold)

## Data Integrity Policy Applied

- No fallback actor assignment is applied for unclassifiable logbook rows.
- Unclassifiable rows are explicitly counted as `rejected`.
- Recommendation generation consumes only inserted, classified events.

## Next Gate

Tune actor classification coverage to reduce rejection volume while preserving explicit failure semantics.
