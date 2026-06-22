#!/usr/bin/env python3
"""Generate the remaining Step 8 topic indexes and structured data."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
THEME_TITLES = {
    "ai_data_center_infra": "AI Data Center / Infra",
    "physical_ai_smart_manufacturing": "Physical AI / Smart Manufacturing",
    "ai_mobility_sdv_aidv": "AI Mobility / SDV·AIDV",
    "enterprise_ax_agentic_operating_model": "Enterprise AX / Agentic Operating Model",
    "ai_for_science_bio_materials_battery": "AI for Science / Bio / Materials / Battery",
    "global_ai_alliance_open_innovation": "Global AI Alliance / Open Innovation",
}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    raw = text.split("---", 2)[1]
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        repaired = []
        for line in raw.splitlines():
            match = re.match(r"^(title):\s*(.+)$", line)
            if match and ":" in match.group(2) and not match.group(2).startswith(("'", '"')):
                line = f"{match.group(1)}: {json.dumps(match.group(2), ensure_ascii=False)}"
            repaired.append(line)
        return yaml.safe_load("\n".join(repaired)) or {}


def main() -> int:
    topics = []
    for path in sorted((ROOT / "topics").glob("[0-9][0-9]_*.md")):
        if not 1 <= int(path.name[:2]) <= 18:
            continue
        metadata = parse_frontmatter(path)
        number = int(path.name[:2])
        concepts = list(dict.fromkeys(metadata.get("related_concepts") or []))
        companies = list(dict.fromkeys(metadata.get("related_companies") or []))
        sources = list(dict.fromkeys(metadata.get("source_ids") or []))
        topics.append(
            {
                "number": number,
                "id": metadata["id"],
                "title": metadata["title"],
                "subtitle": metadata.get("subtitle"),
                "question": metadata["question"],
                "short_answer": metadata["short_answer"],
                "status": metadata.get("status", "unknown"),
                "updated": str(metadata.get("updated", "unknown")),
                "priority": metadata.get("priority", "unscored"),
                "priority_score": float(metadata.get("priority_score", 0)),
                "priority_updated": str(metadata.get("priority_updated", "unknown")),
                "priority_model": metadata.get("priority_model"),
                "priority_factors": metadata.get("priority_factors") or {},
                "priority_rationale": metadata.get("priority_rationale"),
                "topic_type": metadata.get("topic_type") or [],
                "related_themes": metadata.get("related_themes") or [],
                "related_concepts": concepts,
                "related_companies": companies,
                "source_ids": sources,
                "image_policy": metadata.get("image_policy") or {},
                "path": f"topics/{path.name}",
            }
        )

    (ROOT / "data" / "topics.json").write_text(
        json.dumps({"topics": topics}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    companies = json.loads((ROOT / "data" / "companies.json").read_text(encoding="utf-8"))["companies"]
    theme_matrix = {}
    for theme_id, theme_title in THEME_TITLES.items():
        participants = []
        for company in companies:
            if theme_id in company["related_themes"]:
                participants.append(
                    {
                        "id": company["id"],
                        "title": company["title"],
                        "category": company["category"],
                        "path": company["path"],
                    }
                )
        theme_matrix[theme_id] = {
            "title": theme_title,
            "companies": participants,
        }
    (ROOT / "data" / "theme_company_matrix.json").write_text(
        json.dumps({"themes": theme_matrix}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    index_header = [
        "---",
        "id: topic_index",
        "type: index",
        "title: Topic Index",
        "---",
        "",
        "# Topic Index",
        "",
        "LG그룹의 AI 사업기회를 검토하는 18개 전략 질문이다. 각 Topic은 Docs의 테마 가정과 사업성을 질문 중심으로 검증한다.",
        "",
        "| Rank | Priority | Score | No. | Topic | Question | Related Themes |",
        "|---:|---|---:|---:|---|---|---|",
    ]
    rows = []
    priority_topics = sorted(topics, key=lambda item: (-item["priority_score"], item["number"]))
    for rank, topic in enumerate(priority_topics, start=1):
        themes = ", ".join(f"`{theme}`" for theme in topic["related_themes"])
        rows.append(
            f"| {rank} | {topic['priority']} | {topic['priority_score']:.2f} | {topic['number']:02d} "
            f"| [[topics/{Path(topic['path']).stem}|{topic['title']}]] | {topic['question']} | {themes} |"
        )
    topic_index = "\n".join(index_header + rows) + "\n"
    (ROOT / "topics" / "00_topic_index.md").write_text(topic_index, encoding="utf-8")

    docs_index = topic_index.replace(
        "id: topic_index",
        "id: docs_topic_index",
        1,
    ).replace(
        "# Topic Index",
        "# Strategic Topic Index",
        1,
    )
    (ROOT / "docs" / "85_topic_index.md").write_text(docs_index, encoding="utf-8")

    by_theme = defaultdict(list)
    for topic in topics:
        for theme in topic["related_themes"]:
            by_theme[theme].append(topic)
    research = [
        "---",
        "id: research_questions",
        "type: research_questions",
        "title: Research Questions",
        "baseline_date: 2026-06-21",
        "---",
        "",
        "# Research Questions",
        "",
        "18개 Topic의 핵심 질문을 6대 Theme별로 재배열한다. 하나의 질문이 여러 Theme에 걸칠 수 있다.",
        "",
    ]
    for theme_id, theme_title in THEME_TITLES.items():
        research.extend([f"## {theme_title}", ""])
        for topic in sorted(by_theme.get(theme_id, []), key=lambda item: (-item["priority_score"], item["number"])):
            research.append(
                f"- `{topic['priority']}` `{topic['priority_score']:.2f}` "
                f"[[topics/{Path(topic['path']).stem}|{topic['question']}]]"
            )
        research.append("")
    research.extend(
        [
            "## Cross-Theme Validation Agenda",
            "",
            "- One LG 제안이 계열사 나열이 아니라 고객이 구매할 수 있는 product package로 정의되어 있는가?",
            "- 외부 파트너 기술을 사용할 때 데이터·workflow·운영 노하우가 LG 내부 자산으로 축적되는가?",
            "- AI 사업의 성과가 모델 성능이나 사용량이 아니라 매출·생산성·품질·R&D 리드타임으로 측정되는가?",
            "- AI Factory와 AI Data Center의 개념 경계가 모든 문서와 데이터에서 일관되게 유지되는가?",
            "",
        ]
    )
    (ROOT / "docs" / "90_research_questions.md").write_text(
        "\n".join(research),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "topics": len(topics),
                "topic_index": "topics/00_topic_index.md",
                "docs_topic_index": "docs/85_topic_index.md",
                "research_questions": "docs/90_research_questions.md",
                "topics_json": "data/topics.json",
                "theme_company_matrix_json": "data/theme_company_matrix.json",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
