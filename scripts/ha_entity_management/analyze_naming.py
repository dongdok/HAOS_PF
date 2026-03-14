import os, json, asyncio, websockets
from dotenv import load_dotenv

async def analyze():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket".replace("//api", "/api")
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "config/area_registry/list"}))
        res1 = json.loads(await ws.recv())
        areas = {a['area_id']: a['name'] for a in res1.get('result', [])}
        
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        res2 = json.loads(await ws.recv())
        devices = res2.get('result', [])
        
        # Filter valid areas
        invalid_areas = ['[RAW] 중복/미사용', '[SCENE] 보관']
        
        print("## Current Device Naming & Area Analysis\n")
        print("| Area | Device Name | Manufacturer | Model |")
        print("|---|---|---|---|")
        
        valid_devices = [d for d in devices if not d.get('disabled_by')]
        valid_devices.sort(key=lambda x: (areas.get(x.get('area_id'), 'Unassigned'), x.get('name', '')))
        
        for d in valid_devices:
            a_name = areas.get(d.get('area_id'), 'Unassigned')
            if a_name in invalid_areas:
                continue
            d_name = str(d.get('name', 'Unknown')).replace('|', ' ')
            mfg = str(d.get('manufacturer', 'Unknown')).replace('|', ' ')
            mod = str(d.get('model', 'Unknown')).replace('|', ' ')
            print(f"| {a_name} | {d_name} | {mfg} | {mod} |")

if __name__ == "__main__":
    asyncio.run(analyze())
