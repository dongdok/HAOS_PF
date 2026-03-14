import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


UPDATES = {
    "switch.anbang_main_light": "안방 조명",
    "binary_sensor.anbang_presence": "안방 재실 감지",
    "binary_sensor.anbang_bedside_presence": "안방 원 진동 감지",
    "scene.anbangjomyeong_1peo": "안방 조명 1%",
    "scene.anbangjomyeong_100peo": "안방 조명 100%",
    "sensor.anbang_humidifier_current": "안방 가습기 전류",
    "sensor.anbang_humidifier_power": "안방 가습기 전력",
    "sensor.anbang_humidifier_voltage": "안방 가습기 전압",
    "sensor.anbang_humidifier_total_energy": "안방 가습기 총 에너지",
    "sensor.anbang_electric_blanket_current": "안방 전기장판 전류",
    "sensor.anbang_electric_blanket_power": "안방 전기장판 전력",
    "sensor.anbang_electric_blanket_voltage": "안방 전기장판 전압",
    "sensor.anbang_electric_blanket_total_energy": "안방 전기장판 총 에너지",
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

        msg_id = 10
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
                }
            )

        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
