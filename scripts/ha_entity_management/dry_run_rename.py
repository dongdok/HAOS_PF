import os, json, asyncio, websockets
from dotenv import load_dotenv

async def dry_run():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    
    async with websockets.connect(ws_url) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        
        # Get areas
        await ws.send(json.dumps({"id": 1, "type": "config/area_registry/list"}))
        res1 = json.loads(await ws.recv())
        areas_dict = {a['area_id']: a['name'] for a in res1.get('result', [])}
        
        # Get devices
        await ws.send(json.dumps({"id": 2, "type": "config/device_registry/list"}))
        res2 = json.loads(await ws.recv())
        devices = [d for d in res2.get('result', []) if not d.get('disabled_by')]
        
        # Get entities
        await ws.send(json.dumps({"id": 3, "type": "config/entity_registry/list"}))
        res3 = json.loads(await ws.recv())
        entities = [e for e in res3.get('result', []) if not e.get('disabled_by')]
        
        # Map device to entities
        dev_to_entities = {}
        for e in entities:
            dev_id = e.get('device_id')
            if dev_id:
                dev_to_entities.setdefault(dev_id, []).append(e)

        print("## 로직 변경 매핑 시뮬레이션 (Dry Run)")
        print("\n| 기기 및 엔티티 | 기존 영역 | 기존 이름 | ➡️ | 제안 영역 | 제안 이름 | 제안 엔티티 ID |")
        print("|---|---|---|---|---|---|---|")

        def target_area_logic(name, default_area):
            # 시스템 기기들
            sys_keywords = ['Backup', 'Terminal', 'Duck DNS', 'File editor', 'Forecast', 'Home Assistant', 'Matter', 'Mosquitto', 'Samba', 'Studio Code Server', 'Tailscale']
            if any(k in name for k in sys_keywords) or default_area == 'Unassigned' and 'Apple' not in name:
                return '시스템/애드온'
            if 'Apple' in name or 'iPad' in name or 'iPhone' in name:
                return '기기제어'

            name_lower = name.lower()
            if '안방' in name_lower or '침대' in name_lower or '바디럽' in name_lower: return '안방'
            if '거실' in name_lower or 'm7' in name_lower or '테라스' in name_lower: return '거실'
            if '주방' in name_lower: return '주방'
            if '옷방' in name_lower: return '옷방'
            if '화장실' in name_lower: return '화장실'
            if '현관' in name_lower: return '현관'
            if '가상' in name_lower or '일단가상' in name_lower or '굿나잇' in name_lower or '외출' in name_lower: return '[가상] 헬퍼'
            
            return default_area if default_area not in ['센서', 'Unassigned'] else '미분류'
            
        def rename_logic(name, area):
            clean = name.replace('일단가상', '가상').replace('1', '').replace('2', '').replace('3', '').replace('4', '').strip()
            if '가상' in area:
                if '[가상]' not in clean:
                    clean = f"[가상] {clean}".replace('가상스위치', '스위치').replace('가상 스위치', '스위치')
            else:
                if area not in clean and area not in ['시스템/애드온', '기기제어', '미분류']:
                    clean = f"{area} {clean}"
            
            # 띄어쓰기 교정
            clean = clean.replace('재실센서', '재실 센서').replace('창문센서', '창문 센서').replace('도어센서', '도어 센서')
            clean = clean.replace('온습도센서', '온습도 센서').replace('진동센서', '진동 센서')
            # 잉여 숫자나 너무 긴 템플릿 정리 (직접 매핑은 위험하므로 규칙 기반만)
            return ' '.join(clean.split())
            
        def make_entity_id(domain, new_name):
            import re
            # 한글을 로마자로 변환하는 것은 파이썬 외부 라이브러리 없이는 힘들기 때문에
            # 엔티티 ID는 기존 이름을 유지하되 사용자에게 경고만 할지 고민됨.
            # HA가 자체적으로 제공하는 Generate Entity ID 기능은 프론트엔드 로직이므로
            # 스크립트에서는 entity_id를 강제 변경하지 않는 것이 안전함 (자동화 깨짐 방지).
            return "유지 혹은 직접 변경 권장"

        for d in devices:
            old_area = areas_dict.get(d.get('area_id'), 'Unassigned')
            if old_area in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                continue
            
            old_name = d.get('name', 'Unknown')
            new_area = target_area_logic(old_name, old_area)
            new_name = rename_logic(old_name, new_area)
            
            if new_area == '시스템/애드온': # Don't touch system add-ons to avoid mess
                continue
                
            print(f"| **기기** | {old_area} | {old_name} | ➡️ | **{new_area}** | **{new_name}** | - |")
            
            ents = dev_to_entities.get(d['id'], [])
            for e in ents:
                e_old_name = e.get('name', '') or e.get('original_name', 'Unknown')
                e_old_id = e.get('entity_id')
                e_domain = e_old_id.split('.')[0]
                e_new_name = rename_logic(e_old_name, new_area)
                if e_new_name == new_name:
                    e_new_name = f"{new_name} ({e_domain})" # differentiate
                print(f"| ↳ 엔티티 | {old_area} | {e_old_name} | ➡️ | {new_area} | {e_new_name} | {e_old_id} |")

if __name__ == "__main__":
    asyncio.run(dry_run())
