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

        # 1. Fetch valid entities and devices
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_ents = json.loads(await ws.recv()).get('result', [])
        
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        all_devs = {d['id']: d for d in json.loads(await ws.recv()).get('result', [])}
        
        # 2. Fix Entity Registry Names
        print("--- Fixing Entity Registry Names ---")
        for e in all_ents:
            eid = e['entity_id']
            ename = e.get('name') or e.get('original_name') or ''
            dev = all_devs.get(e.get('device_id'), {})
            dname = dev.get('name', '')
            
            # If the name is generic, or 'Unknown', or derived from 'switch_1', prefix it with device name.
            # But do NOT rename if it's already well-named (starts with device name or has custom name not 'Unknown').
            if dname and (not ename or ename.lower() in ['unknown', 'socket', 'switch', '스위치', '플러그 전원', '어린이 보호 잠금'] or 'switch_1' in eid or 'socket_1' in eid or 'child_lock' in eid):
                
                # Derive a robust recognizable name
                suffix = ''
                if "1caegsangseonpunggi_2maikeu_3seupikeo" in eid:
                    if "switch_1" in eid: suffix = "책상선풍기"
                    elif "switch_2" in eid: suffix = "마이크"
                    elif "switch_3" in eid: suffix = "스피커"
                elif "cimdaebul1_meorimatjaesil2_cimdaeseonpunggi3" in eid:
                    if "switch_1" in eid: suffix = "침대불"
                    elif "switch_2" in eid: suffix = "머리맡 재실"
                    elif "switch_3" in eid: suffix = "침대 선풍기"
                elif "2jubang_jaesil_3deuraigibul" in eid:
                    if "switch_1" in eid: suffix = "재실"
                    elif "switch_2" in eid: suffix = "드라이기불"
                elif "switch_1" in eid: suffix = "1구"
                elif "switch_2" in eid: suffix = "2구"
                elif "switch_3" in eid: suffix = "3구"
                elif "socket_1" in eid: suffix = "플러그"
                elif "child_lock" in eid: suffix = "잠금"
                elif "power_on_behavior" in eid: suffix = "초기상태"
                elif "indicator_light_mode" in eid: suffix = "상태등"
                elif "_current" in eid: suffix = "전류"
                elif "_voltage" in eid: suffix = "전압"
                elif "_power" in eid: suffix = "전력"
                elif "_total_energy" in eid: suffix = "누적전력량"
                elif "temperature" in eid: suffix = "온도"
                elif "humidity" in eid: suffix = "습도"
                elif "occupancy" in eid: suffix = "재실감지"
                elif "door" in eid: suffix = "문열림"

                if suffix and suffix not in dname:
                    new_name = f"{dname} {suffix}"
                elif suffix:
                    new_name = dname  # if dname already includes the suffix conceptually
                else:
                    new_name = dname
                    
                # avoid renaming things to just identical names
                if ename != new_name:
                    print(f"Update Registry: {eid} -> {new_name}")
                    msg_id += 1
                    await ws.send(json.dumps({
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": eid,
                        "name": new_name
                    }))
                    await ws.recv()

        # 3. Strip UI overrides
        print("--- Stripping UI Overrides ---")
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if res.get("success"):
            config = res.get("result", {})
            if config and "views" in config and config["views"]:
                view = config["views"][0]
                for c in view.get("cards", []):
                    if c.get("type") == "entities":
                        new_ents = []
                        for e in c.get("entities", []):
                            if isinstance(e, dict):
                                # Just keep the entity_id string!
                                eid = e.get("entity")
                                if eid:
                                    new_ents.append(eid)
                            else:
                                new_ents.append(e)
                        c["entities"] = new_ents
                        
                msg_id += 1
                await ws.send(json.dumps({
                    "id": msg_id, 
                    "type": "lovelace/config/save", 
                    "config": config
                }))
                await ws.recv()
                print("Lovelace UI overrides stripped successfully!")

asyncio.run(run())
