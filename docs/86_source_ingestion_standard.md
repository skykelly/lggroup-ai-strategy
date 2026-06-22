---
id: source_ingestion_standard
type: guide
title: Source Ingestion Standard
baseline_date: 2026-06-21
tags:
  - source
  - ingestion
  - llm-wiki
  - provenance
---

# Source Ingestion Standard

## 1. 결론

이 Wiki의 Source 문서는 “원문 전체 한국어 번역”과 “한 줄 요약” 중 하나를 선택하면 안 된다.

권장 수준은 다음 세 계층을 함께 보존하는 **근거 중심 Source Record**다.

1. 원문을 다시 확인할 수 있는 provenance와 raw capture 정보
2. 원문 구조를 따라가는 충실한 한국어 번역 또는 상세 재서술
3. Docs·Topics·Concepts가 기계적으로 재사용할 수 있는 atomic claim

현재의 한 줄 요약은 검색용 description으로는 쓸 수 있지만, LLM이 새로운 문서를 만들거나 기존 판단을 갱신할 근거로는 부족하다.

## 2. 두 선택지의 평가

| 방식 | 장점 | 문제 | 권장 용도 |
|---|---|---|---|
| 원문 전체 한국어 번역 | 문맥과 세부사항을 많이 보존 | 번역 오류, 원문 위치 상실, 저작권, 갱신 비용, 표·이미지 손실 | 공개 라이선스·자체 자료·번역 허용 자료에 한정 |
| 한 줄 요약 | 빠르고 검색이 쉬움 | 근거·수치·조건·불확실성·문맥이 사라짐 | 검색 결과 preview에만 사용 |
| 구조화된 충실 기록 | 문맥, 검증성, 기계 활용성을 함께 확보 | 작성·수집 비용이 증가 | Wiki의 기본 Source 형식 |

## 3. 원문 전체 번역을 기본값으로 두지 않는 이유

원문 전체 번역은 원문의 대체물이 되기 쉽다. 하지만 LLM Wiki가 필요로 하는 것은 읽기 편한 대체 기사보다 “어떤 주체가 언제 무엇을 어떤 조건으로 말했다”는 추적 가능한 근거다.

전체 번역만 저장하면 다음 정보가 약해진다.

- 원문의 heading, page, paragraph, table과의 위치 대응
- 실적과 목표, 사실과 전망, 발표자 주장과 편집자 해석의 구분
- 수치의 단위, 기준일, 비교 기준
- 원문이 수정되었을 때 변경된 범위
- 하나의 Source가 여러 Entity에 제공한 서로 다른 claim

또한 저작권이 있는 기사·보고서의 전체 번역을 저장소에 복제하는 것은 피해야 한다. 전체 원문이나 전체 번역은 라이선스가 허용되거나 사용 권한이 있는 경우에만 저장한다.

## 4. 권장 Content Policy

각 Source는 frontmatter의 `content_policy`로 수집 수준을 명시한다.

| 값 | 사용 조건 | 저장 내용 |
|---|---|---|
| `full_translation_permitted` | 공개 라이선스, 퍼블릭 도메인, 자체 문서, 명시적 허가 | 원문 전체와 대응되는 완전 번역 가능 |
| `structured_translation` | 공식 페이지, 보도자료, 일반 웹 문서의 기본값 | section별 충실한 번역·상세 재서술, atomic claims |
| `claim_extraction_only` | 유료 기사, 저작권 제한 보고서, 접근 제한 자료 | 최소 요약, 검증 가능한 claim, 짧은 발췌 |
| `metadata_only` | 원문 접근 실패 또는 존재만 확인 | 서지정보와 수집 실패 사유 |

## 5. Source가 반드시 보유해야 하는 정보

### 5.1 Provenance

- canonical URL
- publisher, author, source type
- published, updated, retrieved date
- 원문 언어
- archive URL 또는 허용된 local raw path
- content hash
- 수집 범위와 라이선스

### 5.2 원문 의미 보존

