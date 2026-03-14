import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

async def final_sweep():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url.rstrip('/')}/api/websocket"

    TARGET_AREA_NAME = "[RAW] 중복/미사용"

    async with websockets.connect(ws_url) as ws:
        msg = await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        msg = await ws.recv()
        
        # 1. Get Area ID
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
        res = json.loads(await ws.recv())
        target_area_id = next((a['area_id'] for a in res.get('result', []) if a['name'] == TARGET_AREA_NAME), None)
        
        # 2. Get Devices
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv()).get('result', [])
        dev_map = {d['id']: d for d in devices}
        
        # 3. Get Entities
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv()).get('result', [])
        
        # 4. Find all active entities from ST that are NOT in RAW area
        entities_to_disable = []
        devices_to_disable = set()
        
        for e in entities:
            if e.get('disabled_by') is None and e.get('platform') == 'smartthings':
                dev_id = e.get('device_id')
                dev = dev_map.get(dev_id, {})
                # If the device is not already in the RAW area, it's a target
                if dev.get('area_id') != target_area_id:
                    entities_to_disable.append(e['entity_id'])
                    devices_to_disable.add(dev_id)
                    
        print(f"Found {len(entities_to_disable)} ST entities and {len(devices_to_disable)} ST Devices to clean up.")
        
        # 5. Disable and move Entities
        for e_id in entities_to_disable:
            msg_id += 1
            payload = {
                "id": msg_id,
                "type": "config/entity_registry/update",
                "entity_id": e_id,
                "disabled_by": "user",
                "area_id": target_area_id
            }
            await ws.send(json.dumps(payload))
            await ws.recv()
            print(f"Disabled & Moved Entity: {e_id}")
            await asyncio.sleep(0.05)
            
        # 6. Disable and move Devices
        for d_id in devices_to_disable:
            if d_id is None:
                continue
            msg_id += 1
            payload = {
                "id": msg_id,
                "type": "config/device_registry/update",
                "device_id": d_id,
                "disabled_by": "user",
                "area_id": target_area_id
            }
            await ws.send(json.dumps(payload))
            await ws.recv()
            print(f"Disabled & Moved Device: {dev_map[d_id].get('name')}")
            await asyncio.sleep(0.05)
            
        print("\nFinal Sweep Complete!")

if __name__ == "__main__":
    asyncio.run(final_sweep())
