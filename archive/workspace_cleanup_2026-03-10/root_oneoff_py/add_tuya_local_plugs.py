import os
import json
import time
from typing import Dict, Any, Optional

import requests
from dotenv import load_dotenv
from websocket import create_connection


PLUGS = [
    {
        "name": "안방 가습기 플러그 로컬",
        "device_id": "eb255dffb9d10e9457bbkb",
        "host": "192.168.10.123",
        "local_key": "':N`/$H-5$|Us;r6",
    },
    {
        "name": "안방 전기장판 플러그 로컬",
        "device_id": "eb2718100f510651a8w7hp",
        "host": "192.168.10.100",
        "local_key": "*TWq#A{Ww@!{y?g)",
    },
    {
        "name": "거실 라인 조명 전원 스위치 로컬",
        "device_id": "ebc941b918f2c7f446wr3i",
        "host": "192.168.10.128",
        "local_key": "[5tC~6YSNrkbmP|B",
    },
    {
        "name": "주방 드라이기 플러그 로컬",
        "device_id": "eb61542c4c5afedc0f2fms",
        "host": "192.168.10.125",
        "local_key": "Qrc36^V(dr>9nyS0",
    },
]


def ws_entity_registry(base_url: str, token: str):
    ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    ws = create_connection(ws_url, timeout=20)
    ws.recv()
    ws.send(json.dumps({"type": "auth", "access_token": token}))
    ws.recv()
    ws.send(json.dumps({"id": 1, "type": "config/entity_registry/list"}))
    msg = json.loads(ws.recv())
    ws.close()
    return msg.get("result", [])


def post(base_url: str, token: str, path: str, payload: Dict[str, Any], timeout: int = 45):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(f"{base_url}{path}", headers=headers, json=payload, timeout=timeout)
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}
    return r.status_code, data


def add_device(base_url: str, token: str, plug: Dict[str, str]) -> Dict[str, Any]:
    flow = "/api/config/config_entries/flow"

    st, d = post(base_url, token, flow, {"handler": "tuya_local"})
    if st != 200 or "flow_id" not in d:
        return {"ok": False, "stage": "init", "detail": f"{st} {d}"}
    fid = d["flow_id"]

    st, d = post(base_url, token, f"{flow}/{fid}", {"setup_mode": "manual"})
    if st != 200 or d.get("step_id") != "local":
        return {"ok": False, "stage": "setup_mode", "detail": f"{st} {d}"}

    payload_local = {
        "device_id": plug["device_id"],
        "host": plug["host"],
        "local_key": plug["local_key"],
        "protocol_version": 3.5,
        "poll_only": False,
        "device_cid": "",
    }
    st, d = post(base_url, token, f"{flow}/{fid}", payload_local, timeout=80)
    if st != 200 or d.get("step_id") != "select_type":
        return {"ok": False, "stage": "local", "detail": f"{st} {d}"}

    st, d = post(base_url, token, f"{flow}/{fid}", {"type": "smartplugv2_energy"})
    if st != 200 or d.get("step_id") != "choose_entities":
        return {"ok": False, "stage": "select_type", "detail": f"{st} {d}"}

    st, d = post(base_url, token, f"{flow}/{fid}", {"name": plug["name"]})
    if st != 200 or d.get("type") != "create_entry":
        return {"ok": False, "stage": "choose_entities", "detail": f"{st} {d}"}

    result = d.get("result", {})
    return {
        "ok": True,
        "entry_id": result.get("entry_id"),
        "title": result.get("title"),
    }


def find_switch_entity_for_entry(base_url: str, token: str, entry_id: str) -> Optional[str]:
    entities = ws_entity_registry(base_url, token)
    candidates = [e for e in entities if e.get("config_entry_id") == entry_id and e["entity_id"].startswith("switch.")]
    if not candidates:
        return None
    # main switch is usually the shortest and without suffix entity purpose words
    candidates.sort(key=lambda e: len(e["entity_id"]))
    return candidates[0]["entity_id"]


def call_service(base_url: str, token: str, domain: str, service: str, entity_id: str):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(
        f"{base_url}/api/services/{domain}/{service}",
        headers=headers,
        json={"entity_id": entity_id},
        timeout=20,
    )
    return r.status_code


def get_state(base_url: str, token: str, entity_id: str) -> str:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.get(f"{base_url}/api/states/{entity_id}", headers=headers, timeout=20)
    if r.status_code != 200:
        return f"error:{r.status_code}"
    return r.json().get("state", "unknown")


def main():
    load_dotenv("/Users/dy/Desktop/HAOS_Control/.env")
    base_url = os.environ["HA_URL"].rstrip("/")
    token = os.environ["HA_TOKEN"].strip()

    results = {}
    for plug in PLUGS:
        print(f"\n=== {plug['name']} ===")
        add_result = add_device(base_url, token, plug)
        if not add_result["ok"]:
            print("FAIL", add_result)
            results[plug["name"]] = {"ok": False, **add_result}
            continue

        entry_id = add_result["entry_id"]
        # allow entity registry to refresh
        time.sleep(2)
        switch_eid = find_switch_entity_for_entry(base_url, token, entry_id)
        if not switch_eid:
            print("WARN: switch entity not found")
            results[plug["name"]] = {
                "ok": True,
                "entry_id": entry_id,
                "switch_entity": None,
                "verify": "not_checked",
            }
            continue

        on_code = call_service(base_url, token, "switch", "turn_on", switch_eid)
        time.sleep(2)
        on_state = get_state(base_url, token, switch_eid)
        off_code = call_service(base_url, token, "switch", "turn_off", switch_eid)
        time.sleep(2)
        off_state = get_state(base_url, token, switch_eid)

        verified = on_code == 200 and off_code == 200 and on_state == "on" and off_state == "off"
        print(f"entry={entry_id} switch={switch_eid} verify={'PASS' if verified else 'FAIL'}")

        results[plug["name"]] = {
            "ok": True,
            "entry_id": entry_id,
            "switch_entity": switch_eid,
            "verify": "PASS" if verified else "FAIL",
            "on_state": on_state,
            "off_state": off_state,
            "on_code": on_code,
            "off_code": off_code,
        }

    out = "/Users/dy/Desktop/HAOS_Control/tuya_local_add_results.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nSaved:", out)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
