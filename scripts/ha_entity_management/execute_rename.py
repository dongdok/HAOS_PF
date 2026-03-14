import os, json, asyncio, websockets
from dotenv import load_dotenv

async def execute_rename():
    load_dotenv('../../.env')
    token = os.getenv('HA_TOKEN', '').strip()
    url = os.getenv('HA_URL', '').strip()
    ws_url = url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    
    async_sleep_time = 0.05

    def target_area_logic(name, default_area):
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
        
        clean = clean.replace('재실센서', '재실 센서').replace('창문센서', '창문 센서').replace('도어센서', '도어 센서')
        clean = clean.replace('온습도센서', '온습도 센서').replace('진동센서', '진동 센서')
        return ' '.join(clean.split())

    async with websockets.connect(ws_url) as ws:
        msg = await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        msg = await ws.recv()
        
        msg_id = 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/list"}))
        areas_resp = json.loads(await ws.recv()).get('result', [])
        areas_dict = {a['area_id']: a['name'] for a in areas_resp}
        
        # Ensure target areas exist
        needed_areas = ['안방', '거실', '주방', '옷방', '화장실', '현관', '[가상] 헬퍼', '미분류', '기기제어']
        existing_area_names = {a['name']: a['area_id'] for a in areas_resp}
        
        for area_name in needed_areas:
            if area_name not in existing_area_names:
                msg_id += 1
                await ws.send(json.dumps({"id": msg_id, "type": "config/area_registry/create", "name": area_name}))
                res = json.loads(await ws.recv())
                if res.get('success'):
                    existing_area_names[area_name] = res['result']['area_id']
                    print(f"Created new area: {area_name}")
                else:
                    print(f"Failed to create area {area_name}")

        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/device_registry/list"}))
        devices = [d for d in json.loads(await ws.recv()).get('result', []) if not d.get('disabled_by')]
        
        msg_id += 1
        await ws.send(json.dumps({"id": msg_id, "type": "config/entity_registry/list"}))
        entities = [e for e in json.loads(await ws.recv()).get('result', []) if not e.get('disabled_by')]
        
        dev_to_entities = {}
        for e in entities:
            dev_id = e.get('device_id')
            if dev_id:
                dev_to_entities.setdefault(dev_id, []).append(e)

        print("Starting mass update...\n")
        updated_devices = 0
        updated_entities = 0

        for d in devices:
            old_area_id = d.get('area_id')
            old_area_name = areas_dict.get(old_area_id, 'Unassigned')
            if old_area_name in ['[RAW] 중복/미사용', '[SCENE] 보관']:
                continue
            
            old_name = d.get('name', 'Unknown')
            new_area_name = target_area_logic(old_name, old_area_name)
            new_area_id = existing_area_names.get(new_area_name)
            new_name = rename_logic(old_name, new_area_name)
            
            if new_area_name == '시스템/애드온':
                continue
            
            # Update Device
            if old_name != new_name or old_area_id != new_area_id:
                msg_id += 1
                payload = {
                    "id": msg_id,
                    "type": "config/device_registry/update",
                    "device_id": d['id'],
                    "name_by_user": new_name
                }
                if new_area_id:
                    payload["area_id"] = new_area_id
                    
                await ws.send(json.dumps(payload))
                res = await ws.recv()
                print(f"Updated Device: '{old_name}' -> '{new_name}' in Area: {new_area_name}")
                updated_devices += 1
                await asyncio.sleep(async_sleep_time)
            
            # Update Entities
            ents = dev_to_entities.get(d['id'], [])
            for e in ents:
                e_old_name = e.get('name') or e.get('original_name') or 'Unknown'
                e_new_name = rename_logic(e_old_name, new_area_name)
                
                # if entity new_name conflicts with device name exactly, distinguish it
                if e_new_name == new_name:
                    e_domain = e.get('entity_id').split('.')[0]
                    e_new_name = f"{new_name} ({e_domain})"
                
                if e_old_name != e_new_name or e.get('area_id') != new_area_id:
                    msg_id += 1
                    payload = {
                        "id": msg_id,
                        "type": "config/entity_registry/update",
                        "entity_id": e['entity_id'],
                        "name": e_new_name,  # 'name' is name_by_user equivalent in entity_registry/update
                    }
                    if new_area_id:
                        payload["area_id"] = new_area_id
                        
                    await ws.send(json.dumps(payload))
                    res = await ws.recv()
                    # print(f"  Updated Entity: '{e_old_name}' -> '{e_new_name}'")
                    updated_entities += 1
                    await asyncio.sleep(async_sleep_time)
                    
        print(f"\nUpdate Complete! Modified {updated_devices} devices and {updated_entities} entities.")

if __name__ == "__main__":
    asyncio.run(execute_rename())
