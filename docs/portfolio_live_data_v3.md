# HAOS_Control — Protocol & Device Engineering (포트폴리오 전문성 심화)

> 데이터 기준일: 2026-03-18  
> 이 문서는 시스템의 하부 레이어(L1-L3)인 프로토콜 통신과 기기 엔지니어링 상세를 분석하여, 하드웨어 계층에 대한 깊은 이해도를 증명합니다.

---

## 1. Local-First 프로토콜 엔지니어링

### 1-1. LocalTuya 및 Tuya Local 통합 (Advanced Connectivity)
단순한 클라우드 연동을 넘어, 제조사 프로토콜을 직접 분석하여 로컬 제어망을 구축했습니다.
- **프로토콜 버전 최적화**: 기기별 특성에 따라 **Tuya Protocol 3.3 및 3.5**를 선별 적용하여 통신 안정성을 확보했습니다.
- **Data Point(DP) 매핑 전문성**: 각 기기의 기능 코드(`switch_1`, `child_lock`, `overcharge_switch`, `bright_value_v2` 등)를 HA 엔티티 속성과 1:1로 매핑하여 하드웨어의 모든 기능을 소프트웨어적으로 완벽히 제어합니다.

### 1-2. 보안 통신 인프라 (Security & Credentials)
- **자격 증명 관리**: 17개 이상의 핵심 기기에 대해 **Device ID**와 **Local Key**를 마스터 테이블로 관리하여, 클라우드 의존성 없이 독립적인 운영이 가능한 '생존성 높은' 시스템을 구축했습니다.
- **IP/MAC 정적 바인딩**: 모든 IoT 기기에 대해 고정 IP 및 MAC 주소 관리를 통해 네트워크 토폴로지의 예측 가능성을 구현했습니다.

---

## 2. 아키텍처적 통찰 및 문제 해결 (Problem Solving)

### 2-1. 배터리 기기 통신 최적화 전략
- **분석 역량**: Wi-Fi 기반 배터리 센서(도어 센서 등)의 **딥 슬립(Deep Sleep)** 특성을 정확히 파악하여, TCP 상시 연결 방식인 LocalTuya 대신 이벤트 기반 연동(Cloud/Hub)을 선택하는 합리적 기술 의사결정을 내렸습니다.
- **트러블슈팅**: ARP 스캔 및 네트워크 트리거 분석을 통해 IP 할당 문제를 해결하고, 지연 시간(Latency) 최소화를 위한 네트워크 환경을 조성했습니다.

---

## 3. 정밀 제어 시퀀스 (Precision Control)

### 3-1. 기기별 특화 기능 구현
- **가습기/제습기**: 단순 전원 제어를 넘어 `fan_speed_enum`, `dehumidify_set_value`, `anion` 등 고유 기능을 API 수준에서 제어합니다.
- **조명 시스템**: `colour_data_v2`, `scene_data_v2` 등 복잡한 페이로드를 직접 핸들링하여 색온도 및 모드 전환을 정밀하게 수행합니다.
- **에너지 세이프티**: `overcharge_switch`, `switch_inching` 등 산업용 제어기 수준의 안전 장치를 하드웨어 파라미터로 설정하여 시스템의 신뢰도를 높였습니다.

---

## 4. 최종 결론: Full-Stack Smart Home Architect

본 프로젝트를 통해 입증된 역량은 다음과 같습니다:
- **Frontend**: 사용자 중심의 시각화 및 정보 설계 (Lovelace UI/UX)
- **Logic**: 복잡한 조건 기반의 자동화 아키텍처 (34개 이상의 정밀 자동화)
- **Infrastructure**: 에너지 계층화 및 모바일 컨텍스트 연동
- **Protocol**: 기기 레벨의 DP 매핑 및 로컬 프로토콜(Zigbee, Tuya Local) 최적화
- **Documentation**: 전 공정의 체계적인 문서화 및 형상 관리

> 이 자료는 사용자의 Home Assistant OS가 단순한 '취미'를 넘어, **고도의 엔지니어링 원칙**에 따라 설계되고 운영되고 있음을 보여줍니다.
