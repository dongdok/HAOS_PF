# HAOS_Control — 포트폴리오 세부 기술 문서

> 작성일: 2026-03-18  
> 문서 성격: 포트폴리오 / 자기소개서 원본 소스 (요약 전 상세 버전)  
> 프로젝트 경로: `/Users/dy/Desktop/HAOS_Control`

---

## 1. 프로젝트 개요

### 1-1. 프로젝트 이름 및 성격

**HAOS_Control**은 개인 주거 공간을 대상으로 한 **완전 자가 구축형 스마트홈 자동화 시스템**이다.  
Home Assistant OS(HAOS)를 중심으로, SmartThings/Tuya 같은 클라우드 의존 플랫폼에서 **로컬 우선(Local-First) 아키텍처**로 전면 이전하는 것을 핵심 목표로 한다.

단순한 기기 연결/제어에 그치지 않고, 다음 세 가지 축으로 시스템을 설계했다:

1. **인프라 축** — 디바이스 통합, 엔티티 표준화, 네트워크 설계
2. **자동화 축** — 재실 연동, 환경 제어, 취침/기상 루틴 등 26개 이상 자동화 마이그레이션
3. **데이터/추천 축** — 행동 로그 기반 추천 엔진(Recommendation Engine) 설계 및 구현

---

### 1-2. 프로젝트 배경 및 동기

기존 SmartThings + Tuya 클라우드 기반 스마트홈 환경에서 다음 문제점이 존재했다:

- **클라우드 의존성**: 서버 장애 시 모든 로컬 기기 제어 불가
- **플랫폼 파편화**: SmartThings 자동화, Tuya 앱 자동화, iOS 단축어가 각자 독립적으로 동작하여 전체 흐름 파악 불가
- **명명 혼란**: 통합별로 제각각 생성되는 엔티티 ID(transliteration 혼용, 번호 suffix 남발 등)
- **로그/데이터 부재**: 어떤 기기가 언제 무슨 이유로 켜졌는지 전혀 추적 불가

이 문제를 해결하고자, **Home Assistant OS를 중심에 두고 모든 제어를 단일 플랫폼으로 통합**하는 프로젝트를 설계·실행했다.

---

### 1-3. 프로젝트 기간 및 상태

- 시작: 2026년 초
- 현재 상태: 인프라 안정화 완료 + 추천 엔진 개발 중
- 마지막 문서 기준일: 2026-03-18

---

## 2. 기술 스택 및 도구

| 분류 | 사용 기술 |
|---|---|
| 스마트홈 플랫폼 | Home Assistant OS (HAOS) |
| 로컬 디바이스 통합 | LocalTuya integration (Tuya local protocol 3.3 / 3.4 / 3.5) |
| 클라우드 통합 | SmartThings integration, Samsung SmartTV local |
| 무선 센서 | Zigbee (ZHA), MQTT (mmWave 재실 센서) |
| 원격 접근 | Tailscale (WireGuard 기반 VPN mesh) |
| 코드 언어 | Python 3.x |
| 패키지 관리 | pyproject.toml, uv / pip |
| 지속성 저장소 | SQLite (추천 엔진 DB: `data/reco_engine.db`) |
| 설정 관리 | TOML (`config/policy.toml`, `config/entities_canonical.toml`) |
| 자동화 언어 | Home Assistant YAML automation DSL |
| 대시보드 | Lovelace JSON (`lovelace_active.json`) |
| 버전 관리 | Git |
| 모바일 제어 | iOS 단축어(Shortcuts) + HA Companion App |

---

## 3. 시스템 아키텍처

### 3-1. 전체 구조

```
[물리 디바이스 레이어]
  └── Tuya 스마트플러그 (LocalTuya, 로컬 IP/LAN)
  └── Tuya 조명 (LocalTuya)
  └── Tuya 센서 (온습도, 재실, 진동, 도어)
  └── Zigbee 센서 (ZHA: 도어, 배터리 등)
  └── mmWave 재실 센서 (MQTT over LAN)
  └── Samsung SmartTV (SmartThings integration)
  └── 옷방 제습기 (LocalTuya climate entity)
  └── 안방 히터 (LocalTuya climate entity)
  └── 안방 전동 커튼 (LocalTuya cover entity)

[통합/미들웨어 레이어]
  └── Home Assistant OS (HAOS)
      ├── LocalTuya integration (로컬 통신, 클라우드 불필요)
      ├── SmartThings integration (TV 전용)
      ├── ZHA (Zigbee Home Automation)
      ├── MQTT broker (mosquitto)
      └── Utility Meter (에너지 누적 계측)

[자동화/로직 레이어]
  └── HA YAML Automation
      ├── 재실 연동 조명
      ├── 환경 제어 (습도/온도)
      ├── 취침/기상 루틴
      ├── 외출 모드
      └── 시간 기반 스케줄

[추천 엔진 레이어 — Python]
  └── src/reco_engine/
      ├── core/     (도메인 엔티티, 규칙, KPI)
      ├── adapters/ (HA API client, SQLite)
      ├── services/ (수집, 탐지, 제안, KPI, 대시보드)
      └── interfaces/cli.py

[원격 접근 레이어]
  └── Tailscale VPN (외부 접근 시 WireGuard 터널)

[모바일 제어 레이어]
  └── iOS Shortcuts (굿모닝/굿나잇/잘준비해줘 루틴)
  └── HA Companion App
```

