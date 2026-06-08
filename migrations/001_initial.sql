CREATE EXTENSION IF NOT EXISTS vector;

-- sources: 원문 + AI 요약 통합
CREATE TABLE sources (
  id               text PRIMARY KEY,
  title            text NOT NULL,
  url              text,
  publisher        text,
  published_at     text,
  source_type      text DEFAULT 'external',
  raw_content      text,
  ai_summary       text,
  one_line_summary text,
  topics           text[] DEFAULT '{}',
  status           text DEFAULT 'done',
  error_message    text,
  synthesis_result jsonb DEFAULT '{}',
  created_at       timestamptz DEFAULT now(),
  updated_at       timestamptz DEFAULT now()
);

-- concepts: Homestyle 핵심 개념 (LLM이 지속 유지)
CREATE TABLE concepts (
  id                  text PRIMARY KEY,
  title               text NOT NULL,
  slug                text UNIQUE NOT NULL,
  brief               text,
  aliases             text[] DEFAULT '{}',
  topics              text[] DEFAULT '{}',
  related_concepts    text[] DEFAULT '{}',
  concept_type        text,
  concept_status      text DEFAULT 'candidate',
  confidence          int DEFAULT 0,
  content             text,
  source_count        int DEFAULT 0,
  last_synthesized_at timestamptz,
  updated_at          timestamptz DEFAULT now()
);

-- pages: Wiki 챕터 페이지
CREATE TABLE pages (
  id             text PRIMARY KEY,
  slug           text UNIQUE NOT NULL,
  title          text NOT NULL,
  chapter_number text,
  subsections    jsonb DEFAULT '[]',
  summary        text,
  topics         text[] DEFAULT '{}',
  content        text,
  updated_at     timestamptz DEFAULT now()
);

-- knowledge_embeddings: pgvector RAG
CREATE TABLE knowledge_embeddings (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ref_type   text NOT NULL,
  ref_id     text NOT NULL,
  content    text NOT NULL,
  embedding  vector(1536),
  metadata   jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

CREATE INDEX ON knowledge_embeddings
  USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- settings: 앱 전역 설정
-- keys: editorial_content, editorial_versions, topics_config,
--       metrics_content, graph_data, ingest_log
CREATE TABLE settings (
  key        text PRIMARY KEY,
  value      text,
  updated_at timestamptz DEFAULT now()
);

-- chat_sessions: RAG 챗봇 히스토리
CREATE TABLE chat_sessions (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_email text NOT NULL,
  title      text,
  messages   jsonb DEFAULT '[]',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- knowledge_view: 통합 검색 VIEW
CREATE VIEW knowledge_view AS
  SELECT id, 'source' AS type, title, id AS slug,
         one_line_summary AS summary, topics, updated_at
  FROM sources WHERE status = 'done'
  UNION ALL
  SELECT id, 'concept', title, slug, brief AS summary, topics, updated_at
  FROM concepts
  UNION ALL
  SELECT id, 'page', title, slug, summary, topics, updated_at
  FROM pages;

-- match_knowledge_chunks: cosine similarity 검색 함수
CREATE OR REPLACE FUNCTION match_knowledge_chunks(
  query_embedding  vector(1536),
  match_threshold  float DEFAULT 0.32,
  match_count      int   DEFAULT 8
) RETURNS TABLE (
  id         uuid,
  ref_type   text,
  ref_id     text,
  content    text,
  similarity float,
  metadata   jsonb
) LANGUAGE sql STABLE AS $$
  SELECT id, ref_type, ref_id, content,
    1 - (embedding <=> query_embedding) AS similarity,
    metadata
  FROM knowledge_embeddings
  WHERE 1 - (embedding <=> query_embedding) > match_threshold
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;
