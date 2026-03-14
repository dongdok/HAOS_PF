import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

async def disable_entities():
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

    print(f"Connecting to {ws_url}...")
    
    try:
        async with websockets.connect(ws_url) as websocket:
            # 1. Wait for auth_required
            msg = await websocket.recv()
            data = json.loads(msg)
            if data.get('type') != 'auth_required':
                print(f"Unexpected initial message: {data}")
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
                print(f"Authentication failed: {data}")
                return
                
            print("Authentication successful! Disabling entities...")
            
            # 4. Disable entities one by one
            msg_id = 1
            success_count = 0
            
            for target in targets:
                entity_id = target['entity_id']
                name = target['name']
                
                payload = {
                    "id": msg_id,
                    "type": "config/entity_registry/update",
                    "entity_id": entity_id,
                    "disabled_by": "user"
                }
                
                await websocket.send(json.dumps(payload))
                response = await websocket.recv()
                resp_data = json.loads(response)
                
                if resp_data.get('success'):
                    print(f"[{msg_id}/{len(targets)}] Disabled: {entity_id} ({name})")
                    success_count += 1
                else:
                    print(f"[{msg_id}/{len(targets)}] Failed to disable {entity_id}: {resp_data.get('error')}")
                
                msg_id += 1
                
                # Small delay to prevent overwhelming the server
                await asyncio.sleep(0.1)
                
            print(f"\nDone! Successfully disabled {success_count} out of {len(targets)} entities.")
            
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    asyncio.run(disable_entities())
