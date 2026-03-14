import asyncio
import json
import os
from pathlib import Path

import websockets
from dotenv import load_dotenv


def remove_unused_cards(config):
    # View 0: sections view, jubang section card index 3
    view0_cards = config["views"][0]["sections"][2]["cards"]
    config["views"][0]["sections"][2]["cards"] = [
        card for idx, card in enumerate(view0_cards) if idx != 3
    ]

    # View 1: Home view, jubang grid card index 2
    view1_cards = config["views"][1]["cards"][5]["cards"][1]["cards"]
    config["views"][1]["cards"][5]["cards"][1]["cards"] = [
        card for idx, card in enumerate(view1_cards) if idx != 2
    ]


def replace_scene_cards(config):
    config["views"][0]["sections"][5]["cards"][17]["entity"] = "scene.anbangjomyeong_1peo"
    config["views"][0]["sections"][5]["cards"][18]["entity"] = "scene.anbangjomyeong_100peo"


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

        Path("lovelace_pre_scene_cleanup_backup.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        remove_unused_cards(config)
        replace_scene_cards(config)

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Applied scene replacement and removed unused kitchen tile.")


if __name__ == "__main__":
    asyncio.run(main())
