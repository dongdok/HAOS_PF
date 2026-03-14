# Anbang Display Name Cleanup v2

Last updated: 2026-03-03
Status: applied

## Scope

This batch covers the remaining awkward bedroom display names that are safe to improve without changing entity ids.

## Applied Renames

| Live Entity ID | Current Friendly Name | Proposed Display Name | Reason |
|---|---|---|---|
| `number.anbang_jaesilsenseo_sensitivity` | 안방 재실센서 | 안방 재실 감도 | current name hides the actual metric |
| `number.anbang_jaesilsenseo_near_detection` | 안방 재실센서 | 안방 재실 근거리 감지 | clearer metric labeling |
| `number.anbang_jaesilsenseo_far_detection` | 안방 재실센서 | 안방 재실 원거리 감지 | clearer metric labeling |
| `number.anbang_jaesilsenseo_closest_target_distance` | 안방 재실센서 | 안방 재실 최근접 거리 | clearer metric labeling |
| `number.anbang_bedside_presence_sensitivity` | 안방 머리맡 재실센서 | 안방 침대 재실 감도 | clearer metric labeling |
| `number.anbang_bedside_presence_near_detection` | 안방 머리맡 재실센서 | 안방 침대 재실 근거리 감지 | clearer metric labeling |
| `number.anbang_bedside_presence_far_detection` | 안방 머리맡 재실센서 | 안방 침대 재실 원거리 감지 | clearer metric labeling |
| `switch.anbang_bedtime_virtual` | 안방 취침 가상 스위치 | 안방 취침 가상 스위치 | standardized helper naming |
| `switch.anbang_goodnight_virtual` | 안방 굿나잇 가상 스위치 | 안방 굿나잇 가상 스위치 | standardized helper naming |
| `switch.anbangjomyeong_1peo` | Anbangjomyeong 1peo | 안방 스탠드 조명 1% 보조 스위치 | removes English artifact and clarifies stand-light scope |
| `switch.anbangjomyeong_100peo` | Anbangjomyeong 100peo | 안방 스탠드 조명 100% 보조 스위치 | removes English artifact and clarifies stand-light scope |

## Notes

- This batch still does not change entity ids.
- The two `switch.anbangjomyeong_*` entities should eventually be reviewed to decide whether they are still needed once scenes are fully canonical.
