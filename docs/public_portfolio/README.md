# 공개용 IoT 네트워크 포트폴리오 (HAOS_Control)

이 폴더는 **채용 제출용 공개 버전**입니다.
민감정보(IP/MAC/토큰/개인 식별 데이터)는 제거했고, 네트워크 엔지니어 직무와 직접 연결되는 설계/운영/장애 대응 내용만 담았습니다.

## 포함 문서

1. [`01_project_summary.md`](./01_project_summary.md)
- 프로젝트 배경, 설계 원칙, 핵심 성과 요약

2. [`02_network_topology.md`](./02_network_topology.md)
- L1/L2 토폴로지, 데이터 흐름, 운영 경계

3. [`03_operations_incidents.md`](./03_operations_incidents.md)
- 실운영 장애 사례(증상/원인/조치/결과)

4. [`04_automation_case_studies.md`](./04_automation_case_studies.md)
- 자동화 사례를 네트워크 관점에서 설명

5. [`05_metrics_snapshot.md`](./05_metrics_snapshot.md)
- 수치 지표 정의와 운영 스냅샷

6. [`06_public_release_checklist.md`](./06_public_release_checklist.md)
- 공개 배포 전 보안/품질 점검 체크리스트

## 제출 시 사용 권장 순서

1. `01_project_summary.md`
2. `02_network_topology.md`
3. `03_operations_incidents.md`
4. `05_metrics_snapshot.md`
5. `04_automation_case_studies.md`

## 데이터 기준

- 기준 시각: 2026-03-20 (Asia/Seoul)
- 운영 데이터 출처: Home Assistant 실운영 시스템

## 공개본 제외 범위

아래 항목은 보안/개인정보 보호를 위해 공개본에서 제거했습니다.

- 내부 IP, MAC/IEEE 원문, 외부 접근 도메인/URL
- API 토큰, 계정 식별자, 자격증명, 웹훅/시크릿
- 생활 패턴이 과도하게 드러나는 원시 로그 원문
- 운영 설정 원문(`configuration.yaml`, `secrets.yaml`, 백업 아카이브)
