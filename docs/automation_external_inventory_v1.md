# External Automation Inventory v1

Last updated: 2026-03-08
Status: collecting source automations from SmartThings/Tuya for HA migration

## Purpose

This document is the running inventory of existing external automations.

It is used as the source behavior record before creating Home Assistant automations.

## Canonical Mapping Rule

- Keep original app behavior exactly as captured first.
- Map each source device to canonical live entity IDs from:
  - `docs/current_operating_map.md`
  - `docs/master_hardware_map_live.md`
- If source label and canonical ID mismatch, keep both and mark as mapping assumption.

## Entry 001

- Source app routine names:
  - `옷방 In`
  - `옷방Out`
- Category: `조명`
- Room: `옷방`
- Intent: presence-based light on/off

### 001-A: 옷방 In

- Source trigger:
  - Device label: `옷방 재실센서`
  - Condition mode: `모든 조건이 충족되었을 경우`
  - Condition: `Induction state = move&present`
- Source action:
  - Device label: `옷방불`
  - Action: `Switch 1 -> ON`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity: `binary_sensor.osbang_presence`
- Target entity: `switch.osbang_ceiling_light`

### 001-B: 옷방 Out

- Source trigger:
  - Device label: `옷방 재실센서`
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `Induction state = None`
- Source action:
  - Device label: `옷방불`
  - Action: `Switch 1 -> OFF`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity: `binary_sensor.osbang_presence`
- Target entity: `switch.osbang_ceiling_light`

## Entry 002

- Source app routine names:
  - `화장실in`
  - `화장실 out`
- Category: `조명`, `환풍`
- Room: `화장실`
- Intent: bathroom presence + door condition based light/fan on, no-presence off

### 002-A: 화장실in

- Source trigger:
  - Device label: `화장실 재실센서`
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition 1: `Induction state = move&present`
  - Condition 2: `Door Sensor = ON`
- Source action:
  - Device label: `화장실스위치`
  - Action 1: `화장실 불 -> 켜다`
  - Action 2: `환풍기 -> 켜다`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (presence): `binary_sensor.hwajangsil_presence`
- Trigger/condition entity (door): `binary_sensor.hwajangsil_door_contact`
- Target entity (light): `switch.hwajangsil_ceiling_light`
- Target entity (vent fan): `switch.hwajangsil_vent_fan`

### 002-B: 화장실 out

- Source trigger:
  - Device label: `화장실 재실센서`
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `Induction state = None`
- Source action:
  - Device label: `화장실스위치`
  - Action 1: `화장실 불 -> 폐쇄`
  - Action 2: `환풍기 -> 폐쇄`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity: `binary_sensor.hwajangsil_presence`
- Target entity (light): `switch.hwajangsil_ceiling_light`
- Target entity (vent fan): `switch.hwajangsil_vent_fan`

## Entry 003

- Source app routine name:
  - `밤에 거실off`
- Category: `조명`
- Room: `거실` (with `안방` presence condition)
- Intent: late-night living room lighting off when living room is empty and bedroom is occupied

### 003-A: 밤에 거실off

- Source trigger:
  - Condition mode: `모든 조건이 충족되었을 경우`
  - Condition 1: `거실 재실센서 / Induction state = None`
  - Condition 2: `안방 재실센서 / Induction state = move&present`
- Source action:
  - Device label: `거실 커튼불`
  - Action 1: `Switch 1 -> OFF`
  - Device label: `거실 스탠드 조명`
  - Action 2: `ON/OFF -> OFF`
- Validity range: `오후 11:00 - 다음날 오전 06:00`

Canonical mapping (assumed from live baseline):

- Condition entity (living room presence): `binary_sensor.geosil_presence`
- Condition entity (bedroom presence): `binary_sensor.anbang_presence`
- Target entity (curtain line lighting switch): `switch.geosil_line_lighting_plug`
- Target entity (stand light): `light.geosil_stand_lighting`

## Entry 004

- Source app routine name:
  - `침대 누우면 잘준비모드`
- Category: `취침`, `조명`, `공조`
- Room: `안방`
- Intent: bed presence detected -> bedtime preparation actions

