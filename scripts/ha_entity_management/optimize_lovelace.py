import os, json, asyncio, websockets
from dotenv import load_dotenv

async def optimize_lovelace():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        # 1. Fetch current Lovelace Config
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        if not res.get("success"):
            print("Failed to get lovelace config. You might need to make sure you have fully accepted the 'Take Control' dialog.")
            print(res)
            return
            
        config = res.get("result", {})
        if not config or "views" not in config or not config["views"]:
            print("No views found in Lovelace config")
            return
            
        view = config["views"][0]
        cards = view.get("cards", [])
        
        new_cards = []
        top_cards = []
        
        unwanted_titles = ["[가상] 헬퍼", "미분류", "이진센서", "센서", "기기제어"]
        noise_keywords = [
            "closest_target_distance", "sensitivity", "near_detection", "far_detection", # radar
            "voltage", "current", "power", "total_energy", # power stats
            "indicator_light_mode", "power_on_behavior", # switch settings
            "_tilt", "_drop", "_vibration", "_tamper", "battery" # mostly hidden sensors
        ]
        
        for c in cards:
            c_type = c.get("type", "")
            title = c.get("title", "")
            
            # Weather and Person go to top
            is_person = False
            if c_type == "entities":
                for e in c.get("entities", []):
                    entity_id = e if isinstance(e, str) else e.get("entity", "")
                    if "person." in entity_id:
                        is_person = True
                        break
                        
            if c_type == "weather-forecast" or is_person:
                top_cards.append(c)
                continue
                
            if title in unwanted_titles:
                continue
                
            if c_type == "entities" and title:
                # Filter noise entities
                new_entities = []
                for e in c.get("entities", []):
                    entity_id = e if isinstance(e, str) else e.get("entity", "")
                    
                    is_noise = any(k in entity_id.lower() for k in noise_keywords)
                    # Filter out any duplicate '진동' names mapping to binary_sensor if desired, but keyword covers it
                    if not is_noise:
                        new_entities.append(e)
                
                if new_entities:
                    c["entities"] = new_entities
                    new_cards.append(c)
            else:
                # Keep other custom cards if any
                new_cards.append(c)
                
        # Combine
        view["cards"] = top_cards + new_cards
        config["views"][0] = view
        
        # 2. Save new Config
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        save_res = json.loads(await ws.recv())
        if save_res.get("success"):
            print("Successfully optimized and saved the Lovelace dashboard!")
        else:
            print("Failed to save lovelace config:")
            print(save_res)

if __name__ == "__main__":
    asyncio.run(optimize_lovelace())
