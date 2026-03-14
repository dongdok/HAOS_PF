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
        
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_ents = json.loads(await ws.recv()).get('result', [])
        
        print("--- Current Tuya/Active Entities ---")
        # Let's filter out standard system stuff
        ignore_domains = ['zone', 'sun', 'person', 'weather']
        
        results = []
        for e in all_ents:
            eid = e['entity_id']
            domain = eid.split('.')[0]
            if domain in ignore_domains: continue
            if e.get('disabled_by'): continue # ignore disabled
            
            # Print if platform is tuya or smartthings, or just print all active to be safe
            platform = e.get('platform', '')
            ename = e.get('name') or e.get('original_name') or 'N/A'
            
            if platform in ['tuya', 'smartthings', 'localtuya']:
                results.append((platform, eid, ename))
                
        # sort by platform then name
        results.sort(key=lambda x: (x[0], x[2]))
        
        for p, i, n in results:
            print(f"[{p.upper()}] {i} -> {n}")

asyncio.run(check())
