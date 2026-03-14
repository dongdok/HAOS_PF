# Canonical Device Catalog v1

Last updated: 2026-03-03
Status: safe intermediate catalog before dashboard or automation edits

## Purpose

This catalog defines the canonical device names to use going forward.

It does not rename Home Assistant entities directly.
It gives one stable human-level device name per real device or logical control target.

Use this catalog together with:

- [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
- [entity_id_mapping.md](/Users/dy/Desktop/HAOS_Control/docs/entity_id_mapping.md)
- [naming_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md)

## Rules

- One canonical device name per device
- Prefer Korean display names for user-facing naming
- Keep the current live control entity recorded separately
- Do not include stale entities in the primary device list

## Canonical Devices

### 안방

| Canonical Device Name | Current Primary Live Entity | Notes |
|---|---|---|
| 안방 조명 | `switch.anbangbul` | `light.anbangjomyeong`, `light.anbangjomyeong_2` also exist |
| 안방 커튼 | `cover.curtain` | target naming should later converge to `cover.anbang_curtain` |
| 안방 가습기 | `switch.gaseubgi` | |
| 안방 전기장판 | `switch.jeongimaeteu` | |
| 안방 침대등 | `switch.1cimdaedeung_seuwici` | |
| 안방 침대 선풍기 | `switch.3cimdaeseonpunggi` | |
| 안방 책상 선풍기 | `switch.1caegsangseonpunggi` | |
| 안방 스피커 | `switch.3seupikeo` | |
| 안방 재실센서 | `binary_sensor.anbang_jaesilsenseo_occupancy` | |
| 안방 머리맡 재실센서 | `binary_sensor.meorimat_jaesilsenseo_occupancy` | |
| 안방 온습도센서 | `sensor.anbang_onseubdosenseo_temperature` | humidity is a sibling entity |
| 안방 히터 제어 | `switch.eeokeon_nanbang_on_off_socket_1` | current live naming is not yet normalized |

### 거실

| Canonical Device Name | Current Primary Live Entity | Notes |
|---|---|---|
| 거실 조명 | `switch.geosilbul` | `light.geosiljomyeong`, `light.geosiljomyeong_2` also exist |
| 거실 커튼 라인 조명 | `switch.keoteunbul` | `light.keoteunbul`, `light.keoteunbul_2` also exist |
| 거실 재실센서 | `binary_sensor.geosil_jaesilsenseo_occupancy` | |
| 거실 TV | `media_player.43_smart_monitor_m7` | |

### 주방

| Canonical Device Name | Current Primary Live Entity | Notes |
|---|---|---|
| 주방 조명 | `switch.jubangbul` | |
| 주방 드라이기 | `switch.deuraigi` | |
| 주방 재실센서 | `binary_sensor.jubang_jaesil_senseo_occupancy` | |
| 주방 멀티탭 | `switch.2jubang_jaesil_3deuraigibul_switch_2` | current live control is split into three switches |

### 옷방

| Canonical Device Name | Current Primary Live Entity | Notes |
|---|---|---|
| 옷방 조명 | `switch.osbangbul` | |
| 옷방 재실센서 | `binary_sensor.osbang_jaesilsenseo_occupancy` | |
| 옷방 온습도센서 | `sensor.osbang_onseubdosenseo_temperature` | humidity is a sibling entity |
| 옷방 제습기 | `humidifier.jeseubgi` | `fan.jeseubgi` also exists |

### 화장실

| Canonical Device Name | Current Primary Live Entity | Notes |
|---|---|---|
| 화장실 조명 | `switch.hwajangsil_bul` | `switch.hwajangsil_bul_2` also exists |
| 화장실 환풍기 | `switch.hwajangsil_hwanpunggi` | `switch.hwanpunggi` also exists |
| 화장실 재실센서 | `binary_sensor.hwajangsil_jaesilsenseo_occupancy` | |
| 화장실 도어센서 | `binary_sensor.hwajangsil_doeosenseo_door` | `_2` also exists |
| 화장실 가상스위치 | `switch.hwajangsil_gasangseuwici` | |

### 현관

| Canonical Device Name | Current Primary Live Entity | Notes |
|---|---|---|
| 현관 도어센서 | `binary_sensor.hyeongwandoeosenseo_door` | `_2` also exists |

## Safe Next Use

- Use this file when choosing which single entity should represent a device on the main dashboard
- Use this file before any bulk cleanup to avoid replacing one unstable entity with another
- If a device is missing here, do not add it to the dashboard until it is validated
