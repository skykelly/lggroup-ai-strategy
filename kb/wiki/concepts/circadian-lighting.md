---
concept_id: circadian-lighting
canonical_name: Circadian Lighting
korean_name: 서커디언 조명
concept_type: functional
concept_status: canonical
parent_concept: wellness-lighting
aliases:
- 생체리듬 조명
- 시간대별 조명
- Human-centric Lighting
related_concepts:
- wellness-home
- sleep-wellness
- ai-smart-living
- invisible-technology
contrasted_concepts:
- static-lighting
- mood-lighting-only
applicable_spaces:
- bedroom
- living_room
- home_office
- bathroom
related_product_groups:
- lighting
- appliance
- smart_control
related_audiences:
- brand
- md
- marketer
region_context:
- korea
time_context:
  first_observed: 2010s
  active_period: 2022-2026
  lifecycle: growing
source_evidence:
  document_count: 3
  source_count: 3
  evidence_files:
  - concept/wellness-home.md
  - concept/sleep-wellness.md
  - search-keyword-matrix.json
confidence:
  score: 88
  level: high
review:
  owner: null
  last_reviewed_at: '2026-06-09'
  review_status: batch_06_reviewed
image_references:
- role: hero_candidate
  source: Unsplash
  url: https://unsplash.com/s/photos/circadian+lighting+bedroom+warm+evening+smart+light
  search_query: circadian lighting bedroom warm evening smart light
  alt_text_ko: 시간대에 따라 밝기와 색온도가 달라지는 침실·거실
- role: alternative_candidate
  source: Pexels
  url: https://www.pexels.com/search/circadian+lighting+bedroom+warm+evening+smart+light/
  search_query: circadian lighting bedroom warm evening smart light
  alt_text_ko: 시간대에 따라 밝기와 색온도가 달라지는 침실·거실
- role: reference_search
  source: Wikimedia Commons
  url: https://commons.wikimedia.org/w/index.php?search=circadian+lighting+bedroom+warm+evening+smart+light&title=Special:MediaSearch&type=image
  search_query: circadian lighting bedroom warm evening smart light
  alt_text_ko: 시간대에 따라 밝기와 색온도가 달라지는 침실·거실
image_status: search_links_added
image_updated_at: '2026-06-09'
existing_source_image_references:
- priority: 1
  source_id: housebeautiful_wellness
  source_title: House Beautiful — Invisible Wellness 2026
  source_type: global_editorial
  source_page_url: https://www.housebeautiful.com/design-inspiration/a70249325/next-big-wellness-trend-2026/
  image_use: 웰니스·수면·조명·자연 소재 사례
  usage_status: reference_url
  license_checked: false
- priority: 2
  source_id: ikea_life
  source_title: IKEA — Life at Home
  source_type: global_research
  source_page_url: https://lifeathome.ikea.com/
  image_use: 집에서의 행동·감정·소형 공간·생활 장면
  usage_status: reference_url
  license_checked: false
- priority: 3
  source_id: arxiv_smart_1
  source_title: arXiv — Smart/AI Space Research 2407.15956
  source_type: academic
  source_page_url: https://arxiv.org/abs/2407.15956
  image_use: AI·스마트 공간·시스템 구조 참고
  usage_status: reference_url
  license_checked: false
existing_source_image_status: source_page_urls_added
existing_source_image_updated_at: '2026-06-09'
---

# 서커디언 조명 (Circadian Lighting)

## 1. Concept 정의

### 한 줄 정의

시간대와 사용자의 활동에 따라 밝기와 색온도를 조절해 각성·집중·휴식·수면 전환을 지원하는 Functional Lighting Concept.

### 확장 정의

Circadian Lighting은 단순히 색이 바뀌는 스마트 조명이 아니다. 오전·주간에는 충분한 밝기와 비교적 높은 색온도, 저녁에는 낮은 조도와 따뜻한 빛을 제공해 사용자의 생체리듬과 활동 전환을 지원한다. 자연광과 인공광의 관계, 눈부심, 조도, 색온도, 자동화, 수동 제어, 공간별 활동이 함께 고려되어야 한다.

## 2. Concept 경계

### 포함되는 것

- 시간대별 밝기·색온도 변화
- 자연광과 인공광의 연계
- 기상·집중·휴식·수면 루틴
- 눈부심과 화면 반사 제어
- 자동 스케줄과 수동 오버라이드
- 공간별 활동에 맞춘 조명 장면

### 포함되지 않는 것

- 색상 변경 기능만 있는 RGB 조명
- 무드 연출만을 위한 저조도 조명
- 의학적 치료 효과를 단정하는 조명
- 사용자가 제어할 수 없는 자동화

### 유사 Concept와의 차이

