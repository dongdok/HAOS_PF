import asyncio
import json
import os
from pathlib import Path

import websockets
from dotenv import load_dotenv


REPLACEMENTS = {
    "switch.geosilbul": "switch.geosil_lighting",
    "switch.keoteunbul": "switch.geosil_curtain_lighting_plug",
    "binary_sensor.geosil_jaesilsenseo_occupancy": "binary_sensor.geosil_presence",
    "media_player.43_smart_monitor_m7": "media_player.geosil_tv",
    "sensor.light_sensor_43_smart_monitor_m7_illuminance": "sensor.geosil_tv_illuminance",
    "switch.jubangbul": "switch.jubang_main_light",
    "binary_sensor.jubang_jaesil_senseo_occupancy": "binary_sensor.jubang_presence",
    "switch.2jubang_jaesil_3deuraigibul_switch_2": "switch.jubang_presence_switch",
    "switch.deuraigi": "switch.jubang_dryer_plug",
    "switch.jubang_dryer_plug": "switch.jubang_hair_dryer",
    "switch.hwajangsil_bul": "switch.hwajangsil_lighting",
    "switch.hwajangsil_hwanpunggi": "switch.hwajangsil_lighting_fan",
    "binary_sensor.hwajangsil_doeosenseo_door": "binary_sensor.hwajangsil_door_contact",
    "binary_sensor.hwajangsil_jaesilsenseo_occupancy": "binary_sensor.hwajangsil_presence",
    "switch.osbangbul": "switch.osbang_main_light",
    "binary_sensor.osbang_jaesilsenseo_occupancy": "binary_sensor.osbang_presence",
    "humidifier.jeseubgi": "humidifier.osbang_dehumidifier",
    "switch.anbangbul": "switch.anbang_main_light",
    "switch.1caegsangseonpunggi": "switch.anbang_desk_fan",
    "switch.1caegsangseonpunggi_2maikeu_3seupikeo_switch_2": "switch.anbang_desk_mic",
    "switch.3seupikeo": "switch.anbang_desk_speaker",
    "switch.1cimdaedeung_seuwici": "switch.anbang_bedside_light",
    "switch.2meorimat_jaesil_seuwici": "switch.anbang_bedside_presence_switch",
    "switch.3cimdaeseonpunggi": "switch.anbang_bedside_fan",
    "switch.jeongimaeteu": "switch.anbang_electric_blanket",
    "switch.eeokeon_nanbang_on_off_socket_1": "switch.jubang_ac_heating_plug",
    "binary_sensor.anbang_jaesilsenseo_occupancy": "binary_sensor.anbang_presence",
    "binary_sensor.anbang_round_vibration": "binary_sensor.anbang_bedside_presence",
    "climate.hiteo": "climate.anbang_heater",
    "cover.curtain": "cover.anbang_curtain",
    "switch.gaseubgi": "switch.anbang_humidifier",
}


def replace_entities(node):
    if isinstance(node, dict):
        entity_id = node.get("entity")
        if isinstance(entity_id, str) and entity_id in REPLACEMENTS:
            node["entity"] = REPLACEMENTS[entity_id]
        entities = node.get("entities")
        if isinstance(entities, list):
            for item in entities:
                if isinstance(item, dict):
                    entity_id = item.get("entity")
                    if isinstance(entity_id, str) and entity_id in REPLACEMENTS:
                        item["entity"] = REPLACEMENTS[entity_id]
        for value in node.values():
            replace_entities(value)
    elif isinstance(node, list):
        for item in node:
            replace_entities(item)


def fix_geosil_entities_card(config):
    # Replace stale Smart Monitor switch references with currently live sensors.
    config["views"][1]["cards"][3]["cards"][3]["entities"] = [
        {"entity": "sensor.geosil_tv_illuminance"},
        {"entity": "sensor.geosil_tv_brightness", "secondary_info": "none"},
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

        await ws.send(json.dumps({"id": 1, "type": "lovelace/config"}))
        config = json.loads(await ws.recv())["result"]

        Path("lovelace_pre_live_sync_backup.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        replace_entities(config)
        fix_geosil_entities_card(config)

        Path("lovelace_active.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2)
        )

        await ws.send(json.dumps({"id": 2, "type": "lovelace/config/save", "config": config}))
        result = json.loads(await ws.recv())
        if not result.get("success"):
            raise RuntimeError(f"Save failed: {result}")

        print("Dashboard synced to current live entity set.")


if __name__ == "__main__":
    asyncio.run(main())
