# HA 엔티티 운영 정리 (2026-03-10)

Last updated: 2026-03-10 (Asia/Seoul)
Source of truth: live Home Assistant entity/automation registry

## 1) 이번 정리에서 실제 반영한 변경

### A. 자동화 참조 정리 (캐노니컬 통일)

- 대상 자동화: `automation.culib_hyeongwan_doeo_yeolrim_si_gasangseuwici_on`
- 변경 전:
  - `switch.hyeongwan_door_virtual_spare`
- 변경 후:
  - `switch.hyeongwan_door_virtual`

의미:
- 현관 도어 연동 ON/OFF 자동화가 `current_operating_map.md` 기준 캐노니컬 엔티티를 사용하도록 통일됨.

### B. 중복/레거시 후보 1차 정리 (2026-03-10 초기)

초기 1차 정리에서 아래 3개를 `hidden_by: user` 처리했으며,
이후 사용자 확인으로 최종 상태가 조정됨:

- `switch.anbang_hiteo_peulreogeu_2` (현재: disabled + hidden)
- `switch.smart_plug_9_socket_1` (현재: active + visible)
- `switch.hyeongwan_door_virtual_spare` (현재: hidden 유지)

### C. 사용자 확인 기반 추가 정리 (2026-03-10)

- `switch.anbang_stand_lighting_1` -> `disabled_by: user`
- `switch.anbang_stand_lighting_100` -> `disabled_by: user`
- `switch.anbang_hiteo_peulreogeu_2` -> `disabled_by: user` 유지
- `switch.smart_plug_9_socket_1` -> 숨김 해제(`hidden_by` 제거), 운영 사용 엔티티로 유지
- `binary_sensor.anbang_bedside_presence`는 재활성화: MQTT 메인(`anbang_presence`)과 역할 분리해 병행 운영

## 2) 유지(운영 핵심) 대상

아래는 현재 자동화/운영 기준 핵심 엔티티(요약):

- `switch.hyeongwan_door_virtual`
- `switch.hyeongwan_outing_virtual_2`
- `switch.anbang_hiteo_peulreogeu`
- `switch.jubang_ac_remote_hub`
- `switch.jubang_line_lighting_plug`
- `light.geosil_stand_lighting`
- `light.anbang_stand_lighting`
- `cover.anbang_curtain`

## 3) 확인 필요(삭제/비활성화 보류) 항목

### A. `unavailable` 상태 엔티티 (운영대상 6개)

- `switch.geosil_line_lighting_plug`
- `sensor.osbang_temperature`
- `sensor.osbang_humidity`
- `sensor.osbang_th_monitor_battery`
- `sensor.anbang_cimdae_jaesil_sangtae_rokeol`
- `sensor.anbang_cimdae_jodo_rokeol`

참고:
- `switch.anbang_stand_lighting_1`, `switch.anbang_stand_lighting_100`는 사용자 요청으로 비활성화 완료되어 운영 `unavailable` 점검 대상에서 제외.

정책:
- `unavailable`은 통신/전원/통합 문제일 수 있으므로 바로 삭제 금지.
- 1차로 통신 상태 복구 확인 후 정리 결정.

### A-1. 원인별 점검표 (전원/통신/통합)

기준 시점: 2026-03-10 (KST), 라이브 상태 조회 기준

| Entity | Platform | 관측 근거 | 1차 분류 | 점검 포인트 | 처리 방향 |
|---|---|---|---|---|---|
| `switch.geosil_line_lighting_plug` | `localtuya` | 단일 디바이스 엔티티만 `unavailable`, 같은 공간의 `light.geosil_keoteun_rain_jomyeong_rokeol`은 `on` | 통신 | LocalTuya 대상 IP/응답, 멀티탭 전원, AP 연결 | 통신 복구 우선, 미복구 시 localtuya 재바인딩 |
| `sensor.osbang_temperature` | `smartthings` | 옷방 온습도 3종(온도/습도/배터리) 동시 `unavailable`, 사용자 확인상 투야 클라우드 Wi-Fi 계열 | 통합/통신 | 클라우드 경로 오프라인 여부, 재연결 시 상태 복귀 확인 | 사용자 인지 오프라인으로 유지(비활성화 대상 아님) |
| `sensor.osbang_humidity` | `smartthings` | 위와 동일 | 통합/통신 | 위와 동일 | 위와 동일 |
| `sensor.osbang_th_monitor_battery` | `smartthings` | 위와 동일 | 통합/통신 | 위와 동일 | 위와 동일 |
| `sensor.anbang_cimdae_jaesil_sangtae_rokeol` | `localtuya` | 같은 디바이스의 `binary_sensor/number`까지 일괄 `unavailable` | 전원/통신 | 센서 전원/와이파이 연결, LocalTuya 디바이스 응답 | 물리/통신 복구 후 재검증 |
| `sensor.anbang_cimdae_jodo_rokeol` | `localtuya` | 위와 동일 | 전원/통신 | 위와 동일 | 위와 동일 |

### B. 중복 후보 상태 (최신)

- 현재 상태:
  - `switch.hyeongwan_door_virtual_spare`: hidden
  - `switch.anbang_hiteo_peulreogeu_2`: disabled + hidden
  - `switch.smart_plug_9_socket_1`: active + visible
- 추가 비활성화 판단은 hidden 대상(`_spare`)에 한해 진행.

### B-1. 7일 모니터링 후 `disabled` 전환 기준 (확정)

모니터링 기간:
- 시작: 2026-03-10
- 종료: 2026-03-17

대상(현재 적용 기준):
- `switch.hyeongwan_door_virtual_spare` (tuya, hidden)

즉시 비활성화 완료:
- `switch.anbang_hiteo_peulreogeu_2` (smartthings)

운영 유지(모니터링 대상 제외):
- `switch.smart_plug_9_socket_1` (tuya, hidden 해제)

전환 조건 (모두 만족 시 `disabled_by: user`):

1. 자동화/스크립트 참조 0건
- 점검 대상: HA automation 32개 + script 5개
- 엔티티 ID 문자열 직접 참조가 없어야 함

2. 상태 변화 0회
- 7일 logbook/history에서 상태 전환이 없어야 함

3. 캐노니컬 대체 엔티티 정상 동작 확인
- 히터 계열: `switch.anbang_hiteo_peulreogeu` 정상 제어
- 현관 가상스위치 계열: `switch.hyeongwan_door_virtual` 정상 제어

4. 복귀 루트 확보
- 비활성화 전, 대상 entity_id와 device_id를 문서에 기록
- 문제 시 즉시 재활성화 가능한 상태 유지

비활성화 보류 조건 (하나라도 해당 시 보류):
- 7일 내 상태 변경 이력 존재
- 새 자동화에서 참조 확인
- 대응 캐노니컬 엔티티가 `unavailable` 또는 동작 불안정

## 4) 운영 원칙 (이번 정리 기준)

- 아카이브 문서가 아니라 라이브 HA 상태를 기준으로 판단.
- 자동화 참조 엔티티는 캐노니컬 ID로 단일화.
- 즉시 리스크가 있는 삭제/영구 제거는 보류하고, 숨김 -> 검증 -> 비활성화 순으로 단계적 정리.
