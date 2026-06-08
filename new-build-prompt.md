# homestyle Wiki — 개발 프롬프트

homestyle(홈스타일) 인테리어 트렌드의 지식 위키 플랫폼을 구축하는 단계별 프롬프트.
각 단계는 이전 단계가 완료된 상태에서 순서대로 입력한다.

---

## 설계 원칙 (Karpathy LLM Wiki 기반)

Andrej Karpathy의 LLM Wiki 패턴을 적용한다.
참고: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**핵심 사상**: RAG는 매 쿼리마다 지식을 재발견한다. LLM Wiki는 지식을 한 번 컴파일하고 누적한다.
"정보는 한 번 처리되고, 매번 다시 파생되지 않는다."

### 3계층 구조

```
Raw Sources (읽기 전용)
    RSS 피드, 업로드 문서, kb/wiki/ 기존 파일
    ↓ Ingest
Wiki Pages (LLM이 작성·유지)
    concepts 테이블: Homestyle 개념 페이지 (신규 생성 + 지속 업데이트)
    pages 테이블: 챕터 위키
    ↓ Lint
Schema (구조 정의)
    data
```

### 운영 원칙

- **누적**: 새 소스가 ingest되면 관련 concepts를 자동 업데이트/생성
- **Living editorial**: 지식이 누적되면 editorial을 AI가 갱신 초안 생성, 사람이 검토 후 publish
- **Lint**: 주기적으로 위키 건강도 점검 (고아 개념, 빈 콘텐츠, 오래된 개념)
- **임포트 후 DB가 단일 소스**: kb/wiki/는 초기 seed, 이후 read-only 보관
- **자동 파이프라인**: RSS → 스코어 6점↑ → 자동 ingest → concept 합성 → editorial 초안
- **챗봇**: 로그인 필수, 세션 히스토리, wiki 페이지 인용

## 스택

| 역할 | 선택 |
|------|------|
| 프레임워크 | Next.js 15 App Router |
| DB | Vercel Postgres (Neon 기반, pgvector 지원) |
| ORM | Drizzle ORM + drizzle-kit |
| 인증 | Auth.js v5 (credentials provider) |
| AI | OpenAI (gpt-4.1-mini 요약/합성, text-embedding-3-small) |
| 배포 | Vercel |

---

## Phase 1 — 프로젝트 셋업

```
Next.js 15(App Router), TypeScript, Tailwind CSS로 새 프로젝트를 셋업해줘.

프로젝트명: homestyle-wiki
패키지 매니저: npm

설치 패키지:
- @vercel/postgres
- drizzle-orm drizzle-kit
- next-auth@beta
- openai
- remark remark-gfm remark-html
- react-force-graph-2d
- @tailwindcss/typography

디렉터리 구조:
app/              Next.js 페이지 + API Routes
components/       UI 컴포넌트
lib/              유틸리티, ingest, 합성, 데이터 fetch
lib/db/           Drizzle 스키마 + 클라이언트
scripts/          Python 스크립트 (임포트 + RSS 수집)
.github/workflows/
migrations/       SQL 마이그레이션 파일
kb/wiki/          기존 md 파일 보관 (임포트 소스, 이후 read-only)

.env.example:
# Vercel Postgres (Vercel 대시보드에서 DB 연결 시 자동 주입)
POSTGRES_URL=postgres://...
POSTGRES_URL_NON_POOLING=postgres://...

# Auth.js
AUTH_SECRET=임의_32자_이상_문자열
AUTH_ADMIN_EMAIL=admin@example.com
AUTH_ADMIN_PASSWORD=강력한_패스워드

# OpenAI
OPENAI_API_KEY=sk-...

# Ingest
INGEST_SECRET=임의_문자열

tailwind.config: @tailwindcss/typography 추가. accent 색상 커스텀 (rose-600 기준).
```

---

## Phase 2 — DB 스키마 + 마이그레이션

