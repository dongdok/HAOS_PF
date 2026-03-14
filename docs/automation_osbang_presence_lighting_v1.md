# Automation Draft: Osbang Presence Lighting v1

Last updated: 2026-03-03
Status: active baseline

## Summary

- Category: `조명`
- Room: `옷방`
- Alias: `[조명] 옷방 자동 점등/소등 (재실 연동)`

This automation is the first canonical Home Assistant automation baseline for this project.

It replaces the old SmartThings-style behavior:

- `[옷방 In]`
  - closest target distance detected -> light on
- `[옷방 Out]`
  - no presence -> light off

## Canonical Entity IDs

- trigger entities:
  - `number.osbang_jaesilsenseo_closest_target_distance`
  - `binary_sensor.osbang_presence`
- controlled entity:
  - `switch.osbang_ceiling_light`

Reason:

- all ids are already standardized in the live baseline
- both ids match the room plan and naming rules
- no legacy or rescue ids are involved
- the closest target distance sensor reacts earlier than the occupancy binary sensor

## YAML

```yaml
alias: "[조명] 옷방 자동 점등/소등 (재실 연동)"
description: "옷방 최근접 거리 변화와 재실 상태에 따라 천장 조명을 자동으로 켜고 끕니다."
mode: restart
trigger:
  - platform: numeric_state
    entity_id: number.osbang_jaesilsenseo_closest_target_distance
    above: 0
    id: distance_detected

  - platform: state
    entity_id: binary_sensor.osbang_presence
    to: "off"
    id: presence_off

action:
  - choose:
      - conditions:
          - condition: trigger
            id: distance_detected
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

## Testing Plan

1. Create the HA automation without disabling the old external routine yet.
2. Enter the clothing room and verify:
   - `number.osbang_jaesilsenseo_closest_target_distance` rises above `0`
   - `switch.osbang_ceiling_light` turns `on`
3. Leave the clothing room and verify:
   - `binary_sensor.osbang_presence` changes to `off`
   - `switch.osbang_ceiling_light` turns `off` immediately
4. Repeat the cycle at least once more.
5. Only after successful verification, disable the old SmartThings routine.

## Notes

- This baseline uses closest target distance for faster light-on behavior than the occupancy binary sensor alone.
- This baseline intentionally uses immediate off because that is the desired room behavior.
- No delay, helper entity, or extra condition is introduced.
- This automation is the reference template for future room-lighting automations.
