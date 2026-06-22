import type { APIRoute } from "astro";
import { getTopics } from "../lib/content";

function escapeXml(value: string) {
  return value.replace(/[<>&'"]/g, (char) => ({
    "<": "&lt;", ">": "&gt;", "&": "&amp;", "'": "&apos;", '"': "&quot;"
  })[char] || char);
}

export const GET: APIRoute = async ({ site }) => {
  const topics = await getTopics();
  const base = site || new URL("https://lg-ai-strategy-journal.pages.dev");
  const items = topics
    .slice()
    .sort((a, b) => b.updated.localeCompare(a.updated) || b.number - a.number)
    .map((topic) => {
      const link = new URL(`/insights/${topic.slug}/`, base).href;
      return `<item>
  <title>${escapeXml(topic.title)}</title>
  <link>${link}</link>
  <guid>${link}</guid>
  <pubDate>${new Date(`${topic.updated}T00:00:00+09:00`).toUTCString()}</pubDate>
  <description>${escapeXml(topic.short_answer)}</description>
</item>`;
    }).join("\n");
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>LG AI Strategy Journal</title>
  <link>${new URL("/", base).href}</link>
  <description>LG그룹의 AI 사업기회와 전략 질문을 공개 출처 기반으로 탐색합니다.</description>
  <language>ko-KR</language>
  ${items}
</channel>
</rss>`;
  return new Response(body, { headers: { "Content-Type": "application/rss+xml; charset=utf-8" } });
};