```
DB 스키마를 작성해줘.

## migrations/001_initial.sql

CREATE EXTENSION IF NOT EXISTS vector;

### sources — 원문 + AI 요약 통합
CREATE TABLE sources (
  id                text PRIMARY KEY,        -- "source_{slug}"
  title             text NOT NULL,
  url               text,
  publisher         text,
  published_at      text,
  source_type       text DEFAULT 'external', -- external / internal
  raw_content       text,
  ai_summary        text,                    -- 6섹션 한국어 요약 마크다운
  one_line_summary  text,
  topics            text[] DEFAULT '{}',
  status            text DEFAULT 'done',     -- processing / done / error
  error_message     text,
  synthesis_result  jsonb DEFAULT '{}',      -- {concepts_updated:[], concepts_created:[], synthesized_at:""}
  created_at        timestamptz DEFAULT now(),
  updated_at        timestamptz DEFAULT now()
);

### concepts — Homestyle 핵심 개념 (LLM이 지속 유지)
CREATE TABLE concepts (
  id               text PRIMARY KEY,         -- "concept_{slug}"
  title            text NOT NULL,
  slug             text UNIQUE NOT NULL,
  brief            text,
  aliases          text[] DEFAULT '{}',
  topics           text[] DEFAULT '{}',
  related_concepts text[] DEFAULT '{}',      -- slug 배열
  concept_type     text,                     -- style / lifestyle / spatial / functional / material / market
  concept_status   text DEFAULT 'candidate', -- canonical / candidate / supporting
  confidence       int DEFAULT 0,            -- 신뢰도 점수 (0-100)
  content          text,                     -- 마크다운 본문 (LLM이 누적 업데이트)
  source_count     int DEFAULT 0,            -- 이 개념에 기여한 소스 수
  last_synthesized_at timestamptz,           -- 마지막 LLM 합성 시각
  updated_at       timestamptz DEFAULT now()
);

### pages — Wiki 챕터 페이지
CREATE TABLE pages (
  id               text PRIMARY KEY,         -- "page_{slug}"
  slug             text UNIQUE NOT NULL,
  title            text NOT NULL,
  chapter_number   text,                     -- "01"~"13", "appendix-1", "appendix-2"
  subsections      jsonb DEFAULT '[]',       -- [{number, title}]
  summary          text,
  topics           text[] DEFAULT '{}',
  content          text,                     -- 마크다운 본문
  updated_at       timestamptz DEFAULT now()
);

### knowledge_embeddings — pgvector RAG
CREATE TABLE knowledge_embeddings (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ref_type   text NOT NULL,   -- "source" / "concept" / "page"
  ref_id     text NOT NULL,
  content    text NOT NULL,
  embedding  vector(1536),
  metadata   jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

CREATE INDEX ON knowledge_embeddings
  USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64);

### settings — 앱 전역 설정
CREATE TABLE settings (
  key        text PRIMARY KEY,
  value      text,
  updated_at timestamptz DEFAULT now()
);

-- 초기 키:
-- editorial_content     홈 에디토리얼 마크다운 (living document)
-- editorial_versions    버전 JSON 배열 (최대 20개)
-- topics_config         topic-map 기반 구조 JSON
-- metrics_content       Homestyle-metrics.md 기반 수치 카드 JSON
-- graph_data            지식 그래프 nodes+links JSON
-- ingest_log            최근 ingest 이력 JSON [{source_id, title, concepts_updated, concepts_created, date}]

### chat_sessions — RAG 챗봇 히스토리
CREATE TABLE chat_sessions (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_email  text NOT NULL,
  title       text,
  messages    jsonb DEFAULT '[]', -- [{role, content, citations:[{ref_type,ref_id,title}], created_at}]
  created_at  timestamptz DEFAULT now(),
  updated_at  timestamptz DEFAULT now()
);

## VIEW

CREATE VIEW knowledge_view AS
  SELECT id, 'source' AS type, title, id AS slug,
         one_line_summary AS summary, topics, updated_at
  FROM sources WHERE status = 'done'
  UNION ALL
  SELECT id, 'concept', title, slug, brief, topics, updated_at
  FROM concepts
  UNION ALL
  SELECT id, 'page', title, slug, summary, topics, updated_at
  FROM pages;

## pgvector 함수

CREATE OR REPLACE FUNCTION match_knowledge_chunks(
  query_embedding vector(1536),
  match_threshold float DEFAULT 0.32,
  match_count int DEFAULT 8
) RETURNS TABLE (
  id uuid, ref_type text, ref_id text,
  content text, similarity float, metadata jsonb
) LANGUAGE sql STABLE AS $$
  SELECT id, ref_type, ref_id, content,
    1 - (embedding <=> query_embedding) AS similarity,
    metadata
  FROM knowledge_embeddings
  WHERE 1 - (embedding <=> query_embedding) > match_threshold
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;

## Drizzle 스키마

lib/db/schema.ts 를 작성해줘.
drizzle-orm/pg-core 사용. 위 테이블과 동일한 구조.
vector 타입은 customType으로 정의:
  const vector = customType<{ data: number[]; driverData: string }>({
    dataType() { return 'vector(1536)' },
    toDriver(value) { return JSON.stringify(value) },
    fromDriver(value) { return JSON.parse(value as string) },
  })

## 적용 방법

psql $POSTGRES_URL_NON_POOLING -f migrations/001_initial.sql
```

---

## Phase 3 — md 파일 → DB 일괄 임포트

