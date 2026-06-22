---
id: doc_ai_for_science_bio_materials_battery
type: doc
title: "AI for Science: Bio·Materials·Battery"
theme_id: ai_for_science_bio_materials_battery
status: draft
updated: 2026-06-21
related_concepts:
  - ai-for-science
  - ai-co-scientist
  - exaone-discovery
  - bio-intelligence
  - materials-intelligence
  - chemical-agentic-ai
  - closed-loop-rnd
  - peptide-drug-discovery
  - battery-materials
  - materials-informatics
related_companies:
  - lg-ai-research
  - lg-chem
  - lg-energy-solution
  - lg-household-health-care
  - lg-cns
  - dd-pharmatech
source_ids:
  - src_lgai_exaone
  - src_lgai_materials_intelligence
  - src_lgai_exaone_discovery_patent_20260203
  - src_lgai_dd_pharmatech_20260617
  - src_lgchem_life_science
  - src_lgchem_open_innovation
  - src_lgchem_cathode_material
  - src_lgensol_battery_technology_roadmap_20250620
  - src_lgensol_genai_battery_20250613
  - src_lghnh_ai_cosmetic_ingredients_20250323
tags:
  - ai-for-science
  - exaone-discovery
  - ai-co-scientist
  - bio-ai
  - materials-ai
  - battery-materials
  - drug-discovery
  - cosmetic-ingredients
---

# AI for Science: Bio·Materials·Battery

## 1. Executive Summary

AI for Science: Bio·Materials·Battery는 신약, 바이오, 화학, 배터리, 첨단소재, 화장품 원료 개발을 AI로 가속하는 테마다. 핵심은 [[concepts/exaone-discovery]]와 [[concepts/ai-co-scientist]]가 논문, 특허, 분자구조, 이미지, 실험 데이터 같은 과학 데이터를 이해하고, 후보물질 설계·탐색·실험 설계·결과 예측을 지원하는 것이다.

LG그룹 관점에서 이 테마는 [[companies/lg-ai-research]]의 Bio Intelligence·Materials Intelligence·Advanced Agent와 [[companies/lg-chem]], [[companies/lg-energy-solution]], [[companies/lg-household-health-care]]의 실험·검증·상용화 필드를 연결하는 구조다. AI가 후보를 만들고, 각 계열사가 실험·합성·평가·임상·제품화를 수행하며, 그 결과가 다시 모델에 피드백되는 **closed-loop R&D**가 핵심이다.

이 테마는 단기 매출보다 장기 R&D 생산성, 후보 탐색 속도, 특허 장벽, 고부가 소재·신약 포트폴리오 경쟁력에 의미가 크다. 성공 시 LG그룹은 기존 제조·소재 기업의 한계를 넘어 발견과 설계 중심의 AI 과학 기업으로 확장할 수 있다.

<figure>
  <img src="assets/images/exaone_discovery_operation.jpg" alt="EXAONE Discovery in operation. 논문·특허·분자구조 등 비정형 데이터를 활용해 후보물질 탐색과 실험 설계를 지원하는 예시." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>EXAONE Discovery in operation. 논문·특허·분자구조 등 비정형 데이터를 활용해 후보물질 탐색과 실험 설계를 지원하는 예시. 출처: <a href="https://en.fnnews.com/news/202602031623047760">Financial News / LG AI Research</a></small></figcaption>
</figure>

## 2. AI Market Landscape & Why Now

### 2.1 AI for Science는 연구개발의 병목을 바꾸고 있다

과학 R&D는 후보물질 탐색, 문헌 조사, 실험 설계, 합성 가능성 검토, 물성 예측, 안전성 검증, 임상 개발 등 시간이 오래 걸리고 실패율이 높은 프로세스로 구성된다. AI for Science는 이 중 데이터가 많고 반복성이 높은 영역을 모델이 지원함으로써, 후보 탐색 범위를 넓히고 실험 우선순위를 빠르게 정하는 방향으로 발전하고 있다.

특히 신약과 소재 개발은 후보 공간이 매우 크다. 사람이 논문과 특허를 읽고 후보를 좁히는 방식은 속도와 비용에 한계가 있다. 따라서 AI Co-Scientist는 연구자에게 답을 대신 주는 도구라기보다, 연구자가 질문하고, AI가 후보와 실험 방향을 제안하며, 실험 결과를 다시 학습하는 연구 동료에 가깝다.

