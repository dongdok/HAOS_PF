"""
LocalTuya Plug Provisioner - Final Version
Deploys 5 smart plugs via HA Options Flow REST API.
Each plug gets: switch (DP1), power sensor (DP19), current sensor (DP18), voltage sensor (DP20).
"""
import requests
import json
import time
import sys

HA_URL = "http://ha.story-nase.ts.net:8123"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
ENTRY_ID = "01KJY4Y15NHBF5YGQKN4QAQ59R"

# Standard smart plug DPs (Tuya WiFi Plug with energy monitoring)
PLUG_DPS = "1,9,17,18,19,20,21,22,23,24,25,26,38,39,41,42,43,44"

# Excluded: 옷방 온습도센서(eb1dffeb4e80c3466faybp), 현관 도어 센서(eba8acd736673b1176ajmg)
PLUGS = [
    {"name": "anbang_humidifier",         "device_id": "eb255dffb9d10e9457bbkb", "ip": "192.168.10.123", "key": "':N`/$H-5$|Us;r6`"},
    {"name": "anbang_electric_blanket",   "device_id": "eb2718100f510651a8w7hp", "ip": "192.168.10.100", "key": "*TWq#A{Ww@!{y?g)"},
    {"name": "geosil_line_lighting_plug", "device_id": "ebc941b918f2c7f446wr3i", "ip": "192.168.10.128", "key": "[5tC~6YSNrkbmP|B"},
    {"name": "anbang_heater_plug",        "device_id": "eb1bbd99a961d6c8b2ye9x", "ip": "192.168.10.126", "key": ")K'o*Y<^lCB.JGJ0"},
    {"name": "jubang_hair_dryer_plug",    "device_id": "eb61542c4c5afedc0f2fms", "ip": "192.168.10.125", "key": "Qrc36^V(dr>9nyS0"},
]

def api_post(path, payload):
    res = requests.post(f"{HA_URL}{path}", headers=HEADERS, json=payload)
    data = res.json()
    if res.status_code == 400:
        return data
    res.raise_for_status()
    return data

def api_delete(path):
    requests.delete(f"{HA_URL}{path}", headers=HEADERS)

def extract_dp_id(schema, dp_num):
    """Find the DP option string like '1 (value: False)' from schema options."""
    if not schema or not isinstance(schema, list):
        return None
    opts = schema[0].get('options', [])
    prefix = f"{dp_num} "
    for o in opts:
        if isinstance(o, list) and len(o) >= 1 and o[0].startswith(prefix):
            return o[0]
    return None

