# LG Group AI Strategy Wiki

이 Wiki는 공개 출처를 기반으로 LG그룹의 AI 시대 사업기회, 핵심 개념, 전략 질문을 Entity 단위로 연결한 지식베이스다. 기준일은 2026년 6월 21일이다.

## Knowledge Model

원본 지식의 중심은 `docs/`와 `topics/`다.

- `docs/`: 6대 AI 사업기회 테마 문서
- `topics/`: 18개 핵심 질문 중심의 전략 에세이
- `concepts/`: Docs와 Topics에서 반복되는 핵심 개념과 경계
- `companies/`: LG 계열사와 외부 파트너의 전략적 역할
- `sources/`: 원문·보도·리포트의 Source Card
- `assets/images/`: 원본 출처 이미지의 단일 로컬 저장소
- `data/`: Entity 탐색과 검증을 위한 JSON
- `reports/`: 링크·ID·이미지 검증 결과

```text
Docs + Topics
  ├─ Concepts
  ├─ Companies
  ├─ Sources
  └─ Assets / Data
```

Concepts, Companies, Sources는 독립적으로 내용을 확장하는 문서가 아니라 Docs와 Topics에서 확인된 의미·역할·근거를 사후 정리한 Entity다.

## Six Themes

1. [AI Data Center / Infra](docs/01_ai_data_center_infra.md)
2. [Physical AI / Smart Manufacturing](docs/02_physical_ai_smart_manufacturing.md)
3. [AI Mobility / SDV·AIDV](docs/03_ai_mobility_sdv_aidv.md)
4. [Enterprise AX / Agentic Operating Model](docs/04_enterprise_ax_agentic_operating_model.md)
5. [AI for Science / Bio / Materials / Battery](docs/05_ai_for_science_bio_materials_battery.md)
6. [Global AI Alliance / Open Innovation](docs/06_global_ai_alliance_open_innovation.md)

## Important Classification

`AI Data Center / Infra`는 GPU, 데이터센터, 냉각, 전력, ESS, DC Grid, 클라우드 운영을 포함하는 물리적·연산 인프라 테마다.

`AI Factory`는 독립 테마나 Theme 1의 이름이 아니다. AI Data Center 기반 위에서 제조 데이터, 로봇, 디지털트윈, 합성데이터, 시뮬레이션을 연결해 Physical AI를 학습·검증·배포하는 운영 모델이다. 따라서 primary theme은 `physical_ai_smart_manufacturing`이다.

## Navigation

- [Wiki Overview](docs/00_overview.md)
- [Topic Index](topics/00_topic_index.md)
- [Theme-Company Matrix](docs/80_theme_company_matrix.md)
- [Concept-Theme Map](docs/81_concept_theme_map.md)
- [Partner Map](docs/82_partner_map.md)
- [Source Coverage](docs/83_source_coverage.md)
- [Concept Index](docs/84_concept_index.md)
- [Strategic Topic Index](docs/85_topic_index.md)
- [Research Questions](docs/90_research_questions.md)
- [Validation Report](reports/wiki-validation-report.md)

## Image Policy

모든 다운로드 성공 이미지는 Entity별 하위 폴더 없이 `assets/images/`에 저장한다.

- 성공한 이미지는 Markdown에서 `assets/images/[filename]`을 사용한다.
- 다운로드 실패 이미지는 원격 URL을 유지한다.
- `IMAGE_URL_NEEDED` 표시는 삭제하지 않는다.
- 이미지 출처, 상태, 재사용 Entity는 `data/image_inventory.json`의 `used_by`로 관리한다.
- Concepts, Companies, Sources는 기존 inventory의 이미지를 우선 재사용한다.

## Structured Data

- `data/concepts.json`
- `data/companies.json`
- `data/sources.json`
- `data/topics.json`
- `data/theme_company_matrix.json`
- `data/image_inventory.json`

## Validation

검증은 다음 명령으로 다시 실행할 수 있다.

```powershell
python scripts/validate_wiki.py
```

현재 검증 결과와 허용된 경고 목록은 [Wiki Validation Report](reports/wiki-validation-report.md)에 기록되어 있다.

## Strategy Journal Website

Wiki의 Topic 문서를 블로그형 웹사이트로 제공하는 Astro 앱은 `web/`에 있다.

```powershell
npm install
npm run dev
```

정적 배포 파일은 다음 명령으로 생성한다.

```powershell
npm run check
npm run build
```

Topic 우선순위는 최신성과 이슈성을 중심으로 자동 계산한다.

```powershell
# 기존 Topic 전체 재채점
npm run score:topics

# 새 Topic 채점 + Wiki 인덱스와 data/topics.json 갱신
npm run refresh:topics
```

- 가중치: 최신성 30%, 이슈성 25%, 전략 영향도 20%, 시급성 15%, 실행 가능성 10%
- 등급: P0 4.25 이상, P1 3.70 이상, P2 3.10 이상, 그 외 P3
- One LG 시너지와 Evidence Strength는 평가 지표에서 제외
- 새 글은 `topics/NN_*.md`로 추가하면 다음 실행 시 자동으로 포함
- 자동 판정 보정이 필요한 경우 frontmatter에 `priority_inputs`를 추가
- 상세 산출물: [Topic Priority Report](reports/topic-priority-report.md), `data/topic_priorities.json`

- 홈: 6대 테마 Strategy Radar와 주요 전략 질문
- Insights: 18개 Topic 검색·테마 필터·우선순위 정렬
- Article: Markdown 본문, 목차, 관련 Entity, 출처 수, 읽기 진행률
- Themes: 6대 사업기회 목록과 상세 전략 문서
- Companies: LG 계열사·파트너 25개 역할 탐색
- Concepts: 핵심 개념 87개 검색·테마 필터·상세 페이지
- Sources: 공개 출처 87개 Evidence Ledger와 원문·활용 관계
- Article Evidence Panel: 아티클 안에서 근거 자료 확인
- Global Search: Insights, Themes, Companies, Concepts, Sources 통합 검색
- SEO: canonical, Open Graph, JSON-LD, sitemap, robots, RSS
- Deploy: Vercel 및 Cloudflare Pages 정적 배포 설정
- 원본 콘텐츠: `topics/*.md`
- 웹 이미지: 빌드 시 `assets/images/`에서 자동 복사

배포 도메인이 정해지면 `SITE_URL` 환경변수를 실제 URL로 설정한다.
