# Phase 7 Ops Summary + KPI Auto (2026-03-13, Asia/Seoul)

## Objective

Complete two operational gaps:

1. provide dashboard-ready recommendation summaries from DB,
2. remove manual KPI energy input by reading canonical monthly energy directly from HA.

## Implemented Code

- CLI command wiring:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/interfaces/cli.py`
- Ops summary service (already created, now wired):
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/ops_summary_service.py`
- KPI auto source/validation:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/kpi_service.py`
- HA single-entity state read:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/adapters/ha_client.py`

## New Commands

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli ops-summary \
  --db data/reco_engine.db

PYTHONPATH=src python3 -m reco_engine.interfaces.cli kpi-auto \
  --db data/reco_engine.db \
  --ha-url "<HA_URL>" \
  --ha-token "<HA_TOKEN>" \
  --canonical config/entities_canonical.toml
```

## Policy/Integrity

- No fallback/default monthly energy is used.
- Canonical monthly source is mandatory:
  - `required_utility_meter_entities.monthly[0]`
- Hard failures:
  - missing canonical monthly config
  - HA state `unknown|unavailable|none`
  - non-numeric monthly energy state
  - negative monthly energy value

## Output Contract

### `ops-summary`

- `today_candidates` (status: `proposed|approved|testing`)
- `conflict_top5` (`rule_code=condition_conflict`)
- `savings_top5` (`rule_code in manual_repeat/manual_cancel_after_auto`)

### `kpi-auto`

- `source_entity_id`
- KPI snapshot fields identical to `kpi` command output

