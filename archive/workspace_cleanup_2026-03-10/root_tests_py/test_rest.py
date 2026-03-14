import os
import requests
import json

url = "http://ha.story-nase.ts.net:8123/api/config/config_entries/flow"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# Initialize flow
init_resp = requests.post(url, headers=headers, json={"handler": "localtuya"})
print("Status:", init_resp.status_code)
print("Init Response:", json.dumps(init_resp.json(), indent=2))

if init_resp.status_code == 200:
    data = init_resp.json()
    flow_id = data.get("flow_id")
    # Clean up right away
    if flow_id:
        requests.delete(f"{url}/{flow_id}", headers=headers)
