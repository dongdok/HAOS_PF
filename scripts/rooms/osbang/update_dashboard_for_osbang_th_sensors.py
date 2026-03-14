import asyncio
import json
import os
from pathlib import Path

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

        await ws.send(json.dumps({"id": 1, "type": "lovelace/config"}))
        config = json.loads(await ws.recv())["result"]

        Path("lovelace_pre_osbang_th_sensor_update.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        target_entities = [
            "sensor.osbang_th_monitor_battery",
            "sensor.osbang_temperature",
            "sensor.osbang_humidity",
        ]
        config["views"][0]["sections"][4]["cards"][3]["entities"] = target_entities
        config["views"][1]["cards"][4]["cards"][1]["cards"][2]["entities"] = target_entities

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Updated dashboard osbang TH sensor references.")


if __name__ == "__main__":
    asyncio.run(main())
