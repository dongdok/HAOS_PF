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
        
        # Get Devices
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        devices = json.loads(await ws.recv())["result"]
        msg_id += 1
        
        # Get Entities
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        entities = json.loads(await ws.recv())["result"]
        
        # Separate entities
        tuya_entities = [e for e in entities if e["platform"] == "tuya"]
        st_entities = [e for e in entities if e["platform"] == "smartthings"]
        
        # Map device_id to entities
        st_device_to_entities = {}
        for e in st_entities:
            did = e.get("device_id")
            if did:
                st_device_to_entities.setdefault(did, []).append(e)
                
        # Get Tuya original names for powerful matching
        tuya_entity_orig_names = {e.get("original_name") for e in tuya_entities if e.get("original_name")}
        tuya_device_names = {d.get("name_by_user") or d.get("name") for d in devices if d.get("id") in {e.get("device_id") for e in tuya_entities} }
        tuya_device_names.discard(None)
        
        # We also want to match if ST `name_by_user` or `original_name` matches Tuya
        st_duplicates = []
        st_keepers = []
        
        st_device_ids = set(st_device_to_entities.keys())
        st_devices = [d for d in devices if d["id"] in st_device_ids]
        
        for d in st_devices:
            did = d["id"]
            d_name = d.get("name_by_user") or d.get("name") or "Unknown Device"
            model = d.get("model") or ""
            manufacturer = d.get("manufacturer") or ""
            
            d_entities = st_device_to_entities.get(did, [])
            
            is_duplicate = False
            match_reason = ""
            
            # 1. Device name matches exactly a Tuya device name
            if d_name in tuya_device_names or d.get("name") in tuya_device_names:
                is_duplicate = True
                match_reason = "디바이스 이름이 기존 Tuya 기기와 일치함"
                
            # 2. Entity original name matches a Tuya entity original name
            if not is_duplicate:
                for e in d_entities:
                    orig = e.get("original_name")
                    if orig and orig in tuya_entity_orig_names:
                        is_duplicate = True
                        match_reason = f"엔티티 원본 이름('{orig}')이 Tuya와 동일함"
                        break
            
            # 3. Model / Manufacturer string contains obvious Tuya fingerprints
            if not is_duplicate:
                if "Tuya" in manufacturer or "smartlife" in d_name.lower():
                    is_duplicate = True
                    match_reason = "제조사에 'Tuya' 포함"
                    
            if is_duplicate:
                st_duplicates.append((d, d_entities, match_reason))
            else:
                st_keepers.append((d, d_entities))
                
        # Additional stand-alone entities (no device)
        standalone_st = [e for e in st_entities if not e.get("device_id")]
        if standalone_st:
            st_keepers.append( ({"name": "[단독 엔진] SmartThings 모듈/센서", "model": "N/A", "manufacturer": "System"}, standalone_st) )
                
        # Generate Markdown Report
        md = "# 🔍 스마트띵스(SmartThings) 연동 후 투야(Tuya) 중복 기기 분석 결과\n\n"
        md += "사용 권장 방향: 기존에 세팅된 투야 100% 직접 연동 기기들을 '단일 진실 공급원(SSOT)'으로 남경두고, 스마트띵스를 통해 이중으로 불러와진 투야 기기들의 껍데기와 구성요소는 전면 비활성화(Disable) 처리합니다. (기존 스마트띵스 고유 기기들만 남깁니다.)\n\n"
        
        md += "## 🗑️ 비활성화 대상 (스마트띵스에서 이중으로 불러온 Tuya 기기)\n"
        md += "> 다음 기기들은 기존 Tuya 연동과 완전히 겹치는 것으로 파악되어, **비활성화 후 숨김 처리**해야 할 대상입니다.\n\n"
        if not st_duplicates:
            md += "- 발견된 중복 기기가 없습니다.\n"
        else:
            for d, ents, reason in st_duplicates:
                d_name = d.get('name_by_user') or d.get('name') or 'Unknown'
                md += f"### 🚫 {d_name} (비활성화 예정)\n"
                md += f"- **모델:** {d.get('model', 'Unknown')} | **제조사:** {d.get('manufacturer', 'Unknown')}\n"
                md += f"- **중복 판정 디테일:** {reason}\n"
                md += f"- **포함된 엔티티 수:** {len(ents)}개\n"
                for e in ents:
                    md += f"  - `{e['entity_id']}`\n"
                md += "\n"
                
        md += "---\n\n"
        md += "## ✅ 유지 대상 (본연의 SmartThings 네이티브 기기)\n"
        md += "> 다음 기기들은 Tuya와 겹치지 않는 본연의 삼성/스마트띵스 전용 기기(또는 자체 연동 플랫폼 기기)로 확인되어 **비활성화하지 않고 그대로 유지**합니다.\n\n"
        if not st_keepers:
            md += "- 유지할 네이티브 기기가 발견되지 않았습니다.\n"
        else:
            for d, ents in st_keepers:
                d_name = d.get('name_by_user') or d.get('name') or 'Unknown'
                md += f"### 💡 {d_name} (유지)\n"
                md += f"- **모델:** {d.get('model', 'Unknown')} | **제조사:** {d.get('manufacturer', 'Unknown')}\n"
                md += f"- **포함된 엔티티 수:** {len(ents)}개\n"
                for e in ents:
                    md += f"  - `{e['entity_id']}`\n"
                md += "\n"
        
        os.makedirs('/Users/dy/.gemini/antigravity/brain/68ed4521-aa3f-4b07-afe6-c1a04a9c3acc', exist_ok=True)
        with open('/Users/dy/.gemini/antigravity/brain/68ed4521-aa3f-4b07-afe6-c1a04a9c3acc/st_tuya_analysis.md', 'w') as f:
            f.write(md)
        print("Analysis complete. Saved to st_tuya_analysis.md")

asyncio.run(run())
