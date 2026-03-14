# Entity ID Mapping

Last verified: 2026-03-03
Purpose: safe replacement map from legacy target ids to current live ids

## Rules

- `legacy_entity_id` is the old or target id from the old master hardware map.
- `current_live_entity_id` is a currently live entity confirmed in Home Assistant states.
- If multiple current entities exist, prefer the first one unless a dashboard or automation needs the alternate form.
- Do not bulk rename Home Assistant entities from this file without separate validation.

## Mapping Table

| Area | Legacy / Target Entity ID | Current Live Entity ID | Notes |
|---|---|---|---|
| 안방 | `light.anbang_lighting` | `switch.anbangbul` | `light.anbangjomyeong`, `light.anbangjomyeong_2` also exist |
| 안방 | `light.anbang_stand_lighting` | none | no live equivalent confirmed |
| 안방 | `cover.anbang_curtain` | `cover.curtain` | current curtain entity is generic |
| 안방 | `switch.anbang_humidifier_plug` | `switch.gaseubgi` | |
| 안방 | `switch.anbang_electric_blanket_plug` | `switch.jeongimaeteu` | |
| 안방 | `switch.anbang_desk_multitap` | `switch.1caegsangseonpunggi` | desk group is currently split across individual switches |
| 안방 | `switch.anbang_bed_multitap` | `switch.1cimdaedeung_seuwici` | bed group is currently split across individual switches |
| 안방 | `binary_sensor.anbang_presence` | `binary_sensor.anbang_jaesilsenseo_occupancy` | |
| 안방 | `binary_sensor.anbang_bedside_presence` | `binary_sensor.meorimat_jaesilsenseo_occupancy` | |
| 안방 | `binary_sensor.anbang_round_vibration` | none | no live equivalent confirmed |
| 안방 | `sensor.anbang_th_monitor` | `sensor.anbang_onseubdosenseo_temperature` | humidity uses `sensor.anbang_onseubdosenseo_humidity` |
| 안방 | `switch.anbang_heater_plug` | `switch.eeokeon_nanbang_on_off_socket_1` | heater-related controls no longer use the old name |
| 안방 | `climate.anbang_heater` | none | no live climate entity confirmed |
| 안방 | `switch.anbang_goodnight_virtual` | none | no direct live equivalent confirmed |
| 안방 | `scene.anbang_lighting_100` | none | old Tuya scene ids are not live |
| 안방 | `scene.anbang_lighting_1` | none | old Tuya scene ids are not live |
| 거실 | `media_player.geosil_tv` | `media_player.43_smart_monitor_m7` | |
| 거실 | `sensor.geosil_tv_illuminance` | none | no live replacement confirmed |
| 거실 | `light.geosil_lighting` | `switch.geosilbul` | `light.geosiljomyeong`, `light.geosiljomyeong_2` also exist |
| 거실 | `light.geosil_stand_lighting` | none | no live equivalent confirmed |
| 거실 | `light.geosil_curtain_lighting` | `switch.keoteunbul` | `light.keoteunbul`, `light.keoteunbul_2` also exist |
| 거실 | `switch.geosil_curtain_lighting_plug` | `switch.keoteunbul` | safest current control-level replacement |
| 거실 | `binary_sensor.geosil_presence` | `binary_sensor.geosil_jaesilsenseo_occupancy` | |
| 거실 | `hub.geosil_zigbee_gateway` | none | no live hub entity confirmed |
| 주방 | `light.jubang_lighting` | `switch.jubangbul` | |
| 주방 | `remote.jubang_ac_hub` | none | no live remote entity confirmed |
| 주방 | `binary_sensor.jubang_presence` | `binary_sensor.jubang_jaesil_senseo_occupancy` | |
| 주방 | `binary_sensor.jubang_round_vibration` | none | no live equivalent confirmed |
| 주방 | `event.jubang_button` | none | no live event entity confirmed |
| 주방 | `switch.jubang_dryer_plug` | `switch.deuraigi` | |
| 주방 | `switch.jubang_appliance_multitap` | `switch.2jubang_jaesil_3deuraigibul_switch_2` | group is currently exposed as three split switches |
| 옷방 | `light.osbang_lighting` | `switch.osbangbul` | |
| 옷방 | `binary_sensor.osbang_presence` | `binary_sensor.osbang_jaesilsenseo_occupancy` | |
| 옷방 | `sensor.osbang_th_monitor` | `sensor.osbang_onseubdosenseo_temperature` | humidity uses `sensor.osbang_onseubdosenseo_humidity` |
| 옷방 | `humidifier.osbang_dehumidifier` | `humidifier.jeseubgi` | `fan.jeseubgi` also exists |
| 화장실 | `light.hwajangsil_lighting` | `switch.hwajangsil_bul` | `switch.hwajangsil_bul_2` also exists |
| 화장실 | `switch.hwajangsil_virtual` | `switch.hwajangsil_gasangseuwici` | current live id differs from old map |
| 화장실 | `binary_sensor.hwajangsil_presence` | `binary_sensor.hwajangsil_jaesilsenseo_occupancy` | |
| 화장실 | `binary_sensor.hwajangsil_door` | `binary_sensor.hwajangsil_doeosenseo_door` | `_2` also exists |
| 현관 | `binary_sensor.hyengwan_door` | `binary_sensor.hyeongwandoeosenseo_door` | `_2` also exists |
| 현관 | `switch.hyengwan_leave_virtual_1` | none | no direct live equivalent confirmed |
| 현관 | `switch.hyengwan_leave_virtual_2` | none | no direct live equivalent confirmed |

## Immediate Safe Use

- Replace dashboard cards only when the old entity id appears in this table with a confirmed live replacement.
- Skip any row marked `none` until that device is re-identified or intentionally retired.
- For split-device replacements, review the exact behavior before updating automations.
