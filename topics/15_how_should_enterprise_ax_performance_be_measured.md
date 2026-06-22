---
id: topic_how_should_enterprise_ax_performance_be_measured
type: topic
title: "Enterprise AX의 성과는 사용량이 아니라 일이 바뀐 정도로 측정해야 한다"
subtitle: "도입률·질문 수를 넘어 생산성, 의사결정 품질, 실행 속도, 데이터 축적을 봐야 한다"
status: reviewed
updated: 2026-06-21
priority: P2
priority_score: 3.39
priority_updated: 2026-06-22
priority_model: recency_issue_v1
priority_factors:
  recency: 4.60
  issue_salience: 2.13
  strategic_impact: 3.38
  urgency: 2.65
  actionability: 4.02
priority_rationale: "최신성 4.6, 이슈성 2.1이 우선순위를 주도한다. 강점 요소는 최신성·실행 가능성이며, 최신 기준일 2026-06-21, 최근 180일 Source 비율 67%."
question: "Enterprise AX의 성과는 무엇으로 측정해야 하는가?"
short_answer: "Enterprise AX의 성과를 단순히 사용자 수, 프롬프트 수, 챗봇 호출량으로 측정하면 실제 변화를 놓칠 수 있다. 중요한 것은 AI가 업무의 어디까지 들어갔는가다. 개인 생산성, 업무 cycle time, 의사결정 품질, 실행 자동화, 시스템 연계, 비용 절감, 데이터·ontology 축적, 현업 adoption을 함께 봐야 한다. AX KPI는 AI 사용량이 아니라 조직의 일하는 방식이 바뀐 정도를 측정해야 한다."
topic_type:
  - operating_model
  - measurement_framework
related_themes:
  - enterprise_ax_agentic_operating_model
  - global_ai_alliance_open_innovation
related_concepts:
  - enterprise-ax
  - agentic-operating-model
  - ax-kpi
  - enterprise-ontology
  - workflow-automation
  - decision-intelligence
  - adoption-metrics
related_companies:
  - lg-cns
  - lg-energy-solution
  - lg-display
  - lg-ai-research
  - palantir
source_ids:
  - src_lgcns_ax_platform
  - src_lgcns_agenticworks_20250825
  - src_lgensol_ax_productivity_20260511
  - src_lgcns_palantir_20260312
image_policy:
  use_original_source_images: true
  generate_new_images: false
  download_script: scripts/download_topic_15_images.py
  local_image_dir: assets/images
tags:
  - enterprise-ax
  - ax-kpi
  - productivity
  - decision-intelligence
  - agentic-ai
  - ontology
---

# Enterprise AX의 성과는 사용량이 아니라 일이 바뀐 정도로 측정해야 한다

> **Summary**  
> Enterprise AX의 성과를 “몇 명이 썼는가”, “프롬프트를 몇 번 입력했는가”로만 보면 실제 변화를 놓친다. AI가 조직의 일하는 방식에 들어왔는지 보려면 개인 생산성, 업무 cycle time, 의사결정 품질, 실행 자동화, 비용 절감, 시스템 연계, 데이터·ontology 축적을 함께 봐야 한다. AX의 KPI는 AI 사용량이 아니라 **업무가 얼마나 짧아지고, 판단이 얼마나 좋아지고, 실행이 얼마나 자동화되었는가**를 측정해야 한다.

<figure>
  <img src="assets/images/lgcns_ax_platform_service_development.png" alt="Enterprise AX 성과는 AI 플랫폼 도입률보다 실제 workflow 변화와 연결되어야 한다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Enterprise AX 성과는 AI 플랫폼 도입률보다 실제 workflow 변화와 연결되어야 한다. 출처: <a href="https://www.lgcns.com/en/service/ai/ai-platform/">LG CNS</a></small></figcaption>
</figure>

## 1. Key Factors & Questions

### Key Factors

LG CNS는 AX Platform, AgenticWorks, a:xink 등 기업 AX를 위한 platform과 service를 확대하고 있다. 보도에 따르면 AgenticWorks는 agentic AI service의 설계, 구축, 운영, 관리를 지원하고, 고객관계관리(CRM), ERP 같은 기업 시스템과 연결될 수 있다.

연합뉴스 보도에 따르면 LG CNS는 대규모 채용 업무에 AgenticWorks를 적용하면 업무 생산성을 26% 높일 수 있다고 설명했다. 또 a:xink를 LG Display에 단계적으로 적용한 결과 일평균 업무 생산성이 약 10% 향상됐고 외부 서비스 대비 연간 100억원 이상 비용 절감 효과가 있었다고 밝혔다.

