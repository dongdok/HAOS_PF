import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

async def check_remaining_st_devices():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url.rstrip('/')}/api/websocket"

    async with websockets.connect(ws_url) as ws:
        msg = await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        msg = await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv()).get('result', [])
        
        await ws.send(json.dumps({"id": 2, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv()).get('result', [])
        
        dev_map = {d['id']: d for d in devices}
        area_map = {} # We'll just print area_id for now
        
        print("--- Active Entities from SmartThings Integration ---")
        st_count = 0
        for e in entities:
            # Check if active
            if e.get('disabled_by') is None:
                # Check if it belongs to SmartThings
                if e.get('platform') == 'smartthings':
                    dev_id = e.get('device_id')
                    dev = dev_map.get(dev_id, {})
                    dev_name = dev.get('name', 'Unknown Device')
                    area_id = dev.get('area_id', 'None')
                    
                    # We only care if it's NOT in raw_jungbog_misayong
                    if area_id != 'raw_jungbog_misayong':
                        print(f"Entity: {e['entity_id']} | Device: {dev_name} | Area: {area_id}")
                        st_count += 1
                        
        print(f"\nTotal remaining active SmartThings entities outside RAW area: {st_count}")

if __name__ == "__main__":
    asyncio.run(check_remaining_st_devices())
