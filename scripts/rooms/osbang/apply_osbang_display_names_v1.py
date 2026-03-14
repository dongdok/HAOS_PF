import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


UPDATES = {
    "switch.osbang_main_light": "옷방 천장 조명",
    "number.osbang_presence": "옷방 재실 감도",
    "number.osbang_jaesilsenseo_near_detection": "옷방 재실 근거리 감지",
    "number.osbang_jaesilsenseo_far_detection": "옷방 재실 원거리 감지",
    "number.osbang_jaesilsenseo_closest_target_distance": "옷방 재실 최근접 거리",
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

        msg_id = 2100
        results = []
        for entity_id, name in UPDATES.items():
            msg_id += 1
            await ws.send(
                json.dumps(
                    {
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": entity_id,
                        "name": name,
                    }
                )
            )
            res = json.loads(await ws.recv())
            results.append(
                {
                    "entity_id": entity_id,
                    "name": name,
                    "success": res.get("success", False),
                    "error": res.get("error"),
                }
            )

        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
