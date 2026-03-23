# HAOS_PF

스마트홈 HAOS 포트폴리오 레포지토리입니다.
이 저장소는 **실운영 HAOS 프로젝트 전체 코드**가 아니라, 검토에 필요한 **설계/운영/장애대응/지표 문서**와 **민감정보 제거된 공개용 YAML 샘플**을 제공합니다.

## 빠른 보기

1. [프로젝트 요약](./portfolio/01_project_summary.md)
2. [네트워크 토폴로지](./portfolio/diagrams/network_topology.md)
3. [운영 장애 사례](./portfolio/cases/operations_incidents.md)
4. [자동화 사례 요약](./portfolio/cases/automation_case_studies.md)
5. [자동화 샘플 YAML](./portfolio/samples/README.md)
6. [운영 지표 스냅샷](./portfolio/metrics/metrics_snapshot.md)

## 문서 구조

- `portfolio/01_project_summary.md`: 프로젝트 배경, 설계 원칙, 역할
- `portfolio/diagrams/network_topology.md`: L1/L2 구조 및 데이터 흐름
- `portfolio/cases/operations_incidents.md`: 장애 대응 사례
- `portfolio/cases/automation_case_studies.md`: 자동화 설계 사례
- `portfolio/cases/automation_real_world_flows.md`: 생활 흐름 기반 자동화 예시
- `portfolio/metrics/metrics_snapshot.md`: 수치 지표(정의 포함)
- `portfolio/ops/public_release_checklist.md`: 공개 배포 체크리스트
- `portfolio/samples/README.md`: 공개용 YAML 샘플 모음 (자동화 구현 스타일)
- `portfolio/metrics/reliability_kpi.md`: 신뢰성 KPI 정의/표기 기준
- `portfolio/cases/incident_rca_samples.md`: 장애 원인분석(RCA) 샘플
- `portfolio/cases/integration_qa_matrix.md`: 3자 연동 QA 검증 표
- `portfolio/cases/commissioning_runbook.md`: 시운전 점검 절차

## 범위 및 보안

- 본 저장소는 공개용으로 민감정보(IP/MAC/토큰/개인 식별 데이터)를 제거했습니다.
- 실운영 설정 원문(`configuration.yaml`, `secrets.yaml`, 토큰 등)은 포함하지 않습니다.

## 기술 키워드

`IoT Network`, `Zigbee2MQTT`, `MQTT`, `LocalTuya`, `SmartThings`, `Troubleshooting`, `Incident Response`, `Operational Reliability`