LG에너지솔루션은 2028년까지 AI Transformation을 통해 생산성을 최대 50% 높이겠다는 목표를 제시했다. 이 발표는 AX가 단순 도구 도입이 아니라 core operations와 decision-making, manufacturing performance를 바꾸는 initiatives라는 점을 보여준다.

### Questions

이 흐름에서 LG가 던져야 할 질문은 다음이다.

```text
1. AX 성과는 사용자 수와 사용량으로 충분히 측정될 수 있는가?
2. AI가 업무 전체 cycle time을 줄였는가?
3. AI가 의사결정 품질과 실행 속도를 개선했는가?
4. AI 사용 결과가 데이터와 ontology로 다시 축적되는가?
5. AX KPI는 개인 생산성, 조직 생산성, 사업 성과를 어떻게 나눠 봐야 하는가?
```

## 2. 사용량은 출발점이지 성과가 아니다

Enterprise AX 초기에는 사용량 지표가 필요하다. MAU, WAU, 프롬프트 수, active user, 부서별 도입률은 확산 상태를 보여준다. 하지만 이것만으로는 AX 성과를 말하기 어렵다.

사람들이 많이 쓴다고 해서 일이 바뀐 것은 아니다. 반대로 사용량은 낮아도 특정 핵심 업무의 cycle time이 크게 줄었다면 성과는 클 수 있다.

따라서 AX 지표는 다음처럼 나눠야 한다.

```text
사용 지표
= 누가, 얼마나, 어떤 업무에서 AI를 쓰는가

성과 지표
= 시간이 얼마나 줄었는가
= 비용이 얼마나 줄었는가
= 품질이 얼마나 좋아졌는가
= 의사결정과 실행이 얼마나 빨라졌는가
```

## 3. AX KPI는 workflow 기준으로 봐야 한다

AX는 사람에게 챗봇을 나눠주는 프로젝트가 아니다. 업무 흐름을 바꾸는 일이다. 따라서 KPI도 업무 단위로 설계되어야 한다.

<figure>
  <img src="assets/images/lgcns_ax_platform_operations.png" alt="AI가 기업 시스템과 연결될 때 AX 성과는 productivity, decision quality, execution speed로 측정되어야 한다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>AI가 기업 시스템과 연결될 때 AX 성과는 productivity, decision quality, execution speed로 측정되어야 한다. 출처: <a href="https://www.lgcns.com/en/service/ai/ai-platform/">LG CNS</a></small></figcaption>
</figure>

예를 들어 채용 업무라면 질문은 “AI를 몇 번 썼는가”가 아니다.

```text
- 서류 검토 시간이 얼마나 줄었는가?
- 후보자 shortlist 품질이 좋아졌는가?
- 면접 질문 생성 시간이 줄었는가?
- 채용 담당자의 반복 업무가 줄었는가?
- 최종 채용 품질에 영향이 있었는가?
```

재무, 구매, 품질, R&D, 영업, 고객상담도 마찬가지다. 업무별로 baseline을 잡고, cycle time, error rate, throughput, decision lead time, rework rate를 측정해야 한다.

