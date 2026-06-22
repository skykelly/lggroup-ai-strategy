---
id: topic_should_lg_build_foundation_models_or_focus_on_industry_models
type: topic
title: "LG는 foundation model을 키우되, 승부는 산업 특화 AI에서 봐야 한다"
subtitle: "EXAONE은 목적이 아니라 기반이다. 차별화는 LG의 데이터와 workflow에 붙을 때 생긴다"
status: reviewed
updated: 2026-06-21
priority: P2
priority_score: 3.46
priority_updated: 2026-06-22
priority_model: recency_issue_v1
priority_factors:
  recency: 5.00
  issue_salience: 2.85
  strategic_impact: 3.58
  urgency: 1.50
  actionability: 3.09
priority_rationale: "최신성 5.0, 이슈성 2.9이 우선순위를 주도한다. 강점 요소는 최신성·전략 영향도이며, 최신 기준일 2026-06-21, 최근 180일 Source 비율 100%."
question: "LG는 foundation model을 직접 키워야 하는가, 산업 특화 모델에 집중해야 하는가?"
short_answer: "LG는 foundation model을 포기해서도 안 되고, foundation model만으로 승부하려 해서도 안 된다. EXAONE과 K-EXAONE은 LG가 AI를 이해하고 통제할 수 있는 기반 역량이다. 하지만 글로벌 frontier model과 오픈 모델이 빠르게 발전하는 상황에서 LG의 차별화는 범용 모델 순위보다 산업 문서, 제조 데이터, R&D 데이터, 고객·제품 lifecycle 데이터에 붙은 산업 특화 AI에서 나온다. 전략은 자체 foundation model + 외부 frontier model + 산업 특화 layer를 조합하는 hybrid AI stack이 되어야 한다."
topic_type:
  - strategic_question
  - technology_strategy
related_themes:
  - enterprise_ax_agentic_operating_model
  - ai_for_science_bio_materials_battery
  - physical_ai_smart_manufacturing
  - global_ai_alliance_open_innovation
related_concepts:
  - foundation-model
  - industry-specialized-ai
  - hybrid-ai-strategy
  - exaone
  - k-exaone
  - enterprise-ontology
  - model-governance
related_companies:
  - lg-ai-research
  - lg-cns
  - lg-electronics
  - lg-chem
  - lg-energy-solution
  - nvidia
  - palantir
source_ids:
  - src_lgai_exaone
  - src_lgcorp_exaone45_20260409
  - src_exaone45_technical_report_20260409
  - src_k_exaone_huggingface_20260105
  - src_lg_nvidia_map_20260608
  - src_lgcns_palantir_20260312
image_policy:
  use_original_source_images: true
  generate_new_images: false
  download_script: scripts/download_topic_14_images.py
  local_image_dir: assets/images
tags:
  - foundation-model
  - exaone
  - industry-specialized-ai
  - hybrid-ai
  - model-strategy
---

# LG는 foundation model을 키우되, 승부는 산업 특화 AI에서 봐야 한다

> **Summary**  
> LG가 foundation model을 직접 키워야 하느냐는 질문은 “예/아니오”로 답하기 어렵다. EXAONE과 K-EXAONE은 LG가 AI를 이해하고 통제할 수 있게 만드는 중요한 기반 역량이다. 하지만 글로벌 frontier model과 오픈 모델의 발전 속도를 고려하면, LG가 범용 모델 성능 순위만으로 승부하는 것은 쉽지 않다. LG의 차별화는 foundation model 자체가 아니라, 그 모델을 **산업 문서, 제조 데이터, R&D 데이터, 고객·제품 lifecycle, 기업 workflow**에 붙여 산업 특화 AI로 만드는 데 있다.

<figure>
  <img src="assets/images/exaone_journey_timeline.png" alt="EXAONE은 LG가 자체 foundation model 역량을 축적해온 흐름을 보여준다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>EXAONE은 LG가 자체 foundation model 역량을 축적해온 흐름을 보여준다. 출처: <a href="https://www.lgresearch.ai/exaone/">LG AI Research</a></small></figcaption>
</figure>

## 1. Key Factors & Questions

### Key Factors

LG AI Research는 2026년 4월 EXAONE 4.5를 공개했다. EXAONE 4.5는 LG AI Research가 공개한 첫 open-weight vision-language model이며, 33B 규모의 모델로 소개된다. 기술보고서에 따르면 EXAONE 4.5는 256K context length, document understanding, Korean contextual reasoning, enterprise-scale use case를 강조한다.

K-EXAONE은 더 큰 규모의 proprietary foundation model 방향을 보여준다. Hugging Face 설명에 따르면 K-EXAONE은 236B total parameters, 23B active parameters의 MoE 모델이며, reasoning, agentic capabilities, multilingual understanding, long-context processing을 강조한다.

