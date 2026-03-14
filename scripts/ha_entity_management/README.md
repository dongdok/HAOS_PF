# Home Assistant Entity Management Scripts

이 폴더는 Home Assistant의 중복된 기기(주로 Tuya direct vs SmartThings 연동)들을 브라우저 조작 없이 API를 통해 일괄 분석하고 구조적으로 제어하기 위해 작성된 파이썬 스크립트 모음입니다.

## 📂 파일 구성 및 역할

1. **`analyze_ha_entities.py`**
   - HA REST API (`/api/states`)에 접속하여 현재 전체 엔티티 목록을 가져옵니다.
   - `_2`, `_3` 등의 접미사가 붙은 가상 중복 기기들을 1차적으로 필터링하여 `ha_entities_dump.json`으로 저장합니다.

2. **`analyze_duplicates.py`**
   - 위에서 추출한 덤프 데이터를 기반으로 원본 기기(Base ID)와 파생된 중복 기기들을 그룹핑하고 매핑합니다.
   - 분석된 최종 타겟 리스트를 `targets_to_disable.json`으로 출력합니다.

3. **`verify_redundancy.py`**
   - 리포팅용 스크립트로, 원본 엔티티와 중복 엔티티 간의 상태(State) 값과 이름을 비교하여 동일한 물리적 기기인지 안전성을 검증합니다.

4. **`disable_entities.py`**
   - HA WebSocket API (`config/entity_registry/update`)를 사용하여 `targets_to_disable.json`에 명시된 33개의 기기들을 레지스트리 단에서 영구적으로 "비활성화(Disable)" 처리합니다.

5. **`move_entities_to_raw.py`**
   - HA WebSocket API를 사용하여 비활성화된 기기들을 특정 구역(Area)인 `[RAW] 중복/미사용`(ID: `raw_jungbog_misayong`)으로 일괄 이동시켜 UI 및 시스템 구조를 통합 정리합니다.

## 🚀 사용 요건
- 루트 폴더의 `.env` 파일에 발급받은 `HA_TOKEN`과 `HA_URL`이 기입되어 있어야 합니다.
- `websockets`, `requests`, `python-dotenv` 라이브러리가 설치되어 있어야 합니다.
