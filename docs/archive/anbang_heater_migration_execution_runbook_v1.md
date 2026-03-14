# Anbang Heater Migration Execution Runbook v1

Last updated: 2026-03-03
Status: ready for execution planning

## Objective

Migrate the bedroom heater entity ids from stale `jubang_ac_heating_*` ids to canonical `anbang_heater_*` ids.

Target ids:

- `switch.anbang_heater_plug`
- `sensor.anbang_heater_current`
- `sensor.anbang_heater_power`
- `sensor.anbang_heater_voltage`
- `sensor.anbang_heater_total_energy`

## Current Source Entities

- `switch.jubang_ac_heating_plug`
- `sensor.jubang_ac_heating_current`
- `sensor.jubang_ac_heating_power`
- `sensor.jubang_ac_heating_voltage`
- `sensor.jubang_ac_heating_total_energy`

## Confirmed Reference Scope

Direct live dashboard references:

- `switch.jubang_ac_heating_plug`
  - bedroom tile in `홈킷 뷰(Sections)`
  - bedroom tile in `Home`

No direct live dashboard references were found for:

- `sensor.jubang_ac_heating_current`
- `sensor.jubang_ac_heating_power`
- `sensor.jubang_ac_heating_voltage`
- `sensor.jubang_ac_heating_total_energy`

## Migration Decision Gate

Proceed only if one of these is true:

1. Home Assistant supports direct entity id rename for this integration path
2. The integration can be safely re-created under the target ids
3. New wrapper entities can be introduced and dashboards updated to those wrappers

If none of the above is true, stop and do not force the migration.

## Recommended Execution Order

### Phase 1: Backup

Create and keep:

- current live Lovelace backup
- current entity registry snapshot
- current states snapshot
- a note of the exact source ids and target ids

### Phase 2: Rename Or Recreate

Preferred order:

1. `switch.jubang_ac_heating_plug` -> `switch.anbang_heater_plug`
2. `sensor.jubang_ac_heating_current` -> `sensor.anbang_heater_current`
3. `sensor.jubang_ac_heating_power` -> `sensor.anbang_heater_power`
4. `sensor.jubang_ac_heating_voltage` -> `sensor.anbang_heater_voltage`
5. `sensor.jubang_ac_heating_total_energy` -> `sensor.anbang_heater_total_energy`

### Phase 3: Dashboard Update

Update direct dashboard references:

- replace `switch.jubang_ac_heating_plug` with `switch.anbang_heater_plug`

### Phase 4: Workspace Update

Update these local docs and scripts:

- [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
- [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
- [standardization_plan_anbang_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_anbang_v1.md)
- [anbang_display_name_cleanup_v1.md](/Users/dy/Desktop/HAOS_Control/docs/anbang_display_name_cleanup_v1.md)
- [anbang_heater_entity_migration_plan_v1.md](/Users/dy/Desktop/HAOS_Control/docs/anbang_heater_entity_migration_plan_v1.md)
- any helper scripts containing `jubang_ac_heating_*`

### Phase 5: Verification

Verify:

1. new ids exist in live states
2. old ids are no longer used in the live dashboard
3. heater control still works from the dashboard
4. heater metrics still update
5. no broken entity cards appear

## Rollback Plan

If any step fails:

1. restore previous dashboard config
2. restore previous entity naming or exposure method
3. verify `switch.jubang_ac_heating_plug` works again
4. stop and re-audit before retrying

## Practical Note

The likely safest implementation path is not a blind rename.

Safer options, in order:

1. direct entity id rename if officially supported and verified
2. controlled recreation under canonical ids
3. wrapper or proxy entities if rename is not supported

## Next Technical Task

Determine which migration mechanism is actually supported for these Tuya-backed entities:

- direct entity id rename
- entity registry update with new id
- remove/re-add with canonical naming
- helper/proxy abstraction
