# Wiki Generation Guide for Codex — Final

> Project: LG Group AI Strategy Wiki  
> Purpose: Codex가 GPT-5.5에서 작성한 Docs와 Topics를 기준으로 Wiki repository를 생성·정리·검증하도록 지시한다.  
> Writing language: Korean  
> Current baseline date: 2026-06-21  
> Important principle: 이 Wiki는 공개 출처 기반으로 LG그룹의 AI 시대 사업기회와 핵심 전략 질문을 정리하는 Entity 기반 지식베이스다.

---

## 0. Codex에게 주는 최상위 지시

이 프로젝트의 핵심 작성물은 **Docs**와 **Topics**다.

```text
1차 작성 대상
- docs/    : 6대 테마별 전략 문서
- topics/  : 핵심 질문 중심의 전략 에세이

2차 정리 대상
- concepts/  : Docs와 Topics에서 반복 등장하는 핵심 개념
- companies/ : Docs와 Topics에서 역할이 확인된 LG 계열사·외부 파트너
- sources/   : Docs와 Topics에서 사용된 원문·보도·리포트
- assets/    : Docs와 Topics에 삽입된 원본 이미지의 로컬 저장본. 모든 이미지는 assets/images/ 단일 폴더에 저장
- data/      : Entity 탐색과 검증을 위한 구조화 데이터
```

Codex는 새 내용을 임의로 과도하게 생성하지 않는다.  
먼저 GPT-5.5에서 작성된 `docs/`와 `topics/`를 기준으로 삼고, 그 두 Entity에서 concepts, companies, sources를 추출·정리한다.

---

## 1. 최종 작업 순서

이전 계획의 불필요한 중간 단계를 제거하고, 최종 실행 순서를 아래와 같이 통일한다.

```text
Step 1. Repository 기본 구조 생성
Step 2. Docs 01~06 배치
Step 3. Topics 01~18 배치
Step 4. Docs/Topics 이미지 다운로드 및 로컬 경로 교체
Step 5. Docs/Topics 기반 Concepts 생성
Step 6. Docs/Topics 기반 Companies 생성
Step 7. Docs/Topics 기반 Sources 생성
Step 8. Index / Matrix / Data JSON 생성
Step 9. Link / ID / Image 검증
Step 10. README 및 Overview 정리
```

핵심 원칙은 다음이다.

```text
Docs + Topics = 원본 지식의 중심
Concepts + Companies + Sources = Docs와 Topics를 기반으로 사후 정리
```

---

## 2. 입력 파일

Codex는 아래 파일들을 기준으로 작업한다.

```text
# Seed
lg_group_ai_business_opportunities_6themes_final2.md

# Docs
01_ai_data_center_infra.md
02_physical_ai_smart_manufacturing.md
03_ai_mobility_sdv_aidv.md
04_enterprise_ax_agentic_operating_model.md
05_ai_for_science_bio_materials_battery.md
06_global_ai_alliance_open_innovation.md

# Docs image scripts
download_ai_data_center_infra_images.py
download_physical_ai_smart_manufacturing_images.py
download_ai_mobility_sdv_aidv_images.py
download_enterprise_ax_agentic_operating_model_images.py
download_ai_for_science_bio_materials_battery_images.py
download_global_ai_alliance_open_innovation_images.py

# Planning
topics_entity_plan_v2_18topics.md
concept_taxonomy_and_core_definitions.md
wiki-generation_final_flat_images.md
```

Topic 문서가 GPT-5.5에서 추가 작성될 때마다 Codex는 아래 파일들을 추가 입력으로 본다.

```text
topics/01_what_did_jensen_huang_leave_lg.md
scripts/download_topic_01_images.py
topics/02_how_competitive_is_exaone_globally.md
scripts/download_topic_02_images.py
...
```

---

## 3. 핵심 분류 규칙

가장 중요한 분류 규칙은 다음이다.