---

### 3-2. 네트워크 설계

- 모든 Tuya 로컬 기기는 **고정 IP (DHCP 예약)** 를 사용
- 기기 주소 대역: `192.168.10.x`
- Tailscale을 통한 외부 원격 접근 (VPN mesh, WireGuard 기반)
- HA 서버 내부 URL 및 외부 Tailscale URL 모두 환경변수(`.env`)로 관리

---

### 3-3. Local-First 마이그레이션 전략

| 단계 | 내용 |
|---|---|
| 1단계 | 기존 SmartThings/Tuya 자동화 전체 인벤토리 캡처 (`automation_external_inventory_v1.md`) |
| 2단계 | 각 자동화를 HA Canonical Entity ID로 매핑 |
| 3단계 | LocalTuya integration으로 기기 재연결 (스크립트 자동화) |
| 4단계 | HA YAML 자동화 작성 + 실환경 테스트 |
| 5단계 | 기존 외부 플랫폼 자동화 비활성화 |

---

## 4. 하드웨어 인벤토리 (방별 상세)

### 4-1. 안방 (침실)

| 디바이스 | 타입 | 엔티티 ID | 역할 |
|---|---|---|---|
| 안방 천장 조명 | Switch | `switch.anbang_ceiling_light` | 메인 조명 |
| 안방 스탠드 조명 | Light | `light.anbang_stand_lighting` | 분위기 조명 (밝기/색온도 가변) |
| 안방 커튼 | Cover | `cover.anbang_curtain` | 전동 커튼 (LocalTuya) |
| 안방 가습기 플러그 | Switch | `switch.anbang_gaseubgi_peulreogeu_rokeol` | 가습기 전원 (로컬) |
| 안방 전기장판 플러그 | Switch | `switch.anbang_jeongijangpan_peulreogeu_rokeol` | 전기장판 전원 (로컬) |
| 안방 히터 | Climate | `climate.anbang_hiteo` | 히터 온도 설정 (LocalTuya) |
| 안방 히터 플러그 | Switch | `switch.anbang_hiteo_peulreogeu` | 히터 전원 플러그 (Canonical) |
| 안방 재실센서 | Binary Sensor | `binary_sensor.anbang_presence` | MQTT mmWave 메인 재실 감지 |
| 안방 침대 재실센서 | Binary Sensor | `binary_sensor.anbang_bedside_presence` | LocalTuya 침대 부근 재실 (시간 한정 사용) |
| 안방 침대 재실 스위치 | Switch | `switch.anbang_bedside_presence_switch` | 침대 재실 헬퍼 채널 |
| 안방 책상 선풍기 | Switch | `switch.anbang_desk_fan` | 책상 멀티탭 outlet 1 |
| 안방 책상 마이크 | Switch | `switch.anbang_desk_mic` | 책상 멀티탭 outlet 2 |
| 안방 책상 스피커 | Switch | `switch.anbang_desk_speaker` | 책상 멀티탭 outlet 3 |
| 안방 침대 조명 | Switch | `switch.anbang_bedside_light` | 침대 머리맡 조명 |
| 안방 침대 선풍기 | Switch | `switch.anbang_bedside_fan` | 침대 머리맡 선풍기 |
| 안방 온도 센서 | Sensor | `sensor.anbang_temperature` | 실내 온도 |
| 안방 습도 센서 | Sensor | `sensor.anbang_humidity` | 실내 습도 |
| 안방 굿나잇 가상스위치 | Input Boolean | `input_boolean.gasang_anbang_gusnais` | 굿나잇 로직 헬퍼 |

---

### 4-2. 거실

| 디바이스 | 타입 | 엔티티 ID | 역할 |
|---|---|---|---|
| 거실 TV | Media Player | `media_player.geosil_tv_smartthings` | SmartThings 통합 주 TV |
| 거실 천장 조명 | Switch | `switch.geosil_ceiling_light` | 메인 조명 |
| 거실 스탠드 조명 | Light | `light.geosil_stand_lighting` | 분위기 조명 |
| 거실 라인 조명 | Light | `light.geosil_keoteun_rain_jomyeong_rokeol` | 커튼 라인 조명 (로컬) |
| 거실 라인 조명 전원 | Switch | `switch.geosil_line_lighting_plug` | 라인 조명 전원 스위치 |
| 거실 재실 감지 | Binary Sensor | `binary_sensor.geosil_presence` | 거실 mmWave 재실센서 |
| 거실 TV 조도 | Sensor | `sensor.geosil_tv_illuminance` | TV 주변 조도 측정 |