### 2.2 LG AI Research는 EXAONE을 산업별 AI for Science 기반으로 확장

LG AI Research의 EXAONE은 2021년 이후 지속적으로 고도화되어 EXAONE 4.5까지 발전했다. EXAONE 4.5는 native multimodal 구조와 document-centric 데이터 설계를 강조하며, 복잡한 산업 현장의 시각·문서 맥락을 이해하는 방향으로 확장되고 있다.

AI for Science에서 중요한 것은 범용 LLM 성능만이 아니다. 논문, 특허, 분자구조, 실험 데이터, 이미지와 같은 도메인 데이터를 이해하고, 화학·바이오·소재 분야의 구조적 지식을 반영할 수 있어야 한다. EXAONE Discovery는 이 역할을 수행하는 과학 R&D 특화 플랫폼으로 정리된다.

### 2.3 배터리·소재·바이오 경쟁은 후보 탐색 속도와 특허 장벽의 경쟁이다

LG화학은 배터리 소재, 첨단소재, 생명과학을 중장기 성장축으로 보유하고 있다. LG Chem의 Cathode Material 공식 자료는 양극재가 리튬이온 배터리의 에너지밀도, 안전성, 비용을 좌우하는 핵심 소재라고 설명하며, 고니켈, 고전압 미드니켈, precursor-free cathode material 등 차별화된 소재 개발을 추진하고 있다.

LG에너지솔루션은 배터리 소재 개발에서 수많은 소재 구조를 평가해야 하기 때문에, Materials Informatics와 AI-driven technologies가 빠른 결과를 제공하고 개발 속도를 높일 수 있다고 설명한다. 전해질 소재 개발에서도 수억 건의 소재 기록을 담은 데이터베이스를 기반으로 최적 조합을 빠르게 찾는 시스템을 구축하려는 방향을 제시하고 있다.

## 3. Business Opportunities

| 기회 | 설명 | 관련 계열사 | 보유 자산 |
|---|---|---|---|
| EXAONE Discovery Platform | 논문·특허·분자구조·이미지 데이터를 분석해 신약·소재 후보를 탐색하는 AI 과학 플랫폼 | LG AI연구원 | EXAONE, Bio Intelligence, Materials Intelligence, Advanced Agent |
| AI Co-Scientist | 연구자가 질문하면 AI가 후보물질·실험 설계·예측 결과를 제안하는 연구 동료 모델 | LG AI연구원, LG화학, LG에너지솔루션, LG생활건강 | 과학 문헌, 특허, 실험 데이터, 연구자 workflow |
| Peptide Drug Discovery | 펩타이드 후보 설계, 구조 분석, 합성·평가·임상 피드백 루프 | LG AI연구원, D&D Pharmatech, LG화학 | AI 기반 후보 설계, peptide development, 임상 개발 경험 |
| Battery Materials AI | 양극재, 전해질, 첨가제, 건식전극, 차세대 소재 후보 탐색 | LG화학, LG에너지솔루션, LG AI연구원 | cathode material, electrolyte DB, Materials Informatics, 배터리 R&D |
| Cosmetic Ingredient Discovery | 화장품 효능 소재 후보 탐색, 합성 용이성, 안전성, 유해물질 가능성 예측 | LG생활건강, LG AI연구원 | EXAONE Discovery, 화장품 원료 R&D, 안전성 평가 |
| R&D Data Platform | ELN/LIMS/특허/논문/실험 데이터 통합 및 AI workflow 운영 | LG CNS, LG AI연구원, 각 연구 계열사 | 데이터 플랫폼, workflow 자동화, 보안·거버넌스 |
| Chemical Agentic AI | 배터리, 반도체, 제약, 화장품 등 화학 기반 산업에서 후보 탐색·실험 설계 자동화 | LG AI연구원, LG화학, LG에너지솔루션 | 화학 도메인 모델, 실험 피드백, 소재 데이터 |
| Patent & IP Intelligence | 특허 검색·요약·침해 가능성 검토·R&D 방향 탐색 | LG에너지솔루션, LG화학, LG AI연구원 | 특허 포트폴리오, EXAONE, GenAI chatbot |