| 비교 Concept | 공통점 | 차이점 |
|---|---|---|
| Mood Lighting | 분위기와 감정 조절 | Mood Lighting은 감성 중심이고 Circadian Lighting은 시간·활동 리듬이 중심이다. |
| Smart Lighting | 자동화·앱 제어 | Smart Lighting은 기술 범주이고 Circadian Lighting은 웰니스 목적의 조명 전략이다. |
| Sleep Wellness | 수면 루틴 지원 | Sleep Wellness는 전체 수면 환경이고 서커디언 조명은 그중 빛 요소다. |
| Task Lighting | 집중과 시야 확보 | Task Lighting은 특정 작업 조도, Circadian Lighting은 하루 전체의 빛 변화다. |

## 3. 핵심 구성요소

| Dimension | Entities / Attributes | 필수성 |
|---|---|---|
| Time | morning, daytime, evening, pre-sleep | core |
| Brightness | lux level, dimming curve | core |
| Color Temperature | cooler day, warmer evening | core |
| Light Distribution | ambient, task, indirect, glare control | core |
| Automation | schedule, sensor, adaptive control | supporting |
| User Control | manual override, preference | core |
| Space | bedroom, office, living room, bathroom | supporting |

## 4. 관계 구조

```text
Wellness Lighting
 └─ Circadian Lighting
     ├─ Morning Activation
     ├─ Daytime Focus
     ├─ Evening Wind-down
     ├─ Natural Light Integration
     └─ User Override
```

### 관계 Triple

```yaml
relations:
  - subject: circadian-lighting
    predicate: is_a
    object: wellness-lighting
  - subject: circadian-lighting
    predicate: supports_need
    object: sleep-wake-rhythm
  - subject: circadian-lighting
    predicate: supports_activity
    object: focus
  - subject: circadian-lighting
    predicate: uses_technology
    object: smart-lighting
  - subject: circadian-lighting
    predicate: related_to
    object: sleep-wellness
  - subject: circadian-lighting
    predicate: applied_to
    object: whole-home
```

## 5. 한국 시장 맥락

- 한국 아파트는 깊은 평면과 제한된 자연광으로 시간대별 조명 보완 필요성이 크다.
- 침실·거실·서재·욕실에서 서로 다른 조명 장면이 필요하다.
- 스마트 조명·TV·에어컨·커튼과 연동하면 AI Smart Living으로 확장 가능하다.
- 건강 효과를 단정하기보다 생활 리듬과 환경 지원 관점으로 표현해야 한다.

## 6. 시간·트렌드 관찰

> Concept의 안정적 정의와 특정 시기의 Trend Observation을 분리한다.

| Period | Region | Trend state | Evidence | Note |
|---|---|---|---|---|
| 2018-2022 | Korea | emerging | 스마트 조명과 수면 관심 증가 | 앱 제어 중심 |
| 2023-2026 | Korea | growing | wellness-home and sleep-wellness concepts | 시간·루틴 기반 조명으로 확장 |

## 7. 브랜드·MD·마케팅 활용

### 브랜드

- 색온도 변화 기능보다 하루 장면과 사용 루틴을 보여준다.
- 자동화와 수동 제어를 함께 제공해 신뢰를 높인다.
- 조명기구·스마트홈·수면 브랜드 간 협업이 가능하다.

### MD

- 기상·집중·저녁·수면 전 장면별 패키지를 구성한다.
- lux, CCT, dimming, glare, automation 정보를 상품 필드화한다.
- 공간별 권장 장면과 사용 시간을 콘텐츠에 포함한다.

### 마케팅/콘텐츠

- 정의형: 서커디언 조명이란 무엇인가
- 루틴형: 아침과 저녁 조명을 다르게 써야 하는 이유
- 비교형: 무드등과 서커디언 조명의 차이
- 체크리스트형: 침실 조명 설정 점검

## 8. 검색어 및 동의어

```yaml
primary_keywords:
  - 서커디언 조명
  - 생체리듬 조명
  - 수면 조명
  - 시간대별 조명
  - 스마트 조명
secondary_keywords:
  - 색온도 조절
  - 디밍 조명
  - 아침 조명
  - 저녁 조명
  - 간접 조명
commercial_keywords:
  - 스마트 전구
  - 디밍 조명
  - 침실 조명
  - 플로어 램프
  - 스마트 스위치
negative_or_ambiguous_terms:
  - 무드등
  - 힐링 조명
  - 스마트 조명
```

## 9. 대표 질문

- Circadian Lighting은 Smart Lighting과 무엇이 다른가?
- 공간별 조명 장면은 어떻게 정의하는가?
- 자연광과 인공광을 어떻게 연결하는가?
- 건강 효과를 과장하지 않고 어떤 언어를 써야 하는가?

## 10. 근거와 출처

| Source | Evidence summary | Supports | Confidence |
|---|---|---|---|
| concept/wellness-home.md | 웰니스 조명과 생활 리듬 | parent relation | high |
| concept/sleep-wellness.md | 수면 전·기상 조명 | application | high |
| search-keyword-matrix.json | 침실 조명·수면 키워드 | keyword | medium |

## 11. Concept Score

