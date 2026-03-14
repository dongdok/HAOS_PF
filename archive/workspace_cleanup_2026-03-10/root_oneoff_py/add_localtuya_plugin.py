import requests
import json
import sys

HA_URL = "http://ha.story-nase.ts.net:8123"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

ENTRY_ID = "01KJY4Y15NHBF5YGQKN4QAQ59R"

def api_post(path, payload):
    res = requests.post(f"{HA_URL}{path}", headers=HEADERS, json=payload)
    if res.status_code != 200:
        if res.status_code == 400:
            return res.json()
        print(f"Error {res.status_code} on {path}\n{res.text}")
        sys.exit(1)
    return res.json()

def api_delete(path):
    requests.delete(f"{HA_URL}{path}", headers=HEADERS)

def main():
    flow_id = None
    try:
        step1 = api_post("/api/config/config_entries/options/flow", {"handler": ENTRY_ID})
        flow_id = step1["flow_id"]
        
        step2 = api_post(f"/api/config/config_entries/options/flow/{flow_id}", {"action": "add_device"})
        options = step2['data_schema'][0]['options']
        manual_val = options[0][0]
        
        step3 = api_post(f"/api/config/config_entries/options/flow/{flow_id}", {"selected_device": manual_val})
        
        payload = {
            "friendly_name": "switch.geosil_line_lighting_plug",
            "host": "192.168.10.128",
            "device_id": "ebc941b918f2c7f446wr3i",
            "local_key": "[5tC~6YSNrkbmP|B",
            "protocol_version": "3.4",
            "enable_debug": False
        }
        step4 = api_post(f"/api/config/config_entries/options/flow/{flow_id}", payload)
        
        if step4.get('step_id') == 'pick_entity_type':
            print("Auth Success! Picking switch entity...")
            step5 = api_post(f"/api/config/config_entries/options/flow/{flow_id}", {"platform_to_add": "switch"})
            print("Step 5 result:")
            print(json.dumps(step5, indent=2))
        else:
            print("Failed to reach pick_entity_type", step4)
            
        api_delete(f"/api/config/config_entries/options/flow/{flow_id}")
    except Exception as e:
        print("Exception:", e)
        if flow_id:
            api_delete(f"/api/config/config_entries/options/flow/{flow_id}")

if __name__ == "__main__":
    main()