동시에 LG는 NVIDIA, Palantir 같은 외부 AI stack과도 협력하고 있다. 이는 LG가 자체 모델만으로 모든 것을 해결하기보다, 자체 모델과 외부 모델, 산업 데이터, ontology를 조합하는 hybrid AI 전략을 필요로 한다는 점을 보여준다.

### Questions

이 흐름에서 LG가 던져야 할 질문은 다음이다.

```text
1. LG는 foundation model 자체를 글로벌 1등으로 키워야 하는가?
2. EXAONE은 독립 제품인가, LG 산업 AI의 기반 layer인가?
3. 외부 frontier model과 EXAONE을 어떤 기준으로 나눠 써야 하는가?
4. LG의 차별화는 모델 성능인가, 산업 데이터와 workflow 결합력인가?
```

## 2. 자체 foundation model은 필요하다

LG가 foundation model을 직접 키우는 것은 의미가 있다. 이유는 세 가지다.

첫째, AI를 이해하는 내부 역량이 생긴다. 모델을 직접 만들고 운영해본 조직은 외부 모델을 도입할 때도 더 정확한 판단을 할 수 있다.

둘째, 보안과 거버넌스 관점에서 선택지가 생긴다. 모든 데이터를 외부 모델에 맡기기 어려운 기업 환경에서는 내부적으로 통제 가능한 모델이 필요하다.

셋째, 한국어와 산업 문서 같은 특수 맥락에서 강점을 만들 수 있다. EXAONE 4.5가 문서 이해와 한국어 맥락 이해를 강조하는 것도 이 지점과 맞닿아 있다.

<figure>
  <img src="assets/images/topic_02_lgai_exaone45_performance.png" alt="EXAONE 4.5는 문서 이해와 한국어 맥락 이해 등 산업 적용 영역의 강점을 강조한다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>EXAONE 4.5는 문서 이해와 한국어 맥락 이해 등 산업 적용 영역의 강점을 강조한다. 출처: <a href="https://www.lgresearch.ai/exaone/">LG AI Research</a></small></figcaption>
</figure>

따라서 foundation model을 직접 키우는 것은 단순 연구 과제가 아니라, LG가 AI 시대의 기술 판단권을 갖기 위한 기반이다.

## 3. 하지만 범용 모델 순위가 최종 목표는 아니다

문제는 foundation model을 키우는 목적이다. 글로벌 frontier model은 막대한 자본, 인프라, 데이터, 사용자 피드백, 개발자 생태계를 기반으로 빠르게 발전한다. LG가 모든 범용 벤치마크에서 이들과 정면 승부하는 것은 쉽지 않다.

그렇다면 질문을 바꿔야 한다.

```text
EXAONE이 GPT, Gemini, Claude를 이길 수 있는가?
```

보다 중요한 질문은 다음이다.

```text
EXAONE이 LG의 산업 데이터를 가장 잘 이해하고, LG의 업무와 R&D를 가장 잘 실행하게 만들 수 있는가?
```

이 질문으로 보면 전략 방향이 달라진다.

<figure>
  <img src="https://raw.githubusercontent.com/LG-AI-EXAONE/EXAONE-4.5/main/assets/EXAONE_Symbol%2BBI_3d.png" alt="EXAONE 4.5의 공개는 자체 모델을 생태계와 연결하려는 시도다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>EXAONE 4.5의 공개는 자체 모델을 생태계와 연결하려는 시도다. 출처: <a href="https://github.com/LG-AI-EXAONE/EXAONE-4.5">LG-AI-EXAONE GitHub</a></small></figcaption>
</figure>

## 4. 승부처는 산업 특화 layer다

LG가 진짜로 차별화할 수 있는 영역은 산업 특화 layer다.

```text
- 제품 사양서와 기술 문서를 이해하는 AI
- 제조 데이터와 설비 데이터를 해석하는 AI
- 품질 이슈와 원인을 추적하는 AI
- 배터리 소재와 특허를 분석하는 AI
- 고객·설치·서비스 lifecycle을 이해하는 AI
- 사내 ERP, CRM, MES, PLM과 연결되어 실행하는 Agent
```

이런 AI는 foundation model만으로 만들어지지 않는다. 기업 데이터, ontology, workflow, 평가 체계, 현업 feedback이 결합되어야 한다.

<figure>
  <img src="assets/images/lgcns_palantir_signing.jpg" alt="산업 특화 AI는 모델 자체보다 기업 데이터와 workflow, ontology와 함께 작동할 때 의미가 커진다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>산업 특화 AI는 모델 자체보다 기업 데이터와 workflow, ontology와 함께 작동할 때 의미가 커진다. 출처: <a href="https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion">Digital Today / LG CNS</a></small></figcaption>
