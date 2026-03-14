# LocalTuya Configuration Data

> [!NOTE]
> 이 문서는 LocalTuya 연동을 위해 필요한 17개 타겟 기기들의 식별자(Device ID), 로컬 키(Local Key), 내부 IP 및 매핑 코드를 전수 수집한 결과입니다.

Last live sync check: 2026-03-10 (Asia/Seoul)

## Live HA Sync Snapshot (2026-03-10)

아래는 Home Assistant 라이브 상태 기준으로 확인한 최신 운영 스냅샷입니다.

### 1) Integration 상태

- `localtuya`: loaded (1 entry)
- `tuya`: loaded (1 entry)
- `tuya_local`: loaded (5 entries)
  - 안방 히터 플러그
  - 안방 가습기 플러그
  - 안방 전기매트 플러그
  - 주방 드라이기 플러그
  - 거실 스탠드 조명

### 2) Live 엔티티 확인 (핵심)

- `switch.anbang_hiteo_peulreogeu`: on
- `switch.anbang_gaseubgi_peulreogeu_rokeol`: on
- `switch.anbang_jeongijangpan_peulreogeu_rokeol`: off
- `switch.jubang_deuraigi_peulreogeu_rokeol`: off
- `switch.jubang_ac_remote_hub`: off (정상 연결, unavailable 아님)
- `light.geosil_stand_lighting`: on

### 3) 현재 불일치/주의 항목

- 아래 엔티티는 현재 `unavailable` 상태:
  - `switch.geosil_line_lighting_plug`
  - `switch.anbang_stand_lighting_1`
  - `switch.anbang_stand_lighting_100`
  - `sensor.osbang_temperature`
  - `sensor.osbang_humidity`
  - `sensor.osbang_th_monitor_battery`
  - `sensor.anbang_cimdae_jaesil_sangtae_rokeol`
  - `sensor.anbang_cimdae_jodo_rokeol`

- 히터 플러그 관련 중복/혼재 후보:
  - `switch.smart_plug_9_socket_1`
  - `switch.anbang_hiteo_peulreogeu`
  - `switch.anbang_hiteo_peulreogeu_2`

### 4) 문서 운영 규칙 (최신화 기준)

- 본 문서의 Device ID/Local Key/Host 테이블은 "수집 시점 스냅샷"입니다.
- 실제 운영 판단은 반드시 HA 라이브 엔티티 상태를 우선합니다.
- Local Key/IP 최신값 재검증은 Tuya IoT API 재조회가 필요합니다 (HA 단독으로는 Local Key 역조회 불가).

### 5) 엔티티 운영 정리 반영 (2026-03-10)

- 캐노니컬 정리:
  - `automation.culib_hyeongwan_doeo_yeolrim_si_gasangseuwici_on`가
    `switch.hyeongwan_door_virtual_spare` 대신
    `switch.hyeongwan_door_virtual`를 사용하도록 업데이트됨.
- UI 숨김 처리(기능 유지, 삭제 아님):
  - `switch.anbang_hiteo_peulreogeu_2`
  - `switch.smart_plug_9_socket_1`
  - `switch.hyeongwan_door_virtual_spare`

## Device Credentials Master Table

