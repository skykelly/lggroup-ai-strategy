# Interior Concept Registry

기준일: 2026-06-09

`/concept` 폴더는 여러 문서에서 추출된 Entity를 정규화하고, 관계·맥락·근거가 안정된 의미 단위를 Concept로 관리한다.

## 완료 현황

- 전체 Concept: 38개
- 모든 Concept에 표준 12개 섹션 적용
- Concept Registry YAML/JSON 갱신 완료

## 유형별 수

- `functional`: 7개
- `lifestyle`: 5개
- `market`: 4개
- `material_cmf`: 5개
- `spatial`: 7개
- `style`: 10개

## 기본 원칙

1. Concept는 단순 키워드가 아니라 정의·경계·관계·근거를 가진다.
2. Concept와 Trend Observation을 분리한다.
3. 컬러·소재·상품 단어는 원칙적으로 Supporting Entity로 시작한다.
4. 새 Concept는 `candidate → reviewed → canonical` 단계를 거친다.
5. 시스템 ID는 영문 kebab-case, 본문 표준명은 한국어/영어를 함께 쓴다.

## 상태 원칙

- `canonical`: 독립 의미와 실무 활용성이 충분한 Concept
- `supporting`: 독립 문서를 유지하지만 상위 Concept의 속성·구성요소 성격이 강한 Concept
- `candidate`: 추가 증거와 경계 검토 후 승격 여부를 결정할 Concept

## 파일

- 각 `<concept-id>.md`: 개별 Concept 문서
- `/data/_concept-template.md`: 신규 Concept 문서 템플릿
- `/data/_concept-list.md`: 전체 Concept 후보 목록
- `/data/concept-registry.yml`: 기계 판독용 레지스트리

## 후속 권장 작업

1. 38개 Concept 전체 관계 Triple 통합
2. alias 충돌 및 순환 관계 QA
3. Concept-Entity 분리 검토
4. Concept Registry 기반 `concepts.md` seed 통합본 생성
5. 문서 학습 결과를 자동 매칭하는 Entity Extractor/Normalizer 프롬프트 작성