### 3.1 LG AI Research / EXAONE / EXAONE Discovery

* 내용 요약
  - EXAONE은 LG그룹 AI for Science의 기반 모델이며, EXAONE Discovery는 논문·특허·분자구조·이미지 등 과학 데이터를 분석해 신약·소재 후보 탐색을 지원한다.
  - 핵심 사업기회는 단순 검색 도구가 아니라 후보물질 제안, 실험 설계, 결과 피드백을 연결하는 AI Co-Scientist 플랫폼이다.
  - D&D Pharmatech 협력처럼 AI가 후보를 설계하고 외부·계열사 연구조직이 합성·평가·임상 검증을 수행하는 closed-loop R&D 모델로 확장 가능하다.
  - LG화학·LG에너지솔루션·LG생활건강의 실험·검증 필드와 연결될 때 그룹 차원의 과학 R&D 플랫폼 자산이 된다.

<figure>
  <img src="assets/images/exaone_journey_timeline.png" alt="EXAONE Journey timeline. EXAONE 4.5까지 이어진 LG AI Research의 모델 고도화 흐름." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>EXAONE Journey timeline. EXAONE 4.5까지 이어진 LG AI Research의 모델 고도화 흐름. 출처: <a href="https://www.lgresearch.ai/exaone/">LG AI Research EXAONE</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/exaone_discovery_digitaltoday.gif" alt="EXAONE Discovery image from Digital Today. 일부 fetch 환경에서 400 응답 가능성이 있어 다운로드 확인 필요." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>EXAONE Discovery image from Digital Today. 일부 fetch 환경에서 400 응답 가능성이 있어 다운로드 확인 필요. 출처: <a href="https://www.digitaltoday.co.kr/en/view/2921/lg-ai-research-registers-gateway-patent-for-ai-to-aid-new-materials-and-drug-development">Digital Today / LG AI Research</a></small></figcaption>
</figure>

