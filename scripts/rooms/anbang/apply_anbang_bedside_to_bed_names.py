import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


UPDATES = {
    "switch.anbang_bedside_light": "안방 침대 조명",
    "switch.anbang_bedside_fan": "안방 침대 선풍기",
    "binary_sensor.anbang_bedside_presence": "안방 침대 재실 감지",
    "switch.anbang_bedside_presence_switch": "안방 침대 재실 스위치",
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

        msg_id = 2000
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