```
kb/wiki/ 디렉터리의 기존 md 파일을 Vercel Postgres로 임포트하는 스크립트를 작성해줘.
파일: scripts/import_from_md.py

이 스크립트는 최초 1회만 실행한다.
pip install psycopg2-binary python-frontmatter 필요.

## 실행법

python3 scripts/import_from_md.py \
  --postgres-url "$POSTGRES_URL_NON_POOLING" \
  --wiki-dir ./kb/wiki \
  [--dry-run]

## 임포트 대상 및 처리

### 1. concepts (kb/wiki/concepts/*.md)

대상: kb/wiki/concepts/ 직속 .md 파일만 (data/ 하위 제외, _ 로 시작하는 파일 제외)
slug = slugify(파일명 stem), id = "concept_" + slug
프론트매터 매핑:
  aliases           → aliases
  related_concepts  → related_concepts
  concept_type      → concept_type
  concept_status    → concept_status (없으면 'candidate')
  confidence.score  → confidence (없으면 0)
brief: body에서 "### 한 줄 정의" 이후 첫 단락 추출 (없으면 NULL)
body 전체 → concepts.content
source_count = 0, last_synthesized_at = NULL
upsert (ON CONFLICT DO UPDATE).

### 2. pages (kb/wiki/pages/01-*/ ~ 06-*/)

대상 디렉터리: 01-* ~ 06-* 서브디렉터리 (00-overview/, data/, templates/ 제외)
제외 파일: index.md, source-notes.md, README.md
chapter_number = 부모 디렉터리명 앞 두 자리 (예: "01-trend-history" → "01")
slug = 파일명 stem, id = "page_" + slug
title: 첫 번째 # 헤딩
summary: "TL;DR" 섹션 첫 단락 → 없으면 첫 ## 섹션 아래 첫 단락 → 없으면 앞 200자
subsections: ## 헤딩 → [{number, title}]
content: 전체 본문
upsert.

### 3. editorial

kb/wiki/editorial/main.md 가 없으면 빈 값으로 초기화 (로그 출력):
  → settings key='editorial_content' = ''
  → settings key='editorial_versions' = '[]'
파일이 있으면:
  → settings key='editorial_content' = 전체 내용
  → settings key='editorial_versions'
    [{label:"Initial import", content:..., saved_at:..., is_draft:false}]

### 4. topics (kb/wiki/topics/topic-map.md)

H2 헤딩 패턴: "## {번호} · {한국어 제목} ({영문 레이블})" 파싱
"### 서브토픽" 아래 리스트 항목 → subtopics 배열
→ JSON → settings key='topics_config'
[{ number:"01", title:"연도별/시기별 트렌드", label:"Trend History", subtopics:[...] }]

### 5. metrics

kb/wiki/metrics/Homestyle-metrics.md 가 없으면 빈 배열로 초기화 (로그 출력):
  → settings key='metrics_content' = '[]'
파일이 있으면 Card 섹션 파싱 → JSON → settings key='metrics_content'
[{ id:"card-01", title, stat, definition, source, message, url }]

### 6. sources (kb/wiki/sources/*.md) — 선택

kb/wiki/sources/ 가 없으면 skip (로그 출력).
있는 경우:
  id = "source_" + slugify(파일명 stem)
  frontmatter: title, url, publisher, published_at
  raw_content = 본문, status = 'done', synthesis_result = {}
  upsert.

### 7. summaries (kb/wiki/summaries/*.md) — 선택

kb/wiki/summaries/ 가 없으면 skip (로그 출력).
있는 경우:
  동일 stem의 source 찾아 매칭:
    ai_summary, one_line_summary, topics UPDATE
  없으면 sources INSERT.

## 완료 후 출력

concepts: N개 / pages: N개 / sources: N개 (skip된 항목 로그 출력)
settings 키: editorial_content, editorial_versions, topics_config, metrics_content

## 주의: 임포트 후 embeddings 없음

이 스크립트는 DB 레코드만 생성한다. knowledge_embeddings는 비어 있는 상태.
배포 후 반드시 /admin → Health 탭 → "전체 Embeddings 재빌드" 실행 필요.
```

---

## Phase 4 — DB 클라이언트 + 타입 + 데이터 레이어

```
DB 클라이언트, 타입 정의, 데이터 fetch 함수를 작성해줘.

## lib/db/index.ts

import { drizzle } from 'drizzle-orm/vercel-postgres'
import { sql } from '@vercel/postgres'
import * as schema from './schema'
export const db = drizzle(sql, { schema })
export { sql }

## lib/types.ts

interface SourceItem {
  id: string; title: string; url?: string; publisher?: string;
  published_at?: string; source_type: string;
  one_line_summary?: string; ai_summary?: string;
  topics: string[]; status: string;
  synthesis_result: SynthesisResult;
  created_at: string;
}
interface SynthesisResult {
  concepts_updated: string[]   // concept slugs
  concepts_created: string[]   // concept slugs
  synthesized_at: string
}
interface ConceptItem {
  id: string; title: string; slug: string; brief?: string;
  aliases: string[]; topics: string[]; related_concepts: string[];
  concept_type?: string; concept_status: string; confidence: number;
  content?: string; source_count: number;
  last_synthesized_at?: string; updated_at: string;
}
interface WikiPageItem {
  id: string; slug: string; title: string; chapter_number: string;
  subsections: { number: string; title: string }[];
  summary?: string; topics: string[];
  content?: string; updated_at: string;
}
interface KnowledgeItem {
  id: string; type: 'source' | 'concept' | 'page';
  title: string; slug: string; summary?: string;
  topics: string[]; updated_at: string;
}
interface TopicNode { number: string; title: string; label: string; subtopics: string[]; }
interface MetricCard { id: string; title: string; stat: string; definition: string; source: string; message: string; url: string; }
interface KnowledgeGraphLink { source: string; target: string; }
interface KnowledgeGraphData { nodes: KnowledgeGraphNode[]; links: KnowledgeGraphLink[]; built_at: string; }
interface KnowledgeGraphNode {
  id: string; type: 'topic' | 'source' | 'concept'; label: string;
  slug?: string; brief?: string; description?: string;
  publisher?: string; published_at?: string; topics?: string[];
}
interface ChatMessage { role: 'user' | 'assistant'; content: string; citations?: Citation[]; created_at: string; }
interface Citation { ref_type: string; ref_id: string; title: string; }
interface ChatSession { id: string; title: string; messages: ChatMessage[]; updated_at: string; }
interface IngestLogEntry { source_id: string; title: string; concepts_updated: string[]; concepts_created: string[]; date: string; }

## lib/data.ts

unstable_noStore() 적용. Drizzle 쿼리 사용. 에러 시 빈 배열/null 반환.

- getSources(): SourceItem[]
- getSourceById(id): SourceItem|null
- getConceptItems(): ConceptItem[]         -- slug ASC
- getConceptBySlug(slug): ConceptItem|null
- getWikiPages(): WikiPageItem[]           -- chapter_number ASC
- getPageBySlug(slug): WikiPageItem|null
- getKnowledgeItems(): KnowledgeItem[]     -- knowledge_view raw SQL
- getEditorialContent(): string
- getEditorialVersions(): {label,content,saved_at,is_draft}[]
- getTopicsConfig(): TopicNode[]
- getMetricsContent(): MetricCard[]
- getKnowledgeGraph(): KnowledgeGraphData
- getIngestLog(): IngestLogEntry[]         -- settings key='ingest_log'

## lib/markdown.ts

renderMarkdown(raw: string): Promise<string>
remark → remark-gfm → remark-html.

## lib/slug.ts

slugify(text: string): string
소문자 + 영숫자 + 한글 + 하이픈만, 80자 제한.
```

