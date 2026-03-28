# 네트워크 토폴로지 (공개용)

## 1) L1 설계도

```mermaid
flowchart LR
    subgraph External ["<b>1. 보안 및 외부 접속</b>"]
    direction TB
    ISP["인터넷 / ISP"]
    TS["Tailscale (보안 VPN)"]
    end

    subgraph Infra ["<b>2. 통합 인프라 및 데이터 허브</b>"]
    direction TB
    GTW["ER605 게이트웨이"]
    MQTT["MQTT 브로커 (데이터 허브)"]
    HAOS["통합 제어 노드 (HAOS)"]
    AN["데이터 분석 노드 (Ubuntu)"]
    end

    subgraph Protocols ["<b>3. 통신 프로토콜 및 메시</b>"]
    direction TB
    Z2M["Zigbee2MQTT"]
    COORD["SLZB Zigbee Coordinator"]
    end

    subgraph Devices ["<b>4. 필드 디바이스</b>"]
    direction TB
    Z_DEV["지그비 센서/조명/스위치"]
    W_DEV["로컬 Wi-Fi 기기 (LocalTuya)"]
    C_DEV["클라우드 가전 (SmartThings)"]
    end

    %% 연결 관계
    ISP & TS --> GTW
    GTW <--> MQTT

    %% 데이터 허브 중심 연결
    MQTT <-->|"시스템 통합 제어"| HAOS
    MQTT <-->|"프로토콜 변환"| Z2M

    %% 데이터 파이프라인
    HAOS <-->|"API 데이터 연계"| AN

    %% 물리 장치 연결
    Z2M --> COORD --> Z_DEV
    HAOS <-->|"로컬 Wi-Fi 제어"| W_DEV
    HAOS <-->|"보조 경로"| C_DEV

    %% 스타일링
    classDef default fill:#ffffff,stroke:#eee,stroke-width:1px;
    classDef highlight fill:#f3f0ff,stroke:#6c5ce7,stroke-width:2px;
    class GTW,MQTT,HAOS,AN highlight;
```

## 2) 제어 및 데이터 흐름 (System Workflow)

```mermaid
flowchart TB
    T["트리거: 센서 / 시간 / 사용자"] --> A["HA Automation Engine"]
    A --> C["제어 경로 (Local / Cloud)"]
    C --> D["디바이스 동작 (Actuator)"]
    D --> E["상태 이벤트 수집 (State Change)"]
    E --> F["데이터 분석 및 추천 엔진 (Ubuntu Node)"]
    F --> G["대시보드 / 운영 지표 시각화"]

    %% 피드백 루프 (AIOps 핵심)
    F -.->|"자동화 로직 제안 / 최적화 루프"| A
```

## 3) 운영 및 설계 포인트

- **서버 안정성 확보**: 가상화(Hyper-V)를 통해 제어용(HAOS)과 분석용(Ubuntu) 서버를 분리해서, 한쪽이 느려져도 집안 제어는 끊기지 않도록 구성
- **네트워크 단순화**: 단일 내부망 환경에서 400개 이상의 기기들을 중복 없이 식별하고 관리
- **고정 주소 운영**: 모든 기기에 고정 IP를 부여해서 공유기 재부팅이나 기기 교체 시에도 자동화가 깨지지 않게 유지
- **통신 간섭 최소화**: 와이파이와 지그비 간의 전파 간섭을 줄이기 위해 최적의 채널을 직접 지정해서 운영

## 4) 장애 대응 및 복구

- **상시 모니터링**: 응답 지연이나 기기 오프라인 상태를 로그를 통해 실시간으로 탐지
- **원인 분류**: 통신 문제, 전원 문제, 혹은 자동화 로직의 충돌인지 원인을 명확히 파악
- **복구 조치**: 신호 간섭 시 채널 조정, 기기 재조인 후 깨진 이름 복구 등 상황에 맞는 조치 수행
- **검증**: 자동화 실행 기록을 다시 확인해서 문제가 해결되었는지 최종 검토

## 5) 시스템 제원

| 항목 | 상세 사양 | 비고 |
| :--- | :--- | :--- |
| **서버 하드웨어** | Intel N100 저전력 Mini PC | 24/7 상시 운영 |
| **가상화 기술** | Windows 11 Pro + Hyper-V | 서버 자원 격리 |
| **노드 분리** | 제어용 HAOS / 분석용 Ubuntu | 운영 안정성 확보 |
| **저장소 관리** | LVM (Logical Volume Manager) | 용량 유연 확장 |
| **네트워크 관리** | TP-Link ER605 게이트웨이 | VPN 및 보안 관리 |