---

### 4-3. 주방

| 디바이스 | 타입 | 엔티티 ID | 역할 |
|---|---|---|---|
| 주방 천장 조명 | Switch | `switch.jubang_ceiling_light` | 메인 조명 |
| 주방 드라이기 플러그 | Switch | `switch.jubang_deuraigi_peulreogeu_rokeol` | 드라이기 전원 (로컬) |
| 주방 재실 감지 | Binary Sensor | `binary_sensor.jubang_presence` | 주방 mmWave 재실센서 |
| 주방 재실 센서 플러그 | Switch | `switch.jubang_presence_sensor_plug` | 재실센서 전원 멀티탭 |
| 주방 에어컨 IR 허브 | Switch | `switch.jubang_ac_remote_hub` | AC IR 허브 전원 |
| 주방 라인 조명 플러그 | Switch | `switch.jubang_line_lighting_plug` | 주방 라인 조명 전원 멀티탭 |
| 주방 원 진동센서 | Binary Sensor | `binary_sensor.jubang_round_vibration` | 칼집 진동 감지용 |

---

### 4-4. 옷방

| 디바이스 | 타입 | 엔티티 ID | 역할 |
|---|---|---|---|
| 옷방 천장 조명 | Switch | `switch.osbang_ceiling_light` | 메인 조명 |
| 옷방 재실 감지 | Binary Sensor | `binary_sensor.osbang_presence` | 재실 감지 |
| 옷방 온도 (로컬) | Sensor | `sensor.osbang_ondo_rokeol` | 온도 (LocalTuya 활성) |
| 옷방 습도 (로컬) | Sensor | `sensor.osbang_seubdo_rokeol` | 습도 (LocalTuya 활성) |
| 옷방 제습기 | Humidifier | `humidifier.osbang_jeseubgi_rokeol_naebuseubdo` | 제습기 메인 컨트롤 (LocalTuya climate) |
| 옷방 제습기 전원(내부용) | Switch | `switch.osbang_jeseubgi_jeonweon_rokeol` | 제습기 내부 전원층 (UI 숨김) |

> **설계 의도**: 제습기는 `humidifier` 엔티티 하나만 사용자/자동화/추천에 노출. 내부 전원 switch는 UI에서 숨겨 운영 혼잡도 방지.

---

### 4-5. 화장실

| 디바이스 | 타입 | 엔티티 ID | 역할 |
|---|---|---|---|
| 화장실 천장 조명 | Switch | `switch.hwajangsil_ceiling_light` | 메인 조명 |
| 화장실 환풍기 | Switch | `switch.hwajangsil_vent_fan` | 환풍기 |
| 화장실 재실 감지 | Binary Sensor | `binary_sensor.hwajangsil_presence` | 재실 감지 |
| 화장실 도어 센서 | Binary Sensor | `binary_sensor.hwajangsil_door_contact` | 문 개폐 감지 (Zigbee) |
| 화장실 가상 스위치 | Input Boolean | `input_boolean.gasang_hwajangsil` | 환풍기 타이머 로직 헬퍼 |

---

### 4-6. 현관

| 디바이스 | 타입 | 엔티티 ID | 역할 |
|---|---|---|---|
| 현관 도어 센서 | Binary Sensor | `binary_sensor.hyeongwan_door` | 현관문 개폐 감지 |
| 현관 도어 변조 감지 | Binary Sensor | `binary_sensor.hyeongwan_door_tamper` | 도어센서 탬퍼 감지 |
| 현관 도어 가상 스위치 | Input Boolean | `input_boolean.gasang_hyeongwan_doeo` | 도어 연동 헬퍼 |
| 현관 외출 가상 스위치 1 | Input Boolean | `input_boolean.gasang_hyeongwan_oecul_1` | 외출 모드 트리거 헬퍼 |
| 현관 외출 가상 스위치 2 | Input Boolean | `input_boolean.gasang_hyeongwan_oecul_2` | 외출 모드 체인 헬퍼 |

---

## 5. 자동화 인벤토리 (26개 이상, SmartThings/Tuya → HA 마이그레이션)

### 5-1. 자동화 마이그레이션 방법론

모든 자동화는 다음 절차로 마이그레이션되었다:

1. 기존 앱 루틴을 **스크린캡처 + 수동 문서화** (`automation_external_inventory_v1.md`)
2. 각 트리거/조건/액션을 **Canonical Entity ID로 매핑** (mapping assumption 명시)
3. HA YAML 자동화로 재작성 (`automation_standard_v1.md` 준수)
4. 실환경 테스트 후 기존 앱 루틴 비활성화

---

### 5-2. 자동화 목록 (전체)

#### [조명] 재실 연동

