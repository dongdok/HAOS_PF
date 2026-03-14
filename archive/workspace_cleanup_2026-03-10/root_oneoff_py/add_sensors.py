"""
Add sensors to 3 existing LocalTuya plug devices via edit_device Options Flow.
Uses add_entities=true to open the entity add flow on existing devices.
"""
import requests
import json
import time

HA = "http://ha.story-nase.ts.net:8123"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ENTRY = "01KJY4Y15NHBF5YGQKN4QAQ59R"
FLOW = "/api/config/config_entries/options/flow"
TIMEOUT = 120

TARGETS = [
    {"device_id": "eb1bbd99a961d6c8b2ye9x", "label": "안방 히터 플러그"},
    {"device_id": "ebc941b918f2c7f446wr3i", "label": "거실 라인 조명 플러그"},
    {"device_id": "eb61542c4c5afedc0f2fms", "label": "주방 드라이기 플러그"},
]

def post(path, data):
    r = requests.post(f"{HA}{path}", headers=H, json=data, timeout=TIMEOUT)
    return r.json()

def delete(path):
    requests.delete(f"{HA}{path}", headers=H, timeout=30)

def extract_dp(schema, dp_num):
    if not schema: return None
    for o in schema[0].get("options", []):
        if isinstance(o, list) and o[0].startswith(f"{dp_num} "):
            return o[0]
    return None

def add_sensors(target):
    label = target["label"]
    dev_id = target["device_id"]
    print(f"\n{'='*50}")
    print(f"[{label}] {dev_id}")
    print(f"{'='*50}")

    fid = post(FLOW, {"handler": ENTRY}).get("flow_id")
    if not fid:
        return False

    try:
        post(f"{FLOW}/{fid}", {"action": "edit_device"})
        
        print("  Connecting to device...")
        step = post(f"{FLOW}/{fid}", {"selected_device": dev_id})
        
        if step.get("step_id") != "configure_device":
            print(f"  ✗ Unexpected: {step.get('step_id')} {step.get('errors')}")
            delete(f"{FLOW}/{fid}")
            return False

        # Build config from defaults, but override add_entities=true
        # and keep entities as the multi_select value (list of option keys)
        config = {}
        entities_options = []
        for field in step.get("data_schema", []):
            name = field["name"]
            if name == "entities":
                # multi_select: extract option keys for currently selected entities
                opts = field.get("options", [])
                entities_options = [o[0] if isinstance(o, list) else o for o in opts]
                # Default is a list of dicts representing current entities
                # We need to pass the option keys (strings like "1: ") to keep them
                config["entities"] = entities_options
            elif name == "add_entities":
                config["add_entities"] = True  # KEY: trigger add-entity flow
            elif "default" in field:
                config[name] = field["default"]

        print(f"  Submitting config with add_entities=true...")
        step2 = post(f"{FLOW}/{fid}", config)
        print(f"  Result: {step2.get('step_id')} errors={step2.get('errors')}")

        if step2.get("step_id") != "pick_entity_type":
            print(f"  ✗ Failed to reach pick_entity_type")
            print(f"    {json.dumps(step2, indent=2)[:500]}")
            delete(f"{FLOW}/{fid}")
            return False

        sensors_added = 0

        # Power sensor (DP 19)
        step_pwr = post(f"{FLOW}/{fid}", {"platform_to_add": "sensor"})
        if "data_schema" in step_pwr:
            dp19 = extract_dp(step_pwr["data_schema"], 19)
            if dp19:
                post(f"{FLOW}/{fid}", {
                    "id": dp19, "friendly_name": "Power",
                    "device_class": "power", "unit_of_measurement": "W", "scaling": 0.1
                })
                print("  ✓ Power (DP 19)")
                sensors_added += 1
            else:
                print(f"  ✗ DP 19 not found")
        else:
            print(f"  ✗ Power schema missing")

        # Current sensor (DP 18)
        step_cur = post(f"{FLOW}/{fid}", {"platform_to_add": "sensor"})
        if "data_schema" in step_cur:
            dp18 = extract_dp(step_cur["data_schema"], 18)
            if dp18:
                post(f"{FLOW}/{fid}", {
                    "id": dp18, "friendly_name": "Current",
                    "device_class": "current", "unit_of_measurement": "A", "scaling": 0.001
                })
                print("  ✓ Current (DP 18)")
                sensors_added += 1

        # Voltage sensor (DP 20)
        step_vol = post(f"{FLOW}/{fid}", {"platform_to_add": "sensor"})
        if "data_schema" in step_vol:
            dp20 = extract_dp(step_vol["data_schema"], 20)
            if dp20:
                post(f"{FLOW}/{fid}", {
                    "id": dp20, "friendly_name": "Voltage",
                    "device_class": "voltage", "unit_of_measurement": "V", "scaling": 0.1
                })
                print("  ✓ Voltage (DP 20)")
                sensors_added += 1

        # Finish
        post(f"{FLOW}/{fid}", {"no_additional_entities": True})
        print(f"  → Done! Sensors added: {sensors_added}/3")
        return sensors_added > 0

    except Exception as e:
        print(f"  ✗ Exception: {e}")
        delete(f"{FLOW}/{fid}")
        return False


if __name__ == "__main__":
    results = {}
    for t in TARGETS:
        ok = add_sensors(t)
        results[t["label"]] = "OK" if ok else "FAIL"
        time.sleep(2)

    print(f"\n{'='*50}")
    print("SUMMARY")
    for name, status in results.items():
        print(f"  {'✅' if status=='OK' else '❌'} {name}: {status}")
