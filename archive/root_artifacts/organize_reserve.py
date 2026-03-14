"""
예비(Reserve) 가상스위치 정리 스크립트
- "예비" 영역(Area) 생성
- "일단가상" 시리즈 + 형제 포트(4구/2구) 엔티티를 "예비" 영역으로 이동
- 이름을 일관되게 통일
- 전부 비활성화(disable)
"""
import os, json, asyncio, websockets
from dotenv import load_dotenv

# 비활성화 + 영역 이동할 "일단가상" 시리즈 엔티티 목록
RESERVE_ENTITIES = {
    # entity_id: new_friendly_name
    "switch.ildangasang_2gu_switch_1":      "[예비] 가상 2구A - 1번포트",
    "switch.ildangasang_2gu_switch_2":      "[예비] 가상 2구A - 2번포트",
    "switch.ildangasang_3gu_switch_1":      "[예비] 가상 3구 - 1번포트",
    "switch.ildangasang4gu_switch_1":       "[예비] 가상 4구A - 1번포트",
    "switch.ildangasang4gu_switch_4":       "[예비] 가상 4구A - 4번포트",
    "switch.ildangasang2gu_4_switch_1":     "[예비] 가상 2구B - 1번포트",
    "switch.ildangasang2gu_4_switch_2":     "[예비] 가상 2구B - 2번포트",
    "switch.ildan_gasang4gu_2_switch_1":    "[예비] 가상 4구B - 1번포트",
    "switch.ildan_gasang4gu_2_switch_4":    "[예비] 가상 4구B - 4번포트",
    "switch.ildangasang_4gu_3_switch_1":    "[예비] 가상 4구C - 1번포트",
    "switch.ildangasang_4gu_3_switch_4":    "[예비] 가상 4구C - 4번포트",
}

async def run():
    load_dotenv('.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://") + "/api/websocket"

    async with websockets.connect(ws_url) as ws:
        await ws.recv()  # auth_required
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_res = json.loads(await ws.recv())
        if auth_res.get("type") != "auth_ok":
            print(f"Auth failed: {auth_res}")
            return

        msg_id = 1

        # 1. Get existing areas
        await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
        existing_areas = json.loads(await ws.recv()).get('result', [])
        area_map = {a['name']: a['area_id'] for a in existing_areas}

        # 2. Create "예비" area if not exists
        if "예비" not in area_map:
            msg_id += 1
            await ws.send(json.dumps({
                "id": msg_id,
                "type": "config/area_registry/create",
                "name": "예비"
            }))
            res = json.loads(await ws.recv())
            if res.get('success'):
                area_map["예비"] = res['result']['area_id']
                print("✅ '예비' 영역 생성 완료")
            else:
                print(f"❌ 영역 생성 실패: {res}")
                return
        else:
            print("ℹ️ '예비' 영역 이미 존재")

        reserve_area_id = area_map["예비"]

        # 3. Get entity registry
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        all_ents = json.loads(await ws.recv()).get('result', [])
        ent_map = {e['entity_id']: e for e in all_ents}

        # 4. Update each reserve entity: rename + move to area + disable
        success_count = 0
        for eid, new_name in RESERVE_ENTITIES.items():
            if eid not in ent_map:
                print(f"⚠️ {eid} - 엔티티 레지스트리에 없음 (이미 삭제됨?)")
                continue

            msg_id += 1
            payload = {
                "id": msg_id,
                "type": "config/entity_registry/update",
                "entity_id": eid,
                "name": new_name,
                "area_id": reserve_area_id,
                "disabled_by": "user"
            }
            await ws.send(json.dumps(payload))
            res = json.loads(await ws.recv())

            if res.get('success'):
                print(f"✅ {eid} -> '{new_name}' | 영역: 예비 | 비활성화됨")
                success_count += 1
            else:
                print(f"❌ {eid} 업데이트 실패: {res.get('error', {}).get('message', '?')}")

        print(f"\n{'='*50}")
        print(f"완료: {success_count}/{len(RESERVE_ENTITIES)} 엔티티 정리됨")
        print(f"영역 '예비' (area_id: {reserve_area_id})에 배정 + 비활성화 완료")

asyncio.run(run())
