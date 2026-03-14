import os, json, asyncio, websockets
from dotenv import load_dotenv

async def get_dashboard():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        await ws.send(json.dumps({"id": 1, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        
        with open("lovelace_dump.json", "w") as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
            print("Lovelace config dumped.")

asyncio.run(get_dashboard())
