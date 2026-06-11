# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Homestyle Wiki — a Korean-language knowledge wiki for Korean home/interior design trends, built on Next.js 15 (App Router) + TypeScript + Tailwind CSS v4, with Neon Postgres (pgvector) via Drizzle ORM, Auth.js v5, and OpenAI for summarization/synthesis/embeddings/RAG chat.

The product follows the "Karpathy LLM Wiki" pattern (see `new-build-prompt.md` for the original phased build spec, written in Korean — useful background but some details, e.g. `@vercel/postgres`, are superseded by the actual implementation which uses `@neondatabase/serverless`):

- **Layer 1 — Raw sources (read-only)**: `kb/wiki/*.md` (initial seed, now archival), RSS feeds, manual uploads.
- **Layer 2 — Wiki pages (LLM-maintained)**: `concepts` table is continuously updated/created by an automated synthesis step; `pages` table (chapter wiki) is manually edited via `/admin`; the home `editorial` is drafted by AI and published by a human.
- **Layer 3 — Schema**: `settings.topics_config` and `settings.graph_data` define structure derived from the above.

Core principle: information is processed once and accumulated, not re-derived on every query (contrast with plain RAG).

## Commands

```bash
npm run dev          # next dev --turbopack
npm run build        # next build
npm run start        # next start
npm run lint         # eslint
npm run typecheck    # tsc --noEmit
npm run db:push      # drizzle-kit push (sync lib/db/schema.ts -> DB)
npm run db:studio    # drizzle-kit studio
```

There is no test suite/runner configured in this repo.

Database migrations:
- `migrations/001_initial.sql` — initial schema (tables, `knowledge_view`, `match_knowledge_chunks()` pgvector function). Apply with `node --env-file=.env scripts/run-migration.mjs` (Neon-specific statement splitter that handles `$$`-quoted function bodies).
- `migrations/002_add_image_columns.sql` — adds `image_url`/`image_source_url` to `concepts`/`pages`. New schema columns are best applied via `npm run db:push` (drizzle-kit) once `lib/db/schema.ts` reflects them.

One-time/operational Python scripts (run from repo root):
- `scripts/import_from_md.py --postgres-url "$DATABASE_URL_UNPOOLED" --wiki-dir ./kb/wiki [--dry-run]` — one-time bulk import of `kb/wiki/` into Postgres (concepts, pages, editorial, topics, metrics, sources). Requires `pip install psycopg2-binary python-frontmatter`. Does **not** create embeddings — run "전체 Embeddings 재빌드" (`POST /api/admin/rebuild-embeddings`) afterward.
- `scripts/discover_sources.py` — RSS discovery + GPT scoring + auto-ingest, run daily by `.github/workflows/discover-sources.yml`. Stdlib + `openai` only.
- `scripts/search_pexels_images.py`, `scripts/generate_image_review.py` — one-off scripts used to source/curate hero images for concepts/pages.

## Architecture

### Database (Drizzle, `lib/db/schema.ts`)

7 tables/views, all defined in one schema file:

| Table | Role |
|---|---|
| `sources` | Raw ingested content + AI summary (`ai_summary`, `one_line_summary`, `topics`) + `synthesis_result` jsonb (`{concepts_updated, concepts_created, synthesized_at}`). `status`: `processing` / `done` / `error`. |
| `concepts` | Homestyle concept pages, continuously maintained by `synthesizeConcepts()`. Key fields: `slug`, `aliases`, `topics`, `related_concepts` (slugs), `concept_type` (style/lifestyle/spatial/functional/material/market), `concept_status` (canonical/candidate/supporting), `confidence`, `content` (markdown, append-only updates), `source_count`, `last_synthesized_at`, `image_url`/`image_source_url`. |
| `pages` | Manually-edited chapter wiki pages. `chapter_number` ("01"–"06"), `subsections` jsonb `[{number, title}]`, `content` markdown. |
| `knowledge_embeddings` | pgvector RAG store. `ref_type` (`source`/`concept`/`page`), `ref_id`, `embedding vector(1536)`, HNSW index. Queried via the `match_knowledge_chunks(query_embedding, threshold, count)` SQL function. |
| `settings` | Generic key/value store (used as a JSON config table). Keys: `editorial_content`, `editorial_versions`, `topics_config`, `metrics_content`, `graph_data`, `ingest_log`. Access via `lib/settings.ts` (`getSetting`, `getSettingJson`, `upsertSetting`). |
| `chat_sessions` | RAG chatbot history per user (`messages` jsonb with citations). |
| `knowledge_view` (SQL view) | UNION of sources/concepts/pages for unified search (`/search`). |

