# Master Hardware Map - Live Baseline

Last verified: 2026-03-14 (live sync)
Status: current live source of truth

This document reflects the entity set that is live right now in Home Assistant.
Use this as the operational baseline for dashboards and automations.

## 안방

| Device | Type | Live Entity ID | Function |
|---|---|---|---|
| 안방 천장 조명 | Switch | `switch.anbang_ceiling_light` | Main bedroom ceiling light |
| 안방 스탠드 조명 | Light | `light.anbang_stand_lighting` | Bedroom stand light |
| 안방 커튼 | Cover | `cover.anbang_curtain` | Curtain open/close |
| 안방 가습기 플러그 | Switch | `switch.anbang_gaseubgi_peulreogeu_rokeol` | Humidifier power |
| 안방 전기장판 플러그 | Switch | `switch.anbang_jeongijangpan_peulreogeu_rokeol` | Electric blanket power |
| 안방 책상 선풍기 | Switch | `switch.anbang_desk_fan` | Desk fan power |
| 안방 책상 마이크 | Switch | `switch.anbang_desk_mic` | Desk mic power |
| 안방 책상 스피커 | Switch | `switch.anbang_desk_speaker` | Desk speaker power |
| 안방 침대 조명 | Switch | `switch.anbang_bedside_light` | Bedside light |
| 안방 침대 선풍기 | Switch | `switch.anbang_bedside_fan` | Bedside fan |
| 안방 재실센서 (MQTT main) | Binary Sensor | `binary_sensor.anbang_presence` | Bedroom main presence |
| 안방 침대 재실 스위치 | Switch | `switch.anbang_bedside_presence_switch` | Bedside presence helper |
| 안방 침대 재실센서 (LocalTuya sub) | Binary Sensor | `binary_sensor.anbang_bedside_presence` | Bedside presence sensor (time-scoped use) |
| 안방 온도 | Sensor | `sensor.anbang_temperature` | Temperature |
| 안방 습도 | Sensor | `sensor.anbang_humidity` | Humidity |
| 안방 온습도센서 배터리 | Sensor | `sensor.anbang_th_monitor_battery` | Battery |
| 안방 히터 | Climate | `climate.anbang_hiteo` | Heater control |
| 안방 히터 플러그 | Switch | `switch.anbang_hiteo_peulreogeu` | Heater power plug (canonical) |
| 안방 굿나잇 가상 스위치 | Input Boolean | `input_boolean.gasang_anbang_gusnais` | Goodnight helper |

## 거실

| Device | Type | Live Entity ID | Function |
|---|---|---|---|
| 거실 TV | Media Player | `media_player.geosil_tv_smartthings` | Main TV/monitor (SmartThings integration) |
| 거실 TV (로컬 samsungtv, 비활성) | Media Player | `media_player.geosil_tv` | Local entity only, not used in active automations/dashboard |
| 거실 재실 감지 | Binary Sensor | `binary_sensor.geosil_presence` | Presence |
| 거실 TV 조도 | Sensor | `sensor.geosil_tv_illuminance` | TV area illuminance |
| 거실 TV 밝기 | Sensor | `sensor.geosil_tv_brightness` | TV brightness metric |
| 거실 천장 조명 | Switch | `switch.geosil_ceiling_light` | Main living room ceiling light |
| 거실 스탠드 조명 | Light | `light.geosil_stand_lighting` | Stand light |
| 거실 라인 조명 | Light | `light.geosil_keoteun_rain_jomyeong_rokeol` | Curtain line light |
| 거실 라인 조명 전원 스위치 | Switch | `switch.geosil_line_lighting_plug` | Power/control switch |

## 주방

| Device | Type | Live Entity ID | Function |
|---|---|---|---|
| 주방 천장 조명 | Switch | `switch.jubang_ceiling_light` | Main kitchen ceiling light |
| 주방 드라이기 플러그 | Switch | `switch.jubang_deuraigi_peulreogeu_rokeol` | Hair dryer power |
| 주방 재실 감지 | Binary Sensor | `binary_sensor.jubang_presence` | Presence |
| 주방 재실 센서 플러그 | Switch | `switch.jubang_presence_sensor_plug` | Multitap outlet 2 for kitchen presence sensor |
| 주방 멀티탭 예비 1 | Switch | `switch.jubang_multitab_unused1` | Spare/unused outlet |
| 주방 에어컨 IR 허브 | Switch | `switch.jubang_ac_remote_hub` | AC IR hub |
| 주방 버튼 배터리 | Sensor | `sensor.0xa4c138911b3d4b4b_battery` | Battery |
| 주방 원 진동센서 | Binary Sensor | `binary_sensor.jubang_round_vibration` | Vibration sensor |
| 주방 라인 조명 플러그 | Switch | `switch.jubang_line_lighting_plug` | Multitap outlet 3 for kitchen line lighting |

