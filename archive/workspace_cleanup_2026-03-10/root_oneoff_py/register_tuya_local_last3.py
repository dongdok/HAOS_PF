import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv
from websocket import create_connection


FLOW = "/api/config/config_entries/flow"
PROTOCOL_CANDIDATES = [3.5, 3.4, 3.3, 3.2, 3.1]

DEVICES = [
    {
        "name": "거실 스탠드 조명 로컬",
        "device_id": "ebb3759728f9940ddcbfnw",
        "host": "192.168.10.149",
        "local_key": "S/Vg2[I=)}tBiFX6",
        "type_keywords": ["light", "rgb", "rgbw", "dimmer"],
        "verify_domains": ["light", "switch", "sensor"],
    },
    {
        "name": "옷방 제습기 로컬",
        "device_id": "ebfb316825b9952791aalv",
        "host": "192.168.10.134",
        "local_key": ";dnkYD|t|h{FP1}C",
        "type_keywords": ["dehumidifier", "humidifier", "dryer"],
        "verify_domains": ["humidifier", "fan", "switch", "sensor"],
    },
    {
        "name": "안방 침대 재실센서 로컬",
        "device_id": "eb2c31b500afe44eb0uuhz",
        "host": "192.168.10.140",
        "local_key": "E~ZYGt8bQ08dpRMe",
        "type_keywords": ["presence", "sensor", "mmwave", "motion"],
        "verify_domains": ["binary_sensor", "sensor", "number", "switch"],
    },
]


def post(base_url: str, token: str, path: str, payload: Dict[str, Any], timeout: int = 60) -> Tuple[int, Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.post(f"{base_url}{path}", headers=headers, json=payload, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}
    return resp.status_code, data


def get_entries(base_url: str, token: str) -> List[Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{base_url}/api/config/config_entries/entry", headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


def find_tuya_local_entry_id(base_url: str, token: str, title: str) -> Optional[str]:
    for entry in get_entries(base_url, token):
        if entry.get("domain") == "tuya_local" and entry.get("title") == title:
            return entry.get("entry_id")
    return None


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
    lowered = [(raw, raw.lower()) for raw in available]
    for kw in keywords:
        needle = kw.lower()
        for raw, low in lowered:
            if needle in low:
                return raw
    return available[0]


def verify_entities_for_entry(base_url: str, token: str, entry_id: str, verify_domains: List[str]) -> Dict[str, Any]:
    entities = ws_entity_registry(base_url, token)
    matched = [e for e in entities if e.get("config_entry_id") == entry_id]
    entity_ids = sorted(e["entity_id"] for e in matched)
    focused: List[str] = []
    for domain in verify_domains:
        focused.extend([eid for eid in entity_ids if eid.startswith(f"{domain}.")])
    return {
        "entity_count": len(entity_ids),
        "entity_ids": entity_ids,
        "verify_entities": sorted(set(focused)),
    }


def add_one_device(base_url: str, token: str, device: Dict[str, Any]) -> Dict[str, Any]:
    for proto in PROTOCOL_CANDIDATES:
        st, init_data = post(base_url, token, FLOW, {"handler": "tuya_local"})
        if st != 200 or "flow_id" not in init_data:
            return {"ok": False, "stage": "init", "detail": {"status": st, "data": init_data}}
        flow_id = init_data["flow_id"]

        st, setup_data = post(base_url, token, f"{FLOW}/{flow_id}", {"setup_mode": "manual"})
        if st != 200 or setup_data.get("step_id") != "local":
            return {"ok": False, "stage": "setup_mode", "protocol": proto, "detail": {"status": st, "data": setup_data}}

        st, local_data = post(
            base_url,
            token,
            f"{FLOW}/{flow_id}",
            {
                "device_id": device["device_id"],
                "host": device["host"],
                "local_key": device["local_key"],
                "protocol_version": proto,
                "poll_only": False,
                "device_cid": "",
            },
            timeout=90,
        )
        if st != 200:
            continue

        if local_data.get("type") == "abort":
            if local_data.get("reason") == "already_configured":
                entry_id = find_tuya_local_entry_id(base_url, token, device["name"])
                return {
                    "ok": True,
                    "already_configured": True,
                    "protocol": proto,
                    "entry_id": entry_id,
                    "detail": local_data,
                }
            continue

        if local_data.get("step_id") != "select_type":
            continue

        available_types = get_step_options(local_data, "type")
        if not available_types:
            continue

        selected_type = choose_device_type(available_types, device["type_keywords"])
        st, select_data = post(base_url, token, f"{FLOW}/{flow_id}", {"type": selected_type})
        if st != 200 or select_data.get("step_id") != "choose_entities":
            continue

        st, finish_data = post(base_url, token, f"{FLOW}/{flow_id}", {"name": device["name"]})
        if st == 200 and finish_data.get("type") == "create_entry":
            entry_id = finish_data.get("result", {}).get("entry_id")
            return {
                "ok": True,
                "protocol": proto,
                "selected_type": selected_type,
                "entry_id": entry_id,
                "title": finish_data.get("result", {}).get("title"),
            }

    return {"ok": False, "stage": "all_protocols_failed"}


def main() -> None:
    load_dotenv("/Users/dy/Desktop/HAOS_Control/.env")
    base_url = os.environ["HA_URL"].rstrip("/")
    token = os.environ["HA_TOKEN"].strip()

    results: Dict[str, Any] = {}

    for device in DEVICES:
        print(f"\n=== {device['name']} ===")
        result = add_one_device(base_url, token, device)
        if result.get("ok") and result.get("entry_id"):
            time.sleep(2)
            result["verify"] = verify_entities_for_entry(
                base_url,
                token,
                result["entry_id"],
                device["verify_domains"],
            )
        results[device["name"]] = result
        print(json.dumps(result, ensure_ascii=False, indent=2))

    out_path = "/Users/dy/Desktop/HAOS_Control/tuya_local_last3_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nSaved: {out_path}")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
