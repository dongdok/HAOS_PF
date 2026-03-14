# Hyeongwan Standardization Plan v1

Last updated: 2026-03-03
Status: initial live-based plan

## Device Catalog

| Current Live Entity | Current Friendly Name | Canonical Device | Target Display Name | Target Entity ID | Notes |
|---|---|---|---|---|---|
| `binary_sensor.hyeongwan_door` | 현관 도어 센서 | 현관 도어센서 | 현관 도어 센서 | `binary_sensor.hyeongwan_door` | fix `hyengwan`/`hyeongwan` inconsistency |
| `sensor.hyeongwan_door_battery` | 현관 도어 센서 배터리 | 현관 도어센서 | 현관 도어 센서 배터리 | `sensor.hyeongwan_door_battery` | battery layer |
| `binary_sensor.hyeongwan_door_tamper` | 현관 도어 변조 감지 | 현관 도어센서 | 현관 도어 변조 감지 | `binary_sensor.hyeongwan_door_tamper` | tamper layer already acceptable |
| `switch.hyeongwan_outing_virtual_1` | 현관 외출 가상 스위치 1 | 현관 외출 가상 스위치 | 현관 외출 가상 스위치 1 | `switch.hyeongwan_outing_virtual_1` | canonical virtual-switch layer |
| `switch.hyeongwan_outing_virtual_2` | 현관 외출 가상 스위치 2 | 현관 외출 가상 스위치 | 현관 외출 가상 스위치 2 | `switch.hyeongwan_outing_virtual_2` | canonical virtual-switch layer |

## Direction

- First normalize display names.
- Then normalize `hyengwan` to `hyeongwan`.
- Convert outing helper plugs to explicit `virtual` IDs because they are not physical plugs.