```text
Theme 1 = AI Data Center / Infra
Theme 2 = Physical AI / Smart Manufacturing
AI Factory = Theme 2의 하위 Concept
```

Codex는 아래 규칙을 반드시 지킨다.

```text
1. docs/01 파일명은 01_ai_data_center_infra.md 이다.
2. docs/01의 theme_id는 ai_data_center_infra 이다.
3. ai_infra_factory 라는 구 ID를 사용하지 않는다.
4. AI Factory는 docs/01의 제목이나 theme_id로 사용하지 않는다.
5. AI Factory는 concepts/ai-factory.md 로 생성한다.
6. AI Factory의 primary_theme은 physical_ai_smart_manufacturing 이다.
7. docs/01에서는 AI Factory를 “AI 데이터센터 인프라 위에서 작동하는 Physical AI 운영 모델”로만 연결한다.
8. docs/02에서는 AI Factory를 핵심 하위 Concept으로 설명한다.
9. docs/06과 topics에서는 NVIDIA 협력 관점에서 AI Factory를 다룰 수 있으나, primary link는 Theme 2로 둔다.
```

---

## 4. 최종 폴더 구조

```text
lg-ai-strategy-wiki/
  README.md

  docs/
    00_overview.md
    01_ai_data_center_infra.md
    02_physical_ai_smart_manufacturing.md
    03_ai_mobility_sdv_aidv.md
    04_enterprise_ax_agentic_operating_model.md
    05_ai_for_science_bio_materials_battery.md
    06_global_ai_alliance_open_innovation.md
    80_theme_company_matrix.md
    81_concept_theme_map.md
    82_partner_map.md
    83_source_coverage.md
    84_concept_index.md
    85_topic_index.md
    90_research_questions.md

  topics/
    00_topic_index.md
    01_what_did_jensen_huang_leave_lg.md
    02_how_competitive_is_exaone_globally.md
    03_ai_infra_demand_next_5_years.md
    04_is_ai_factory_a_data_center_or_operating_model.md
    05_what_did_palantir_ask_lg.md
    06_can_lg_win_ai_mobility_without_making_cars.md
    07_is_physical_ai_more_than_smart_factory_rebranding.md
    08_can_battery_software_become_lges_next_platform.md
    09_is_lg_ai_alliance_an_option_strategy_or_dependency_risk.md
    10_can_ai_for_science_change_lg_rnd_productivity.md
    11_what_is_one_lg_in_the_ai_age.md
    12_where_is_lg_real_ai_moat.md
    13_will_power_and_cooling_become_lges_next_growth_axis.md
    14_should_lg_build_or_buy_ai_foundation_models.md
    15_what_should_lg_measure_in_enterprise_ax.md
    16_how_should_lg_turn_manufacturing_data_into_ai_products.md
    17_can_korean_ai_sovereignty_become_lg_opportunity.md
    18_what_happens_if_gpu_cloud_prices_fall.md

  concepts/
    # generated from docs/ and topics/

  companies/
    # generated from docs/ and topics/
    partners/

  sources/
    # generated from docs/ and topics/

  scripts/
    download_ai_data_center_infra_images.py
    download_physical_ai_smart_manufacturing_images.py
    download_ai_mobility_sdv_aidv_images.py
    download_enterprise_ax_agentic_operating_model_images.py
    download_ai_for_science_bio_materials_battery_images.py
    download_global_ai_alliance_open_innovation_images.py
    download_topic_01_images.py
    download_topic_02_images.py
    ...

  assets/
    images/
      # flat image store
      # docs/topics/concepts/companies 하위 폴더를 만들지 않음
      # 파일명 prefix와 data/image_inventory.json으로 출처와 사용처 관리

  data/
    concepts.json
    companies.json
    sources.json
    topics.json
    theme_company_matrix.json
    image_inventory.json

  _templates/
    template_doc.md
    template_topic.md
    template_concept.md
    template_company.md
    template_source.md
```

---

## 5. Step 1 — Repository 기본 구조 생성

### 작업

