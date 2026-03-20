# YAML 샘플 (공개용)

이 폴더는 포트폴리오 검토자가 "문서"뿐 아니라 "구현 스타일"도 확인할 수 있도록 만든 공개 샘플입니다.

원칙:
- 실운영 원본을 그대로 올리지 않고, 민감정보를 제거한 구조 중심 샘플만 공개
- 엔티티명/IP/MAC/토큰은 예시값 또는 마스킹 값 사용
- 각 샘플은 네트워크 운영 관점(중복명령 방지, 오프라인 감시, 경로 분리)을 포함

## 파일 설명

1. `automation_living_night_off.yaml`
- 밤 시간 거실 소등 자동화 기본형 (조건 중심)

2. `automation_bathroom_presence_vent.yaml`
- 재실 기반 조명 + 체류 기반 환풍 분기

3. `automation_command_dedup_guard.yaml`
- 이미 ON/OFF 상태면 명령 전송을 스킵해 네트워크 부하 감소

4. `automation_device_offline_alert.yaml`
- Zigbee/Wi-Fi 핵심 기기 오프라인 상태 감지 알림

5. `automation_return_tv_wol.yaml`
- 복귀 시나리오에서 명시적 WOL로 TV 기동

## 적용 시 주의

- 실제 운영 적용 전 반드시 엔티티 ID를 본인 환경에 맞게 교체
- 알림 채널(`notify.mobile_app_*`)과 네트워크 정보는 환경별 수정 필요
- HA UI에서 트레이스 확인 후 운영 반영 권장
