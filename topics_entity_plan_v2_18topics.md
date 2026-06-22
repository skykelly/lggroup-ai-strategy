# LG AI Strategy Wiki — Topics Entity Plan v2

> 목적: `topics/`를 새로운 핵심 Entity로 추가한다.  
> 기준: 기존 `docs / concepts / companies / sources`와 동일하게 Wiki의 주요 지식 축으로 관리한다.  
> 변경사항: 기존 후보 중 **19번, 20번은 삭제**하고, 1~18번 Topic만 유지한다.  
> 작성 방식: Codex 대량 생성이 아니라, **GPT-5.5에서 개별 Topic을 docs급 중요도로 작성**한 뒤 Codex로 repo 정리·링크·이미지 다운로드·검증을 수행한다.

---

## 1. Topics Entity의 역할

기존 Entity의 역할은 다음과 같다.

```text
docs      = 6대 테마별 전략 문서
concepts  = 반복 등장하는 핵심 개념 정의
companies = LG 계열사·외부 파트너별 역할
sources   = 원문·보도·리포트 단위 근거
topics    = 핵심 질문에 답하는 전략 에세이
```

`topics/`는 단순 보조 문서가 아니라, `docs/`와 같은 수준의 중요도를 가진다.  
다만 `docs/`가 “사업기회가 무엇인가”를 다룬다면, `topics/`는 “그래서 우리가 물어야 할 전략적 질문은 무엇인가”에 답한다.

---

## 2. Topics 작성 원칙

### 2.1 질문 중심

Topic 제목은 가능하면 질문형으로 쓴다.

예:

```text
젠슨 황이 LG에게 남긴 것은?
EXAONE의 글로벌 AI 플랫폼 대비 객관적 경쟁력은?
AI Infra 수요에 대한 향후 5년의 전망은?
AI Factory는 데이터센터인가 제조 운영 모델인가?
```

### 2.2 해석 중심

Topic은 사업기회 목록을 반복하지 않는다.  
확인된 사실을 기반으로 전략적 의미를 해석한다.

### 2.3 다중 Entity 연결

각 Topic은 여러 Entity를 가로지른다.

```text
Topic
  ├─ related_themes → docs/
  ├─ related_concepts → concepts/
  ├─ related_companies → companies/
  └─ source_ids → sources/
```

### 2.4 이미지 포함

Topic 문서도 docs와 마찬가지로 원본 소스 이미지를 최대한 포함한다.

이미지 원칙:

1. 공식자료, 원문 보도자료, 주요 언론 보도에 포함된 이미지를 우선한다.
2. 가능한 경우 원본 이미지 URL을 Markdown/HTML 이미지 태그로 직접 삽입한다.
3. 이미지 URL이 막혀 있거나 동적 렌더링만 제공되는 경우 `이미지 URL 확보 필요`로 표시하고 원문 링크를 병기한다.
4. 별도 이미지, SVG, 인포그래픽을 새로 생성하지 않는다.
5. 각 Topic별 이미지 다운로드 스크립트를 Python으로 함께 만든다.
6. 나중에 Codex가 전체 이미지를 `assets/images/topics/[topic_id]/`에 다운로드하도록 한다.

### 2.5 GPT-5.5에서 개별 작성

Topics는 docs급 중요도를 가지므로 Codex에 초안 생성을 맡기지 않는다.  
GPT-5.5에서 Topic별로 직접 작성하고, Codex는 다음 역할만 수행한다.

```text
Codex 역할
- 파일 위치 정리
- wikilink 보정
- source_ids 정합성 점검
- 이미지 다운로드 스크립트 실행/정리
- image manifest 생성
- README / index 업데이트
```

---

## 3. 권장 폴더 구조

```text
lg-ai-strategy-wiki/
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

  scripts/
    download_topic_01_images.py
    download_topic_02_images.py
    ...

  assets/
    images/
      topics/
        01_what_did_jensen_huang_leave_lg/
        02_how_competitive_is_exaone_globally/
        ...
```

---

## 4. Topic Frontmatter Schema

```yaml
---
id: topic_[topic_id]
type: topic
title: "[질문형 제목]"
status: draft
updated: 2026-06-21
question: "[핵심 질문]"
short_answer: "[3~5문장 요약 답변]"
topic_type:
  - strategic_question
  - market_outlook
  - technology_assessment
  - partner_analysis
  - risk_debate
  - operating_model
related_themes:
  - [theme_id]
related_concepts:
  - [concept_id]
related_companies:
  - [company_id]
source_ids:
  - [source_id]
image_policy:
  use_original_source_images: true
  generate_new_images: false
  download_script: scripts/download_topic_[nn]_images.py
tags:
  - [tag]
---
```