1. 최종 폴더 구조를 생성한다.
2. `_templates/` 파일을 생성한다.
3. README.md를 생성한다.
4. docs/00_overview.md를 생성한다.

### README 핵심 설명

```markdown
# LG Group AI Strategy Wiki

이 Wiki는 공개 출처 기반으로 LG그룹의 AI 시대 사업기회와 전략 질문을 정리한다.

## Entity Structure

- `docs/`: 6대 AI 사업기회 테마 문서
- `topics/`: 핵심 질문 중심의 전략 에세이
- `concepts/`: Docs와 Topics에서 반복 등장하는 핵심 개념 정의
- `companies/`: Docs와 Topics에서 확인된 LG 계열사 및 외부 파트너 역할
- `sources/`: Docs와 Topics에서 사용된 원문·보도·리포트 source card
- `assets/`: 원본 소스 이미지 다운로드 결과
- `data/`: Wiki 탐색과 검증을 위한 구조화 데이터

## Important Classification

이 Wiki에서는 `AI Factory`를 독립 테마로 보지 않는다.

`AI Data Center / Infra`는 GPU, 데이터센터, 냉각, 전력, ESS, DC Grid, 클라우드 운영을 포함하는 물리적·연산 인프라 테마다.

`AI Factory`는 이 인프라 위에서 제조 데이터, 로봇, 디지털트윈, 합성데이터, 시뮬레이션을 연결해 Physical AI를 학습·검증·배포하는 운영 모델이다. 따라서 `AI Factory`는 `Physical AI / Smart Manufacturing` 테마의 핵심 Concept으로 관리한다.
```

---

## 6. Step 2 — Docs 01~06 배치

### 작업

아래 파일을 `docs/`에 배치한다.

```text
01_ai_data_center_infra.md
02_physical_ai_smart_manufacturing.md
03_ai_mobility_sdv_aidv.md
04_enterprise_ax_agentic_operating_model.md
05_ai_for_science_bio_materials_battery.md
06_global_ai_alliance_open_innovation.md
```

### 원칙

```text
1. 파일명과 frontmatter를 유지한다.
2. Appendix A, B, C를 유지한다.
3. 원본 이미지 URL을 삭제하지 않는다.
4. 이미지 URL 확보 필요 표시를 삭제하지 않는다.
5. docs 본문과 Appendix C Source Notes는 이후 concepts, companies, sources 생성의 기준으로 사용한다.
```

---

## 7. Step 3 — Topics 01~18 배치

### 작업

1. `topics/` 폴더를 생성한다.
2. `topics/00_topic_index.md`를 생성한다.
3. GPT-5.5에서 작성한 Topic MD를 순차적으로 `topics/`에 배치한다.
4. 아직 작성되지 않은 Topic은 skeleton만 생성한다.
5. `topics_entity_plan_v2_18topics.md`의 18개 목록만 사용한다.

### 최종 Topic 목록

```text
01. 젠슨 황이 LG에게 남긴 것은?
02. EXAONE의 글로벌 AI 플랫폼 대비 객관적 경쟁력은?
03. AI Infra 수요에 대한 향후 5년의 전망은?
04. AI Factory는 데이터센터인가 제조 운영 모델인가?
05. Palantir가 LG에 던진 진짜 질문은?
06. LG는 완성차를 만들지 않으면서 AI Mobility에서 무엇을 장악할 수 있는가?
07. Physical AI는 스마트팩토리의 재포장인가?
08. 배터리 SW는 LG에너지솔루션의 다음 플랫폼이 될 수 있는가?
09. LG의 글로벌 AI Alliance는 옵션 전략인가 종속 리스크인가?
10. AI for Science는 LG R&D 생산성을 얼마나 바꿀 수 있는가?
11. AI 시대의 One LG는 실제 시너지가 될 수 있는가?
12. LG의 진짜 AI Moat는 모델인가, 데이터인가, 물리 세계 자산인가?
13. 전력·냉각 병목은 LG전자와 LG에너지솔루션의 새 성장축인가?
14. LG는 foundation model을 직접 키워야 하는가, 산업 특화 모델에 집중해야 하는가?
15. Enterprise AX의 성과는 무엇으로 측정해야 하는가?
16. 제조 데이터는 어떻게 AI 제품이 되는가?
17. 한국형 AI Sovereignty는 LG에게 기회인가 부담인가?
18. GPU Cloud 가격이 하락하면 AIDC 사업성은 어떻게 변하는가?
```

