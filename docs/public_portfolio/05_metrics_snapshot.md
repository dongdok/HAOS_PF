# 운영 지표 스냅샷 (과장 방지 정의 포함)

> 기준 시각: 2026-03-20 (Asia/Seoul)
> 데이터 출처: Home Assistant 실운영 API(`ha_get_overview`, `ha_get_integration`, `ha_list_services`)

## 1) 핵심 수치

- 엔티티: **406개**
- 통합구성요소(Config Entry): **49개** (`loaded 46`, `not_loaded 3`)
- 서비스 엔드포인트: **343개**

## 2) 지표 정의 (중요)

- 엔티티 406개
  - 센서/스위치/조명/자동화/스크립트/헬퍼 등 운영 객체 총량

- 통합구성요소 49개
  - 통합 이름 종류가 아니라, Home Assistant 설정 엔트리 개수
  - 예: mobile_app 2개, homekit 브리지 여러 개, utility_meter 다중 엔트리

- 서비스 엔드포인트 343개
  - `light.turn_on`, `automation.trigger` 같은 호출 가능한 명령 종류 수
  - “343개를 통합”이 아니라 “343개 서비스 호출이 가능한 환경”이 정확함

## 3) 도메인 구성(일부)

- `sensor`: 104
- `script`: 87
- `number`: 38
- `switch`: 34
- `automation`: 34 (`on 32`, `off 2`)
- `binary_sensor`: 23

## 4) 포트폴리오 표기 권장 문장

"HAOS에서 엔티티 406개를 운영하고, 통합구성요소 49개(활성 46)를 관리했으며,
서비스 엔드포인트 343개가 호출 가능한 자동화 환경을 구축·운영했습니다."

## 5) 해석 주의

- 지표는 시점 기반 값이므로 배포 시각에 따라 소폭 변동 가능
- 제출 문서에는 기준 날짜/시간을 반드시 함께 표기
