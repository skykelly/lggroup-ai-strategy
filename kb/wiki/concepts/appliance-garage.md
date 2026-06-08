---
concept_id: appliance-garage
canonical_name: Appliance Garage
korean_name: 어플라이언스 가라지
concept_type: functional
concept_status: canonical
parent_concept: kitchen-storage
aliases:
- 소형가전 숨김장
- 가전 수납장
- Small-appliance Garage
related_concepts:
- hidden-storage
- open-kitchen
- kitchen-island
- ai-smart-living
contrasted_concepts:
- countertop-appliance-display
- sealed-appliance-cabinet
applicable_spaces:
- kitchen
related_product_groups:
- storage
- furniture
- appliance
- finish_material
related_audiences:
- brand
- md
- marketer
region_context:
- korea
time_context:
  first_observed: late-2010s
  active_period: 2022-2026
  lifecycle: growing
source_evidence:
  document_count: 3
  source_count: 3
  evidence_files:
  - space/kitchen-trend.md
  - concept/hidden-storage.md
  - search-keyword-matrix.json
confidence:
  score: 85
  level: high
review:
  owner: null
  last_reviewed_at: '2026-06-09'
  review_status: batch_05_reviewed
---

# 어플라이언스 가라지 (Appliance Garage)

## 1. Concept 정의

### 한 줄 정의

커피머신·토스터·밥솥 등 소형 주방가전을 전원과 함께 수납장 내부에 통합해 필요할 때 사용하고 평소에는 상판을 비우는 Functional Concept.

### 확장 정의

Appliance Garage는 소형 가전을 단순히 장 안에 넣는 수납이 아니다. 콘센트·환기·열·수증기·도어 간섭·슬라이딩 선반·청소·AS 접근성을 고려해 가전을 제자리에서 사용하거나 쉽게 꺼낼 수 있도록 설계한다. 대면형 오픈 키친처럼 주방이 거실에 노출될수록 시각적 정돈 효과가 크다.

## 2. Concept 경계

### 포함되는 것

- 소형가전 전용 수납 구획
- 내부 또는 인접 전원
- 열·증기·환기 조건
- 리프트·포켓·슬라이딩·플랩 도어
- 가전 사용 상태와 수납 상태의 전환
- 청소·배선·AS 접근성

### 포함되지 않는 것

- 콘센트·환기 없이 가전을 일반 장에 밀폐하는 방식
- 사용할 때마다 무거운 가전을 멀리 이동해야 하는 수납
- 문을 열면 통로와 작업대를 막는 구조
- 가전 크기 변화와 교체를 고려하지 않은 고정 구획

### 유사 Concept와의 차이

| 비교 Concept | 공통점 | 차이점 |
|---|---|---|
| Hidden Storage | 가전 은닉·시각적 정돈 | Appliance Garage는 주방 소형가전·전원·열 관리에 특화된 하위 Concept다. |
| Pantry | 식재료·주방 용품 수납 | 팬트리는 저장 범위가 넓고 가전 즉시 사용 기능은 필수가 아니다. |
| Built-in Appliance | 가전과 가구 통합 | 빌트인 가전은 설치형 대형 가전이고 Appliance Garage는 주로 소형 이동 가전이다. |
| Coffee Station | 커피 장면·도구 집합 | Coffee Station은 보여주는 연출도 가능하고 Appliance Garage는 은닉과 상판 비우기가 중심이다. |

## 3. 핵심 구성요소

| Dimension | Entities / Attributes | 필수성 |
|---|---|---|
| Appliance | coffee machine, toaster, rice cooker, blender, air fryer | core |
| Power | outlet, cable route, switch access | core |
| Ventilation | heat, steam, airflow clearance | core |
| Mechanism | pocket, tambour, flap, lift, sliding shelf | core |
| Dimension | appliance clearance, replacement tolerance | core |
| Workflow | use-in-place, pull-out, return, cleaning | core |
| Safety | heat-resistant finish, moisture, circuit load | core |

## 4. 관계 구조

```text
Kitchen Storage
 └─ Appliance Garage
     ├─ Hidden Storage
     ├─ Power Integration
     ├─ Ventilation
     ├─ Sliding Work Surface
     └─ Clear Countertop
```

### 관계 Triple

```yaml
relations:
  - subject: appliance-garage
    predicate: is_a
    object: kitchen-storage
  - subject: appliance-garage
    predicate: specializes
    object: hidden-storage
  - subject: appliance-garage
    predicate: contains
    object: small-appliance
  - subject: appliance-garage
    predicate: requires
    object: power-integration
  - subject: appliance-garage
    predicate: requires
    object: ventilation
  - subject: appliance-garage
    predicate: supports_need
    object: clear-countertop
```