### 삭제 Topic

아래 Topic은 생성하지 않는다.

```text
19. AI Agent가 조직을 바꾸는가, 보고서를 빠르게 만드는가?
20. LG AI Home과 산업 AI 전략은 만날 수 있는가?
```

### Topic 작성 운영 방식

```text
Pilot
- 01번 단독 작성

이후
- 2개씩 작성하는 것을 기본으로 한다.
- 최대 3개까지 가능하지만 이미지 검증과 해석 품질을 고려하면 2개가 최적이다.
```

---

## 8. Step 4 — 이미지 다운로드 및 로컬 경로 교체

### 핵심 원칙

Docs와 Topics의 이미지는 작성 시점에는 원본 URL로 삽입되어 있다.  
Codex는 각 이미지 다운로드 스크립트를 실행하여 가능한 이미지는 로컬에 저장하고, Markdown 본문의 이미지 경로를 로컬 경로로 교체한다.

이미지는 Entity별 하위 폴더를 나누지 않고 **모두 `assets/images/` 단일 폴더에 저장한다.**  
이유는 `docs`, `topics`에서 수집한 이미지를 나중에 `concepts`, `companies`, `sources`에서도 재사용할 수 있도록 하기 위함이다.

단, 다운로드에 실패한 이미지는 원격 URL을 그대로 유지한다.

```text
다운로드 성공:
원격 URL → 로컬 경로로 교체

다운로드 실패:
원격 URL 유지
manifest에 실패 사유 기록

IMAGE_URL_NEEDED:
다운로드 대상에서 제외
본문의 이미지 URL 확보 필요 표시 유지
```

### 파일명 규칙

`assets/images/`를 단일 폴더로 사용하므로 파일명 충돌을 반드시 방지한다.

```text
1. 로컬 파일명은 image_id 기반으로 생성한다.
2. image_id가 없으면 문서 prefix와 원본 파일명을 조합한다.
3. 동일 파일명이 이미 존재하면 덮어쓰지 않고 suffix를 붙인다.
...
```

예:

```text
assets/images/lge_dcw_direct_to_chip.png
assets/images/lg_nvidia_map_koo_huang.jpg
assets/images/company_nvidia_logo.png
assets/images/concept_ai_factory_reference.png
```

같은 원본 이미지가 여러 Entity에서 사용될 수 있으므로, `data/image_inventory.json`에는 `used_by` 배열을 둔다.

```json
{
  "image_id": "lg_nvidia_map_koo_huang",
  "original_url": "https://...",
  "local_path": "assets/images/topic_01_lg_nvidia_map_koo_huang.jpg",
  "status": "downloaded",
  "used_by": [
    "topics/01_what_did_jensen_huang_leave_lg.md",
    "companies/partners/nvidia.md",
    "concepts/global-ai-alliance.md"
  ]
}
```

### Docs 이미지 스크립트

아래 스크립트를 `scripts/`에 배치하고 output path를 통일한다.

```text
scripts/download_ai_data_center_infra_images.py
scripts/download_physical_ai_smart_manufacturing_images.py
scripts/download_ai_mobility_sdv_aidv_images.py
scripts/download_enterprise_ax_agentic_operating_model_images.py
scripts/download_ai_for_science_bio_materials_battery_images.py
scripts/download_global_ai_alliance_open_innovation_images.py
```

Output path:

```text
assets/images/
```