| ID | 이름 | 트리거 | 대상 |
|---|---|---|---|
| 001 | 옷방 In/Out | `binary_sensor.osbang_presence` | `switch.osbang_ceiling_light` |
| 002 | 화장실 재실 점등/소등 | `binary_sensor.hwajangsil_presence` + 도어 조건 | `switch.hwajangsil_ceiling_light`, `switch.hwajangsil_vent_fan` |
| 009 | 안방→거실 조명 핸드오버 | 거실 재실 ON + 안방 재실 OFF + 안방조명 ON | 거실 커튼불 ON, 안방불 OFF, 거실 스탠드 ON |
| 011 | 주방등 Off (재실 해제) | `binary_sensor.jubang_presence` OFF | `switch.jubang_ceiling_light` |

#### [조명] 크로스룸 / 야간 로직

| ID | 이름 | 조건 | 대상 |
|---|---|---|---|
| 003 | 밤에 거실 Off | 거실 재실 None AND 안방 재실 Present (23:00~06:00) | 거실 커튼불, 거실 스탠드 OFF |
| 010 | 안방의자 앉으면 안방불 ON | 의자 진동 감지 + 안방 조명 OFF + 커튼 닫혀있음 | 스피커/선풍기/마이크/천장照 ON |

#### [취침] 굿나잇/잘준비 루틴

| ID | 이름 | 트리거 | 액션 |
|---|---|---|---|
| 004 | 침대 누우면 잘준비모드 | `binary_sensor.anbang_bedside_presence` ON | 전기장판 ON, 커튼 닫기, 침대불 ON, 침대선풍기 ON, 스탠드 1%, 천장불 OFF |
| 005 | 침대 재실 헬퍼 ON | 매일 23:00 | `switch.anbang_bedside_presence_switch` ON |
| 006 | 굿나잇시 침대 재실 OFF | 침대불 OFF → | 침대 재실 헬퍼 OFF, 굿나잇 가상스위치 OFF |

#### [기상] 기상 루틴

| ID | 이름 | 조건 | 액션 |
|---|---|---|---|
| 021 | 기상시 안방불 off | 06:00~12:01, 안방불 ON AND 화장실불 ON, 하루 1회 | 안방불 OFF, 침대선풍기 OFF |

#### [공조] 환경 자동 제어

| ID | 이름 | 트리거/조건 | 대상 |
|---|---|---|---|
| 012 | 옷방 제습기 ON | 도어 가상스위치 OFF AND 내부/외부 습도 > 50% | `humidifier.osbang_jeseubgi_rokeol_naebuseubdo` |
| 013 | 옷방 제습기 OFF | 옷방 습도 < 42% → | 제습기 OFF + 알림 발송 |
| 014 | 새벽 히터 ON/OFF | 매일 05:00 | 히터 ON → 30분 대기 → 히터 OFF |
| 015 | 가습기 ON | 안방 습도 < 45% | `switch.anbang_gaseubgi_peulreogeu_rokeol` |
| 016 | 가습기 OFF | 안방 습도 > 60% | `switch.anbang_gaseubgi_peulreogeu_rokeol` |

#### [환풍] 화장실 환풍기 타이머 시퀀스

| ID | 이름 | 로직 |
|---|---|---|
| 023 | 화장실 5분 이상 환풍기 ON | 가상스위치 ON + 화장실 불 OFF → 환풍기 켜기 → 3초 → 가상스위치 리셋 → 6분 57초 → 환풍기 끄기 |
| 024 | 화장실 가상스위치 켜기 | 화장실 불 ON 3분 30초 이상 지속 → 가상스위치 ON |

> **설계 의도**: 화장실 사용 시간이 3분 30초를 넘으면 자동으로 장시간 환풍 사이클을 기동. 가상스위치를 중간 레이어로 사용하여 상태 전이를 깔끔하게 분리.

#### [외출] 외출 모드

| ID | 이름 | 로직 |
|---|---|---|
| 008 | 외출 가상2 ON | 외출 가상1 ON 시 (전 방 재실 None 조건) → 외출 가상2 ON |
| 017 | 현관 도어 열림 | 현관 도어 센서 → 도어 가상스위치 ON |
| 018 | 현관 도어 닫힘 | 현관 도어 센서 닫힘 → 도어 가상스위치 OFF |
| 022 | 외출 가상스위치 자동 리셋 | 외출 가상1 ON 상태로 1분 이상 유지 → 자동 OFF |

#### [스케줄] 일출/일몰/일과

| ID | 이름 | 로직 |
|---|---|---|
| 019 | 일몰에 커튼 닫기 | 일몰 1분 전 → `cover.anbang_curtain` 닫기 |
| 020 | 데일리 루틴 스피커 | 매일 05:59 스피커 OFF → 06:02 스피커 ON (전원 사이클) |

#### [센서이벤트] 진동 기반 트리거

| ID | 이름 | 트리거 | 액션 |
|---|---|---|---|
| 007 | 칼집문 열 때 주방등 ON | 진동센서 Vibration OR Tilt (주방 재실 중) | `switch.jubang_ceiling_light` ON |
| 025 | 드라이기 켜면 라인조명 ON | `switch.jubang_deuraigi_peulreogeu_rokeol` ON | `switch.jubang_line_lighting_plug` ON |
| 026 | 드라이기 사용 10분 후 라인조명 OFF | 드라이기 ON 20초 이상 → 11분 대기 → 라인조명 OFF | |

