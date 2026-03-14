import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


UPDATES = {
    "switch.jubang_presence_switch": "주방 재실 센서 플러그",
    "switch.jubang_appliance_multitap": "주방 라인 조명 플러그",
    "switch.jubang_multitab_unused1": "주방 멀티탭 예비 1",
}


async def main():
    load_dotenv(".env")
    token = os.getenv("HA_TOKEN", "").strip()
    url = os.getenv("HA_URL", "").strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"

    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()

        msg_id = 1700
        results = []
        for entity_id, name in UPDATES.items():
            msg_id += 1
            await ws.send(json.dumps({
                "id": msg_id,
                "type": "config/entity_registry/update",
                "entity_id": entity_id,
                "name": name,
            }))
            res = json.loads(await ws.recv())
            results.append({
                "entity_id": entity_id,
                "name": name,
                "success": res.get("success", False),
                "error": res.get("error"),
            })

        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