주의: `assets/images/` 아래에는 docs/topics/concepts/companies 하위 폴더를 만들지 않는다.  
모든 이미지는 단일 폴더에 두고, 파일명 prefix와 `image_inventory.json`으로 출처와 사용처를 관리한다.

### Topics 이미지 스크립트

Topic별 이미지 다운로드 스크립트는 아래 형식으로 둔다.

```text
scripts/download_topic_01_images.py
scripts/download_topic_02_images.py
...
```

Output path:

```text
assets/images/
```

주의: Topic 이미지도 별도 하위 폴더를 만들지 않고 `assets/images/`에 직접 저장한다.  
파일명은 `topic_01_`, `topic_02_` 같은 prefix를 붙여 docs 이미지와 충돌하지 않도록 한다.

### 이미지 처리 절차

```text
1. docs와 topics에서 image_url 목록을 수집한다.
2. 각 문서별 download script를 실행한다.
3. 성공한 이미지는 모두 assets/images/ 단일 폴더에 저장한다.
4. 파일명은 image_id 기반으로 만들고, 충돌 시 suffix를 붙인다.
5. 문서별 manifest는 scripts 실행 결과로 남기되, 최종 통합본은 data/image_inventory.json으로 생성한다.
6. 성공 항목은 Markdown 본문의 <img src="원격 URL">을 로컬 경로로 교체한다.
7. 실패 항목은 원격 URL을 유지한다.
8. IMAGE_URL_NEEDED 항목은 그대로 둔다.
9. data/image_inventory.json에 original_url, local_path, status, error, used_by를 모두 기록한다.
10. concepts, companies, sources에서 같은 이미지를 재사용할 경우 새로 다운로드하지 말고 image_inventory.json의 local_path를 참조한다.
```

### 금지

```text
1. 새 이미지, SVG, 인포그래픽을 생성하지 않는다.
2. 원본 출처가 없는 이미지를 추가하지 않는다.
3. 실패한 원격 URL을 임의로 삭제하지 않는다.
4. IMAGE_URL_NEEDED 표시를 삭제하지 않는다.
```

---

## 9. Step 5 — Docs/Topics 기반 Concepts 생성

### 입력

```text
docs/01~06
topics/01~18
concept_taxonomy_and_core_definitions.md
```

### 작업

1. `concepts/` 폴더를 생성한다.
2. docs와 topics의 frontmatter, wikilink, 본문에서 반복 등장하는 핵심 개념을 추출한다.
3. `concept_taxonomy_and_core_definitions.md`를 기준으로 Concept 목록과 정의를 보정한다.
4. 핵심 10개 Concept는 계획 문서의 정의를 우선 반영한다.
5. 나머지 Concept는 docs와 topics에 등장한 맥락을 기준으로 초안을 작성한다.

### 핵심 10개 Concept

```text
ai-data-center
ai-factory
physical-ai
smart-manufacturing
sdv
aidv
enterprise-ontology
agentic-operating-model
ai-co-scientist
global-ai-alliance
```

### Concept frontmatter 필수 필드

```yaml
---
id: concept_[id]
type: concept
title: [title]
aliases:
  - [alias]
primary_theme: [theme_id]
related_themes:
  - [theme_id]
related_companies:
  - [company_id]
source_ids:
  - [source_id]
tags:
  - [tag]
---
```

### 검증

```text
1. 모든 concept 파일에 primary_theme이 있는가?
2. AI Factory의 primary_theme이 physical_ai_smart_manufacturing 인가?
3. AI Data Center의 primary_theme이 ai_data_center_infra 인가?
4. docs/와 topics/의 related_concepts가 concepts/ 파일과 일치하는가?
5. ai_infra_factory 구 ID가 남아 있지 않은가?
6. source_ids가 없는 경우 source_ids: []로 두고 본문에 Source 보강 필요라고 표시했는가?
```

---

## 10. Step 6 — Docs/Topics 기반 Companies 생성

### 입력

```text
docs/01~06
topics/01~18
```

### 작업

`companies/`와 `companies/partners/`를 생성한다.

