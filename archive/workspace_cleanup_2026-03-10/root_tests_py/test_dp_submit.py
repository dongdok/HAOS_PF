import requests
import json
import sys

HA_URL = "http://ha.story-nase.ts.net:8123"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

if __name__ == "__main__":
    fid = requests.post(f"{HA_URL}/api/config/config_entries/options/flow", headers=HEADERS, json={"handler": "01KJY4Y15NHBF5YGQKN4QAQ59R"}).json()["flow_id"]
    requests.post(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS, json={"action": "add_device"})
    
    manual_val = requests.get(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS).json()['data_schema'][0]['options'][0][0]
    
    requests.post(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS, json={"selected_device": manual_val})
    
    requests.post(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS, json={
        "friendly_name": "geosil_line_lighting_plug",
        "host": "192.168.10.128", "device_id": "ebc941b918f2c7f446wr3i",
        "local_key": "[5tC~6YSNrkbmP|B", "protocol_version": "3.4", "enable_debug": False
    })
    
    step5 = requests.post(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS, json={"platform_to_add": "switch"}).json()
    id_opt = next(o[0] for o in step5['data_schema'][0]['options'] if o[0].startswith("1 "))
    
    step6 = requests.post(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS, json={
        "id": id_opt, "friendly_name": "Switch", "restore_on_reconnect": False, "is_passive_entity": False
    }).json()
    
    print("After successful switch add:", step6.get("step_id", "NO STEP ID"))
    print(json.dumps(step6.get('data_schema', []), indent=2))
    requests.delete(f"{HA_URL}/api/config/config_entries/options/flow/{fid}", headers=HEADERS)
