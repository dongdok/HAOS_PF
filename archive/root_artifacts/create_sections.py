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
        
        main_view = config["views"][0]
        
        # Check if tab already exists, if so remove it to avoid duplicates
        config["views"] = [v for v in config["views"] if v.get("title") != "홈킷 뷰(Sections)"]
        
        sections_view = {
            "title": "홈킷 뷰(Sections)",
            "path": "homekit-sections",
            "type": "sections",
            "icon": "mdi:home-group",
            "sections": []
        }
        
        for vcard in main_view.get("cards", []):
            if vcard.get("type") == "vertical-stack" and "cards" in vcard:
                inner = vcard["cards"]
                if not inner: continue
                first = inner[0]
                
                room_name = ""
                if first.get("type") == "markdown" and "content" in first:
                    content = first["content"]
                    if content.startswith("## "):
                        room_name = content.replace("## ", "").strip()
                
                if room_name:
                    section = {
                        "title": room_name,
                        "cards": []
                    }
                    
                    # Extract and flatten cards
                    for scard in inner[1:]:
                        if scard.get("type") == "grid" and "cards" in scard:
                            section["cards"].extend(scard["cards"])
                        elif scard.get("type") == "horizontal-stack" and "cards" in scard:
                            # Usually horizontal stack has 3 items. They fit perfectly into the Sections grid.
                            section["cards"].extend(scard["cards"])
                        elif scard.get("type") == "entities" and "entities" in scard:
                             for e in scard["entities"]:
                                 eid = e if isinstance(e, str) else e.get("entity", "")
                                 if eid: section["cards"].append({"type": "tile", "entity": eid})
                        else:
                            section["cards"].append(scard)
                            
                    sections_view["sections"].append(section)
        
        # Non-room cards at the root (like weather, person)
        home_section = {
            "title": "집(Home)",
            "cards": []
        }
        for vcard in main_view.get("cards", []):
            if vcard.get("type") != "vertical-stack":
                home_section["cards"].append(vcard)
        
        if home_section["cards"]:
            sections_view["sections"].insert(0, home_section)

        config["views"].append(sections_view)
        
        msg_id += 1
        await ws.send(json.dumps({
            "id": msg_id, 
            "type": "lovelace/config/save", 
            "config": config
        }))
        await ws.recv()
        print("Sections view successfully appended to the dashboard!")

asyncio.run(run())
