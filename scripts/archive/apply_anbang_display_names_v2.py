import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


UPDATES = {
    "number.anbang_jaesilsenseo_sensitivity": "안방 재실 감도",
    "number.anbang_jaesilsenseo_near_detection": "안방 재실 근거리 감지",
    "number.anbang_jaesilsenseo_far_detection": "안방 재실 원거리 감지",
    "number.anbang_jaesilsenseo_closest_target_distance": "안방 재실 최근접 거리",
    "number.anbang_bedside_presence_sensitivity": "안방 머리맡 재실 감도",
    "number.anbang_bedside_presence_near_detection": "안방 머리맡 재실 근거리 감지",
    "number.anbang_bedside_presence_far_detection": "안방 머리맡 재실 원거리 감지",
    "switch.anbang_bedtime_plug": "안방 취침 가상 스위치",
    "switch.anbang_goodnight_plug": "안방 굿나잇 가상 스위치",
    "switch.anbangjomyeong_1peo": "안방 조명 1% 보조 스위치",
    "switch.anbangjomyeong_100peo": "안방 조명 100% 보조 스위치",
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

        results = []
        msg_id = 200
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
