# Current Operating Map

Last verified: 2026-03-14 (live sync)
Source of truth: live Home Assistant current entity states

## Purpose

This document is the safe working baseline for further cleanup.
It reflects what is currently live in Home Assistant, not the target naming plan.

## Area Status

- Active live ids are currently aligned around: `geosil`, `jubang`, `anbang`, `osbang`, `hwajangsil`, `hyeongwan`
- The currently working operational baseline is the live entity set, not the previous rescue/renaming attempts
- Bedroom is now operationally using the `anbang` live id family again

## Room Baseline

### 거실

- Main ceiling light switch: `switch.geosil_ceiling_light`
- Stand light: `light.geosil_stand_lighting`
- Line light: `light.geosil_keoteun_rain_jomyeong_rokeol`
- Line-light power switch: `switch.geosil_line_lighting_plug`
- Presence sensor: `binary_sensor.geosil_presence`
- TV (local Samsung integration): `media_player.geosil_tv`
  - backup (disabled): `media_player.geosil_tv_smartthings` (`disabled_by=user`)

### 주방

- Main ceiling light switch: `switch.jubang_ceiling_light`
- Presence sensor: `binary_sensor.jubang_presence`
- Presence sensor plug: `switch.jubang_presence_sensor_plug`
- Hair dryer plug: `switch.jubang_deuraigi_peulreogeu_rokeol`
- Line-light plug: `switch.jubang_line_lighting_plug`
- AC IR hub: `switch.jubang_ac_remote_hub`

### 안방

- Main ceiling light switch: `switch.anbang_ceiling_light`
- Stand light: `light.anbang_stand_lighting`
- Presence sensor (MQTT main): `binary_sensor.anbang_presence`
- Bedside presence (LocalTuya sub, time-scoped use): `binary_sensor.anbang_bedside_presence`
- Temperature sensor: `sensor.anbang_temperature`
- Humidity sensor: `sensor.anbang_humidity`
- TH monitor battery: `sensor.anbang_th_monitor_battery`
- Curtain: `cover.anbang_curtain`
- Humidifier plug: `switch.anbang_gaseubgi_peulreogeu_rokeol`
- Electric blanket plug: `switch.anbang_jeongijangpan_peulreogeu_rokeol`
- Heater: `climate.anbang_hiteo`
- Heater plug: `switch.anbang_hiteo_peulreogeu`

### 옷방

- Main ceiling light switch: `switch.osbang_ceiling_light`
- Presence sensor: `binary_sensor.osbang_presence`
- Temperature sensor (active/local): `sensor.osbang_ondo_rokeol`
- Humidity sensor (active/local): `sensor.osbang_seubdo_rokeol`
- Temperature sensor (legacy/smartthings): `sensor.osbang_temperature`
- Humidity sensor (legacy/smartthings): `sensor.osbang_humidity`
- Dehumidifier: `humidifier.osbang_jeseubgi_rokeol_naebuseubdo`
- Dehumidifier power switch (internal/control-layer): `switch.osbang_jeseubgi_jeonweon_rokeol`
  - 운영 원칙: 사용자 제어/추천/자동화 기준은 `humidifier.osbang_jeseubgi_rokeol_naebuseubdo` 단일 사용
  - 운영 상태: 엔티티 이름 `옷방 제습기 전원(내부용)`, UI 숨김(`hidden_by=user`)
  - 옷방 제습 ON/OFF 자동화 트리거 습도 센서는 `sensor.osbang_seubdo_rokeol` 사용

### 화장실

- Main ceiling light switch: `switch.hwajangsil_ceiling_light`
- Vent fan switch: `switch.hwajangsil_vent_fan`
- Presence sensor: `binary_sensor.hwajangsil_presence`
- Door sensor: `binary_sensor.hwajangsil_door_contact`
- Door battery sensor: `sensor.hwajangsil_door_battery`
- Virtual helper: `input_boolean.gasang_hwajangsil`

### 현관

- Door sensor: `binary_sensor.hyeongwan_door`
- Door battery sensor: `sensor.hyeongwan_door_battery`
- Door virtual helper: `input_boolean.gasang_hyeongwan_doeo`
- Outing virtual helper 1: `input_boolean.gasang_hyeongwan_oecul_1`
- Outing virtual helper 2: `input_boolean.gasang_hyeongwan_oecul_2`
- Door tamper sensor: `binary_sensor.hyeongwan_door_tamper`

## Live Availability Snapshot (2026-03-10)

`unavailable` 운영대상 6개:

- `switch.geosil_line_lighting_plug`
- `sensor.osbang_temperature`
- `sensor.osbang_humidity`
- `sensor.osbang_th_monitor_battery`
- `sensor.anbang_cimdae_jaesil_sangtae_rokeol`
- `sensor.anbang_cimdae_jodo_rokeol`

비활성화(사용 안 함):

- `switch.anbang_stand_lighting_1`
- `switch.anbang_stand_lighting_100`
- `switch.anbang_hiteo_peulreogeu_2`

숨김 처리(운영 혼잡도 감소, 기능 유지):

- `switch.hyeongwan_door_virtual_spare`

운영 유지(실사용):

- `switch.anbang_hiteo_peulreogeu` (안방 히터 플러그)

## Safety Rules

- Do not use stale rescue mappings as the live source of truth.
- Before changing dashboards or automations, validate against live `states`.
- Use [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md) as the current operational baseline.
