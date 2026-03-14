import json
import re
from pathlib import Path
from typing import Any, Dict, Tuple

import requests


ENV_PATH = "/Users/dy/Desktop/HAOS_Control/.env"
OUT_PATH = "/Users/dy/Desktop/HAOS_Control/tuya_local_add_anbang_heater_plug_result.json"
FLOW = "/api/config/config_entries/flow"

DEVICE = {
    "name": "안방 히터 플러그 로컬",
    "device_id": "eb1bbd99a961d6c8b2ye9x",
    "host": "192.168.10.126",
    "local_key": ")K'o*Y<^lCB.JGJ0",
    "protocols": [3.5, 3.4, 3.3, 3.2, 3.1, "auto"],
}


def load_env(path: str) -> Tuple[str, str]:
    text = Path(path).read_text(encoding="utf-8")
    url = re.search(r'HA_URL="([^"]+)"', text)
    token = re.search(r'HA_TOKEN="([\s\S]*?)"', text)
    if not url or not token:
        raise RuntimeError("HA_URL/HA_TOKEN not found in .env")
    return url.group(1).rstrip("/"), token.group(1).strip()


def post(base_url: str, token: str, path: str, payload: Dict[str, Any], timeout: int = 60):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    resp = requests.post(f"{base_url}{path}", headers=headers, json=payload, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}
    return resp.status_code, data


def list_tuya_local_entries(base_url: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{base_url}/api/config/config_entries/entry", headers=headers, timeout=30)
    r.raise_for_status()
    entries = r.json()
    return [
        {k: e.get(k) for k in ("entry_id", "domain", "title", "state")}
        for e in entries
        if e.get("domain") == "tuya_local"
    ]


def run() -> Dict[str, Any]:
    base_url, token = load_env(ENV_PATH)
    result: Dict[str, Any] = {"device_id": DEVICE["device_id"], "attempts": []}

    for proto in DEVICE["protocols"]:
        attempt: Dict[str, Any] = {"protocol": proto}

        st, init_data = post(base_url, token, FLOW, {"handler": "tuya_local"})
        attempt["init_status"] = st
        if st != 200 or "flow_id" not in init_data:
            attempt["result"] = {"stage": "init", "detail": init_data}
            result["attempts"].append(attempt)
            continue

        flow_id = init_data["flow_id"]

        st, setup_data = post(base_url, token, f"{FLOW}/{flow_id}", {"setup_mode": "manual"})
        attempt["setup_status"] = st
        if st != 200:
            attempt["result"] = {"stage": "setup_mode", "detail": setup_data}
            result["attempts"].append(attempt)
            continue

        payload = {
            "device_id": DEVICE["device_id"],
            "host": DEVICE["host"],
            "local_key": DEVICE["local_key"],
            "protocol_version": proto,
            "poll_only": False,
            "device_cid": "",
        }
        st, local_data = post(base_url, token, f"{FLOW}/{flow_id}", payload, timeout=90)
        attempt["local_status"] = st
        attempt["local_type"] = local_data.get("type")
        attempt["local_step"] = local_data.get("step_id")

        if local_data.get("type") == "abort":
            attempt["result"] = {
                "stage": "abort",
                "reason": local_data.get("reason"),
                "detail": local_data,
            }
            result["attempts"].append(attempt)
            if local_data.get("reason") == "already_configured":
                result["final"] = "already_configured"
                break
            continue

        if st != 200 or local_data.get("step_id") != "select_type":
            attempt["result"] = {"stage": "local", "detail": local_data}
            result["attempts"].append(attempt)
            continue

        options = []
        for field in local_data.get("data_schema", []):
            if field.get("name") != "type":
                continue
            for opt in field.get("options", []):
                options.append(str(opt[0] if isinstance(opt, list) else opt))
        attempt["type_options"] = options

        selected = None
        for needle in ("smartplugv2_energy", "smartplugv2", "smartplug", "switch"):
            for opt in options:
                if needle in opt.lower():
                    selected = opt
                    break
            if selected:
                break
        if not selected and options:
            selected = options[0]
        if not selected:
            attempt["result"] = {"stage": "select_type", "detail": "no type options"}
            result["attempts"].append(attempt)
            continue

        st, type_data = post(base_url, token, f"{FLOW}/{flow_id}", {"type": selected})
        attempt["choose_type_status"] = st
        attempt["selected_type"] = selected
        if st != 200 or type_data.get("step_id") != "choose_entities":
            attempt["result"] = {"stage": "choose_type", "detail": type_data}
            result["attempts"].append(attempt)
            continue

        st, finish_data = post(base_url, token, f"{FLOW}/{flow_id}", {"name": DEVICE["name"]})
        attempt["finish_status"] = st
        if st == 200 and finish_data.get("type") == "create_entry":
            result["final"] = "created"
            result["entry_id"] = finish_data.get("result", {}).get("entry_id")
            attempt["result"] = {"stage": "success", "detail": finish_data}
            result["attempts"].append(attempt)
            break

        attempt["result"] = {"stage": "finish", "detail": finish_data}
        result["attempts"].append(attempt)

    if "final" not in result:
        result["final"] = "failed"

    result["tuya_local_entries"] = list_tuya_local_entries(base_url, token)
    return result


if __name__ == "__main__":
    out = run()
    Path(OUT_PATH).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\nSaved: {OUT_PATH}")
