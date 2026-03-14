import os, json, asyncio, websockets
from dotenv import load_dotenv

async def run():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    
    target_areas = ["거실", "안방", "옷방", "주방", "화장실", "현관"]
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()

        msg_id = 1
        
        # 1. Fetch / Create Areas
        await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
        existing_areas = json.loads(await ws.recv()).get('result', [])
        area_map = {a['name']: a['area_id'] for a in existing_areas}
        
        for ta in target_areas:
            if ta not in area_map:
                msg_id += 1
                await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/create", "name": ta}))
                res = json.loads(await ws.recv())
                if res.get('success'):
                    area_map[ta] = res['result']['area_id']
                    print(f"Created Area: {ta}")
                    
        # 2. Assign Entities to Areas
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_ents = json.loads(await ws.recv()).get('result', [])

        msg_id += 1        
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        all_devs = {d['id']: d for d in json.loads(await ws.recv()).get('result', [])}

        ignore_domains = ['zone', 'sun']
        valid_eids = []
        area_entities = {a: [] for a in target_areas}
        
        print("--- Assigning Areas ---")
        for e in all_ents:
            eid = e['entity_id']
            domain = eid.split('.')[0]
            if domain in ignore_domains or e.get('disabled_by'):
                continue
                
            ename = e.get('name') or e.get('original_name') or ''
            dev = all_devs.get(e.get('device_id'), {})
            dname = dev.get('name', '')
            platform = e.get('platform', '')
            
            full_identifier = f"{ename} {dname} {eid}".lower()
            
            assigned_area = None
            # Find matching area string
            for ta in target_areas:
                if ta in full_identifier:
                    assigned_area = ta
                    break
            
            # Additional context logic
            if not assigned_area:
                if "마이크" in full_identifier or "스피커" in full_identifier or "선풍기" in full_identifier or "히터" in full_identifier or "침대" in full_identifier or "매트" in full_identifier:
                    assigned_area = "안방"
                elif "제습기" in full_identifier:
                    assigned_area = "옷방"
                elif "플러그" in full_identifier and "테라스" in full_identifier:
                    assigned_area = "거실"
            
            valid_eids.append(eid)
            
            if assigned_area:
                area_entities[assigned_area].append(eid)
                # Update Entity Registry
                if e.get('area_id') != area_map[assigned_area]:
                    msg_id += 1
                    await ws.send(json.dumps({
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": eid,
                        "area_id": area_map[assigned_area]
                    }))
                    await ws.recv()
                
        # 3. Build Lovelace Dashboard
        print("--- Rebuilding Lovelace ---")
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        config = res.get("result", {})
        
        if not config or "views" not in config:
            config = {"views": [{"title": "Home", "path": "default_view", "cards": []}]}
            
        new_cards = []
        
        # Weather first
        weathers = [e for e in valid_eids if e.startswith("weather.")]
        if weathers:
            new_cards.append({"type": "weather-forecast", "entity": weathers[0], "show_forecast": False})

        # Person second
        persons = [e for e in valid_eids if e.startswith("person.")]
        if persons:
            new_cards.append({"type": "entities", "entities": persons})

        # Room Cards
        for ta in target_areas:
            ents = area_entities[ta]
            if ents:
                clean_ents = []
                noise_keywords = ["_closest_target_distance", "_sensitivity", "_near_detection", "_far_detection", "battery", "update.", "scene.", "_tilt", "_drop", "_vibration", "_tamper", "_power_on_behavior", "_indicator_light_mode", "_voltage", "_current", "_total_energy", "_power", "gasang", "scene"]
                # some extra noise we observed
                for e in ents:
                    if not any(k in e for k in noise_keywords) and e not in clean_ents:
                        clean_ents.append(e)
                
                # sort lights/switches to top, sensors to bottom visually
                # We sort boolean (lights/switches/binary) first, numbers/sensors last
                def sorter(eid):
                    d = eid.split('.')[0]
                    if d in ['light', 'switch']: return 0
                    if d in ['binary_sensor', 'cover', 'fan', 'humidifier', 'climate']: return 1
                    if d in ['sensor', 'number', 'select']: return 2
                    return 3
                    
                clean_ents.sort(key=lambda x: (sorter(x), x))
                
                if clean_ents:
                    new_cards.append({
                        "type": "entities",
                        "title": ta,
                        "entities": clean_ents
                    })
        
        config["views"][0]["cards"] = new_cards
        
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Areas Assigned and Dashboard Successfully Rebuilt!")

asyncio.run(run())