---

## 6. iOS 단축어 (Shortcuts) 인벤토리

### 6-1. 주요 단축어 루틴

| 단축어 이름 | 의도 | 주요 액션 순서 |
|---|---|---|
| `굿모닝` | 기상 멀티액션 루틴 | 히터끄기 → 환풍기켜기 → 커튼열기 → 안방조명켜기 → Too dark → 안방불켜기 → 전기장판끄기 → TV켜기 → 커튼불켜기 → 음악재생 |
| `굿나잇` | 취침 조명 OFF | 침대불끄기 → 안방조명끄기 |
| `잘 준비해줘` | 취침 준비 환경 세팅 | 커튼닫기 → 전기장판켜기 → Too bright(1% 2000K) → 침대불켜기 → 안방불끄기 |

### 6-2. 스탠드 조명 서브루틴

| 서브루틴 | 역할 | 설정 |
|---|---|---|
| `Too dark` | 밝은 모드 | 밝기 100%, 색온도 태양 기반 |
| `Too bright` | 취침 모드 | 밝기 1%, 색온도 2000K |

### 6-3. iPhone 자동화 (개인용)

| 자동화 | 트리거 | 액션 |
|---|---|---|
| A001 | 매일 오후 4:06 (시간 조정 가능) | 음량 80% → `굿모닝` 단축어 실행 |
| A002 | iPhone이 홈 Wi-Fi `SK_AA9E_2.4G` 연결 시 | 스피커 연결 → 음량 26% → 음악 실행 (귀가 감지) |
| A003 | iPhone이 홈 Wi-Fi 연결 해제 시 | 날짜 저장 → 외출 가상스위치 ON → 카카오버스 앱 열기 (외출 감지) |

> **A002/A003 설계 포인트**: Wi-Fi SSID 연결/해제로 귀가/외출을 감지하여, HA 외출 모드 연동. GPS나 Bluetooth 없이 Wi-Fi 기반으로 구현한 경량 Presence Detection.

---

## 7. 표준 설계 (Standards)

### 7-1. 네이밍 표준 (naming_standard_v1.md)

#### 2계층 모델

| 계층 | 패턴 | 예시 |
|---|---|---|
| 디바이스명 | `[영역] [기기명]` | `안방 가습기`, `거실 TV` |
| 엔티티 표시명 | `[영역] [기기명] [기능/상세]` | `안방 가습기 플러그`, `안방 가습기 전력` |

#### 영역 ID 표준

| 한글 | Canonical ID |
|---|---|
| 거실 | `geosil` |
| 주방 | `jubang` |
| 안방 | `anbang` |
| 옷방 | `osbang` |
| 화장실 | `hwajangsil` |
| 현관 | `hyeongwan` |

#### 엔티티 ID 규칙

```
domain.area_device_detail
```

- 소문자 snake_case
- 영어/로마자 표기 통일 (transliteration 방식 혼용 금지)
- 벤더명 포함 금지
- `_2`, `_1` 등 임시 suffix 지양

---

### 7-2. 자동화 표준 (automation_standard_v1.md)

#### Alias 패턴

```
[분류] [영역] [행동] ([기준])
```

예: `[조명] 옷방 자동 점등/소등 (재실 연동)`

#### YAML 구조 순서

```yaml
alias: ...
description: ...
mode: restart  # 기본값
trigger: ...
condition: ...  # 불필요시 생략
action: ...
```

#### 대표 자동화 템플릿

```yaml
alias: "[조명] 옷방 자동 점등/소등 (재실 연동)"
description: "옷방 재실 상태에 따라 천장 조명을 자동으로 켜고 끕니다."
mode: restart
trigger:
  - platform: state
    entity_id: binary_sensor.osbang_presence
    to: "on"
    id: presence_on
  - platform: state
    entity_id: binary_sensor.osbang_presence
    to: "off"
    id: presence_off
action:
  - choose:
      - conditions:
          - condition: trigger
            id: presence_on
        sequence:
          - service: switch.turn_on
            target:
              entity_id: switch.osbang_ceiling_light
      - conditions:
          - condition: trigger
            id: presence_off
        sequence:
          - service: switch.turn_off
            target:
              entity_id: switch.osbang_ceiling_light
```

---

### 7-3. 디바이스 온보딩 규칙 (device_onboarding_rules_v1.md)

신규 기기가 시스템에 추가될 때 반드시 따르는 절차:

1. 통합이 생성한 live entity 확인
2. Canonical 방 이름/기기명 결정
3. Entity ID 및 Display Name 표준에 맞게 수정
4. Live Hardware Map 업데이트
5. 그 이후에만 대시보드/자동화에 노출

#### 엔티티 분류

