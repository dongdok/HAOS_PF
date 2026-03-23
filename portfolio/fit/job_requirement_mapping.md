# 공고 요구사항 매핑 (아카라라이프 스마트홈 시스템 엔지니어)

> 기준 공고: 사람인 rec_idx=53398935 (확인일: 2026-03-23)
> 작성 원칙: 확인 가능한 사실만 기재, 추정/과장 문구 미사용

## 1) 요구사항 대응표

| 공고 요구사항 | 내 수행 경험 | 증빙 문서 |
|---|---|---|
| 스마트홈 시스템 구성/설계 지원 | Home Assistant 중심 로컬 제어 구조 운영. Zigbee2MQTT, MQTT, LocalTuya를 통합 운용 | `portfolio/01_project_summary.md`, `portfolio/diagrams/network_topology.md` |
| 설치/시운전(Commissioning) 지원 | 현장 점검 항목 기반으로 통신/제어/상태 동기화 확인 절차 수행 | `portfolio/cases/commissioning_runbook.md` |
| 연동 이슈 대응 및 기술지원 | 월패드-서버-플랫폼 3자 연동 QA 수행, 장애 원인 분리 후 협력사와 수정 반영 | `portfolio/cases/integration_qa_matrix.md`, `portfolio/cases/operations_incidents.md` |
| 운영 중 장애 분석/복구 | Zigbee route error, delivery fail, 엔티티 참조 불일치 등 실제 이슈를 로그 기반으로 조치 | `portfolio/cases/incident_rca_samples.md` |
| 문서화 및 협업 | 변경 이력과 운영 기준 문서를 분리 관리, 재등록 시 참조 복구 절차 유지 | `portfolio/ops/public_release_checklist.md`, `portfolio/cases/commissioning_runbook.md` |

## 2) 우대사항 대응(직접 경험 기준)

- IoT/네트워크 운영 경험: 있음
  - 실운영 환경에서 Zigbee/Wi-Fi 혼합망 운용 및 문제 대응
- 프로토콜 이해(MQTT/Zigbee 등): 있음
  - MQTT Broker + Zigbee2MQTT 기반 제어/관측 경로 운영
- 설치/시운전 실무: 있음
  - 점검 항목 기반 검증 절차 수행 및 오픈 전 확인
- KNX/DALI: 본 포트폴리오 범위에서 직접 수행 내용 없음
- 중국어/영어 협업: 본 문서에 별도 증빙 없음

## 3) 면접에서 설명할 핵심 한 문장

"기능 구현보다 운영 안정성을 우선해, 현장 이슈를 로그로 재현하고 원인 분리 후 재발 방지 조건까지 반영하는 방식으로 스마트홈 시스템을 운영했습니다."
