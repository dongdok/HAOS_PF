import os
import requests
import json
from dotenv import load_dotenv

def verify_redundancy():
    load_dotenv()
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    if not token or not url:
        print("Error: Missing credentials")
        return

    api_endpoint = f"{url.rstrip('/')}/api/states"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(api_endpoint, headers=headers)
    entities = response.json()
    
    # We will pick a few examples from our list and compare the original vs _2/_3
    # Look for: state, friendly_name, device_class, last_changed
    
    examples = [
        "sensor.anbang_onseubdosenseo_humidity",
        "binary_sensor.hwajangsil_doeosenseo_door",
        "switch.switch_3"
    ]
    
    print("--- Redundancy Verification Report ---\n")
    
    for base in examples:
        orig = next((e for e in entities if e['entity_id'] == base), None)
        dup2 = next((e for e in entities if e['entity_id'] == f"{base}_2"), None)
        dup3 = next((e for e in entities if e['entity_id'] == f"{base}_3"), None)
        
        print(f"Base Entity: {base}")
        if orig:
            print(f"  [Original ] State: {orig['state']:<5} | Name: {orig['attributes'].get('friendly_name')}")
        else:
            print(f"  [Original ] Not Found")
            
        if dup2:
            print(f"  [Dup (_2) ] State: {dup2['state']:<5} | Name: {dup2['attributes'].get('friendly_name')}")
        if dup3:
            print(f"  [Dup (_3) ] State: {dup3['state']:<5} | Name: {dup3['attributes'].get('friendly_name')}")
        print("-" * 50)

if __name__ == "__main__":
    verify_redundancy()
