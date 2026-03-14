# Anbang Heater Entity Migration Plan v1

Last updated: 2026-03-03
Status: executed on 2026-03-03

## Goal

Normalize the bedroom heater entity ids so they match:

- actual room ownership: `anbang`
- actual function: `heater`
- current user-facing naming already in use

This is an entity-id architecture cleanup, not a behavior change.

## Previous Problem

The following entities previously belonged to the bedroom heater but used the stale prefix `jubang_ac_`.

| Current Live Entity ID | Current Display Name | Actual Room | Actual Function |
|---|---|---|---|
| `switch.jubang_ac_heating_plug` | 안방 히터 플러그 | 안방 | Heater power plug |
| `sensor.jubang_ac_heating_current` | 안방 히터 전류 | 안방 | Current |
| `sensor.jubang_ac_heating_power` | 안방 히터 전력 | 안방 | Power |
| `sensor.jubang_ac_heating_voltage` | 안방 히터 전압 | 안방 | Voltage |
| `sensor.jubang_ac_heating_total_energy` | 안방 히터 총 에너지 | 안방 | Total energy |

These five entities were confirmed in the entity registry as:

- `area_id = anbang`
- same `device_id = 4ddc242e9150187bcec5aedafce5b0c8`

## Important Non-Target

Do not rename this entity as part of the heater migration:

- `switch.jubang_ac_remote_hub`

Reason:
- it is a real kitchen entity
- `area_id = jubang`
- function is an IR hub, not the bedroom heater

## Target Entity IDs

| Current Entity ID | Target Entity ID |
|---|---|
| `switch.jubang_ac_heating_plug` | `switch.anbang_heater_plug` |
| `sensor.jubang_ac_heating_current` | `sensor.anbang_heater_current` |
| `sensor.jubang_ac_heating_power` | `sensor.anbang_heater_power` |
| `sensor.jubang_ac_heating_voltage` | `sensor.anbang_heater_voltage` |
| `sensor.jubang_ac_heating_total_energy` | `sensor.anbang_heater_total_energy` |

## Execution Result

Migration completed successfully.

Current live ids:

- `switch.anbang_heater_plug`
- `sensor.anbang_heater_current`
- `sensor.anbang_heater_power`
- `sensor.anbang_heater_voltage`
- `sensor.anbang_heater_total_energy`

Old ids no longer exist in live states:

- `switch.jubang_ac_heating_plug`
- `sensor.jubang_ac_heating_current`
- `sensor.jubang_ac_heating_power`
- `sensor.jubang_ac_heating_voltage`
- `sensor.jubang_ac_heating_total_energy`

## Current Reference Scope

Confirmed dashboard references were updated to:

- [lovelace_active.json](/Users/dy/Desktop/HAOS_Control/lovelace_active.json)
  - `switch.anbang_heater_plug` in the bedroom section of `홈킷 뷰(Sections)`
  - `switch.anbang_heater_plug` in the bedroom section of `Home`

Workspace search findings:

- direct references to `switch.jubang_ac_heating_plug` exist in local Lovelace snapshot files and helper scripts
- no clear direct references to the four heater metric sensors were found in current working scripts

## Migration Risk

### Low Risk

- display names are already correct
- room ownership is already correct in the registry
- target naming is obvious

### Medium Risk

- entity id changes can break dashboards, automations, scripts, and scenes if any hidden reference exists outside this workspace
- integration behavior depends on whether Home Assistant allows renaming the entity id directly or requires re-registration/recreation

## Safe Execution Strategy

1. confirm all direct references to the five current ids
2. decide migration method:
   - registry rename if supported and stable
   - otherwise create or re-expose new canonical entities
3. update dashboards to the new ids
4. update local scripts and docs
5. verify no remaining references to old ids
6. only then retire the old ids if applicable

## Pre-Migration Checklist

- dashboard references audited
- local workspace references audited
- no hidden automation references remain, or they are documented
- fallback or rollback path defined

## Rollback

If the new ids fail or references were missed:

1. revert dashboard references to the current `jubang_ac_heating_*` ids
2. restore previous entity ids or entity exposure
3. re-run audit before retrying

## Decision

Migration is complete. Keep this document as the audit trail for the heater id cleanup.
