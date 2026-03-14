import json
import os
import time
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv
from websocket import create_connection


FLOW = "/api/config/config_entries/flow"
PROTOCOL_CANDIDATES = [3.5, 3.4, 3.3, 3.2, 3.1]

DEVICE = {
    "name": "거실 스탠드 조명 로컬",
    "device_id": "ebb3759728f9940ddcbfnw",
    "host": "192.168.10.149",
    "local_key": "S/Vg2[I=)}tBiFX6",
    "type_keywords": ["light", "rgb", "rgbw", "dimmer"],
    "verify_domains": ["light", "switch", "sensor"],
}


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


def get_options(step_data: Dict[str, Any], field_name: str) -> List[str]:
    out: List[str] = []
    for field in step_data.get("data_schema", []):
        if field.get("name") != field_name:
            continue
        for opt in field.get("options", []):
            if isinstance(opt, list) and opt:
                out.append(str(opt[0]))
            else:
                out.append(str(opt))
    return out


def choose_device_type(available: List[str], keywords: List[str]) -> str:
    lowered = [(raw, raw.lower()) for raw in available]
    for kw in keywords:
        kw_l = kw.lower()
        for raw, low in lowered:
            if kw_l in low:
                return raw
    return available[0]


def find_entry_id(base_url: str, token: str, title: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{base_url}/api/config/config_entries/entry", headers=headers, timeout=30)
    r.raise_for_status()
    for entry in r.json():
        if entry.get("domain") == "tuya_local" and entry.get("title") == title:
            return entry.get("entry_id")
    return ""


def verify_entities(base_url: str, token: str, entry_id: str, verify_domains: List[str]) -> Dict[str, Any]:
    entities = ws_entity_registry(base_url, token)
    matched = [e for e in entities if e.get("config_entry_id") == entry_id]
    entity_ids = sorted(e["entity_id"] for e in matched)
    focused: List[str] = []
    for d in verify_domains:
        focused.extend([eid for eid in entity_ids if eid.startswith(f"{d}.")])
    return {"entity_count": len(entity_ids), "entity_ids": entity_ids, "verify_entities": sorted(focused)}


def main() -> None:
    load_dotenv("/Users/dy/Desktop/HAOS_Control/.env")
    base_url = os.environ["HA_URL"].rstrip("/")
    token = os.environ["HA_TOKEN"].strip()

    result: Dict[str, Any] = {"device": DEVICE["name"]}

    for proto in PROTOCOL_CANDIDATES:
        st, init_data = post(base_url, token, FLOW, {"handler": "tuya_local"})
        if st != 200 or "flow_id" not in init_data:
            result = {"ok": False, "stage": "init", "detail": {"status": st, "data": init_data}}
            continue

        fid = init_data["flow_id"]

        st, step2 = post(base_url, token, f"{FLOW}/{fid}", {"setup_mode": "manual"})
        if st != 200 or step2.get("step_id") != "local":
            result = {"ok": False, "stage": "setup_mode", "protocol": proto, "detail": {"status": st, "data": step2}}
            continue

        st, step3 = post(
            base_url,
            token,
            f"{FLOW}/{fid}",
            {
                "device_id": DEVICE["device_id"],
                "host": DEVICE["host"],
                "local_key": DEVICE["local_key"],
                "protocol_version": proto,
                "poll_only": False,
                "device_cid": "",
            },
            timeout=90,
        )
        if st != 200:
            result = {"ok": False, "stage": "local_connect", "protocol": proto, "detail": {"status": st, "data": step3}}
            continue

        if step3.get("type") == "abort":
            if step3.get("reason") == "already_configured":
                entry_id = find_entry_id(base_url, token, DEVICE["name"])
                result = {"ok": True, "already_configured": True, "protocol": proto, "entry_id": entry_id, "detail": step3}
                break
            result = {"ok": False, "stage": "abort", "protocol": proto, "detail": step3}
            continue

        if step3.get("step_id") != "select_type":
            result = {"ok": False, "stage": "select_type_missing", "protocol": proto, "detail": step3}
            continue

        types = get_options(step3, "type")
        if not types:
            result = {"ok": False, "stage": "no_type_options", "protocol": proto, "detail": step3}
            continue

        selected_type = choose_device_type(types, DEVICE["type_keywords"])
        st, step4 = post(base_url, token, f"{FLOW}/{fid}", {"type": selected_type})
        if st != 200 or step4.get("step_id") != "choose_entities":
            result = {"ok": False, "stage": "choose_entities", "protocol": proto, "selected_type": selected_type, "detail": step4}
            continue

        st, step5 = post(base_url, token, f"{FLOW}/{fid}", {"name": DEVICE["name"]})
        if st == 200 and step5.get("type") == "create_entry":
            created = step5.get("result", {})
            result = {
                "ok": True,
                "protocol": proto,
                "selected_type": selected_type,
                "entry_id": created.get("entry_id"),
                "title": created.get("title"),
            }
            break

        result = {"ok": False, "stage": "create_entry", "protocol": proto, "selected_type": selected_type, "detail": step5}

    if result.get("ok") and result.get("entry_id"):
        time.sleep(2)
        result["verify"] = verify_entities(base_url, token, result["entry_id"], DEVICE["verify_domains"])

    out_path = "/Users/dy/Desktop/HAOS_Control/tuya_local_stand_light_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
