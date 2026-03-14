# Anbang TH Sensor Migration Plan v1

Last updated: 2026-03-03
Status: investigated

## Scope

This plan covers the active bedroom temperature/humidity monitor entities:

- `sensor.anbang_onseubdosenseo_temperature`
- `sensor.anbang_onseubdosenseo_humidity`
- `sensor.anbang_onseubdosenseo_battery`

## Findings

- All three active entities belong to the same live Tuya device:
  - `device_id = 6be75bec7f54fb03075a771d64f25a0e`
  - `area_id = anbang`
  - `platform = tuya`
- Their current display names are already clean:
  - `안방 온도`
  - `안방 습도`
  - `안방 온습도센서 배터리`
- Active dashboard references are narrow:
  - one bedroom sensor card in `홈킷 뷰(Sections)`
  - one bedroom sensor card in `Home`

## Duplicate Legacy Entities

There are disabled SmartThings remnants:

- `sensor.anbang_onseubdosenseo_temperature_2`
- `sensor.anbang_onseubdosenseo_humidity_2`

These are not part of the live target set because:

- `disabled_by = user`
- `area_id = None`
- they belong to a different device
- they are not used by the active dashboard

## Target Entity IDs

- `sensor.anbang_onseubdosenseo_temperature` -> `sensor.anbang_temperature`
- `sensor.anbang_onseubdosenseo_humidity` -> `sensor.anbang_humidity`
- `sensor.anbang_onseubdosenseo_battery` -> `sensor.anbang_th_monitor_battery`

## Risk Assessment

Risk is moderate-low.

- Active dashboard references are simple and known.
- Duplicate legacy entities are already disabled, so id collisions are unlikely for the target ids above.
- Remaining unknown risk is hidden references in automations or scripts outside the current workspace snapshots.

## Recommended Execution Order

1. Confirm no active automation relies on the old ids.
2. Rename the three entities directly in the entity registry.
3. Update active Lovelace references.
4. Verify live states on the new ids.
5. Verify the dashboard still renders without missing entities.