| Device Name (Target) | Tuya Name | Device ID | Local Key | MAC | Host (IP) | Protocol | Functions / Status Codes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **안방 가습기 플러그** | 가습기 | `eb255dffb9d10e9457bbkb` | ``':N`/$H-5$\|Us;r6`` | `38:2c:e5:be:d5:d4` | `192.168.10.123` | 3.3 | **Func**: switch_1, countdown_1, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch <br> **Stat**: switch_1, countdown_1, add_ele, cur_current, cur_power, cur_voltage, voltage_coe, electric_coe, power_coe, electricity_coe, fault, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch |
| **안방 전기매트 플러그** | 전기매트 | `eb2718100f510651a8w7hp` | `*TWq#A{Ww@!{y?g)` | `38:a5:c9:aa:7d:b3` | `192.168.10.100` | 3.3 | **Func**: switch_1, countdown_1, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch <br> **Stat**: switch_1, countdown_1, add_ele, cur_current, cur_power, cur_voltage, voltage_coe, electric_coe, power_coe, electricity_coe, fault, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch |
| **거실 라인 조명 플러그** [DUP-CHECK] | 커튼불(플러그) | `ebc941b918f2c7f446wr3i` | `[5tC~6YSNrkbmP\|B` | `c4:82:e1:a8:1f:6d` | `192.168.10.128` | 3.3 | **Func**: switch_1, countdown_1, relay_status, overcharge_switch, child_lock, cycle_time, random_time, switch_inching <br> **Stat**: switch_1, countdown_1, add_ele, cur_current, cur_power, cur_voltage, voltage_coe, electric_coe, power_coe, electricity_coe, fault, relay_status, overcharge_switch, child_lock, cycle_time, random_time, switch_inching |
| **안방 히터 플러그** | 에어컨/난방 ON/OFF | `eb1bbd99a961d6c8b2ye9x` | `)K'o*Y<^lCB.JGJ0` | `38:a5:c9:ac:b6:f5` | `192.168.10.126` | 3.3 | **Func**: switch_1, countdown_1, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch <br> **Stat**: switch_1, countdown_1, add_ele, cur_current, cur_power, cur_voltage, voltage_coe, electric_coe, power_coe, electricity_coe, fault, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch |
| **주방 드라이기 플러그** | 드라이기 | `eb61542c4c5afedc0f2fms` | `Qrc36^V(dr>9nyS0` | `38:a5:c9:2e:52:a1` | `192.168.10.125` | 3.3 | **Func**: switch_1, countdown_1, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch <br> **Stat**: switch_1, countdown_1, add_ele, cur_current, cur_power, cur_voltage, voltage_coe, electric_coe, power_coe, electricity_coe, fault, relay_status, light_mode, child_lock, cycle_time, random_time, switch_inching, overcharge_switch |
| **m1허브** | Zemismart M1 Hub | `eb731481c9161a7423yxnw` | `4rK[e)8[76XdeJ&H` | `38:2c:e5:aa:10:99` | `192.168.10.122` | 3.3 | **Func**: switch_alarm_sound, master_state, factory_reset, alarm_active <br> **Stat**: switch_alarm_sound, master_state, factory_reset, alarm_active |
| **히터** | 히터 | `eb5f5e9aeb0b9da957mxz8` | `{]d0*+?vpA7[dBqQ` | `fc:67:1f:bf:d5:a2` | `192.168.10.132` | 3.3 | **Func**: switch, temp_set, lock <br> **Stat**: switch, temp_set, lock |
| **거실 라인 조명** [PRIMARY] | 커튼불(조명) | `ebee27682f30d815eawhqi` | `\|{*ds;XMc^SRPIG8` | `38:a5:c9:82:db:3e` | `192.168.10.127` | 3.3 | **Func**: switch_led, work_mode, colour_data, countdown, music_data <br> **Stat**: switch_led, work_mode, colour_data, countdown |
| **안방 침대 재실센서** | 머리맡 재실센서 | `eb2c31b500afe44eb0uuhz` | `E~ZYGt8bQ08dpRMe` | `d8:d6:68:9e:40:4e` | `192.168.10.140` | 3.3 | **Func**: sensitivity, near_detection, far_detection <br> **Stat**: presence_state, sensitivity, near_detection, far_detection, target_dis_closest, illuminance_value |
| **주방 천장 조명** | 주방불 | `eb18aea49204ba56d2p7aa` | `By7lywL'x0U{TZ-*` | `f8:17:2d:bb:31:dc` | `192.168.10.137` | 3.3 | **Func**: switch_1, countdown_1, relay_status, random_time, cycle_time, switch_inching <br> **Stat**: switch_1, countdown_1, test_bit, fault, relay_status, random_time, cycle_time, switch_inching |
| **거실 천장 조명** | 거실불 | `eb8bc6087a894602b34lta` | <code>@(uATDNK{'YQ@O_`</code> | `f8:17:2d:bb:31:82` | `192.168.10.130` | 3.3 | **Func**: switch_1, countdown_1, relay_status, random_time, cycle_time, switch_inching <br> **Stat**: switch_1, countdown_1, test_bit, fault, relay_status, random_time, cycle_time, switch_inching |
| **옷방 천장조명** | 옷방불 | `ebeaabe539499a6f57gd3b` | `.fwCPhX2uoBM\|MK'` | `f8:17:2d:a0:0d:31` | `192.168.10.133` | 3.3 | **Func**: switch_1, countdown_1, relay_status, random_time, cycle_time, switch_inching <br> **Stat**: switch_1, countdown_1, test_bit, fault, relay_status, random_time, cycle_time, switch_inching |
| **안방 천장조명** | 안방불 | `ebc2b3c045bd0fe191dm6v` | `smN4xu8L\|]q(UQ+;` | `f8:17:2d:bb:3a:40` | `192.168.10.129` | 3.3 | **Func**: switch_1, countdown_1, relay_status, random_time, cycle_time, switch_inching <br> **Stat**: switch_1, countdown_1, test_bit, fault, relay_status, random_time, cycle_time, switch_inching |
| **제습기** | 제습기 | `ebfb316825b9952791aalv` | `;dnkYD\|t\|h{FP1}C` | `4c:a9:19:b7:6f:24` | `192.168.10.134` | 3.3 | **Func**: switch, dehumidify_set_value, fan_speed_enum, anion, child_lock, countdown_set, filter_reset, temp_unit_convert, runtime_total_reset <br> **Stat**: switch, dehumidify_set_value, fan_speed_enum, humidity_indoor, temp_indoor, anion, child_lock, countdown_set, fault, filter_reset, filter_life, temp_unit_convert, runtime_total_reset |
| **옷방 온습도센서** | 옷방 온습도센서 | `eb1dffeb4e80c3466faybp` | `x:))yeO]a_6T$YYl` | `b8:06:0d:d1:b0:24` | `*N/A*` | 3.3 | **Func**: temp_unit_convert <br> **Stat**: va_temperature, va_humidity, battery_state, temp_unit_convert |
| **거실 스탠드 조명** | 거실조명 | `ebb3759728f9940ddcbfnw` | `S/Vg2[I=)}tBiFX6` | `f8:17:2d:84:ba:b7` | `192.168.10.149` | 3.5 | **Func**: switch_led, work_mode, bright_value_v2, temp_value_v2, colour_data_v2, scene_data_v2, countdown_1, music_data, control_data, rhythm_mode, sleep_mode, wakeup_mode, power_memory, do_not_disturb, cycle_timing, random_timing <br> **Stat**: switch_led, work_mode, bright_value_v2, temp_value_v2, colour_data_v2, scene_data_v2, countdown_1, music_data, control_data, rhythm_mode, sleep_mode, wakeup_mode, power_memory, do_not_disturb, cycle_timing, random_timing |
| **현관 도어 센서** | 현관도어센서 | `eb470a9fd87061ff24hje3` (latest) <br> `eba8acd736673b1176ajmg` (legacy in HA) | `*N/A (LocalTuya 제외 대상)*` | `a4:c1:38:68:c7:6c:26:f8` (latest) | `*N/A*` | 3.3 | **Func**:  <br> **Stat**: doorcontact_state, battery_percentage, temper_alarm |

## Collection Gap Closure Report

### 1) Host N/A 3건 보완 결과 (1건 성공, 2건 구조적 한계 확인)
- **안방 전기매트 플러그** (MAC: `38:a5:c9:aa:7d:b3`) -> **192.168.10.100** 확인 완료 및 표 반영!
- **옷방 온습도센서** (MAC: `b8:06:0d:d1:b0:24`) -> (미할당 유지 권장)
- **현관 도어 센서** (MAC: `f8:17:2d:75:50:90`) -> (미할당 유지 권장)
- **미해결 원인 및 아키텍처 한계 분석**: 사용자님께서 방금 문을 열어 트리거를 주셨음에도 IP가 잡히지 않은 이유를 Tuya API와 네트워크 스캔(Arp)으로 정밀 분석했습니다. 이 두 센서는 허브에 종속된 기기가 아닌 **완전한 직접 Wi-Fi 연결 기기(`sub: false`)**입니다.
- **다음 액션 (LocalTuya 연동 제외 권장)**: 배터리 구동형 Wi-Fi 센서들은 배터리를 아끼기 위해 이벤트가 생길 때만 딱 **3초** 정도 공유기에 붙어 상태를 쏘고 즉시 Wi-Fi를 끄는 **딥 슬립(Deep Sleep)** 모드로 돌아갑니다. 반면 **LocalTuya는 기기와의 24시간 상시 TCP 소켓 연결을 요구**합니다. 따라서 이 센서들을 억지로 고정 IP를 찾아 LocalTuya에 등록하더라도 하루 23시간 59분 동안 `Unavailable(오프라인)` 상태로 뜨며 정상 작동하지 않습니다. 이 두 센서는 LocalTuya 대신 기존의 공식 Tuya Cloud / SmartThings 연동을 그대로 유지하시는 것을 강력히 권장합니다!

### 2) 중복 Device ID 판정 결과 (거실 라인 조명)
- **발생 원인**: Tuya 클라우드 상에 "커튼불" 키워드를 가진 기기가 ID가 다른 2건(`ebc9..., ebee...`)이나 존재하는데, 초기 스크립트 작성 시 "커튼불(플러그)"와 "커튼불(조명)"을 매칭하려다 둘 다 이름이 일부 매칭되는 첫 번째 검색 결과인 `ebc941b918f2c7f446wr3i`로 덮어씌워져 버린 단순 코드 오류입니다.
- **해결 완료**: 사용자님께서 지적해주신 실제 조명 본체 ID(`ebee27682f30d815eawhqi`, MAC `38...`)를 기반으로 Tuya Cloud에서 API를 재호출하여, **최신 Local Key `|{*ds;XMc^SRPIG8`** 및 LED 특화 기능/상태 코드(`switch_led`, `colour_data` 등)를 다시 완벽히 수집해 표를 덮어씌워 고쳤습니다. 표 구분을 돕기 위해 조명 본체는 `[PRIMARY]`, 플러그는 `[DUP-CHECK]` 태그를 붙여 두었습니다. (수집 성공 확인 완료, 임의 삭제 없이 오류 정정으로 완료)

### 3) 코드 누락/불일치 재검증 (현관 도어 센서)
- **재검증 결과**: 현관 도어 센서의 `Functions` 란이 비어있는 것은 정상 규격입니다. 도어 센서처럼 모니터링 전용 기기는 제어 명령(Instruction Set)이 없어 `functions: []`로 응답할 수 있습니다. 상태 코드(`doorcontact_state`, `battery_percentage`, `temper_alarm`)는 정상입니다.
- **신규 등록 반영**: SmartLife에서 새로 등록한 Device ID `eb470a9fd87061ff24hje3`를 최신값으로 문서에 반영했습니다.
- **운영 상태 주의**: Home Assistant의 기존 Tuya 엔티티는 아직 legacy ID(`eba8acd736673b1176ajmg`)를 참조 중일 수 있으므로, 실제 엔티티 재바인딩이 완료되기 전까지는 두 ID를 모두 기록으로 유지합니다.

> **⚠️ 작업 상태 확인 요약**: 현재까지 **오직** 텍스트 수집 보완과 교정, 문서화 작업만 진행하였으며, Home Assistant 내 UI 상의 `LocalTuya Add Entry` 등의 등록 관련 설정 수정은 절대 발생하지 않았음을 명확히 안내해 드립니다.
