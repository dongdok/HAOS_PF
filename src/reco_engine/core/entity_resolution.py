from __future__ import annotations


REPRESENTATIVE_ENTITY_MAP = {
    # Treat the humidifier power switch as an implementation detail of the same device.
    "switch.osbang_jeseubgi_jeonweon_rokeol": "humidifier.osbang_jeseubgi_rokeol_naebuseubdo",
    # Resolve script proxies to their primary controlled entities for user-facing summaries.
    "script.cmd_switch_anbang_ceiling_light_off": "switch.anbang_ceiling_light",
    "script.gasang_anbang_gusnais_on": "input_boolean.gasang_anbang_gusnais",
}

SHADOW_ENTITY_IDS = {
    # Internal power layer: keep available for control, exclude from recommendation scoring/view.
    "switch.osbang_jeseubgi_jeonweon_rokeol",
}


DISPLAY_NAME_MAP = {
    "script.apply_solar_color_temp": "공용 태양 기반 색온도 적용",
    "humidifier.osbang_jeseubgi_rokeol_naebuseubdo": "옷방 제습기",
    "input_boolean.gasang_hwajangsil": "화장실 가상 스위치",
    "switch.hwajangsil_vent_fan": "화장실 환풍기",
    "switch.jubang_line_lighting_plug": "주방 라인 조명 플러그",
    "switch.osbang_ceiling_light": "옷방 천장 조명",
    "switch.hwajangsil_ceiling_light": "화장실 천장 조명",
    "switch.jubang_ceiling_light": "주방 천장 조명",
    "switch.anbang_ceiling_light": "안방 천장 조명",
    "input_boolean.gasang_anbang_gusnais": "안방 굿나잇",
    "switch.geosil_ceiling_light": "거실 천장 조명",
    "light.geosil_keoteun_rain_jomyeong_rokeol": "거실 라인 조명",
    "switch.jubang_deuraigi_peulreogeu_rokeol": "주방 드라이기 플러그",
}


def representative_entity_id(entity_id: str) -> str:
    return REPRESENTATIVE_ENTITY_MAP.get(entity_id, entity_id)


def display_entity_name(entity_id: str) -> str:
    resolved = representative_entity_id(entity_id)
    return DISPLAY_NAME_MAP.get(resolved, resolved)


def is_shadow_entity(entity_id: str) -> bool:
    return entity_id in SHADOW_ENTITY_IDS
