# Dashboard Broken Cards Audit

Last verified: 2026-03-03
Source: current `lovelace_active.json` vs live Home Assistant states

## Summary

- Total broken card references found: 73
- Unique broken entity references after deduplication: 70
- Main pattern: dashboard cards still reference old entity ids from the old hardware map

## Post Safe Replacement Status

After applying only confirmed replacements:

- Remaining broken card references: 17
- Remaining unique broken entities: 10

Remaining unresolved entities:

- `sensor.geosil_tv_illuminance`
- `switch.jubang_multitab_unused1`
- `switch.jubang_presence_switch`
- `light.anbang_stand_lighting`
- `switch.anbang_desk_mic`
- `binary_sensor.anbang_round_vibration`
- `climate.anbang_heater`
- `scene.anbang_lighting_1`
- `scene.anbang_lighting_100`
- `switch.jubang_ac_remote_hub`

## Safe Replacement Queue

Replace only cards whose replacement is confirmed below.
Leave rows marked `none` untouched until separately re-identified.

### 거실

| Broken Entity ID | Card Type | Safe Replacement | Notes |
|---|---|---|---|
| `switch.geosil_lighting` | `tile` | `switch.geosilbul` | `light.geosiljomyeong` also exists |
| `switch.geosil_curtain_lighting_plug` | `tile` | `switch.keoteunbul` | |
| `light.geosil_curtain_lighting` | `tile` | `switch.keoteunbul` | `light.keoteunbul` also exists |
| `binary_sensor.geosil_presence` | `tile` | `binary_sensor.geosil_jaesilsenseo_occupancy` | |
| `media_player.geosil_tv` | `media-control` | `media_player.43_smart_monitor_m7` | |
| `sensor.geosil_tv_illuminance` | `tile` | none | no live replacement confirmed |

### 주방

| Broken Entity ID | Card Type | Safe Replacement | Notes |
|---|---|---|---|
| `switch.jubang_main_light` | `tile` | `switch.jubangbul` | |
| `binary_sensor.jubang_presence` | `tile` | `binary_sensor.jubang_jaesil_senseo_occupancy` | |
| `switch.jubang_multitab_unused1` | `tile` | none | likely should be removed rather than replaced |
| `switch.jubang_presence_switch` | `tile` | none | live direct replacement not confirmed |
| `switch.jubang_appliance_multitap` | `tile` | `switch.2jubang_jaesil_3deuraigibul_switch_2` | split-device replacement |
| `switch.jubang_dryer_plug` | `tile` | `switch.deuraigi` | |
| `switch.jubang_ac_remote_hub` | `tile` | none | no live remote-equivalent confirmed |

### 화장실

| Broken Entity ID | Card Type | Safe Replacement | Notes |
|---|---|---|---|
| `switch.hwajangsil_lighting` | `tile` | `switch.hwajangsil_bul` | |
| `switch.hwajangsil_lighting_fan` | `tile` | `switch.hwajangsil_hwanpunggi` | |
| `binary_sensor.hwajangsil_door_contact` | `tile` | `binary_sensor.hwajangsil_doeosenseo_door` | `_2` also exists |
| `binary_sensor.hwajangsil_presence` | `tile` | `binary_sensor.hwajangsil_jaesilsenseo_occupancy` | |

### 옷방

| Broken Entity ID | Card Type | Safe Replacement | Notes |
|---|---|---|---|
| `switch.osbang_main_light` | `tile` | `switch.osbangbul` | |
| `binary_sensor.osbang_presence` | `tile` | `binary_sensor.osbang_jaesilsenseo_occupancy` | |
| `humidifier.osbang_dehumidifier` | `humidifier` | `humidifier.jeseubgi` | `fan.jeseubgi` also exists |

### 안방

| Broken Entity ID | Card Type | Safe Replacement | Notes |
|---|---|---|---|
| `light.anbang_stand_lighting` | `tile` | none | no live equivalent confirmed |
| `switch.anbang_main_light` | `tile` | `switch.anbangbul` | `light.anbangjomyeong` also exists |
| `switch.anbang_desk_fan` | `tile` | `switch.1caegsangseonpunggi` | |
| `switch.anbang_desk_mic` | `tile` | none | no direct live replacement confirmed |
| `switch.anbang_desk_speaker` | `tile` | `switch.3seupikeo` | |
| `switch.anbang_bedside_light` | `tile` | `switch.1cimdaedeung_seuwici` | |
| `switch.anbang_bedside_presence_switch` | `tile` | `switch.2meorimat_jaesil_seuwici` | nearest live control |
| `switch.anbang_bedside_fan` | `tile` | `switch.3cimdaeseonpunggi` | |
| `switch.anbang_electric_blanket_plug` | `tile` | `switch.jeongimaeteu` | |
| `switch.jubang_ac_heating_plug` | `tile` | `switch.eeokeon_nanbang_on_off_socket_1` | old bedroom heater naming is stale |
| `binary_sensor.anbang_presence` | `tile` | `binary_sensor.anbang_jaesilsenseo_occupancy` | |
| `binary_sensor.anbang_round_vibration` | `tile` | none | no live equivalent confirmed |
| `climate.anbang_heater` | `thermostat` | none | no live climate entity confirmed |
| `cover.anbang_curtain` | `tile` | `cover.curtain` | |
| `switch.anbang_humidifier` | `tile` | `switch.gaseubgi` | |
| `scene.anbang_lighting_1` | `tile` | none | old scene not live |
| `scene.anbang_lighting_100` | `tile` | none | old scene not live |

## Recommended Safe Edit Order

1. Replace all confirmed lighting and sensor cards in the main `Home` view
2. Replace confirmed media and humidifier cards
3. Remove or defer cards with `none`
4. After the `Home` view is stable, apply the same replacements to the secondary `홈킷 뷰(Sections)` view

## Do Not Touch Yet

- Any card whose replacement is `none`
- Any old scene card
- Any thermostat card tied to `climate.anbang_heater`
- Any card whose old entity mapped to a split-device replacement unless the intended behavior is reviewed
