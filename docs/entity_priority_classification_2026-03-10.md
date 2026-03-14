# Entity Priority Classification (2026-03-10)

Last updated: 2026-03-10 (Asia/Seoul)
Policy owner: 사용자 운영 원칙

## 기준

1. 1순위(메인): `mqtt`, `localtuya`, `tuya_local`
2. 2순위(보조): `tuya`, `smartthings` (단, 1순위와 비중복일 때만 유지)
3. 2순위 중복 엔티티: 비활성화 대상

## A. 1순위 유지 엔티티군 (메인)

- MQTT 주요 예:
  - `binary_sensor.anbang_presence` (안방 메인 재실)
  - `binary_sensor.geosil_presence`
  - `binary_sensor.jubang_presence`
  - `binary_sensor.osbang_presence`
  - `binary_sensor.hwajangsil_presence`
- LocalTuya 주요 예:
  - `binary_sensor.anbang_bedside_presence` (안방 보조/시간조건 재실)
  - `sensor.anbang_cimdae_jaesil_sangtae_rokeol`
  - `sensor.anbang_cimdae_jodo_rokeol`
  - `switch.geosil_line_lighting_plug`
- Tuya Local 주요 예:
  - `switch.anbang_hiteo_peulreogeu`
  - `switch.anbang_gaseubgi_peulreogeu_rokeol`
  - `switch.anbang_jeongijangpan_peulreogeu_rokeol`
  - `switch.jubang_deuraigi_peulreogeu_rokeol`
  - `light.geosil_stand_lighting`

## B. 2순위 유지 (비중복)

### Tuya (cloud)

- `switch.hyeongwan_door_virtual`
- `switch.hyeongwan_outing_virtual_2`
- `switch.anbang_bedtime_virtual`
- `switch.anbang_goodnight_virtual`
- `switch.hyeongwan_door_virtual_spare` (현재 hidden, 7일 모니터링 대상)

### SmartThings

- `switch.outlet1_4`
- `switch.outlet51_2`
- `sensor.osbang_temperature` (클라우드 Wi-Fi, 현재 오프라인 인지)
- `sensor.osbang_humidity` (클라우드 Wi-Fi, 현재 오프라인 인지)
- `sensor.osbang_th_monitor_battery` (클라우드 Wi-Fi, 현재 오프라인 인지)

## C. 2순위 중복(비활성화 대상/완료)

아래는 1순위와 기능 중복으로 판단된 엔티티:

- `switch.smart_plug_9_socket_1` (`tuya`)  
  - 중복 기준: `switch.anbang_hiteo_peulreogeu` (`tuya_local`)와 동일 히터 플러그 경로
  - 상태: `disabled_by: user` (완료)

- `switch.anbang_hiteo_peulreogeu_2` (`smartthings`)  
  - 중복 기준: 동일 히터 플러그 대체 경로
  - 상태: `disabled_by: user` (완료)

- `switch.anbang_stand_lighting_1` (`smartthings`)  
  - 중복 기준: 안방 스탠드 조명 보조 스위치(직접 조명 제어/씬으로 대체 가능)
  - 상태: `disabled_by: user` (완료)

- `switch.anbang_stand_lighting_100` (`smartthings`)  
  - 중복 기준: 안방 스탠드 조명 보조 스위치(직접 조명 제어/씬으로 대체 가능)
  - 상태: `disabled_by: user` (완료)

## D. 오프라인 인지 항목 (유지)

- `sensor.osbang_temperature`
- `sensor.osbang_humidity`
- `sensor.osbang_th_monitor_battery`

설명:
- 사용자 운영 기준상 해당 3개는 투야 클라우드 계열 Wi-Fi 기기로 관리.
- 현재 오프라인 상태는 인지된 상태이며, 비활성화 대상이 아님.

## E. 운영 메모

- 안방 재실은 “이원화” 유지:
  - 메인: `binary_sensor.anbang_presence` (MQTT)
  - 보조(시간조건): `binary_sensor.anbang_bedside_presence` (LocalTuya)
- 위 이원화는 중복 비활성화 규칙의 예외가 아니라, 의도된 역할 분리로 간주.