## 옷방

| Device | Type | Live Entity ID | Function |
|---|---|---|---|
| 옷방 천장 조명 | Switch | `switch.osbang_ceiling_light` | Main clothing room ceiling light |
| 옷방 재실 감지 | Binary Sensor | `binary_sensor.osbang_presence` | Presence |
| 옷방 온도 (active/local) | Sensor | `sensor.osbang_ondo_rokeol` | Temperature |
| 옷방 습도 (active/local) | Sensor | `sensor.osbang_seubdo_rokeol` | Humidity |
| 옷방 온도 (legacy/smartthings) | Sensor | `sensor.osbang_temperature` | Temperature (currently unavailable) |
| 옷방 습도 (legacy/smartthings) | Sensor | `sensor.osbang_humidity` | Humidity (currently unavailable) |
| 옷방 온습도센서 배터리 (legacy/smartthings) | Sensor | `sensor.osbang_th_monitor_battery` | Battery (currently unavailable) |
| 옷방 제습기 | Humidifier | `humidifier.osbang_jeseubgi_rokeol_naebuseubdo` | Dehumidifier main control |
| 옷방 제습기 전원(내부용) | Switch | `switch.osbang_jeseubgi_jeonweon_rokeol` | Dehumidifier internal power/control layer (hidden in UI, not user-facing target) |

## 화장실

| Device | Type | Live Entity ID | Function |
|---|---|---|---|
| 화장실 천장 조명 | Switch | `switch.hwajangsil_ceiling_light` | Main bathroom ceiling light |
| 화장실 환풍기 | Switch | `switch.hwajangsil_vent_fan` | Ventilation fan |
| 화장실 재실 감지 | Binary Sensor | `binary_sensor.hwajangsil_presence` | Presence |
| 화장실 도어 센서 | Binary Sensor | `binary_sensor.hwajangsil_door_contact` | Door open/close |
| 화장실 도어 센서 배터리 | Sensor | `sensor.hwajangsil_door_battery` | Battery |
| 화장실 가상 스위치 | Input Boolean | `input_boolean.gasang_hwajangsil` | Helper switch |

## 현관

| Device | Type | Live Entity ID | Function |
|---|---|---|---|
| 현관 도어 센서 | Binary Sensor | `binary_sensor.hyeongwan_door` | Door open/close |
| 현관 도어 센서 배터리 | Sensor | `sensor.hyeongwan_door_battery` | Battery |
| 현관 도어 변조 감지 | Binary Sensor | `binary_sensor.hyeongwan_door_tamper` | Door tamper sensor |
| 현관 도어 가상 스위치 | Input Boolean | `input_boolean.gasang_hyeongwan_doeo` | Door helper |
| 현관 외출 가상 스위치 1 | Input Boolean | `input_boolean.gasang_hyeongwan_oecul_1` | Outing helper |
| 현관 외출 가상 스위치 2 | Input Boolean | `input_boolean.gasang_hyeongwan_oecul_2` | Outing helper 2 |

## Operating Rule

- Treat this file as the operational truth source
- If Home Assistant live entities change again, update this file first
- Update dashboards and automations only after this file is refreshed

## Live Sync Notes (2026-03-10)

- `unavailable` 운영대상 6 entities are tracked in
  [ha_entity_operations_2026-03-10.md](/Users/dy/Desktop/HAOS_Control/docs/ha_entity_operations_2026-03-10.md).
- Disabled by user:
  - `switch.anbang_stand_lighting_1`
  - `switch.anbang_stand_lighting_100`
  - `switch.anbang_hiteo_peulreogeu_2`
- Hidden by user:
  - `switch.hyeongwan_door_virtual_spare`
- Active in-use (hidden 해제):
  - `switch.anbang_hiteo_peulreogeu`
- Canonical switch alignment applied:
  - `[출입] 현관 도어 연동 가상스위치 ON/OFF` automation now controls
    `input_boolean.gasang_hyeongwan_doeo`.
- Presence role alignment:
  - `binary_sensor.anbang_presence` is the MQTT main presence sensor.
  - `binary_sensor.anbang_bedside_presence` is a LocalTuya sub sensor used in time-scoped routines.
