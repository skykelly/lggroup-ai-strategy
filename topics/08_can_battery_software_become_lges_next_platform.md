---
id: topic_can_battery_software_become_lges_next_platform
type: topic
title: "배터리 SW는 셀을 플랫폼으로 바꿀 수 있다"
subtitle: "BMS·BMTS·SDVerse로 보는 LG에너지솔루션의 다음 경쟁 레이어"
status: reviewed
updated: 2026-06-21
priority: P2
priority_score: 3.12
priority_updated: 2026-06-22
priority_model: recency_issue_v1
priority_factors:
  recency: 4.20
  issue_salience: 2.60
  strategic_impact: 2.75
  urgency: 2.22
  actionability: 3.23
priority_rationale: "최신성 4.2, 이슈성 2.6이 우선순위를 주도한다. 강점 요소는 최신성·실행 가능성이며, 최신 기준일 2026-06-21, 최근 180일 Source 비율 33%."
question: "배터리 SW는 LG에너지솔루션의 다음 플랫폼이 될 수 있는가?"
short_answer: "배터리 SW는 셀 사업의 부가 기능에 그치지 않을 수 있다. SDV 시대에는 배터리 상태, 수명, 안전, 열화, 충전 행동이 차량 software가 이해해야 할 핵심 데이터가 된다. LG에너지솔루션이 BMS를 BMTS와 SDVerse로 확장하는 흐름은 배터리를 hardware component에서 energy intelligence platform으로 바꾸려는 시도로 볼 수 있다."
topic_type:
  - strategic_question
  - technology_assessment
related_themes:
  - ai_mobility_sdv_aidv
  - global_ai_alliance_open_innovation
related_concepts:
  - bms-bmts
  - battery-software
  - sdv
  - aidv
  - on-device-ai
related_companies:
  - lg-energy-solution
  - qualcomm
  - sdverse
source_ids:
  - src_lgensol_baround
  - src_lgensol_sdverse_20260403
  - src_lgensol_qualcomm_20241223
  - src_lgensol_qualcomm_20240310
image_policy:
  use_original_source_images: true
  generate_new_images: false
  download_script: scripts/download_topic_08_images.py
  local_image_dir: assets/images
tags:
  - battery-software
  - bms
  - bmts
  - sdv
  - sdverse
  - qualcomm
---

# 배터리 SW는 셀을 플랫폼으로 바꿀 수 있다

> **Summary**  
> 배터리 사업의 중심은 오랫동안 셀의 성능, 원가, 수율, 공급 안정성이었다. 하지만 SDV 시대에는 배터리가 차량 software가 이해해야 할 데이터 자산이 된다. 배터리 상태, 수명, 안전성, 열화, 충전 습관은 차량의 주행 경험과 유지비, 잔존가치, 안전성에 직접 영향을 준다. LG에너지솔루션이 BMS를 BMTS, SDVerse, Qualcomm Snapdragon Digital Chassis와 연결하는 흐름은 배터리를 단순 부품에서 **energy intelligence platform**으로 확장하려는 신호다.

<figure>
  <img src="assets/images/lgensol_baround_core_values.png" alt="B.around는 배터리 생애주기 전반을 진단·관리·서비스로 확장하는 BMTS 관점을 보여준다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>B.around는 배터리 생애주기 전반을 진단·관리·서비스로 확장하는 BMTS 관점을 보여준다. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

## 1. Key Factors & Questions

### Key Factors

LG에너지솔루션은 B.around를 통해 BMTS, 즉 Battery Management Total Solution을 설명하고 있다. BMTS는 전통적인 BMS를 넘어 software, cloud, AI를 통합해 배터리 생애주기 전반의 안전하고 효율적인 관리를 제공하는 기술로 소개된다.

2026년 4월에는 배터리 기업 최초로 SDVerse에 참여했다. SDVerse는 automotive software B2B marketplace이며, LG에너지솔루션은 SDV 환경에 최적화된 5개 battery software solution을 제시했다. Battery Platform SW, Safety Diagnostic Calibration Tool, Onboard FRISM, Onboard BLiS, Onboard DASH가 여기에 포함된다.

