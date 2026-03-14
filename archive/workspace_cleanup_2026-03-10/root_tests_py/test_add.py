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
            print(f"Validation Error 400 on {path}\n{res.text}")
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
        
        # Look closely at step 2 schema
        options = step2['data_schema'][0]['options']
        manual_val = options[0][0]
        print(f"Manual value extracted: '{manual_val}'")
        
        step3 = api_post(f"/api/config/config_entries/options/flow/{flow_id}", {"selected_device": manual_val})
        print(f"Step 3 result: {step3.get('step_id')}")
        print(json.dumps(step3.get('data_schema', []), indent=2))
        
        api_delete(f"/api/config/config_entries/options/flow/{flow_id}")
    except Exception as e:
        print("Exception:", e)
        if flow_id:
            api_delete(f"/api/config/config_entries/options/flow/{flow_id}")

if __name__ == "__main__":
    main()