---

## Phase 5 — 레이아웃 + 인증

```
앱 레이아웃, 네비게이션, Auth.js v5 인증을 구현해줘.

## Auth.js v5 설정

auth.ts (프로젝트 루트):
- Credentials provider
- authorize: credentials.email === AUTH_ADMIN_EMAIL && credentials.password === AUTH_ADMIN_PASSWORD
- JWT 세션 (DB adapter 불필요)

app/api/auth/[...nextauth]/route.ts:
  import { handlers } from '@/auth'
  export const { GET, POST } = handlers

## 미들웨어

/admin/** 및 /chat: auth() 세션 없으면 /auth/signin?callbackUrl=... 리다이렉트.

## app/layout.tsx

다크 헤더 (bg-neutral-950): 로고 "Homestyle Wiki" + 데스크탑 nav + 모바일 햄버거.
max-w-7xl mx-auto px-4 sm:px-6.
ChatPopup 포함.

네비게이션:
- Home (/)
- Sources (/sources)
- Knowledge → Graph(/knowledge) · Concepts(/concepts) · Wiki(/wiki)
- Metrics (/metrics)
- Chat (/chat)
- Admin (/admin)   로그인 시만
- 로그인/로그아웃

## app/auth/signin/page.tsx

이메일 + 패스워드 폼. signIn('credentials', ...).
에러 시 "이메일 또는 패스워드가 올바르지 않습니다." 표시.

## app/auth/signout/route.ts

POST → signOut() → / 리다이렉트.

## EmbeddedChrome

"use client". ?popup=1 감지 → body[data-embedded="true"].
globals.css:
  body[data-embedded="true"] > header { display: none }
  body[data-embedded="true"] > main { padding-top: 1rem }
```

---

## Phase 6 — 홈 페이지

```
홈 랜딩 페이지를 구현해줘.

## / (홈)

서버 컴포넌트.
- getEditorialContent() → 마크다운 렌더링
- getConceptItems() → source_count 높은 순 상위 6개 카드 (가장 많이 인용된 개념)
- getSources() → 최신 4개 카드

2컬럼 레이아웃:
- 좌: 에디토리얼 콘텐츠 (prose)
- 우: 핵심 개념 카드 + 최신 소스 카드

상단 통계 배너: Sources N개 · Concepts N개 · 마지막 업데이트 날짜
```

---

## Phase 7 — Ingest + Concept 합성