IDs follow a `{type}_{slug}` convention (`source_*`, `concept_*`, `page_*`); `lib/slug.ts#slugify` lowercases and keeps alphanumerics, Korean (Hangul), and hyphens, max 80 chars.

`lib/db/index.ts` exports `db` — Drizzle over `@neondatabase/serverless` `Pool` using `DATABASE_URL`.

### Data layer (`lib/data.ts`)

All `get*` functions call `unstable_noStore()` and **swallow errors, returning `[]`/`null`/empty defaults** rather than throwing — server components rendering this data should not assume DB availability. This is the standard pattern to follow for any new read function.

### Ingest & synthesis pipeline (the LLM Wiki core)

`lib/ingest.ts#runIngest({title, raw_content, url?, publisher?, source_type?})`:
1. Insert `sources` row, `id = "source_" + slugify(title)`, `status='processing'`.
2. `gpt-4.1-mini` produces a fixed 6-section Korean markdown summary (`## 한 줄 요약`, `## 핵심 메시지`, `## 주요 수치와 데이터`, `## Homestyle 시사점`, `## 액션 아이템`, `## 관련 개념`). `one_line_summary` and `topics` are extracted from this via regex against the `## 한 줄 요약` and `## 관련 개념` sections.
3. Update `sources` with summary/topics, `status='done'`.
4. Rebuild embeddings for the source (raw content chunks + full summary) — non-fatal on error.
5. Call `synthesizeConcepts()` — non-fatal on error.
6. Persist `synthesis_result`, prepend an entry to `ingest_log` (max 50, in `settings`).
7. On any thrown error before completion: `status='error'`, `error_message` set.

`lib/synthesize.ts`:
- `synthesizeConcepts({sourceId, aiSummary, topics})` — loads all concepts, filters candidates by topic overlap (falls back to all concepts if <3 match), asks `gpt-4.1` (JSON mode) to return `{updates: [{slug, additions}], new_concepts: [{title, slug, brief, content}]}`. Updates **append** `additions` to existing `content`, bump `source_count`, set `last_synthesized_at`, and rebuild that concept's embeddings. New concepts are inserted (`onConflictDoNothing`) and embedded.
- `synthesizeEditorial()` — `gpt-4.1` rewrites the home editorial using the current editorial + 10 most-recently-synthesized concepts + 5 latest sources. Result is pushed onto `editorial_versions` (max 20) as `{label: "AI 초안 (date)", is_draft: true}` — **does not** overwrite `editorial_content`; a human must publish via `/admin`.
- `lintWiki()` — health check over `concepts`, returns `LintIssue[]` with types `empty_content` (content < 100 chars), `no_topics`, `no_sources` (`source_count === 0`), `stale` (`last_synthesized_at` set and >90 days old), `orphan` (`related_concepts` referencing a nonexistent slug).

`lib/embed.ts`:
- `chunkText(text, maxLen=1200, overlap=150)`.
- `rebuildEmbeddings(refType, refId, chunks)` — deletes existing rows for `(ref_type, ref_id)`, embeds with `text-embedding-3-small` in batches of 20, inserts in batches of 50. Called whenever `concepts`/`pages`/`sources` content changes.

`lib/graph.ts#rebuildGraph()` — rebuilds `settings.graph_data` (`{nodes, links, built_at}`) from `concepts`, latest 50 `done` `sources`, and `topics_config`:
- topic→concept links via `CONCEPT_TYPE_TO_CHAPTERS` (`style→03`, `lifestyle→02`, `spatial→04`, `functional→05`, `market→06`, `material→03+04`); concepts without a `concept_type` get no topic link.
- topic→source links via case-insensitive overlap of `source.topics` and `topic.label`.
- concept→concept links via `related_concepts` slugs.
- concept→source links via topic-array intersection.

