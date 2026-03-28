# HAOS_PF (Infrastructure & Operations Log)

본 저장소는 **N100 서버와 Hyper-V 가상화** 환경에서 Home Assistant를 직접 운영하며 기록한 엔지니어링 로그입니다. 약 400여 개의 스마트홈 기기를 통합 관리하며 겪은 네트워크 설계, 장애 대응, 운영 지표를 사실 중심으로 정리했습니다.

---

## 📁 주요 운영 문서

1. **[프로젝트 요약](./portfolio/01_project_summary.md)**: 설계 철학 및 핵심 운영 성과
2. **[네트워크 토폴로지](./portfolio/diagrams/network_topology.md)**: L1 구성 및 데이터 흐름도 (Mermaid)
3. **[장애 대응 이력](./portfolio/cases/operations_incidents.md)**: 실제 발생한 이슈별 원인 분석 및 조치
4. **[자동화 설계 사례](./portfolio/cases/automation_case_studies.md)**: 안정성을 고려한 논리 설계
5. **[운영 수치 스냅샷](./portfolio/metrics/metrics_snapshot.md)**: 관리 엔티티 및 스택 통계
6. **[공개 릴리스 체크리스트](./06_public_release_checklist.md)**: 보안 및 정합성 검증 항목

---

## 🛠️ 시스템 환경 (System Specs)

- **Hardware**: Intel N100 저전력 서버
- **Virtualization**: Hyper-V (제어 노드 / 분석 노드 격리 운영)
- **Networking**: Zigbee, MQTT, Local Wi-Fi, Cloud Bridge
- **Scale**: 406 Entities, 343 Service Endpoints

---

## 🔒 보안 정책
- 민감한 개인정보(IP, MAC, Token)와 실제 운영 설정 원문은 포함되어 있지 않습니다.
- 모든 기능과 로그는 공개를 위해 비식별화 처리를 거쳤습니다.

---

`IoT Network`, `Zigbee2MQTT`, `MQTT`, `LocalTuya`, `SmartThings`, `Troubleshooting`, `Incident Response`, `Operational Reliability`