### 004-A: 침대 누우면 잘준비모드

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `안방 침대 재실 센서 / Presence_state = Presence`
- Source action:
  - Device label: `안방 전기매트`
  - Action 1: `Switch 1 -> ON`
  - Device label: `안방 커튼`
  - Action 2: `Control -> Close`
  - Device label: `안방 침대불1/머리맡재실2/침대선풍기3`
  - Action 3: `1침대불 -> ON`
  - Action 4: `3침대선풍기 -> ON`
  - Scene label: `안방조명 1퍼`
  - Action 5: `탭하여 실행`
  - Device label: `안방불`
  - Action 6: `Switch 1 -> OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (bedside presence): `binary_sensor.anbang_bedside_presence`
- Target entity (electric blanket): `switch.anbang_electric_blanket`
- Target entity (curtain): `cover.anbang_curtain`
- Target entity (bedside light): `switch.anbang_bedside_light`
- Target entity (bedside fan): `switch.anbang_bedside_fan`
- Target entity (stand-light 1% scene): `scene.anbang_stand_lighting_1`
- Target entity (main ceiling light off): `switch.anbang_ceiling_light`

## Entry 005

- Source app routine name:
  - `안방 침대 재실 On`
- Category: `취침`, `스케줄`
- Room: `안방`
- Intent: at 23:00 daily, turn on bedside-presence helper channel

### 005-A: 안방 침대 재실 On

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `스케줄 = 매일 오후 11:00`
- Source action:
  - Device label: `안방 침대불1/머리맡재실2/침대선풍기3`
  - Action: `2머리맡재실 -> ON`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger type: daily time schedule (`23:00`)
- Target entity (bedside presence switch/helper): `switch.anbang_bedside_presence_switch`

## Entry 006

- Source app routine name:
  - `굿나잇시 안방 침대 재실Off`
- Category: `취침`, `가상스위치`
- Room: `안방`
- Intent: when bedside light turns off, disable bedside-presence helper and goodnight virtual switch

### 006-A: 굿나잇시 안방 침대 재실Off

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `1침대불 = OFF`
- Source action:
  - Device label: `안방 침대불1/머리맡재실2/침대선풍기3`
  - Action 1: `2머리맡재실 -> OFF`
  - Device label: `굿나잇 가상스위치`
  - Action 2: `Switch 1 -> OFF`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (bedside light): `switch.anbang_bedside_light`
- Target entity (bedside presence switch/helper): `switch.anbang_bedside_presence_switch`
- Target entity (goodnight virtual): `switch.anbang_goodnight_virtual`

## Entry 007

- Source app routine name:
  - `칼집문 열 때 주방등 On`
- Category: `조명`, `센서이벤트`
- Room: `주방`
- Intent: when kitchen round vibration sensor detects vibration/tilt, turn on kitchen light (only during kitchen presence-valid window)

### 007-A: 칼집문 열 때 주방등 On

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition 1: `Vibration State = Vibration detected` (주방 원 진동센서)
  - Condition 2: `Tilt = Tilt detected` (주방 원 진동센서)
- Source action:
  - Device label: `주방불`
  - Action: `Switch 1 -> ON`
- Validity range:
  - 유효 기간: `하루 종일`
  - 유효 시기 조건: `주방 재실 센서 / Induction state = move&present`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (round vibration sensor): `binary_sensor.jubang_round_vibration`
- Validity condition entity (kitchen presence): `binary_sensor.jubang_presence`
- Target entity (kitchen ceiling light): `switch.jubang_ceiling_light`

Mapping note:

- Source app exposes `Vibration` and `Tilt` as separate conditions from the same device.
- In HA, this may be represented as one binary sensor with attributes/events depending on integration.

## Entry 008

- Source app routine name:
  - `외출 가상2 on`
- Category: `외출`, `가상스위치`
- Room: `현관` (global home-state gate conditions included)
- Intent: when outing virtual switch 1 turns on, turn on outing virtual switch 2 (only under defined away-state validity conditions)

### 008-A: 외출 가상2 on

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `외출 가상스위치 / POWER1 = ON`
- Source action:
  - Device label: `외출 가상스위치2`
  - Action: `Switch 1 -> ON`
- Validity range:
  - 유효 기간: `하루 종일`
  - 유효 시기: `모든 조건 충족` (6개 조건)
    - `화장실 재실센서 / Induction state = None`
    - `거실 재실센서 / Induction state = None`
    - `주방 재실 센서 / Induction state = None`
    - `안방조명 / Brightness := 996`
    - `주방 재실 센서 / Induction state = None` (source screen duplicated)
    - `안방 재실센서 / Induction state = None`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (outing virtual 1): `switch.hyeongwan_outing_virtual_1`
- Target entity (outing virtual 2): `switch.hyeongwan_outing_virtual_2`
- Validity condition entity (bathroom presence): `binary_sensor.hwajangsil_presence`
- Validity condition entity (living room presence): `binary_sensor.geosil_presence`
- Validity condition entity (kitchen presence): `binary_sensor.jubang_presence`
- Validity condition entity (bedroom presence): `binary_sensor.anbang_presence`
- Validity condition entity (bedroom light brightness, assumed): `switch.anbang_ceiling_light`

Mapping note:

- Source condition `Brightness := 996` is vendor-app specific representation and likely corresponds to a brightness/state threshold on bedroom light.
- `주방 재실 None` appears twice in the source capture; documented as-is pending final HA migration cleanup.

## Entry 009

- Source app routine name:
  - `안방OFF 거실ON`
- Category: `조명`
- Room: `안방`, `거실` (cross-room handoff)
- Intent: when moving to living room while bedroom is empty and bedroom light is on, hand off lighting from bedroom to living room

### 009-A: 안방OFF 거실ON

- Source trigger:
  - Condition mode: `모든 조건이 충족되었을 경우`
  - Condition 1: `거실 재실센서 / Induction state = move&present`
  - Condition 2: `안방 재실센서 / Induction state = None`
  - Condition 3: `안방조명 / ON/OFF = ON`
- Source action:
  - Device label: `거실 커튼불`
  - Action 1: `Switch 1 -> ON`
  - Device label: `안방불`
  - Action 2: `Switch 1 -> OFF`
  - Action 3: `작업 연기 1초`
  - Device label: `거실 스탠드 조명`
  - Action 4: `ON/OFF -> ON`

Canonical mapping (assumed from live baseline):

- Condition entity (living room presence): `binary_sensor.geosil_presence`
- Condition entity (bedroom presence): `binary_sensor.anbang_presence`
- Condition entity (bedroom ceiling light on): `switch.anbang_ceiling_light`
- Target entity (living room curtain line lighting switch): `switch.geosil_line_lighting_plug`
- Target entity (bedroom ceiling light off): `switch.anbang_ceiling_light`
- Target entity (living room stand light on): `light.geosil_stand_lighting`

## Entry 010

- Source app routine name:
  - `안방의자 앉으면 안방불ON`
- Category: `조명`, `작업환경`
- Room: `안방`
- Intent: when sitting at bedroom desk chair under specific room state, power on desk setup and bedroom ceiling light

### 010-A: 안방의자 앉으면 안방불ON

- Source trigger:
  - Condition mode: `모든 조건이 충족되었을 경우`
  - Condition 1: `안방 의자센서 / Vibration State = Vibration detected`
  - Condition 2: `안방조명 / Brightness := 996`
  - Condition 3: `안방 커튼 / Control = Close`
- Source action:
  - Device label: `안방 1책상선풍기/2마이크/3스피커`
  - Action 1: `스피커 -> ON`
  - Action 2: `책상선풍기 -> ON`
  - Action 3: `마이크 -> ON`
  - Device label: `안방불`
  - Action 4: `Switch 1 -> ON`

Canonical mapping (assumed from live baseline):

- Condition entity (chair vibration, assumed): `binary_sensor.anbang_chair_vibration`
- Condition entity (bedroom light brightness/state): `switch.anbang_ceiling_light`
- Condition entity (curtain closed state): `cover.anbang_curtain`
- Target entity (desk speaker): `switch.anbang_desk_speaker`
- Target entity (desk fan): `switch.anbang_desk_fan`
- Target entity (desk mic): `switch.anbang_desk_mic`
- Target entity (bedroom ceiling light): `switch.anbang_ceiling_light`

Mapping note:

- `안방 의자센서` is not currently listed in live baseline docs and is recorded as an assumed mapping placeholder pending live entity verification.

## Entry 011

- Source app routine name:
  - `주방등Off`
- Category: `조명`
- Room: `주방`
- Intent: when kitchen presence clears, turn off kitchen light (only while kitchen light is currently on)

### 011-A: 주방등Off

- Source trigger:
  - Condition mode: `모든 조건이 충족되었을 경우`
  - Condition: `주방 재실 센서 / Induction state = None`
- Source action:
  - Device label: `주방불`
  - Action: `Switch 1 -> OFF`
- Validity range:
  - 유효 기간: `하루 종일`
  - 유효 시기 조건: `어떤 조건이든 충족`
    - `주방불 / Switch 1 = ON`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (kitchen presence): `binary_sensor.jubang_presence`
- Validity condition entity (kitchen light state): `switch.jubang_ceiling_light`
- Target entity (kitchen ceiling light): `switch.jubang_ceiling_light`

## Entry 012

- Source app routine name:
  - `제습기 On`
- Category: `공조`, `습도제어`
- Room: `옷방` (with door/outing helper gate)
- Intent: turn on dehumidifier when humidity is high and door helper condition allows operation

### 012-A: 제습기 On

- Source trigger:
  - Condition mode: `모든 조건이 충족되었을 경우`
  - Condition 1: `현관 도어 가상스위치 / Switch 1 = OFF`
  - Condition 2: `옷방 제습기 / Indoor Humidity > 50%`
  - Condition 3: `옷방 온습도센서 / 습도 > 49%`
- Source action:
  - Device label: `옷방 제습기`
  - Action: `Power -> ON`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Condition entity (door virtual switch, assumed): `switch.hyeongwan_door_virtual`
- Condition entity (osbang humidity sensor): `sensor.osbang_humidity`
- Target entity (dehumidifier power): `humidifier.osbang_dehumidifier`

Mapping note:

- `현관 도어 가상스위치` is not listed in current live baseline docs and is recorded as an assumed placeholder pending live verification.
- Source uses both device-reported humidity and external humidity sensor threshold together.

## Entry 013

- Source app routine name:
  - `제습기 Off 1`
- Category: `공조`, `습도제어`, `알림`
- Room: `옷방`
- Intent: turn off dehumidifier when humidity drops below threshold, then send inbox notification

### 013-A: 제습기 Off 1

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `옷방 온습도센서 / 습도 < 42%`
- Source action:
  - Device label: `옷방 제습기`
  - Action 1: `Power -> OFF`
  - Action 2: `수신함 켜짐` (inbox notification)
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (osbang humidity sensor): `sensor.osbang_humidity`
- Target entity (dehumidifier power): `humidifier.osbang_dehumidifier`
- Notification action: `HA notification service mapping required at implementation`

## Entry 014

- Source app routine name:
  - `새벽히터ON`
- Category: `공조`, `스케줄`
- Room: `안방`
- Intent: run heater-on scene at dawn, then auto-run heater-off scene after 30 minutes

### 014-A: 새벽히터ON

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `스케줄 = 매일 오전 5:00`
- Source action:
  - Action 1: `히터 ON` (탭하여 실행)
  - Action 2: `작업 연기 30분`
  - Action 3: `히터 OFF` (탭하여 실행)
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger type: daily time schedule (`05:00`)
- Target domain (heater control): `climate.anbang_heater` and/or `switch.anbang_heater_plug`

Mapping note:

- `히터 ON` and `히터 OFF` are source app scene/automation actions; exact HA service mapping (climate setpoint vs plug power) must be finalized during implementation.

## Entry 015

- Source app routine name:
  - `가습기ON`
- Category: `공조`, `습도제어`
- Room: `안방`
- Intent: turn on humidifier when bedroom humidity is low

### 015-A: 가습기ON

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `안방 온습도센서 / Humidity < 45.0%`
- Source action:
  - Device label: `안방 가습기`
  - Action: `Switch 1 -> ON`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (bedroom humidity): `sensor.anbang_humidity`
- Target entity (humidifier plug): `switch.anbang_humidifier`

## Entry 016

- Source app routine name:
  - `가습기OFF`
- Category: `공조`, `습도제어`
- Room: `안방`
- Intent: turn off humidifier when bedroom humidity is high

### 016-A: 가습기OFF

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `안방 온습도센서 / Humidity > 60.0%`
- Source action:
  - Device label: `안방 가습기`
  - Action: `Switch 1 -> OFF`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (bedroom humidity): `sensor.anbang_humidity`
- Target entity (humidifier plug): `switch.anbang_humidifier`

## Entry 017

- Source app routine name:
  - `현관 도어 열림`
- Category: `출입`, `가상스위치`
- Room: `현관`
- Intent: when entrance door opens, turn on entrance door virtual switch

### 017-A: 현관 도어 열림

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `현관 도어 센서 / Door Sensor = ON`
- Source action:
  - Device label: `현관 도어 가상스위치`
  - Action: `Switch 1 -> ON`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (entrance door): `binary_sensor.hyeongwan_door`
- Target entity (entrance door virtual switch, assumed): `switch.hyeongwan_door_virtual`

Mapping note:

- `현관 도어 가상스위치` is not listed in current live baseline docs and is recorded as an assumed placeholder pending live verification.

## Entry 018

- Source app routine name:
  - `현관 도어 닫힘`
- Category: `출입`, `가상스위치`
- Room: `현관`
- Intent: when entrance door closes, turn off entrance door virtual switch

### 018-A: 현관 도어 닫힘

- Source trigger:
  - Condition mode: `어떤 조건이든 충족되었을 경우`
  - Condition: `현관 도어 센서 / Door Sensor = OFF`
- Source action:
  - Device label: `현관 도어 가상스위치`
  - Action: `Switch 1 -> OFF`
- Validity range: `하루 종일`
- Room display: `OFF`

Canonical mapping (assumed from live baseline):

- Trigger entity (entrance door): `binary_sensor.hyeongwan_door`
- Target entity (entrance door virtual switch, assumed): `switch.hyeongwan_door_virtual`

## Entry 019

- Source app routine name:
  - `일몰에 커튼 닫기`
- Category: `커튼`, `스케줄`
- Room: `안방` (device label: `CURTAIN`)
- Intent: close curtain daily at sunset offset

### 019-A: 일몰에 커튼 닫기

- Source trigger:
  - Type: `일몰 1분 전`
  - Schedule: `매일`
- Source action:
  - Device label: `CURTAIN`
  - Action: `블라인드 -> 닫기`

Canonical mapping (assumed from live baseline):

- Trigger type: `sunset - 1 minute`
- Target entity (curtain): `cover.anbang_curtain`

## Entry 020

- Source app routine name:
  - `데일리 루틴 스피커`
- Category: `스케줄`, `전원제어`
- Room: source label shows `거실` (physical room likely `안방`, pending verification)
- Intent: daily speaker power cycle (off then on)

### 020-A: 데일리 루틴 스피커

- Source trigger/action:
  - `매일 05:59` -> `3스피커 끄기`
  - `매일 06:02` -> `3스피커 켜기`
- Source device label:
  - `3스피커`
  - App room label: `거실`

Canonical mapping (assumed from live baseline):

- Target entity candidate 1: `switch.anbang_desk_speaker`
- Target entity candidate 2: `switch.anbang_bedside_speaker` (if separate bedside plug exists)

Mapping note:

- User indicated this is likely bedroom bedside speaker plug/switch.
- Current live baseline explicitly lists `switch.anbang_desk_speaker` but does not list a dedicated bedside speaker entity.
- Final HA migration should verify the physical device by toggling candidate entities once in live state.

## Entry 021

- Source app routine name:
  - `기상시 안방불 off`
- Category: `기상`, `조명`, `스케줄`
- Room: `안방` (with bathroom state condition)
- Intent: in morning window, if bedroom light and bathroom light are on, execute wake-up off actions

### 021-A: 기상시 안방불 off

- Source preceding conditions:
  - Time window: `매일 오전 06:00 - 오후 12:01`
  - Execution policy: `하루에 한 번만 실행`
  - Condition mode: `아래 조건을 모두 만족하면`
    - `안방조명 = 켜짐`
    - `화장실 불 = 켜짐`
- Source action (visible in provided capture):
  - Action 1: `안방불 -> 끄기`
  - Action 2: `3침대선풍기 -> 끄기`

Canonical mapping (assumed from live baseline):

- Time condition: daily between `06:00` and `12:01`, once-per-day
- Condition entity (bedroom light): `switch.anbang_ceiling_light`
- Condition entity (bathroom light): `switch.hwajangsil_ceiling_light`
- Target entity (bedroom light off): `switch.anbang_ceiling_light`
- Target entity (bedside fan off): `switch.anbang_bedside_fan`

Mapping note:

- This routine is documented as preceding-condition driven (not a separate explicit trigger row in source capture).
- Screenshot is partially cropped; only visible actions were documented.
- If additional actions exist below the visible area, append them in a follow-up capture.

## Entry 022

- Source app routine name:
  - `외출 가상스위치 길게 켜져있으면 끄기`
- Category: `외출`, `가상스위치`, `자동복귀`
- Room: source label shows `거실` (logical function is outing helper)
- Intent: auto-reset outing virtual switch to off if it stays on for at least 1 minute

### 022-A: 외출 가상스위치 길게 켜져있으면 끄기

- Source trigger:
  - Device: `외출 가상스위치`
  - State: `켜짐`
  - Duration: `1분 이상`
- Source action:
  - Device: `외출 가상스위치`
  - Action: `끄기`

Canonical mapping (assumed from live baseline):

- Trigger/target entity candidate: `switch.hyeongwan_outing_virtual_1`

Mapping note:

- Source label does not explicitly distinguish outing virtual 1 vs 2.
- Existing source routines indicate primary chaining from outing virtual 1 to 2, so this entry is mapped to virtual 1 as default assumption.

## Entry 023

- Source app routine name:
  - `화장실 5분 이상이면 환풍기on`
- Category: `환풍`, `타이머`, `가상스위치`
- Room: `화장실`
- Intent: when bathroom virtual switch is on and bathroom light state condition matches, run timed vent-fan cycle and reset virtual switch

### 023-A: 화장실 5분 이상이면 환풍기on

- Source trigger:
  - Condition mode: `아래 조건을 모두 만족하면`
  - Condition 1: `화장실 가상스위치 = 켜짐`
  - Condition 2: `화장실 불 = 꺼짐`
- Source action:
  - Action 1: `화장실 환풍기 -> 켜기`
  - Action 2: `대기 3초`
  - Action 3: `화장실 가상스위치 -> 끄기`
  - Action 4: `대기 6분 57초`
  - Action 5: `화장실 환풍기 -> 끄기`

Canonical mapping (assumed from live baseline):

- Condition entity (bathroom virtual switch): `switch.hwajangsil_virtual`
- Condition entity (bathroom light): `switch.hwajangsil_ceiling_light`
- Target entity (vent fan): `switch.hwajangsil_vent_fan`
- Mid-sequence reset target: `switch.hwajangsil_virtual`

Mapping note:

- Routine title says "5분 이상" but the shown trigger is state-combination based; the duration behavior appears implemented through the internal wait sequence.
- Total timed sequence shown: `3초 + 6분57초 = 7분`.

## Entry 024

- Source app routine name:
  - `화장실 가상스위치 켜기`
- Category: `환풍`, `가상스위치`, `지연트리거`
- Room: `화장실`
- Intent: if bathroom light remains on for 3 minutes 30 seconds, turn on bathroom virtual switch

### 024-A: 화장실 가상스위치 켜기

- Source trigger:
  - Device: `화장실 불`
  - State: `켜짐`
  - Duration: `3분 30초 이상`
- Source action:
  - Device: `화장실 가상스위치`
  - Action: `켜기`

Canonical mapping (assumed from live baseline):

- Trigger entity: `switch.hwajangsil_ceiling_light`
- Target entity: `switch.hwajangsil_virtual`

## Entry 025

- Source app routine name:
  - `3드라이기불 스위치 켜기`
- Category: `전원연동`, `플러그`
- Room: source labels mixed (`지정된 방 없음`, action label `거실`)
- Intent: when `드라이기` turns on, turn on `3드라이기불 스위치`

### 025-A: 3드라이기불 스위치 켜기

- Source trigger:
  - Device: `드라이기`
  - State: `켜짐`
- Source action:
  - Device: `3드라이기불 스위치`
  - Action: `켜기`

Canonical mapping (assumed from live baseline):

- Trigger entity candidate: `switch.jubang_hair_dryer_plug`
- Target entity candidate (user-provided likely mapping): `switch.jubang_line_lighting_plug`

Mapping note:

- User indicated this is probably kitchen line-lighting plug; recorded as primary assumption.
- Source room labels are inconsistent, so final migration should verify by live toggle check.

## Entry 026

- Source app routine name:
  - `드라이기 사용시 불 10분후 자동Off`
- Category: `전원연동`, `타이머`, `플러그`
- Room: 주방 (user-confirmed target: kitchen line-lighting plug)
- Intent: when dryer remains on, auto turn off linked line-lighting plug after delay

### 026-A: 드라이기 사용시 불 10분후 자동Off

- Source trigger:
  - Device: `드라이기`
  - State: `켜짐`
  - Duration: `20초 이상`
- Source action:
  - Action 1: `대기 11분`
  - Action 2: `3드라이기불 스위치 -> 끄기`

Canonical mapping (assumed from live baseline):

- Trigger entity: `switch.jubang_hair_dryer_plug`
- Target entity (user-confirmed): `switch.jubang_line_lighting_plug`

Mapping note:

- Routine title says `10분후` while shown wait is `11분`; source values are documented as-is.

## Entry 027

- Source app routine name:
  - `굿나잇 가상스위치 끄기`
- Category: `취침`, `가상스위치`, `자동복귀`
- Room: logical `안방` (source room label shows `거실`)
- Intent: auto-reset goodnight virtual switch to off after it stays on
- Status: `구현 보류` (현재 기능은 Entry 006에서 `switch.anbang_goodnight_virtual` OFF 처리로 충족)

### 027-A: 굿나잇 가상스위치 끄기

- Source trigger:
  - Device: `굿나잇 가상스위치`
  - State: `켜짐`
  - Duration: `10초 이상`
- Source action:
  - Device: `굿나잇 가상스위치`
  - Action: `끄기`

Canonical mapping (assumed from live baseline):

- Trigger/target entity: `switch.anbang_goodnight_virtual`

## Entry 028

- Source app routine name:
  - `굿나잇`
- Category: `취침`, `조명`, `가상스위치`
- Room: `안방`
- Intent: when bedtime conditions are met, run goodnight shutdown actions

### 028-A: 굿나잇

- Source preceding conditions:
  - Condition 1: `1침대등 스위치 = 켜짐`
  - Condition 2: `2머리말 재실 스위치 = 켜짐`
  - Condition 3: `안방조명 밝기 = 1%`
- Source trigger:
  - `굿나잇 가상스위치 = 켜짐`
- Source action (visible in provided capture):
  - Action 1: `안방조명 -> 끄기`
  - Action 2: `1침대등 스위치 -> 끄기`

Canonical mapping (assumed from live baseline):

- Condition entity (bedside light): `switch.anbang_bedside_light`
- Condition entity (bedside presence switch): `switch.anbang_bedside_presence_switch`
- Condition entity (stand-light 1% state): `scene.anbang_stand_lighting_1` or stand-light brightness state (implementation check required)
- Trigger entity (goodnight virtual): `switch.anbang_goodnight_virtual`
- Target entity (bedroom ceiling light): `switch.anbang_ceiling_light`
- Target entity (bedside light): `switch.anbang_bedside_light`

Mapping note:

- Screenshot is partially cropped; only visible actions were documented.
- If there are additional actions below the visible area, append in a follow-up capture.

## Entry 029

- Source app routine name:
  - `외출`
- Category: `외출`, `전체소등`, `알림`
- Room: 전역(다중 방)
- Intent: when outing virtual switch 2 turns on, run whole-home shutdown sequence, send notification, then reset outing virtual switches

### 029-A: 외출

- Source trigger:
  - Device: `외출 가상스위치2`
  - State: `켜짐`
- Source action (visible in provided captures):
  - Action 1: `거실 스탠드 조명 -> 끄기`
  - Action 2: `커튼불 -> 끄기`
  - Action 3: `43" Smart Monitor M7 -> 끄기`
  - Action 4: `멤버에게 알림 보내기 -> 외출 완료`
  - Action 5: `주방불 -> 끄기`
  - Action 6: `안방불 -> 끄기`
  - Action 7: `안방조명 -> 끄기`
  - Action 8: `거실불 -> 끄기`
  - Action 9: `3침대선풍기 -> 끄기`
  - Action 10: `대기 10초`
  - Action 11: `외출 가상스위치 -> 끄기`
  - Action 12: `외출 가상스위치2 -> 끄기`

