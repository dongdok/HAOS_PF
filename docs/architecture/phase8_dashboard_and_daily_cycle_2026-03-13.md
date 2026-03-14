# Phase 8 Dashboard Cards + Daily Cycle (2026-03-13, Asia/Seoul)

## Objective

Implement operational outputs for immediate use:

1. three recommendation dashboard cards,
2. one-shot daily run command for stable operations.

## Implemented Code

- Daily orchestration:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/pipeline_service.py`
- Card payload generation:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/dashboard_card_service.py`
- CLI command wiring:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/interfaces/cli.py`

## Added Commands

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli dashboard-cards \
  --db data/reco_engine.db \
  --output data/dashboard_cards.json

PYTHONPATH=src python3 -m reco_engine.interfaces.cli run-daily-cycle \
  --db data/reco_engine.db \
  --ha-url "<HA_URL>" \
  --ha-token "<HA_TOKEN>" \
  --policy config/policy.toml \
  --canonical config/entities_canonical.toml \
  --collect-hours 24 \
  --intervention-window-minutes 3
```

## Runtime Verification

### dashboard-cards

- Output file created:
  - `/Users/dy/Desktop/HAOS_Control/data/dashboard_cards.json`
- Contains exactly 3 markdown cards:
  - 오늘의 후보 자동화
  - 충돌/오동작 상위 5개
  - 절감 기여 상위 5개

### run-daily-cycle

Observed run result:

- `collected_inserted`: `131`
- `collected_rejected`: `2`
- `interventions_updated`: `1`
- `proposals_inserted`: `1`
- `monthly_energy_entity_id`: `sensor.weol_nujeog_cong_jeonryeog`
- `monthly_energy_kwh`: `0.009`

## Integrity Notes

- No default/fallback monthly energy value is used.
- Daily-cycle run fails explicitly on invalid canonical/energy state conditions.
- Dashboard output is derived only from persisted DB facts.