### LG 계열사

```text
lg-corp
lg-ai-research
lg-uplus
lg-cns
lg-electronics
lg-energy-solution
lg-display
lg-innotek
lg-chem
lg-household-health-care
lg-technology-ventures
```

### 외부 파트너

```text
nvidia
skild-ai
palantir
qualcomm
sdverse
dd-pharmatech
sinar-mas-group
```

### Company 문서 구조

```markdown
---
id: company_[id]
type: company
title: [Company Name]
category: lg_affiliate | partner
related_themes:
  - [theme_id]
related_topics:
  - [topic_id]
related_concepts:
  - [concept_id]
source_ids:
  - [source_id]
tags:
  - [tag]
---

# [Company Name]

## 1. Role Summary

## 2. Theme Participation

| Theme | Role | Evidence |
|---|---|---|

## 3. Topic Participation

| Topic | Why It Matters |
|---|---|

## 4. Key Assets

## 5. Related Concepts

## 6. Related Sources

## 7. Open Questions
```

### 원칙

```text
1. 회사 소개를 길게 쓰지 않는다.
2. 이 Wiki에서의 전략적 역할만 쓴다.
3. 직접 근거가 약한 역할은 검증 필요 표시를 한다.
4. 계열사별 역할은 docs/01~06의 계열사별 역할 표를 우선 반영한다.
5. topics에서 추가된 전략적 해석은 Topic Participation에 반영한다.
```

---

## 11. Step 7 — Docs/Topics 기반 Sources 생성

### 입력

```text
docs/01~06 Appendix C Source Notes
topics/01~18 Appendix B Source Notes
docs/topics frontmatter source_ids
```

### 작업

1. `sources/` 폴더를 생성한다.
2. docs와 topics의 Source Notes를 기준으로 source card를 만든다.
3. source_id와 파일명을 일관되게 정리한다.
4. 각 source에는 원문 URL, publisher, published date, key facts, related themes, related topics, related concepts, related companies를 넣는다.

### Source 문서 구조

```markdown
---
id: src_[source_id]
type: source
title: [Source Title]
publisher: [Publisher]
published: [YYYY-MM-DD or unknown]
url: [URL]
related_themes:
  - [theme_id]
related_topics:
  - [topic_id]
related_concepts:
  - [concept_id]
related_companies:
  - [company_id]
tags:
  - [tag]
---

# [Source Title]

## 1. Source Summary

## 2. Key Facts

- ...

## 3. Used In

| Entity | Usage |
|---|---|

## 4. Image Notes

| image_id | original_url | local_path | status | used_by | note |
|---|---|---|---|---|---|

## 5. Reliability Notes
```

### 원칙

```text
1. Source는 원문 자체의 요약이다.
2. 전략 해석은 docs 또는 topics에 둔다.
3. source card에는 과도한 해석을 넣지 않는다.
4. 원문 이미지 정보가 있는 경우 Image Notes에 기록한다.
5. 이미지 다운로드 성공 여부, 로컬 경로, 재사용 Entity 목록을 기록한다.
```

---

## 12. Step 8 — Index / Matrix / Data JSON 생성

### 생성할 index 문서

```text
docs/80_theme_company_matrix.md
docs/81_concept_theme_map.md
docs/82_partner_map.md
docs/83_source_coverage.md
docs/84_concept_index.md
docs/85_topic_index.md
docs/90_research_questions.md
```

### 생성할 data JSON

```text
data/concepts.json
data/companies.json
data/sources.json
data/topics.json
data/theme_company_matrix.json
data/image_inventory.json
```

### data/topics.json 예시