Canonical mapping (assumed from live baseline):

- Trigger entity: `switch.hyeongwan_outing_virtual_2`
- Target entity (living room stand): `light.geosil_stand_lighting`
- Target entity (curtain line light switch): `switch.geosil_line_lighting_plug`
- Target entity (monitor): `media_player.geosil_tv` (source device label: `43\" Smart Monitor M7`)
- Notification action: `HA notification service mapping required at implementation`
- Target entity (kitchen ceiling light): `switch.jubang_ceiling_light`
- Target entity (bedroom ceiling light): `switch.anbang_ceiling_light`
- Target entity (bedroom stand/aux light, assumed from source label `안방조명`): `light.anbang_stand_lighting`
- Target entity (living room main light, assumed from source label `거실불`): `switch.geosil_ceiling_light`
- Target entity (bedside fan): `switch.anbang_bedside_fan`
- Reset entity (outing virtual 1): `switch.hyeongwan_outing_virtual_1`
- Reset entity (outing virtual 2): `switch.hyeongwan_outing_virtual_2`

Mapping note:

- Source contains both `안방불` and `안방조명` as separate targets; documented as separate entities.
- Source contains both `커튼불` and `거실불`; documented as separate targets.

## Entry 030

- Source app routine name:
  - `복귀`
- Category: `복귀`, `전체복원`, `알림`
- Room: 전역(다중 방)
- Intent: when return-home conditions are met, restore key lights/devices and send return notification