| 분류 | 설명 | 대시보드 노출 |
|---|---|---|
| Core device layer | 실제 제어/센서 | 메인 대시보드 허용 |
| Helper layer | 가상스위치, 시나리오 헬퍼 | 레이블 명시 필요 |
| Tuning/config layer | 민감도, 거리 등 설정 | 메인 대시보드 금지 |
| Spare/reserve layer | 미사용 예비 | 숨김 처리 |

---

## 8. 추천 엔진 (Recommendation Engine)

### 8-1. 목적 및 설계 철학

행동 로그 기반의 **데이터 드리븐 자동화 추천 시스템**:

- 사용자가 수동으로 반복 조작하는 패턴을 탐지 → 자동화 후보 제안
- 자동화가 의도와 다르게 동작하는 경우(충돌/오동작) 감지 → 피드백 수집
- KPI 기반 에너지 절감 기여도 측정

### 8-2. 아키텍처 레이어

```
1. core/
   - 도메인 엔티티, 규칙, KPI 공식, 스코어링 로직
   - HA / SQLite 의존성 없음 (순수 도메인)

2. adapters/
   - ha_client.py: HA REST API 접근
   - repository_sqlite.py: SQLite 지속성

3. services/
   - collect_service: 관찰 이벤트 수집
   - detection_service: 규칙 탐지 실행
   - proposal_service: 추천 후보 저장 (proposal-only)
   - kpi_service: KPI 스냅샷 계산/저장
   - ops_summary_service: 대시보드용 Top-Card 요약
   - dashboard_card_service: HA Markdown 카드 페이로드 생성
   - pipeline_service: 일일 실행 오케스트레이션
   - feedback_service: 사용자 피드백 수집 (intended/unintended)
   - validation_service: Canonical entity 기준선 검증

4. interfaces/
   - cli.py: 단일 CLI 진입점
```

### 8-3. 이벤트 로그 스키마

```text
- timestamp
- entity_id
- actor_type         (manual | automation | system)
- action
- pre_state
- post_state
- source_automation
- result             (success | failed | cancelled)
- reason_code
```

> **원칙**: fallback 값 합성 없음. actor 분류 불가 시 실행 자체가 명시적 실패.

### 8-4. CLI 명령 전체 목록

```bash
# DB 초기화
reco-engine init-db --db data/reco_engine.db

# 로그북 수집 (HA Logbook API → SQLite)
reco-engine collect-logbook --db data/reco_engine.db --ha-url <url> --ha-token <token> --hours 24

# 규칙 탐지
reco-engine detect --db data/reco_engine.db --policy config/policy.toml

# 추천 후보 생성
reco-engine propose --db data/reco_engine.db --policy config/policy.toml

# 개입 이벤트 보강 (3분 윈도우)
reco-engine enrich-interventions --db data/reco_engine.db --window-minutes 3

# 후보 승인
reco-engine approve-candidates --db data/reco_engine.db --candidate-ids 1,2,3

# 테스트 배치 시작 (7일 테스트)
reco-engine start-test-batch --db data/reco_engine.db --candidate-ids 1,2,3 --days 7

# 테스트 배치 완료
reco-engine finalize-test-batch --db data/reco_engine.db --batch-id 1 --result pass

# 롤백
reco-engine rollback-batch --db data/reco_engine.db --batch-id 1 --reason "rollback reason"

# Canonical entity 검증
reco-engine validate-canonical --ha-url <url> --ha-token <token> --canonical config/entities_canonical.toml

# Utility meter 검증
reco-engine validate-utility --ha-url <url> --ha-token <token> --canonical config/entities_canonical.toml

# KPI 계산 (수동 에너지 입력)
reco-engine kpi --db data/reco_engine.db --monthly-energy-kwh 12.5

# KPI 계산 (HA utility meter 자동 읽기)
reco-engine kpi-auto --db data/reco_engine.db --ha-url <url> --ha-token <token> --canonical config/entities_canonical.toml

# Ops 요약 (대시보드용)
reco-engine ops-summary --db data/reco_engine.db

# 대시보드 카드 JSON 생성
reco-engine dashboard-cards --db data/reco_engine.db --output data/dashboard_cards.json

# 일일 전체 파이프라인 실행
reco-engine run-daily-cycle --db ... --ha-url ... --ha-token ... --policy ... --canonical ... --collect-hours 24 --intervention-window-minutes 3

# 충돌 피드백 수집
reco-engine ingest-conflict-feedback --db data/reco_engine.db
```

### 8-5. 대시보드 카드 출력 구조

추천 엔진이 생성하는 HA Markdown 카드는 정확히 3장:

- **오늘의 후보 자동화** — 상태: `proposed | approved | testing`
- **충돌/오동작 상위 5개** — `rule_code=condition_conflict`
- **절감 기여 상위 5개** — `rule_code in manual_repeat / manual_cancel_after_auto`

---

## 9. 구현 스크립트 주요 내용

### 9-1. `rebuild_tuya_local_10_devices.py`

**목적**: 10개의 Tuya 로컬 기기를 HA Config Flow API를 통해 자동으로 재등록하는 스크립트

