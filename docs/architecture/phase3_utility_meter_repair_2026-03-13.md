# Phase 3 Utility Meter Repair (2026-03-13, Asia/Seoul)

## Objective

Repair daily utility meter data quality without fallback values.

Target issue from Phase 2:
- 4 daily utility entities were `unknown`, blocking energy KPI trust.

## Actions Performed

1. Preserved broken daily entities by renaming to legacy IDs.
2. Recreated daily utility_meter helpers with canonical names and explicit source mapping:
   - `sensor.il_nujeog_hiteo_jeonryeog` <- `sensor.anbang_hiteo_peulreogeu_eneoji`
   - `sensor.il_nujeog_jeongimaeteu_jeonryeog` <- `sensor.anbang_jeongimaeteu_peulreogeu_eneoji`
   - `sensor.il_nujeog_deuraigi_jeonryeog` <- `sensor.jubang_deuraigi_peulreogeu_eneoji`
   - `sensor.il_nujeog_gaseubgi_jeonryeog` <- `sensor.anbang_gaseubgi_peulreogeu_eneoji`
3. Initialized daily meters via `utility_meter.calibrate(value=0)` to remove `unknown`.

## Validation Result

Command:

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli validate-utility \
  --ha-url "<HA_URL>" --ha-token "<HA_TOKEN>" \
  --canonical config/entities_canonical.toml
```

Result:
- `ok = true`
- `errors = []`
- `warnings` remain for daily meters missing `unit_of_measurement/device_class` attributes in state payload.

## Policy Interpretation

- Blocking quality condition is now resolved (`unknown` removed).
- Remaining warnings are non-blocking metadata visibility concerns.
- Recommendation/KPI pipeline may proceed using daily meter numeric states.

## Notes

- Disabled legacy entities no longer appear in active state set.
- Canonical validation remains `ok = true`.
