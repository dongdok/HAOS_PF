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

        Path("lovelace_pre_geosil_card_layout_fix.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        view0_cards = config["views"][0]["sections"][1]["cards"]
        view0_cards[1]["entity"] = "switch.geosil_ceiling_light"
        view0_cards[2]["entity"] = "light.geosil_stand_lighting"
        view0_cards[3]["entity"] = "switch.geosil_line_lighting_plug"
        view0_cards[4]["entity"] = "light.geosil_line_lighting"

        view1_cards = config["views"][1]["cards"][3]["cards"][1]["cards"]
        view1_cards[0]["entity"] = "switch.geosil_ceiling_light"
        view1_cards[1]["entity"] = "light.geosil_stand_lighting"
        view1_cards[2]["entity"] = "switch.geosil_line_lighting_plug"
        view1_cards[3]["entity"] = "light.geosil_line_lighting"

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Fixed geosil card layout.")


if __name__ == "__main__":
    asyncio.run(main())
