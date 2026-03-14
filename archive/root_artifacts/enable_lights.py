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
        
        await ws.send(json.dumps({"id": 1, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv()).get('result', [])
        
        await ws.send(json.dumps({"id": 2, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv()).get('result', [])
        
        targets = ['안방조명', '화장실스위치', '히터', '전기매트', '거실불', '주방불', '옷방불', '가습기', '제습기', '책상']
        
        print("--- Enabling Missing Targets ---")
        msg_id = 2
        
        dev_to_ents = {}
        for e in entities:
            d_id = e.get('device_id')
            if d_id: dev_to_ents.setdefault(d_id, []).append(e)
            
        for d in devices:
            name = d.get('name', '')
            if any(t in name for t in targets):
                # We do NOT want to enable the Scene proxies (which have " 켜", " 꺼" in name usually, or manufacturer Unknown)
                # But let's just enable the ones that are actual Tuya devices
                if '켜' in name or '꺼' in name or 'ON' in name or 'OFF' in name:
                    continue # these are scenes/virtuals
                    
                if d.get('disabled_by'):
                    print(f"Re-enabling Device: {name}")
                    msg_id += 1
                    await ws.send(json.dumps({
                        "id": msg_id,
                        "type": "config/device_registry/update",
                        "device_id": d['id'],
                        "disabled_by": None
                    }))
                    await ws.recv()
                    
                # Enable entities
                for e in dev_to_ents.get(d['id'], []):
                    if e.get('disabled_by'):
                        msg_id += 1
                        await ws.send(json.dumps({
                            "id": msg_id,
                            "type": "config/entity_registry/update",
                            "entity_id": e['entity_id'],
                            "disabled_by": None
                        }))
                        await ws.recv()

asyncio.run(check())
