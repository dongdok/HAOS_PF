import asyncio
import json
import os
from copy import deepcopy
from pathlib import Path

import websockets
from dotenv import load_dotenv


REPLACEMENTS = {
    "switch.geosil_lighting": "switch.geosilbul",
    "switch.geosil_curtain_lighting_plug": "switch.keoteunbul",
    "light.geosil_curtain_lighting": "switch.keoteunbul",
    "binary_sensor.geosil_presence": "binary_sensor.geosil_jaesilsenseo_occupancy",
    "media_player.geosil_tv": "media_player.43_smart_monitor_m7",
    "switch.jubang_main_light": "switch.jubangbul",
    "binary_sensor.jubang_presence": "binary_sensor.jubang_jaesil_senseo_occupancy",
    "switch.jubang_appliance_multitap": "switch.2jubang_jaesil_3deuraigibul_switch_2",
    "switch.jubang_dryer_plug": "switch.deuraigi",
    "switch.hwajangsil_lighting": "switch.hwajangsil_bul",
    "switch.hwajangsil_lighting_fan": "switch.hwajangsil_hwanpunggi",
    "binary_sensor.hwajangsil_door_contact": "binary_sensor.hwajangsil_doeosenseo_door",
    "binary_sensor.hwajangsil_presence": "binary_sensor.hwajangsil_jaesilsenseo_occupancy",
    "switch.osbang_main_light": "switch.osbangbul",
    "binary_sensor.osbang_presence": "binary_sensor.osbang_jaesilsenseo_occupancy",
    "humidifier.osbang_dehumidifier": "humidifier.jeseubgi",
    "switch.anbang_main_light": "switch.anbangbul",
    "switch.anbang_desk_fan": "switch.1caegsangseonpunggi_2maikeu_3seupikeo_switch_1",
    "switch.anbang_desk_mic": "switch.1caegsangseonpunggi_2maikeu_3seupikeo_switch_2",
    "switch.anbang_desk_speaker": "switch.1caegsangseonpunggi_2maikeu_3seupikeo_switch_3",
    "switch.anbang_bedside_light": "switch.1cimdaedeung_seuwici",
    "switch.anbang_bedside_presence_switch": "switch.2meorimat_jaesil_seuwici",
    "switch.anbang_bedside_fan": "switch.3cimdaeseonpunggi",
    "switch.anbang_electric_blanket_plug": "switch.jeongimaeteu",
    "switch.jubang_ac_heating_plug": "switch.eeokeon_nanbang_on_off_socket_1",
    "binary_sensor.anbang_presence": "binary_sensor.anbang_jaesilsenseo_occupancy",
    "cover.anbang_curtain": "cover.curtain",
    "switch.anbang_humidifier": "switch.gaseubgi",
    "sensor.geosil_tv_illuminance": "sensor.light_sensor_43_smart_monitor_m7_illuminance",
    "climate.anbang_heater": "climate.hiteo",
}


def replace_entities(node, stats):
    if isinstance(node, dict):
        if isinstance(node.get("entity"), str):
            entity_id = node["entity"]
            replacement = REPLACEMENTS.get(entity_id)
            if replacement:
                node["entity"] = replacement
                stats["replaced"].append((entity_id, replacement))
        if isinstance(node.get("entities"), list):
            for item in node["entities"]:
                if isinstance(item, dict) and isinstance(item.get("entity"), str):
                    entity_id = item["entity"]
                    replacement = REPLACEMENTS.get(entity_id)
                    if replacement:
                        item["entity"] = replacement
                        stats["replaced"].append((entity_id, replacement))
        for value in node.values():
            replace_entities(value, stats)
    elif isinstance(node, list):
        for item in node:
            replace_entities(item, stats)


async def main():
    load_dotenv(".env")
    token = os.getenv("HA_TOKEN", "").strip()
    url = os.getenv("HA_URL", "").strip()
    if not token or not url:
        raise RuntimeError("Missing HA_TOKEN or HA_URL in .env")

    ws_url = url.replace("http://", "ws://") + "/api/websocket"

    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth = json.loads(await ws.recv())
        if auth.get("type") != "auth_ok":
            raise RuntimeError("Home Assistant websocket auth failed")

        await ws.send(json.dumps({"id": 1, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        config = res.get("result", {})
        if "views" not in config:
            raise RuntimeError("Lovelace config missing views")

        backup_path = Path("lovelace_pre_safe_replace_backup.json")
        backup_path.write_text(json.dumps(config, ensure_ascii=False, indent=2))

        new_config = deepcopy(config)
        stats = {"replaced": []}
        replace_entities(new_config, stats)

        Path("lovelace_active.json").write_text(
            json.dumps(new_config, ensure_ascii=False, indent=2)
        )

        await ws.send(
            json.dumps({"id": 2, "type": "lovelace/config/save", "config": new_config})
        )
        save_res = json.loads(await ws.recv())
        if not save_res.get("success"):
            raise RuntimeError(f"Lovelace save failed: {save_res}")

        unique = sorted(set(stats["replaced"]))
        print(json.dumps({"replaced_count": len(stats["replaced"]), "unique_replacements": unique}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
