import re

with open('/Users/dy/.gemini/antigravity/brain/68ed4521-aa3f-4b07-afe6-c1a04a9c3acc/localtuya_configuration_data.md', 'r') as f:
    orig = f.read()

# 안방 전기매트 플러그: 38:A5:C9:AA:7D:B3 -> 192.168.10.100
# 옷방 온습도센서: B8:06:0D:D1:B0:24 -> Not found in screenshot
# 현관 도어 센서: F8:17:2D:75:50:90 -> Not found in screenshot

mat_row_old = "| **안방 전기매트 플러그** | 전기매트 | `eb2718100f510651a8w7hp` | `*TWq#A{Ww@!{y?g)` | `38:a5:c9:aa:7d:b3` | `*N/A*` | 3.3"
mat_row_new = "| **안방 전기매트 플러그** | 전기매트 | `eb2718100f510651a8w7hp` | `*TWq#A{Ww@!{y?g)` | `38:a5:c9:aa:7d:b3` | `192.168.10.100` | 3.3"
orig = orig.replace(mat_row_old, mat_row_new)

# Update report section
report_old = """### 1) Host N/A 3건 보완 결과 (실패/사용자 직접 확인 필요)
- **안방 전기매트 플러그** (MAC: `38:A5:C9:AA:7D:B3`)
- **옷방 온습도센서** (MAC: `B8:06:0D:D1:B0:24`)
- **현관 도어 센서** (MAC: `F8:17:2D:75:50:90`)
- **미해결 사유**: 브라우저 자동화 도구(Subagent)의 일일 API Quota 한도(429 Error) 초과로 인하여, 현재 제가 직접 수동으로 ER605(192.168.10.1)의 Web UI로 접속해 DHCP 테이블을 긁어오는 작업이 기술적으로 차단되었습니다.
- **다음 액션 (물리 조치)**: 번거로우시겠지만, 공유기 관리자 페이지 `Network > LAN > DHCP Client List`에 접속하셔서 위 3개 MAC 주소 체인을 직접 검색해 보셔야 합니다. 배터리를 사용하는 도어 센서와 온습도 센서, 그리고 현재 꺼져있는 플러그라면 한 번 깨우거나 트리거를 준 뒤 1~2분 후 새로고침해야 DHCP 리스트에 노출됩니다. IP가 확인되면 저에게 알려주시면 되며, 그 전까지는 이 항목들에 대한 LocalTuya 등록을 보류하시면 됩니다."""

report_new = """### 1) Host N/A 3건 보완 결과 (1건 성공, 2건 미해결)
- **안방 전기매트 플러그** (MAC: `38:A5:C9:AA:7D:B3`) -> **192.168.10.100** 확인 완료 및 표 반영!
- **옷방 온습도센서** (MAC: `B8:06:0D:D1:B0:24`) -> (미확인)
- **현관 도어 센서** (MAC: `F8:17:2D:75:50:90`) -> (미확인)
- **미해결 사유**: 전기매트 플러그는 제공해주신 스크린샷 2번 라인(192.168.10.100)에서 발견되었으나, 나머지 2개 기기는 스크린샷 22개 목록 내에 존재하지 않습니다.
- **다음 액션 (사용자 물리 조치)**: 도어 센서와 온습도 센서는 배터리 기반이라 통신할 때만 IP를 가져가거나 허브(m1허브)에 종속된 형태의 센서일 확률이 높습니다. 센서 옆 버튼을 누르거나 문을 여닫아 강제로 네트워크를 깨운 뒤 공유기 리스트 새로고침이 필요합니다."""

orig = orig.replace(report_old, report_new)

with open('/Users/dy/.gemini/antigravity/brain/68ed4521-aa3f-4b07-afe6-c1a04a9c3acc/localtuya_configuration_data.md', 'w') as f:
    f.write(orig)

with open('/Users/dy/Desktop/HAOS_Control/localtuya_configuration_data.md', 'w') as f:
    f.write(orig)

print("Update complete")
