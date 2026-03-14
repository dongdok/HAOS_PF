import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

async def move_entities_to_raw():
    load_dotenv()
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    if not token or not url:
        print("Error: Missing HA_TOKEN or HA_URL in .env file.")
        return

    # Convert HTTP URL to WebSocket URL
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url.rstrip('/')}/api/websocket"

    # Load targets
    try:
        with open('targets_to_disable.json', 'r', encoding='utf-8') as f:
            targets = json.load(f)
    except FileNotFoundError:
        print("Error: targets_to_disable.json not found.")
        return
        
    # The ID of the [RAW] 중복/미사용 area. 
    # Usually, HA creates area IDs from the name by lowercasing and replacing spaces/special chars with underscores.
    # A common ID for "[RAW] 중복/미사용" might be 'raw_jungbog_misayong' or similar based on HA transliteration, 
    # OR the user might have created it. Let's first search for the exact area ID.
    
    TARGET_AREA_NAME = "[RAW] 중복/미사용"

    print(f"Connecting to {ws_url}...")
    
    try:
        async with websockets.connect(ws_url) as websocket:
            # 1. Wait for auth_required
            msg = await websocket.recv()
            data = json.loads(msg)
            if data.get('type') != 'auth_required':
                return
                
            # 2. Send auth
            await websocket.send(json.dumps({
                "type": "auth",
                "access_token": token
            }))
            
            # 3. Wait for auth_ok
            msg = await websocket.recv()
            data = json.loads(msg)
            if data.get('type') != 'auth_ok':
                return
                
            print("Authentication successful! Finding Area ID...")
            
            # Get Areas
            msg_id = 1
            await websocket.send(json.dumps({
                "id": msg_id,
                "type": "config/area_registry/list"
            }))
            
            response = await websocket.recv()
            resp_data = json.loads(response)
            areas = resp_data.get('result', [])
            
            target_area_id = None
            for area in areas:
                if area.get('name') == TARGET_AREA_NAME:
                    target_area_id = area.get('area_id')
                    break
                    
            if not target_area_id:
                print(f"Error: Area '{TARGET_AREA_NAME}' not found.")
                print(f"Available areas: {[a.get('name') for a in areas]}")
                return
                
            print(f"Found Area ID for '{TARGET_AREA_NAME}': {target_area_id}")
            print("Moving entities...")
            
            msg_id += 1
            success_count = 0
            
            # Move entities
            for target in targets:
                entity_id = target['entity_id']
                
                payload = {
                    "id": msg_id,
                    "type": "config/entity_registry/update",
                    "entity_id": entity_id,
                    "area_id": target_area_id
                }
                
                await websocket.send(json.dumps(payload))
                response = await websocket.recv()
                result_data = json.loads(response)
                
                if result_data.get('success'):
                    print(f"[{msg_id}] Moved: {entity_id} to {TARGET_AREA_NAME}")
                    success_count += 1
                else:
                    print(f"[{msg_id}] Failed to move {entity_id}: {result_data.get('error')}")
                
                msg_id += 1
                await asyncio.sleep(0.1)
                
            print(f"\nDone! Successfully moved {success_count} out of {len(targets)} entities to {TARGET_AREA_NAME}.")
            
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    asyncio.run(move_entities_to_raw())
