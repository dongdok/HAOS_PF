import os, json, asyncio, websockets
from dotenv import load_dotenv

def undo_transform(cards):
    new_cards = []
    for c in cards:
        # Check if it's a horizontal-stack with 2 or 3 tiles of sensors
        if c.get("type") == "horizontal-stack" and "cards" in c:
            inner_cards = c.get("cards", [])
            if len(inner_cards) in [2, 3]:
                is_target = True
                entities_list = []
                for ic in inner_cards:
                    if ic.get("type") != "tile":
                        is_target = False
                        break
                    eid = ic.get("entity", "")
                    if not eid.startswith("sensor."):
                        is_target = False
                        break
                    entities_list.append(eid)
                
                if is_target:
                    new_cards.append({
                        "type": "entities",
                        "entities": entities_list
                    })
                    continue
        
        # Recurse
        if "cards" in c:
            c["cards"] = undo_transform(c["cards"])
            
        new_cards.append(c)
    return new_cards

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
        
        config["views"][0]["cards"] = undo_transform(config["views"][0].get("cards", []))
        
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Sensors reverted back to original entities list!")

asyncio.run(run())
