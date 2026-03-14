# Jubang Standardization Plan v1

Last updated: 2026-03-03
Status: initial live-based plan

## Device Catalog

| Current Live Entity | Current Friendly Name | Canonical Device | Target Display Name | Target Entity ID | Notes |
|---|---|---|---|---|---|
| `switch.jubang_ceiling_light` | 주방 천장 조명 | 주방 천장 조명 | 주방 천장 조명 스위치 | `switch.jubang_ceiling_light` | standardized ceiling-light layer |
| `switch.jubang_hair_dryer_plug` | 주방 드라이기 플러그 | 주방 드라이기 | 주방 드라이기 플러그 | `switch.jubang_hair_dryer_plug` | standardized plug layer |
| `binary_sensor.jubang_presence` | 주방 재실 감지 | 주방 재실센서 | 주방 재실 감지 | `binary_sensor.jubang_presence` | presence state |
| `switch.jubang_presence_sensor_plug` | 주방 재실 센서 플러그 | 주방 재실센서 플러그 | 주방 재실 센서 플러그 | `switch.jubang_presence_sensor_plug` | standardized multitap outlet 2 |
| `number.jubang_presence_sensitivity` | 주방 재실 감도 | 주방 재실센서 | 주방 재실 감도 | `number.jubang_presence_sensitivity` | tuning layer |
| `number.jubang_presence_near_detection` | 주방 재실 근거리 감지 | 주방 재실센서 | 주방 재실 근거리 감지 | `number.jubang_presence_near_detection` | tuning layer |
| `number.jubang_presence_far_detection` | 주방 재실 원거리 감지 | 주방 재실센서 | 주방 재실 원거리 감지 | `number.jubang_presence_far_detection` | tuning layer |
| `number.jubang_presence` | 주방 재실 최근접 거리 | 주방 재실센서 | 주방 재실 최근접 거리 | `number.jubang_presence` | tuning layer |
| `binary_sensor.jubang_round_vibration` | 주방 원 진동센서 | 주방 원 진동센서 | 주방 원 진동 감지 | `binary_sensor.jubang_round_vibration` | separate from presence |
| `event.jubang_button` | 주방 버튼 | 주방 버튼 | 주방 버튼 | `event.jubang_button` | already clear |
| `sensor.jubang_button_battery` | 주방 버튼 배터리 | 주방 버튼 | 주방 버튼 배터리 | `sensor.jubang_button_battery` | already clear |
| `switch.jubang_line_lighting_plug` | 주방 라인 조명 플러그 | 주방 라인 조명 플러그 | 주방 라인 조명 플러그 | `switch.jubang_line_lighting_plug` | standardized multitap outlet 3 |
| `switch.jubang_multitab_unused1` | 주방 멀티탭 미사용1 | 주방 멀티탭 예비 | 주방 멀티탭 예비 1 | pending | multitap outlet 1 reserve |
| `switch.jubang_ac_remote_hub` | 주방 에어컨 IR 허브 | 주방 에어컨 IR 허브 | 주방 에어컨 IR 허브 | `switch.jubang_ac_remote_hub` | separate appliance-control layer |

## Open Questions

- `switch.jubang_multitab_unused1` should stay reserve-only, not part of the main canonical set.
- `switch.jubang_dryer_plug` is a disabled legacy duplicate on the same device and should remain non-canonical.
