import type { APIRoute } from "astro";
import { getCompanies, getConcepts, getSources, getThemes, getTopics } from "../../lib/content";

export const GET: APIRoute = async () => {
  const [topics, themes, companies, concepts, sources] = await Promise.all([
    getTopics(), getThemes(), getCompanies(), getConcepts(), getSources()
  ]);
  return new Response(
    JSON.stringify(
      [
        ...topics.map((topic) => ({
          type: "insight",
          label: `Q${String(topic.number).padStart(2, "0")}`,
          title: topic.title,
          description: topic.question,
          href: `/insights/${topic.slug}`,
          search: `${topic.title} ${topic.question} ${topic.tags.join(" ")}`
        })),
        ...themes.map((theme) => ({
          type: "theme", label: "Theme", title: theme.title, description: theme.summary,
          href: `/themes/${theme.slug}`, search: `${theme.title} ${theme.tags.join(" ")}`
        })),
        ...companies.map((company) => ({
          type: "company", label: company.category === "partner" ? "Partner" : "Company",
          title: company.title, description: company.summary, href: `/companies/${company.slug}`,
          search: `${company.title} ${company.tags.join(" ")}`
        })),
        ...concepts.map((concept) => ({
          type: "concept", label: "Concept", title: concept.title, description: concept.summary,
          href: `/concepts/${concept.slug}`, search: `${concept.title} ${concept.aliases.join(" ")} ${concept.tags.join(" ")}`
        })),
        ...sources.map((source) => ({
          type: "source", label: "Source", title: source.title,
          description: `${source.publisher} · ${source.published}`, href: `/sources/${source.slug}`,
          search: `${source.title} ${source.publisher} ${source.tags.join(" ")}`
        }))
      ]
    ),
    { headers: { "Content-Type": "application/json; charset=utf-8" } }
  );
};