| 기준 | 배점 | 점수 | 근거 |
|---|---:|---:|---|
| 반복성 | 20 | 17 | 웰니스·수면·스마트홈에서 반복 |
| 출처 다양성 | 20 | 14 | Concept·검색 자료 |
| 의미 응집성 | 20 | 19 | 시간·조도·색온도가 일관 |
| 구별성 | 15 | 13 | 무드·스마트 조명과 구별 가능 |
| 실무 활용성 | 15 | 15 | 조명·스마트홈 활용 높음 |
| 시간 지속성 | 10 | 10 | 장기 성장 가능성 높음 |
| **총점** | **100** | **88** | Canonical 유지 |

## 12. 편집 및 검토 기록

- 생성일: 2026-06-09
- 마지막 검토일: 2026-06-09
- 변경 내용: Batch 6 기준으로 Material/CMF 및 기술 Concept를 실제 샘플 수준으로 확장함.
- 미해결 이슈: 의학적 기준이 아닌 생활용 권장 지표 범위를 별도 가이드로 정의해야 함.

## 13. 이미지 레퍼런스

> 아래 링크는 Concept에 맞는 대표 이미지를 선택하기 위한 검색 결과다. 최종 발행 전 이미지별 라이선스·저작자·상업적 이용 범위를 확인한다.

### 권장 대표 장면

- **이미지 설명/대체 텍스트:** 시간대에 따라 밝기와 색온도가 달라지는 침실·거실
- **권장 구도:** 16:9 lighting scene
- **검색 문구:** `circadian lighting bedroom warm evening smart light`

### 이미지 후보 링크

| 우선순위 | 출처 | 링크 | 활용 |
|---|---|---|---|
| 1 | Unsplash | [대표 이미지 후보 검색](https://unsplash.com/s/photos/circadian+lighting+bedroom+warm+evening+smart+light) | Hero 이미지 및 공간 전경 후보 |
| 2 | Pexels | [대체 이미지 후보 검색](https://www.pexels.com/search/circadian+lighting+bedroom+warm+evening+smart+light/) | 공간·제품 사용 장면 후보 |
| 3 | Wikimedia Commons | [라이선스 확인이 쉬운 후보 검색](https://commons.wikimedia.org/w/index.php?search=circadian+lighting+bedroom+warm+evening+smart+light&title=Special:MediaSearch&type=image) | 출처·라이선스가 명확한 이미지 후보 |
| 보조 | Bing Images | [추가 레퍼런스 검색](https://www.bing.com/images/search?q=circadian+lighting+bedroom+warm+evening+smart+light) | 시각 방향 탐색용이며 원출처를 다시 확인해야 함 |

### 선정 기준

- Concept의 핵심 속성이 한 장면에서 명확히 보여야 한다.
- 단순히 색상이 비슷한 이미지보다 **공간 구성·소재·행동·기능**이 Concept 정의와 일치해야 한다.
- 한국 아파트·원룸·생활 환경과 지나치게 동떨어진 대저택 이미지는 우선순위를 낮춘다.
- 최종 저장 시 `source_url`, `creator`, `license`, `downloaded_at`, `linked_concept`를 기록한다.

## 14. 기존 출처 기반 이미지 URL

> 이 섹션은 Concept 정의와 Wiki 작성에 실제로 참고한 기존 출처의 원문 URL을 우선순위별로 연결한다. 링크된 페이지 안의 공간·소재·가구·도식 이미지를 후보로 사용한다. 실제 이미지 파일을 발행물에 복제하기 전에는 개별 출처의 라이선스와 저작권을 확인한다.

| 우선순위 | 기존 출처 | 원문 URL | 적합한 이미지 역할 | 상태 |
|---:|---|---|---|---|
| 1 | House Beautiful — Invisible Wellness 2026 | [원문 이미지/사례 보기](https://www.housebeautiful.com/design-inspiration/a70249325/next-big-wellness-trend-2026/) | 웰니스·수면·조명·자연 소재 사례 | `reference_url` |
| 2 | IKEA — Life at Home | [원문 이미지/사례 보기](https://lifeathome.ikea.com/) | 집에서의 행동·감정·소형 공간·생활 장면 | `reference_url` |
| 3 | arXiv — Smart/AI Space Research 2407.15956 | [원문 이미지/사례 보기](https://arxiv.org/abs/2407.15956) | AI·스마트 공간·시스템 구조 참고 | `reference_url` |

### 적용 원칙

- 기존 출처의 이미지가 Concept 정의와 직접 일치하면 Unsplash·Pexels 후보보다 우선한다.
- 같은 원문 안에서도 공간 전경, 소재 디테일, 가구/상품 장면, 구조 도식 중 문서 목적에 맞는 이미지를 선택한다.
- 원문 페이지 URL은 `reference_url`로 관리하며, 직접 이미지 URL을 추출할 때는 `creator`, `license`, `original_page_url`을 함께 기록한다.
- 오늘의집·상업 매체·브랜드·트렌드 리서치의 이미지는 기본적으로 원문 링크 참조 상태로 둔다.
