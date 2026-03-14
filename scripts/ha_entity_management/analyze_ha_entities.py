import os
import requests
import json
from dotenv import load_dotenv

def get_ha_entities():
    # Load environment variables from .env file
    load_dotenv()
    
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    if not token or not url:
        print("Error: HA_TOKEN or HA_URL not found in .env file.")
        return

    # Set up the API endpoint and headers
    api_endpoint = f"{url.rstrip('/')}/api/states"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    print(f"Fetching entities from {api_endpoint}...")
    
    try:
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        entities = response.json()
        
        duplicates = []
        
        # We are looking for '_2' suffix or entities from Tuya overlapping with SmartThings
        # In /api/states, we mainly see entity_id and state/attributes.
        # We will filter for entity_ids ending in _2 first, as that was the established pattern.
        
        for entity in entities:
            entity_id = entity.get('entity_id', '')
            state = entity.get('state', '')
            attributes = entity.get('attributes', {})
            friendly_name = attributes.get('friendly_name', 'Unknown')
            
            # Simple heuristic: Ends with _2 (or _3) and is not hidden/unavailable
            if entity_id.endswith('_2') or entity_id.endswith('_3'):
                duplicates.append({
                    'entity_id': entity_id,
                    'friendly_name': friendly_name,
                    'state': state
                })
                
        print(f"\nFound {len(entities)} total entities.")
        print(f"Found {len(duplicates)} potential duplicates (ending in _2 or _3):\n")
        
        for dup in sorted(duplicates, key=lambda x: x['entity_id']):
            print(f"- {dup['entity_id']} ({dup['friendly_name']}) | Status: {dup['state']}")

        # Save the full list for deeper analysis if needed
        with open('ha_entities_dump.json', 'w', encoding='utf-8') as f:
            json.dump(entities, f, ensure_ascii=False, indent=2)
            
        print("\nFull entity dump saved to ha_entities_dump.json")

    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Home Assistant API: {e}")

if __name__ == "__main__":
    get_ha_entities()