```
신규 소스 처리 파이프라인과 LLM Wiki 합성 로직을 구현해줘.
Karpathy LLM Wiki 패턴: 소스가 ingest되면 관련 concepts를 자동으로 업데이트하거나 신규 생성한다.

## lib/ingest.ts

runIngest(params: {
  title: string
  raw_content: string
  url?: string
  publisher?: string
  source_type?: string
}): Promise<string>  -- 반환: source_id

처리 순서:
1. sources INSERT status='processing'
   id = "source_" + slugify(title)
2. gpt-4.1-mini → 한국어 6섹션 요약:
   ## 한 줄 요약 / ## 핵심 메시지 / ## 주요 수치와 데이터
   ## Homestyle 시사점 / ## 액션 아이템 / ## 관련 개념
3. sources UPDATE ai_summary, one_line_summary, topics, status='done'
4. knowledge_embeddings INSERT (lib/embed.ts):
   - raw_content 청크 (ref_type='source')
   - ai_summary 전체 1개 청크 추가
5. synthesizeConcepts() 호출 (lib/synthesize.ts)
6. sources UPDATE synthesis_result
7. ingest_log에 이번 ingest 결과 prepend (최대 50개)
8. 에러 시: status='error', error_message 저장

## lib/embed.ts

rebuildEmbeddings(refType, refId, chunks): Promise<void>
  knowledge_embeddings WHERE ref_type=refType AND ref_id=refId DELETE
  → text-embedding-3-small 배치 호출
  → knowledge_embeddings INSERT

chunkText(text, maxLen=1200, overlap=150): string[]

## lib/synthesize.ts  ← LLM Wiki 핵심 모듈

### synthesizeConcepts()

synthesizeConcepts(params: {
  sourceId: string
  aiSummary: string
  topics: string[]
}): Promise<SynthesisResult>

처리:
1. DB에서 concepts 전체 로드 (id, title, slug, brief, topics, content 앞 500자)
2. topics 기반 1차 후보 필터 (source.topics ∩ concept.topics)
3. GPT-4.1 호출 — concept 매칭 + 업데이트 결정:

   시스템 프롬프트:
   "당신은 Homestyle Wiki의 지식 합성 에이전트입니다.
   새 소스 요약을 읽고 기존 개념 중 업데이트가 필요한 것을 파악하세요.
   기존 개념에 없는 새로운 Homestyle 개념이 발견되면 신규 생성을 제안하세요.
   각 개념의 content는 마크다운으로, 기존 내용과 충돌 없이 새 정보를 추가합니다."

   입력:
   - ai_summary (새 소스 요약)
   - existing_concepts: [{slug, title, brief, content_preview}] (후보 목록)

   출력 JSON:
   {
     updates: [
       { slug: "Homestyle-개요", additions: "## 2025년 업데이트\n..." }
     ],
     new_concepts: [
       { title: "신규 개념명", slug: "sin-gyu-gaenyeom", brief: "...", content: "..." }
     ]
   }

4. updates 처리:
   - concepts.content에 additions를 append
   - source_count += 1
   - last_synthesized_at = now()
   - rebuildEmbeddings('concept', id, chunks)

5. new_concepts 처리:
   - concepts INSERT
   - rebuildEmbeddings('concept', id, chunks)

6. SynthesisResult 반환 { concepts_updated, concepts_created, synthesized_at }

### synthesizeEditorial()

synthesizeEditorial(): Promise<string>  -- 반환: 생성된 editorial 초안

처리:
1. 현재 editorial_content 로드
2. 최근 업데이트된 concepts 10개 (last_synthesized_at DESC)
3. 최신 sources 5개 (one_line_summary + topics)
4. GPT-4.1 호출:

   시스템 프롬프트:
   "당신은 Homestyle Wiki의 수석 에디터입니다.
   최신 Homestyle 지식 동향을 반영해서 홈 에디토리얼을 업데이트하세요.
   기존 에디토리얼의 구조와 톤을 유지하면서, 새로 추가된 지식을 자연스럽게 통합하세요.
   마크다운으로 작성하고, 특정 개념과 소스를 구체적으로 언급하세요."

   입력:
   - current_editorial
   - recent_concepts: [{title, brief, topics}]
   - recent_sources: [{title, one_line_summary, topics}]

5. 결과를 editorial_versions에 draft로 추가:
   { label: "AI 초안 (날짜)", content: 새_내용, saved_at: now(), is_draft: true }
6. editorial_versions는 최대 20개 유지
7. editorial_content는 변경 안 함 (사람이 검토 후 publish)

### lintWiki()

lintWiki(): Promise<LintIssue[]>

interface LintIssue {
  type: 'empty_content' | 'no_topics' | 'no_sources' | 'stale' | 'orphan'
  concept_slug: string
  title: string
  detail: string
}

점검 항목:
- empty_content: content가 100자 미만
- no_topics: topics 배열이 빈 경우
- no_sources: source_count === 0
- stale: last_synthesized_at이 NOT NULL이고 90일 이상 지난 경우
  (last_synthesized_at IS NULL인 경우는 아직 합성 전 상태이므로 no_sources로 충분)
- orphan: related_concepts에 존재하지 않는 slug 참조

## API Routes

POST /api/ingest
  Authorization: Bearer {INGEST_SECRET}
  body: { title, raw_content, url?, publisher?, source_type? }
  → runIngest() 호출
  export const runtime = "nodejs", maxDuration = 120

POST /api/sources/upload
  auth() 세션 확인.
  { title, content, url? } or file (.md/.txt)
  → runIngest({ source_type: 'internal' })
  export const runtime = "nodejs", maxDuration = 120

GET /api/sources/exists?url=
  { exists: boolean }

DELETE /api/source?id=
  auth() 세션 확인.
  knowledge_embeddings + sources DELETE.

POST /api/admin/synthesize-editorial
  auth() 세션 확인.
  → synthesizeEditorial()
  반환: { draft_label, preview: 앞 300자 }
  export const runtime = "nodejs", maxDuration = 60

POST /api/admin/lint
  auth() 세션 확인.
  → lintWiki()
  반환: LintIssue[]
```

---

## Phase 8 — Sources 페이지

```
소스 목록, 상세, 업로드 페이지를 구현해줘.

## /sources

서버 컴포넌트 → getSources() → SourceTable 클라이언트 컴포넌트.

SourceTable:
- 컬럼: No / Topic / Title / 한 줄 요약 / Publisher / Date / 삭제
- 컬럼 정렬 (asc/desc)
- Title 클릭: 인라인 패널
  - 메타 + one_line_summary + topics
  - synthesis_result: "개념 N개 업데이트, N개 신규 생성" 표시 (있을 때만)
  - "전체 보기 →" 링크
- 삭제: DELETE /api/source → optimistic UI

## /sources/upload

로그인 필수. UploadForm 클라이언트 컴포넌트.
탭 1: URL 입력 → Jina Reader fetch → POST /api/sources/upload
탭 2: 텍스트 직접 입력
탭 3: 파일 업로드 (.md/.txt)
완료 → /sources 이동.

## /sources/[id]

서버 컴포넌트. getSourceById(id).
상단: 메타 (publisher / date / url / topics)
synthesis_result 있으면: "이 소스로 업데이트된 개념" 배지 목록 + 링크
2섹션:
- AI 요약: renderMarkdown(ai_summary)
- 원문: renderMarkdown(raw_content), 접기/펼치기

## MarkdownRenderer

"use client". props: html. prose 클래스.
```

---

## Phase 9 — Concepts + Wiki + Admin 에디터

