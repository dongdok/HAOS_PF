import re
import time
from pathlib import Path

import requests


FLOW = "/api/config/config_entries/options/flow"
MANUAL_DPS = "1,9,17,18,19,20,21,22,23,24,25,26,38,39,41,42,43,44"

PLUGS = [
    {
        "friendly_name": "안방 가습기 플러그",
        "device_id": "eb255dffb9d10e9457bbkb",
        "host": "192.168.10.123",
        "local_key": "':N`/$H-5$|Us;r6",
    },
    {
        "friendly_name": "안방 전기장판 플러그",
        "device_id": "eb2718100f510651a8w7hp",
        "host": "192.168.10.100",
        "local_key": "*TWq#A{Ww@!{y?g)",
    },
    {
        "friendly_name": "거실 라인 조명 전원 스위치",
        "device_id": "ebc941b918f2c7f446wr3i",
        "host": "192.168.10.128",
        "local_key": "[5tC~6YSNrkbmP|B",
    },
    {
        "friendly_name": "안방 히터 플러그",
        "device_id": "eb1bbd99a961d6c8b2ye9x",
        "host": "192.168.10.126",
        "local_key": ")K'o*Y<^lCB.JGJ0",
    },
    {
        "friendly_name": "주방 드라이기 플러그",
        "device_id": "eb61542c4c5afedc0f2fms",
        "host": "192.168.10.125",
        "local_key": "Qrc36^V(dr>9nyS0",
    },
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
        # Pick newest entry by modified_at/created_at
        local_entries.sort(
            key=lambda e: e.get("modified_at") or e.get("created_at") or 0,
            reverse=True,
        )
        return local_entries[0]["entry_id"]


def extract_dp1(schema):
    if not schema:
        return None
    options = schema[0].get("options", [])
    for opt in options:
        if isinstance(opt, list) and opt and str(opt[0]).startswith("1 "):
            return opt[0]
        if isinstance(opt, str) and opt.startswith("1 "):
            return opt
    return None


def add_plug_switch(client: HAClient, entry_id: str, plug: dict):
    status, data = client.post(FLOW, {"handler": entry_id})
    if status != 200 or "flow_id" not in data:
        return False, f"flow init failed: {status} {data}"
    fid = data["flow_id"]

    try:
        status, data = client.post(f"{FLOW}/{fid}", {"action": "add_device"})
        if status != 200:
            return False, f"add_device step failed: {status} {data}"

        # Always select manual input row ("...")
        status, data = client.post(f"{FLOW}/{fid}", {"selected_device": "..."})
        if status != 200:
            return False, f"manual select failed: {status} {data}"

        auth_payload = {
            "friendly_name": plug["friendly_name"],
            "host": plug["host"],
            "device_id": plug["device_id"],
            "local_key": plug["local_key"],
            "protocol_version": "3.4",
            "enable_debug": False,
            "manual_dps_strings": MANUAL_DPS,
        }
        status, data = client.post(f"{FLOW}/{fid}", auth_payload)
        if status == 400 and data.get("errors"):
            # fallback
            auth_payload["protocol_version"] = "3.3"
            status, data = client.post(f"{FLOW}/{fid}", auth_payload)
        if status == 400 and data.get("errors"):
            return False, f"auth failed: {data.get('errors')}"
        if status != 200 or data.get("step_id") != "pick_entity_type":
            return False, f"unexpected after auth: {status} {data}"

        status, data = client.post(f"{FLOW}/{fid}", {"platform_to_add": "switch"})
        if status != 200 or "data_schema" not in data:
            return False, f"switch schema failed: {status} {data}"

        dp1 = extract_dp1(data["data_schema"])
        if not dp1:
            return False, "dp1 not found"

        status, data = client.post(
            f"{FLOW}/{fid}",
            {
                "id": dp1,
                "friendly_name": "",
                "restore_on_reconnect": False,
                "is_passive_entity": False,
            },
        )
        if status != 200:
            return False, f"switch submit failed: {status} {data}"

        # Finish flow. Some HA builds return 404 here because flow auto-closes; treat as success.
        status, data = client.post(f"{FLOW}/{fid}", {"no_additional_entities": True})
        if status not in (200, 404):
            return False, f"flow finalize failed: {status} {data}"

        return True, "ok"
    finally:
        # Cleanup best effort
        try:
            client.delete(f"{FLOW}/{fid}")
        except Exception:
            pass


def main():
    base_url, token = load_env()
    client = HAClient(base_url, token)
    entry_id = client.current_localtuya_entry_id()
    results = {}

    for plug in PLUGS:
        name = plug["friendly_name"]
        print(f"\n=== {name} ({plug['host']}) ===")
        ok, msg = add_plug_switch(client, entry_id, plug)
        results[name] = {"ok": ok, "detail": msg}
        print(("SUCCESS" if ok else "FAIL"), msg)
        time.sleep(1.5)

    print("\n=== SUMMARY ===")
    success = sum(1 for v in results.values() if v["ok"])
    total = len(results)
    print(f"{success}/{total} success")
    for k, v in results.items():
        print(f"- {k}: {'OK' if v['ok'] else 'FAIL'} ({v['detail']})")


if __name__ == "__main__":
    main()
