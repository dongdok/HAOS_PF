# Hwajangsil Standardization Plan v1

Last updated: 2026-03-03
Status: initial live-based plan

## Device Catalog

| Current Live Entity | Current Friendly Name | Canonical Device | Target Display Name | Target Entity ID | Notes |
|---|---|---|---|---|---|
| `switch.hwajangsil_ceiling_light` | 화장실 천장 조명 | 화장실 천장 조명 | 화장실 천장 조명 | `switch.hwajangsil_ceiling_light` | standardized ceiling-light layer |
| `switch.hwajangsil_vent_fan` | 화장실 환풍기 | 화장실 환풍기 | 화장실 환풍기 | `switch.hwajangsil_vent_fan` | standardized fan layer |
| `binary_sensor.hwajangsil_presence` | 화장실 재실 감지 | 화장실 재실센서 | 화장실 재실 감지 | `binary_sensor.hwajangsil_presence` | state layer already acceptable |
| `number.hwajangsil_jaesilsenseo_sensitivity` | 화장실 재실 감도 | 화장실 재실센서 | 화장실 재실 감도 | `number.hwajangsil_jaesilsenseo_sensitivity` | tuning layer |
| `number.hwajangsil_jaesilsenseo_near_detection` | 화장실 재실 근거리 감지 | 화장실 재실센서 | 화장실 재실 근거리 감지 | `number.hwajangsil_jaesilsenseo_near_detection` | tuning layer |
| `number.hwajangsil_jaesilsenseo_far_detection` | 화장실 재실 원거리 감지 | 화장실 재실센서 | 화장실 재실 원거리 감지 | `number.hwajangsil_jaesilsenseo_far_detection` | tuning layer |
| `number.hwajangsil_jaesilsenseo_closest_target_distance` | 화장실 재실 최근접 거리 | 화장실 재실센서 | 화장실 재실 최근접 거리 | `number.hwajangsil_jaesilsenseo_closest_target_distance` | tuning layer |
| `binary_sensor.hwajangsil_door_contact` | 화장실 도어 센서 | 화장실 도어센서 | 화장실 도어 센서 | `binary_sensor.hwajangsil_door` | `door_contact` can be simplified later |
| `sensor.hwajangsil_door_battery` | 화장실 도어 센서 배터리 | 화장실 도어센서 | 화장실 도어 센서 배터리 | `sensor.hwajangsil_door_battery` | standardized battery layer |
| `switch.hwajangsil_virtual` | 화장실 가상 스위치 | 화장실 가상 스위치 | 화장실 가상 스위치 | `switch.hwajangsil_virtual` | already acceptable |

## Direction

- Display-name normalization is complete.
- `ceiling_light` and `vent_fan` are the canonical live IDs.
- Next decide whether to simplify `door_contact`.
