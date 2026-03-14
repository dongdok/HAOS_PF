import asyncio
import json
import os
from pathlib import Path

import websockets
from dotenv import load_dotenv


def fix_cards(config):
    views = config.get("views", [])
    if len(views) < 2:
        return

    # 홈킷 뷰(Sections) 거실 TV 센서 horizontal-stack
    sections = views[0].get("sections", [])
    if len(sections) > 1:
        cards = sections[1].get("cards", [])
        for card in cards:
            if card.get("type") == "horizontal-stack":
                inner = card.get("cards", [])
                if len(inner) == 2:
                    inner[0]["entity"] = "sensor.geosil_tv_illuminance"
                    inner[1]["entity"] = "sensor.geosil_tv_brightness"

    # Home 뷰는 이미 entities 카드라 유지하되 안전하게 보정
    cards = views[1].get("cards", [])
    for card in cards:
        if card.get("type") == "vertical-stack":
            stack_cards = card.get("cards", [])
            if len(stack_cards) >= 3 and stack_cards[0].get("content") == "## 거실":
                entities_card = stack_cards[2]
                if entities_card.get("type") == "entities":
                    entities_card["entities"] = [
                        {"entity": "sensor.geosil_tv_illuminance"},
                        {"entity": "sensor.geosil_tv_brightness", "secondary_info": "none"},
                    ]


async def main():
    load_dotenv(".env")
    token = os.getenv("HA_TOKEN", "").strip()
    url = os.getenv("HA_URL", "").strip().strip('"').strip("'")
    ws_url = url.replace("http://", "ws://") + "/api/websocket"

    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()

        await ws.send(json.dumps({"id": 1, "type": "lovelace/config"}))
        config = json.loads(await ws.recv())["result"]

        Path("lovelace_pre_geosil_tv_sensor_card_fix.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        fix_cards(config)

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Updated geosil TV sensor cards.")


if __name__ == "__main__":
    asyncio.run(main())
