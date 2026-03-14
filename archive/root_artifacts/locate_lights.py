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
                
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        r2 = json.loads(await ws.recv())
        devices = r2.get('result', [])
        
        await ws.send(json.dumps({"id": 3, "type": "config/entity_registry/list"}))
        r3 = json.loads(await ws.recv())
        entities = r3.get('result', [])

        targets = ['거실불', '안방조명', '옷방불', '주방불']
        print("--- Checking Missing Targets ---")
        
        dev_map = {d['id']: d for d in devices}
        
        for e in entities:
            # We care about light. and switch. domains
            ename = e.get('name', '') or e.get('original_name', '') or ''
            
            is_target = False
            for t in targets:
                if t in ename:
                    is_target = True
                
            if is_target:
                dev = dev_map.get(e.get('device_id'))
                if dev:
                    area_name = areas.get(dev.get('area_id'), 'No Area')
                    disabled = d.get('disabled_by') or e.get('disabled_by')
                    print(f"Entity: {e['entity_id']} | Name: {ename} | Area: {area_name} | Disabled: {disabled}")

asyncio.run(check())
