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
