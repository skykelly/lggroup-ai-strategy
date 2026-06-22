# LG Group AI Strategy Wiki — Cloud Handoff

## 1. 프로젝트 목적

이 저장소는 공개 근거를 기반으로 LG그룹의 AI 사업기회와 전략 질문을 정리한
Wiki이자, 해당 콘텐츠를 블로그형 웹사이트로 제공하는 프로젝트다.

작업 우선순위는 다음과 같다.

1. `wiki-generation.md`의 생성·검증 규칙
2. `docs/`와 `topics/`의 원본 연구 내용
3. Entity 문서인 `concepts/`, `companies/`, `sources/`
4. Astro 기반 Strategy Journal 웹사이트

Concepts, Companies, Sources는 독립적인 추론을 추가하는 문서가 아니라
Docs와 Topics에서 확인된 의미, 역할, 근거를 정리한 Entity다.

## 2. 저장소와 현재 상태

- GitHub: `https://github.com/skykelly/lggroup-ai-strategy.git`
- 기본 브랜치: `main`
- 운영 도메인: `https://axblog.kr`
- Vercel 프로젝트: `offshoes-projects/lggroup-ai-strategy`
- Vercel Project ID: `prj_hkNsISsFyqhFP6xfez48JChH6FQM`
- 최신 홈페이지 개편 커밋: `d8e60bc`
- Featured 이미지 추가 커밋: `9c330f0`
- 2026-06-23 기준 `main`과 `origin/main`은 동기화된 상태다.

이 문서를 작성한 시점에 로컬 `pptx/` 폴더는 Git에 포함되지 않은 유일한
미추적 항목이다. 클라우드 환경에서는 해당 폴더를 사용할 수 없다.

## 3. 주요 폴더

```text
docs/                    6대 테마와 Wiki 인덱스
topics/                  18개 전략 질문 아티클
concepts/                핵심 개념 Entity
companies/               LG 계열사와 외부 파트너 Entity
sources/                 근거 Source Card
assets/images/           Wiki 본문의 로컬 이미지 단일 저장소
assets/hero_images/      홈페이지 Strategy Carousel 이미지
assets/featured_images/  선별된 발표자료 이미지 52개
data/                    Entity, 관계, 이미지, 우선순위 JSON
reports/                 검증 및 Topic 우선순위 보고서
scripts/                 생성, 채점, 이미지 처리, Wiki 검증 스크립트
web/                     Astro 컴포넌트, 페이지, 스타일
db/migrations/           Neon 데이터베이스 마이그레이션
```

## 4. 로컬·클라우드 실행

Node.js와 Python이 필요하다. 의존성 설치와 실행 명령은 저장소 루트에서
수행한다.

```bash
npm install
npm run dev
```

기본 개발 주소는 `http://localhost:4321/`이다.

변경 후 최소 검증:

```bash
npm run check
npm run build
python scripts/validate_wiki.py
```

웹 UI만 수정한 경우에도 `npm run check`와 `npm run build`를 모두 통과시킨다.
홈페이지 인터랙션을 수정한 경우 데스크톱과 모바일 너비에서 브라우저로 직접
확인한다.

## 5. Wiki 생성·콘텐츠 규칙

- Wiki 생성 작업 전 `wiki-generation.md`를 먼저 읽는다.
- 다운로드에 성공한 Wiki 이미지는 Entity별 하위 폴더를 만들지 않고
  `assets/images/`에 저장한다.
- Markdown의 로컬 이미지 경로는 `assets/images/[filename]` 형식을 유지한다.
- 다운로드에 실패한 이미지는 원격 URL을 유지하고
  `data/image_inventory.json`에 실패 사유를 기록한다.
- `IMAGE_URL_NEEDED` 항목은 삭제하거나 임의로 대체하지 않는다.
- Source 문서에는 원문에 없는 전략 해석을 추가하지 않는다.
- Source Notes 및 원문의 구조를 보존하며, 반복 템플릿 문구를 다시 삽입하지
  않는다.
- Topic의 `status: draft`를 변경할 때는 내용, 근거, 링크를 함께 최종 검토한다.

Wiki 검증 결과는 `reports/wiki-validation-report.md`에 반영한다.

## 6. Topic 우선순위 모델

Topic은 다음 가중치로 자동 채점된다.

| 지표 | 가중치 |
|---|---:|
| 최신성 | 30% |
| 이슈성 | 25% |
| 전략 영향도 | 20% |
| 시급성 | 15% |
| 실행 가능성 | 10% |

One LG 시너지와 Evidence Strength는 현재 평가 지표에서 제외되어 있다.

```bash
# 전체 Topic 재채점
npm run score:topics

# 재채점 후 Wiki 인덱스와 data/topics.json 갱신
npm run refresh:topics
```

새 Topic은 `topics/NN_*.md` 형식으로 추가한다. 자동 판정이 맥락을 놓칠 때만
frontmatter의 `priority_inputs`로 1~5점 범위의 값을 보정한다.

관련 파일:

- `scripts/score_topic_priorities.py`
- `data/topic_priorities.json`
- `reports/topic-priority-report.md`

## 7. 현재 홈페이지 디자인과 인터랙션

홈페이지 구현의 중심 파일:

- `web/src/pages/index.astro`
- `web/src/components/HeroSphere.astro`
- `web/src/components/StrategyCarousel.astro`
- `web/src/styles/global.css`

현재 디자인 의도:

1. Hero
   - 검정·남색 그라데이션 배경
   - 점으로 구성된 회전 Sphere 애니메이션
   - 중앙 질문: `AI가 산업을 바꿀 때, LG는 무엇을 장악해야 하는가?`
   - 질문은 페이지 로딩 후 천천히 등장한다.
   - 추가 버튼과 보조 문구는 두지 않는다.