---

## 5. Topic 문서 템플릿

```markdown
# [질문형 제목]

## 1. Question

이 글이 답하려는 핵심 질문을 2~3문장으로 설명한다.

## 2. Short Answer

현재 기준의 답을 3~5문장으로 요약한다.

## 3. Why This Question Matters

이 질문이 LG그룹 AI 전략에서 중요한 이유를 설명한다.

## 4. What We Know

공식 발표, 보도, 기술자료에서 확인된 사실을 정리한다.

## 5. Interpretation

확인된 사실을 바탕으로 전략적 의미를 해석한다.

## 6. Counterpoints

반대 관점, 리스크, 아직 모호한 부분을 정리한다.

## 7. Implications for LG

LG그룹, 계열사, 테마별로 무엇을 해야 하는지 정리한다.

## 8. Original Source Images

원문 이미지 URL을 직접 삽입한다.  
막힌 이미지는 `이미지 URL 확보 필요`로 표시한다.

## 9. Related Entities

- Themes:
- Concepts:
- Companies:
- Sources:

## 10. Open Questions

추가로 검증해야 할 질문을 정리한다.

## Appendix A. Image Inventory

| id | source | status | image_url |
|---|---|---|---|

## Appendix B. Source Notes

핵심 출처별 요약과 활용 위치를 정리한다.
```

---

## 6. 최종 Topic 목록: 18개

| No | Topic | 핵심 질문 | 관련 테마 | 우선순위 |
|---:|---|---|---|---|
| 1 | 젠슨 황이 LG에게 남긴 것은? | NVIDIA 협력의 본질은 GPU 확보인가, LG 사업 포트폴리오 재정의인가? | 1, 2, 3, 6 | High |
| 2 | EXAONE의 글로벌 AI 플랫폼 대비 객관적 경쟁력은? | EXAONE은 글로벌 frontier model이 아니라면 어떤 포지션에서 이길 수 있는가? | 4, 5, 6 | High |
| 3 | AI Infra 수요에 대한 향후 5년의 전망은? | AI 데이터센터 수요는 계속 폭증할 것인가, 전력·냉각·GPU 병목에서 조정될 것인가? | 1, 6 | High |
| 4 | AI Factory는 데이터센터인가 제조 운영 모델인가? | NVIDIA가 말한 AI Factory를 LG 전략에서는 어디에 위치시켜야 하는가? | 1, 2, 6 | High |
| 5 | Palantir가 LG에 던진 진짜 질문은? | 온톨로지는 데이터 통합 프로젝트인가, 경영 의사결정 운영체계인가? | 4, 6 | High |
| 6 | LG는 완성차를 만들지 않으면서 AI Mobility에서 무엇을 장악할 수 있는가? | LG가 AIDV 시대에 장악할 레이어는 어디인가? | 3, 6 | High |
| 7 | Physical AI는 스마트팩토리의 재포장인가? | 기존 스마트팩토리와 Physical AI의 실질 차이는 무엇인가? | 2, 6 | Medium |
| 8 | 배터리 SW는 LG에너지솔루션의 다음 플랫폼이 될 수 있는가? | BMS/BMTS는 부가 기능인가, SDV 시대 소프트웨어 플랫폼인가? | 3, 6 | Medium |
| 9 | LG의 글로벌 AI Alliance는 옵션 전략인가 종속 리스크인가? | 외부 파트너십이 기술 옵션을 넓히는가, 핵심 기술 의존도를 키우는가? | 6 | Medium |
| 10 | AI for Science는 LG R&D 생산성을 얼마나 바꿀 수 있는가? | 후보 탐색 속도 개선이 실제 소재·신약 성공률로 이어질 수 있는가? | 5, 6 | Medium |
| 11 | AI 시대의 One LG는 실제 시너지가 될 수 있는가? | 계열사 자산을 묶는 것이 구호인지, 사업모델인지 판단할 기준은 무엇인가? | 1~6 | High |
| 12 | LG의 진짜 AI Moat는 모델인가, 데이터인가, 물리 세계 자산인가? | LG가 글로벌 AI 플랫폼과 다르게 방어할 수 있는 경쟁우위는 무엇인가? | 1~6 | High |
| 13 | 전력·냉각 병목은 LG전자와 LG에너지솔루션의 새 성장축인가? | AI 데이터센터의 병목이 GPU에서 power/cooling으로 이동하면 누가 이익을 보는가? | 1 | Medium |
| 14 | LG는 foundation model을 직접 키워야 하는가, 산업 특화 모델에 집중해야 하는가? | 자체 모델 전략과 파트너 모델 전략의 균형은 무엇인가? | 4, 5, 6 | Medium |
| 15 | Enterprise AX의 성과는 무엇으로 측정해야 하는가? | 사용률이 아니라 원가·재고·납기·품질·R&D 속도로 측정할 수 있는가? | 4 | High |
| 16 | 제조 데이터는 어떻게 AI 제품이 되는가? | 내부 제조 레퍼런스를 외부 산업 AI 솔루션으로 전환하는 조건은 무엇인가? | 2, 4 | Medium |
| 17 | 한국형 AI Sovereignty는 LG에게 기회인가 부담인가? | K-EXAONE, EXAONE, 국내 AI 인프라가 국가·산업 전략과 어떻게 연결되는가? | 1, 4, 5, 6 | Medium |
| 18 | GPU Cloud 가격이 하락하면 AIDC 사업성은 어떻게 변하는가? | GPU 희소성이 줄어들 때 데이터센터 사업은 전력·운영·서비스 경쟁으로 이동하는가? | 1, 6 | Medium |

