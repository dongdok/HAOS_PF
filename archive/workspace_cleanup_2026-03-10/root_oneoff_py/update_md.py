import re

with open('/Users/dy/.gemini/antigravity/brain/68ed4521-aa3f-4b07-afe6-c1a04a9c3acc/localtuya_configuration_data.md', 'r') as f:
    orig = f.read()

# Replace missing IPs with '보완 필요' or keep them N/A and mention in report
# 안방 전기매트 플러그: 38:a5:c9:aa:7d:b3
# 옷방 온습도센서: b8:06:0d:d1:b0:24
# 현관 도어 센서: f8:17:2d:75:50:90

# Fix the duplicate device item ('거실 라인 조명')
o_row = "| **거실 라인 조명** | 커튼불(조명) | `ebc941b918f2c7f446wr3i` | `[5tC~6YSNrkbmP\\|B` | `c4:82:e1:a8:1f:6d` | `192.168.10.128` | 3.3 | **Func**: switch_1, countdown_1, relay_status, overcharge_switch, child_lock, cycle_time, random_time, switch_inching <br> **Stat**: switch_1, countdown_1, add_ele, cur_current, cur_power, cur_voltage, voltage_coe, electric_coe, power_coe, electricity_coe, fault, relay_status, overcharge_switch, child_lock, cycle_time, random_time, switch_inching |"

n_row = "| **거실 라인 조명** [PRIMARY] | 커튼불(조명) | `ebee27682f30d815eawhqi` | `<QXZ0DOl/gJ>;lUz` | `38:a5:c9:82:db:3e` | `*N/A*` | 3.3 | **Func**: switch_led, work_mode, colour_data, countdown, music_data <br> **Stat**: switch_led, work_mode, colour_data, countdown |"
orig = orig.replace(o_row, n_row)

plug_row = "| **거실 라인 조명 플러그** | 커튼불(플러그)"
plug_row_new = "| **거실 라인 조명 플러그** [DUP-CHECK] | 커튼불(플러그)"
orig = orig.replace(plug_row, plug_row_new)

report = """

## Collection Gap Closure Report

### 1) Host N/A 3건 보완 결과 (실패/사용자 직접 확인 필요)
- **안방 전기매트 플러그** (MAC: `38:A5:C9:AA:7D:B3`)
- **옷방 온습도센서** (MAC: `B8:06:0D:D1:B0:24`)
- **현관 도어 센서** (MAC: `F8:17:2D:75:50:90`)
- **미해결 사유**: 브라우저 자동화 도구(Subagent)의 일일 API Quota 한도(429 Error) 초과로 인하여, 현재 제가 직접 수동으로 ER605(192.168.10.1)의 Web UI로 접속해 DHCP 테이블을 긁어오는 작업이 기술적으로 차단되었습니다.
- **다음 액션 (물리 조치)**: 번거로우시겠지만, 공유기 관리자 페이지 `Network > LAN > DHCP Client List`에 접속하셔서 위 3개 MAC 주소 체인을 직접 검색해 보셔야 합니다. 배터리를 사용하는 도어 센서와 온습도 센서, 그리고 현재 꺼져있는 플러그라면 한 번 깨우거나 트리거를 준 뒤 1~2분 후 새로고침해야 DHCP 리스트에 노출됩니다. IP가 확인되면 저에게 알려주시면 되며, 그 전까지는 이 항목들에 대한 LocalTuya 등록을 보류하시면 됩니다.

### 2) 중복 Device ID 판정 결과 (거실 라인 조명)
- **발생 원인**: Tuya 클라우드 상에 "커튼불" 키워드를 가진 기기가 ID가 다른 2건(`ebc9..., ebee...`)이나 존재하는데, 초기 스크립트 작성 시 "커튼불(플러그)"와 "커튼불(조명)"을 매칭하려다 둘 다 이름이 일부 매칭되는 첫 번째 검색 결과인 `ebc941b918f2c7f446wr3i`로 덮어씌워져 버린 단순 코드 오류입니다.
- **해결 완료**: 사용자님께서 지적해주신 실제 조명 본체 ID(`ebee27682f30d815eawhqi`, MAC `38...`)를 기반으로 Tuya Cloud에서 API를 재호출하여, Local Key `<QXZ0DOl/gJ>;lUz` 및 LED 특화 기능/상태 코드(`switch_led`, `colour_data` 등)를 다시 완벽히 수집해 표를 덮어씌워 고쳤습니다. 표 구분을 돕기 위해 조명 본체는 `[PRIMARY]`, 플러그는 `[DUP-CHECK]` 태그를 붙여 두었습니다. (수집 성공 확인 완료, 임의 삭제 없이 오류 정정으로 완료)

### 3) 코드 누락/불일치 재검증 (현관 도어 센서)
- **재검증 결과**: 현관 도어 센서(`eba8acd736673b1176ajmg`)의 `Functions` 란이 비어있는 것이 문제가 아닌지 API를 직접 찔러 다시 검증한 결과, 도어 센서 같은 모니터링 전용 기기는 원래 제어 명령(Instruction Set)을 받지 않으므로 `functions` 배열 자체가 `[]` 빈 값으로 응답하는 것이 **정상 규격이 맞습니다**. 상태 코드인 `doorcontact_state, battery_percentage, temper_alarm`은 이상 없이 수집되었습니다.

> **⚠️ 작업 상태 확인 요약**: 현재까지 **오직** 텍스트 수집 보완과 교정, 문서화 작업만 진행하였으며, Home Assistant 내 UI 상의 `LocalTuya Add Entry` 등의 등록 관련 설정 수정은 절대 발생하지 않았음을 명확히 안내해 드립니다.
"""

final = orig + report

with open('/Users/dy/.gemini/antigravity/brain/68ed4521-aa3f-4b07-afe6-c1a04a9c3acc/localtuya_configuration_data.md', 'w') as f:
    f.write(final)

with open('/Users/dy/Desktop/HAOS_Control/localtuya_configuration_data.md', 'w') as f:
    f.write(final)

print("Update complete")