> **이미지 URL 확보 필요**  
> LG AI Research-D&D Pharmatech next-generation oral peptide drug discovery 협력. PRNewswire 원문에는 직접 삽입 가능한 행사 이미지가 확인되지 않아 이미지 URL 확보 필요.  
> 원문: [PRNewswire / LG AI Research](https://www.prnewswire.com/news-releases/lg-ai-research-announces-collaboration-with-dd-pharmatech-to-accelerate-next-generation-oral-peptide-drug-discovery-302802738.html)

## 3.2 LG Chem Life Science / Open Innovation / Battery Materials

* 내용 요약
  - LG화학은 생명과학, 첨단소재, 배터리 소재를 보유한 AI for Science의 핵심 실험·검증 계열사다.
  - Life Science 영역에서는 AI 신약 후보 탐색과 임상·제품화 역량을 연결할 수 있고, Open Innovation은 외부 기술과 AI 후보 발굴을 접목하는 통로가 된다.
  - 배터리 소재에서는 양극재, 전해질, 첨가제 등 후보 공간이 넓어 AI 기반 소재 탐색과 특허·문헌 분석의 가치가 크다.
  - Theme 5 관점에서는 LG AI Research가 후보를 제안하고 LG화학이 합성·검증·상용화를 담당하는 구조가 핵심이다.

<figure>
  <img src="assets/images/lgchem_life_science_sales_graph.png" alt="LG Chem Life Science sales graph. 생명과학 사업의 중장기 성장축을 보여주는 공식 이미지." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Chem Life Science sales graph. 생명과학 사업의 중장기 성장축을 보여주는 공식 이미지. 출처: <a href="https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US">LG Chem Life Science</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_life_science_primary_care.jpg" alt="LG Chem Life Science Primary Care division image. AI 신약개발의 실험·검증 필드와 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Chem Life Science Primary Care division image. AI 신약개발의 실험·검증 필드와 연결된다. 출처: <a href="https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US">LG Chem Life Science</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_life_science_specialty_care.jpg" alt="LG Chem Life Science Specialty Care division image. 바이오·신약 R&D 자산과 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Chem Life Science Specialty Care division image. 바이오·신약 R&D 자산과 연결된다. 출처: <a href="https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US">LG Chem Life Science</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_open_innovation_energy_materials.jpg" alt="Energy Transition & Sustainable Materials. 배터리·재생에너지 소재 오픈이노베이션 방향과 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Energy Transition & Sustainable Materials. 배터리·재생에너지 소재 오픈이노베이션 방향과 연결된다. 출처: <a href="https://www.lgchem.com/company/research-and-development/open-innovation?lang=en_US">LG Chem Open Innovation</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_cathode_mobile_application.png" alt="Cathode material application image: mobile batteries." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Cathode material application image: mobile batteries. 출처: <a href="https://www.lgchem.com/product-detail/cathode-material?lang=en_US">LG Chem Cathode Material</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_cathode_auto_application.png" alt="Cathode material application image: automotive batteries." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Cathode material application image: automotive batteries. 출처: <a href="https://www.lgchem.com/product-detail/cathode-material?lang=en_US">LG Chem Cathode Material</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_cathode_ess_application.png" alt="Cathode material application image: ESS batteries." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Cathode material application image: ESS batteries. 출처: <a href="https://www.lgchem.com/product-detail/cathode-material?lang=en_US">LG Chem Cathode Material</a></small></figcaption>
</figure>

### 3.3 LG Energy Solution Battery Materials / GenAI

* 내용 요약
  - LG에너지솔루션은 배터리 성능·안전·수명과 직결되는 소재·공정 데이터를 보유한 AI for Science 적용 필드다.
  - Materials Informatics와 GenAI는 양극재, 전해질, 건식전극, 첨가제 등 배터리 소재 후보 탐색 속도를 높이는 데 활용될 수 있다.
  - 특허·논문·실험 데이터 기반 AI chatbot과 소재 탐색 모델은 연구자의 탐색·분석·검증 시간을 줄이는 R&D 생산성 도구가 된다.
  - 장기적으로는 배터리 소재 발견, 셀 설계, 수명 예측, 품질 데이터가 연결되는 battery intelligence 플랫폼으로 확장 가능하다.

<figure>
  <img src="assets/images/lgensol_battery_technology_roadmap_mid_nickel.png" alt="LG Energy Solution battery technology roadmap presentation. 소재·공정 혁신과 AI-driven materials research 흐름." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Energy Solution battery technology roadmap presentation. 소재·공정 혁신과 AI-driven materials research 흐름. 출처: <a href="https://inside.lgensol.com/en/2025/06/lg-energy-solutions-battery-technology-roadmap-creating-customer-value-through-material-and-process-innovation/">LG Energy Solution Battery Inside</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgchem_cathode_material_main.png" alt="LG Chem Cathode Material page hero image. 배터리 소재 탐색·검증의 핵심 적용 영역." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Chem Cathode Material page hero image. 배터리 소재 탐색·검증의 핵심 적용 영역. 출처: <a href="https://www.lgchem.com/product-detail/cathode-material?lang=en_US">LG Chem Cathode Material</a></small></figcaption>
</figure>

### 3.4 LG Household & Health Care Cosmetic Ingredient Innovation

* 내용 요약
  - LG생활건강은 EXAONE Discovery를 활용한 화장품 효능 소재 발굴의 대표적인 상용화 필드다.
  - AI가 분자구조와 물성 데이터를 분석해 효능 가능성, 합성 용이성, 안전성, 유해물질 가능성을 사전 검토함으로써 원료 탐색 시간을 줄일 수 있다.
  - 화장품 원료는 신약보다 상용화 사이클이 짧아 AI for Science의 초기 사업성과 레퍼런스를 만들기 유리하다.
  - Theme 5에서는 AI 후보 탐색 결과가 실제 브랜드·제품으로 연결되는 소비재 적용 사례로 정리할 수 있다.

<figure>
  <img src="assets/images/lghnh_bichup_nad_symposium.jpg" alt="LG Household & Health Care The Whoo Bichup NAD+ Symposium. AI 기반 화장품 효능 소재 개발 사례와 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Household & Health Care The Whoo Bichup NAD+ Symposium. AI 기반 화장품 효능 소재 개발 사례와 연결된다. 출처: <a href="https://www.mk.co.kr/en/special-edition/11271183">Maeil Business News / LG Household & Health Care</a></small></figcaption>
</figure>

## 4. LG Group Strategic Meaning

### 4.1 AI가 후보를 찾고, 계열사가 실험·검증·상용화한다

AI for Science의 핵심은 모델 단독 성능이 아니다. LG그룹은 AI 모델을 보유한 LG AI Research와, 실제 실험·검증·제품화 필드를 가진 화학·배터리·생활과학 계열사를 동시에 보유한다. 따라서 AI가 후보를 생성하고, 계열사가 실험·검증하며, 결과가 다시 AI 모델에 피드백되는 폐쇄 루프를 만들 수 있다.

```text
논문/특허/분자구조/이미지/실험 데이터
  → EXAONE Discovery 분석
  → 후보물질·후보소재 생성
  → 실험 설계·물성·안전성 예측
  → 계열사 연구소 합성·검증·평가
  → 결과 피드백
  → 모델 성능 개선
```

### 4.2 AI for Science는 LG의 제조·소재 경쟁력을 발견 역량으로 확장한다

LG의 전통적 강점은 소재·제조·품질·양산 역량이다. 하지만 AI for Science는 이 강점을 한 단계 앞단으로 끌어올린다. 즉, 이미 정해진 소재를 잘 만드는 기업에서, **어떤 소재를 만들지 AI로 먼저 발견하고 설계하는 기업**으로 이동할 수 있다.

LG화학은 배터리 소재와 생명과학, LG에너지솔루션은 배터리 성능·안전·수명 데이터, LG생활건강은 화장품 효능 소재와 안전성 평가, LG AI Research는 AI 모델과 후보 탐색 엔진을 제공한다. 이 조합은 단일 계열사보다 그룹 차원의 시너지가 크다.

### 4.3 특허와 데이터가 장기 진입장벽이 된다

EXAONE Discovery 특허는 단순 알고리즘이 아니라, 비정형 문서에서 분자구조를 추출하고, 연구자 질문과 라벨을 기반으로 실험과 물질 예측을 수행하는 R&D 프로세스 전반을 보호하는 것으로 설명된다. 이는 AI for Science에서 모델 성능뿐 아니라 workflow, 데이터, 특허가 함께 진입장벽이 된다는 점을 보여준다.


## 5. 계열사별 역할

| 계열사 | 역할 | 관련 Source |
|---|---|---|
| LG AI연구원 | EXAONE Discovery, AI Co-Scientist, Bio Intelligence, Materials Intelligence, 후보물질 설계·탐색·실험 설계, Cancer Agentic AI, Chemical Agentic AI | [[sources/src_lgai_exaone]], [[sources/src_lgai_exaone_discovery_patent_20260203]], [[sources/src_lgai_dd_pharmatech_20260617]] |
| LG화학 | 생명과학 R&D, 신약 후보 검증, 첨단소재·배터리 소재 개발, 오픈이노베이션 기반 외부 협력 | [[sources/src_lgchem_life_science]], [[sources/src_lgchem_open_innovation]], [[sources/src_lgchem_cathode_material]] |
| LG에너지솔루션 | 배터리 소재 후보 탐색, 전해질·첨가제·건식전극 등 소재·공정 R&D, Materials Informatics, 특허 AI chatbot | [[sources/src_lgensol_battery_technology_roadmap_20250620]], [[sources/src_lgensol_genai_battery_20250613]] |
| LG생활건강 | 화장품 효능 소재 탐색, 합성 가능성·안전성 검토, AI 기반 신원료 상용화 | [[sources/src_lghnh_ai_cosmetic_ingredients_20250323]], [[sources/src_lgai_exaone_discovery_patent_20260203]] |
| LG CNS | 연구 데이터 플랫폼, 실험 데이터 관리, LIMS/ELN, 특허·논문 데이터 파이프라인, AI 모델 운영 환경 | 검증 필요. 직접 사례보다 시스템 구현 역량 기반 |
| LG디스플레이 | OLED/디스플레이 소재 탐색, 패널 수명·효율·공정 소재 개선 | 검증 필요. AI 소재 탐색과 디스플레이 소재 연계 가능성 |
| LG이노텍 | 광학·기판·센서·방열 소재 개선 | 검증 필요. 부품 소재 고도화 가능성 |
| LG Corp. / LG Technology Ventures | 바이오·소재·AI 스타트업 투자, 오픈이노베이션 포트폴리오 조정 | 검증 필요. 그룹 미래기술 투자 역할 기반 |

## 6. Related Concepts

- [[concepts/ai-for-science]]
- [[concepts/ai-co-scientist]]
- [[concepts/exaone-discovery]]
- [[concepts/bio-intelligence]]
- [[concepts/materials-intelligence]]
- [[concepts/chemical-agentic-ai]]
- [[concepts/closed-loop-rnd]]
- [[concepts/peptide-drug-discovery]]
- [[concepts/battery-materials]]
- [[concepts/materials-informatics]]
- [[concepts/patent-intelligence]]

## 7. Related Companies

- [[companies/lg-ai-research]]
- [[companies/lg-chem]]
- [[companies/lg-energy-solution]]
- [[companies/lg-household-health-care]]
- [[companies/lg-cns]]
- [[companies/partners/dd-pharmatech]]
- [[companies/partners/vanderbilt-university-medical-center]]

## 8. Sources

- [[sources/src_lgai_exaone]]
- [[sources/src_lgai_materials_intelligence]]
- [[sources/src_lgai_exaone_discovery_patent_20260203]]
- [[sources/src_lgai_dd_pharmatech_20260617]]
- [[sources/src_lgchem_life_science]]
- [[sources/src_lgchem_open_innovation]]
- [[sources/src_lgchem_cathode_material]]
- [[sources/src_lgensol_battery_technology_roadmap_20250620]]
- [[sources/src_lgensol_genai_battery_20250613]]
- [[sources/src_lghnh_ai_cosmetic_ingredients_20250323]]

## 9. Open Questions

- EXAONE Discovery의 실제 기술 구조는 어느 수준까지 공개되어 있는가?
- AI Co-Scientist와 기존 소재·신약 실험 자동화의 차이는 무엇인가?
- 배터리 소재 탐색에서 AI가 줄일 수 있는 가장 큰 병목은 후보 생성, 물성 예측, 합성 가능성, 안전성 평가 중 무엇인가?
- LG AI연구원과 LG화학·LG에너지솔루션·LG생활건강 간 실험 피드백 루프는 어느 수준까지 운영되고 있는가?
- AI 신약개발에서 후보 탐색 속도 개선이 임상 성공률 개선으로 이어질 수 있는가?
- Bio AI와 Materials AI를 공통 플랫폼으로 묶을 수 있는가?
- AI가 생성한 후보물질의 특허권과 책임 소재는 어떻게 설계해야 하는가?
- AI for Science의 KPI는 후보 탐색 시간, 실험 성공률, 특허 수, 제품화 기간, 임상 성공률 중 무엇을 중심으로 봐야 하는가?

---

# Appendix A. Source Notes

## src_lgai_exaone

- URL: https://www.lgresearch.ai/exaone/
- Publisher: LG AI Research
- Key facts:
  - EXAONE은 2021년 이후 4.5까지 발전했다.
  - EXAONE 4.5는 native multimodal 구조, visual encoder, document understanding, long-context reasoning을 강조한다.
  - 산업 분야 지원을 모델 특징 중 하나로 제시한다.

## src_lgai_materials_intelligence

- URL: https://www.lgresearch.ai/ourwork/research?tab=PE
- Publisher: LG AI Research
- Key facts:
  - Materials Intelligence는 오픈 DB, 논문·특허 문헌 정보, 직접 실험 데이터 등을 활용한다.
  - 소재 구조와 물성을 예측하고, 후보물질 탐색과 실험 설계의 효율화를 지향한다.

## src_lgai_exaone_discovery_patent_20260203

- URL: https://en.fnnews.com/news/202602031623047760
- Publisher: Financial News
- Published: 2026-02-03
- Key facts:
  - EXAONE Discovery는 신소재·신약 개발을 위한 AI 기반 플랫폼이다.
  - 논문, 특허, 분자구조, 이미지 등 멀티모달 데이터를 분석한다.
  - LG는 EXAONE Discovery를 화장품 원료, 배터리 소재, 신약 개발에 적용하고 있다.
  - 화장품 소재 사례에서 4천만 개 이상 물질을 검토했고, 22개월 걸리던 검토를 하루로 단축했다.
  - LG는 EXAONE Discovery를 Chemical Agentic AI로 발전시킬 계획이라고 설명했다.

## src_lgai_dd_pharmatech_20260617

- URL: https://www.prnewswire.com/news-releases/lg-ai-research-announces-collaboration-with-dd-pharmatech-to-accelerate-next-generation-oral-peptide-drug-discovery-302802738.html
- Publisher: PRNewswire / LG AI Research
- Published: 2026-06-17
- Key facts:
  - LG AI Research와 D&D Pharmatech는 차세대 경구용 펩타이드 신약 공동개발 계약을 체결했다.
  - LG AI Research는 펩타이드 후보물질 발견·설계 모델을 개발한다.
  - D&D Pharmatech는 구조 설계, 합성, 평가, 제형, 전임상·임상, 글로벌 규제 승인 절차를 담당한다.
  - 두 회사는 AI 후보 제안과 실험 검증 결과 피드백을 연결하는 continuous feedback loop를 구축할 계획이다.
  - Cancer Agentic AI와 EXAONE Discovery 등 Biology AI 포트폴리오가 함께 언급된다.

## src_lgchem_life_science

- URL: https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US
- Publisher: LG Chem
- Key facts:
  - Life Science는 LG Chem의 중장기 성장엔진으로 설명된다.
  - LG Chem은 R&D 역량, 신약 파이프라인, 글로벌 진출, AVEO 인수 등을 통해 글로벌 제약사로의 도약을 지향한다.

## src_lgchem_open_innovation

- URL: https://www.lgchem.com/company/research-and-development/open-innovation?lang=en_US
- Publisher: LG Chem
- Key facts:
  - LG Chem은 친환경 소재, 배터리 소재, 재생에너지 소재, 신약 등에서 외부 협력과 오픈이노베이션을 추진한다.
  - 배터리 성능·효율 개선을 위해 CNT, aerogel, heat-resistant adhesives, cathode binders 등 새로운 소재를 개발하고 있다.

## src_lgchem_cathode_material

- URL: https://www.lgchem.com/product-detail/cathode-material?lang=en_US
- Publisher: LG Chem
- Key facts:
  - Cathode materials are at the core of lithium-ion battery innovation.
  - LG Chem은 high-nickel, high-voltage mid-nickel, precursor-free cathode materials를 개발하고 있다.
  - 2030년까지 생산능력 360,000 tons/year 확대 계획을 제시한다.

## src_lgensol_battery_technology_roadmap_20250620

- URL: https://inside.lgensol.com/en/2025/06/lg-energy-solutions-battery-technology-roadmap-creating-customer-value-through-material-and-process-innovation/
- Publisher: LG Energy Solution Battery Inside
- Published: 2025-06-20
- Key facts:
  - LG Energy Solution은 Materials Informatics와 AI-driven technologies를 배터리 소재 개발에 활용한다고 설명한다.
  - 수많은 소재 구조를 평가해야 하는 cathode material 개발에서 AI가 빠른 결과와 개발 속도 향상을 제공할 수 있다고 설명한다.
  - 전해질 소재 개발에서도 수억 건의 소재 기록 DB를 기반으로 최적 조합을 빠르게 찾는 시스템을 지향한다.

## src_lgensol_genai_battery_20250613

- URL: https://inside.lgensol.com/en/2025/06/genai-transforming-the-present-and-future-of-the-battery-industry/
- Publisher: LG Energy Solution Battery Inside
- Published: 2025-06-13
- Key facts:
  - LG Energy Solution은 EXAONE 7.8B 기반 배터리 지식 AI chatbot을 활용해 특허 검색·요약을 수행한다.
  - 내부 특허뿐 아니라 공개 특허 데이터 전체로 범위를 확장할 계획이다.
  - LG Energy Solution은 약 72,000건의 특허를 보유하고 있다고 설명한다.

## src_lghnh_ai_cosmetic_ingredients_20250323

- URL: https://www.mk.co.kr/en/special-edition/11271183
- Publisher: Maeil Business News
- Published: 2025-03-23
- Key facts:
  - LG생활건강과 LG AI연구원이 AI 모델로 고효능 화장품 소재를 개발했다고 보도됐다.
  - EXAONE Discovery가 분자구조 데이터를 분석하고 각 물질의 특성을 예측해 후보 소재 탐색 시간과 비용을 줄였다고 설명된다.
  - AI가 분자 수준에서 연구 과정 전체를 설계한 사례로 설명된다.
