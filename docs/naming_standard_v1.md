# HAOS Naming Standard v1

Last updated: 2026-03-03
Status: proposed working standard

## Goal

This standard defines the target naming model for:

- area names
- device names
- entity display names
- entity ids

It is intended to become the long-term stable standard for dashboards, automations, and documentation.

## Core Principle

Use a two-layer naming model.

| Layer | Pattern | Purpose | Example |
|---|---|---|---|
| Device name | `[영역] [기기명]` | identify the physical or logical device | `안방 가습기`, `거실 커튼` |
| Entity name | `[영역] [기기명] [기능/상세]` | identify one function, sensor, or control of that device | `안방 가습기 전력`, `거실 커튼 전류` |

This avoids mixing:

- what the device is
- what the specific entity does

## Area Naming

### Display Name

Use short Korean names for user-facing labels.

- `거실`
- `주방`
- `안방`
- `옷방`
- `화장실`
- `현관`

### Internal Area ID

Use stable romanized ids.

- `geosil`
- `jubang`
- `anbang`
- `osbang`
- `hwajangsil`
- `hyeongwan`

## Device Naming

### Rule

Use:

`[영역] [기기명]`

### Examples

- `안방 가습기`
- `안방 전기장판`
- `안방 책상 멀티탭`
- `안방 침대 멀티탭`
- `거실 TV`
- `거실 커튼 라인 조명`
- `주방 드라이기`
- `화장실 도어센서`

### Guidance

- Prefer the user-recognizable device name over a generic category label.
- Use one canonical name per device.
- Avoid adding integration/vendor details to the device name.
- Avoid inconsistent synonyms such as mixing `전등`, `조명`, `불` for the same device class unless they intentionally describe different devices.

## Entity Display Naming

### Rule

Use:

`[영역] [기기명] [기능/상세]`

### Common Examples

- `안방 가습기 플러그`
- `안방 가습기 전류`
- `안방 가습기 전력`
- `안방 가습기 전압`
- `안방 전기장판 플러그`
- `안방 전기장판 전력`
- `거실 커튼 라인 조명 밝기`
- `주방 재실센서 재실감지`
- `화장실 도어센서 배터리`

### Detail Vocabulary

Use a controlled vocabulary where possible.

- control: `플러그`, `스위치`, `밝기`, `색상`, `전원`, `온도 설정`
- power metrics: `전류`, `전력`, `전압`, `총 에너지`
- sensor readings: `온도`, `습도`, `배터리`, `조도`, `재실감지`, `열림`
- special functions: `차일드 락`, `표시등`, `필터 재설정`

## Entity ID Standard

### Rule

Use lowercase snake case:

`domain.area_device_name_detail`

If no detail is needed:

`domain.area_device_name`

### Examples

- `switch.anbang_humidifier_plug`
- `sensor.anbang_humidifier_power`
- `sensor.anbang_humidifier_voltage`
- `switch.anbang_electric_blanket_plug`
- `sensor.anbang_electric_blanket_power`
- `media_player.geosil_tv`
- `cover.anbang_curtain`
- `binary_sensor.jubang_presence`
- `binary_sensor.hwajangsil_door`

### Entity ID Rules

- Use English or stable romanized words only
- Use one canonical device token
- Use one canonical detail token
- Do not mix Korean transliteration styles across ids
- Do not encode vendor names in the id
- Do not include temporary numbering like `_2` unless required by the platform and explicitly accepted

## Device vs Entity Examples

### Single-function device

- Device: `안방 가습기`
- Entities:
  - `switch.anbang_humidifier_plug`
  - `sensor.anbang_humidifier_power`
  - `sensor.anbang_humidifier_voltage`

### Multi-outlet device

- Device: `안방 책상 멀티탭`
- Entities:
  - `switch.anbang_desk_fan`
  - `switch.anbang_desk_mic`
  - `switch.anbang_desk_speaker`

### Composite climate-related device

- Device: `안방 히터`
- Entities:
  - `switch.anbang_heater_plug`
  - `climate.anbang_heater`
  - `sensor.anbang_heater_power`

## Dashboard Naming Guidance

- Prefer display names, not entity ids, in cards
- Show one primary control entity per device on the main dashboard
- Hide power metrics and config entities from main views unless they are frequently used
- Use the device name as the visual grouping label

## Migration Policy

This standard is the target model, not the current live truth.

Safe migration order:

1. confirm live entity
2. map old id to current live id
3. update dashboards and automations
4. only then rename or recreate entities toward the standard

Do not rename everything at once.

## Current Known Exceptions

- Bedroom currently has mixed legacy area references
- Some current live entities are exposed as `switch.*` even when the target model would prefer `light.*`
- Some target entities do not currently exist as live entities and must remain unmapped until reintroduced or retired

## Decision Rule

When current live behavior and target naming conflict:

- keep live behavior stable first
- keep mappings documented
- move gradually toward this standard
