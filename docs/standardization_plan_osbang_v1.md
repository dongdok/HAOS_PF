# Osbang Standardization Plan v1

Last updated: 2026-03-03
Status: initial live-based plan

## Device Catalog

| Current Live Entity | Current Friendly Name | Canonical Device | Target Display Name | Target Entity ID | Notes |
|---|---|---|---|---|---|
| `switch.osbang_ceiling_light` | 옷방 천장 조명 | 옷방 천장 조명 | 옷방 천장 조명 스위치 | `switch.osbang_ceiling_light` | standardized ceiling-light layer |
| `binary_sensor.osbang_presence` | 옷방 재실 감지 | 옷방 재실센서 | 옷방 재실 감지 | `binary_sensor.osbang_presence` | presence state |
| `number.osbang_presence` | 옷방 재실 감도 | 옷방 재실센서 | 옷방 재실 감도 | `number.osbang_presence` | tuning layer |
| `number.osbang_jaesilsenseo_near_detection` | 옷방 재실 근거리 감지 | 옷방 재실센서 | 옷방 재실 근거리 감지 | `number.osbang_jaesilsenseo_near_detection` | tuning layer |
| `number.osbang_jaesilsenseo_far_detection` | 옷방 재실 원거리 감지 | 옷방 재실센서 | 옷방 재실 원거리 감지 | `number.osbang_jaesilsenseo_far_detection` | tuning layer |
| `number.osbang_jaesilsenseo_closest_target_distance` | 옷방 재실 최근접 거리 | 옷방 재실센서 | 옷방 재실 최근접 거리 | `number.osbang_jaesilsenseo_closest_target_distance` | tuning layer |
| `sensor.osbang_temperature` | 옷방 온도 | 옷방 온습도센서 | 옷방 온도 | `sensor.osbang_temperature` | standardized |
| `sensor.osbang_humidity` | 옷방 습도 | 옷방 온습도센서 | 옷방 습도 | `sensor.osbang_humidity` | standardized |
| `sensor.osbang_th_monitor_battery` | 옷방 온습도센서 배터리 | 옷방 온습도센서 | 옷방 온습도센서 배터리 | `sensor.osbang_th_monitor_battery` | already acceptable |
| `humidifier.osbang_dehumidifier` | 옷방 제습기 | 옷방 제습기 | 옷방 제습기 | `humidifier.osbang_dehumidifier` | main device layer |
| `fan.osbang_dehumidifier` | 옷방 제습기 | 옷방 제습기 | 옷방 제습기 풍량 제어 | `fan.osbang_dehumidifier` | secondary control layer |