**등록 대상 기기** (모두 고정 IP):

| 기기명 | IP 주소 | 프로토콜 |
|---|---|---|
| 안방 가습기 플러그 | 192.168.10.123 | 3.3/auto/3.4/3.5 |
| 안방 전기장판 플러그 | 192.168.10.100 | 3.3/auto/3.4/3.5 |
| 거실 라인 조명 전원 스위치 | 192.168.10.128 | 3.3/auto/3.4/3.5 |
| 안방 히터 플러그 | 192.168.10.126 | 3.3/auto/3.4/3.5 |
| 주방 드라이기 플러그 | 192.168.10.125 | 3.3/auto/3.4/3.5 |
| 주방 천장 조명 | 192.168.10.137 | 3.3/auto/3.4/3.5 |
| 거실 천장 조명 | 192.168.10.130 | 3.3/auto/3.4/3.5 |
| 옷방 천장 조명 | 192.168.10.133 | 3.3/auto/3.4/3.5 |
| 안방 천장 조명 | 192.168.10.129 | 3.3/auto/3.4/3.5 |
| 거실 스탠드 조명 | 192.168.10.149 | 3.5/auto/3.4/3.3 |

**핵심 로직**:

```python
# 프로토콜 버전별 fallback (3.3 → auto → 3.4 → 3.5 순서 시도)
for proto in dev["protocols"]:
    # 1단계: flow 초기화
    # 2단계: manual setup_mode 선택
    # 3단계: device_id + host + local_key + protocol_version 전송
    # 4단계: already_configured 체크 (幂等성 보장)
    # 5단계: type 선택 (keyword 기반 자동 매칭)
    # 6단계: entity 이름 설정 + create_entry 완료
```

- **프로토콜 자동 fallback**: 각 기기에 맞는 프로토콜 버전을 우선순위대로 시도
- **type 자동 선택**: `smartplug`, `plug`, `outlet` 등 keyword list 기반 fuzzy 매칭
- **재시도 로직**: `requests.post` 3회 재시도, exponential backoff
- **결과 저장**: `tuya_local_rebuild_10_results.json` 으로 실행 결과 전체 영속화

---

### 9-2. `scripts/ha_entity_management/` 스크립트군

**목적**: 대규모 엔티티 표준화 작업을 자동화한 관리 도구 모음

| 스크립트 | 역할 |
|---|---|
| `analyze_ha_entities.py` | 현재 live 엔티티 전체 목록 분석 |
| `analyze_duplicates.py` | 중복 엔티티 그룹 탐지 |
| `analyze_final_dups.py` | 최종 중복 목록 보고 |
| `analyze_naming.py` | 네이밍 패턴 위반 엔티티 탐지 |
| `dry_run_rename.py` | 이름 변경 시뮬레이션 (실제 변경 없음) |
| `execute_rename.py` | 실제 엔티티 ID/이름 일괄 변경 실행 |
| `disable_entities.py` | 불필요 엔티티 일괄 비활성화 |
| `disable_empty_devices.py` | 엔티티 없는 빈 디바이스 비활성화 |
| `move_entities_to_raw.py` | 엔티티를 raw/예비 영역으로 이동 |
| `check_remaining.py` | 표준화 미완료 엔티티 잔여 확인 |
| `final_sweep.py` | 최종 전수 검사 |
| `verify_redundancy.py` | 중복 자동화/엔티티 이중 검증 |
| `optimize_lovelace.py` | Lovelace 대시보드 JSON 정리 |

---

## 10. 검증 파이프라인 (Architecture Phases)

### Phase 1: 기반 구축 및 Entity 로그 수집
- `collect_service` 구현, HA Logbook API → SQLite 수집

### Phase 2: Canonical Baseline 검증
- `entities_canonical.toml` 작성
- `validate-canonical` 명령 → **결과: ok=true, errors=0**
- `validate-utility` 명령 → 일일 에너지 누적 entity 4개 `unknown` 상태 발견 (초기 데이터 없음)
- 비활성/숨김 reserve 엔티티 4개 확인 (운영 무관)

### Phase 3: Utility Meter 수리
- 일일 에너지 누적 entity 매핑/속성 수정 → `unknown` 상태 해제

### Phase 4: 수동 개입 파이프라인
- `enrich-interventions` 구현 (3분 윈도우 내 수동 조작 감지)

### Phase 5: Actor 분류 강화
- `actor_type` 분류 로직 하드닝 — fallback 없이 분류 불가 시 명시적 실패

### Phase 6: 승인/테스트/롤백 사이클
- `approve-candidates`, `start-test-batch`, `finalize-test-batch`, `rollback-batch` 구현

### Phase 7: Ops Summary + KPI Auto
- `ops-summary`, `kpi-auto` 구현
- KPI monthly energy를 HA utility meter에서 직접 읽어 자동 계산
- invalid 상태(`unknown`, `unavailable`, 음수) → 즉시 실패 (fallback 없음)

