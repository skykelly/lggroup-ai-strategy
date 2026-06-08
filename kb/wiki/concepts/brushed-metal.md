---
concept_id: brushed-metal
canonical_name: Brushed Metal
korean_name: 브러시드 메탈
concept_type: material_cmf
concept_status: supporting
parent_concept: metal-finish
aliases:
- 헤어라인 메탈
- 브러시드 스틸
- 무광 메탈
related_concepts:
- natural-luxury
- quiet-premium
- material-storytelling
- tactile-materiality
contrasted_concepts:
- mirror-polished-metal
- high-gloss-chrome
applicable_spaces:
- kitchen
- bathroom
- living_room
- dining_room
related_product_groups:
- finish_material
- furniture
- lighting
- appliance
- decor
related_audiences:
- brand
- md
- marketer
region_context:
- korea
time_context:
  first_observed: long-term
  active_period: 2022-2026
  lifecycle: growing
source_evidence:
  document_count: 3
  source_count: 3
  evidence_files:
  - search-keyword-matrix.json
  - concept/natural-luxury.md
  - concept/tactile-materiality.md
confidence:
  score: 70
  level: medium
review:
  owner: null
  last_reviewed_at: '2026-06-09'
  review_status: batch_07_reviewed
---

# 브러시드 메탈 (Brushed Metal)

## 1. Concept 정의

### 한 줄 정의

금속 표면에 미세한 방향성 결을 만들어 광택을 낮추고 촉각적 깊이와 절제된 고급감을 부여하는 Supporting Material Concept.

### 확장 정의

Brushed Metal은 스테인리스·알루미늄·황동 등의 표면을 일정 방향으로 연마해 미세한 헤어라인과 확산 반사를 만드는 마감 방식이다. 거울처럼 강하게 반사하지 않아 주방·욕실·조명·가구 디테일에 조용한 프리미엄을 더한다. 다만 수종이나 소재 자체가 아니라 finish treatment이므로, 독립 Style Concept가 아니라 CMF supporting element로 관리하는 것이 적절하다.

## 2. Concept 경계

### 포함되는 것

- 방향성 있는 미세한 헤어라인
- 낮은 광택과 확산 반사
- 스테인리스·알루미늄·황동 등 금속 기반
- 손잡이·조명·가전·가구 디테일
- 지문·스크래치·세척 특성 고려
- 주변 우드·스톤·패브릭과의 대비

### 포함되지 않는 것

- 거울처럼 반사되는 폴리시드 크롬
- 페인트로 금속 질감만 모방한 표면
- 방향성이 없는 일반 무광 도장
- 오염·스크래치 관리 정보 없이 고급감만 강조하는 표현

### 유사 Concept와의 차이

| 비교 Concept | 공통점 | 차이점 |
|---|---|---|
| Polished Metal | 금속성·프리미엄 | Polished는 반사와 화려함, Brushed는 절제와 방향성 질감이 중심이다. |
| Matte Metal | 낮은 광택 | Matte는 균일한 무광, Brushed는 실제 선형 결이 핵심이다. |
| Tactile Materiality | 질감·촉각 | 브러시드 메탈은 특정 finish이며 Tactile Materiality는 더 넓은 감각 전략이다. |
| Quiet Premium | 절제된 고급감 | Quiet Premium은 시장·브랜드 가치이고 Brushed Metal은 이를 구현하는 소재 요소다. |

## 3. 핵심 구성요소

| Dimension | Entities / Attributes | 필수성 |
|---|---|---|
| Base Metal | stainless steel, aluminum, brass | core |
| Finish | linear abrasion, hairline, satin-brushed | core |
| Gloss | low-to-medium diffuse reflection | core |
| Direction | vertical, horizontal, radial | core |
| Touch | fine texture, cool surface | supporting |
| Performance | fingerprint, scratch, corrosion, cleaning | core |
| Pairing | wood, stone, ceramic, glass | supporting |

## 4. 관계 구조

```text
Metal Finish
 └─ Brushed Metal
     ├─ Hairline Texture
     ├─ Diffuse Reflection
     ├─ Stainless / Aluminum / Brass
     ├─ Low-gloss Premium
     └─ Surface Maintenance
```

### 관계 Triple