</figure>

## 5. 결론은 hybrid AI stack이다

LG의 답은 하나의 모델을 고르는 것이 아니다. 자체 foundation model, 외부 frontier model, 산업 특화 모델을 조합해야 한다.

```text
외부 frontier model
= 최고 성능, 범용 추론, 빠른 기능 활용

EXAONE / K-EXAONE
= 내부 통제, 한국어·산업 문서, LG 특화 tuning

산업 특화 layer
= 제조·R&D·고객·배터리·모빌리티 workflow와 연결

Ontology / data operating model
= 모델이 LG의 운영 세계를 이해하게 만드는 기반
```

NVIDIA 협력도 같은 맥락에서 봐야 한다. 외부 stack을 쓰되, LG의 산업 데이터와 workflow를 내부 자산으로 남기는 방식이어야 한다.

<figure>
  <img src="assets/images/lg_nvidia_map_koo_huang_prn.jpg" alt="NVIDIA 협력은 LG가 자체 모델과 글로벌 AI stack을 함께 쓰는 hybrid strategy의 필요성을 보여준다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>NVIDIA 협력은 LG가 자체 모델과 글로벌 AI stack을 함께 쓰는 hybrid strategy의 필요성을 보여준다. 출처: <a href="https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html">PRNewswire / LG</a></small></figcaption>
</figure>

## 6. 한 줄 결론

LG는 foundation model을 키워야 한다.  
하지만 승부는 foundation model 자체가 아니라 **LG의 데이터와 업무에 붙은 산업 특화 AI layer**에서 봐야 한다.

---

## Appendix A. Image Inventory

| image_id | source | status | image_url | local_filename |
|---|---|---|---|---|
| lgai_exaone_journey | LG AI Research | confirmed | https://www.lgresearch.ai/img/solution/exaone_journey_pc.png | topic_14_lgai_exaone_journey.png |
| lgai_exaone45_performance | LG AI Research | confirmed | https://www.lgresearch.ai/img/solution/perpomance_4_5_h1.png | topic_14_lgai_exaone45_performance.png |
| exaone45_github_symbol | LG-AI-EXAONE GitHub | confirmed | https://raw.githubusercontent.com/LG-AI-EXAONE/EXAONE-4.5/main/assets/EXAONE_Symbol%2BBI_3d.png | topic_14_exaone45_github_symbol.png |
| lg_nvidia_map_koo_huang | PRNewswire / LG | confirmed | https://mma.prnewswire.com/media/2995864/1.jpg?w=500 | topic_14_lg_nvidia_map_koo_huang.jpg |
| lgcns_palantir_signing | Digital Today / LG CNS | confirmed | https://cdn.digitaltoday.co.kr/news/photo/202603/640006_590746_75.jpg | topic_14_lgcns_palantir_signing.jpg |

---

## Appendix B. Source Notes

### src_lgai_exaone

- URL: https://www.lgresearch.ai/exaone/
- Publisher: LG AI Research
- Published: unknown
- Used for: EXAONE Journey, EXAONE model family context
- Images:
  - `lgai_exaone_journey`
  - `lgai_exaone45_performance`

### src_lgcorp_exaone45_20260409

- URL: https://www.lg.co.kr/media/release/30024
- Publisher: LG Corp.
- Published: 2026-04-09
- Used for: EXAONE 4.5, 33B, open-weight release, VLM, multimodal expansion, physical intelligence goal

### src_exaone45_technical_report_20260409

- URL: https://arxiv.org/abs/2604.08644
- Publisher: arXiv / LG AI Research
- Published: 2026-04-09
- Used for: EXAONE 4.5, first open-weight VLM, 256K context, document understanding, Korean contextual reasoning, enterprise-scale use case

### src_k_exaone_huggingface_20260105

- URL: https://huggingface.co/LGAI-EXAONE/K-EXAONE-236B-A23B
- Publisher: Hugging Face / LG AI Research
- Published: 2026-01-05
- Used for: K-EXAONE 236B total parameters, 23B active parameters, MoE architecture, reasoning and long-context capabilities

### src_lg_nvidia_map_20260608

- URL: https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html
- Publisher: PRNewswire / LG
- Published: 2026-06-08
- Used for: NVIDIA 협력과 hybrid AI stack 필요성
- Image:
  - `lg_nvidia_map_koo_huang`

### src_lgcns_palantir_20260312

- URL: https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion
- Publisher: Digital Today / LG CNS
- Published: 2026-03-12
- Used for: ontology, enterprise AI, industry workflow와 model 결합
- Image:
  - `lgcns_palantir_signing`