### Phase 8: 대시보드 및 일일 사이클
- `dashboard-cards` 출력 카드 3장 확정
- `run-daily-cycle` 통합 오케스트레이션 명령 구현

### Phase 9: 충돌 피드백 버튼
- HA helper(`input_select`) 기반 충돌 피드백 수집 UI
- `ingest-conflict-feedback` CLI 명령으로 DB에 적재

---

## 11. 운영 원칙 및 거버넌스

### 11-1. 소스 오브 트루스(Source of Truth) 원칙

```
master_hardware_map_live.md  ← 현재 live entity 정규 목록
current_operating_map.md     ← 방별 운영 baseline 요약
naming_standard_v1.md        ← 명명 규칙
```

- 모든 대시보드/자동화 변경은 **이 문서들을 먼저 확인 후** 진행
- live entity 변경 시 이 파일들을 가장 먼저 업데이트

### 11-2. 엔티티 상태 관리

| 상태 | 의미 |
|---|---|
| Active | 운영 중, 대시보드/자동화 노출 가능 |
| Disabled | 비활성화됨, 플랫폼 수준 off |
| Hidden (`hidden_by=user`) | 기능 유지, UI에서만 숨김 |
| Unavailable | 기기 응답없음, 운영 대상 추적 필요 |

### 11-3. 절대 금지 사항

- 외부 자동화 비활성화는 **HA 자동화 실환경 테스트 확인 후**에만
- Rename은 **dry_run 먼저, dry_run 결과 확인 후 execute**
- 임시 ID(`_2`, `unused`, `main`) 운영 투입 금지
- Fallback 데이터 합성 금지 (추천 엔진 integrity 원칙)

---

## 12. 프로젝트 디렉토리 구조

```
HAOS_Control/
├── config/
│   ├── entities_canonical.toml    # Canonical entity 기준선
│   └── policy.toml                # 추천 엔진 정책
├── data/
│   └── reco_engine.db             # SQLite DB
├── docs/
│   ├── master_hardware_map_live.md
│   ├── current_operating_map.md
│   ├── naming_standard_v1.md
│   ├── automation_standard_v1.md
│   ├── automation_external_inventory_v1.md
│   ├── device_onboarding_rules_v1.md
│   ├── ios_shortcuts_inventory_v1.md
│   ├── standardization_plan_*.md  (방별 표준화 계획)
│   └── architecture/
│       ├── recommendation_engine_architecture_v1.md
│       └── phase2~phase9_*.md     (개발 단계별 기록)
├── scripts/
│   ├── rebuild_tuya_local_10_devices.py
│   ├── ha_entity_management/      (16개 엔티티 관리 스크립트)
│   └── rooms/                     (방별 디바이스 스크립트)
│       ├── anbang/
│       ├── geosil/
│       ├── jubang/
│       ├── osbang/
│       ├── hwajangsil/
│       └── hyeongwan/
├── src/
│   └── reco_engine/
│       ├── core/
│       ├── adapters/
│       ├── services/
│       └── interfaces/cli.py
├── localtuya_configuration_data.md
├── lovelace_active.json
└── pyproject.toml
```

---

## 13. 핵심 기술적 성과 요약

| 성과 | 상세 내용 |
|---|---|
| **Local-First 전환** | SmartThings/Tuya 클라우드 의존 → LocalTuya로 완전 로컬 통신 |
| **26개 이상 자동화 마이그레이션** | 3개 플랫폼(SmartThings, Tuya, iOS 단축어) 자동화를 HA로 통합 |
| **표준 설계** | 네이밍/온보딩/자동화 표준 v1 작성, 전체 엔티티 적용 |
| **엔티티 대규모 정리** | 16개 스크립트로 HA 전체 entity 분석/중복제거/리네이밍 자동화 |
| **탐지 가능한 자동 onboarding** | Tuya 10기기 자동 재등록 스크립트 (프로토콜 fallback 포함) |
| **추천 엔진 설계 및 구현** | 9단계 Phase로 log→detect→propose→KPI→dashboard 파이프라인 구현 |
| **Canonical 검증** | validate-canonical ok=true (0 errors), 무결성 유지 |
| **크로스 플랫폼 설계** | macOS/Windows 동시 실행 가능한 추천 엔진 CLI |

---

## 14. 향후 계획 (Next Steps)

- [ ] SmartThings 자동화 전부 HA YAML로 교체 완료
- [ ] 방별 표준화 계획(`standardization_plan_*.md`) 순차 실행
- [ ] 추천 엔진 일일 파이프라인 cron 등록 및 자동 운영
- [ ] Utility meter daily entity `unknown` 상태 완전 해소
- [ ] 충돌 피드백 루프 실데이터 수집 시작
- [ ] iOS 단축어 → HA Script 전환 (완전 HA 중심화)

---

*이 문서는 포트폴리오 및 자기소개서 작성의 원본 소스입니다. 세부 항목은 이 문서를 기반으로 필요에 따라 압축·재구성하세요.*