```yaml
relations:
  - subject: brushed-metal
    predicate: is_a
    object: metal-finish
  - subject: brushed-metal
    predicate: supports_value
    object: quiet-premium
  - subject: brushed-metal
    predicate: used_by
    object: natural-luxury
  - subject: brushed-metal
    predicate: related_to
    object: tactile-materiality
  - subject: brushed-metal
    predicate: contrasts_with
    object: polished-metal
  - subject: brushed-metal
    predicate: communicated_by
    object: material-storytelling
```

## 5. 한국 시장 맥락

- 주방 가전·수전·손잡이·조명·욕실 하드웨어에서 적용 빈도가 높다.
- ‘헤어라인’, ‘무광’, ‘새틴’, ‘브러시드’가 혼용되어 실제 마감 차이를 설명해야 한다.
- 스테인리스는 지문과 미세 스크래치, 황동은 변색과 patina 관리가 중요하다.
- 우드·스톤과 조합하면 과시적이지 않은 프리미엄 이미지를 만들 수 있다.

## 6. 시간·트렌드 관찰

> Concept의 안정적 정의와 특정 시기의 Trend Observation을 분리한다.

| Period | Region | Trend state | Evidence | Note |
|---|---|---|---|---|
| 2015-2021 | Korea | stable | 주방·욕실 하드웨어 중심 | 기능성 마감 |
| 2022-2026 | Korea | growing | 내추럴 럭셔리·조용한 프리미엄 | 가구·조명 디테일로 확장 |

## 7. 브랜드·MD·마케팅 활용

### 브랜드

- 마감명을 통일하고 실제 표면의 방향성과 광택을 보여준다.
- 지문·세척·변색·스크래치 특성을 솔직하게 설명한다.
- 우드·스톤과의 조합으로 소재 스토리를 만든다.

### MD

- base metal과 finish를 분리 태깅한다.
- gloss_level, brush_direction, fingerprint_resistance, corrosion 정보를 관리한다.
- 주방·욕실·조명별 적용 이미지를 제공한다.

### 마케팅/콘텐츠

- 정의형: 브러시드 메탈이란 무엇인가
- 비교형: 브러시드와 폴리시드 메탈의 차이
- 관리형: 스테인리스 헤어라인 관리법
- 조합형: 우드와 브러시드 메탈을 함께 쓰는 법

## 8. 검색어 및 동의어

```yaml
primary_keywords:
  - 브러시드 메탈
  - 헤어라인 메탈
  - 무광 메탈
  - 브러시드 스틸
  - 새틴 메탈
secondary_keywords:
  - 스테인리스 인테리어
  - 황동 마감
  - 메탈 손잡이
  - 무광 수전
  - 메탈 조명
commercial_keywords:
  - 브러시드 수전
  - 헤어라인 손잡이
  - 스테인리스 조명
  - 브러시드 가전
  - 황동 하드웨어
negative_or_ambiguous_terms:
  - 무광 메탈
  - 스테인리스
  - 헤어라인
```

## 9. 대표 질문

- Brushed Metal은 Material Entity인가 Concept인가?
- Polished·Matte·Satin과 어떻게 구분하는가?
- 표면 관리 속성을 어떻게 지식화하는가?
- Quiet Premium과 어떤 관계를 갖는가?

## 10. 근거와 출처

| Source | Evidence summary | Supports | Confidence |
|---|---|---|---|
| search-keyword-matrix.json | 브러시드 메탈과 프리미엄 소재 키워드 | keyword/relation | medium |
| concept/natural-luxury.md | 소재 기반 고급감 | style relation | high |
| concept/tactile-materiality.md | 표면·촉각 관계 | material relation | high |

## 11. Concept Score

| 기준 | 배점 | 점수 | 근거 |
|---|---:|---:|---|
| 반복성 | 20 | 14 | 프리미엄 소재 문맥에서 반복 |
| 출처 다양성 | 20 | 12 | 검색·Concept 자료 |
| 의미 응집성 | 20 | 18 | finish 특성이 명확 |
| 구별성 | 15 | 8 | Material Entity 성격이 강함 |
| 실무 활용성 | 15 | 12 | 상품 태그·소재 설명에 유용 |
| 시간 지속성 | 10 | 6 | 장기 마감이나 최근 재부상 |
| **총점** | **100** | **70** | Supporting Concept 유지 |

## 12. 편집 및 검토 기록

- 생성일: 2026-06-09
- 마지막 검토일: 2026-06-09
- 변경 내용: Batch 7 기준으로 Material Supporting 및 Market Concept를 실제 샘플 수준으로 확장함.
- 미해결 이슈: 향후 material finish Entity로 통합할 가능성이 높음.
