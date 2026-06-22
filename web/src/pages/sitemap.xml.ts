import type { APIRoute } from "astro";
import { getCompanies, getConcepts, getSources, getThemes, getTopics } from "../lib/content";

export const GET: APIRoute = async ({ site }) => {
  const [topics, themes, companies, concepts, sources] = await Promise.all([
    getTopics(), getThemes(), getCompanies(), getConcepts(), getSources()
  ]);
  const paths = [
    "/", "/insights/", "/themes/", "/companies/", "/concepts/", "/sources/",
    ...topics.map((item) => `/insights/${item.slug}/`),
    ...themes.map((item) => `/themes/${item.slug}/`),
    ...companies.map((item) => `/companies/${item.slug}/`),
    ...concepts.map((item) => `/concepts/${item.slug}/`),
    ...sources.map((item) => `/sources/${item.slug}/`)
  ];
  const base = site || new URL("https://lg-ai-strategy-journal.pages.dev");
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${
    paths.map((path) => `  <url><loc>${new URL(path, base).href}</loc></url>`).join("\n")
  }\n</urlset>`;
  return new Response(body, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
};
