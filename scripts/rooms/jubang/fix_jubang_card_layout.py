import asyncio
import json
import os
from pathlib import Path

import websockets
from dotenv import load_dotenv


def build_tile(entity_id, vertical=False, features=False):
    card = {"type": "tile", "entity": entity_id}
    if vertical:
        card["vertical"] = False
    if features:
        card["features_position"] = "bottom"
    return card


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

        Path("lovelace_pre_jubang_card_layout_fix.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        section_cards = config["views"][0]["sections"][2]["cards"]
        section_cards[:] = [
            section_cards[0],
            {"type": "tile", "entity": "switch.jubang_ceiling_light", "vertical": False, "features_position": "bottom"},
            {"type": "tile", "entity": "binary_sensor.jubang_presence"},
            {"type": "tile", "entity": "switch.jubang_presence_sensor_plug"},
            {"type": "tile", "entity": "switch.jubang_hair_dryer_plug", "vertical": False, "features_position": "bottom"},
            {"type": "tile", "entity": "switch.jubang_line_lighting_plug"},
            {"type": "tile", "entity": "switch.jubang_ac_remote_hub"},
            {"type": "tile", "entity": "binary_sensor.jubang_round_vibration"},
        ]

        home_cards = config["views"][1]["cards"][5]["cards"][1]["cards"]
        home_cards[:] = [
            {"type": "tile", "entity": "switch.jubang_ceiling_light", "vertical": False, "features_position": "bottom"},
            {"type": "tile", "entity": "binary_sensor.jubang_presence"},
            {"type": "tile", "entity": "switch.jubang_presence_sensor_plug"},
            {"type": "tile", "entity": "switch.jubang_hair_dryer_plug", "vertical": False, "features_position": "bottom"},
            {"type": "tile", "entity": "switch.jubang_line_lighting_plug"},
            {"type": "tile", "entity": "switch.jubang_ac_remote_hub"},
            {"type": "tile", "entity": "binary_sensor.jubang_round_vibration"},
        ]

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Fixed jubang card layout.")


if __name__ == "__main__":
    asyncio.run(main())
