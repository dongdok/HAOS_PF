import json
import os
from typing import Any, Dict, Tuple

import requests
from dotenv import load_dotenv


FLOW = "/api/config/config_entries/flow"
OUT_PATH = "/Users/dy/Desktop/HAOS_Control/tuya_local_geosil_stand_diagnose.json"

TARGET = {
    "device_id": "ebb3759728f9940ddcbfnw",
    "host": "192.168.10.149",
    "local_key": "S/Vg2[I=)}tBiFX6",
    "protocol_version": 3.5,
}


def post(base_url: str, token: str, path: str, payload: Dict[str, Any], timeout: int = 60) -> Tuple[int, Dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(f"{base_url}{path}", headers=headers, json=payload, timeout=timeout)
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}
    return r.status_code, data


def test_manual_flow(base_url: str, token: str, payload: Dict[str, Any], timeout: int = 90) -> Dict[str, Any]:
    st, init_data = post(base_url, token, FLOW, {"handler": "tuya_local"})
    if st != 200 or "flow_id" not in init_data:
        return {"ok": False, "stage": "init", "status": st, "data": init_data}

    fid = init_data["flow_id"]
    st, local_form = post(base_url, token, f"{FLOW}/{fid}", {"setup_mode": "manual"})
    if st != 200:
        return {"ok": False, "stage": "setup_mode", "status": st, "data": local_form, "flow_id": fid}

    st, submit = post(base_url, token, f"{FLOW}/{fid}", payload, timeout=timeout)
    return {
        "ok": st == 200 and submit.get("type") != "abort",
        "stage": "submit_local",
        "status": st,
        "flow_id": fid,
        "response_type": submit.get("type"),
        "step_id": submit.get("step_id"),
        "reason": submit.get("reason"),
        "errors": submit.get("errors"),
        "submit_response": submit,
    }


def main() -> None:
    load_dotenv("/Users/dy/Desktop/HAOS_Control/.env")
    base_url = os.environ["HA_URL"].rstrip("/")
    token = os.environ["HA_TOKEN"].strip()

    tests = []

    tests.append(
        {
            "name": "target_payload",
            "payload": {
                "device_id": TARGET["device_id"],
                "host": TARGET["host"],
                "local_key": TARGET["local_key"],
                "protocol_version": TARGET["protocol_version"],
                "poll_only": False,
                "device_cid": "",
            },
        }
    )

    tests.append(
        {
            "name": "fake_device_same_host",
            "payload": {
                "device_id": "xxyyzz00112233445566aa",
                "host": TARGET["host"],
                "local_key": TARGET["local_key"],
                "protocol_version": TARGET["protocol_version"],
                "poll_only": False,
                "device_cid": "",
            },
        }
    )

    tests.append(
        {
            "name": "fake_device_bad_host",
            "payload": {
                "device_id": "xxyyzz00112233445566aa",
                "host": "192.168.10.150",
                "local_key": TARGET["local_key"],
                "protocol_version": TARGET["protocol_version"],
                "poll_only": False,
                "device_cid": "",
            },
        }
    )

    result = {"target": TARGET, "results": []}
    for t in tests:
        try:
            r = test_manual_flow(base_url, token, t["payload"])
        except Exception as e:
            r = {"ok": False, "stage": "exception", "error": f"{type(e).__name__}: {e}"}
        result["results"].append({"name": t["name"], "result": r})

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
