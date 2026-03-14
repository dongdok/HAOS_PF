import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

async def disable_empty_devices():
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))
    
    # Actually, the script is in scripts/ha_entity_management now.
    # We should just load from the workspace root where .env is.
    load_dotenv('../../.env')
    
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    if not token or not url:
        print("Error: Missing HA_TOKEN or HA_URL in .env file.")
        return

    ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url.rstrip('/')}/api/websocket"

    # We need to target the same Area ID we used earlier
    TARGET_AREA_NAME = "[RAW] 중복/미사용"

    print(f"Connecting to {ws_url}...")
    
    try:
        async with websockets.connect(ws_url) as websocket:
            # 1. Auth Flow
            msg = await websocket.recv()
            if json.loads(msg).get('type') != 'auth_required': return
            await websocket.send(json.dumps({"type": "auth", "access_token": token}))
            msg = await websocket.recv()
            if json.loads(msg).get('type') != 'auth_ok':
                print("Auth failed")
                return
                
            print("Auth successful! Getting areas, devices, and entities...")
            
            # 2. Get target area ID
            msg_id = 1
            await websocket.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
            res = json.loads(await websocket.recv())
            target_area_id = next((a['area_id'] for a in res.get('result', []) if a['name'] == TARGET_AREA_NAME), None)
            
            if not target_area_id:
                print(f"Area {TARGET_AREA_NAME} not found!")
                return
                
            # 3. Get Entity Registry
            msg_id += 1
            await websocket.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
            entity_list = json.loads(await websocket.recv()).get('result', [])
            
            # Map devices to their active/enabled entities
            # We want to find devices from SmartThings that have 0 enabled entities.
            
            device_active_entities = {}
            device_disabled_entities = {}
            
            for ent in entity_list:
                dev_id = ent.get('device_id')
                if not dev_id: continue
                
                # If disabled_by is None, it is active/enabled.
                is_disabled = ent.get('disabled_by') is not None
                
                if is_disabled:
                    device_disabled_entities[dev_id] = device_disabled_entities.get(dev_id, 0) + 1
                else:
                    device_active_entities[dev_id] = device_active_entities.get(dev_id, 0) + 1
                    
            # 4. Get Device Registry
            msg_id += 1
            await websocket.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
            device_list = json.loads(await websocket.recv()).get('result', [])
            
            # Find candidate devices
            # Criteria: 
            # - Belong to SmartThings integration (via connections or identifiers or we just rely on having no active entities and being already touched by us)
            # - Actually, if a device has > 0 disabled entities and 0 active entities, it's a "zombie" device we can disable.
            # - Specifically, let's target devices generated via SmartThings integration that have NO active entities.
            
            # SmartThings devices typically have identifiers like: ["smartthings", "xxx"]
            # Or their entities are tied to SmartThings.
            
            target_devices_to_disable = []
            
            for dev in device_list:
                dev_id = dev['id']
                
                # Check if it has any entities at all
                total_disabled = device_disabled_entities.get(dev_id, 0)
                total_active = device_active_entities.get(dev_id, 0)
                
                if total_disabled > 0 and total_active == 0:
                    # It has disabled entities but NO active entities. Zombie!
                    # Make sure it is not already disabled to save API calls
                    if dev.get('disabled_by') is None:
                        target_devices_to_disable.append({
                            'id': dev_id,
                            'name': dev.get('name', 'Unknown Device'),
                            'area_id': dev.get('area_id')
                        })
            
            print(f"\nFound {len(target_devices_to_disable)} zombie devices (with disabled entities but 0 active entities).")
            for d in target_devices_to_disable:
                print(f" - {d['name']} ({d['id']})")
                
            if len(target_devices_to_disable) == 0:
                print("No devices need disabling. Everything is clean.")
                return
                
            # 5. Disable and move the devices
            print("\nDisabling and moving devices...")
            success_count = 0
            for d in target_devices_to_disable:
                msg_id += 1
                payload = {
                    "id": msg_id,
                    "type": "config/device_registry/update",
                    "device_id": d['id'],
                    "disabled_by": "user",
                    "area_id": target_area_id
                }
                
                await websocket.send(json.dumps(payload))
                res = json.loads(await websocket.recv())
                
                if res.get('success'):
                    print(f"[{msg_id}] Disabled & Moved Device: {d['name']}")
                    success_count += 1
                else:
                    print(f"[{msg_id}] Failed for {d['name']}: {res.get('error')}")
                    
                await asyncio.sleep(0.1)
                
            print(f"\nDone! Disabled and moved {success_count} devices.")

    except Exception as e:
        print(f"WebSocket Error: {e}")

if __name__ == "__main__":
    asyncio.run(disable_empty_devices())