---

## 7. 삭제 Topic

아래 2개는 이번 v2 계획에서 제외한다.

```text
19. AI Agent가 조직을 바꾸는가, 보고서를 빠르게 만드는가?
20. LG AI Home과 산업 AI 전략은 만날 수 있는가?
```

삭제 이유:

- 19번은 15번 `Enterprise AX의 성과는 무엇으로 측정해야 하는가?`와 중복도가 높다.
- 20번은 현재 6대 테마의 핵심 범위에서 다소 벗어나며, 추후 `AI Home / Customer AI` 별도 확장 테마에서 다루는 것이 적합하다.

---

## 8. 작성 순서 제안

Topic은 순서대로 작성하되, 한 번에 너무 많이 만들지 않는다.  
이미지 조사와 원문 검증이 필요하기 때문에, `docs` 작성 때와 비슷하게 **1~2개씩 작성**하는 것이 안정적이다.

### 8.1 1차 작성

```text
01. 젠슨 황이 LG에게 남긴 것은?
02. EXAONE의 글로벌 AI 플랫폼 대비 객관적 경쟁력은?
03. AI Infra 수요에 대한 향후 5년의 전망은?
```

### 8.2 2차 작성

```text
04. AI Factory는 데이터센터인가 제조 운영 모델인가?
05. Palantir가 LG에 던진 진짜 질문은?
06. LG는 완성차를 만들지 않으면서 AI Mobility에서 무엇을 장악할 수 있는가?
```

### 8.3 3차 작성

```text
07. Physical AI는 스마트팩토리의 재포장인가?
08. 배터리 SW는 LG에너지솔루션의 다음 플랫폼이 될 수 있는가?
09. LG의 글로벌 AI Alliance는 옵션 전략인가 종속 리스크인가?
```

### 8.4 4차 작성

```text
10. AI for Science는 LG R&D 생산성을 얼마나 바꿀 수 있는가?
11. AI 시대의 One LG는 실제 시너지가 될 수 있는가?
12. LG의 진짜 AI Moat는 모델인가, 데이터인가, 물리 세계 자산인가?
```

### 8.5 5차 작성

```text
13. 전력·냉각 병목은 LG전자와 LG에너지솔루션의 새 성장축인가?
14. LG는 foundation model을 직접 키워야 하는가, 산업 특화 모델에 집중해야 하는가?
15. Enterprise AX의 성과는 무엇으로 측정해야 하는가?
```

### 8.6 6차 작성

```text
16. 제조 데이터는 어떻게 AI 제품이 되는가?
17. 한국형 AI Sovereignty는 LG에게 기회인가 부담인가?
18. GPU Cloud 가격이 하락하면 AIDC 사업성은 어떻게 변하는가?
```

---

## 9. 하나씩 작성할 때의 산출물

각 Topic 작성 시 다음 2개 파일을 만든다.

```text
topics/[nn]_[topic_id].md
scripts/download_topic_[nn]_images.py
```

예: Topic 1

```text
topics/01_what_did_jensen_huang_leave_lg.md
scripts/download_topic_01_images.py
```

이미지 다운로드 경로:

