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

        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_ents = json.loads(await ws.recv()).get('result', [])
        valid_eids = {e['entity_id'] for e in all_ents if not e.get('disabled_by')}
        
        # We also need to consider entities that are natively provided by HA and not in the registry
        safe_domains = ['person', 'weather', 'sun', 'zone', 'scene']

        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if not res.get("success"): return
            
        config = res.get("result", {})
        if not config or "views" not in config or not config["views"]: return
            
        view = config["views"][0]
        
        for c in view.get("cards", []):
            if c.get("type") == "entities":
                new_ents = []
                for e in c.get("entities", []):
                    eid = e if isinstance(e, str) else e.get("entity", "")
                    domain = eid.split('.')[0] if '.' in eid else ''
                    
                    if domain not in safe_domains and eid not in valid_eids:
                        continue # Skip missing entities entirely
                    
                    new_ents.append(e)
                c["entities"] = new_ents
                
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Missing entities swept!")

asyncio.run(run())
