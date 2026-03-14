import re
import time
from pathlib import Path

import requests


FLOW = "/api/config/config_entries/options/flow"

TARGETS = [
    ("안방 가습기 플러그", "eb255dffb9d10e9457bbkb"),
    ("안방 전기장판 플러그", "eb2718100f510651a8w7hp"),
    ("거실 라인 조명 전원 스위치", "ebc941b918f2c7f446wr3i"),
    ("안방 히터 플러그", "eb1bbd99a961d6c8b2ye9x"),
    ("주방 드라이기 플러그", "eb61542c4c5afedc0f2fms"),
]


def load_env():
    text = Path("/Users/dy/Desktop/HAOS_Control/.env").read_text()
    url_match = re.search(r'HA_URL="([^"]+)"', text)
    token_match = re.search(r'HA_TOKEN="([\s\S]*?)"', text)
    if not url_match or not token_match:
        raise RuntimeError("HA_URL/HA_TOKEN not found in .env")
    return url_match.group(1), token_match.group(1).strip()


class HAClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: dict, timeout: int = 40):
        r = requests.post(
            f"{self.base_url}{path}",
            headers=self.headers,
            json=payload,
            timeout=timeout,
        )
        try:
            data = r.json()
        except Exception:
            data = {"raw": r.text}
        return r.status_code, data

    def delete(self, path: str, timeout: int = 15):
        return requests.delete(
            f"{self.base_url}{path}",
            headers=self.headers,
            timeout=timeout,
        )

    def current_localtuya_entry_id(self):
        r = requests.get(
            f"{self.base_url}/api/config/config_entries/entry",
            headers=self.headers,
            timeout=30,
        )
        r.raise_for_status()
        entries = r.json()
        local_entries = [e for e in entries if e.get("domain") == "localtuya"]
        if not local_entries:
            raise RuntimeError("No localtuya config entry found")
        local_entries.sort(
            key=lambda e: e.get("modified_at") or e.get("created_at") or 0,
            reverse=True,
        )
        return local_entries[0]["entry_id"]


def extract_dp(schema, target_dp):
    if not schema:
        return None
    options = schema[0].get("options", [])
    for opt in options:
        key = opt[0] if isinstance(opt, list) else opt
        if str(key).startswith(f"{target_dp} "):
            return key
    return None


def submit_sensor(client: HAClient, fid: str, dp: int, name: str, device_class: str, unit: str, scaling: float):
    status, data = client.post(f"{FLOW}/{fid}", {"platform_to_add": "sensor"})
    if status != 200 or "data_schema" not in data:
        return False, f"sensor schema failed: {status} {data}"
    dp_key = extract_dp(data["data_schema"], dp)
    if not dp_key:
        return False, f"dp{dp} not found"
    payload = {
        "id": dp_key,
        "friendly_name": name,
        "device_class": device_class,
        "unit_of_measurement": unit,
        "scaling": scaling,
    }
    status, data = client.post(f"{FLOW}/{fid}", payload)
    if status != 200:
        return False, f"dp{dp} submit failed: {status} {data}"
    return True, "ok"


def add_sensors_for_device(client: HAClient, entry_id: str, label: str, device_id: str):
    status, data = client.post(FLOW, {"handler": entry_id})
    if status != 200 or "flow_id" not in data:
        return False, f"flow init failed: {status} {data}"
    fid = data["flow_id"]
    try:
        status, data = client.post(f"{FLOW}/{fid}", {"action": "edit_device"})
        if status != 200:
            return False, f"edit_device failed: {status} {data}"

        status, data = client.post(f"{FLOW}/{fid}", {"selected_device": device_id})
        if status != 200 or data.get("step_id") != "configure_device":
            return False, f"select device failed: {status} {data}"

        keep_entities = []
        cfg_payload = {"add_entities": True}
        for field in data.get("data_schema", []):
            name = field.get("name")
            if name == "entities":
                for opt in field.get("options", []):
                    key = opt[0] if isinstance(opt, list) else opt
                    keep_entities.append(key)
                cfg_payload["entities"] = keep_entities
            elif name == "add_entities":
                continue
            elif "default" in field:
                cfg_payload[name] = field["default"]

        status, data = client.post(f"{FLOW}/{fid}", cfg_payload)
        if status != 200 or data.get("step_id") != "pick_entity_type":
            return False, f"add_entities entry failed: {status} {data}"

        ok, msg = submit_sensor(client, fid, 19, "Power", "power", "W", 0.1)
        if not ok:
            return False, msg
        ok, msg = submit_sensor(client, fid, 18, "Current", "current", "A", 0.001)
        if not ok:
            return False, msg
        ok, msg = submit_sensor(client, fid, 20, "Voltage", "voltage", "V", 0.1)
        if not ok:
            return False, msg

        status, data = client.post(f"{FLOW}/{fid}", {"no_additional_entities": True})
        if status not in (200, 404):
            return False, f"finalize failed: {status} {data}"
        return True, "ok"
    finally:
        try:
            client.delete(f"{FLOW}/{fid}")
        except Exception:
            pass


def main():
    base_url, token = load_env()
    client = HAClient(base_url, token)
    entry_id = client.current_localtuya_entry_id()
    print(f"entry_id={entry_id}")
    results = {}
    for label, device_id in TARGETS:
        print(f"\n=== {label} ===")
        ok, msg = add_sensors_for_device(client, entry_id, label, device_id)
        results[label] = {"ok": ok, "detail": msg}
        print(("SUCCESS" if ok else "FAIL"), msg)
        time.sleep(1.0)

    print("\n=== SUMMARY ===")
    total = len(results)
    success = sum(1 for v in results.values() if v["ok"])
    print(f"{success}/{total} success")
    for name, v in results.items():
        print(f"- {name}: {'OK' if v['ok'] else 'FAIL'} ({v['detail']})")


if __name__ == "__main__":
    main()
