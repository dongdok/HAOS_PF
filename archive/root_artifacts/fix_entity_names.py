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
        
        # 1. Restore previous Lovelace dump (before the massive cut)
        try:
            with open('lovelace_dump.json', 'r') as f:
                dump = json.load(f)
            if dump.get("success"):
                await ws.send(json.dumps({"id": 100, "type": "lovelace/config/save", "config": dump["result"]}))
                await ws.recv()
                print("Restored Lovelace from lovelace_dump.json")
        except Exception as e:
            print("Could not restore Lovelace:", e)
            
        # 2. Fix Entity Names
        msg_id = 101
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv()).get('result', [])
        
        # We need to map things to better names
        print("--- Fixing Missing Entity Names ---")
        for e in entities:
            eid = e['entity_id']
            ename = e.get('name') or e.get('original_name') or ''
            
            # If name is missing, Unknown, Socket, or Switch, we need to fix it.
            if not ename or ename.lower() == 'unknown' or 'socket' in ename.lower() or 'switch' in ename.lower():
                # Let's derive a good name from entity_id
                # light.geosilbul -> 거실불
                # switch.1caegsangseonpunggi_2maikeu_3seupikeo_switch_1
                new_name = None
                domain, name_part = eid.split('.', 1)
                
                # Check specifics
                if '1caegsangseonpunggi_2maikeu_3seupikeo' in name_part:
                    if 'switch_1' in name_part: new_name = '1책상선풍기'
                    elif 'switch_2' in name_part: new_name = '2마이크'
                    elif 'switch_3' in name_part: new_name = '3스피커'
                elif 'switch_1' in name_part: new_name = '1구'
                elif 'switch_2' in name_part: new_name = '2구'
                elif 'switch_3' in name_part: new_name = '3구'
                elif 'switch_4' in name_part: new_name = '4구'
                elif 'socket_1' in name_part: new_name = '플러그'
                elif 'child_lock' in name_part: new_name = '차일드락'
                elif 'filter_reset' in name_part: new_name = '필터리셋'
                elif 'ionizer' in name_part: new_name = '이오나이저'
                
                # Only update if we derived a better name or if it still says Unknown
                if new_name or ename.lower() == 'unknown' or not ename:
                    final_name = new_name if new_name else name_part.replace('_', ' ').capitalize()
                    print(f"Updating {eid} name to {final_name}")
                    msg_id += 1
                    await ws.send(json.dumps({
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": eid,
                        "name": final_name
                    }))
                    await ws.recv()

asyncio.run(run())