### 030-A: 복귀

- Source preceding conditions:
  - Condition 1: `거실 스탠드 조명 = 꺼짐`
  - Condition 2: `현관 도어 가상스위치 = 켜짐`
- Source action (visible in provided captures):
  - Action 1: `멤버에게 알림 보내기 -> 복귀`
  - Action 2: `43" Smart Monitor M7 -> 켜기`
  - Action 3: `거실 스탠드 조명 -> 켜기 (밝기 100, 하루 조명 자동 색온도)`
  - Action 4: `커튼불 -> 켜기`
  - Action 5: `안방조명 -> 켜기 (밝기 100%)`
  - Action 6: `3침대선풍기 -> 켜기`
  - Action 7: `1책상선풍기 -> 켜기`
  - Action 8: `3스피커 -> 켜기`

Canonical mapping (assumed from live baseline):

- Condition entity (living room stand light): `light.geosil_stand_lighting`
- Condition entity (entrance door virtual switch, assumed): `switch.hyeongwan_door_virtual`
- Notification action: `HA notification service mapping required at implementation`
- Target entity (monitor): `media_player.geosil_tv`
- Target entity (living room stand light): `light.geosil_stand_lighting`
- Target entity (curtain line light switch): `switch.geosil_line_lighting_plug`
- Target entity (bedroom stand/aux light, assumed from source label `안방조명`): `light.anbang_stand_lighting`
- Target entity (bedside fan): `switch.anbang_bedside_fan`
- Target entity (desk fan): `switch.anbang_desk_fan`
- Target entity (speaker, assumed): `switch.anbang_desk_speaker`

Mapping note:

- Source includes plug labels with room shown as `거실` for some bedroom devices; device-role mapping follows established prior assumptions in this inventory.
- If additional actions exist below visible capture area, append in follow-up.

## Migration Notes

- This source behavior is effectively the same policy as:
  - `[조명] 옷방 자동 점등/소등 (재실 연동)`
- For HA implementation, these two source routines can be merged into one automation with `choose`.
- Bathroom source behavior can be implemented as one HA automation with `choose`:
  - `presence on` (+ optional door condition) -> light/fan on
  - `presence off` -> light/fan off
