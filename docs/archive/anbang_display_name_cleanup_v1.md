# Anbang Display Name Cleanup v1

Last updated: 2026-03-03
Status: display-name-only proposal

## Goal

Normalize bedroom display names without changing live entity ids yet.

This is the safest first step because:

- dashboards become easier to read
- automations keep working
- entity id migration can be handled later

## Proposed Renames

| Live Entity ID | Current Friendly Name | Proposed Display Name | Reason |
|---|---|---|---|
| `switch.anbang_ceiling_light` | 안방 천장 조명 | 안방 천장 조명 | standardized ceiling-light naming |
| `light.anbang_stand_lighting` | 안방 스탠드 조명 | 안방 스탠드 조명 | keep as is |
| `cover.anbang_curtain` | 안방 커튼 | 안방 커튼 | keep as is |
| `switch.anbang_humidifier` | 안방 가습기 플러그 | 안방 가습기 플러그 | keep as is |
| `sensor.anbang_humidifier_current` | 안방 가습기 플러그 전류 | 안방 가습기 전류 | remove unnecessary `플러그` in metric entities |
| `sensor.anbang_humidifier_power` | 안방 가습기 플러그 전력 | 안방 가습기 전력 | same rule |
| `sensor.anbang_humidifier_voltage` | 안방 가습기 플러그 전압 | 안방 가습기 전압 | same rule |
| `sensor.anbang_humidifier_total_energy` | 안방 가습기 플러그 총 에너지 | 안방 가습기 총 에너지 | same rule |
| `switch.anbang_electric_blanket` | 안방 전기장판 플러그 | 안방 전기장판 플러그 | keep as is |
| `sensor.anbang_electric_blanket_current` | 안방 전기장판 플러그 전류 | 안방 전기장판 전류 | remove unnecessary `플러그` in metric entities |
| `sensor.anbang_electric_blanket_power` | 안방 전기장판 플러그 전력 | 안방 전기장판 전력 | same rule |
| `sensor.anbang_electric_blanket_voltage` | 안방 전기장판 플러그 전압 | 안방 전기장판 전압 | same rule |
| `sensor.anbang_electric_blanket_total_energy` | 안방 전기장판 플러그 총 에너지 | 안방 전기장판 총 에너지 | same rule |
| `switch.anbang_desk_fan` | 안방 책상 선풍기 | 안방 책상 선풍기 | keep as is |
| `switch.anbang_desk_mic` | 안방 책상 마이크 | 안방 책상 마이크 | keep as is |
| `switch.anbang_desk_speaker` | 안방 책상 스피커 | 안방 책상 스피커 | keep as is |
| `switch.anbang_bedside_light` | 안방 침대불 | 안방 침대 조명 | align with desk/bed location naming |
| `switch.anbang_bedside_fan` | 안방 침대 선풍기 | 안방 침대 선풍기 | keep as is |
| `switch.anbang_bedside_presence_switch` | 안방 머리맡 재실 스위치 | 안방 침대 재실 스위치 | align with desk/bed location naming |
| `binary_sensor.anbang_presence` | 안방 재실센서 | 안방 재실 감지 | user-facing wording is clearer |
| `binary_sensor.anbang_bedside_presence` | 안방 원 진동센서 | 안방 침대 재실 감지 | align with desk/bed location naming |
| `sensor.anbang_temperature` | 안방 온도 | 안방 온도 | standardized |
| `sensor.anbang_humidity` | 안방 습도 | 안방 습도 | standardized |
| `sensor.anbang_th_monitor_battery` | 안방 온습도센서 배터리 | 안방 온습도센서 배터리 | standardized |
| `climate.anbang_heater` | 안방 히터 | 안방 히터 | keep as is |
| `switch.anbang_heater_plug` | 안방 히터 플러그 | 안방 히터 플러그 | standardized |
| `sensor.anbang_heater_current` | 안방 히터 전류 | 안방 히터 전류 | standardized |
| `sensor.anbang_heater_power` | 안방 히터 전력 | 안방 히터 전력 | standardized |
| `sensor.anbang_heater_voltage` | 안방 히터 전압 | 안방 히터 전압 | standardized |
| `sensor.anbang_heater_total_energy` | 안방 히터 총 에너지 | 안방 히터 총 에너지 | standardized |
| `switch.anbang_bedtime_virtual` | 안방 취침 가상 스위치 | 안방 취침 가상 스위치 | standardized |
| `switch.anbang_goodnight_virtual` | 안방 굿나잇 가상 스위치 | 안방 굿나잇 가상 스위치 | standardized |
| `scene.anbangjomyeong_1peo` | 안방 조명 1퍼 | 안방 스탠드 조명 1% | stand-light preset, not main-light preset |
| `scene.anbangjomyeong_100peo` | 안방 조명 100퍼 | 안방 스탠드 조명 100% | stand-light preset, not main-light preset |

## Recommended First Batch

Apply these first because they improve readability with low ambiguity:

- `switch.anbang_ceiling_light` -> `안방 천장 조명`
- `binary_sensor.anbang_presence` -> `안방 재실 감지`
- `binary_sensor.anbang_bedside_presence` -> `안방 침대 재실 감지`
- `scene.anbangjomyeong_1peo` -> `안방 스탠드 조명 1%`
- `scene.anbangjomyeong_100peo` -> `안방 스탠드 조명 100%`
- metric entities that remove `플러그` from sensor names

## Not In Scope Yet

- area id changes
