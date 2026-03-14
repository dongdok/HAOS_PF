# Python Environment Guide v1

Last updated: 2026-03-10 (Asia/Seoul)
Scope: `/Users/dy/Desktop/HAOS_Control`

## 목적

이 저장소의 Python 실행 환경을 다음 2개로 고정합니다.

- 기본 작업환경: `.venv`
- Tuya 전용환경: `.tuya_env`

## 고정 정책

### 1) `.venv` (기본)

- 용도:
  - 일반 문서/스크립트 작업
  - HA 운영 보조 스크립트
  - 엔티티/자동화 점검 스크립트
- 원칙:
  - Tuya 전용 라이브러리 설치 금지
  - 평소 터미널 기본 활성 환경으로 사용

### 2) `.tuya_env` (Tuya 전용)

- 용도:
  - Tuya 클라우드/로컬 키 수집
  - TinyTuya 기반 진단/추출 작업
  - Tuya 계정/디바이스 API 관련 스크립트
- 원칙:
  - Tuya 관련 작업 외에는 사용하지 않음

## 현재 확인 상태 (2026-03-10)

- Python 버전:
  - `.venv`: `Python 3.13.7`
  - `.tuya_env`: `Python 3.13.7`
- 패키지 확인:
  - `tinytuya`는 `.tuya_env`에만 설치됨
  - `.venv`에는 Tuya 전용 패키지 없음

## 사용법

### 기본 작업 시작

```bash
cd /Users/dy/Desktop/HAOS_Control
source .venv/bin/activate
python -V
```

### Tuya 작업 시작

```bash
cd /Users/dy/Desktop/HAOS_Control
source .tuya_env/bin/activate
python -V
```

### 작업 종료

```bash
deactivate
```

## 빠른 확인 체크리스트

작업 전 아래 2가지만 확인:

1. `echo $VIRTUAL_ENV`
2. `python -V`

판단 기준:

- 일반 작업이면 경로가 `.../.venv` 여야 함
- Tuya 작업이면 경로가 `.../.tuya_env` 여야 함

## 권장 운영 규칙

- 쉘 최초 진입 시 `.venv`를 기본 활성화
- Tuya 작업이 끝나면 `deactivate` 후 `.venv`로 복귀
- 패키지 설치 시 항상 현재 활성 환경을 먼저 확인

## 금지 사항

- `.venv`에 Tuya 전용 의존성 혼합 설치
- `.tuya_env`에서 일반 운영 스크립트를 상시 실행
- 환경 확인 없이 `pip install` 실행
