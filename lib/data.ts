import { unstable_noStore as noStore } from 'next/cache'
import { asc, desc, eq, sql } from 'drizzle-orm'
import { db } from './db'
import { sources, concepts, pages, settings } from './db/schema'
import type {
  SourceItem, ConceptItem, WikiPageItem, KnowledgeItem,
  TopicNode, MetricCard, KnowledgeGraphData,
  IngestLogEntry, EditorialVersion, SynthesisResult,
} from './types'

// ─── mappers ──────────────────────────────────────────────

function mapSource(r: typeof sources.$inferSelect): SourceItem {
  return {
    id: r.id,
    title: r.title,
    url: r.url ?? undefined,
    publisher: r.publisher ?? undefined,
    published_at: r.published_at ?? undefined,
    source_type: r.source_type ?? 'external',
    one_line_summary: r.one_line_summary ?? undefined,
    ai_summary: r.ai_summary ?? undefined,
    topics: (r.topics as string[]) ?? [],
    status: r.status ?? 'done',
    synthesis_result: (r.synthesis_result as SynthesisResult) ?? {
      concepts_updated: [], concepts_created: [], synthesized_at: '',
    },
    created_at: r.created_at?.toISOString() ?? '',
  }
}

function mapConcept(r: typeof concepts.$inferSelect): ConceptItem {
  return {
    id: r.id,
    title: r.title,
    slug: r.slug,
    brief: r.brief ?? undefined,
    aliases: (r.aliases as string[]) ?? [],
    topics: (r.topics as string[]) ?? [],
    related_concepts: (r.related_concepts as string[]) ?? [],
    concept_type: r.concept_type ?? undefined,
    concept_status: r.concept_status ?? 'candidate',
    confidence: r.confidence ?? 0,
    content: r.content ?? undefined,
    source_count: r.source_count ?? 0,
    last_synthesized_at: r.last_synthesized_at?.toISOString() ?? undefined,
    updated_at: r.updated_at?.toISOString() ?? '',
  }
}

function mapPage(r: typeof pages.$inferSelect): WikiPageItem {
  return {
    id: r.id,
    slug: r.slug,
    title: r.title,
    chapter_number: r.chapter_number ?? '',
    subsections: (r.subsections as { number: string; title: string }[]) ?? [],
    summary: r.summary ?? undefined,
    topics: (r.topics as string[]) ?? [],
    content: r.content ?? undefined,
    updated_at: r.updated_at?.toISOString() ?? '',
  }
}

// ─── sources ──────────────────────────────────────────────

export async function getSources(): Promise<SourceItem[]> {
  noStore()
  try {
    const rows = await db.select().from(sources).orderBy(desc(sources.created_at))
    return rows.map(mapSource)
  } catch { return [] }
}

export async function getSourceById(id: string): Promise<SourceItem | null> {
  noStore()
  try {
    const [row] = await db.select().from(sources).where(eq(sources.id, id))
    return row ? mapSource(row) : null
  } catch { return null }
}

// ─── concepts ─────────────────────────────────────────────

export async function getConceptItems(): Promise<ConceptItem[]> {
  noStore()
  try {
    const rows = await db.select().from(concepts).orderBy(asc(concepts.slug))
    return rows.map(mapConcept)
  } catch { return [] }
}

export async function getConceptBySlug(slug: string): Promise<ConceptItem | null> {
  noStore()
  try {
    const [row] = await db.select().from(concepts).where(eq(concepts.slug, slug))
    return row ? mapConcept(row) : null
  } catch { return null }
}

// ─── pages ────────────────────────────────────────────────

export async function getWikiPages(): Promise<WikiPageItem[]> {
  noStore()
  try {
    const rows = await db.select().from(pages).orderBy(asc(pages.chapter_number))
    return rows.map(mapPage)
  } catch { return [] }
}

export async function getPageBySlug(slug: string): Promise<WikiPageItem | null> {
  noStore()
  try {
    const [row] = await db.select().from(pages).where(eq(pages.slug, slug))
    return row ? mapPage(row) : null
  } catch { return null }
}

// ─── knowledge view (unified search) ──────────────────────

export async function getKnowledgeItems(): Promise<KnowledgeItem[]> {
  noStore()
  try {
    const result = await db.execute(sql`
      SELECT id, type, title, slug, summary, topics, updated_at
      FROM knowledge_view
      ORDER BY updated_at DESC
    `)
    return (result.rows as Array<{
      id: string; type: string; title: string; slug: string
      summary: string | null; topics: string[] | null; updated_at: Date
    }>).map(r => ({
      id: r.id,
      type: r.type as KnowledgeItem['type'],
      title: r.title,
      slug: r.slug,
      summary: r.summary ?? undefined,
      topics: r.topics ?? [],
      updated_at: r.updated_at?.toISOString?.() ?? String(r.updated_at),
    }))
  } catch { return [] }
}

// ─── settings helpers ─────────────────────────────────────

async function getSetting(key: string): Promise<string | null> {
  const [row] = await db.select().from(settings).where(eq(settings.key, key))
  return row?.value ?? null
}

async function getSettingJson<T>(key: string, fallback: T): Promise<T> {
  try {
    const value = await getSetting(key)
    return value ? (JSON.parse(value) as T) : fallback
  } catch { return fallback }
}

// ─── editorial ────────────────────────────────────────────

export async function getEditorialContent(): Promise<string> {
  noStore()
  try { return (await getSetting('editorial_content')) ?? '' }
  catch { return '' }
}

export async function getEditorialVersions(): Promise<EditorialVersion[]> {
  noStore()
  return getSettingJson<EditorialVersion[]>('editorial_versions', [])
}

// ─── topics / metrics / graph / ingest_log ────────────────

export async function getTopicsConfig(): Promise<TopicNode[]> {
  noStore()
  return getSettingJson<TopicNode[]>('topics_config', [])
}

export async function getMetricsContent(): Promise<MetricCard[]> {
  noStore()
  return getSettingJson<MetricCard[]>('metrics_content', [])
}

export async function getKnowledgeGraph(): Promise<KnowledgeGraphData> {
  noStore()
  return getSettingJson<KnowledgeGraphData>('graph_data', {
    nodes: [], links: [], built_at: '',
  })
}

export async function getIngestLog(): Promise<IngestLogEntry[]> {
  noStore()
  return getSettingJson<IngestLogEntry[]>('ingest_log', [])
}
