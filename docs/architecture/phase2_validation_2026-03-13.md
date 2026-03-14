# Phase 2 Validation Report (2026-03-13, Asia/Seoul)

## Scope

- Canonical entity baseline validation
- Utility meter health validation
- Live docs sync check against Home Assistant states

## Implemented Artifacts

- Canonical baseline config:
  - `/Users/dy/Desktop/HAOS_Control/config/entities_canonical.toml`
- Validation service:
  - `/Users/dy/Desktop/HAOS_Control/src/reco_engine/services/validation_service.py`
- CLI commands:
  - `validate-canonical`
  - `validate-utility`

## Execution

```bash
PYTHONPATH=src python3 -m reco_engine.interfaces.cli validate-canonical \
  --ha-url "<HA_URL>" --ha-token "<HA_TOKEN>" \
  --canonical config/entities_canonical.toml

PYTHONPATH=src python3 -m reco_engine.interfaces.cli validate-utility \
  --ha-url "<HA_URL>" --ha-token "<HA_TOKEN>" \
  --canonical config/entities_canonical.toml
```

## Result Summary

### 1) Canonical validation

- Result: `ok = true`
- Errors: `0`
- Warnings: `0`

Interpretation:
- Recommendation input baseline is structurally valid.
- No missing required core entity in current live states.

### 2) Utility meter validation

- Result: `ok = false`
- Blocking errors: `4`

Blocking entities:
- `sensor.il_nujeog_hiteo_jeonryeog` (`state=unknown`)
- `sensor.il_nujeog_jeongimaeteu_jeonryeog` (`state=unknown`)
- `sensor.il_nujeog_deuraigi_jeonryeog` (`state=unknown`)
- `sensor.il_nujeog_gaseubgi_jeonryeog` (`state=unknown`)

Warnings (non-blocking but important):
- Daily utility entities currently miss `unit_of_measurement=kWh`
- Daily utility entities currently miss `device_class=energy`

Policy decision:
- This is treated as a hard data-quality failure.
- No recommendation KPI that depends on daily energy should be promoted until fixed.

### 3) Live docs sync

After updating `current_operating_map.md` and `master_hardware_map_live.md`, remaining non-live IDs are:

- `switch.anbang_hiteo_peulreogeu_2`
- `switch.anbang_stand_lighting_1`
- `switch.anbang_stand_lighting_100`
- `switch.hyeongwan_door_virtual_spare`

Interpretation:
- All remaining misses are disabled/hidden reserve entities.
- Active operational baseline is now aligned to live states.

## Next Action (Phase 3 Gate)

1. Fix daily utility-meter source mapping and attributes until all four daily entities leave `unknown`.
2. Re-run `validate-utility` and require `ok=true`.
3. Only then enable KPI computations that consume daily energy series.

Status update:
- Completed in
  `/Users/dy/Desktop/HAOS_Control/docs/architecture/phase3_utility_meter_repair_2026-03-13.md`.
