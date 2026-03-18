# Raw HAOS_Control System Inventory (Objective Data Only)

> 데이터 기준일: 2026-03-18  
> 본 문서에는 시스템의 모든 엔티티, 자동화, 스크립트, 그리고 프로토콜 레벨의 구성 정보가 있는 그대로 기술되어 있습니다.

---

## 1. Full Entity & State List (핵심 요약)

| Entity ID | State | Friendly Name | Model/Manufacturer |
| :--- | :--- | :--- | :--- |
| `automation.jomyeong_osbang_jadong_jeomdeung_sodeung_jaesil_yeondong_2` | on | [조명] 옷방 자동 점등/소등 (재실 연동) | - |
| `automation.cwicim_anbang_cimdae_jaesil_gamji_si_jaljunbimodeu_silhaeng` | on | [취침] 안방 침대 재실 감지 시 잘준비모드 실행 | - |
| `script.too_bright` | off | Too bright | - |
| `sensor.anbang_presence_distance` | 2.7m | anbang_presence Distance | mmWave |
| `sensor.anbang_presence_illuminance` | 54lx | anbang_presence Illuminance | mmWave |
| `sensor.cong_jeonryeog_eneoji_habgye` | 4.006kWh | 총 전력 에너지 합계 | - |
| `climate.anbang_heater` | off | 안방 히터 로컬 | Tuya |
| `humidifier.osbang_jeseubgi_rokeol_naebuseubdo` | off | 옷방 제습기(로컬) | Tuya |
| `cover.anbang_curtain` | closed | 안방 커튼 | Tuya |
| `media_player.geosil_tv_smartthings` | on | 거실 TV | Samsung TV |
| `light.geosil_stand_lighting` | on | 거실 스탠드 조명 | Zigbee |
| `switch.anbang_gaseubgi_peulreogeu_rokeol` | on | 안방 가습기 플러그 | LocalTuya |
| `switch.anbang_hiteo_peulreogeu` | on | 안방 히터 플러그 | LocalTuya |
| `switch.jubang_deuraigi_peulreogeu_rokeol` | off | 주방 드라이기 플러그 | LocalTuya |
| `binary_sensor.anbang_presence` | on | 안방 재실 감지 (메인) | mmWave |
| `binary_sensor.hyeongwan_door` | off | 현관 도어 센서 | Zigbee |

*(전체 279개 엔티티 리스트는 `ha_states.json` 원본 데이터에 기반함)*

---

## 2. Automations Inventory (34 items)

- `automation.gongjo_anbang_gaseubgi_jadong_on_seubdo_45_miman` (공조 가습기 제어)
- `automation.jomyeong_seutaendeu_saegondo_jugi_bojeong_kyeojim_yuji` (색온도 보정)
- `automation.jomyeong_anbang_yija_cagseog_si_anbangbul_on_weonjindong_keoteundadhim` (착석 점등)
- `automation.oecul_oecul_silhaeng_gasangseuwici2` (외출 실행)
- `automation.boggu_zigbee2mqtt_beuriji_opeurain_jadong_jaesijag` (MQTT 복구)
- *(기타 29개 자동화 포함)*

---

## 3. Scripts Inventory (87 items)

- `script.s001_goodmorning` (굿모닝 루틴)
- `script.jal_junbihaejwo` (잘 준비 스크립트)
- `script.nap_mode` (낮잠 모드)
- `script.cmd_media_player_geosil_tv_off` (TV 제어 표준 명령)
- `script.reco_feedback_intended_geosil_line_light` (추천 피드백)
- *(기타 82개 스크립트 포함)*

---

## 4. UI Structure (Lovelace Views)

- **View: 홈킷 뷰(Sections)** (`path: homekit-sections`)
  - Sections: 집(Home), 거실, 주방, 화장실, 옷방, 안방
  - 주요 카드: `weather-forecast`, `tile` (features: trend-graph, cover-open-close, humidifier-toggle)
- **View: Home** (`path: default_view`)
  - 구조: Vertical Stack 기반 룸별 Grid 카드 배치
  - 주요 카드: `thermostat`, `media-control`, `markdown` (Room titles)

---

## 5. Network & Infrastructure (Raw Config)

- **Main Host**: `ha.story-nase.ts.net:8123` (Tailscale VPN mesh)
- **Integrations Configured**:
  - `localtuya`: 17 devices (Protocol 3.3/3.5)
  - `tuya_local`: 5 devices (Heater, Humidifier, Blanket, Dryer, Living room light)
  - `zigbee2mqtt`: Bridge monitoring auto-restart
  - `smartthings`: TV & Vacuum integration
  - `hacs`: Repository based extensions
- **Device IDs & Keys**: `localtuya_configuration_data.md` 내 17개 기기의 ID/Local Key/IP/MAC 전수 관리 중.

---

## 6. Safety & Security Measures

- **Child Lock**: 가동 기기(가습기, 매트, 히터, 드라이기) 전수 적용.
- **Overcharge Cutoff**: 전력 측정형 플러그 9개 이상에 적용.
- **Tamper Alert**: 현관 도어 센서 변조 감지(`binary_sensor.hyeongwan_door_tamper`).
- **Low Battery Alert**: 모든 Zigbee 센서에 대한 전압 및 배터리 로우 상태 감시.

---

## 7. System Architecture (Abstraction Layer)

- **Command Standardization**: 직접 엔티티를 제어하지 않고 `script.cmd_*` 레이어를 통해 하드웨어 제어권을 추상화함.
- **Virtual Switches**: 5개 이상의 `input_boolean` 가상 스위치를 통해 복합 상태(외출 1/2, 굿나잇 등) 관리.
- **Feedback Loop**: 추천 엔진 제안에 대한 `input_select` 기반 사용자 피드백 수집 체계 운영.
