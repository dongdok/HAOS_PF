# HAOS 포트폴리오 보강 권장안 v1

> 작성일: 2026-03-19 (Asia/Seoul)  
> 대상 문서:  
> - `portfolio_documentation_v1.md`  
> - `portfolio_live_data_v1.md`  
> - `portfolio_live_data_v2.md`  
> - `portfolio_live_data_v3.md`  
> - `python_environment_guide_v1.md`

---

## 1. 현재 문서의 강점

- 시스템 범위(인프라/자동화/프로토콜/UI)가 이미 넓고, 기술 키워드가 풍부함
- 로컬 우선 전환(Local-First), 표준 엔티티 정리, 추천 엔진 설계 의도가 명확함
- 하드웨어 맵/운영 맵/표준화 문서와 연결되어 추적성이 좋음

---

## 2. 보강이 필요한 핵심 포인트

### A. 숫자로 증명하는 성과 섹션 추가

현재 문서는 설명은 강하지만, 심사자 입장에서 한눈에 보는 “성과 숫자”가 상대적으로 약함.
아래 항목을 1페이지 요약 블록으로 추가 권장:

1. 운영 로그 총량
2. 자동화/수동/시스템 이벤트 분포
3. 추천 후보 생성/거절/롤백 분포
4. 충돌 피드백(의도됨/비의도됨) 분포
5. 최근 KPI(수동 조작 수, 자동화 취소율, 월 전력)

### B. 장애 복구 사례(Incident) 섹션 추가

포트폴리오 평가에서 강력한 요소:

1. 증상
2. 원인
3. 조치
4. 재발방지
5. 결과

권장 사례:
- Zigbee 채널 이동 후 재페어링 + canonical ID 복구
- IEEE 기반 엔티티명 드리프트 복구
- SmartThings TV/WOL 경고 대응 및 경로 전환

### C. 운영 원칙(Guardrails) 섹션 명시

현재 대화/실운영에서 이미 적용한 규칙을 문서화하면 신뢰도가 올라감:

1. `unknown/unavailable` 상태는 fallback 없이 명시적 실패로 기록
2. 재등록 시 디바이스명 + 엔티티명 + 자동화 참조를 한 번에 복구
3. 캐노니컬 ID를 단일 운영 진실 소스로 사용

### D. 산출물 링크 매트릭스 추가

문서가 많아진 상태라 심사자가 길을 잃기 쉬움.  
“무엇을 보면 어떤 역량을 확인할 수 있는지” 매트릭스 추가 권장:

- 아키텍처 역량: `docs/architecture/...`
- 운영 안정성: `docs/current_operating_map.md`
- 표준화 역량: `docs/standardization_v1_complete.md`
- 코드 구현: `src/reco_engine/...`
- 실운영 자동화: HA 자동화 UI 캡처/엔티티 맵

### E. python 환경 가이드 강화

`python_environment_guide_v1.md`에 아래 3개 보강 권장:

1. 재현 명령(설치 → 실행 → 검증) 섹션
2. 의존성 잠금 규칙(버전 고정 원칙)
3. 트러블슈팅 3건(venv 오염, 잘못된 pip 대상, token/env 누락)

---

## 3. 자동 추출로 보강 가능한 데이터

아래 스크립트가 추가됨:

- `scripts/portfolio/export_portfolio_snapshot.py`

이 스크립트는 다음을 자동 수집해 Markdown으로 출력:

1. `event_log` 총량/분포
2. `recommendation_candidate` 상태 분포
3. `conflict_feedback` 분포
4. `kpi_snapshot` 최신값
5. `lovelace_active.json` 기준 뷰/섹션/카드 수
6. `dashboard_cards.json` 운영 카드 타이틀

실행 예시:

```bash
cd /Users/dy/Desktop/HAOS_Control
python3 scripts/portfolio/export_portfolio_snapshot.py
```

출력 파일:

- `docs/portfolio_live_metrics_snapshot_v1.md`

---

## 4. 포트폴리오 문서에 바로 반영할 추천 구조

### 섹션 0: Executive Summary (신규)
- “문제 → 해결 → 결과” 6~8줄 요약

### 섹션 1: 시스템 범위
- 현재 `portfolio_documentation_v1.md` 내용 유지

### 섹션 2: 운영 성과 지표 (신규)
- 스냅샷 파일의 숫자 인용

### 섹션 3: 대표 장애 3건 (신규)
- 원인-조치-결과 템플릿

### 섹션 4: 아키텍처 설계 판단
- 왜 SmartThings/LocalTuya/Zigbee/MQTT를 혼합했는지 판단 기준

### 섹션 5: 확장 계획
- ML 추천 레이어(행동/환경/출입 패턴) 고도화 계획

---

## 5. 작성 시 주의(중요)

1. “가능하다/할 수 있다”보다 “실제 수치” 중심으로 기술
2. 운영 중인 canonical entity만 명시
3. 임시/보정 수치 대신 실제 로그 기반 수치만 기재
4. 날짜/기준시각(Asia/Seoul) 반드시 명시

