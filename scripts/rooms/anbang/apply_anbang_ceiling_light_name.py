import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


async def main():
    load_dotenv(".env")
    token = os.getenv("HA_TOKEN", "").strip()
    url = os.getenv("HA_URL", "").strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"

    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        await ws.send(json.dumps({
            "id": 800,
            "type": "config/entity_registry/update",
            "entity_id": "switch.anbang_main_light",
            "name": "안방 천장 조명",
        }))
        res = json.loads(await ws.recv())
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
