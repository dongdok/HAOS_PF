import os, json, asyncio, websockets
from dotenv import load_dotenv

async def clean():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if not res.get("success"): return
            
        config = res.get("result", {})
        if not config or "views" not in config or not config["views"]: return
            
        view = config["views"][0]
        
        noise_keywords = [
            "closest_target_distance", "sensitivity", "near_detection", "far_detection",
            "voltage", "current", "power", "total_energy",
            "indicator_light_mode", "power_on_behavior",
            "_tilt", "_drop", "_vibration", "_tamper", "battery",
            "update.", "_firmware", "scene.", "_child_lock", "filter_reset", "ionizer",
            "_kyeo", "_ggeo", "_1peo", "_100peo", "1peo", "100peo", "on_off_", "gasang", "firmware",
            "jeongimaeteuon", "hiteo_off", "hiteo_on", "hiteo", "jeongimaeteu_off" # remove random scene proxies
        ]
        
        for c in view.get("cards", []):
            if c.get("type") == "entities":
                new_ents = []
                for e in c.get("entities", []):
                    eid = e if isinstance(e, str) else e.get("entity", "")
                    
                    # specific logic for 안방조명, 거실불 proxy switches vs real light
                    if any(k in eid.lower() for k in noise_keywords):
                        continue
                        
                    # Also keep only the main switches for lights, not switch.geosilbul_switch_1 and switch.geosilbul
                    if eid.endswith("_switch_1") or eid.endswith("_switch_2") or eid.endswith("_switch_3"):
                        # Keep it if there's no better alternative, but typically we want the parent
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
        print("Final clean complete!")

asyncio.run(clean())
