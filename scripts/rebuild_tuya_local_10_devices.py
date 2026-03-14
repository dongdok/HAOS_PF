import json
import os
import time
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException


FLOW = "/api/config/config_entries/flow"
OUT_PATH = "/Users/dy/Desktop/HAOS_Control/tuya_local_rebuild_10_results.json"

DEVICES: List[Dict[str, Any]] = [
    {
        "name": "안방 가습기 플러그 로컬",
        "device_id": "eb255dffb9d10e9457bbkb",
        "host": "192.168.10.123",
        "local_key": "':N`/$H-5$|Us;r6",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["smartplug", "plug", "outlet", "energy", "switch"],
    },
    {
        "name": "안방 전기장판 플러그 로컬",
        "device_id": "eb2718100f510651a8w7hp",
        "host": "192.168.10.100",
        "local_key": "*TWq#A{Ww@!{y?g)",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["smartplug", "plug", "outlet", "energy", "switch"],
    },
    {
        "name": "거실 라인 조명 전원 스위치 로컬",
        "device_id": "ebc941b918f2c7f446wr3i",
        "host": "192.168.10.128",
        "local_key": "[5tC~6YSNrkbmP|B",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["smartplug", "plug", "outlet", "energy", "switch"],
    },
    {
        "name": "안방 히터 플러그 로컬",
        "device_id": "eb1bbd99a961d6c8b2ye9x",
        "host": "192.168.10.126",
        "local_key": ")K'o*Y<^lCB.JGJ0",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["smartplug", "plug", "outlet", "energy", "switch"],
    },
    {
        "name": "주방 드라이기 플러그 로컬",
        "device_id": "eb61542c4c5afedc0f2fms",
        "host": "192.168.10.125",
        "local_key": "Qrc36^V(dr>9nyS0",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["smartplug", "plug", "outlet", "energy", "switch"],
    },
    {
        "name": "주방 천장 조명 로컬",
        "device_id": "eb18aea49204ba56d2p7aa",
        "host": "192.168.10.137",
        "local_key": "By7lywL'x0U{TZ-*",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["switch", "light", "dimmer"],
    },
    {
        "name": "거실 천장 조명 로컬",
        "device_id": "eb8bc6087a894602b34lta",
        "host": "192.168.10.130",
        "local_key": "F=RN'$?2E|oV4i9R",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["switch", "light", "dimmer"],
    },
    {
        "name": "옷방 천장 조명 로컬",
        "device_id": "ebeaabe539499a6f57gd3b",
        "host": "192.168.10.133",
        "local_key": ".fwCPhX2uoBM|MK'",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["switch", "light", "dimmer"],
    },
    {
        "name": "안방 천장 조명 로컬",
        "device_id": "ebc2b3c045bd0fe191dm6v",
        "host": "192.168.10.129",
        "local_key": "smN4xu8L|]q(UQ+;",
        "protocols": [3.3, "auto", 3.4, 3.5],
        "type_keywords": ["switch", "light", "dimmer"],
    },
    {
        "name": "거실 스탠드 조명 로컬",
        "device_id": "ebb3759728f9940ddcbfnw",
        "host": "192.168.10.149",
        "local_key": "S/Vg2[I=)}tBiFX6",
        "protocols": [3.5, "auto", 3.4, 3.3],
        "type_keywords": ["light", "rgb", "rgbw", "dimmer", "switch"],
    },
]


def post(base_url: str, token: str, path: str, payload: Dict[str, Any], timeout: int = 60) -> Tuple[int, Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    last_err: str = ""
    for attempt in range(3):
        try:
            r = requests.post(f"{base_url}{path}", headers=headers, json=payload, timeout=timeout)
            try:
                data = r.json()
            except Exception:
                data = {"raw": r.text}
            return r.status_code, data
        except RequestException as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt < 2:
                time.sleep(1.0 + attempt)
                continue
    return 599, {"error": "request_exception", "detail": last_err}


def get_type_options(step_data: Dict[str, Any]) -> List[str]:
    for f in step_data.get("data_schema", []):
        if f.get("name") != "type":
            continue
        out: List[str] = []
        for opt in f.get("options", []):
            out.append(str(opt[0] if isinstance(opt, list) else opt))
        return out
    return []


def choose_type(options: List[str], keywords: List[str]) -> str:
    lowered = [(o, o.lower()) for o in options]
    for kw in keywords:
        k = kw.lower()
        for raw, low in lowered:
            if k in low:
                return raw
    return options[0]


def add_device(base_url: str, token: str, dev: Dict[str, Any]) -> Dict[str, Any]:
    for proto in dev["protocols"]:
        st, d = post(base_url, token, FLOW, {"handler": "tuya_local"})
        if st != 200 or "flow_id" not in d:
            return {"ok": False, "stage": "init", "status": st, "detail": d}
        fid = d["flow_id"]

        st, d = post(base_url, token, f"{FLOW}/{fid}", {"setup_mode": "manual"})
        if st != 200 or d.get("step_id") != "local":
            return {"ok": False, "stage": "setup_mode", "status": st, "detail": d, "protocol": proto}

        st, d = post(
            base_url,
            token,
            f"{FLOW}/{fid}",
            {
                "device_id": dev["device_id"],
                "host": dev["host"],
                "local_key": dev["local_key"],
                "protocol_version": proto,
                "poll_only": False,
                "device_cid": "",
            },
            timeout=30,
        )
        if st != 200:
            continue

        if d.get("type") == "abort":
            if d.get("reason") == "already_configured":
                return {"ok": True, "already_configured": True, "protocol": proto, "detail": d}
            return {"ok": False, "stage": "abort", "protocol": proto, "detail": d}

        if d.get("step_id") != "select_type":
            if d.get("errors"):
                continue
            return {"ok": False, "stage": "select_type_missing", "protocol": proto, "detail": d}

        options = get_type_options(d)
        if not options:
            return {"ok": False, "stage": "no_type_options", "protocol": proto, "detail": d}

        selected = choose_type(options, dev["type_keywords"])
        st, d = post(base_url, token, f"{FLOW}/{fid}", {"type": selected})
        if st != 200 or d.get("step_id") != "choose_entities":
            continue

        st, d = post(base_url, token, f"{FLOW}/{fid}", {"name": dev["name"]})
        if st == 200 and d.get("type") == "create_entry":
            return {
                "ok": True,
                "protocol": proto,
                "selected_type": selected,
                "entry_id": d.get("result", {}).get("entry_id"),
                "title": d.get("result", {}).get("title"),
            }

    return {"ok": False, "stage": "all_protocols_failed"}


def main() -> None:
    load_dotenv("/Users/dy/Desktop/HAOS_Control/.env")
    base_url = os.environ["HA_URL"].rstrip("/")
    token = os.environ["HA_TOKEN"].strip()

    results: Dict[str, Any] = {}
    for dev in DEVICES:
        print(f"\n=== {dev['name']} ===")
        try:
            r = add_device(base_url, token, dev)
        except Exception as e:
            r = {"ok": False, "stage": "exception", "detail": f"{type(e).__name__}: {e}"}
        results[dev["name"]] = r
        print(json.dumps(r, ensure_ascii=False))
        time.sleep(0.5)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {OUT_PATH}")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
