import os, json, asyncio, websockets
from dotenv import load_dotenv

async def rescue():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    
    async_sleep = 0.05
    
    def target_area_logic(name):
        name_lower = name.lower()
        if '안방' in name_lower or '침대' in name_lower or '바디럽' in name_lower: return '안방'
        if '거실' in name_lower or 'm7' in name_lower or '테라스' in name_lower: return '거실'
        if '주방' in name_lower: return '주방'
        if '옷방' in name_lower: return '옷방'
        if '화장실' in name_lower: return '화장실'
        if '현관' in name_lower: return '현관'
        if '가상' in name_lower or '일단가상' in name_lower or '굿나잇' in name_lower or '외출' in name_lower: return '[가상] 헬퍼'
        return '미분류'
        
    def rename_logic(name, area):
        clean = name.replace('일단가상', '가상').replace('1', '').replace('2', '').replace('3', '').replace('4', '').strip()
        if '가상' in area and '[가상]' not in clean:
            clean = f"[가상] {clean}".replace('가상스위치', '스위치').replace('가상 스위치', '스위치')
        elif area not in clean and area not in ['시스템/애드온', '기기제어', '미분류']:
            clean = f"{area} {clean}"
        return ' '.join(clean.split())

    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
        areas_resp = json.loads(await ws.recv()).get('result', [])
        area_name_to_id = {a['name']: a['area_id'] for a in areas_resp}
        area_id_to_name = {a['area_id']: a['name'] for a in areas_resp}
        
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        devices = [d for d in json.loads(await ws.recv()).get('result', []) if not d.get('disabled_by')]
        
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        entities = [e for e in json.loads(await ws.recv()).get('result', []) if not e.get('disabled_by')]
        
        dev_to_entities = {}
        for e in entities:
            dev_id = e.get('device_id')
            if dev_id:
                dev_to_entities.setdefault(dev_id, []).append(e)

        rescued_entities = []

        print("--- Rescuing Devices from RAW ---")
        for d in devices:
            old_area_name = area_id_to_name.get(d.get('area_id'), '')
            if old_area_name in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                
                # Exceptions - if it's literally named Scene, it shouldn't be active anyway but let's just categorize it
                old_name = d.get('name', 'Unknown')
                new_area_name = target_area_logic(old_name)
                # If we couldn't classify it and it was in RAW, maybe keep it in RAW, but user wants to see it.
                if new_area_name == '미분류':
                    if 'Switch' in old_name or 'outlet' in old_name:
                        new_area_name = '[가상] 헬퍼'
                    else:
                        new_area_name = '거실' # fallback to living room so they aren't lost
                
                new_area_id = area_name_to_id.get(new_area_name)
                new_name = rename_logic(old_name, new_area_name)
                
                msg_id += 1
                payload = {
                    "id": msg_id,
                    "type": "config/device_registry/update",
                    "device_id": d['id'],
                    "name_by_user": new_name,
                    "area_id": new_area_id
                }
                await ws.send(json.dumps(payload))
                await ws.recv()
                print(f"Rescued Device: '{old_name}' -> '{new_name}' in Area: {new_area_name}")
                
                # Update Entities
                ents = dev_to_entities.get(d['id'], [])
                for e in ents:
                    e_old_name = e.get('name') or e.get('original_name') or 'Unknown'
                    e_new_name = rename_logic(e_old_name, new_area_name)
                    if e_new_name == new_name:
                        e_new_name = f"{new_name} ({e.get('entity_id').split('.')[0]})"
                        
                    msg_id += 1
                    epayload = {
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": e['entity_id'],
                        "name": e_new_name,
                        "area_id": new_area_id
                    }
                    await ws.send(json.dumps(epayload))
                    await ws.recv()
                    rescued_entities.append({
                        "id": e['entity_id'],
                        "area": new_area_name
                    })
                    await asyncio.sleep(async_sleep)

        # Update Lovelace
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if res.get("success"):
            config = res.get("result", {})
            if config and "views" in config and config["views"]:
                view = config["views"][0]
                cards = view.get("cards", [])
                
                for re in rescued_entities:
                    eid = re["id"]
                    if eid.startswith("light.") or eid.startswith("switch.") or eid.startswith("climate."):
                        target_area = re["area"]
                        # Find the card for this area
                        target_card = next((c for c in cards if c.get("title") == target_area and c.get("type") == "entities"), None)
                        if target_card:
                            # Avoid duplicates
                            if not any((e == eid if isinstance(e, str) else e.get("entity") == eid) for e in target_card.get("entities", [])):
                                target_card["entities"].append(eid)
                        else:
                            # Need to create the card
                            if target_area not in ["[가상] 헬퍼", "미분류"]:
                                new_card = {
                                    "type": "entities",
                                    "title": target_area,
                                    "entities": [eid]
                                }
                                cards.append(new_card)
                
                msg_id += 1
                await ws.send(json.dumps({
                    "id": msg_id, 
                    "type": "lovelace/config/save", 
                    "config": config
                }))
                await ws.recv()
                print("Dashboard updated with rescued entities!")

asyncio.run(rescue())