```
개념, Wiki 페이지, 그리고 모든 콘텐츠를 관리하는 /admin을 구현해줘.

## /concepts

ConceptGrid 클라이언트 컴포넌트:
- 카드 그리드 (2-3열): 개념명 + brief + topics 배지 + source_count 표시
- getTopicsConfig()로 토픽 그룹 필터 버튼
- 카드 클릭: 인라인 패널 (brief + aliases + related_concepts + last_synthesized_at + "전체 보기 →")

## /concepts/[slug]

getConceptBySlug(slug). renderMarkdown(content).
사이드: aliases / related_concepts 링크 / source_count / last_synthesized_at.

## /wiki

getWikiPages() → chapter_number 순 카드 그리드.

## /wiki/[slug]

getPageBySlug(slug). renderMarkdown(content).
좌측 WikiChapterDrawer: 챕터 목록 (데스크탑 고정).

## /admin — 탭 구조 (로그인 필수)

서버 컴포넌트에서 auth() → 미인증 시 리다이렉트.

### Tab 1: Editorial

좌우 split: textarea + 미리보기.

버전 드롭다운:
- AI 초안(is_draft=true)은 "AI 초안 (날짜)" 레이블로 구분 표시
- 선택 → textarea 로드
- 초안 선택 후 저장하면 publish (is_draft → false)

저장 버튼: PUT /api/admin/editorial { content }
  1. editorial_versions에 현재 content push (최대 20개)
  2. settings upsert editorial_content

"AI 초안 생성" 버튼: POST /api/admin/synthesize-editorial
  → 스피너 → 완료 시 버전 드롭다운에 새 초안 추가 + toast "초안이 생성되었습니다"

### Tab 2: Concepts

좌: 개념 목록 (slug 정렬, 검색 가능)
    각 항목에 concept_status 배지 + source_count + last_synthesized_at 표시
우: 선택된 개념 편집 폼
  - title, slug, brief
  - concept_type: 드롭다운 (style / lifestyle / spatial / functional / material / market)
  - concept_status: 드롭다운 (canonical / candidate / supporting)
  - confidence: 숫자 입력 (0-100)
  - aliases: textarea (줄 구분)
  - topics: textarea (줄 구분, 자유 입력)
  - related_concepts: textarea (slug 줄 구분)
  - content: 마크다운 textarea + 미리보기 토글
저장: PUT /api/admin/concept
  → concepts UPDATE + rebuildEmbeddings('concept', id, chunks)

### Tab 3: Wiki Pages

좌: 페이지 목록 (chapter_number 순)
우: 선택된 페이지 편집 폼
  - title, chapter_number, summary
  - subsections: [{number, title}] JSON 편집
  - content: 마크다운 textarea + 미리보기 토글
저장: PUT /api/admin/page
  → pages UPDATE + rebuildEmbeddings('page', id, chunks)

### Tab 4: Metrics

metrics_content (MetricCard[] JSON) 편집.
테이블 형태 카드 목록 + 인라인 편집.
저장: PUT /api/admin/metrics

### Tab 5: Wiki Health (Lint)

"점검 실행" 버튼: POST /api/admin/lint
결과 테이블:
- type별 색상 구분 (empty=red, stale=yellow, orphan=orange 등)
- 각 이슈에 "편집 →" 링크 (Tab 2 해당 concept로 이동)

"전체 Embeddings 재빌드" 버튼: POST /api/admin/rebuild-embeddings
  auth() 세션 확인.
  concepts 전체 + pages 전체를 순회하며 rebuildEmbeddings() 호출.
  완료 시 재빌드된 레코드 수 반환. export const runtime = "nodejs", maxDuration = 300.
  초기 배포 후 반드시 1회 실행 (import_from_md.py는 embeddings를 생성하지 않음).

하단: Ingest Log 섹션
- getIngestLog() → 최근 50건 목록
- 각 항목: 날짜 / 소스 제목 / 업데이트 개념 수 / 신규 생성 개념 수
- 클릭: 상세 (업데이트된 개념 slug 목록)

### Tab 6: Graph

"그래프 재생성" 버튼 + 마지막 생성 시각.
POST /api/graph/rebuild.

## API Routes (모두 auth() 확인)

PUT /api/admin/editorial
PUT /api/admin/concept
PUT /api/admin/page
PUT /api/admin/metrics
POST /api/admin/synthesize-editorial  (Phase 7에서 정의)
POST /api/admin/lint                  (Phase 7에서 정의)
POST /api/admin/rebuild-embeddings
POST /api/graph/rebuild
```

---

## Phase 10 — Knowledge Graph

```
DB 데이터 기반 지식 그래프를 구현해줘.

## POST /api/graph/rebuild (로그인 필수)

DB 쿼리:
- concepts 전체 (id, title, slug, brief, topics, related_concepts, source_count)
- sources WHERE status='done' 최신 50개
- getTopicsConfig()로 토픽 목록

노드 생성:
- topic: topics_config 각 항목 (id="topic_{slug}", label=title)
- concept: { id, type:'concept', label:title, slug, brief, topics, source_count }
- source: { id, type:'source', label:title, publisher, published_at, description:one_line_summary, topics }

링크 생성:
- topic-concept: concept_type → chapter 매핑으로 결정
    style       → "스타일 사전" (03)
    lifestyle   → "2026 인테리어 테마" (02)
    spatial     → "공간별 트렌드" (04)
    functional  → "카테고리 맵" (05)
    market      → "마케팅 인사이트" (06)
    material    → "스타일 사전" (03) + "공간별 트렌드" (04) 양쪽 연결
    concept_type 없으면 링크 생략
- topic-source: source.topics (AI 생성) ∩ topic.label (대소문자 무시)
- concept-concept: concept.related_concepts
- concept-source: concept.topics ∩ source.topics (교집합 1개 이상)

settings upsert key='graph_data', value=JSON.stringify({ nodes, links, built_at })

## /knowledge

서버 컴포넌트. getKnowledgeGraph().
비어 있으면 재생성 안내.
KnowledgeGraph 클라이언트 컴포넌트 렌더링.

## KnowledgeGraph 컴포넌트

react-force-graph-2d (dynamic import, ssr: false).

색상: topic=#d4d4d8, source=#ec4899, concept=#22d3ee
배경: #080a12
cooldownTicks:80, warmupTicks:60
nodeRelSize:1, nodeVal: topic=100/concept=40/source=31
마운트 시 zoom(0.35).
onEngineStop: hasFittedRef로 최초 1회만 zoomToFit(250ms, 20px).

커스텀 캔버스: 원(반지름 topic=10/concept=6.3/source=5.6) + 레이블.
concept 노드 크기: source_count에 비례해서 +20% 까지 가중치.

인터랙션:
- 좌클릭: NodePanel 인라인 패널
  concept: brief + topics + source_count + last_synthesized_at + "전체 보기 →"
  source: description + publisher + synthesis_result + "전체 보기 →"
  topic: 연결 개념 수 + 소스 수
- 우클릭: 센터링 + zoom 3배
- 패널 외부 클릭: 닫기

필터: topic/concept/source 토글, 키워드 검색.
토글 시 350ms 후 fitView(220ms).
```