```text
assets/images/topics/01_what_did_jensen_huang_leave_lg/
```

---

## 10. Topic 1 작성 기준

첫 번째 Topic은 다음 기준으로 작성한다.

```text
Title:
젠슨 황이 LG에게 남긴 것은?

핵심 질문:
NVIDIA 협력은 LG에게 GPU 확보 이상의 무엇을 남겼는가?

핵심 관점:
젠슨 황이 LG에게 남긴 것은 단순한 GPU 협력이 아니라,
LG의 사업 포트폴리오를 AI 시대의 physical infrastructure,
physical AI, mobility platform으로 다시 읽는 관점이다.

반드시 다룰 내용:
- NVIDIA M.A.P. 협력
- Mobility / AI Infra / Physical AI 3축
- LG전자 냉각·VS·로봇
- LG U+ AIDC
- LG CNS DSX / AI Factory / AX
- LG에너지솔루션 800V DC / 전력·배터리
- LG이노텍 sensing / communication / lighting
- LG AI연구원 EXAONE 고도화
- AI Factory를 Theme 2 하위 Concept으로 정리
- NVIDIA 의존 리스크와 LG 내부화 과제

이미지 후보:
- LG–NVIDIA M.A.P. 보도 이미지
- NVIDIA Blog LG AI Factory 이미지
- LG전자 Data Center Cooling 이미지
- LG CNS AI Box 또는 DSX 관련 이미지
- LG U+ AIDC 이미지
- LG에너지솔루션 B.around 또는 800V DC 관련 이미지
```

---

## 11. Codex 작업 지시문

```text
작업 목표:
topics/ Entity를 Wiki에 추가하고, GPT-5.5에서 작성한 Topic 문서를 repo 구조에 맞게 정리한다.

규칙:
1. topics/ 폴더를 생성한다.
2. topics/00_topic_index.md를 생성한다.
3. topics_entity_plan_v2_18topics.md의 18개 Topic 목록만 사용한다.
4. 19번, 20번 Topic은 생성하지 않는다.
5. Topic 문서는 GPT-5.5가 작성한 원문을 우선한다.
6. Codex는 본문을 임의로 대폭 재작성하지 않는다.
7. Codex는 wikilink, frontmatter, source_ids, image inventory, download script 경로만 정리한다.
8. 각 Topic별 이미지 다운로드 스크립트를 scripts/에 둔다.
9. 이미지 다운로드 대상 경로는 assets/images/topics/[topic_id]/로 한다.
10. 생성 이미지나 SVG는 만들지 않는다.
11. 원본 이미지 URL이 막힌 경우 `이미지 URL 확보 필요` 표시를 유지한다.
12. README에 Topics Entity 설명을 추가한다.
13. docs/00_overview.md에 topics/로 가는 링크를 추가한다.

검증:
1. topics/00_topic_index.md가 있는가?
2. Topic이 18개만 있는가?
3. 19번, 20번 파일이 없는가?
4. 모든 Topic frontmatter에 question, short_answer, related_themes, related_concepts, related_companies, source_ids가 있는가?
5. 모든 Topic에 Original Source Images 또는 Image Inventory가 있는가?
6. 모든 Topic별 download script가 있는가?
7. 이미지 다운로드 경로가 assets/images/topics/ 아래로 통일되어 있는가?
8. Topic 본문이 docs의 사업기회 내용을 단순 반복하지 않는가?
```

---

## 12. README 추가 문구

```markdown
## Topics

`topics/`는 LG그룹 AI 전략에서 반복적으로 제기되는 핵심 질문을 다루는 전략 에세이 영역이다.

`docs/`가 6대 사업기회 테마를 설명하고, `concepts/`가 개념을 정의하며, `companies/`가 계열사·파트너 역할을 정리하고, `sources/`가 근거 자료를 관리한다면, `topics/`는 이 모든 Entity를 가로질러 다음과 같은 질문에 답한다.

- 젠슨 황이 LG에게 남긴 것은?
- EXAONE의 글로벌 AI 플랫폼 대비 객관적 경쟁력은?
- AI Infra 수요에 대한 향후 5년 전망은?
- AI Factory는 데이터센터인가 제조 운영 모델인가?
- Palantir가 LG에 던진 진짜 질문은?

Topics는 사업기회 목록이 아니라, 전략적 해석과 논쟁을 담는 docs급 문서다. 각 Topic은 원본 소스 이미지와 image inventory, 다운로드 스크립트를 함께 관리한다.
```
