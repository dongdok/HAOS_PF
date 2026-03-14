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
        r1 = json.loads(await ws.recv()).get('result', [])
        area_name_to_id = {a['name']: a['area_id'] for a in r1}
        area_id_to_name = {a['area_id']: a['name'] for a in r1}
                
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        r2 = json.loads(await ws.recv()).get('result', [])
        
        await ws.send(json.dumps({"id": 3, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv()).get('result', [])
        
        targets = ['안방조명', '화장실스위치', '히터', '전기매트', '거실불', '주방불', '옷방불', '가습기', '제습기', '책상']
        
        print("--- Force Rescuing Targets ---")
        msg_id = 3
        
        dev_to_ents = {}
        for e in entities:
            d_id = e.get('device_id')
            if d_id: dev_to_ents.setdefault(d_id, []).append(e)
            
        rescued_eids = []
            
        for d in r2:
            name = d.get('name', '')
            if any(t in name for t in targets):
                old_area_name = area_id_to_name.get(d.get('area_id'), '')
                print(f"Found Target Device: {name} | Currently in: {old_area_name} | Disabled: {d.get('disabled_by')}")
                
                # Determine new area
                new_area = '거실'
                if '안방' in name or '침대' in name: new_area = '안방'
                if '화장실' in name: new_area = '화장실'
                if '주방' in name: new_area = '주방'
                if '옷방' in name: new_area = '옷방'
                if '책상' in name: new_area = '안방'
                
                new_area_id = area_name_to_id.get(new_area)
                
                # Update Device Area
                msg_id += 1
                await ws.send(json.dumps({
                    "id": msg_id,
                    "type": "config/device_registry/update",
                    "device_id": d['id'],
                    "area_id": new_area_id,
                    "name_by_user": f"{new_area} {name}" if new_area not in name else name
                }))
                await ws.recv()
                
                # Update Entities Area
                for e in dev_to_ents.get(d['id'], []):
                    msg_id += 1
                    await ws.send(json.dumps({
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": e['entity_id'],
                        "area_id": new_area_id
                    }))
                    await ws.recv()
                    rescued_eids.append({"id": e['entity_id'], "area": new_area})

        # Append to Dashboard
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if res.get("success"):
            config = res.get("result", {})
            if "views" in config and config["views"]:
                cards = config["views"][0].get("cards", [])
                for rev in rescued_eids:
                    # add to entity card matching rev["area"]
                    c = next((c for c in cards if c.get("title") == rev["area"] and c.get("type") == "entities"), None)
                    if c:
                        if not any(e == rev["id"] or isinstance(e, dict) and e.get("entity") == rev["id"] for e in c.get("entities", [])):
                            c["entities"].append(rev["id"])
                
                msg_id += 1
                await ws.send(json.dumps({
                    "id": msg_id,
                    "type": "lovelace/config/save",
                    "config": config
                }))
                await ws.recv()
                print("Dashboard updated!")

asyncio.run(check())
