# HAOS Standardization v1 Complete

Last updated: 2026-03-03
Status: active baseline

## Purpose

This document marks the end of the first full standardization pass.

It should be read together with:

- [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
- [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
- [naming_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md)

## What v1 Completed

### 1. Live truth source recovered

- Dashboard references were brought back to the current live entity set.
- Active Lovelace now resolves without missing entities.
- Room-by-room cleanup was done from the live HA state, not from stale rescue mappings.

### 2. Core room structure standardized

- 안방
  - `switch.anbang_ceiling_light`
  - `light.anbang_stand_lighting`
  - `switch.anbang_heater_plug`
  - `sensor.anbang_temperature`
  - `sensor.anbang_humidity`
  - `sensor.anbang_th_monitor_battery`
  - `switch.anbang_bedtime_virtual`
  - `switch.anbang_goodnight_virtual`
  - `switch.anbang_stand_lighting_1`
  - `switch.anbang_stand_lighting_100`
  - `scene.anbang_stand_lighting_1`
  - `scene.anbang_stand_lighting_100`

- 거실
  - `switch.geosil_ceiling_light`
  - `light.geosil_stand_lighting`
  - `light.geosil_line_lighting`
  - `switch.geosil_line_lighting_plug`
  - `media_player.geosil_tv`
  - `sensor.geosil_tv_illuminance`
  - `sensor.geosil_tv_brightness`

- 주방
  - `switch.jubang_ceiling_light`
  - `switch.jubang_presence_sensor_plug`
  - `switch.jubang_hair_dryer_plug`
  - `switch.jubang_line_lighting_plug`
  - `switch.jubang_ac_remote_hub`

- 옷방
  - `switch.osbang_ceiling_light`
  - `sensor.osbang_temperature`
  - `sensor.osbang_humidity`
  - `sensor.osbang_th_monitor_battery`

- 화장실
  - `switch.hwajangsil_ceiling_light`
  - `switch.hwajangsil_vent_fan`
  - `binary_sensor.hwajangsil_door_contact`
  - `sensor.hwajangsil_door_battery`

- 현관
  - `binary_sensor.hyeongwan_door`
  - `sensor.hyeongwan_door_battery`
  - `binary_sensor.hyeongwan_door_tamper`
  - `switch.hyeongwan_outing_virtual_1`
  - `switch.hyeongwan_outing_virtual_2`

### 3. Dashboard stabilized

- Main Lovelace room cards were corrected after the entity-id migrations.
- Repeated problems from stale cards and duplicated cards were removed.
- Validation target after each change was:
  - `missing_count = 0`

## Canonical Baseline

Use these three documents in this order:

1. [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
2. [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
3. [naming_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md)

Interpretation:

- `current_operating_map.md`
  - short operational summary
- `master_hardware_map_live.md`
  - live entity inventory
- `naming_standard_v1.md`
  - long-term target rule set

## Remaining Exceptions

These are no longer blocking, but they still exist as policy exceptions or lower-priority cleanup items.

- `binary_sensor.hwajangsil_door_contact`
  - still uses `door_contact` instead of the shorter `door`
- some legacy/historical docs still mention pre-v1 ids
- some one-off scripts still contain old ids for historical recovery purposes

## Definition Of Done For v1

v1 should be treated as complete when all of the following are true:

- main dashboard works
- `lovelace_active.json` has no missing entity references
- each active room has one canonical area-id family
- helper/virtual entities are named as helper/virtual entities
- preset entities no longer use opaque transliterated ids

That condition is now met.