### API routes (`app/api/**/route.ts`)

- `POST /api/ingest` — Bearer-token auth via `INGEST_SECRET` (not session-based). `runtime='nodejs'`, `maxDuration=120`. Used by GitHub Actions discovery.
- `POST /api/sources/upload` — session-authed (`auth()`), `runIngest({source_type:'internal'})`, same runtime/duration.
- `GET /api/sources/exists?url=` — dedup check used by `discover_sources.py`.
- `DELETE /api/source?id=` — session-authed, deletes embeddings + source.
- `POST /api/admin/synthesize-editorial`, `POST /api/admin/lint`, `POST /api/admin/rebuild-embeddings` (`maxDuration=300`, re-embeds all concepts+pages), `POST /api/graph/rebuild` — all session-authed admin actions.
- `PUT /api/admin/editorial` / `concept` / `page` / `metrics` — admin edits; concept/page saves call `rebuildEmbeddings` after writing.
- `POST /api/chat` — session-authed RAG chat: embed query → `match_knowledge_chunks` (threshold 0.32, top 8) → build citations from concept/page/source ids → streamed `gpt-4.1` response → persists `chat_sessions`. `maxDuration=60`.

Routes that call OpenAI for non-trivial work set `export const runtime = 'nodejs'` and an explicit `maxDuration` — follow this convention for any new long-running route.

Auth pattern: every mutating/admin API route starts with `const session = await auth(); if (!session) return Response.json({error:'Unauthorized'}, {status:401})`, except `/api/ingest` (and `/api/sources/exists`) which use the `INGEST_SECRET` bearer token instead.

### Auth & routing

- `auth.ts` — Auth.js v5, single Credentials provider checking `AUTH_ADMIN_EMAIL`/`AUTH_ADMIN_PASSWORD` env vars (no DB adapter, JWT session).
- `middleware.ts` — protects `/admin/**` and `/chat` (and subpaths), redirecting to `/auth/signin?callbackUrl=...`.
- `components/EmbeddedChrome.tsx` — detects `?popup=1` and sets `body[data-embedded="true"]`, which `globals.css` uses to hide the header and adjust `<main>` padding for iframe/popup embedding (used by `ChatPopup`).

### App Router pages (`app/`)

- `/` — home: editorial (rendered markdown) + top concepts by `source_count` + latest sources.
- `/sources`, `/sources/[id]`, `/sources/upload` — source list/detail/upload (URL via Jina Reader, raw text, or file).
- `/concepts`, `/concepts/[slug]` — concept grid (filterable by `topics_config`) and detail.
- `/wiki`, `/wiki/[slug]` — chapter pages, ordered by `chapter_number`, with `WikiChapterDrawer`/`WikiIndexDrawer` navigation.
- `/knowledge` — knowledge graph, rendered client-side via `react-force-graph-2d` (dynamic import, `ssr:false`); colors: topic `#d4d4d8`, concept `#22d3ee`, source `#ec4899` on `#080a12` background.
- `/metrics` — `MetricCard[]` dashboard from `settings.metrics_content`.
- `/chat` — RAG chatbot UI (session list + streaming responses + citation links); `ChatPopup` is the floating widget version embedded in the layout.
- `/search` — unified search over `knowledge_view`, client-side filter by type/keyword.
- `/admin` — 6 tabs (`AdminTabs.tsx`): Editorial, Concepts, Pages (Wiki), Metrics, Health (lint + ingest log + rebuild-embeddings trigger), Graph (rebuild trigger). All gated by `auth()` server-side redirect.
- `/auth/signin`, `/auth/signout`.

### Rendering markdown

`lib/markdown.ts#renderMarkdown` — `remark` → `remark-gfm` → `remark-html` (`sanitize: false`); output is rendered via `components/MarkdownRenderer.tsx` (`"use client"`, applies `prose` classes).

## Environment variables (`.env.example`)

```
DATABASE_URL, DATABASE_URL_UNPOOLED   # Neon Postgres
AUTH_SECRET, AUTH_ADMIN_EMAIL, AUTH_ADMIN_PASSWORD
OPENAI_API_KEY
INGEST_SECRET
```
