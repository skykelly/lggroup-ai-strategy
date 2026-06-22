import { readFile, readdir } from "node:fs/promises";
import { basename, resolve } from "node:path";
import { marked } from "marked";
import { parse as parseYaml } from "yaml";

export const THEME_META = {
  ai_data_center_infra: {
    number: "01",
    title: "AI Data Center / Infra",
    short: "AI Infra",
    color: "#A50034",
    description: "GPU를 넘어 전력·냉각·운영 효율까지 연결하는 One LG 인프라 스택"
  },
  physical_ai_smart_manufacturing: {
    number: "02",
    title: "Physical AI / Smart Manufacturing",
    short: "Physical AI",
    color: "#DB3A62",
    description: "제조 데이터, 로봇, 디지털트윈을 AI Factory 운영 모델로 연결"
  },
  ai_mobility_sdv_aidv: {
    number: "03",
    title: "AI Mobility / SDV·AIDV",
    short: "AI Mobility",
    color: "#356DFF",
    description: "완성차 없이도 디스플레이·센싱·배터리 SW·연결성 레이어를 확보"
  },
  enterprise_ax_agentic_operating_model: {
    number: "04",
    title: "Enterprise AX / Agentic Operating Model",
    short: "Enterprise AX",
    color: "#596579",
    description: "전사 온톨로지와 Agent workflow를 기반으로 운영체계를 재설계"
  },
  ai_for_science_bio_materials_battery: {
    number: "05",
    title: "AI for Science / Bio / Materials / Battery",
    short: "AI for Science",
    color: "#008E9B",
    description: "AI 후보 제안과 실험·검증을 잇는 closed-loop R&D"
  },
  global_ai_alliance_open_innovation: {
    number: "06",
    title: "Global AI Alliance / Open Innovation",
    short: "AI Alliance",
    color: "#6750A4",
    description: "외부 기술을 빠르게 활용하면서 데이터와 운영 지식을 내부화"
  }
} as const;

export type ThemeId = keyof typeof THEME_META;

export interface Topic {
  slug: string;
  path: string;
  number: number;
  id: string;
  title: string;
  subtitle: string;
  question: string;
  short_answer: string;
  status: string;
  updated: string;
  priority: string;
  priorityScore: number;
  priorityUpdated: string;
  priorityFactors: {
    recency?: number;
    issue_salience?: number;
    strategic_impact?: number;
    urgency?: number;
    actionability?: number;
  };
  topic_type: string[];
  related_themes: ThemeId[];
  related_concepts: string[];
  related_companies: string[];
  source_ids: string[];
  tags: string[];
  body: string;
  html: string;
  heroImage?: string;
  readingTime: number;
}

export interface KnowledgeEntity {
  slug: string;
  path: string;
  id: string;
  title: string;
  type: "concept" | "company" | "theme";
  category?: string;
  aliases: string[];
  primary_theme?: ThemeId;
  related_themes: ThemeId[];
  related_topics: string[];
  related_concepts: string[];
  related_companies: string[];
  source_ids: string[];
  tags: string[];
  body: string;
  html: string;
  heroImage?: string;
  summary: string;
}

export interface SourceEntity {
  slug: string;
  path: string;
  id: string;
  title: string;
  publisher: string;
  published: string;
  url: string;
  related_themes: ThemeId[];
  related_topics: string[];
  related_concepts: string[];
  related_companies: string[];
  tags: string[];
  body: string;
  html: string;
  summary: string;
  heroImage?: string;
}

function parseFrontmatter(raw: string) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return { data: {} as Record<string, any>, content: raw };
  return {
    data: parseYaml(match[1]) as Record<string, any>,
    content: raw.slice(match[0].length)
  };
}

function normalizeImagePath(value: string) {
  if (value.startsWith("assets/images/")) return `/${value}`;
  return value;
}

