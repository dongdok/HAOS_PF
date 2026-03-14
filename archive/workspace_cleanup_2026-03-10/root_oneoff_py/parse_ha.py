import requests
import json

url = "http://ha.story-nase.ts.net:8123/api/config/config_entries/entry"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

res = requests.get(url, headers=headers)
if res.status_code == 200:
    entries = res.json()
    tuya_entries = [e for e in entries if e["domain"] == "localtuya"]
    print(json.dumps(tuya_entries, indent=2))
else:
    print(f"Error: {res.status_code} - {res.text}")