- 원문 제목과 section 구조
- section 또는 page 단위의 한국어 기록
- 번역하지 않고 보존해야 할 기술·제품 용어
- 표, 그림, 각주, methodology의 핵심 내용
- 원문에 없는 전략 해석을 분리하는 규칙

### 5.3 Atomic Claims

각 claim은 다음 질문에 답해야 한다.

```text
누가 / 언제 / 무엇을 / 어느 범위에서 / 어떤 수치나 조건으로 / 어떤 근거 유형으로 말했는가?
```

Claim에는 안정적인 `claim_id`를 부여한다. Docs, Topics, Concepts는 Source 전체가 아니라 가능한 경우 claim_id를 참조한다.

### 5.4 변경 가능한 사실

- 실적
- 목표
- 투자액
- 생산능력
- 계약·파트너십
- 출시·구축 일정
- 기술 버전

이 항목은 `Numbers, Dates, and Commitments`에 분리해야 한다. 그래야 후속 Source가 들어올 때 기존 값을 비교하고 갱신 후보를 찾을 수 있다.

### 5.5 신뢰성과 한계

- 1차 자료인지 2차 자료인지
- 기업 홍보자료인지 독립 분석인지
- 실측인지 전망인지
- 방법론과 표본이 공개됐는지
- 상충하는 Source가 있는지

## 6. LLM Ingestion 단위

Source 전체를 하나의 chunk로 embedding하지 않는다. 다음 단위로 분리한다.

| Chunk Type | 권장 단위 | 주요 metadata |
|---|---|---|
| `source_identity` | Source당 1개 | source_id, publisher, dates, URL |
| `source_section` | 원문 section당 1개 | heading, page, language |
| `atomic_claim` | claim당 1개 | claim_id, subject, date, certainty |
| `numeric_fact` | 수치당 1개 | value, unit, period, actual/target |
| `entity_relation` | 관계당 1개 | subject, predicate, object, valid_at |
| `figure_note` | 그림·표당 1개 | asset_id, source location |
| `limitation` | 한계 항목당 1개 | reliability grade, caveat |

이 구조를 사용하면 LLM은 관련 section과 claim만 검색하고, 인용 가능한 근거를 유지하면서 Entity를 갱신할 수 있다.

## 7. Entity 업데이트 원칙

Source ingest가 곧바로 Docs·Topics·Concepts를 덮어쓰면 안 된다.

```text
Source 수집
→ claim 추출
→ 기존 claim과 비교
→ 신규·변경·상충 사실 판정
→ 영향받는 Entity 제안
→ 검토 후 반영
```

Source에는 해석을 최소화하고, 전략 해석은 Docs와 Topics에 둔다. Concept에는 여러 Source에서 반복 확인된 정의와 경계를 둔다.

## 8. 작성 품질 기준

적정한 Source Card는 원문 길이의 일정 비율로 판단하지 않는다. 다음 조건을 충족해야 한다.

- 원문의 주요 section이 누락되지 않는다.
- 모든 중요한 수치와 날짜가 별도 필드로 남는다.
- 목표와 실적이 구분된다.
- 핵심 주장에 원문 위치가 있다.
- 관련 Entity가 어떤 claim을 사용했는지 추적할 수 있다.
- 원문에 없는 전략 판단이 섞이지 않는다.
- 후속 Source가 들어왔을 때 변경점을 비교할 수 있다.

## 9. 마이그레이션 우선순위

기존 Source를 한 번에 전체 재작성하지 않는다.

1. Docs와 Topics에서 참조 횟수가 많은 Source
2. 수치·투자·일정·파트너십을 포함한 Source
3. 핵심 10개 Concept의 정의 근거 Source
4. 현재 한 줄 키워드만 있는 Source
5. 접근 실패 또는 중복 Source

기존 `Source Summary`는 `Evidence Abstract`의 초안으로 이동할 수 있지만, keyword 나열만 있는 경우 원문 재수집이 필요하다.
