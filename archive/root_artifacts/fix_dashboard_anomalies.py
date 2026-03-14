import os, json, asyncio, websockets
from dotenv import load_dotenv

async def fix_dashboard():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_entities = json.loads(await ws.recv()).get('result', [])
        
        # Build set of valid entity IDs and a map of their names
        valid_eids = {e['entity_id'] for e in all_entities if not e.get('disabled_by')}
        eid_to_name = {e['entity_id']: (e.get('name') or e.get('original_name') or '') for e in all_entities}
        
        # We also need to consider entities that are natively provided by HA and not in the registry (like some weather, persons)
        # So we won't strictly delete everything not in valid_eids if they are typical HA domains
        safe_domains = ['person', 'weather', 'sun', 'zone']
        
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if not res.get("success"): return
            
        config = res.get("result", {})
        if not config or "views" not in config or not config["views"]: return
            
        view = config["views"][0]
        
        # Additional aggressive filters
        bad_keywords = ["unknown", "socket", "switch_1", "switch_2", "switch_3", "switch_4"]
        
        for c in view.get("cards", []):
            if c.get("type") == "entities":
                new_ents = []
                for e in c.get("entities", []):
                    eid = e if isinstance(e, str) else e.get("entity", "")
                    domain = eid.split('.')[0] if '.' in eid else ''
                    
                    # 1. Check if entity actually exists and is active
                    if domain not in safe_domains and eid not in valid_eids:
                        continue # "구성 요소를 찾을 수 없음" fix
                        
                    # 2. Check name for "Unknown" or "Socket"
                    ename = eid_to_name.get(eid, '').lower()
                    if any(b in ename for b in bad_keywords):
                        continue # "거실 Unknown" and "거실 Socket" fix
                        
                    # 3. Check eid itself for "_socket" or "_switch_1"
                    if any(b in eid.lower() for b in bad_keywords):
                        continue
                        
                    new_ents.append(e)
                    
                c["entities"] = new_ents
                
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Anomaly fix complete!")

asyncio.run(fix_dashboard())
