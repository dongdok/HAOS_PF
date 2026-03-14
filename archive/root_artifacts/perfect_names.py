import os, json, asyncio, websockets
from dotenv import load_dotenv

async def run():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()

        # 1. Fetch valid entities
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_ents = json.loads(await ws.recv()).get('result', [])
        valid_eids = {e['entity_id'] for e in all_ents if not e.get('disabled_by')}
        
        safe_domains = ['person', 'weather', 'sun', 'zone']
        
        # 2. Fetch current lovelace config
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if not res.get("success"): return
            
        config = res.get("result", {})
        if not config or "views" not in config or not config["views"]: return
            
        view = config["views"][0]
        
        # We will iterate and build a shiny new entities list for each card
        for c in view.get("cards", []):
            if c.get("type") == "entities":
                new_ents = []
                for e in c.get("entities", []):
                    eid = e if isinstance(e, str) else e.get("entity", "")
                    domain = eid.split('.')[0] if '.' in eid else ''
                    
                    # Remove "Not Found" entities
                    if domain not in safe_domains and eid not in valid_eids:
                        continue 
                        
                    # Calculate a nice name
                    name_override = None
                    if "1caegsangseonpunggi_2maikeu_3seupikeo" in eid:
                        if "switch_1" in eid: name_override = "책상선풍기"
                        elif "switch_2" in eid: name_override = "책상 마이크"
                        elif "switch_3" in eid: name_override = "책상 스피커"
                        elif "child_lock" in eid: name_override = "멀티탭 잠금"
                    elif "cimdaebul1_meorimatjaesil2_cimdaeseonpunggi3" in eid:
                        if "switch_1" in eid: name_override = "침대불"
                        elif "switch_2" in eid: name_override = "머리맡 재실"
                        elif "switch_3" in eid: name_override = "침대 선풍기"
                    elif "2jubang_jaesil_3deuraigibul" in eid:
                        if "switch_1" in eid: name_override = "주방 재실"
                        elif "switch_2" in eid: name_override = "드라이기불"
                    elif "child_lock" in eid: name_override = "어린이 보호 잠금"
                    elif "socket_1" in eid: name_override = "플러그 전원"
                    elif "filter_reset" in eid: name_override = "필터 리셋"
                    elif "ionizer" in eid: name_override = "이오나이저"
                    elif eid.endswith("_switch_1") or eid.endswith("_switch_2") or eid.endswith("_switch_3"):
                        name_override = "스위치"
                    elif "power_on_behavior" in eid: name_override = "초기 전원 설정"
                    elif "indicator_light_mode" in eid: name_override = "상태등 설정"
                    elif "_current" in eid: name_override = "전류"
                    elif "_voltage" in eid: name_override = "전압"
                    elif "_power" in eid: name_override = "전력"
                    elif "_total_energy" in eid: name_override = "누적 전력량"
                    elif "_humidity" in eid: name_override = "습도"
                    elif "_temperature" in eid: name_override = "온도"
                    elif "occupancy" in eid: name_override = "재실 상태"
                    elif "door" in eid: name_override = "열림 상태"
                    
                    if name_override:
                        new_ents.append({"entity": eid, "name": name_override})
                    elif isinstance(e, dict) and e.get("name") in ["Socket", "Switch", "Unknown"]:
                        # remove the bad hardcoded english name so it falls back to device name, or provide a generic
                        new_ents.append({"entity": eid, "name": "스위치"})
                    else:
                        new_ents.append(e) # keep as is
                        
                c["entities"] = new_ents
                
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Dashboard perfectly cleansed and named!")

asyncio.run(run())
