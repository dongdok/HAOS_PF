import os
import sys
import json

# Setup Tuya Credentials
CLIENT_ID = "x3d8ckadqnjqry4hg8g5"
SECRET = "302fd10c29764c2db63b3fe4ae28b9c9"
DEVICE_ID = "eb731481c9161a7423yxnw" # M1 Hub as anchor

# MAC to IP mapping from ER605
mac_to_ip = {
    "28:4e:e9:5b:aa:9e": "192.168.10.101",
    "00:15:5d:2d:cf:00": "192.168.10.104", # HA
    "38:2c:e5:aa:10:99": "192.168.10.122",
    "38:2c:e5:be:d5:d4": "192.168.10.123",
    "c8:c9:a3:3e:b9:8f": "192.168.10.124",
    "38:a5:c9:2e:52:a1": "192.168.10.125",
    "38:a5:c9:ac:b6:f5": "192.168.10.126",
    "38:a5:c9:82:db:3e": "192.168.10.127",
    "c4:82:e1:a8:1f:6d": "192.168.10.128",
    "f8:17:2d:bb:3a:40": "192.168.10.129",
    "f8:17:2d:bb:31:82": "192.168.10.130",
    "f8:17:2d:84:ba:b7": "192.168.10.149",
    "fc:67:1f:bf:d5:a2": "192.168.10.132",
    "f8:17:2d:a0:0d:31": "192.168.10.133",
    "4c:a9:19:b7:6f:24": "192.168.10.134",
    "f8:17:2d:bb:31:dc": "192.168.10.137",
    "d8:d6:68:9e:40:4e": "192.168.10.140",
    # Alternative formats without colons for matching
    "284EE95BAA9E": "192.168.10.101",
    "382CE5AA1099": "192.168.10.122",
    "382CE5BED5D4": "192.168.10.123",
    "C8C9A33EB98F": "192.168.10.124",
    "38A5C92E52A1": "192.168.10.125",
    "38A5C9ACB6F5": "192.168.10.126",
    "38A5C982DB3E": "192.168.10.127",
    "C482E1A81F6D": "192.168.10.128",
    "F8172DBB3A40": "192.168.10.129",
    "F8172DBB3182": "192.168.10.130",
    "F8172D84BAB7": "192.168.10.149",
    "FC671FBFD5A2": "192.168.10.132",
    "F8172DA00D31": "192.168.10.133",
    "4CA919B76F24": "192.168.10.134",
    "F8172DBB31DC": "192.168.10.137",
    "D8D6689E404E": "192.168.10.140",
}

target_device_mapping = {
    "안방 가습기 플러그": "가습기",
    "안방 전기매트 플러그": "전기매트",
    "거실 라인 조명 플러그": "커튼불(플러그)",
    "안방 히터 플러그": "에어컨/난방 ON/OFF",
    "주방 드라이기 플러그": "드라이기",
    "m1허브": "Zemismart M1 Hub",
    "히터": "히터",
    "거실 라인 조명": "커튼불(조명)",
    "안방 침대 재실센서": "머리맡 재실센서",
    "주방 천장 조명": "주방불",
    "거실 천장 조명": "거실불",
    "옷방 천장조명": "옷방불",
    "안방 천장조명": "안방불",
    "제습기": "제습기",
    "옷방 온습도센서": "옷방 온습도센서",
    "거실 스탠드 조명": "거실조명",
    "현관 도어 센서": "현관도어센서"
}

try:
    import tinytuya
except ImportError:
    print("tinytuya not installed", file=sys.stderr)
    sys.exit(1)

def format_mac(mac_str):
    if not mac_str: return mac_str
    m = mac_str.replace(":", "").upper()
    return m

def main():
    print("Connecting to Tuya Cloud...")
    c = tinytuya.Cloud(
        apiRegion="us", 
        apiKey=CLIENT_ID, 
        apiSecret=SECRET, 
        apiDeviceID=DEVICE_ID 
    )

    devices = c.getdevices()
    if not devices:
        print("Failed to get devices")
        return

    result_table = []
    
    # Pre-process Tuya list
    tuya_dict = {}
    for d in devices:
        name = d.get('name', '')
        tuya_dict[name] = d

    # For each target
    for user_name, tuya_name in target_device_mapping.items():
        matched_device = tuya_dict.get(tuya_name)
        
        if not matched_device:
            # Maybe it matches partially?
            for tn, td in tuya_dict.items():
                if tuya_name in tn or tn in tuya_name:
                    matched_device = td
                    break
                    
        if matched_device:
            dev_id = matched_device.get('id', '')
            
            dev_details = c.cloudrequest(f"/v1.0/devices/{dev_id}")
            if dev_details and 'result' in dev_details:
                local_key = dev_details['result'].get('local_key', '')
                mac = dev_details['result'].get('mac', matched_device.get('mac', ''))
                ip = dev_details['result'].get('ip', matched_device.get('ip', ''))
            else:
                local_key = matched_device.get('local_key', '')
                mac = matched_device.get('mac', '')
                ip = matched_device.get('ip', '')
            
            # Find in ER605 mapped table
            fmac = format_mac(mac)
            host = mac_to_ip.get(fmac, "")
            # fallback: maybe IP is local?
            if not host and ip and ip.startswith("192.168.10."):
                host = ip
            
            # Additional Cloud Queries for functions/status
            # Try to get instruction set
            functions_codes = ""
            status_codes = ""
            
            # We can use tinytuya to get status
            # Actually, standard tinytuya doesn't fetch instruction set by default via cloud, 
            # but we can get it from the Cloud request directly if we use c.cloudrequest
            
            req_url = f"/v1.0/devices/{dev_id}/specifications"
            specs = c.cloudrequest(req_url)
            
            if specs and 'result' in specs and specs['result']:
                funcs = specs['result'].get('functions', [])
                stats = specs['result'].get('status', [])
                if funcs:
                    functions_codes = ", ".join([f['code'] for f in funcs])
                if stats:
                    status_codes = ", ".join([s['code'] for s in stats])
                    
            if not functions_codes and not status_codes:
                # Some devices might not have spec, use category
                functions_codes = matched_device.get('category', 'unknown')
                status_codes = matched_device.get('category', 'unknown')
                
            result_table.append({
                "device_name": user_name,
                "tuya_name": tuya_name,
                "device_id": dev_id,
                "local_key": local_key,
                "mac": mac,
                "host": host,
                "protocol": "3.3",
                "functions_codes": functions_codes,
                "status_codes": status_codes
            })
        else:
            result_table.append({
                "device_name": user_name,
                "tuya_name": tuya_name,
                "device_id": "NOT FOUND",
                "local_key": "",
                "mac": "",
                "host": "",
                "protocol": "",
                "functions_codes": "",
                "status_codes": ""
            })

    output_file = "/Users/dy/Desktop/HAOS_Control/tuya_data_extracted.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_table, f, indent=2, ensure_ascii=False)
        
    print(f"Extraction complete. Data saved to {output_file}")

if __name__ == "__main__":
    main()
