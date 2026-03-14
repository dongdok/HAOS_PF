import requests
import json
import sys

url = "http://ha.story-nase.ts.net:8123/api/config/config_entries/options/flow"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# Start options flow
payload = {"handler": "01KJY4Y15NHBF5YGQKN4QAQ59R"}
init_resp = requests.post(url, headers=headers, json=payload)
print("Init Status:", init_resp.status_code)

if init_resp.status_code != 200:
    print(init_resp.text)
    sys.exit(1)

data = init_resp.json()
flow_id = data.get("flow_id")
print("Options Flow Init:")
print(json.dumps(data, indent=2))

if flow_id:
    # Delete the flow after checking schema
    requests.delete(f"http://ha.story-nase.ts.net:8123/api/config/config_entries/flow/{flow_id}", headers=headers)
