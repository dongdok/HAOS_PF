# Anbang Standardization Plan v1

Last updated: 2026-03-03
Status: proposed migration plan based on current live entities

## Goal

This document standardizes the bedroom (`anbang`) first.

It keeps the current live system stable while defining:

- current live entity
- canonical device name
- target entity display name
- target entity id

## Naming Rules Used

- Device name: `[영역] [기기명]`
- Entity display name: `[영역] [기기명] [기능/상세]`
- Target entity id: `domain.area_device_detail`

## Device Catalog

| Current Live Entity | Current Friendly Name | Canonical Device | Target Display Name | Target Entity ID | Notes |
|---|---|---|---|---|---|
| `switch.anbang_ceiling_light` | 안방 천장 조명 | 안방 천장 조명 | 안방 천장 조명 스위치 | `switch.anbang_ceiling_light` | standardized ceiling-light entity |
| `light.anbang_stand_lighting` | 안방 스탠드 조명 | 안방 스탠드 조명 | 안방 스탠드 조명 | `light.anbang_stand_lighting` | already close to target |
| `cover.anbang_curtain` | 안방 커튼 | 안방 커튼 | 안방 커튼 | `cover.anbang_curtain` | already canonical |
| `switch.anbang_humidifier` | 안방 가습기 플러그 | 안방 가습기 | 안방 가습기 플러그 | `switch.anbang_humidifier_plug` | |
| `sensor.anbang_humidifier_current` | 안방 가습기 플러그 전류 | 안방 가습기 | 안방 가습기 전류 | `sensor.anbang_humidifier_current` | |
| `sensor.anbang_humidifier_power` | 안방 가습기 플러그 전력 | 안방 가습기 | 안방 가습기 전력 | `sensor.anbang_humidifier_power` | |
| `sensor.anbang_humidifier_voltage` | 안방 가습기 플러그 전압 | 안방 가습기 | 안방 가습기 전압 | `sensor.anbang_humidifier_voltage` | |
| `sensor.anbang_humidifier_total_energy` | 안방 가습기 플러그 총 에너지 | 안방 가습기 | 안방 가습기 총 에너지 | `sensor.anbang_humidifier_total_energy` | |
| `switch.anbang_electric_blanket` | 안방 전기장판 플러그 | 안방 전기장판 | 안방 전기장판 플러그 | `switch.anbang_electric_blanket_plug` | |
| `sensor.anbang_electric_blanket_current` | 안방 전기장판 플러그 전류 | 안방 전기장판 | 안방 전기장판 전류 | `sensor.anbang_electric_blanket_current` | |
| `sensor.anbang_electric_blanket_power` | 안방 전기장판 플러그 전력 | 안방 전기장판 | 안방 전기장판 전력 | `sensor.anbang_electric_blanket_power` | |
| `sensor.anbang_electric_blanket_voltage` | 안방 전기장판 플러그 전압 | 안방 전기장판 | 안방 전기장판 전압 | `sensor.anbang_electric_blanket_voltage` | |
| `sensor.anbang_electric_blanket_total_energy` | 안방 전기장판 플러그 총 에너지 | 안방 전기장판 | 안방 전기장판 총 에너지 | `sensor.anbang_electric_blanket_total_energy` | |
| `switch.anbang_desk_fan` | 안방 책상 선풍기 | 안방 책상 멀티탭 | 안방 책상 선풍기 | `switch.anbang_desk_fan` | device is the multitap, entity is outlet 1 |
| `switch.anbang_desk_mic` | 안방 책상 마이크 | 안방 책상 멀티탭 | 안방 책상 마이크 | `switch.anbang_desk_mic` | entity is outlet 2 |
| `switch.anbang_desk_speaker` | 안방 책상 스피커 | 안방 책상 멀티탭 | 안방 책상 스피커 | `switch.anbang_desk_speaker` | entity is outlet 3 |
| `switch.anbang_bedside_light` | 안방 침대 조명 | 안방 침대 멀티탭 | 안방 침대 조명 | `switch.anbang_bedside_light` | |
| `switch.anbang_bedside_fan` | 안방 침대 선풍기 | 안방 침대 멀티탭 | 안방 침대 선풍기 | `switch.anbang_bedside_fan` | |
| `switch.anbang_bedside_presence_switch` | 안방 침대 재실 스위치 | 안방 침대 재실센서 | 안방 침대 재실 스위치 | `switch.anbang_bedside_presence_switch` | helper/control entity |
| `binary_sensor.anbang_presence` | 안방 재실센서 | 안방 재실센서 | 안방 재실 감지 | `binary_sensor.anbang_presence` | |
| `binary_sensor.anbang_bedside_presence` | 안방 침대 재실 감지 | 안방 침대 재실센서 | 안방 침대 재실 감지 | `binary_sensor.anbang_bedside_presence` | control/sensor pair confirmed |
| `sensor.anbang_temperature` | 안방 온도 | 안방 온습도센서 | 안방 온도 | `sensor.anbang_temperature` | standardized |
| `sensor.anbang_humidity` | 안방 습도 | 안방 온습도센서 | 안방 습도 | `sensor.anbang_humidity` | standardized |
| `sensor.anbang_th_monitor_battery` | 안방 온습도센서 배터리 | 안방 온습도센서 | 안방 온습도센서 배터리 | `sensor.anbang_th_monitor_battery` | standardized |
| `climate.anbang_heater` | 안방 히터 | 안방 히터 | 안방 히터 | `climate.anbang_heater` | already canonical |
| `switch.anbang_heater_plug` | 안방 히터 플러그 | 안방 히터 | 안방 히터 플러그 | `switch.anbang_heater_plug` | standardized |
| `sensor.anbang_heater_current` | 안방 히터 전류 | 안방 히터 | 안방 히터 전류 | `sensor.anbang_heater_current` | standardized |
| `sensor.anbang_heater_power` | 안방 히터 전력 | 안방 히터 | 안방 히터 전력 | `sensor.anbang_heater_power` | standardized |
| `sensor.anbang_heater_voltage` | 안방 히터 전압 | 안방 히터 | 안방 히터 전압 | `sensor.anbang_heater_voltage` | standardized |
| `sensor.anbang_heater_total_energy` | 안방 히터 총 에너지 | 안방 히터 | 안방 히터 총 에너지 | `sensor.anbang_heater_total_energy` | standardized |
| `switch.anbang_bedtime_virtual` | 안방 취침 가상 스위치 | 안방 취침 가상스위치 | 안방 취침 가상 스위치 | `switch.anbang_bedtime_virtual` | standardized helper |
| `switch.anbang_goodnight_virtual` | 안방 굿나잇 가상 스위치 | 안방 굿나잇 가상스위치 | 안방 굿나잇 가상 스위치 | `switch.anbang_goodnight_virtual` | standardized helper |
| `switch.anbang_stand_lighting_1` | 안방 스탠드 조명 1% 보조 스위치 | 안방 스탠드 조명 프리셋 | 안방 스탠드 조명 1% 보조 스위치 | `switch.anbang_stand_lighting_1` | base preset control layer |
| `switch.anbang_stand_lighting_100` | 안방 스탠드 조명 100% 보조 스위치 | 안방 스탠드 조명 프리셋 | 안방 스탠드 조명 100% 보조 스위치 | `switch.anbang_stand_lighting_100` | base preset control layer |
| `scene.anbang_stand_lighting_1` | 안방 스탠드 조명 1% | 안방 스탠드 조명 | 안방 스탠드 조명 1% | `scene.anbang_stand_lighting_1` | convenience preset layer |
| `scene.anbang_stand_lighting_100` | 안방 스탠드 조명 100% | 안방 스탠드 조명 | 안방 스탠드 조명 100% | `scene.anbang_stand_lighting_100` | convenience preset layer |

## Priority

### Safe To Standardize First

- display names only
- documentation names
- dashboard labels where they do not depend on entity id changes

### Rename Later

- sensor ids with verbose transliterated suffixes
- scene ids if automation references are verified

## Open Questions

- Ceiling light should remain distinct from stand light and preset layers.
- Bedside presence pair is now confirmed as sensor + switch, so this no longer needs vibration-based interpretation.
- Should `안방 취침 가상 플러그` and `안방 굿나잇 가상 플러그` stay as plug-style names or move to virtual switch naming?

## Recommended Migration Order

1. lock current live state in documentation
2. normalize bedroom display names
3. review heater-related `jubang_*` ids
4. review scene naming and references
5. ceiling-light normalization is complete for bedroom