2. Strategy Map
   - 헤드라인: `Six AI Strategy Themes`
   - 설명: `물리적 세계와 산업 현장의 AI를 위한 ONE LG 청사진`
   - 6개 테마의 가로 캐러셀을 사용한다.
   - 마우스 휠로 가로 이동시키지 않는다.
   - 스와이프, 좌우 키보드, 화살표 버튼 이동을 지원한다.
   - 다음 테마가 일부 보이는 크기를 유지한다.
   - 테마 설명은 이미지 위의 별도 쿨그레이 패널에 표시하며 이미지에
     Overlay하지 않는다.
   - 이미지는 원본의 약 2.10:1 가로 비율을 유지하고 `object-fit: contain`으로
     전체가 잘리지 않게 표시한다.
   - Hover 확대는 이미지 잘림을 유발하므로 사용하지 않는다.

3. Page navigation
   - 메인 섹션은 세로 Scroll Snap을 사용한다.
   - 화면 오른쪽에 5개의 Pagination dots를 표시한다.
   - `prefers-reduced-motion` 환경에서는 Scroll Snap과 dots를 비활성화한다.

4. 콘텐츠 섹션
   - Featured Insights는 6개 글과 `더 보기` 버튼을 표시한다.
   - Six Opportunity Fields는 6개 LG 회사의 역할을 설명하고 Companies로
     이동한다.
   - 기존 Research Journal 영역은 삭제된 상태다.

과거 컴포넌트 `HeroCarousel.astro`와 `StrategyRadar.astro`는 현재 홈페이지에서
사용하지 않는다. 삭제 여부는 별도 정리 작업에서 판단한다.

## 8. 이미지 자산

`web/scripts/prepare-assets.mjs`가 빌드 전에 다음 자산을 웹 공개 폴더로
복사한다.

- `assets/images/` → `web/public/assets/images/`
- `assets/hero_images/` → `web/public/assets/hero_images/`

`assets/featured_images/`에는 발표자료에서 선별한 이미지 52개가 있으며
GitHub에 포함되어 있다. 현재 홈페이지가 이 폴더를 직접 사용하지는 않는다.
새로운 Featured 콘텐츠나 상세 페이지 비주얼을 만들 때 우선 재사용한다.

`assets/hero_images/`의 `lggroup_ax_01.png`부터 `lggroup_ax_06.png`까지가 현재
Strategy Carousel에서 사용된다.

## 9. Vercel·Neon 운영

배포 설정:

- Framework: Astro
- Build command: `npm run build`
- Production domain: `https://axblog.kr`
- 상태 확인 API: `https://axblog.kr/api/health.json`

필수 Vercel 환경변수:

```text
DATABASE_URL=<Neon pooled connection string>
SITE_URL=https://axblog.kr
```

실제 인증 정보는 문서, 소스, Git 커밋에 기록하지 않는다. 클라우드 환경에는
Vercel 또는 Codex Environment의 Secret으로 별도 설정해야 한다.

Neon 초기 마이그레이션:

```text
db/migrations/0001_app_metadata.sql
```

DB 연결 코드:

- `web/src/lib/db.ts`
- `web/src/pages/api/health.json.ts`

Vercel CLI로 수동 운영 배포할 때:

```bash
npx vercel --prod --yes
```

GitHub `main` 푸시가 Vercel 프로젝트의 자동 배포와 연결되어 있다면 중복
배포하지 말고 Vercel 대시보드에서 먼저 상태를 확인한다.

## 10. Git 작업 원칙

- 사용자의 기존 변경과 미추적 파일을 임의로 포함하거나 삭제하지 않는다.
- 현재 로컬 전용 `pptx/`는 사용자가 별도로 요청하기 전까지 커밋하지 않는다.
- 혼합된 작업 트리에서는 `git add -A` 대신 대상 파일을 명시적으로 Stage한다.
- 변경 후 `git diff --check`와 관련 검증 명령을 실행한다.
- 운영 반영 요청이 없으면 커밋이나 배포를 자동으로 확대하지 않는다.
- 운영 반영 요청이 있으면 커밋 → GitHub push → Vercel 상태 확인 순서로 진행한다.

## 11. 클라우드에서 첫 작업 순서

1. GitHub 저장소의 `main`을 체크아웃한다.
2. 이 문서와 `wiki-generation.md`, `README.md`를 읽는다.
3. `npm install`을 실행한다.
4. `npm run check`와 `npm run build`로 기준 상태를 확인한다.
5. DB 작업이 필요하면 `DATABASE_URL`과 `SITE_URL` Secret의 존재 여부만
   확인하고 값을 출력하지 않는다.
6. 작업 전 `git status`로 예상하지 못한 변경이 없는지 확인한다.
7. 웹 작업은 변경 후 실제 브라우저에서 인터랙션과 반응형 레이아웃을 검증한다.

## 12. 다음 작업 후보

명시적으로 확정된 미완료 작업은 없다. 다음 개선은 필요에 따라 선택한다.

- `assets/featured_images/`를 Insight 또는 Theme 상세 페이지에 연결
- 미사용 홈페이지 컴포넌트 정리
- 모바일 환경에서 Strategy Carousel의 카드 높이와 텍스트 밀도 추가 조정
- 운영 도메인의 Lighthouse·접근성·SEO 재검증
- 새 Topic 추가 시 우선순위 자동 채점과 인덱스 갱신

새 클라우드 스레드에서는 먼저 사용자가 원하는 다음 작업을 확인하고, 이 후보를
자동으로 모두 수행하지 않는다.
