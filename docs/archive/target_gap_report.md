# Target Gap Report

Last verified: 2026-03-03
Reference target: user-provided "Master Hardware Map - final"

## Summary

The target hardware map is usable as a future naming target.
It is not safe to use as the current operating source of truth.

Reason:
- many target entity ids do not currently exist in live Home Assistant states
- some target entities exist only in the registry as stale references
- some devices are now exposed under different domains or different ids

## High-Risk Mismatches

### 안방

- Target `light.anbang_lighting`
  - Live equivalents: `switch.anbangbul`, `light.anbangjomyeong`, `light.anbangjomyeong_2`
- Target `light.anbang_stand_lighting`
  - Live status: not present
- Target `cover.anbang_curtain`
  - Live equivalent: `cover.curtain`
- Target `binary_sensor.anbang_presence`
  - Live equivalent: `binary_sensor.anbang_jaesilsenseo_occupancy`
- Target `binary_sensor.anbang_bedside_presence`
  - Live equivalent: `binary_sensor.meorimat_jaesilsenseo_occupancy`
- Target `climate.anbang_heater`
  - Live status: not present as climate entity
- Target `switch.anbang_humidifier_plug`
  - Live equivalent: `switch.gaseubgi`
- Target `switch.anbang_electric_blanket_plug`
  - Live equivalent: `switch.jeongimaeteu`

### 거실

- Target `media_player.geosil_tv`
  - Live equivalent: `media_player.43_smart_monitor_m7`
- Target `light.geosil_lighting`
  - Live equivalents: `switch.geosilbul`, `light.geosiljomyeong`, `light.geosiljomyeong_2`
- Target `light.geosil_stand_lighting`
  - Live status: not present
- Target `light.geosil_curtain_lighting`
  - Live equivalents: `switch.keoteunbul`, `light.keoteunbul`, `light.keoteunbul_2`
- Target `binary_sensor.geosil_presence`
  - Live equivalent: `binary_sensor.geosil_jaesilsenseo_occupancy`

### 주방

- Target `light.jubang_lighting`
  - Live equivalent: `switch.jubangbul`
- Target `binary_sensor.jubang_presence`
  - Live equivalent: `binary_sensor.jubang_jaesil_senseo_occupancy`
- Target `switch.jubang_dryer_plug`
  - Live equivalent: `switch.deuraigi`
- Target `switch.jubang_appliance_multitap`
  - Live equivalents:
    - `switch.2jubang_jaesil_3deuraigibul_switch_1`
    - `switch.2jubang_jaesil_3deuraigibul_switch_2`
    - `switch.2jubang_jaesil_3deuraigibul_switch_3`
- Target `remote.jubang_ac_hub`
  - Live status: not confirmed as remote entity

### 옷방

- Target `light.osbang_lighting`
  - Live equivalent: `switch.osbangbul`
- Target `binary_sensor.osbang_presence`
  - Live equivalent: `binary_sensor.osbang_jaesilsenseo_occupancy`
- Target `sensor.osbang_th_monitor`
  - Live equivalents:
    - `sensor.osbang_onseubdosenseo_temperature`
    - `sensor.osbang_onseubdosenseo_humidity`
- Target `humidifier.osbang_dehumidifier`
  - Live equivalents: `humidifier.jeseubgi`, `fan.jeseubgi`

### 화장실 / 현관

- Target `light.hwajangsil_lighting`
  - Live equivalents: `switch.hwajangsil_bul`, `switch.hwajangsil_bul_2`
- Target `binary_sensor.hwajangsil_presence`
  - Live equivalent: `binary_sensor.hwajangsil_jaesilsenseo_occupancy`
- Target `binary_sensor.hwajangsil_door`
  - Live equivalents:
    - `binary_sensor.hwajangsil_doeosenseo_door`
    - `binary_sensor.hwajangsil_doeosenseo_door_2`
- Target `binary_sensor.hyengwan_door`
  - Live equivalents:
    - `binary_sensor.hyeongwandoeosenseo_door`
    - `binary_sensor.hyeongwandoeosenseo_door_2`

## Interpretation

The target map should be treated as a target schema, not a live registry mirror.

Safe usage:
- naming convention target
- cleanup target
- future dashboard design target

Unsafe usage:
- direct dashboard entity references
- direct automation updates without live validation
- cleanup decisions based only on the target document

## Recommended Next Step

Use a two-layer model:

1. `current_operating_map.md`
   - live source of truth
2. target hardware map
   - desired final naming model

Only after the mapping is reviewed should dashboards or automations be updated.
