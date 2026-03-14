## 로직 변경 매핑 시뮬레이션 (Dry Run)

| 기기 및 엔티티 | 기존 영역 | 기존 이름 | ➡️ | 제안 영역 | 제안 이름 | 제안 엔티티 ID |
|---|---|---|---|---|---|---|
| **기기** | 센서 | Zemismart M1 Hub | ➡️ | **미분류** | **Zemismart M Hub** | - |
| ↳ 엔티티 | 센서 | 문제 | ➡️ | 미분류 | 문제 | binary_sensor.zemismart_m1_hub_problem |
| **기기** | 센서 | 옷방 재실센서  | ➡️ | **옷방** | **옷방 재실 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 옷방 | 옷방 재실감지 | binary_sensor.osbang_jaesilsenseo_occupancy |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 옷방 | 옷방 감도 | number.osbang_jaesilsenseo_sensitivity |
| ↳ 엔티티 | 센서 | 근거리 감지 | ➡️ | 옷방 | 옷방 근거리 감지 | number.osbang_jaesilsenseo_near_detection |
| ↳ 엔티티 | 센서 | 원거리 감지 | ➡️ | 옷방 | 옷방 원거리 감지 | number.osbang_jaesilsenseo_far_detection |
| ↳ 엔티티 | 센서 | Closest target distance | ➡️ | 옷방 | 옷방 Closest target distance | number.osbang_jaesilsenseo_closest_target_distance |
| **기기** | 센서 | 거실 재실센서 | ➡️ | **거실** | **거실 재실 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 거실 | 거실 재실감지 | binary_sensor.geosil_jaesilsenseo_occupancy |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 거실 | 거실 감도 | number.geosil_jaesilsenseo_sensitivity |
| ↳ 엔티티 | 센서 | 근거리 감지 | ➡️ | 거실 | 거실 근거리 감지 | number.geosil_jaesilsenseo_near_detection |
| ↳ 엔티티 | 센서 | 원거리 감지 | ➡️ | 거실 | 거실 원거리 감지 | number.geosil_jaesilsenseo_far_detection |
| ↳ 엔티티 | 센서 | Closest target distance | ➡️ | 거실 | 거실 Closest target distance | number.geosil_jaesilsenseo_closest_target_distance |
| **기기** | 센서 | 화장실 재실센서 | ➡️ | **화장실** | **화장실 재실 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 화장실 | 화장실 재실감지 | binary_sensor.hwajangsil_jaesilsenseo_occupancy |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 화장실 | 화장실 감도 | number.hwajangsil_jaesilsenseo_sensitivity |
| ↳ 엔티티 | 센서 | 근거리 감지 | ➡️ | 화장실 | 화장실 근거리 감지 | number.hwajangsil_jaesilsenseo_near_detection |
| ↳ 엔티티 | 센서 | 원거리 감지 | ➡️ | 화장실 | 화장실 원거리 감지 | number.hwajangsil_jaesilsenseo_far_detection |
| ↳ 엔티티 | 센서 | Closest target distance | ➡️ | 화장실 | 화장실 Closest target distance | number.hwajangsil_jaesilsenseo_closest_target_distance |
| **기기** | 센서 | 화장실 도어센서 | ➡️ | **화장실** | **화장실 도어 센서** | - |
| ↳ 엔티티 | 센서 | 문 | ➡️ | 화장실 | 화장실 문 | binary_sensor.hwajangsil_doeosenseo_door |
| ↳ 엔티티 | 센서 | 배터리 | ➡️ | 화장실 | 화장실 배터리 | sensor.hwajangsil_doeosenseo_battery |
| **기기** | 센서 | 안방 온습도센서 | ➡️ | **안방** | **안방 온습도 센서** | - |
| ↳ 엔티티 | 센서 | 온도 | ➡️ | 안방 | 안방 온도 | sensor.anbang_onseubdosenseo_temperature |
| ↳ 엔티티 | 센서 | 습도 | ➡️ | 안방 | 안방 습도 | sensor.anbang_onseubdosenseo_humidity |
| ↳ 엔티티 | 센서 | 배터리 | ➡️ | 안방 | 안방 배터리 | sensor.anbang_onseubdosenseo_battery |
| **기기** | 가상 | 외출 가상스위치 | ➡️ | **[가상] 헬퍼** | **[가상] 외출 스위치** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | [가상] 헬퍼 | [가상] 전원 켜기 동작 | select.oecul_gasangseuwici_power_on_behavior |
| ↳ 엔티티 | 가상 | 표시등 모드 | ➡️ | [가상] 헬퍼 | [가상] 표시등 모드 | select.oecul_gasangseuwici_indicator_light_mode |
| ↳ 엔티티 | 가상 | 전류 | ➡️ | [가상] 헬퍼 | [가상] 전류 | sensor.oecul_gasangseuwici_current |
| ↳ 엔티티 | 가상 | 전력 | ➡️ | [가상] 헬퍼 | [가상] 전력 | sensor.oecul_gasangseuwici_power |
| ↳ 엔티티 | 가상 | 전압 | ➡️ | [가상] 헬퍼 | [가상] 전압 | sensor.oecul_gasangseuwici_voltage |
| ↳ 엔티티 | 가상 | 총 에너지 | ➡️ | [가상] 헬퍼 | [가상] 총 에너지 | sensor.oecul_gasangseuwici_total_energy |
| ↳ 엔티티 | 가상 | 차일드 락 | ➡️ | [가상] 헬퍼 | [가상] 차일드 락 | switch.oecul_gasangseuwici_child_lock |
| ↳ 엔티티 | 가상 | Socket 1 | ➡️ | [가상] 헬퍼 | [가상] Socket | switch.oecul_gasangseuwici_socket_1 |
| **기기** | 가상 | 외출 가상스위치2 | ➡️ | **[가상] 헬퍼** | **[가상] 외출 스위치** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | [가상] 헬퍼 | [가상] 전원 켜기 동작 | select.oecul_gasangseuwici2_power_on_behavior |
| ↳ 엔티티 | 가상 | 전류 | ➡️ | [가상] 헬퍼 | [가상] 전류 | sensor.oecul_gasangseuwici2_current |
| ↳ 엔티티 | 가상 | 전력 | ➡️ | [가상] 헬퍼 | [가상] 전력 | sensor.oecul_gasangseuwici2_power |
| ↳ 엔티티 | 가상 | 전압 | ➡️ | [가상] 헬퍼 | [가상] 전압 | sensor.oecul_gasangseuwici2_voltage |
| ↳ 엔티티 | 가상 | 총 에너지 | ➡️ | [가상] 헬퍼 | [가상] 총 에너지 | sensor.oecul_gasangseuwici2_total_energy |
| ↳ 엔티티 | 가상 | Socket 1 | ➡️ | [가상] 헬퍼 | [가상] Socket | switch.oecul_gasangseuwici2_socket_1 |
| **기기** | 센서 | 긴 진동센서 | ➡️ | **미분류** | **긴 진동 센서** | - |
| ↳ 엔티티 | 센서 | 진동 | ➡️ | 미분류 | 진동 | binary_sensor.gin_jindongsenseo_vibration |
| ↳ 엔티티 | 센서 | 드롭 | ➡️ | 미분류 | 드롭 | binary_sensor.gin_jindongsenseo_drop |
| ↳ 엔티티 | 센서 | 기울기 | ➡️ | 미분류 | 기울기 | binary_sensor.gin_jindongsenseo_tilt |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 미분류 | 감도 | number.gin_jindongsenseo_sensitivity |
| ↳ 엔티티 | 센서 | 배터리 | ➡️ | 미분류 | 배터리 | sensor.gin_jindongsenseo_battery |
| ↳ 엔티티 | 센서 | 배터리 상태 | ➡️ | 미분류 | 배터리 상태 | sensor.gin_jindongsenseo_battery_state |
| **기기** | 센서 | 원 진동센서 | ➡️ | **미분류** | **원 진동 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 미분류 | 재실감지 | binary_sensor.weon_jindongsenseo_occupancy |
| **기기** | 센서 | 안방 재실센서 | ➡️ | **안방** | **안방 재실 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 안방 | 안방 재실감지 | binary_sensor.anbang_jaesilsenseo_occupancy |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 안방 | 안방 감도 | number.anbang_jaesilsenseo_sensitivity |
| ↳ 엔티티 | 센서 | 근거리 감지 | ➡️ | 안방 | 안방 근거리 감지 | number.anbang_jaesilsenseo_near_detection |
| ↳ 엔티티 | 센서 | 원거리 감지 | ➡️ | 안방 | 안방 원거리 감지 | number.anbang_jaesilsenseo_far_detection |
| ↳ 엔티티 | 센서 | Closest target distance | ➡️ | 안방 | 안방 Closest target distance | number.anbang_jaesilsenseo_closest_target_distance |
| **기기** | 가상 | 침대 누울때 가상스위치 | ➡️ | **안방** | **안방 침대 누울때 가상스위치** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | 안방 | 안방 전원 켜기 동작 | select.cimdae_nuulddae_gasangseuwici_power_on_behavior |
| ↳ 엔티티 | 가상 | 표시등 모드 | ➡️ | 안방 | 안방 표시등 모드 | select.cimdae_nuulddae_gasangseuwici_indicator_light_mode |
| ↳ 엔티티 | 가상 | 전류 | ➡️ | 안방 | 안방 전류 | sensor.cimdae_nuulddae_gasangseuwici_current |
| ↳ 엔티티 | 가상 | 전력 | ➡️ | 안방 | 안방 전력 | sensor.cimdae_nuulddae_gasangseuwici_power |
| ↳ 엔티티 | 가상 | 전압 | ➡️ | 안방 | 안방 전압 | sensor.cimdae_nuulddae_gasangseuwici_voltage |
| ↳ 엔티티 | 가상 | 총 에너지 | ➡️ | 안방 | 안방 총 에너지 | sensor.cimdae_nuulddae_gasangseuwici_total_energy |
| ↳ 엔티티 | 가상 | Socket 1 | ➡️ | 안방 | 안방 Socket | switch.cimdae_nuulddae_gasangseuwici_socket_1 |
| **기기** | 가상 | 굿나잇 가상스위치  | ➡️ | **[가상] 헬퍼** | **[가상] 굿나잇 스위치** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | [가상] 헬퍼 | [가상] 전원 켜기 동작 | select.gusnais_gasangseuwici_power_on_behavior |
| ↳ 엔티티 | 가상 | 표시등 모드 | ➡️ | [가상] 헬퍼 | [가상] 표시등 모드 | select.gusnais_gasangseuwici_indicator_light_mode |
| ↳ 엔티티 | 가상 | 전류 | ➡️ | [가상] 헬퍼 | [가상] 전류 | sensor.gusnais_gasangseuwici_current |
| ↳ 엔티티 | 가상 | 전력 | ➡️ | [가상] 헬퍼 | [가상] 전력 | sensor.gusnais_gasangseuwici_power |
| ↳ 엔티티 | 가상 | 전압 | ➡️ | [가상] 헬퍼 | [가상] 전압 | sensor.gusnais_gasangseuwici_voltage |
| ↳ 엔티티 | 가상 | 총 에너지 | ➡️ | [가상] 헬퍼 | [가상] 총 에너지 | sensor.gusnais_gasangseuwici_total_energy |
| ↳ 엔티티 | 가상 | 차일드 락 | ➡️ | [가상] 헬퍼 | [가상] 차일드 락 | switch.gusnais_gasangseuwici_child_lock |
| ↳ 엔티티 | 가상 | Socket 1 | ➡️ | [가상] 헬퍼 | [가상] Socket | switch.gusnais_gasangseuwici_socket_1 |
| **기기** | 가상 | 일단가상 2구  | ➡️ | **[가상] 헬퍼** | **[가상] 가상 구** | - |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang_2gu_switch_1 |
| ↳ 엔티티 | 가상 | Switch 2 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang_2gu_switch_2 |
| **기기** | 가상 | 테라스 가상스위치 | ➡️ | **거실** | **거실 테라스 가상스위치** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | 거실 | 거실 전원 켜기 동작 | select.teraseu_gasangseuwici_power_on_behavior |
| ↳ 엔티티 | 가상 | 표시등 모드 | ➡️ | 거실 | 거실 표시등 모드 | select.teraseu_gasangseuwici_indicator_light_mode |
| ↳ 엔티티 | 가상 | 차일드 락 | ➡️ | 거실 | 거실 차일드 락 | switch.teraseu_gasangseuwici_child_lock |
| ↳ 엔티티 | 가상 | Socket 1 | ➡️ | 거실 | 거실 Socket | switch.teraseu_gasangseuwici_socket_1 |
| **기기** | 가상 | 일단가상4구 | ➡️ | **[가상] 헬퍼** | **[가상] 가상구** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | [가상] 헬퍼 | [가상] 전원 켜기 동작 | select.ildangasang4gu_power_on_behavior |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang4gu_switch_1 |
| ↳ 엔티티 | 가상 | Switch 4 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang4gu_switch_4 |
| **기기** | 가상 | 일단 가상4구 2 | ➡️ | **[가상] 헬퍼** | **[가상] 일단 가상구** | - |
| ↳ 엔티티 | 가상 | 전원 켜기 동작 | ➡️ | [가상] 헬퍼 | [가상] 전원 켜기 동작 | select.ildan_gasang4gu_2_power_on_behavior |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildan_gasang4gu_2_switch_1 |
| ↳ 엔티티 | 가상 | Switch 4 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildan_gasang4gu_2_switch_4 |
| **기기** | 가상 | 일단가상 3구  | ➡️ | **[가상] 헬퍼** | **[가상] 가상 구** | - |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang_3gu_switch_1 |
| **기기** | 가상 | 일단가상 4구 3 | ➡️ | **[가상] 헬퍼** | **[가상] 가상 구** | - |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang_4gu_3_switch_1 |
| ↳ 엔티티 | 가상 | Switch 4 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang_4gu_3_switch_4 |
| **기기** | 가상 | 일단가상2구 4 | ➡️ | **[가상] 헬퍼** | **[가상] 가상구** | - |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang2gu_4_switch_1 |
| ↳ 엔티티 | 가상 | Switch 2 | ➡️ | [가상] 헬퍼 | [가상] Switch | switch.ildangasang2gu_4_switch_2 |
| **기기** | 가상 | 거실창문 가상스위치 | ➡️ | **거실** | **거실창문 가상스위치** | - |
| ↳ 엔티티 | 가상 | Switch 1 | ➡️ | 거실 | 거실 Switch | switch.geosilcangmun_gasangseuwici_switch_1 |
| **기기** | 센서 | 현관도어센서 | ➡️ | **현관** | **현관도어 센서** | - |
| ↳ 엔티티 | 센서 | 문 | ➡️ | 현관 | 현관 문 | binary_sensor.hyeongwandoeosenseo_door |
| ↳ 엔티티 | 센서 | Tamper | ➡️ | 현관 | 현관 Tamper | binary_sensor.hyeongwandoeosenseo_tamper |
| ↳ 엔티티 | 센서 | 배터리 | ➡️ | 현관 | 현관 배터리 | sensor.hyeongwandoeosenseo_battery |
| **기기** | 센서 | 옷방 온습도센서 | ➡️ | **옷방** | **옷방 온습도 센서** | - |
| ↳ 엔티티 | 센서 | 온도 | ➡️ | 옷방 | 옷방 온도 | sensor.osbang_onseubdosenseo_temperature |
| ↳ 엔티티 | 센서 | 습도 | ➡️ | 옷방 | 옷방 습도 | sensor.osbang_onseubdosenseo_humidity |
| ↳ 엔티티 | 센서 | 배터리 상태 | ➡️ | 옷방 | 옷방 배터리 상태 | sensor.osbang_onseubdosenseo_battery_state |
| **기기** | 센서 | 테라스 도어센서 | ➡️ | **거실** | **거실 테라스 도어 센서** | - |
| ↳ 엔티티 | 센서 | 문 | ➡️ | 거실 | 거실 문 | binary_sensor.teraseu_doeosenseo_door |
| ↳ 엔티티 | 센서 | 배터리 | ➡️ | 거실 | 거실 배터리 | sensor.teraseu_doeosenseo_battery |
| **기기** | 센서 | 머리맡 재실센서 | ➡️ | **미분류** | **머리맡 재실 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 미분류 | 재실감지 | binary_sensor.meorimat_jaesilsenseo_occupancy |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 미분류 | 감도 | number.meorimat_jaesilsenseo_sensitivity |
| ↳ 엔티티 | 센서 | 근거리 감지 | ➡️ | 미분류 | 근거리 감지 | number.meorimat_jaesilsenseo_near_detection |
| ↳ 엔티티 | 센서 | 원거리 감지 | ➡️ | 미분류 | 원거리 감지 | number.meorimat_jaesilsenseo_far_detection |
| ↳ 엔티티 | 센서 | Closest target distance | ➡️ | 미분류 | Closest target distance | number.meorimat_jaesilsenseo_closest_target_distance |
| **기기** | 센서 | 주방 재실 센서 | ➡️ | **주방** | **주방 재실 센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 주방 | 주방 재실감지 | binary_sensor.jubang_jaesil_senseo_occupancy |
| ↳ 엔티티 | 센서 | 감도 | ➡️ | 주방 | 주방 감도 | number.jubang_jaesil_senseo_sensitivity |
| ↳ 엔티티 | 센서 | 근거리 감지 | ➡️ | 주방 | 주방 근거리 감지 | number.jubang_jaesil_senseo_near_detection |
| ↳ 엔티티 | 센서 | 원거리 감지 | ➡️ | 주방 | 주방 원거리 감지 | number.jubang_jaesil_senseo_far_detection |
| ↳ 엔티티 | 센서 | Closest target distance | ➡️ | 주방 | 주방 Closest target distance | number.jubang_jaesil_senseo_closest_target_distance |
| **기기** | 센서 | 안방 의자센서 | ➡️ | **안방** | **안방 의자센서** | - |
| ↳ 엔티티 | 센서 | 재실감지 | ➡️ | 안방 | 안방 재실감지 | binary_sensor.anbang_yijasenseo_occupancy |
| **기기** | 센서 | 거실 창문센서 | ➡️ | **거실** | **거실 창문 센서** | - |
| ↳ 엔티티 | 센서 | 문 | ➡️ | 거실 | 거실 문 | binary_sensor.geosil_cangmunsenseo_door |
| ↳ 엔티티 | 센서 | 배터리 | ➡️ | 거실 | 거실 배터리 | sensor.geosil_cangmunsenseo_battery |
| **기기** | 거실 | Hub - 43" Smart Monitor M7 | ➡️ | **거실** | **거실 Hub - " Smart Monitor M7** | - |
| **기기** | 가상 | 가상스위치 생성 | ➡️ | **[가상] 헬퍼** | **[가상] 스위치 생성** | - |