---

## Phase 11 — Metrics 페이지

```
Homestyle 지표 대시보드를 구현해줘.

## /metrics

서버 컴포넌트. getMetricsContent() → MetricCard[].

레이아웃:
상단: "Homestyle 지표 레퍼런스" + 데이터 출처 안내
카드 그리드 (2-3열):
  - stat: text-3xl font-bold
  - title: 카드 헤더
  - definition: 작은 텍스트
  - message: 인용구 스타일
  - source: 링크 → url

데이터 없으면: "Admin → Metrics 탭에서 설정하세요." 안내.
```

---

## Phase 12 — RAG 챗봇

```
pgvector 기반 RAG 챗봇을 구현해줘.
응답에 wiki 페이지 인용을 포함한다.

## POST /api/chat

auth() 세션 확인.
body: { message: string, session_id?: string }

처리:
1. text-embedding-3-small로 질문 임베딩
2. match_knowledge_chunks() raw SQL (임계값 0.32, 최대 8개)
3. 청크의 ref_type/ref_id → 제목 조회 (citations 구성)
4. 청크 + 세션 히스토리 → GPT-4.1 스트리밍

   시스템 프롬프트:
   "당신은 Homestyle Wiki의 AI 어시스턴트입니다.
   제공된 컨텍스트(concepts, pages, sources)를 바탕으로 한국어로 답변하세요.
   답변 말미에 참고한 위키 페이지나 소스를 간략히 언급하세요.
   컨텍스트에 없는 내용은 솔직하게 모른다고 답하세요."

5. ReadableStream 스트리밍 (text/event-stream)
6. 완료 후 chat_sessions upsert
   - messages에 { role, content, citations, created_at } 추가
   - session_id 없으면 신규 생성, title = 첫 질문 앞 30자

export const runtime = "nodejs", maxDuration = 60

## /chat

로그인 필수. ChatInterface 클라이언트 컴포넌트.
좌: 세션 목록 사이드바 (최신순, "새 대화" 버튼)
우: 채팅 영역
  - 입력 + 전송 (Enter)
  - 스트리밍 실시간 렌더링
  - 각 응답 하단: citations 링크 (소스/개념 페이지로 이동)

## ChatPopup

우하단 고정 버튼 (로그인 시만). 슬라이드업 패널 (h-[480px]).
layout.tsx에 포함.
```

---

## Phase 13 — 검색

```
통합 검색 페이지를 구현해줘.

## /search

헤더 SearchBox → /search?q=keyword.
서버 컴포넌트에서 getKnowledgeItems() (knowledge_view raw SQL).
클라이언트 필터링: 탭(전체/Sources/Concepts/Wiki) + 텍스트 검색 (제목+요약+토픽).
```

---

## Phase 14 — GitHub Actions (RSS 자동 ingest)

```
RSS 소스를 자동 수집해서 ingest하는 워크플로를 구현해줘.
수동 승인 없음. 점수 기준 통과 시 자동 처리.
ingest 후 synthesizeConcepts()가 자동 실행되므로 워크플로는 소스 수집만 담당.

## .github/workflows/discover-sources.yml

트리거: cron 매일 09:00 KST (00:00 UTC) + workflow_dispatch

steps:
1. python3 scripts/discover_sources.py

secrets: OPENAI_API_KEY, INGEST_API_URL, INGEST_SECRET

## scripts/discover_sources.py

표준 라이브러리 + openai만 사용.

RSS 피드 (한국 리빙·인테리어·디자인 트렌드 관련 — 운영 전 각 URL 실제 피드 존재 여부 검증 필요):
- 오늘의집 블로그:        https://blog.ohou.se/feed
- 한국디자인진흥원 뉴스:  https://www.kidp.or.kr/rss.do
- 서울디자인재단 뉴스:    https://www.seouldesign.or.kr/rss/news
- 한경 라이프 섹션:       https://rss.hankyung.com/economy/life.xml
- 조선일보 라이프 섹션:   https://www.chosun.com/rss/life.xml

처리 흐름:
1. 피드 파싱 → 신규 항목
   중복 확인: GET {INGEST_API_URL}/api/sources/exists?url={url}
2. gpt-4.1-mini 스코어링:
   관련성(0-4) + 품질(0-3) + 독창성(0-2) + 최신성(0-1)
3. 점수 6 이상:
   a. Jina Reader: GET https://r.jina.ai/{url}
   b. POST {INGEST_API_URL}/api/ingest
      { title, raw_content, url, publisher, source_type:"external" }
      → runIngest() → synthesizeConcepts() 자동 실행
4. 점수 미달: 스킵

rate limit: 항목당 1초. 피드당 최신 10개.
```

---