Qualcomm과의 협력도 같은 흐름에 있다. LG에너지솔루션은 Snapdragon Digital Chassis에서 advanced BMS diagnostic solution을 사용할 수 있도록 하고, high-performance computing platform에서 배터리 알고리즘을 실시간으로 구동하는 방향을 제시했다.

### Questions

이 흐름에서 LG가 던져야 할 질문은 다음이다.

```text
1. 배터리 SW는 셀 판매를 보완하는 기능인가, 별도 플랫폼인가?
2. SDV 시대에 BMS는 차량 software architecture 안에서 어떤 위치를 차지하는가?
3. 배터리 데이터는 완성차, 보험, 중고차, 충전, fleet management와 연결될 수 있는가?
4. LG에너지솔루션은 배터리 제조사에서 energy intelligence company로 확장할 수 있는가?
```

## 2. BMS는 더 이상 숨은 제어기가 아니다

과거 BMS는 배터리 팩 안에서 상태를 모니터링하고 안전을 관리하는 제어 시스템에 가까웠다. 사용자는 BMS를 직접 경험하지 않았고, 완성차 업체 입장에서도 BMS는 배터리 패키지 안의 기능에 가까웠다.

하지만 SDV에서는 상황이 달라진다. 차량의 기능이 software로 정의되면, 배터리 상태도 차량 software가 이해해야 하는 정보가 된다. 주행 가능 거리, 충전 전략, 열관리, 안전 경고, 수명 예측, 잔존가치 모두 battery data와 연결된다.

<figure>
  <img src="assets/images/lgensol_bms_lifecycle.png" alt="BMTS는 전통적 BMS를 넘어 배터리 전체 lifecycle을 관리하는 software·cloud·AI 기반 솔루션으로 설명된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>BMTS는 전통적 BMS를 넘어 배터리 전체 lifecycle을 관리하는 software·cloud·AI 기반 솔루션으로 설명된다. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

그래서 BMS는 배터리 팩 안의 숨은 제어기를 넘어, 차량 전체 software architecture와 연결되는 data layer가 된다.

## 3. BMTS는 배터리를 생애주기 서비스로 확장한다

LG에너지솔루션이 말하는 BMTS는 BMS보다 넓다. 배터리의 현재 상태만 보는 것이 아니라, 진단, 예측, 관리, 서비스까지 포함한다.

<figure>
  <img src="assets/images/lgensol_sdv_bms.png" alt="SDV BMS는 BMS 기능을 차량의 고성능 컴퓨팅 환경과 연결하는 방향을 보여준다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>SDV BMS는 BMS 기능을 차량의 고성능 컴퓨팅 환경과 연결하는 방향을 보여준다. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

이 관점에서 배터리 SW의 가치는 세 가지로 확장된다.

```text
첫째, 안전성
- 이상 징후 감지
- 열화와 위험 신호 진단
- 사고 예방

둘째, 경제성
- 수명 예측
- 충전 전략 최적화
- 잔존가치 관리

셋째, 서비스화
- fleet battery management
- used battery assessment
- cloud-based diagnostics
- subscription or software service model
```

배터리 SW는 셀을 팔고 끝나는 사업이 아니라, 배터리가 사용되는 기간 전체를 관리하는 사업으로 이어질 수 있다.

## 4. SDVerse와 Qualcomm은 배터리 SW의 시장 위치를 바꾼다

LG에너지솔루션의 SDVerse 참여가 중요한 이유는 배터리 SW가 automotive software marketplace에 올라간다는 점이다. 즉, 배터리 회사의 software가 완성차 software ecosystem 안에서 거래되고 통합될 수 있다는 뜻이다.