function wikilinksToWeb(markdown: string) {
  return markdown.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_match, target, label) => {
    const clean = String(target).replace(/\.md$/, "");
    const text = label || clean.split("/").at(-1)?.replace(/[-_]/g, " ") || clean;
    if (clean.startsWith("topics/")) return `[${text}](/insights/${clean.split("/").at(-1)})`;
    if (clean.startsWith("concepts/")) return `[${text}](/concepts/${clean.split("/").at(-1)})`;
    if (clean.startsWith("companies/partners/")) return `[${text}](/companies/${clean.split("/").at(-1)})`;
    if (clean.startsWith("companies/")) return `[${text}](/companies/${clean.split("/").at(-1)})`;
    if (clean.startsWith("sources/")) return `[${text}](/sources/${clean.split("/").at(-1)})`;
    if (/^docs\/0[1-6]_/.test(clean)) {
      const themeId = Object.keys(THEME_META)[Number(clean.split("/").at(-1)?.slice(0, 2)) - 1];
      return themeId ? `[${text}](/themes/${themeId})` : `**${text}**`;
    }
    return `**${text}**`;
  });
}

function cleanArticle(markdown: string) {
  const withoutAppendices = markdown.split(/\n---\s*\n\s*## Appendix [A-Z]\./)[0];
  const withoutDuplicateTitle = withoutAppendices.replace(/^# .+\r?\n+/, "");
  return wikilinksToWeb(withoutDuplicateTitle)
    .replace(/src=(["'])assets\/images\//g, "src=$1/assets/images/")
    .replace(/style=(["'])[^"']*\1/g, "");
}

function extractSummary(markdown: string) {
  const candidates = [
    /## 1\. (?:Role Summary|Definition|Executive Summary)\s+([\s\S]*?)(?=\n##|\n<figure|\n\|)/,
    /> \*\*Summary\*\*\s+([\s\S]*?)(?=\n\n|<figure)/,
    /## [^\n]+\s+([\s\S]*?)(?=\n##|\n<figure|\n\|)/
  ];
  for (const pattern of candidates) {
    const value = markdown.match(pattern)?.[1]
      ?.replace(/<[^>]+>/g, " ")
      .replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, "$2")
      .replace(/[*_`#]/g, "")
      .replace(/\s+/g, " ")
      .trim();
    if (value) return value.slice(0, 280);
  }
  return "";
}

function getFirstImage(markdown: string) {
  const htmlImage = markdown.match(/<img[^>]+src=["']([^"']+)["']/i)?.[1];
  const mdImage = markdown.match(/!\[[^\]]*\]\(([^)\s]+)[^)]*\)/)?.[1];
  const image = htmlImage || mdImage;
  return image ? normalizeImagePath(image) : undefined;
}

function formatDate(value: unknown) {
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  return String(value || "");
}

export async function getTopics(): Promise<Topic[]> {
  const directory = resolve("topics");
  const files: string[] = (await readdir(directory))
    .filter((file) => /^\d{2}_.*\.md$/.test(file) && !file.startsWith("00_"))
    .sort();

  const topics = await Promise.all(
    files.map(async (file) => {
      const path = resolve(directory, file);
      const raw = await readFile(path, "utf8");
      const { data, content } = parseFrontmatter(raw);
      const body = cleanArticle(content);
      const words = body.replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;

      return {
        slug: basename(file, ".md"),
        path: `topics/${file}`,
        number: Number(file.slice(0, 2)),
        id: data.id,
        title: data.title,
        subtitle: data.subtitle,
        question: data.question,
        short_answer: data.short_answer,
        status: data.status,
        updated: formatDate(data.updated),
        priority: data.priority || "unscored",
        priorityScore: Number(data.priority_score || 0),
        priorityUpdated: formatDate(data.priority_updated),
        priorityFactors: data.priority_factors || {},
        topic_type: data.topic_type || [],
        related_themes: data.related_themes || [],
        related_concepts: data.related_concepts || [],
        related_companies: data.related_companies || [],
        source_ids: data.source_ids || [],
        tags: data.tags || [],
        body,
        html: await marked.parse(body),
        heroImage: getFirstImage(content),
        readingTime: Math.max(4, Math.round(words / 360))
      } satisfies Topic;
    })
  );

  return topics.sort((a, b) => b.priorityScore - a.priorityScore || a.number - b.number);
}

async function getEntitiesFromDirectory(
  directoryName: "concepts" | "companies",
  type: "concept" | "company"
): Promise<KnowledgeEntity[]> {
  const root = resolve(directoryName);
  const entries = directoryName === "companies"
    ? [
        ...(await readdir(root)).filter((file) => file.endsWith(".md")).map((file) => ({ file, path: resolve(root, file) })),
        ...(await readdir(resolve(root, "partners"))).filter((file) => file.endsWith(".md")).map((file) => ({
          file,
          path: resolve(root, "partners", file)
        }))
      ]
    : (await readdir(root)).filter((file) => file.endsWith(".md")).map((file) => ({ file, path: resolve(root, file) }));

  return Promise.all(entries.sort((a, b) => a.file.localeCompare(b.file)).map(async ({ file, path }) => {
    const raw = await readFile(path, "utf8");
    const { data, content } = parseFrontmatter(raw);
    const body = cleanArticle(content);
    return {
      slug: basename(file, ".md"),
      path: `${directoryName}/${file}`,
      id: data.id,
      title: data.title,
      type,
      category: data.category,
      aliases: data.aliases || [],
      primary_theme: data.primary_theme,
      related_themes: data.related_themes || (data.primary_theme ? [data.primary_theme] : []),
      related_topics: data.related_topics || [],
      related_concepts: data.related_concepts || [],
      related_companies: data.related_companies || [],
      source_ids: data.source_ids || [],
      tags: data.tags || [],
      body,
      html: await marked.parse(body),
      heroImage: getFirstImage(content),
      summary: extractSummary(content)
    };
  }));
}

export async function getConcepts() {
  return getEntitiesFromDirectory("concepts", "concept");
}

export async function getCompanies() {
  return getEntitiesFromDirectory("companies", "company");
}

export async function getThemes(): Promise<KnowledgeEntity[]> {
  const files = (await readdir(resolve("docs"))).filter((file) => /^0[1-6]_.*\.md$/.test(file)).sort();
  return Promise.all(files.map(async (file) => {
    const raw = await readFile(resolve("docs", file), "utf8");
    const { data, content } = parseFrontmatter(raw);
    const body = cleanArticle(content);
    const themeId = data.theme_id as ThemeId;
    return {
      slug: themeId,
      path: `docs/${file}`,
      id: data.id,
      title: data.title,
      type: "theme" as const,
      aliases: [],
      related_themes: [themeId],
      related_topics: [],
      related_concepts: data.related_concepts || [],
      related_companies: data.related_companies || [],
      source_ids: data.source_ids || [],
      tags: data.tags || [],
      body,
      html: await marked.parse(body),
      heroImage: getFirstImage(content),
      summary: extractSummary(content)
    };
  }));
}

export async function getSources(): Promise<SourceEntity[]> {
  const files = (await readdir(resolve("sources"))).filter((file) => file.endsWith(".md")).sort();
  return Promise.all(files.map(async (file) => {
    const raw = await readFile(resolve("sources", file), "utf8");
    const { data, content } = parseFrontmatter(raw);
    const body = cleanArticle(content);
    return {
      slug: basename(file, ".md"),
      path: `sources/${file}`,
      id: data.id,
      title: data.title,
      publisher: data.publisher || "Unknown publisher",
      published: formatDate(data.published || "unknown"),
      url: data.url || "",
      related_themes: data.related_themes || [],
      related_topics: data.related_topics || [],
      related_concepts: data.related_concepts || [],
      related_companies: data.related_companies || [],
      tags: data.tags || [],
      body,
      html: await marked.parse(body),
      summary: extractSummary(content),
      heroImage: getFirstImage(content)
    };
  }));
}

export function themeLabel(id: string) {
  return THEME_META[id as ThemeId]?.short || id.replace(/_/g, " ");
}
