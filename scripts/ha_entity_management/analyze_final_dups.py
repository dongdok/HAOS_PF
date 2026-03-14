import os
import json
import asyncio
import websockets
from dotenv import load_dotenv

async def analyze_remaining_duplicates():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url.rstrip('/')}/api/websocket"

    async with websockets.connect(ws_url) as ws:
        msg = await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        # Get areas
        await ws.send(json.dumps({"id": 1, "type": "config/area_registry/list"}))
        areas = json.loads(await ws.recv()).get('result', [])
        area_map = {a['area_id']: a['name'] for a in areas}
        
        # Get devices
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv()).get('result', [])
        
        # Get entities
        await ws.send(json.dumps({"id": 3, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv()).get('result', [])
        
        print("--- Detailed Duplicate Analysis ---")
        
        # The user noticed that even some "Tuya" (orange icon) devices are in RAW area, 
        # while other Tuya devices with similar names are active.
        # Let's map all devices by name to find name collisions.
        
        devices_by_name = {}
        
        for d in devices:
            name = d.get('name')
            if not name:
                continue
            
            # Clean up names slightly to match base names (e.g., removing suffixes if any, though the UI shows exact matches)
            # Actually, from the screenshot:
            # - 안방 온습도센서 (센서 / Tuya) - active
            # - 안방 온습도센서 ([RAW] / SmartThings) - this is what we expected
            # But the user pointed something else out.
            # Look at: 
            # - 안방조명 ([RAW] / Tuya / Tuya / Smart Lighting) -> Orange Tuya icon, in RAW!
            # - 에어컨/난방 ON/OFF ([RAW] / Tuya / Tuya / smart plug) -> Orange Tuya icon, in RAW!
            # - 거실조명 ([RAW] / Tuya / Tuya / LED BULB...) -> Orange Tuya icon, in RAW!
            
            if name not in devices_by_name:
                devices_by_name[name] = []
            
            devices_by_name[name].append({
                'id': d['id'],
                'manufacturer': d.get('manufacturer', 'Unknown'),
                'model': d.get('model', 'Unknown'),
                'area': area_map.get(d.get('area_id'), 'No Area'),
                'disabled': True if d.get('disabled_by') else False
            })
            
        # Let's print devices that share the same exact name and have multiple entries
        duplicates_found = 0
        for name, device_list in devices_by_name.items():
            if len(device_list) > 1:
                duplicates_found += 1
                print(f"\n[Duplicate Name Found: {name}]")
                for idx, dev in enumerate(device_list):
                    status = "DISABLED" if dev['disabled'] else "ACTIVE"
                    mfg = str(dev['manufacturer']) if dev['manufacturer'] else 'Unknown'
                    mdl = str(dev['model']) if dev['model'] else 'Unknown'
                    print(f"  {idx+1}. Area: {dev['area']:<15} | Mfg: {mfg:<15} | Model: {mdl:<20} | Status: {status}")
                    
        print(f"\nTotal potential duplicate groups based on exact names: {duplicates_found}")

if __name__ == "__main__":
    asyncio.run(analyze_remaining_duplicates())