## 5. 한국 시장 맥락

- 한국 주방에는 밥솥·정수기·커피머신·에어프라이어·전자레인지 등 소형·중형 가전 밀도가 높다.
- 밥솥 수증기와 에어프라이어 열 때문에 일반 외국 사례보다 환기와 인출 선반이 중요하다.
- 대면형 주방에서는 거실에서 보이는 상판을 비우는 효과가 크다.
- 가전 교체 주기가 가구보다 짧아 여유 치수와 조절 가능한 선반이 필요하다.

## 6. 시간·트렌드 관찰

> Concept의 안정적 정의와 특정 시기의 Trend Observation을 분리한다.

| Period | Region | Trend state | Evidence | Note |
|---|---|---|---|---|
| 2018-2021 | Korea | emerging | 밥솥장·키큰장 중심 | 개별 가전 수납 |
| 2022-2026 | Korea | growing | 오픈 키친·팬트리·상판 비우기 | 복수 가전 통합과 도어 메커니즘 고도화 |

## 7. 브랜드·MD·마케팅 활용

### 브랜드

- 예쁜 문보다 실제 가전 사용·열·수증기·청소 장면을 보여준다.
- 가전 브랜드와 가구·주방 시공 브랜드의 규격 연동이 가능하다.
- 가전 교체를 고려한 가변 선반·콘센트·환기 옵션을 강조한다.

### MD

- coffee, rice-cooker, breakfast, multi-appliance garage로 사용 장면을 나눈다.
- 가전별 최소 여유 치수·열·수증기·전력 정보를 제공한다.
- appliance_clearance, power_ready, ventilation_type, use_in_place 태그를 운영한다.

### 마케팅/콘텐츠

- 정의형: 어플라이언스 가라지란 무엇인가
- 체크리스트형: 밥솥과 에어프라이어를 장 안에 넣기 전 확인할 것
- 비교형: 팬트리와 가전 수납장의 차이
- 공간형: 주방 상판을 비우는 가전 수납

## 8. 검색어 및 동의어

```yaml
primary_keywords:
  - 어플라이언스 가라지
  - 소형가전 수납
  - 가전 수납장
  - 주방 상판 비우기
  - 밥솥장
secondary_keywords:
  - 커피머신 수납
  - 에어프라이어 수납
  - 키큰장
  - 포켓 도어
  - 인출 선반
commercial_keywords:
  - 가전 수납장
  - 밥솥장
  - 키큰장
  - 슬라이딩 선반
  - 포켓 도어장
negative_or_ambiguous_terms:
  - 가전장
  - 팬트리
  - 주방 수납
```

## 9. 대표 질문

- Appliance Garage와 일반 가전 수납장의 차이는 무엇인가?
- 가전별 환기·열·수증기 조건은 어떻게 관리하는가?
- 가전 교체를 고려한 치수 설계는 어떻게 하는가?
- 사용 상태와 수납 상태를 어떻게 전환하는가?

## 10. 근거와 출처

| Source | Evidence summary | Supports | Confidence |
|---|---|---|---|
| space/kitchen-trend.md | 가전 은닉·상판 비우기 | definition/application | high |
| concept/hidden-storage.md | 숨김 수납의 하위 개념 | parent relation | high |
| search-keyword-matrix.json | 어플라이언스 가라지·주방 키워드 | keyword | high |

## 11. Concept Score

| 기준 | 배점 | 점수 | 근거 |
|---|---:|---:|---|
| 반복성 | 20 | 17 | 주방·수납 문서에서 반복 |
| 출처 다양성 | 20 | 14 | 공간·Concept·검색 자료 |
| 의미 응집성 | 20 | 19 | 가전·전원·환기·도어가 일관 |
| 구별성 | 15 | 14 | 팬트리·빌트인과 구별 명확 |
| 실무 활용성 | 15 | 15 | 주방 시공·가전 판매 활용 높음 |
| 시간 지속성 | 10 | 6 | 최근 성장 Concept, 장기성 관찰 필요 |
| **총점** | **100** | **85** | Canonical 유지 |

## 12. 편집 및 검토 기록

- 생성일: 2026-06-09
- 마지막 검토일: 2026-06-09
- 변경 내용: Batch 5 기준으로 Functional Concept를 실제 샘플 수준으로 확장함.
- 미해결 이슈: 한국형 밥솥·에어프라이어 열/증기 규격 데이터를 보강해야 함.
