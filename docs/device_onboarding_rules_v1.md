# Device Onboarding Rules v1

Last updated: 2026-03-03
Status: active rule set

## Purpose

This document defines how new devices, spare devices, and previously disabled devices should enter the system from now on.

Goal:

- keep the live entity set consistent
- prevent new naming drift
- stop old `legacy/temporary/misnamed` ids from coming back into active use

## Core Rule

Do not let a newly added device become part of dashboards or automations until it passes the onboarding checklist.

Order:

1. discover the live entity created by the integration
2. decide the canonical room and device name
3. rename the entity id if needed
4. rename the display name
5. update the live hardware map
6. only then place it on dashboards or use it in automations

## Room And Area Rule

- Every active device must belong to one canonical room family:
  - `anbang`
  - `geosil`
  - `jubang`
  - `osbang`
  - `hwajangsil`
  - `hyeongwan`
- Do not activate a device with mixed room spellings such as `hyengwan` when `hyeongwan` is the canonical form.
- If an integration creates the wrong room-family token, correct it before the device becomes operationally visible.

## Device Naming Rule

Use:

- Device name: `[영역] [기기명]`
- Entity display name: `[영역] [기기명] [기능/상세]`

Examples:

- `거실 라인 조명`
- `주방 재실 센서 플러그`
- `화장실 도어 센서 배터리`
- `현관 외출 가상 스위치 1`

## Entity ID Rule

Use:

- `domain.area_device`
- or `domain.area_device_detail`

Examples:

- `switch.geosil_ceiling_light`
- `switch.jubang_line_lighting_plug`
- `sensor.hwajangsil_door_battery`
- `switch.hyeongwan_outing_virtual_1`

## Classification Rule

Before activation, every entity must be placed in one of these categories.

### 1. Core device layer

Actual operational controls or readings.

Examples:

- `switch.*`
- `light.*`
- `cover.*`
- `climate.*`
- main `binary_sensor.*`
- main `sensor.*`

These may go to dashboard and automations.

### 2. Helper layer

Virtual or helper controls.

Examples:

- `*_virtual_*`
- scenario helpers
- helper switches used only to trigger automations

These must be clearly labeled as virtual/helper.

### 3. Tuning / config layer

Adjustment-only entities.

Examples:

- sensitivity
- near detection
- far detection
- closest target distance
- indicator-light options

These do not belong on the main dashboard by default.

### 4. Spare / reserve layer

Connected but intentionally unused outlets or devices.

Examples:

- `*_unused1`
- reserve outlets
- test hardware

These should stay in `예비` or equivalent hidden area until promoted.

## Spare Device Activation Rule

When promoting a spare or disabled device:

1. confirm the physical role first
2. assign its final room
3. rename id and display name immediately
4. move it from spare/reserve status to active documentation
5. only then expose it to dashboards

Do not temporarily expose a spare device with placeholder names like:

- `unused`
- `main`
- `switch_1`
- integration default transliteration

unless there is a same-day cleanup planned.

## Integration Drift Rule

If Tuya, SmartThings, Samsung, or another integration recreates ids:

1. do not trust the new ids as-is
2. compare against [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
3. restore the canonical id if possible
4. fix dashboard references only after the canonical id is restored

## Dashboard Rule

- Only put primary controls and primary readings on the main dashboard.
- Do not put config/tuning entities on the main dashboard.
- If a device has multiple entities, the main dashboard should show:
  - one primary control
  - optional one primary sensor

Examples:

- show `거실 라인 조명`
- hide its lower-level recovery or setup entities

## Documentation Rule

Every new active device must update:

1. [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
2. [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)

If the onboarding changes the standard itself, also update:

3. [naming_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md)

## Activation Checklist

Before marking a new device active, confirm:

- room family is canonical
- entity id follows the standard
- display name follows the standard
- helper vs core vs tuning classification is decided
- dashboard placement is intentional
- documentation is updated

If any item is missing, the device is not ready for active use.
