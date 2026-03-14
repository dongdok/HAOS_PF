# Automation Agent Prompt Template

Use this prompt when asking any agent to work on automations in this repository.

```text
이 프로젝트에서 자동화 작업을 시작하기 전에 반드시 아래 문서들을 읽고 현재 기준을 먼저 파악해:

1. /Users/dy/Desktop/HAOS_Control/docs/standardization_v1_complete.md
2. /Users/dy/Desktop/HAOS_Control/docs/current_operating_map.md
3. /Users/dy/Desktop/HAOS_Control/docs/master_hardware_map_live.md
4. /Users/dy/Desktop/HAOS_Control/docs/naming_standard_v1.md
5. /Users/dy/Desktop/HAOS_Control/docs/device_onboarding_rules_v1.md
6. /Users/dy/Desktop/HAOS_Control/docs/automation_standard_v1.md
7. /Users/dy/Desktop/HAOS_Control/docs/automation_agent_contract_v1.md

방별 작업이면 해당 방 문서도 읽어:
- /Users/dy/Desktop/HAOS_Control/docs/standardization_plan_anbang_v1.md
- /Users/dy/Desktop/HAOS_Control/docs/standardization_plan_geosil_v1.md
- /Users/dy/Desktop/HAOS_Control/docs/standardization_plan_jubang_v1.md
- /Users/dy/Desktop/HAOS_Control/docs/standardization_plan_osbang_v1.md
- /Users/dy/Desktop/HAOS_Control/docs/standardization_plan_hwajangsil_v1.md
- /Users/dy/Desktop/HAOS_Control/docs/standardization_plan_hyeongwan_v1.md

중요 규칙:
- archived 문서와 백업 파일은 참고만 하고 truth source로 쓰지 마.
- 자동화는 canonical entity id만 사용해.
- alias는 `[분류] [영역] [행동] ([기준])` 형식을 지켜.
- YAML 구조는 `alias -> description -> mode -> trigger -> condition -> action` 순서를 지켜.
- SmartThings나 다른 외부 루틴을 대체할 때는 HA 자동화를 먼저 검증한 후 기존 루틴을 끄는 순서로 가.

실제 구현 전 먼저 짧게 정리해:
1. 이번 자동화에 사용할 canonical entity id
2. 왜 그 id가 맞는지
3. 자동화 alias와 category
4. 테스트 방법

그 다음에만 자동화 설계 또는 구현을 진행해.
```
