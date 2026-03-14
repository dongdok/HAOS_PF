import asyncio
import json
import os

import websockets
from dotenv import load_dotenv


RENAMES = [
    ("switch.jubang_ac_heating_plug", "switch.anbang_heater_plug"),
    ("sensor.jubang_ac_heating_current", "sensor.anbang_heater_current"),
    ("sensor.jubang_ac_heating_power", "sensor.anbang_heater_power"),
    ("sensor.jubang_ac_heating_voltage", "sensor.anbang_heater_voltage"),
    ("sensor.jubang_ac_heating_total_energy", "sensor.anbang_heater_total_energy"),
]


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
        msg_id = 100
        for old_id, new_id in RENAMES:
            msg_id += 1
            await ws.send(
                json.dumps(
                    {
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": old_id,
                        "new_entity_id": new_id,
                    }
                )
            )
            res = json.loads(await ws.recv())
            results.append(
                {
                    "old_id": old_id,
                    "new_id": new_id,
                    "success": res.get("success", False),
                    "error": res.get("error"),
                }
            )

        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