def configure_plug(plug, proto):
    """Run the full Options Flow to add one device with switch + 3 sensors."""
    flow_url = "/api/config/config_entries/options/flow"
    
    # Start flow
    step1 = api_post(flow_url, {"handler": ENTRY_ID})
    fid = step1.get("flow_id")
    if not fid:
        return False, f"Could not start flow: {step1}"
    
    try:
        # Step 2: Select add_device
        api_post(f"{flow_url}/{fid}", {"action": "add_device"})
        
        # Step 3: Select manual entry
        api_post(f"{flow_url}/{fid}", {"selected_device": "..."})
        
        # Step 4: Submit device credentials + manual_dps_strings
        step4 = api_post(f"{flow_url}/{fid}", {
            "friendly_name": plug['name'],
            "host": plug['ip'],
            "device_id": plug['device_id'],
            "local_key": plug['key'],
            "protocol_version": proto,
            "enable_debug": False,
            "manual_dps_strings": PLUG_DPS,
        })
        
        if step4.get("errors"):
            api_delete(f"{flow_url}/{fid}")
            return False, step4["errors"]
        
        if step4.get("step_id") != "pick_entity_type":
            api_delete(f"{flow_url}/{fid}")
            return False, f"Unexpected step after auth: {step4.get('step_id')}"
        
        print(f"  Auth OK (proto {proto}), mapping entities...")
        
        # === Entity 1: Switch (DP 1) ===
        step_sw = api_post(f"{flow_url}/{fid}", {"platform_to_add": "switch"})
        if 'data_schema' not in step_sw:
            api_delete(f"{flow_url}/{fid}")
            return False, f"Switch schema missing: {step_sw}"
        
        dp1 = extract_dp_id(step_sw['data_schema'], 1)
        if not dp1:
            api_delete(f"{flow_url}/{fid}")
            return False, "DP 1 not found in switch options"
        
        api_post(f"{flow_url}/{fid}", {
            "id": dp1,
            "friendly_name": "",
            "restore_on_reconnect": False,
            "is_passive_entity": False,
        })
        print("    ✓ Switch (DP 1)")
        
        # === Entity 2: Power Sensor (DP 19) ===
        step_pwr = api_post(f"{flow_url}/{fid}", {"platform_to_add": "sensor"})
        if 'data_schema' not in step_pwr:
            print("    ✗ Power sensor schema missing, skipping remaining sensors")
            api_post(f"{flow_url}/{fid}", {"no_additional_entities": True})
            return True, "Partial (switch only)"
        
        dp19 = extract_dp_id(step_pwr['data_schema'], 19)
        if dp19:
            api_post(f"{flow_url}/{fid}", {
                "id": dp19,
                "friendly_name": "Power",
                "device_class": "power",
                "unit_of_measurement": "W",
                "scaling": 0.1,
            })
            print("    ✓ Power (DP 19, W, scale 0.1)")
        else:
            print("    ✗ DP 19 not found, skipping power sensor")
            # Submit empty to advance
            api_post(f"{flow_url}/{fid}", {"no_additional_entities": True})
            return True, "Partial (no power)"
        
        # === Entity 3: Current Sensor (DP 18) ===
        step_cur = api_post(f"{flow_url}/{fid}", {"platform_to_add": "sensor"})
        if 'data_schema' not in step_cur:
            api_post(f"{flow_url}/{fid}", {"no_additional_entities": True})
            return True, "Partial (switch+power)"
        
        dp18 = extract_dp_id(step_cur['data_schema'], 18)
        if dp18:
            api_post(f"{flow_url}/{fid}", {
                "id": dp18,
                "friendly_name": "Current",
                "device_class": "current",
                "unit_of_measurement": "A",
                "scaling": 0.001,
            })
            print("    ✓ Current (DP 18, A, scale 0.001)")
        else:
            print("    ✗ DP 18 not found")
            api_post(f"{flow_url}/{fid}", {"no_additional_entities": True})
            return True, "Partial (switch+power)"
        
        # === Entity 4: Voltage Sensor (DP 20) ===
        step_vol = api_post(f"{flow_url}/{fid}", {"platform_to_add": "sensor"})
        if 'data_schema' not in step_vol:
            api_post(f"{flow_url}/{fid}", {"no_additional_entities": True})
            return True, "Partial (switch+power+current)"
        
        dp20 = extract_dp_id(step_vol['data_schema'], 20)
        if dp20:
            api_post(f"{flow_url}/{fid}", {
                "id": dp20,
                "friendly_name": "Voltage",
                "device_class": "voltage",
                "unit_of_measurement": "V",
                "scaling": 0.1,
            })
            print("    ✓ Voltage (DP 20, V, scale 0.1)")
        else:
            print("    ✗ DP 20 not found")
        
        # === Finish ===
        final = api_post(f"{flow_url}/{fid}", {"no_additional_entities": True})
        print(f"    → Flow complete (step: {final.get('step_id', 'done')})")
        return True, "Full (switch+power+current+voltage)"
        
    except Exception as e:
        api_delete(f"{flow_url}/{fid}")
        return False, str(e)


def main():
    results = {}
    
    for plug in PLUGS:
        print(f"\n{'='*60}")
        print(f"[{plug['name']}] host={plug['ip']}")
        print(f"{'='*60}")
        
        # Try 3.4 first (proven to work), fallback to 3.3
        for proto in ["3.4", "3.3"]:
            print(f"  Trying protocol {proto}...")
            success, msg = configure_plug(plug, proto)
            if success:
                results[plug['name']] = {"status": "OK", "protocol": proto, "detail": msg}
                print(f"  ✅ SUCCESS ({proto}): {msg}")
                break
            else:
                print(f"  ❌ Failed ({proto}): {msg}")
                if proto == "3.3":
                    results[plug['name']] = {"status": "FAIL", "detail": str(msg)}
        
        time.sleep(1)  # Brief pause between devices
    
    # Summary
    print(f"\n{'='*60}")
    print("PROVISION SUMMARY")
    print(f"{'='*60}")
    ok = sum(1 for r in results.values() if r['status'] == 'OK')
    fail = sum(1 for r in results.values() if r['status'] == 'FAIL')
    print(f"Success: {ok}/5, Failed: {fail}/5\n")
    
    for name, r in results.items():
        icon = "✅" if r['status'] == 'OK' else "❌"
        print(f"  {icon} {name}: {r['status']} - {r.get('detail','')}")
    
    with open("local_tuya_provision_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nResults saved to local_tuya_provision_results.json")


if __name__ == "__main__":
    main()
