#!/usr/bin/env python3
"""Score Topic priorities with a recency- and issue-led model.

The script updates Topic frontmatter, writes data/topic_priorities.json, and
generates reports/topic-priority-report.md. New Topic files are included
automatically when they follow the `NN_*.md` naming convention.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
TOPICS_DIR = ROOT / "topics"
SOURCES_DIR = ROOT / "sources"

WEIGHTS = {
    "recency": 0.30,
    "issue_salience": 0.25,
    "strategic_impact": 0.20,
    "urgency": 0.15,
    "actionability": 0.10,
}

ISSUE_SIGNALS = {
    1.00: (
        "sovereignty", "주권", "규제", "정책", "법", "전력", "냉각", "병목",
        "가격", "price", "수요", "시장", "nvidia", "palantir", "alliance", "파트너",
    ),
    0.75: (
        "foundation model", "파운데이션", "exaone", "gpu", "aidc", "data center",
        "데이터센터", "physical ai", "ai factory", "mobility", "모빌리티",
    ),
    0.45: (
        "agent", "ax", "배터리", "battery", "제조", "manufacturing", "science",
        "r&d", "robot", "로봇", "software", "소프트웨어",
    ),
}

STRATEGIC_SIGNALS = {
    1.00: (
        "성장축", "moat", "경쟁력", "사업성", "플랫폼", "장악", "투자", "build",
        "buy", "제품", "product", "운영 모델", "operating model",
    ),
    0.75: (
        "시장", "수요", "infra", "인프라", "mobility", "모빌리티", "factory",
        "제조 데이터", "foundation model", "산업 특화", "alliance",
    ),
    0.45: (
        "생산성", "r&d", "성과", "kpi", "software", "소프트웨어", "physical ai",
        "sovereignty", "주권",
    ),
}

URGENCY_SIGNALS = {
    1.00: (
        "향후 5년", "가격", "하락", "병목", "수요", "규제", "정책", "투자 균형",
        "build", "buy", "측정", "kpi", "종속", "리스크",
    ),
    0.70: (
        "전망", "시장", "경쟁력", "플랫폼", "장악", "사업성", "전력", "냉각",
        "sovereignty", "주권", "alliance",
    ),
    0.40: ("무엇", "어떻게", "가능", "바꿀", "다음", "전환"),
}

ACTION_SIGNALS = {
    1.00: (
        "어떻게", "측정", "kpi", "제품", "product", "플랫폼", "platform", "build",
        "buy", "투자", "운영 모델", "business", "사업성",
    ),
    0.70: (
        "장악", "집중", "전환", "package", "workflow", "데이터", "software",
        "소프트웨어", "factory",
    ),
    0.40: ("경쟁력", "전망", "기회", "리스크", "생산성"),
}

TYPE_BONUS = {
    "market_outlook": {"issue_salience": 0.50, "urgency": 0.50},
    "partner_analysis": {"issue_salience": 0.45, "urgency": 0.25},
    "technology_assessment": {"issue_salience": 0.25, "strategic_impact": 0.25},
    "operating_model": {"strategic_impact": 0.45, "actionability": 0.45},
    "business_model": {"strategic_impact": 0.50, "actionability": 0.50},
    "policy_analysis": {"issue_salience": 0.50, "urgency": 0.45},
}

PRIORITY_KEYS = {
    "priority",
    "priority_score",
    "priority_updated",
    "priority_model",
    "priority_factors",
    "priority_rationale",
}


def remove_generated_priority_fields(raw_frontmatter: str) -> str:
    """Remove prior generated fields, including malformed wrapped scalar lines."""
    lines = re.sub(r"(?m)^\.\.\.\r?\n", "", raw_frontmatter).splitlines()
    cleaned: list[str] = []
    index = 0
    while index < len(lines):
        match = re.match(r"^([A-Za-z0-9_]+):", lines[index])
        if match and match.group(1) in PRIORITY_KEYS:
            index += 1
            while index < len(lines) and (lines[index].startswith((" ", "\t")) or not lines[index].strip()):
                index += 1
            continue
        cleaned.append(lines[index])
        index += 1
    return "\n".join(cleaned)


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?", text)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    raw_frontmatter = remove_generated_priority_fields(match.group(1))
    return yaml.safe_load(raw_frontmatter) or {}, raw_frontmatter, text[match.end():]


def parse_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value or "").strip().strip("'\"")
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            parsed = datetime.strptime(text, fmt).date()
            if fmt == "%Y-%m":
                return parsed.replace(day=15)
            if fmt == "%Y":
                return parsed.replace(month=7, day=1)
            return parsed
        except ValueError:
            continue
    return None


def freshness_score(age_days: int) -> float:
    if age_days <= 30:
        return 5.0
    if age_days <= 90:
        return 4.5
    if age_days <= 180:
        return 4.0
    if age_days <= 365:
        return 3.3
    if age_days <= 730:
        return 2.4
    if age_days <= 1095:
        return 1.7
    return 1.0


def recency_score(topic: dict[str, Any], source_dates: dict[str, date], as_of: date) -> tuple[float, str]:
    updated = parse_date(topic.get("updated"))
    linked = [
        min(source_dates[source_id], as_of)
        for source_id in topic.get("source_ids") or []
        if source_id in source_dates
    ]
    if updated:
        updated = min(updated, as_of)
    dates = linked + ([updated] if updated else [])
    if not dates:
        return 1.0, "Topic 수정일과 Source 발행일을 확인할 수 없음"

    newest = max(dates)
    newest_score = freshness_score(max(0, (as_of - newest).days))
    recent_180 = sum((as_of - item).days <= 180 for item in linked)
    ratio = recent_180 / len(linked) if linked else (1.0 if updated and (as_of - updated).days <= 180 else 0.0)
    score = min(5.0, newest_score * 0.70 + (1.0 + 4.0 * ratio) * 0.30)
    return round(score, 2), f"최신 기준일 {newest.isoformat()}, 최근 180일 Source 비율 {ratio:.0%}"


def keyword_score(text: str, groups: dict[float, tuple[str, ...]], base: float = 1.6) -> float:
    lowered = text.lower()
    points = 0.0
    matches = 0
    for weight, keywords in groups.items():
        found = {keyword for keyword in keywords if keyword.lower() in lowered}
        points += len(found) * weight
        matches += len(found)
    score = base + min(3.4, points * 0.48)
    if matches == 0:
        score = base
    return round(min(5.0, score), 2)


def apply_type_bonus(scores: dict[str, float], topic_types: list[str]) -> None:
    for topic_type in topic_types:
        for factor, bonus in TYPE_BONUS.get(topic_type, {}).items():
            scores[factor] = min(5.0, scores[factor] + bonus)


def manual_factor_overrides(topic: dict[str, Any], scores: dict[str, float]) -> list[str]:
    """Allow optional editorial overrides for genuinely exceptional new topics."""
    notes = []
    overrides = topic.get("priority_inputs") or {}
    for factor in WEIGHTS:
        if factor in overrides:
            value = max(1.0, min(5.0, float(overrides[factor])))
            scores[factor] = value
            notes.append(f"{factor}={value:.1f} 수동 입력")
    return notes


def priority_band(score: float) -> str:
    if score >= 4.25:
        return "P0"
    if score >= 3.70:
        return "P1"
    if score >= 3.10:
        return "P2"
    return "P3"


def score_topic(topic: dict[str, Any], source_dates: dict[str, date], as_of: date) -> dict[str, Any]:
    searchable = " ".join(
        str(value)
        for value in (
            topic.get("title"),
            topic.get("subtitle"),
            topic.get("question"),
            topic.get("short_answer"),
            " ".join(topic.get("tags") or []),
            " ".join(topic.get("topic_type") or []),
        )
        if value
    )
    recency, recency_note = recency_score(topic, source_dates, as_of)
    scores = {
        "recency": recency,
        "issue_salience": keyword_score(searchable, ISSUE_SIGNALS, 1.7),
        "strategic_impact": keyword_score(searchable, STRATEGIC_SIGNALS, 1.8),
        "urgency": keyword_score(searchable, URGENCY_SIGNALS, 1.5),
        "actionability": keyword_score(searchable, ACTION_SIGNALS, 1.6),
    }
    apply_type_bonus(scores, topic.get("topic_type") or [])
    overrides = manual_factor_overrides(topic, scores)
    scores = {key: round(value, 2) for key, value in scores.items()}
    weighted = round(sum(scores[key] * weight for key, weight in WEIGHTS.items()), 2)
    factor_labels = {
        "recency": "최신성",
        "issue_salience": "이슈성",
        "strategic_impact": "전략 영향도",
        "urgency": "시급성",
        "actionability": "실행 가능성",
    }
    strongest = sorted(scores, key=scores.get, reverse=True)[:2]
    rationale = (
        f"최신성 {scores['recency']:.1f}, 이슈성 {scores['issue_salience']:.1f}이 우선순위를 주도한다. "
        f"강점 요소는 {factor_labels[strongest[0]]}·{factor_labels[strongest[1]]}이며, {recency_note}."
    )
    if overrides:
        rationale += " 편집 보정: " + ", ".join(overrides) + "."
    return {
        "priority": priority_band(weighted),
        "priority_score": weighted,
        "priority_updated": as_of.isoformat(),
        "priority_model": "recency_issue_v1",
        "priority_factors": scores,
        "priority_rationale": rationale,
    }


def yaml_scalar(value: Any) -> str:
    # JSON strings are valid YAML scalars and avoid PyYAML's trailing `...`
    # document marker, which would prematurely terminate the frontmatter.
    return json.dumps(value, ensure_ascii=False)


def priority_block(result: dict[str, Any]) -> list[str]:
    factors = result["priority_factors"]
    return [
        f"priority: {result['priority']}",
        f"priority_score: {result['priority_score']:.2f}",
        f"priority_updated: {result['priority_updated']}",
        f"priority_model: {result['priority_model']}",
        "priority_factors:",
        f"  recency: {factors['recency']:.2f}",
        f"  issue_salience: {factors['issue_salience']:.2f}",
        f"  strategic_impact: {factors['strategic_impact']:.2f}",
        f"  urgency: {factors['urgency']:.2f}",
        f"  actionability: {factors['actionability']:.2f}",
        f"priority_rationale: {yaml_scalar(result['priority_rationale'])}",
    ]


def update_frontmatter(path: Path, raw_frontmatter: str, body: str, result: dict[str, Any]) -> None:
    cleaned = remove_generated_priority_fields(raw_frontmatter).splitlines()

    insert_at = next(
        (i + 1 for i, line in enumerate(cleaned) if line.startswith("updated:")),
        next((i + 1 for i, line in enumerate(cleaned) if line.startswith("status:")), len(cleaned)),
    )
    updated_lines = cleaned[:insert_at] + priority_block(result) + cleaned[insert_at:]
    path.write_text("---\n" + "\n".join(updated_lines) + "\n---\n\n" + body.lstrip("\r\n"), encoding="utf-8")


def load_source_dates() -> dict[str, date]:
    result: dict[str, date] = {}
    for path in SOURCES_DIR.glob("*.md"):
        metadata, _, _ = parse_frontmatter(path)
        published = parse_date(metadata.get("published"))
        if published:
            result[str(metadata.get("id") or path.stem)] = published
    return result


def report_markdown(records: list[dict[str, Any]], as_of: date) -> str:
    lines = [
        "# Topic Priority Report",
        "",
        f"- 기준일: {as_of.isoformat()}",
        "- 모델: `recency_issue_v1`",
        "- 가중치: 최신성 30%, 이슈성 25%, 전략 영향도 20%, 시급성 15%, 실행 가능성 10%",
        "- 등급: P0 ≥ 4.25, P1 ≥ 3.70, P2 ≥ 3.10, P3 < 3.10",
        "",
        "| Rank | Priority | Score | Topic | 최신성 | 이슈성 | 전략 영향 | 시급성 | 실행성 |",
        "|---:|---|---:|---|---:|---:|---:|---:|---:|",
    ]
    for rank, record in enumerate(records, start=1):
        factors = record["priority_factors"]
        lines.append(
            f"| {rank} | {record['priority']} | {record['priority_score']:.2f} "
            f"| {record['title']} | {factors['recency']:.2f} | {factors['issue_salience']:.2f} "
            f"| {factors['strategic_impact']:.2f} | {factors['urgency']:.2f} "
            f"| {factors['actionability']:.2f} |"
        )
    lines.extend(
        [
            "",
            "## 운영 규칙",
            "",
            "- 새 Topic은 `topics/NN_*.md`로 추가한 뒤 `python scripts/score_topic_priorities.py`를 실행한다.",
            "- 기준일이 바뀌거나 Source가 추가되면 다시 실행해 최신성 점수를 갱신한다.",
            "- 자동 판정이 맥락을 놓치는 경우에만 frontmatter의 `priority_inputs`로 1~5 점수를 보정한다.",
            "- One LG 시너지와 Evidence Strength는 평가 요소로 사용하지 않는다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Scoring date in YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="Calculate without changing files")
    args = parser.parse_args()
    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date()
    source_dates = load_source_dates()

    records = []
    topic_paths = sorted(path for path in TOPICS_DIR.glob("[0-9][0-9]_*.md") if not path.name.startswith("00_"))
    for path in topic_paths:
        metadata, raw_frontmatter, body = parse_frontmatter(path)
        result = score_topic(metadata, source_dates, as_of)
        record = {
            "number": int(path.name[:2]),
            "id": metadata["id"],
            "title": metadata["title"],
            "path": f"topics/{path.name}",
            **result,
        }
        records.append(record)
        if not args.dry_run:
            update_frontmatter(path, raw_frontmatter, body, result)

    records.sort(key=lambda item: (-item["priority_score"], item["number"]))
    for rank, record in enumerate(records, start=1):
        record["priority_rank"] = rank

    output = {
        "generated_at": as_of.isoformat(),
        "model": "recency_issue_v1",
        "weights": WEIGHTS,
        "thresholds": {"P0": 4.25, "P1": 3.70, "P2": 3.10},
        "topics": records,
    }
    if not args.dry_run:
        (ROOT / "data" / "topic_priorities.json").write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (ROOT / "reports" / "topic-priority-report.md").write_text(
            report_markdown(records, as_of),
            encoding="utf-8",
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
