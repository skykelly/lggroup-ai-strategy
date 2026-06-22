---
id: src_[source_id]
type: source
title: [원문의 정확한 제목]
publisher: [발행기관]
authors: []
published: unknown
updated: unknown
retrieved_at: [YYYY-MM-DD]
url: [Canonical URL]
source_type: press_release
language: [원문 언어 코드]
content_policy: structured_translation
capture_status: complete
archive_url: null
local_raw_path: null
content_hash: null
license: unknown
reliability_grade: B
related_themes: []
related_topics: []
related_concepts: []
related_companies: []
tags: []
---

# [원문의 정확한 제목]

## 1. Source Identity

| 항목 | 내용 |
|---|---|
| 발행기관 | [Publisher] |
| 저자·발표자 | [Author or Speaker] |
| 원문 유형 | [press release / official page / report / paper / news / dataset / policy] |
| 발행일·수정일 | [Dates] |
| 수집일 | [Retrieved Date] |
| 원문 언어 | [Language] |
| 원문 URL | [URL] |
| Archive / Raw | [Archive URL or local raw path] |
| 수집 범위 | [complete / partial / metadata_only] |
| 라이선스 | [License or unknown] |

## 2. Evidence Abstract

원문의 목적, 다루는 범위, 핵심 결론을 5~10문장으로 기술한다.  
전략적 평가를 넣지 않고 원문이 실제로 주장하거나 보고한 내용만 쓴다.

## 3. Atomic Claims

| claim_id | 원문 위치 | 주체 | 주장·사실 | 수치·기간 | 근거 유형 | 확실성 |
|---|---|---|---|---|---|---|
| [source_id]_c01 | [section/page/paragraph] | [Entity] | [한 문장에 하나의 검증 가능한 사실] | [value/unit/date] | direct_quote / statement / measured / estimate / inference | high |

규칙:

- 한 행에는 하나의 사실만 기록한다.
- 발표자의 계획·목표와 이미 달성된 실적을 구분한다.
- 전망, 추정, 제3자 평가를 사실처럼 기록하지 않는다.
- 수치에는 단위, 기준시점, 비교 기준을 함께 기록한다.

## 4. Entities and Relationships

| 주체 | 관계 | 대상 | 원문 근거 | 유효시점 |
|---|---|---|---|---|
| [Company A] | partnered_with / invested_in / supplies / operates / develops | [Company or Asset B] | [claim_id] | [date or period] |

## 5. Numbers, Dates, and Commitments

| 항목 | 값 | 단위 | 기준시점 | 성격 | claim_id |
|---|---:|---|---|---|---|
| [Metric] | [Value] | [Unit] | [Date] | actual / target / estimate / capacity / investment | [claim_id] |

## 6. Definitions and Terminology

| 원문 용어 | 한국어 표기 | 원문에서의 의미 | Wiki Concept 후보 |
|---|---|---|---|
| [Term] | [Translation] | [Context-specific definition] | `concepts/[slug].md` |

## 7. Figures, Tables, and Images

| asset_id | 유형 | 원문 위치 | 설명·읽을 수 있는 사실 | original_url | local_path | status |
|---|---|---|---|---|---|---|
| [image_id] | image / chart / table | [figure/page] | [시각자료가 직접 보여주는 내용] | [URL] | assets/images/[filename] | downloaded |

## 8. Source Limitations

- 원문이 직접 제공하지 않는 정보
- 기업 발표자료의 홍보성 또는 이해관계
- 표본, 방법론, 비교 기준의 한계
- 확인되지 않은 계획·목표·전망
- 접근 제한이나 수집 누락 구간

## 9. Reliability Assessment

| 평가 항목 | 판단 | 이유 |
|---|---|---|
| 출처 직접성 | high / medium / low | [Primary or secondary] |
| 사실 검증성 | high / medium / low | [수치·방법·원문 근거 여부] |
| 최신성 | current / dated / unknown | [Date reasoning] |
| 이해관계 | low / medium / high | [Publisher incentives] |
| 종합 등급 | A / B / C / D | [Short rationale] |

## 10. Used In

| Entity | 사용한 claim_id | 사용 방식 |
|---|---|---|
| `docs/[document].md` | [claim IDs] | 시장 사실 / 기술 정의 / 회사 역할 / 전략 가정 |

## 11. Update Hooks

- **변경 감지 기준:** 제목, 수정일, 핵심 수치, 제품·파트너·목표 변경
- **영향받는 Entity:** `docs/[document].md`, `topics/[topic].md`, `concepts/[concept].md`, `companies/[company].md`
- **재검토 조건:** [새 버전 발표, 목표 시점 도달, 후속 실적 발표 등]
- **마지막 검토일:** [YYYY-MM-DD]

## Appendix A. Permitted Evidence Excerpts

저작권과 검증 목적에 필요한 짧은 원문만 기록한다. 각 발췌문에는 위치와 claim_id를 연결한다.

| claim_id | 원문 위치 | 짧은 원문 발췌 |
|---|---|---|
| [source_id]_c01 | [section/page] | “[Short excerpt]” |

## Appendix B. Ingestion Notes

- 파서 또는 수집 방법
- 제외한 navigation, 광고, cookie 문구
- PDF OCR 여부와 품질
- 번역 방식과 사람이 확인한 범위
- 중복 Source 또는 대체 URL
