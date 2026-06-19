# Wiki Generator — 개발 계획

## 개요

임의 주제를 입력하면 자동으로 위키를 생성하고 지속적으로 업데이트하는 플랫폼.  
homestyle-wiki의 LLM 위키 파이프라인을 멀티 테넌트 SaaS로 확장한다.

### 핵심 전제

| 항목 | 결정 |
|---|---|
| 아키텍처 | 단일 플랫폼, 멀티 테넌시 (wiki_id 기반) |
| 리서치 API | Tavily API |
| 현재 목적 | 본인 사용 |
| 향후 계획 | 외부 SaaS 출시 |

### homestyle-wiki와의 차이

| | homestyle-wiki | wiki-generator |
|---|---|---|
| 주제 | 고정 (한국 인테리어) | 임의 주제, 사용자 입력 |
| 초안 방식 | 수동 (kb/wiki/*.md 시드) | 자동 리서치 → LLM 생성 |
| 위키 수 | 1개 | N개 (멀티 테넌트) |
| 사용자 | 단일 관리자 | 위키별 소유자 |
| RSS 설정 | 수동 | 주제 기반 자동 추천 |
| 지속 업데이트 | ✅ | ✅ (동일 패턴 재사용) |

---

## 전체 흐름

```
[주제 입력]
    │
    ▼
[Phase A: 리서치]
Tavily 검색 → 상위 소스 20-30개 수집
    │
    ▼
[Phase B: 구조 설계]
GPT-4.1 → 챕터 목차 / 핵심 개념 / 토픽 맵 (JSON)
    │
    ▼
[Phase C: 초안 생성]
챕터(pages) 내용 + 개념(concepts) 내용 + 에디토리얼 자동 생성
    │
    ▼
[Phase D: 임베딩]
전체 콘텐츠 임베딩 빌드 → RAG 준비
    │
    ▼
[Phase E: 지속 업데이트] ←──────────────────┐
RSS / 키워드 모니터링 → ingest → synthesize  │
자동으로 반복                                 │
                                             └── GitHub Actions (일 1회)
```

---

## 아키텍처

### DB 스키마 (멀티 테넌트)

기존 homestyle-wiki 스키마에 `wikis` 마스터 테이블 추가 + 모든 테이블에 `wiki_id` 컬럼 추가.

```sql
-- 신규: 위키 마스터
wikis
  id          text PK          -- "wiki_{slug}"
  slug        text UNIQUE
  title       text
  description text
  topic       text             -- 원본 주제 입력값
  language    text DEFAULT 'ko'
  owner_id    text             -- 향후 user 테이블 연결
  status      text             -- 'scaffolding' | 'ready' | 'error'
  created_at  timestamp
  updated_at  timestamp

-- 기존 테이블에 wiki_id 추가
sources           + wiki_id text REFERENCES wikis(id)
concepts          + wiki_id text REFERENCES wikis(id)
pages             + wiki_id text REFERENCES wikis(id)
settings          + wiki_id text REFERENCES wikis(id)
knowledge_embeddings + wiki_id text REFERENCES wikis(id)
chat_sessions     + wiki_id text REFERENCES wikis(id)
```

기존 homestyle-wiki 데이터는 `wiki_id = 'wiki_homestyle'`로 마이그레이션.

### URL 라우팅

```
/                           → 플랫폼 홈 (위키 목록)
/create                     → 위키 생성 마법사
/w/[wikiSlug]               → 위키 홈 (에디토리얼)
/w/[wikiSlug]/wiki/[slug]   → 챕터 페이지
/w/[wikiSlug]/concepts      → 개념 목록
/w/[wikiSlug]/concepts/[slug] → 개념 상세
/w/[wikiSlug]/sources       → 소스 목록
/w/[wikiSlug]/chat          → RAG 챗봇
/w/[wikiSlug]/admin         → 관리자 (소유자 전용)
```

### API 라우팅

```
POST /api/wikis                    → 위키 생성 시작
GET  /api/wikis/[id]/status        → 생성 진행상황 (SSE)
POST /api/wikis/[id]/ingest        → 소스 수동 추가
POST /api/wikis/[id]/admin/*       → 기존 admin API (wiki_id 필터 추가)
```

---

## 개발 단계

### Phase 1 — 스키마 & 라우팅 리팩터 (기반 작업)

**작업 목록**

- [ ] `wikis` 테이블 추가 + 기존 테이블 `wiki_id` 컬럼 추가
- [ ] `lib/db/schema.ts` 업데이트
- [ ] `lib/data.ts` 전체 함수에 `wikiId` 파라미터 추가
- [ ] `app/` 라우팅을 `/w/[wikiSlug]/...` 구조로 재편
- [ ] `lib/settings.ts` — `getSetting(key, wikiId)` 형태로 변경
- [ ] 기존 homestyle-wiki 데이터 마이그레이션 스크립트

**완료 기준**: 기존 homestyle-wiki가 `/w/homestyle` 경로로 정상 동작

---

### Phase 2 — 리서치 파이프라인 (핵심 신규)

**작업 목록**

- [ ] Tavily API 클라이언트 (`lib/research.ts`)
  ```ts
  researchTopic(topic: string): Promise<ResearchResult[]>
  // → { title, url, content, score }[]
  ```
- [ ] 구조 설계 LLM 프롬프트 (`lib/scaffold.ts`)
  - Tavily 결과 → GPT-4.1 → `ScaffoldResult` (JSON)
  ```ts
  interface ScaffoldResult {
    wiki_title: string
    description: string
    chapters: { number: string; title: string; subsections: string[] }[]
    concepts: { slug: string; title: string; brief: string; topics: string[] }[]
    topics_config: TopicNode[]
    suggested_rss_feeds: { url: string; label: string }[]
  }
  ```
- [ ] `/create` 위키 생성 마법사 UI
  - Step 1: 주제 입력 (주제명, 설명, 언어)
  - Step 2: 리서치 진행상황 표시 (SSE 스트리밍)
  - Step 3: 생성된 구조 확인/편집 (챕터, 개념 목록)
  - Step 4: 최종 생성

**완료 기준**: 주제 입력 → 챕터/개념 구조 JSON 생성

---

### Phase 3 — 초안 콘텐츠 생성

**작업 목록**

- [ ] `lib/generate.ts` — 콘텐츠 생성 파이프라인
  ```ts
  generateWiki(wikiId: string, scaffold: ScaffoldResult, sources: ResearchResult[]): Promise<void>
  // 1. topics_config 저장
  // 2. chapters(pages) 내용 생성 (챕터당 GPT-4.1 호출)
  // 3. concepts 내용 생성 (배치 처리)
  // 4. editorial 초안 생성
  // 5. 전체 임베딩 빌드
  ```
- [ ] 비동기 처리: 생성에 수분 소요 → `wikis.status` 상태 추적 + SSE 진행상황
- [ ] 각 단계별 부분 실패 시 재시도 가능하도록 체크포인트 설계

**완료 기준**: 주제 → 완성된 위키 (챕터, 개념, 에디토리얼) 자동 생성

---

### Phase 4 — 지속 업데이트 자동화

**작업 목록**

- [ ] `lib/ingest.ts` + `lib/synthesize.ts` — `wikiId` 파라미터 추가
- [ ] RSS 피드 관리 테이블 (`rss_feeds`: wikiId, url, label, last_fetched)
- [ ] Scaffold 시 Tavily 제안 RSS 피드 자동 등록
- [ ] GitHub Actions 워크플로우: 위키별 `wikiId` 기반 스케줄 수집
- [ ] `/api/wikis/[id]/admin/ingest` — 수동 소스 추가 API

**완료 기준**: 신규 소스 자동 수집 → 위키 자동 업데이트

---

### Phase 5 — 플랫폼 UI

**작업 목록**

- [ ] 플랫폼 홈 (`/`): 내 위키 목록 + 새 위키 만들기 CTA
- [ ] 위키 홈 (`/w/[slug]`): 에디토리얼 + 최근 업데이트
- [ ] 위키 내 네비게이션: 기존 Header/WikiIndexDrawer를 위키 컨텍스트 인식으로 수정
- [ ] 관리자 대시보드: 위키별 Admin 탭 (기존 `/admin` 구조 재사용)
- [ ] 위키 생성 상태 페이지: 생성 중 진행상황 표시

---

### Phase 6 — SaaS 준비 (향후)

**작업 목록**

- [ ] 사용자 계정 (OAuth: Google, GitHub)
- [ ] 위키별 공개/비공개 설정
- [ ] 커스텀 도메인 지원
- [ ] 플랜 / 사용량 제한 (위키 수, 월 소스 수집 횟수)
- [ ] 결제 연동 (Stripe)
- [ ] 랜딩 페이지

---

## 기술 스택

### 신규 추가

| 역할 | 기술 | 비고 |
|---|---|---|
| 웹 리서치 | Tavily API | `@tavily/core` |
| 비동기 진행상황 | Server-Sent Events (SSE) | Next.js Route Handler |
| 작업 큐 (향후) | Vercel Queue 또는 Upstash QStash | 초안 생성 장시간 작업 |
| 사용자 인증 (Phase 6) | Auth.js v5 + Google/GitHub OAuth | 기존 구조 확장 |
| 결제 (Phase 6) | Stripe | |

### 재사용 (homestyle-wiki 그대로)

- Next.js 15 App Router + TypeScript + Tailwind CSS v4
- Neon Postgres + pgvector + Drizzle ORM
- OpenAI (`getOpenAI()` lazy init 패턴 유지)
- `lib/ingest.ts`, `lib/synthesize.ts`, `lib/embed.ts` 파이프라인
- `components/MarkdownRenderer`, `DiffView`, `SearchBox` 등 UI 컴포넌트

### 환경변수 추가

```env
TAVILY_API_KEY=
NEXT_PUBLIC_APP_URL=
# Phase 6
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

---

## MVP 범위 (1인 사용 기준)

Phase 1 → 2 → 3 → 4 완료 시 MVP.  
Phase 5는 병행 진행 (UI 없으면 개발/검증 불가).  
Phase 6는 외부 출시 시 진행.

**MVP 완료 기준**: 주제 입력 → 위키 자동 생성 → 자동 업데이트 동작 확인

---

## 개발 순서 요약

```
Week 1-2: Phase 1 (스키마 리팩터)
Week 3-4: Phase 2 (Tavily 리서치 + 구조 생성)
Week 5-6: Phase 3 (콘텐츠 초안 생성)
Week 7:   Phase 4 (지속 업데이트 자동화)
Week 8:   Phase 5 (플랫폼 UI 정리)
이후:     Phase 6 (SaaS 준비, 외부 출시)
```
