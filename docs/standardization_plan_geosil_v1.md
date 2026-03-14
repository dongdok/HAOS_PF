# Geosil Standardization Plan v1

Last updated: 2026-03-03
Status: initial live-based plan

## Device Catalog

| Current Live Entity | Current Friendly Name | Canonical Device | Target Display Name | Target Entity ID | Notes |
|---|---|---|---|---|---|
| `switch.geosil_ceiling_light` | 거실 천장 조명 | 거실 천장 조명 | 거실 천장 조명 스위치 | `switch.geosil_ceiling_light` | standardized ceiling-light layer |
| `light.geosil_stand_lighting` | 거실 스탠드 조명 | 거실 스탠드 조명 | 거실 스탠드 조명 | `light.geosil_stand_lighting` | already canonical |
| `light.geosil_line_lighting` | 거실 라인 조명 | 거실 라인 조명 | 거실 라인 조명 | `light.geosil_line_lighting` | standardized line-light layer |
| `switch.geosil_line_lighting_plug` | 거실 라인 조명 전원 스위치 | 거실 라인 조명 | 거실 라인 조명 전원 스위치 | `switch.geosil_line_lighting_plug` | standardized power/control layer |
| `binary_sensor.geosil_presence` | 거실 재실 감지 | 거실 재실센서 | 거실 재실 감지 | `binary_sensor.geosil_presence` | already clear |
| `number.geosil_jaesilsenseo_sensitivity` | 거실 재실 감도 | 거실 재실센서 | 거실 재실 감도 | `number.geosil_jaesilsenseo_sensitivity` | presence tuning layer |
| `number.geosil_jaesilsenseo_near_detection` | 거실 재실 근거리 감지 | 거실 재실센서 | 거실 재실 근거리 감지 | `number.geosil_jaesilsenseo_near_detection` | presence tuning layer |
| `number.geosil_jaesilsenseo_far_detection` | 거실 재실 원거리 감지 | 거실 재실센서 | 거실 재실 원거리 감지 | `number.geosil_jaesilsenseo_far_detection` | presence tuning layer |
| `number.geosil_jaesilsenseo_closest_target_distance` | 거실 재실 최근접 거리 | 거실 재실센서 | 거실 재실 최근접 거리 | `number.geosil_jaesilsenseo_closest_target_distance` | presence tuning layer |
| `media_player.geosil_tv` | 거실 TV | 거실 TV | 거실 TV | `media_player.geosil_tv` | already canonical |
| `sensor.geosil_tv_illuminance` | 거실 TV 조도 | 거실 TV 조도센서 | 거실 TV 조도 | `sensor.geosil_tv_illuminance` | already clear |
| `sensor.geosil_tv_brightness` | 거실 TV 밝기 | 거실 TV 밝기센서 | 거실 TV 밝기 | `sensor.geosil_tv_brightness` | already clear |

## TV Model

- media player: `media_player.geosil_tv`
- ambient light metric: `sensor.geosil_tv_illuminance`
- screen brightness metric: `sensor.geosil_tv_brightness`
- TV 계층은 현재 ID와 display name 모두 canonical 상태다.

## Lighting Model

- ceiling light: `switch.geosil_ceiling_light`
- stand light: `light.geosil_stand_lighting`
- line light: `light.geosil_line_lighting`
- line-light power switch: `switch.geosil_line_lighting_plug`

## Presence Model

- presence state: `binary_sensor.geosil_presence`
- presence tuning:
  - `number.geosil_jaesilsenseo_sensitivity`
  - `number.geosil_jaesilsenseo_near_detection`
  - `number.geosil_jaesilsenseo_far_detection`
  - `number.geosil_jaesilsenseo_closest_target_distance`
