# iOS Shortcuts Inventory v1

Last updated: 2026-03-10
Status: collecting iPhone Shortcuts routines separately from SmartThings/Tuya automations

## Purpose

This document tracks iPhone Shortcuts-based routines.

It is intentionally separate from:

- `docs/automation_external_inventory_v1.md` (SmartThings/Tuya source automations)

## Shortcut S001

- Shortcut name:
  - `굿모닝`
- Source type:
  - iPhone Shortcuts
- Intent:
  - Morning multi-action routine that sequentially executes multiple prebuilt actions/scenes and media playback.

### S001-A: 실행 액션 순서 (visible in provided captures)

1. `히터 꺼` 실행
2. `환풍기 켜` 실행
3. `커튼 열어` 실행
4. `안방조명 켜` 실행
5. `Too dark` 실행
6. `안방불 켜` 실행
7. `전기장판 꺼` 실행
8. `TV 켜줘` 실행
9. `커튼불 켜` 실행
10. `조명 켜 1` 실행
11. `Songbird (Korean Ver.)` 재생 실행

## Mapping Notes

- Current captures show action labels and order, but not each action's underlying Home Assistant service/entity mapping.
- During HA migration, each action label should be mapped to canonical live entity IDs or scripts/scenes.

## Shortcut Sub-routines (Bedroom Stand Light)

- `Too dark`
  - Role: 안방 스탠드 조명 밝게 전환
  - Target: 안방 스탠드 조명
  - Action profile:
    - 밝기 `100%`
    - 색온도 `태양 기반`
  - Visual note from user capture:
    - 내부 호출: `안방조명 100퍼`

- `Too bright`
  - Role: 안방 스탠드 조명 취침 밝기 전환
  - Target: 안방 스탠드 조명
  - Action profile:
    - 밝기 `1%`
    - 색온도 `2000K`
  - Visual note from user capture:
    - 내부 호출: `안방조명1퍼`

## iOS Automation Tab (Personal Automation)

- This section tracks items from the iPhone Shortcuts app `자동화` tab.
- Time conditions are user-configurable and may change.

## Shortcut S002

- Shortcut name:
  - `굿나잇`
- Source type:
  - iPhone Shortcuts
- Intent:
  - Night routine for turning off bedroom lighting.

### S002-A: 실행 액션 순서 (visible in provided capture)

1. `침대불 꺼`
2. `안방조명 꺼` 실행

## Shortcut S003

- Shortcut name:
  - `잘 준비해줘`
- Source type:
  - iPhone Shortcuts
- Intent:
  - Bedtime preparation routine with bedroom environment setup.

### S003-A: 실행 액션 순서 (visible in provided capture)

1. `재생 대상 설정: iPhone`
2. `커튼 닫아` 실행
3. `전기장판 켜` 실행
4. `Too bright` 실행
5. `침대불 켜` 실행
6. `안방불 꺼` 실행

## Automation A001

- Automation type:
  - iPhone Shortcuts app `자동화` tab (개인용 자동화)
- Trigger:
  - `매일 오후 4:06` (user-settable time)
  - Run mode: `즉시 실행`
  - Notify when run: `OFF`
- Action:
  1. `미디어 음량 80%로 설정`
  2. `굿모닝` 단축어 실행

### A001 Note

- User stated the time is not fixed and can be adjusted.
- Core intent is: `지정 시간에 굿모닝 실행` (with optional pre-volume step).

## Automation A002

- Automation type:
  - iPhone Shortcuts app `자동화` tab (개인용 자동화)
- Trigger:
  - `iPhone동동이`가 Wi-Fi `SK_AA9E_2.4G`에 연결될 때
  - Run mode: `즉시 실행`
- Action:
  1. `스피커 연결` 단축어 실행
  2. `미디어 음량 26%로 설정`
  3. `Wi‑Fi 연결 후 음악 실행` 단축어 실행

### A002 Note

- User described this as arrival/home-return iPhone automation.

## Automation A003

- Automation type:
  - iPhone Shortcuts app `자동화` tab (개인용 자동화)
- Trigger:
  - `iPhone동동이`가 Wi-Fi `SK_AA9E_2.4G`에서 연결 해제될 때
  - Run mode: `즉시 실행`
- Action:
  1. `wifi 해지시 날짜 저장` 단축어 실행
  2. `외출 가상스위치 on` 단축어 실행
  3. `카카오버스` 앱 열기

### A003 Note

- User described this as leave-home iPhone automation.
