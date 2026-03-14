import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


UPDATES = {
    "binary_sensor.hyeongwan_door": "현관 도어 센서",
    "sensor.hyeongwan_door_battery": "현관 도어 센서 배터리",
    "binary_sensor.hyeongwan_door_tamper": "현관 도어 변조 감지",
    "switch.hyeongwan_outing_virtual_1": "현관 외출 가상 스위치 1",
    "switch.hyeongwan_outing_virtual_2": "현관 외출 가상 스위치 2",
}


async def main():
    load_dotenv(".env")
    token = os.getenv("HA_TOKEN", "").strip()
    url = os.getenv("HA_URL", "").strip().strip('"').strip("'")
    ws_url = url.replace("http://", "ws://") + "/api/websocket"

    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()

        msg_id = 2600
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
