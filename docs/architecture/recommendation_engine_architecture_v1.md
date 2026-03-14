# Recommendation Engine Architecture v1

## Purpose

This module defines a log/data-driven recommendation pipeline for Home Assistant.
It is designed for:

- macOS and Windows parity
- strict fail-fast behavior
- additive architecture without monolithic scripts

## Layering

1. `core/`
- Domain entities, rules, KPI formulas, scoring.
- No Home Assistant or SQLite dependencies.

2. `adapters/`
- Home Assistant API access (`ha_client.py`)
- SQLite persistence (`repository_sqlite.py`)

3. `services/`
- `collect_service`: ingest observed events
- `detection_service`: run rule detections
- `proposal_service`: persist proposal-only recommendations
- `kpi_service`: compute and store KPI snapshots
- `ops_summary_service`: dashboard-ready top-card summaries
- `dashboard_card_service`: HA markdown card payload generation
- `pipeline_service`: daily run orchestration (`collect -> intervention -> detect -> propose -> kpi`)
- `feedback_service`: user feedback ingestion (`intended` / `unintended`)

4. `interfaces/`
- `cli.py` command entrypoint

## Event Logging Policy

Required fields:

- `timestamp`
- `entity_id`
- `actor_type` (`manual|automation|system`)
- `action`
- `pre_state`
- `post_state`
- `source_automation`
- `result` (`success|failed|cancelled`)
- `reason_code`

No fallback values are synthesized.
If actor classification is impossible, execution fails explicitly.

## Commands

```bash
reco-engine init-db --db data/reco_engine.db
reco-engine collect-logbook --db data/reco_engine.db --ha-url <url> --ha-token <token> --hours 24
reco-engine detect --db data/reco_engine.db --policy config/policy.toml
reco-engine propose --db data/reco_engine.db --policy config/policy.toml
reco-engine enrich-interventions --db data/reco_engine.db --window-minutes 3
reco-engine approve-candidates --db data/reco_engine.db --candidate-ids 1,2,3
reco-engine start-test-batch --db data/reco_engine.db --candidate-ids 1,2,3 --days 7
reco-engine finalize-test-batch --db data/reco_engine.db --batch-id 1 --result pass
reco-engine rollback-batch --db data/reco_engine.db --batch-id 1 --reason "rollback reason"
reco-engine validate-canonical --ha-url <url> --ha-token <token> --canonical config/entities_canonical.toml
reco-engine validate-utility --ha-url <url> --ha-token <token> --canonical config/entities_canonical.toml
reco-engine kpi --db data/reco_engine.db --monthly-energy-kwh 12.5
reco-engine kpi-auto --db data/reco_engine.db --ha-url <url> --ha-token <token> --canonical config/entities_canonical.toml
reco-engine ops-summary --db data/reco_engine.db
reco-engine dashboard-cards --db data/reco_engine.db --output data/dashboard_cards.json
reco-engine run-daily-cycle --db data/reco_engine.db --ha-url <url> --ha-token <token> --policy config/policy.toml --canonical config/entities_canonical.toml --collect-hours 24 --intervention-window-minutes 3
reco-engine ingest-conflict-feedback --db data/reco_engine.db
```

## Cross-Platform Execution

macOS/Linux:

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli --help
```

Windows (PowerShell):

```powershell
$env:PYTHONPATH = "src"
python -m reco_engine.interfaces.cli --help
```

Windows (cmd):

```bat
set PYTHONPATH=src
python -m reco_engine.interfaces.cli --help
```

## Operational Notes

- `kpi-auto` reads monthly energy from canonical config:
  `required_utility_meter_entities.monthly[0]`.
- Invalid monthly energy state (`unknown`, `unavailable`, non-numeric, negative)
  fails explicitly.
- `dashboard-cards` generates exactly three cards:
  - 오늘의 후보 자동화
  - 충돌/오동작 상위 5개
  - 절감 기여 상위 5개
- conflict feedback buttons are persisted via HA helpers (`input_select`) and
  ingested by `ingest-conflict-feedback`.