## Phase 15 — 배포 + 최종 점검

```
Vercel 배포 설정과 최종 체크리스트를 확인해줘.

## Vercel 설정

package.json scripts:
  "build": "next build"
  "start": "next start"
  "typecheck": "tsc --noEmit"
  "db:push": "drizzle-kit push"
  "db:studio": "drizzle-kit studio"

drizzle.config.ts:
  export default defineConfig({
    schema: './lib/db/schema.ts',
    out: './migrations',
    dialect: 'postgresql',
    dbCredentials: { url: process.env.POSTGRES_URL_NON_POOLING! },
  })

## Vercel 환경 변수

# Postgres (DB 연결 시 자동 생성):
POSTGRES_URL, POSTGRES_URL_NON_POOLING

# 수동 추가:
AUTH_SECRET, AUTH_ADMIN_EMAIL, AUTH_ADMIN_PASSWORD
OPENAI_API_KEY, INGEST_SECRET

## 초기 운영 순서

1. Vercel 프로젝트 생성 → Vercel Postgres 연결
2. .env.local에 POSTGRES_URL_NON_POOLING 복사
3. psql $POSTGRES_URL_NON_POOLING -f migrations/001_initial.sql
4. python3 scripts/import_from_md.py --wiki-dir ./kb/wiki
5. git push → Vercel 자동 배포
6. /auth/signin 로그인 → /admin → Health 탭 → "전체 Embeddings 재빌드" (※ 필수)
7. Admin → Graph 탭 → "그래프 재생성"
8. Editorial 탭 → "AI 초안 생성" → 검토 후 publish
9. 이후 kb/wiki/는 archive 보관

## 최종 체크리스트

- [ ] npm run typecheck 통과
- [ ] npm run build 성공
- [ ] /api/ingest, /api/sources/upload: runtime="nodejs", maxDuration=120
- [ ] /api/chat, /api/admin/synthesize-editorial: maxDuration=60
- [ ] AUTH_SECRET, OPENAI_API_KEY: 클라이언트 노출 없음
- [ ] /admin, /chat: middleware.ts 보호 확인
- [ ] pgvector EXTENSION 생성 확인
- [ ] synthesizeConcepts(): GPT 호출 실패 시 ingest는 계속 진행 (try/catch)
- [ ] lintWiki(): 빈 결과 시 "이슈 없음" 표시
- [ ] rebuild-embeddings: 초기 배포 후 1회 실행 여부 확인
- [ ] editorial is_draft 구분 UI 확인
- [ ] app/not-found.tsx, app/error.tsx
- [ ] loading.tsx (sources, knowledge)
```

---

## 전체 구조 요약

### 데이터 흐름 (Karpathy LLM Wiki 패턴)

```
[3계층 구조]

Layer 1 — Raw Sources (읽기 전용)
  kb/wiki/*.md (초기 seed)
  RSS 피드
  수동 업로드 파일

Layer 2 — Wiki Pages (LLM이 작성·유지)
  concepts 테이블  ← synthesizeConcepts()가 자동 업데이트/생성
  pages 테이블     ← Admin에서 수동 편집
  editorial        ← synthesizeEditorial()이 초안 생성, 사람이 publish

Layer 3 — Schema (구조 정의)
  settings.topics_config
  settings.graph_data

[초기 1회 — Seed]
kb/wiki/*.md
    └─ import_from_md.py
           ├─ concepts, pages, sources → DB
           ├─ editorial → settings.editorial_content
           ├─ topic-map → settings.topics_config
           └─ Homestyle-metrics → settings.metrics_content

[지속 운영 — Living Wiki]
RSS 피드 (매일 자동)
수동 업로드
    └─ POST /api/ingest
           ├─ sources 생성 + ai_summary 생성
           ├─ embeddings 생성
           ├─ synthesizeConcepts()
           │      ├─ 기존 concepts 업데이트 (content 보강, source_count++)
           │      └─ 신규 concepts 생성
           └─ ingest_log 기록

Admin 트리거
    ├─ synthesizeEditorial() → editorial 초안 → 검토 후 publish
    ├─ lintWiki() → 고아·빈·오래된 개념 탐지
    └─ graph/rebuild → settings.graph_data 갱신
```

### 테이블 (6개 + VIEW)

| 이름 | 역할 |
|------|------|
| sources | 원문 + AI 요약 + synthesis_result |
| concepts | Homestyle 개념 (LLM이 지속 유지, source_count 추적) |
| pages | Wiki 챕터 (수동 관리) |
| knowledge_embeddings | pgvector RAG |
| settings | editorial·topics·metrics·graph·ingest_log |
| chat_sessions | 챗봇 히스토리 (citations 포함) |
| knowledge_view | 통합 검색 VIEW |

### 페이지 (13개)

| 경로 | 설명 |
|------|------|
| / | 홈 (living editorial + source_count 기준 top 개념) |
| /sources | 소스 목록 (synthesis_result 표시) |
| /sources/[id] | 소스 상세 + 기여한 개념 목록 |
| /sources/upload | 내부 업로드 |
| /concepts | 개념 그리드 (source_count, last_synthesized_at) |
| /concepts/[slug] | 개념 상세 |
| /wiki | 챕터 목록 |
| /wiki/[slug] | 위키 페이지 |
| /knowledge | 지식 그래프 |
| /metrics | Homestyle 지표 카드 |
| /chat | RAG 챗봇 (citations) |
| /search | 통합 검색 |
| /admin | 에디터 6탭 (Editorial·Concepts·Wiki·Metrics·Health·Graph) |
| /auth/signin | 로그인 |
