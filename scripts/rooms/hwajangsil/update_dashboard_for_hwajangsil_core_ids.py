import asyncio
import json
import os
from pathlib import Path

import websockets
from dotenv import load_dotenv


REPLACEMENTS = {
    "switch.hwajangsil_lighting": "switch.hwajangsil_ceiling_light",
    "switch.hwajangsil_lighting_fan": "switch.hwajangsil_vent_fan",
}


def walk(node):
    if isinstance(node, dict):
        entity_id = node.get("entity")
        if entity_id in REPLACEMENTS:
            node["entity"] = REPLACEMENTS[entity_id]
        entities = node.get("entities")
        if isinstance(entities, list):
            for i, item in enumerate(entities):
                if isinstance(item, str) and item in REPLACEMENTS:
                    entities[i] = REPLACEMENTS[item]
                elif isinstance(item, dict) and item.get("entity") in REPLACEMENTS:
                    item["entity"] = REPLACEMENTS[item["entity"]]
        for value in node.values():
            walk(value)
    elif isinstance(node, list):
        for item in node:
            walk(item)


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

        Path("lovelace_pre_hwajangsil_core_update.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        walk(config)

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Updated dashboard hwajangsil core references.")


if __name__ == "__main__":
    asyncio.run(main())
