# Automation Standard v1

Last updated: 2026-03-03
Status: active working standard

## Purpose

This document defines the baseline rules for creating Home Assistant automations in this project.

Goal:

- keep automations structurally consistent
- make automations readable and reviewable
- ensure automations are built on canonical entity ids
- make the system presentable as a coherent portfolio-grade setup

## Core Principle

Automations must be built on top of the already standardized live entity model.

Always check these first:

1. [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
2. [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
3. [naming_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md)
4. [device_onboarding_rules_v1.md](/Users/dy/Desktop/HAOS_Control/docs/device_onboarding_rules_v1.md)

## Naming Rule

Use:

`[분류] [영역] [행동] ([기준])`

Examples:

- `[조명] 옷방 자동 점등/소등 (재실 연동)`
- `[조명] 화장실 자동 점등/소등 (재실 연동)`
- `[환풍] 화장실 자동 종료 (재실 해제)`
- `[취침] 안방 굿나잇 실행`
- `[외출] 현관 외출 모드 실행`

## Required Automation Structure

Keep the YAML section order stable:

1. `alias`
2. `description`
3. `mode`
4. `trigger`
5. `condition`
6. `action`

If `condition` is not needed, omit it instead of leaving placeholder noise.

## Description Rule

Every automation should explain:

- what it controls
- what triggers it
- what main entity it affects

Example:

- `옷방 재실 상태에 따라 천장 조명을 자동으로 켜고 끕니다.`

## Entity Rule

- Use only canonical entity ids.
- Do not use legacy ids from historical docs or archive files.
- Do not use temporary integration-generated names if a canonical id already exists.

Examples:

- use `switch.osbang_ceiling_light`
- not `switch.osbang_main_light`

- use `switch.hwajangsil_ceiling_light`
- not `switch.hwajangsil_lighting`

## Scope Rule

One automation should have one clear responsibility.

Good:

- one room
- one behavioral purpose
- one coherent trigger set

Examples:

- 옷방 재실에 따라 조명 on/off
- 화장실 재실 해제 후 환풍기 끄기

Avoid:

- one automation controlling multiple unrelated rooms
- one automation mixing lighting, climate, and notifications without a clear reason

## Consolidation Rule

Use one automation with `choose` when two opposite actions belong to the same event pair.

Example:

- presence `on` -> light `on`
- presence `off` -> light `off`

This is preferred over creating two separate automations when the logic is symmetrical.

## Mode Rule

Default recommendations:

- state-reactive automation: `restart`
- strict one-shot automation: `single`
- truly independent concurrent runs only: `parallel`

Project default:

- prefer `restart` unless there is a strong reason not to

## Trigger Rule

Triggers should be explicit and minimal.

Good:

- state changes
- helper switch changes
- time triggers with a clear reason

Avoid:

- broad triggers with hidden filtering in actions

When using multiple triggers, give them `id` values and branch using `choose`.

## Condition Rule

Conditions should express policy, not compensate for bad triggers.

Use conditions for:

- time windows
- occupancy checks
- mode checks
- preventing unwanted execution

Do not overload conditions when a better trigger design would solve the same issue.

## Action Rule

Actions should be readable and deterministic.

Guidelines:

- prefer direct service calls to the canonical entity
- group opposite reactions with `choose`
- avoid deeply nested sequences unless necessary
- use helper entities only when their role is already documented

## Classification Rule

Every automation should belong to one category.

Suggested categories:

- `조명`
- `재실`
- `환풍`
- `공조`
- `취침`
- `외출`
- `알림`
- `안전`

This category should appear in the alias prefix.

## Migration Rule

When replacing SmartThings, Tuya, or another platform routine:

1. identify the original behavior exactly
2. map it to canonical HA entity ids
3. create the HA automation
4. test the HA automation first
5. only then disable the old external routine

Do not disable the original routine before verifying the HA replacement works.

## Testing Rule

Before declaring an automation active:

1. verify trigger entity
2. verify controlled entity
3. test the `on` path
4. test the `off` path
5. check for duplicate behavior from another platform

Minimum requirement:

- one real-world test cycle in the target room

## Documentation Rule

If an automation introduces a new dependency on a helper, virtual switch, scene, or unusual rule, document it.

At minimum update:

- [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md) if the operational baseline changes
- [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md) if the active entity set changes

If only behavior changes and entity set does not, keep the automation documented separately.

## Canonical First-Automation Template

```yaml
alias: "[조명] 옷방 자동 점등/소등 (재실 연동)"
description: "옷방 재실 상태에 따라 천장 조명을 자동으로 켜고 끕니다."
mode: restart
trigger:
  - platform: state
    entity_id: binary_sensor.osbang_presence
    to: "on"
    id: presence_on

  - platform: state
    entity_id: binary_sensor.osbang_presence
    to: "off"
    id: presence_off

action:
  - choose:
      - conditions:
          - condition: trigger
            id: presence_on
        sequence:
          - service: switch.turn_on
            target:
              entity_id: switch.osbang_ceiling_light

      - conditions:
          - condition: trigger
            id: presence_off
        sequence:
          - service: switch.turn_off
            target:
              entity_id: switch.osbang_ceiling_light
```

## Portfolio Rule

For this project to remain portfolio-grade:

- naming must stay predictable
- entity ids must stay canonical
- automations must look like they were written by one system designer
- every new automation must follow the same structural template
