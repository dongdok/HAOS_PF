import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv
from websocket import create_connection


DEVICES = [
    {
        "name": "안방 히터 로컬",
        "device_id": "eb5f5e9aeb0b9da957mxz8",
        "host": "192.168.10.132",
        "local_key": "{]d0*+?vpA7[dBqQ",
        "type_keywords": ["heater", "climate", "thermostat", "qn"],
        "verify_domains": ["climate", "switch"],
    },
    {
        "name": "옷방 제습기 로컬",
        "device_id": "ebfb316825b9952791aalv",
        "host": "192.168.10.134",
        "local_key": ";dnkYD|t|h{FP1}C",
        "type_keywords": ["dehumidifier", "humidifier", "dryer"],
        "verify_domains": ["humidifier", "switch"],
    },
    {
        "name": "거실 스탠드 조명 로컬",
        "device_id": "ebb3759728f9940ddcbfnw",
        "host": "192.168.10.149",
        "local_key": "S/Vg2[I=)}tBiFX6",
        "type_keywords": ["light", "rgb", "rgbw", "dimmer"],
        "verify_domains": ["light", "switch"],
    },
    {
        "name": "거실 라인 조명 로컬",
        "device_id": "ebee27682f30d815eawhqi",
        "host": "192.168.10.127",
        "local_key": "<QXZ0DOl/gJ>;lUz",
        "type_keywords": ["light", "rgb", "rgbw", "dimmer"],
        "verify_domains": ["light", "switch"],
    },
    {
        "name": "안방 침대 재실센서 로컬",
        "device_id": "eb2c31b500afe44eb0uuhz",
        "host": "192.168.10.140",
        "local_key": "E~ZYGt8bQ08dpRMe",
        "type_keywords": ["presence", "sensor", "mmwave", "motion"],
        "verify_domains": ["binary_sensor", "sensor"],
    },
]

FLOW = "/api/config/config_entries/flow"
PROTOCOL_CANDIDATES = [3.5, 3.4, 3.3]


def post(base_url: str, token: str, path: str, payload: Dict[str, Any], timeout: int = 60) -> Tuple[int, Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.post(f"{base_url}{path}", headers=headers, json=payload, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}
    return resp.status_code, data


def ws_entity_registry(base_url: str, token: str) -> List[Dict[str, Any]]:
    ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    ws = create_connection(ws_url, timeout=20)
    ws.recv()
    ws.send(json.dumps({"type": "auth", "access_token": token}))
    ws.recv()
    ws.send(json.dumps({"id": 1, "type": "config/entity_registry/list"}))
    msg = json.loads(ws.recv())
    ws.close()
    return msg.get("result", [])


def get_step_options(step_data: Dict[str, Any], field_name: str) -> List[str]:
    options: List[str] = []
    for field in step_data.get("data_schema", []):
        if field.get("name") != field_name:
            continue
        for opt in field.get("options", []):
            if isinstance(opt, list) and opt:
                options.append(str(opt[0]))
            else:
                options.append(str(opt))
    return options


def choose_device_type(available: List[str], keywords: List[str]) -> str:
    lowered = [(opt, opt.lower()) for opt in available]
    for kw in keywords:
        kw_l = kw.lower()
        for raw, low in lowered:
            if kw_l in low:
                return raw
    return available[0]


def add_one_device(base_url: str, token: str, device: Dict[str, Any]) -> Dict[str, Any]:
    for proto in PROTOCOL_CANDIDATES:
        st, init_data = post(base_url, token, FLOW, {"handler": "tuya_local"})
        if st != 200 or "flow_id" not in init_data:
            return {"ok": False, "stage": "init", "detail": f"{st} {init_data}"}
        fid = init_data["flow_id"]

        st, setup_data = post(base_url, token, f"{FLOW}/{fid}", {"setup_mode": "manual"})
        if st != 200 or setup_data.get("step_id") != "local":
            return {"ok": False, "stage": "setup_mode", "detail": f"{st} {setup_data}"}

        payload_local = {
            "device_id": device["device_id"],
            "host": device["host"],
            "local_key": device["local_key"],
            "protocol_version": proto,
            "poll_only": False,
            "device_cid": "",
        }
        st, local_data = post(base_url, token, f"{FLOW}/{fid}", payload_local, timeout=90)

        if st != 200:
            continue
        if local_data.get("type") == "abort":
            reason = local_data.get("reason")
            if reason == "already_configured":
                return {"ok": True, "already_configured": True, "protocol": proto, "detail": local_data}
            return {"ok": False, "stage": "local_abort", "protocol": proto, "detail": local_data}
        if local_data.get("step_id") != "select_type":
            continue

        available_types = get_step_options(local_data, "type")
        if not available_types:
            return {"ok": False, "stage": "select_type_options", "protocol": proto, "detail": local_data}

        selected_type = choose_device_type(available_types, device["type_keywords"])
        st, select_data = post(base_url, token, f"{FLOW}/{fid}", {"type": selected_type})
        if st != 200 or select_data.get("step_id") != "choose_entities":
            continue

        st, finish_data = post(base_url, token, f"{FLOW}/{fid}", {"name": device["name"]})
        if st == 200 and finish_data.get("type") == "create_entry":
            result = finish_data.get("result", {})
            return {
                "ok": True,
                "protocol": proto,
                "selected_type": selected_type,
                "entry_id": result.get("entry_id"),
                "title": result.get("title"),
            }

    return {"ok": False, "stage": "all_protocols_failed"}


def find_entry_id(base_url: str, token: str, title: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{base_url}/api/config/config_entries/entry", headers=headers, timeout=30)
    if r.status_code != 200:
        return None
    for entry in r.json():
        if entry.get("domain") == "tuya_local" and entry.get("title") == title:
            return entry.get("entry_id")
    return None


def verify_entities_for_entry(base_url: str, token: str, entry_id: str, verify_domains: List[str]) -> Dict[str, Any]:
    entities = ws_entity_registry(base_url, token)
    matched = [e for e in entities if e.get("config_entry_id") == entry_id]
    entity_ids = [e["entity_id"] for e in matched]
    verify_ids = []
    for domain in verify_domains:
        verify_ids.extend([eid for eid in entity_ids if eid.startswith(f"{domain}.")])
    return {
        "entity_count": len(entity_ids),
        "entity_ids": sorted(entity_ids),
        "verify_entities": sorted(verify_ids),
    }


def main():
    load_dotenv("/Users/dy/Desktop/HAOS_Control/.env")
    base_url = os.environ["HA_URL"].rstrip("/")
    token = os.environ["HA_TOKEN"].strip()

    all_results: Dict[str, Any] = {}

    for dev in DEVICES:
        print(f"\n=== {dev['name']} ===")
        result = add_one_device(base_url, token, dev)
        all_results[dev["name"]] = result
        print(result)

        if not result.get("ok"):
            continue

        entry_id = result.get("entry_id")
        if not entry_id:
            entry_id = find_entry_id(base_url, token, dev["name"])
            if entry_id:
                result["entry_id"] = entry_id

        if not entry_id:
            continue

        # Wait briefly for entity registry population.
        time.sleep(2)
        verify = verify_entities_for_entry(base_url, token, entry_id, dev["verify_domains"])
        all_results[dev["name"]]["verify"] = verify

    out_path = "/Users/dy/Desktop/HAOS_Control/tuya_local_remaining_5_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")
    print(json.dumps(all_results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