> **이미지 URL 확보 필요**  
> LG CNS는 AgenticWorks와 a:xink를 공개하며 채용 업무 생산성 26% 개선, LG Display 적용 시 일평균 생산성 약 10% 향상과 연 100억원 이상 비용 절감 효과를 설명했다. 원문 이미지 URL은 별도 확보 필요.  
> 원문: [Yonhap News](https://www.yna.co.kr/view/AKR20250825032051017)

## 4. Enterprise AX의 깊이는 시스템 연계에서 갈린다

진짜 AX는 AI가 답변만 하는 단계에서 끝나지 않는다. ERP, CRM, SCM, MES, PLM 같은 기업 시스템과 연결되어야 한다. 그래야 AI가 추천을 넘어 실행으로 이어질 수 있다.

Palantir 협력이 중요한 이유도 여기에 있다. Foundry, AIP, ontology 기반 접근은 AI가 기업 데이터를 이해하고, 의사결정과 실행 시스템에 연결되는 방향을 보여준다.

<figure>
  <img src="assets/images/lgcns_palantir_signing.jpg" alt="Enterprise AX 성과를 깊게 보려면 AI 도구 사용량보다 ontology 기반 의사결정과 실행 연결성을 봐야 한다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Enterprise AX 성과를 깊게 보려면 AI 도구 사용량보다 ontology 기반 의사결정과 실행 연결성을 봐야 한다. 출처: <a href="https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion">Digital Today / LG CNS</a></small></figcaption>
</figure>

AX KPI도 이 깊이를 반영해야 한다.

```text
Level 1. 개인 생산성
- 문서 작성, 요약, 검색, 번역, 회의록

Level 2. 업무 생산성
- 특정 업무 cycle time 단축
- 오류율 감소
- 처리량 증가

Level 3. 의사결정 생산성
- 예측 정확도
- decision lead time
- 대안 탐색 폭
- 회의·보고 단계 축소

Level 4. 실행 자동화
- ERP/CRM/MES 연계
- agent workflow completion rate
- human approval 후 자동 실행률

Level 5. 학습 체계
- 실행 결과 데이터 축적
- ontology 업데이트
- 다음 의사결정 품질 개선
```

## 5. AX 성과는 조직 목표와 연결되어야 한다

LG에너지솔루션의 2028년 50% 생산성 목표는 AX KPI가 조직 목표와 연결되어야 한다는 점을 보여준다. AX는 IT 도입 프로젝트가 아니라 경쟁력 개선 프로젝트가 되어야 한다.

> **이미지 URL 확보 필요**  
> LG에너지솔루션은 2028년까지 AI Transformation을 통해 생산성을 최대 50% 향상하겠다는 목표를 제시했다. 원문 이미지 URL은 별도 확보 필요.  
> 원문: [LG Energy Solution](https://news.lgensol.com/company-news/supplementary-stories/4920/)

따라서 Enterprise AX KPI는 다음 네 가지 묶음으로 설계할 수 있다.

```text
1. Adoption
- active user
- 업무별 사용률
- 반복 사용률
- 부서별 확산률

2. Productivity
- cycle time reduction
- throughput increase
- cost saving
- rework reduction

3. Decision & Execution
- decision lead time
- forecast accuracy
- action completion rate
- system integration rate

4. Learning Asset
- reusable prompt / agent
- ontology object growth
- validated workflow template
- feedback data accumulation
```

## 6. 한 줄 결론

Enterprise AX의 성과는 AI를 얼마나 썼는지가 아니라 **일이 얼마나 바뀌었는가**로 측정해야 한다.  
사용량은 시작 지표이고, 진짜 KPI는 생산성, 의사결정 품질, 실행 자동화, 학습 자산 축적이다.

---

## Appendix A. Image Inventory

| image_id | source | status | image_url | local_filename |
|---|---|---|---|---|
| lgcns_ax_platform_1 | LG CNS | confirmed | https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_1.png | topic_15_lgcns_ax_platform_1.png |
| lgcns_ax_platform_2 | LG CNS | confirmed | https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_2.png | topic_15_lgcns_ax_platform_2.png |
| lgcns_agenticworks_image_needed | Yonhap News | image_url_needed | IMAGE_URL_NEEDED | topic_15_lgcns_agenticworks.jpg |
| lgensol_ax_productivity_image_needed | LG Energy Solution | image_url_needed | IMAGE_URL_NEEDED | topic_15_lgensol_ax_productivity.jpg |
| lgcns_palantir_signing | Digital Today / LG CNS | confirmed | https://cdn.digitaltoday.co.kr/news/photo/202603/640006_590746_75.jpg | topic_15_lgcns_palantir_signing.jpg |

---

## Appendix B. Source Notes

### src_lgcns_ax_platform

- URL: https://www.lgcns.com/en/service/ai/ai-platform/
- Publisher: LG CNS
- Published: unknown
- Used for: LG CNS AX Platform, enterprise AI platform context
- Images:
  - `lgcns_ax_platform_1`
  - `lgcns_ax_platform_2`

### src_lgcns_agenticworks_20250825

- URL: https://www.yna.co.kr/view/AKR20250825032051017
- Publisher: Yonhap News
- Published: 2025-08-25
- Used for: LG CNS AgenticWorks, a:xink, 채용 업무 생산성 26% 개선, LG Display 적용 시 일평균 생산성 약 10% 향상 및 연간 100억원 이상 비용 절감 효과
- Image:
  - `lgcns_agenticworks_image_needed`

### src_lgensol_ax_productivity_20260511

- URL: https://news.lgensol.com/company-news/supplementary-stories/4920/
- Publisher: LG Energy Solution
- Published: 2026-05-11
- Used for: AI Transformation, 2028년까지 생산성 최대 50% 향상 목표, core operations, real-time decision-making, predictive capabilities, intelligent automation
- Image:
  - `lgensol_ax_productivity_image_needed`

### src_lgcns_palantir_20260312

- URL: https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion
- Publisher: Digital Today / LG CNS
- Published: 2026-03-12
- Used for: Palantir Foundry, AIP, enterprise AI, ontology and decision intelligence
- Image:
  - `lgcns_palantir_signing`