> **이미지 URL 확보 필요**  
> LG에너지솔루션은 배터리 기업 최초로 SDVerse에 참여하며 SDV 환경에 최적화된 5개 battery software solution을 제시했다. 원문 이미지 URL은 별도 확보 필요.  
> 원문: [LG Energy Solution](https://www.lgensol.com/mobile/en/company/newsroom-detail?seq=8753)

Qualcomm과의 협력도 같은 방향이다. LG에너지솔루션은 Snapdragon Digital Chassis에서 SoC-based BMS diagnostic solution을 사용할 수 있도록 했다. 이는 battery algorithm이 dedicated low-performance hardware에 머물지 않고 차량의 high-performance computing platform에서 실시간으로 구동될 수 있다는 의미다.

<figure>
  <img src="assets/images/lgensol_bms_features_to_hpc.png" alt="Battery software가 SDV architecture와 연결되면 배터리는 차량 software layer의 일부가 된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Battery software가 SDV architecture와 연결되면 배터리는 차량 software layer의 일부가 된다. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

이 변화가 중요한 이유는 명확하다. 배터리 SW가 차량의 중앙 컴퓨팅 구조와 연결되면, 배터리는 부품이 아니라 차량 software experience의 일부가 된다.

## 5. 한 줄 결론

배터리 SW는 LG에너지솔루션의 부가 기능이 아니라 다음 플랫폼이 될 수 있다.  
셀의 성능을 넘어서 **배터리 데이터를 안전, 수명, 잔존가치, 차량 software 경험으로 연결하는 energy intelligence layer**가 되기 때문이다.

---

## Appendix A. Image Inventory

| image_id | source | status | image_url | local_filename |
|---|---|---|---|---|
| lgensol_baround_core_values | LG Energy Solution B.around | confirmed | https://www.lgensol.com/inc/images/img/serv02_img_03_mo_en.png | topic_08_lgensol_baround_core_values.png |
| lgensol_bms_lifecycle | LG Energy Solution B.around | confirmed | https://www.lgensol.com/inc/images/img/serv_bms_pop1_mo_en.png | topic_08_lgensol_bms_lifecycle.png |
| lgensol_sdv_bms | LG Energy Solution B.around | confirmed | https://www.lgensol.com/inc/images/img/serv_bms_pop5_mo_en.png | topic_08_lgensol_sdv_bms.png |
| lgensol_bms_to_hpc | LG Energy Solution B.around | confirmed | https://www.lgensol.com/inc/images/img/serv_bms_pop3_mo_en.png | topic_08_lgensol_bms_to_hpc.png |
| lgensol_sdverse_image_needed | LG Energy Solution | image_url_needed | IMAGE_URL_NEEDED | topic_08_lgensol_sdverse.jpg |

---

## Appendix B. Source Notes

### src_lgensol_baround

- URL: https://www.lgensol.com/mobile/en/business/baround
- Publisher: LG Energy Solution
- Published: unknown
- Used for: B.around, BMTS, SDV BMS, software·cloud·AI 기반 battery lifecycle management
- Images:
  - `lgensol_baround_core_values`
  - `lgensol_bms_lifecycle`
  - `lgensol_sdv_bms`
  - `lgensol_bms_to_hpc`

### src_lgensol_sdverse_20260403

- URL: https://www.lgensol.com/mobile/en/company/newsroom-detail?seq=8753
- Publisher: LG Energy Solution
- Published: 2026-04-03
- Used for: 배터리 기업 최초 SDVerse 참여, SDV 환경 최적화 5개 battery software solution
- Image:
  - `lgensol_sdverse_image_needed`

### src_lgensol_qualcomm_20241223

- URL: https://www.lgcorp.com/media/release/28499
- Publisher: LG Corp. / LG Energy Solution
- Published: 2024-12-23
- Used for: Qualcomm Snapdragon Digital Chassis 기반 SoC BMS diagnostic solution availability

### src_lgensol_qualcomm_20240310

- URL: https://news.lgensol.com/company-news/press-releases/2483/
- Publisher: LG Energy Solution
- Published: 2024-03-10
- Used for: dedicated low-performance hardware에서 high-performance Snapdragon Digital Chassis로 BMS algorithm 구동 구조 전환
