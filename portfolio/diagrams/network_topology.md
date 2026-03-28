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

## 2) 데이터 흐름

```mermaid
flowchart TB
    T["트리거: 센서/시간/사용자"] --> A["HA Automation Engine"]
    A --> C1["제어 경로1: MQTT/Zigbee"]
    A --> C2["제어 경로2: LocalTuya"]
    A --> C3["보조 경로: SmartThings"]

    C1 --> D["디바이스 동작"]
    C2 --> D
    C3 --> D

    D --> E["상태 이벤트 수집"]
    E --> F["로그/지표/추천 엔진"]
    F --> G["대시보드/운영 판단"]
```

## 3) 네트워크 엔지니어 관점 포인트

- L2/L3 경계 단순화: 단일 내부망에서 IoT 디바이스 식별/관리
- 주소 관리: DHCP 예약 기반 운영으로 장치 식별 안정화
- 프로토콜 분리: Zigbee(Mesh), MQTT(메시지 버스), Wi-Fi(디바이스 제어) 역할 분리
- 운영 경로 분리: 로컬 우선 + 클라우드 보조

## 4) 장애 대응 경로

- 증상 탐지: timeout/offline/route failure
- 분류: 통신 문제 / 전원 문제 / 통합 참조 문제
- 조치: 채널 조정, 재조인, 엔티티 참조 복구
- 검증: 자동화 트레이스/상태 변경/실행 로그 확인
