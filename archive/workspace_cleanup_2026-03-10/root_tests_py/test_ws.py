import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)

HA_URL = "ws://ha.story-nase.ts.net:8123/api/websocket"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkNDE1MTUwZjc1NjM0MGI4ODA4NzM3YTQ5NDQzMmQ2NCIsImlhdCI6MTc2MzQ1MDQ2MiwiZXhwIjoyMDc4ODEwNDYyfQ.X5IUX6eRDFe0M3SYI1krqiJ5yrNYTAAIw6xBNDl1pTQ"

async def main():
    async with websockets.connect(HA_URL) as ws:
        auth_msg = await ws.recv()
        print("Auth msg:", auth_msg)
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        auth_ok = await ws.recv()
        print("Auth ok:", auth_ok)
        
        # Init config flow
        msg = {
            "id": 1,
            "type": "config_entries/flow/initialize",
            "handler": "localtuya"
        }
        await ws.send(json.dumps(msg))
        flow_init = await ws.recv()
        resp = json.loads(flow_init)
        print("Flow Init:", json.dumps(resp, indent=2))
        
        if resp.get("success"):
            flow_id = resp["result"]["flow_id"]
            # Abort the flow so we don't leave it hanging
            abort_msg = {
                "id": 2,
                "type": "config_entries/flow/delete",
                "flow_id": flow_id
            }
            await ws.send(json.dumps(abort_msg))
            resp2 = await ws.recv()
            print("Abort Resp:", resp2)

if __name__ == "__main__":
    asyncio.run(main())
