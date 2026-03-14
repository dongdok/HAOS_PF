import os, json, asyncio, websockets
from dotenv import load_dotenv

async def check():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "config/area_registry/list"}))
        areas = {a['area_id']: a['name'] for a in json.loads(await ws.recv()).get('result', [])}
        
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv()).get('result', [])
        
        print("--- Active Devices currently in [RAW] or [SCENE] ---")
        for d in devices:
            if not d.get('disabled_by'):
                area_name = areas.get(d.get('area_id'), 'No Area')
                if area_name in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                    print(f"Name: {d.get('name')} | Area: {area_name}")

asyncio.run(check())
