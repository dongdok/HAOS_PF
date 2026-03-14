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
        
        print("--- Active Devices in Checked Areas ---")
        cnt = 0
        for d in devices:
            if not d.get('disabled_by'):
                area_name = areas.get(d.get('area_id'), 'No Area')
                if area_name not in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                    cnt += 1
                    # print(f"{cnt}. {d.get('name')} ({area_name})")
        
        print(f"Total active visible devices: {cnt}")
        
        print("\n--- ALL Devices in Checked Areas (Active + Disabled) ---")
        cnt2 = 0
        for d in devices:
            area_name = areas.get(d.get('area_id'), 'No Area')
            if area_name not in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                cnt2 += 1
        print(f"Total visible devices if 'Disabled' is NOT filtered: {cnt2}")

        print("\n--- ALL Devices Total (Active) ---")
        cnt3 = 0
        for d in devices:
            if not d.get('disabled_by'):
                    cnt3 += 1
        print(f"Total active devices everywhere: {cnt3}")


asyncio.run(check())