```json
{
  "topics": [
    {
      "id": "topic_what_did_jensen_huang_leave_lg",
      "title": "젠슨 황이 LG에게 남긴 것은?",
      "question": "NVIDIA 협력은 LG에게 GPU 확보 이상의 무엇을 남겼는가?",
      "related_themes": [
        "ai_data_center_infra",
        "physical_ai_smart_manufacturing",
        "ai_mobility_sdv_aidv",
        "global_ai_alliance_open_innovation"
      ],
      "related_concepts": [
        "global-ai-alliance",
        "ai-data-center",
        "ai-factory",
        "physical-ai",
        "aidv"
      ],
      "related_companies": [
        "lg-corp",
        "lg-electronics",
        "lg-uplus",
        "lg-cns",
        "lg-energy-solution",
        "lg-innotek",
        "lg-ai-research",
        "nvidia"
      ],
      "source_ids": [
        "src_lg_nvidia_map_20260608",
        "src_nvidia_lg_ai_factory_20260607"
      ]
    }
  ]
}
```

---

## 13. Step 9 — Link / ID / Image 검증

Codex는 다음을 검사한다.

### Link 검증

```text
1. [[docs/...]] 링크 대상 파일 존재 여부
2. [[topics/...]] 링크 대상 파일 존재 여부
3. [[concepts/...]] 링크 대상 파일 존재 여부
4. [[companies/...]] 링크 대상 파일 존재 여부
5. [[companies/partners/...]] 링크 대상 파일 존재 여부
6. [[sources/...]] 링크 대상 파일 존재 여부
```

### ID 검증

```text
1. frontmatter의 related_* 값과 실제 파일명 일치 여부
2. source_ids가 sources/의 id와 일치하는지 여부
3. concept IDs와 파일명 일치 여부
4. company IDs와 파일명 일치 여부
5. topic IDs와 파일명 일치 여부
6. ai_infra_factory 구 ID가 repo 전체에 남아 있지 않은지 여부
```

### Image 검증

```text
1. 모든 docs/topics 이미지가 image_inventory.json에 기록되어 있는가?
2. 다운로드 성공 이미지는 assets/images/ 단일 폴더에 저장되었는가?
3. 다운로드 성공 이미지는 Markdown에서 로컬 경로로 교체되었는가?
4. 다운로드 실패 이미지는 원격 URL을 유지하는가?
5. IMAGE_URL_NEEDED 항목은 그대로 유지되는가?
6. local_path가 존재하는가?
7. broken local image path가 없는가?
8. 동일한 이미지가 concepts/companies/sources에서 재사용될 경우 used_by에 반영되어 있는가?
```

---

## 14. Step 10 — README 및 Overview 정리

### README에 포함할 내용

```text
1. Wiki 목적
2. Entity 구조
3. Docs와 Topics가 핵심 작성물이라는 점
4. Concepts/Companies/Sources는 Docs와 Topics를 바탕으로 정리된다는 점
5. AI Factory 분류 원칙
6. 이미지 운영 원칙: 모든 이미지는 `assets/images/` 단일 폴더에 저장하고, 재사용은 `data/image_inventory.json`의 `used_by`로 관리한다.
```

### docs/00_overview.md에 포함할 내용

```text
1. 6대 Theme 요약
2. 18개 Topic 요약
3. Entity 간 관계
4. 전체 Navigation
```

---

## 15. 금지 사항

Codex는 다음을 하지 않는다.

```text
1. AI Factory를 Theme 1으로 되돌리지 않는다.
2. ai_infra_factory 구 ID를 되살리지 않는다.
3. 원본 이미지가 아닌 새 이미지나 SVG를 생성하지 않는다.
4. 출처 없는 수치를 단정적으로 추가하지 않는다.
5. GPT-5.5가 작성한 docs나 topics 본문을 임의로 대폭 축약하지 않는다.
6. IMAGE_URL_NEEDED 항목을 삭제하지 않는다.
7. 19번, 20번 Topic을 생성하지 않는다.
8. Palantir를 Theme 4의 목적 자체로 쓰지 않는다. Palantir는 ontology/AX 벤치마크와 파트너로만 다룬다.
9. NVIDIA를 모든 Theme의 주체로 쓰지 않는다. LG 계열사 자산을 우선 설명하고 NVIDIA는 enabling partner로 둔다.
10. 이미지 다운로드 실패를 이유로 원격 URL을 삭제하지 않는다.
```

