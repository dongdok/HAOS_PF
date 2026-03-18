# HAOS_Control

Home Assistant OS 기반 로컬 우선 스마트홈 운영/자동화/추천 엔진 프로젝트입니다.  
핵심 목표는 “기기 제어”가 아니라 **운영 가능한 아키텍처 + 정량 데이터 기반 개선**입니다.

---

## 프로젝트 핵심

- LocalTuya, Zigbee2MQTT, MQTT, SmartThings 혼합 통합
- 캐노니컬 엔티티 표준화 및 재등록 복구 절차 운영
- 로그/추천/KPI를 SQLite로 수집하는 추천 엔진 구축
- 대시보드(운영/분석)와 자동화(실행)를 분리한 구조

---

## 현재 스냅샷 (2026-03-19 기준)

- 이벤트 로그: **6,057건**
- 액션 분포: 자동화 **1,423건**, 수동 **216건**, 시스템 **4,418건**
- 결과: 성공 **6,054건**, 취소 **3건**, 실패 **0건**
- 추천 후보: **50건** (`proposed 45 / rejected 3 / rolled_back 2`)
- 충돌 피드백: **6건** (`intended 5 / unintended 1`)

상세 수치 문서:  
- [/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_metrics_snapshot_v1.md](/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_metrics_snapshot_v1.md)

---

## 문서 바로가기

### 포트폴리오 핵심 문서
- [/Users/dy/Desktop/HAOS_Control/docs/portfolio_documentation_v1.md](/Users/dy/Desktop/HAOS_Control/docs/portfolio_documentation_v1.md)
- [/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_data_v1.md](/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_data_v1.md)
- [/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_data_v2.md](/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_data_v2.md)
- [/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_data_v3.md](/Users/dy/Desktop/HAOS_Control/docs/portfolio_live_data_v3.md)
- [/Users/dy/Desktop/HAOS_Control/docs/portfolio_onepage_self_intro_v1.md](/Users/dy/Desktop/HAOS_Control/docs/portfolio_onepage_self_intro_v1.md)

### 운영 기준 문서
- [/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md](/Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md)
- [/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md](/Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md)
- [/Users/dy/Desktop/HAOS_Control/docs/standardization_v1_complete.md](/Users/dy/Desktop/HAOS_Control/docs/standardization_v1_complete.md)
- [/Users/dy/Desktop/HAOS_Control/docs/automation_standard_v1.md](/Users/dy/Desktop/HAOS_Control/docs/automation_standard_v1.md)

---

## 코드 구조

```text
src/reco_engine/
  core/        # 도메인 규칙, 정책, 스코어링, 엔티티 모델
  adapters/    # HA API, SQLite 저장소
  services/    # 수집/탐지/제안/피드백/KPI/대시보드 서비스
  interfaces/  # CLI 엔트리포인트

scripts/
  rooms/       # 방 단위 엔티티/대시보드 복구 스크립트
  ha_entity_management/
  portfolio/   # 포트폴리오 지표 추출 스크립트
```

---

## 빠른 실행

### 1) Python 환경
환경 가이드:  
- [/Users/dy/Desktop/HAOS_Control/docs/python_environment_guide_v1.md](/Users/dy/Desktop/HAOS_Control/docs/python_environment_guide_v1.md)

### 2) 추천 엔진 초기화
```bash
cd /Users/dy/Desktop/HAOS_Control
source .venv/bin/activate
reco-engine init-db --db data/reco_engine.db
```

### 3) 포트폴리오 스냅샷 갱신
```bash
cd /Users/dy/Desktop/HAOS_Control
python3 scripts/portfolio/export_portfolio_snapshot.py
```

---

## 설계 원칙

- 캐노니컬 엔티티를 단일 운영 진실 소스로 사용
- `unknown/unavailable`를 임시값으로 덮지 않고 실패를 명시 기록
- 자동화 추천은 즉시 적용하지 않고 제안-승인-테스트-롤백 절차 준수
- UI/자동화/스크립트를 분리해 유지보수성과 확장성 확보
