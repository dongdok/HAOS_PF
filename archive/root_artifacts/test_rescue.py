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
        r1 = json.loads(await ws.recv())
        areas = {a['area_id']: a['name'] for a in r1.get('result', [])}
        print("Areas count:", len(areas))
        
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        r2 = json.loads(await ws.recv())
        opts = r2.get('result', [])
        print("Devices count:", len(opts))
        
        match_count = 0
        for d in opts:
            if not d.get('disabled_by'):
                area_name = areas.get(d.get('area_id'), 'No Area')
                if area_name in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                    match_count += 1
        print("Matches:", match_count)

asyncio.run(check())
