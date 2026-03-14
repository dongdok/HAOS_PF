# Automation Agent Contract v1

Last updated: 2026-03-03
Status: mandatory execution contract

## Purpose

This document is the cross-agent execution contract for any automation work in this repository.

It is intended to be followed by:

- Codex
- Antigravity
- Claude
- any future coding or automation assistant

## Mandatory Reading Order

Before proposing, editing, or creating any automation, the agent must read these files in order:

1. [standardization_v1_complete.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_v1_complete.md)
2. [current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
3. [master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
4. [naming_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md)
5. [device_onboarding_rules_v1.md](/Users/dy/Desktop/HAOS_Control/docs/device_onboarding_rules_v1.md)
6. [automation_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/automation_standard_v1.md)

If the task is room-specific, the agent must also read the matching room plan:

- [standardization_plan_anbang_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_anbang_v1.md)
- [standardization_plan_geosil_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_geosil_v1.md)
- [standardization_plan_jubang_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_jubang_v1.md)
- [standardization_plan_osbang_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_osbang_v1.md)
- [standardization_plan_hwajangsil_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_hwajangsil_v1.md)
- [standardization_plan_hyeongwan_v1.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_plan_hyeongwan_v1.md)

## Canonical Rule

Automations must use only canonical entity ids from the live baseline.

The agent must not:

- use ids from archived docs
- use ids from backup lovelace json files
- use ids from rescue mappings
- use stale integration-generated names if a canonical id already exists

## Required Workflow

For every automation task:

1. identify the intended behavior exactly
2. confirm the current canonical entity ids
3. map the behavior to canonical ids only
4. write the automation using the structure in [automation_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/automation_standard_v1.md)
5. explain what old routine or behavior it replaces
6. define how it should be tested
7. only then propose or implement it

## Naming Rule

Automation aliases must follow:

`[분류] [영역] [행동] ([기준])`

Examples:

- `[조명] 옷방 자동 점등/소등 (재실 연동)`
- `[환풍] 화장실 자동 종료 (재실 해제)`
- `[외출] 현관 외출 모드 실행`

## YAML Rule

The automation must keep this section order:

1. `alias`
2. `description`
3. `mode`
4. `trigger`
5. `condition`
6. `action`

If `condition` is unnecessary, omit it cleanly.

## Mode Rule

Default mode policy:

- use `restart` for most state-driven room automations
- use `single` only when overlapping runs must be blocked
- use `parallel` only when concurrency is intentional

## Scope Rule

One automation should have one coherent purpose.

Preferred:

- one room
- one behavior family
- one set of related entities

Avoid:

- mixed-room automations
- mixed concern automations without a clear policy reason

## Replacement Rule

If replacing SmartThings, Tuya, or another external routine:

1. keep the original routine active until HA behavior is verified
2. test the HA automation in the real room
3. disable the original only after HA behavior is confirmed

## Output Rule

Before implementation, the agent must summarize:

1. which canonical ids are being used
2. why those ids are correct
3. what automation category and alias will be used
4. how the automation will be tested

## Change Control Rule

If the automation would require:

- a new helper entity
- a new scene
- a new virtual switch
- or a change to naming policy

the agent must state that explicitly before proceeding.

## Archive Rule

Archived files are reference-only.

The agent may read them for history, but must not treat them as the operational source of truth.
