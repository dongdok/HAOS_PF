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
        
        # 1. Fetch Area
        await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
        areas = json.loads(await ws.recv())["result"]
        msg_id += 1
        raw_area_id = next((a["area_id"] for a in areas if a.get("name") == "[RAW] 중복/미사용"), None)
        
        # 2. Fetch Devices & Entities
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv())["result"]
        msg_id += 1
        
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv())["result"]
        msg_id += 1
        
        st_entities = [e for e in entities if e["platform"] == "smartthings"]
        st_device_ids = {e["device_id"] for e in st_entities if e.get("device_id")}
        st_devices = [d for d in devices if d["id"] in st_device_ids]
        st_standalone_entities = [e for e in st_entities if not e.get("device_id")]
        
        disable_device_ids = []
        disable_entity_ids = []
        
        allowed_mfg = ["samsung electronics", "samsung", "goqual"]
        
        for d in st_devices:
            mfg = (d.get("manufacturer") or "").lower().strip()
            
            # Keep Samsung/Goqual native devices
            if mfg in allowed_mfg:
                continue
            
            # The rest are Tuya duplicates imported through ST
            disable_device_ids.append(d["id"])
            
            # Disable all their entities
            for e in st_entities:
                if e.get("device_id") == d["id"]:
                    disable_entity_ids.append(e["entity_id"])
                    
        for e in st_standalone_entities:
            disable_entity_ids.append(e["entity_id"])
            
        print(f"Planning to disable {len(disable_device_ids)} Devices and {len(disable_entity_ids)} Entities.")
        
        # Execute Disable
        disabled_ent_count = 0
        disabled_dev_count = 0
        
        for eid in disable_entity_ids:
             ent = next((x for x in st_entities if x["entity_id"] == eid), None)
             if ent and ent.get("disabled_by"):
                 continue
                 
             payload = {"id": msg_id, "type": "config/entity_registry/update", "entity_id": eid, "disabled_by": "user"}
             if raw_area_id: payload["area_id"] = raw_area_id
             await ws.send(json.dumps(payload))
             await ws.recv()
             msg_id += 1
             disabled_ent_count += 1
             
        for did in disable_device_ids:
             dev = next((x for x in st_devices if x["id"] == did), None)
             if dev and dev.get("disabled_by"):
                 continue
                 
             payload = {"id": msg_id, "type": "config/device_registry/update", "device_id": did, "disabled_by": "user"}
             if raw_area_id: payload["area_id"] = raw_area_id
             await ws.send(json.dumps(payload))
             await ws.recv()
             msg_id += 1
             disabled_dev_count += 1
             
        print(f"Successfully disabled {disabled_dev_count} ST Tuya Duplicate devices and {disabled_ent_count} ST Tuya Duplicate entities.")

asyncio.run(run())