---

## 16. 최종 검증 체크리스트

### 구조

```text
- [ ] README.md 존재
- [ ] docs/00_overview.md 존재
- [ ] docs/01~06 존재
- [ ] topics/00_topic_index.md 존재
- [ ] topics/01~18 존재 또는 skeleton 존재
- [ ] concepts/ 존재
- [ ] companies/ 존재
- [ ] companies/partners/ 존재
- [ ] sources/ 존재
- [ ] scripts/ 존재
- [ ] assets/images/ 존재
- [ ] assets/images/ 존재
- [ ] assets/images/ 아래에 Entity별 하위 폴더가 생성되지 않았는가?
- [ ] data/ 존재
```

### Docs

```text
- [ ] docs/01 파일명이 01_ai_data_center_infra.md인가?
- [ ] docs/01 theme_id가 ai_data_center_infra인가?
- [ ] docs/02에 ai-factory가 related_concepts로 들어가 있는가?
- [ ] docs/06에서 NVIDIA 협력이 1,2,3,6 테마와 연결되어 있는가?
```

### Topics

```text
- [ ] Topic 파일이 18개인가?
- [ ] 19번, 20번 Topic 파일이 없는가?
- [ ] 모든 Topic에 question이 있는가?
- [ ] 모든 Topic에 short_answer가 있는가?
- [ ] 모든 Topic에 image_policy가 있는가?
- [ ] 모든 Topic에 Image Inventory가 있는가?
```

### Concepts

```text
- [ ] ai-data-center.md 존재
- [ ] ai-factory.md 존재
- [ ] ai-factory primary_theme = physical_ai_smart_manufacturing
- [ ] enterprise-ontology.md 존재
- [ ] agentic-operating-model.md 존재
- [ ] global-ai-alliance.md 존재
```

### Images

```text
- [ ] docs 01~06 이미지 다운로드 스크립트가 scripts/에 있는가?
- [ ] topic별 이미지 다운로드 스크립트가 scripts/에 있는가?
- [ ] 성공한 이미지는 assets/images/ 단일 폴더에 저장되었는가?
- [ ] assets/images/ 아래에 docs/topics/concepts/companies 같은 하위 폴더가 생성되지 않았는가?
- [ ] 로컬 이미지 파일명이 충돌하지 않도록 image_id 또는 prefix 기반으로 생성되었는가?
- [ ] 성공한 이미지는 Markdown에서 로컬 경로로 교체되었는가?
- [ ] 실패한 이미지는 원격 URL을 유지하는가?
- [ ] IMAGE_URL_NEEDED 항목은 다운로드 대상에서 제외되어 있는가?
- [ ] image_inventory.json에 original_url, local_path, status, error, used_by가 기록되어 있는가?
```

### IDs

```text
- [ ] ai_infra_factory 구 ID가 repo 전체에 없는가?
- [ ] Theme ID가 6개로 통일되어 있는가?
- [ ] source_ids와 sources/ id가 일치하는가?
- [ ] concept IDs와 파일명이 일치하는가?
- [ ] company IDs와 파일명이 일치하는가?
- [ ] topic IDs와 파일명이 일치하는가?
```

---
## 17. 최종 원칙

이 Wiki의 목적은 LG그룹 AI 사업기회를 단순 홍보자료처럼 정리하는 것이 아니다.  
공개 출처를 기반으로 아래 세 가지를 동시에 축적하는 것이다.

```text
1. 사업기회
2. 개념 체계
3. 전략 질문
```

따라서 Codex는 문서를 “많이 만드는 것”보다 다음을 우선한다.

```text
- Docs와 Topics의 해석 품질
- 개념 경계의 명확성
- source 기반의 근거성
- entity 간 link 정합성
- 이미지 출처와 `assets/images/` 단일 폴더 기반 로컬 저장 관리
- AI Factory / AI Data Center 분류 일관성
```
