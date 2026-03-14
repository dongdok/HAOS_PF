# Anbang Lighting Preset Structure v1

Last updated: 2026-03-03
Status: active decision

## Layer Model

These preset entities should be interpreted as bedroom stand-light presets, not as whole-room main-light presets.

### Base control layer

- `switch.anbang_stand_lighting_1`
- `switch.anbang_stand_lighting_100`

Reason:
- We are standardizing the system from the device/control layer upward.
- Switch entities are closer to the hardware-control foundation than scenes.
- Automations, scripts, and scenes should be built on top of stable control entities.
- The main bedroom light is `switch.anbang_ceiling_light`, which is on/off only.
- Brightness presets therefore align with `light.anbang_stand_lighting`, not with the main ceiling light.

### Convenience preset layer

- `scene.anbang_stand_lighting_1`
- `scene.anbang_stand_lighting_100`

Reason:
- Scenes are useful user-facing shortcuts.
- They are not the architectural truth source for device normalization.
- They should remain a derived layer built on top of the control layer.

## Architectural Decision

Use `switch.anbangjomyeong_*` as the canonical stand-light preset-control layer for normalization work.

Use `scene.anbangjomyeong_*` as the convenience stand-light preset layer for dashboard and future automation shortcuts.

## Practical Consequence

- Naming standards should treat the `switch.*` entities as the base stand-light preset control entities.
- The `scene.*` entities stay available, but they are not the primary normalization anchor.
- Dashboard can continue using the `scene.*` tiles for convenience without changing the architectural basis.

## Notes

- The two `switch.anbangjomyeong_*` entities currently have no area assignment in the registry, so they still need a later validation pass.
- This decision only changes the normalization model, not the current live dashboard behavior.

## Next Safe Step

1. Keep the current dashboard cards as-is.
2. Treat `switch.anbang_stand_lighting_1` and `switch.anbang_stand_lighting_100` as the canonical preset-control pair in docs.
3. Continue the remaining bedroom cleanup from core control entities such as `switch.anbang_bedside_presence_switch`.
