import os, json, asyncio, websockets
from dotenv import load_dotenv

async def run():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "lovelace/config"}))
        res = json.loads(await ws.recv())
        config = res.get("result", {})
        
        if not config or "views" not in config: return
        
        view = config["views"][0]
        new_cards = []
        
        for c in view.get("cards", []):
            if c.get("type") == "entities" and "title" in c:
                room_title = c["title"]
                
                tiles = []
                for e in c.get("entities", []):
                    eid = e if isinstance(e, str) else e.get("entity", "")
                    
                    # specific tuning for tiles to make them look best
                    tile_card = {
                        "type": "tile",
                        "entity": eid
                    }
                    tiles.append(tile_card)
                
                # Build the beautiful HomeKit structure
                if tiles:
                    new_cards.append({
                        "type": "vertical-stack",
                        "cards": [
                            {
                                "type": "markdown",
                                "content": f"## {room_title}"
                            },
                            {
                                "type": "grid",
                                "columns": 2, # Apple HomeKit uses 2 wide columns generally on mobile
                                "square": False, # Pillow shape instead of perfect squares
                                "cards": tiles
                            }
                        ]
                    })
            else:
                new_cards.append(c) # Keep weather, person, etc. as is
                
        config["views"][0]["cards"] = new_cards
        
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Dashboard successfully transformed into Apple HomeKit style!")

asyncio.run(run())
