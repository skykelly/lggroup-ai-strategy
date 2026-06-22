#!/usr/bin/env python3
"""Migrate all Source cards to the LLM-ingestion Source standard."""

from __future__ import annotations

import concurrent.futures
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "sources"
INVENTORY_PATH = ROOT / "data" / "image_inventory.json"
MANIFEST_PATH = ROOT / "data" / "source_ingestion_manifest.json"
REPORT_PATH = ROOT / "docs" / "87_source_migration_report.md"
RETRIEVED_AT = "2026-06-21"

OFFICIAL_MARKERS = (
    "LG Electronics",
    "LG CNS",
    "LG Energy Solution",
    "LG AI Research",
    "LG Chem",
    "LG Display",
    "LG Innotek",
    "LG U+",
    "LG Corp",
    "MSIT",
    "NVIDIA",
    "Microsoft",
    "World Economic Forum",
    "International Energy Agency",
    "IEA",
    "Uptime Institute",
    "International Federation of Robotics",
    "Vanderbilt",
    "LS ",
    "Sinar Mas",
    "SK Enmove",
    "GRC",
)
SECONDARY_MARKERS = (
    "Korea Times",
    "Digital Today",
    "Maeil",
    "Pulse",
    "Seoul Economic",
    "Asia Economy",
    "Yonhap",
    "전자신문",
    "Financial News",
    "AIMultiple",
    "GPUPerHour",
    "SemiAnalysis",
    "Goldman Sachs",
)
KNOWN_ENTITIES = [
    "LG Corp.",
    "LG Electronics",
    "LG CNS",
    "LG U+",
    "LG Energy Solution",
    "LG AI Research",
    "LG Display",
    "LG Innotek",
    "LG Chem",
    "LG Household & Health Care",
    "LG Technology Ventures",
    "NVIDIA",
    "Palantir",
    "Skild AI",
    "Qualcomm",
    "SDVerse",
    "D&D Pharmatech",
    "Applied Intuition",
    "Microsoft",
    "IEA",
    "MSIT",
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.headings: list[str] = []
        self.paragraphs: list[str] = []
        self.meta: dict[str, str] = {}
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        if tag in {"script", "style", "nav", "footer", "header", "aside"}:
            self._ignored += 1
        if self._ignored:
            return
        if tag == "title":
            self._capture = "title"
            self._buffer = []
        elif tag in {"h1", "h2", "h3"}:
            self._capture = "heading"
            self._buffer = []
        elif tag == "p":
            self._capture = "paragraph"
            self._buffer = []
        elif tag == "meta":
            key = attrs_dict.get("property") or attrs_dict.get("name")
            content = attrs_dict.get("content")
            if key and content:
                self.meta[key.lower()] = clean_text(content)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer", "header", "aside"}:
            self._ignored = max(0, self._ignored - 1)
            return
        if self._ignored or not self._capture:
            return
        expected = {"title": "title", "h1": "heading", "h2": "heading", "h3": "heading", "p": "paragraph"}
        if expected.get(tag) != self._capture:
            return
        value = clean_text(" ".join(self._buffer))
        if value:
            if self._capture == "title":
                self.title_parts.append(value)
            elif self._capture == "heading" and value not in self.headings:
                self.headings.append(value)
            elif self._capture == "paragraph" and len(value) >= 40:
                self.paragraphs.append(value)
        self._capture = None
        self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._capture and not self._ignored:
            self._buffer.append(data)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw) or {}, body


def extract_section(body: str, heading: str, next_heading: str | None = None) -> str:
    if next_heading:
        pattern = rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## {re.escape(next_heading)}\s*$)"
    else:
        pattern = rf"^## {re.escape(heading)}\s*$\n(.*)"
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_bullets(section: str) -> list[str]:
    facts = []
    for line in section.splitlines():
        match = re.match(r"^\s*-\s+(.+)$", line)
        if match:
            fact = clean_text(match.group(1))
            if fact and fact not in facts:
                facts.append(fact)
    return facts


def extract_used_rows(section: str) -> list[tuple[str, str]]:
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or "---" in line or "Entity" in line:
            continue
        new_match = re.match(r"^\|\s*(\[\[[^\]]+\]\]|[^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|$", line)
        if new_match:
            rows.append((new_match.group(1).strip(), new_match.group(3).strip()))
            continue
        old_match = re.match(r"^\|\s*(\[\[[^\]]+\]\]|[^|]+?)\s*\|\s*(.*?)\s*\|$", line)
        if old_match:
            rows.append((old_match.group(1).strip(), old_match.group(2).strip()))
    return rows


def extract_image_rows(section: str) -> list[str]:
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or "---" in line or "image_id" in line:
            continue
        if line.count("|") >= 6:
            rows.append(line)
    return rows


def classify_source(publisher: str, url: str) -> tuple[str, str, str]:
    lower = f"{publisher} {url}".lower()
    if "arxiv.org" in lower:
        return "research_paper", "structured_translation", "A"
    if "github.com" in lower or "huggingface.co" in lower:
        return "repository_or_model_card", "structured_translation", "A"
    if ".pdf" in lower:
        return "report", "structured_translation", "A"
    if any(marker.lower() in lower for marker in SECONDARY_MARKERS):
        return "news_or_analysis", "claim_extraction_only", "C"
    if any(marker.lower() in lower for marker in OFFICIAL_MARKERS):
        return "official_page", "structured_translation", "B"
    return "web_page", "claim_extraction_only", "C"


def infer_language(url: str, publisher: str) -> str:
    lower = f"{url} {publisher}".lower()
    if "/en/" in lower or "global" in lower or "english" in lower or "arxiv" in lower:
        return "en"
    if any(domain in lower for domain in ("mk.co.kr", "yna.co.kr", "etnews.com", "lg.co.kr")):
        return "ko"
    return "en"


def fetch_url(url: str, timeout: int = 18) -> dict[str, Any]:
    if not url or url == "unknown":
        return {"status": "missing_url", "error": "URL missing"}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/pdf,text/plain,*/*;q=0.8",
    }
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read(4_000_000)
            content_type = response.headers.get("Content-Type", "")
            final_url = response.geturl()
            last_modified = response.headers.get("Last-Modified")
        result: dict[str, Any] = {
            "status": "fetched",
            "http_status": 200,
            "final_url": final_url,
            "content_type": content_type,
            "bytes_read": len(data),
            "content_hash": hashlib.sha256(data).hexdigest(),
            "last_modified": last_modified,
            "title": None,
            "description": None,
            "headings": [],
        }
        if "html" in content_type.lower() or data.lstrip().startswith(b"<!DOCTYPE") or b"<html" in data[:1000].lower():
            charset = "utf-8"
            match = re.search(r"charset=([\w-]+)", content_type, re.I)
            if match:
                charset = match.group(1)
            text = data.decode(charset, errors="replace")
            parser = PageParser()
            parser.feed(text)
            result["title"] = (
                parser.meta.get("og:title")
                or parser.meta.get("twitter:title")
                or (parser.title_parts[0] if parser.title_parts else None)
            )
            result["description"] = (
                parser.meta.get("description")
                or parser.meta.get("og:description")
                or parser.meta.get("twitter:description")
            )
            result["headings"] = parser.headings[:20]
        return result
    except urllib.error.HTTPError as exc:
        return {"status": "failed", "http_status": exc.code, "error": f"HTTP {exc.code}: {exc.reason}"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}


def sentence(value: str) -> str:
    value = clean_text(value).strip(" -")
    if not value:
        return ""
    return value if value[-1] in ".!?" else value + "."


def korean_ratio(value: str) -> float:
    if not value:
        return 0.0
    korean = len(re.findall(r"[가-힣]", value))
    letters = len(re.findall(r"[A-Za-z가-힣]", value))
    return korean / letters if letters else 0.0


def make_abstract(
    summary: str,
    facts: list[str],
    publisher: str,
    title: str,
    concept_titles: list[str],
) -> str:
    candidates = [summary, *facts]
    sentences = []
    for item in candidates:
        value = sentence(item)
        if value and korean_ratio(value) >= 0.08 and value not in sentences:
            sentences.append(value)
    if not sentences:
        concepts = ", ".join(concept_titles[:5]) or "관련 AI 전략 개념"
        sentences.append(
            f"{publisher}가 발행한 ‘{title}’ 자료다. 이 Source는 {concepts}에 관한 원문 근거로 사용된다. "
            "현재 자동 변환본에는 한국어 핵심 사실이 충분하지 않아 원문 section 단위 기록을 추가 검토해야 한다."
        )
    return " ".join(sentences[:7])


def title_quality(value: str) -> int:
    value = clean_text(value)
    if not value:
        return -100
    score = min(len(value), 120)
    if value.lower() in {"view", "view.do", "pressview.do", "press releases - 과학기술정보통신부 >"}:
        score -= 150
    if re.fullmatch(r"[A-Z][a-z0-9 ]+", value) and len(value.split()) > 5:
        score -= 30
    if re.search(r"\b(src|view|detail)\b", value, re.I):
        score -= 20
    if any(char in value for char in (":", "—", "-", "·")):
        score += 10
    if re.search(r"[A-Z]{2,}|[가-힣]", value):
        score += 15
    return score


def split_claim_text(value: str) -> list[str]:
    normalized = re.sub(r"^(?:\[원문 언어 기록\]\s*)+", "", clean_text(value))
    parts = re.split(r";\s*|\n+", normalized)
    return [part.strip() for part in parts if len(part.strip()) >= 12]


def fact_key(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", clean_text(value).lower())


def deduplicate_facts(values: list[str]) -> list[str]:
    candidates = []
    seen = set()
    for value in values:
        key = fact_key(value)
        if len(key) < 8 or key in seen:
            continue
        seen.add(key)
        candidates.append((key, clean_text(value)))
    result = []
    for _, value in candidates:
        if re.search(r"\bM\.A\.P\.$", value):
            continue
        result.append(value)
    return result


def collect_appendix_facts() -> dict[str, list[str]]:
    facts: dict[str, list[str]] = {}
    source_heading = re.compile(r"^#{2,3}\s+(src_[a-zA-Z0-9_-]+)\s*$", re.MULTILINE)
    field_pattern = re.compile(r"^-\s+([^:]+):\s*(.*)$")
    for folder in ("docs", "topics"):
        for path in sorted((ROOT / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            matches = list(source_heading.finditer(text))
            for index, match in enumerate(matches):
                source_id = match.group(1)
                end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
                block = text[match.end():end]
                for line in block.splitlines():
                    field = field_pattern.match(line.strip())
                    if not field:
                        continue
                    key = field.group(1).strip().lower().replace(" ", "_")
                    value = clean_text(field.group(2))
                    if key in {"used_for", "key_facts"} and value:
                        facts.setdefault(source_id, [])
                        if value not in facts[source_id]:
                            facts[source_id].append(value)
    return facts


def collect_entity_usage() -> dict[str, list[tuple[str, str]]]:
    usage: dict[str, list[tuple[str, str]]] = {}
    folder_usage = {
        "docs": "전략·시장 근거",
        "topics": "사업기회·전략 근거",
        "concepts": "개념 정의·맥락 근거",
        "companies": "기업 역할·연결 근거",
    }
    excluded = {"docs/83_source_coverage.md", "docs/87_source_migration_report.md"}
    for folder, usage_label in folder_usage.items():
        for path in sorted((ROOT / folder).glob("*.md")):
            relative = path.relative_to(ROOT).as_posix()
            if relative in excluded:
                continue
            text = path.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(text)
            source_ids = set(str(item) for item in metadata.get("source_ids") or [])
            source_ids.update(str(item) for item in metadata.get("sources") or [])
            source_ids.update(
                re.findall(
                    r"\[\[(?:sources/)?(src_[a-zA-Z0-9_-]+)(?:\|[^\]]+)?\]\]",
                    body,
                )
            )
            if not source_ids:
                continue
            title = clean_text(str(metadata.get("title") or path.stem))
            entity = f"[[{path.with_suffix('').relative_to(ROOT).as_posix()}|{title}]]"
            for source_id in source_ids:
                row = (entity, usage_label)
                if row not in usage.setdefault(source_id, []):
                    usage[source_id].append(row)
    return usage


def claim_type(fact: str) -> tuple[str, str]:
    if re.search(r"계획|목표|예정|전망|예상|will|target", fact, re.I):
        return "statement", "medium"
    if re.search(r"조사|측정|기록|보고서|데이터|benchmark|index", fact, re.I):
        return "measured_or_reported", "medium"
    return "statement", "high"


def extract_numbers(fact: str) -> list[tuple[str, str]]:
    patterns = re.findall(
        r"(?<![A-Za-z0-9])(\d[\d,.]*)(?:\s*)(MW|GW|kW|MW급|GW급|%|조\s*원|억\s*원|원|달러|USD|장|개|개월|년|TB|GWh|MWh|VDC|kV|V|축|배)?",
        fact,
        re.I,
    )
    return [(value, unit or "unspecified") for value, unit in patterns]


def entities_in(text: str) -> list[str]:
    aliases = {
        "LG전자": "LG Electronics",
        "LG CNS": "LG CNS",
        "LG U+": "LG U+",
        "LG유플러스": "LG U+",
        "LG에너지솔루션": "LG Energy Solution",
        "LG AI연구원": "LG AI Research",
        "LG AI Research": "LG AI Research",
        "LG디스플레이": "LG Display",
        "LG이노텍": "LG Innotek",
        "LG화학": "LG Chem",
        "LG생활건강": "LG Household & Health Care",
        "NVIDIA": "NVIDIA",
        "Palantir": "Palantir",
        "Skild AI": "Skild AI",
        "Qualcomm": "Qualcomm",
        "SDVerse": "SDVerse",
        "D&D Pharmatech": "D&D Pharmatech",
    }
    found = []
    for alias, canonical in aliases.items():
        if alias.lower() in text.lower() and canonical not in found:
            found.append(canonical)
    for entity in KNOWN_ENTITIES:
        if entity.lower() in text.lower() and entity not in found:
            found.append(entity)
    return found


def relation_predicate(fact: str) -> str:
    if re.search(r"협력|파트너|MOU|collaborat|partner", fact, re.I):
        return "partnered_with"
    if re.search(r"투자|invest", fact, re.I):
        return "invested_in"
    if re.search(r"공급|제공|provide|supply", fact, re.I):
        return "supplies"
    if re.search(r"운영|operate", fact, re.I):
        return "operates"
    if re.search(r"개발|develop", fact, re.I):
        return "develops"
    return "mentioned_with"


def yaml_text(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000).strip()


def migrate_one(
    path: Path,
    fetch: dict[str, Any],
    image_inventory: list[dict[str, Any]],
    appendix_facts: dict[str, list[str]],
    entity_usage: dict[str, list[tuple[str, str]]],
    concept_title_map: dict[str, str],
) -> dict[str, Any]:
    original = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(original)
    source_id = metadata.get("id") or path.stem
    publisher = str(metadata.get("publisher") or "unknown")
    url = str(metadata.get("url") or "unknown")
    source_type, content_policy, reliability_grade = classify_source(publisher, url)
    is_new_standard = "## 3. Atomic Claims" in body
    if is_new_standard:
        old_summary = extract_section(body, "2. Evidence Abstract", "3. Atomic Claims")
        facts = []
        claim_section = extract_section(body, "3. Atomic Claims", "4. Entities and Relationships")
        image_section = extract_section(body, "7. Figures, Tables, and Images", "8. Source Limitations")
        for line in claim_section.splitlines():
            match = re.match(r"^\|\s*`[^`]+`\s*\|.*?\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
            if match:
                for part in split_claim_text(match.group(2)):
                    if part not in facts:
                        facts.append(part)
        used_rows = entity_usage.get(source_id, [])
        old_image_rows = extract_image_rows(image_section)
        old_reliability = ""
    else:
        old_summary = extract_section(body, "1. Source Summary", "2. Key Facts")
        facts = extract_bullets(extract_section(body, "2. Key Facts", "3. Used In"))
        if not facts and old_summary:
            fragments = [clean_text(item) for item in re.split(r"[;\n]", old_summary) if clean_text(item)]
            facts = fragments[:8]
        used_rows = entity_usage.get(source_id, [])
        old_image_rows = extract_image_rows(extract_section(body, "4. Image Notes", "5. Reliability Notes"))
        old_reliability = extract_section(body, "5. Reliability Notes")

    for appendix_fact in appendix_facts.get(source_id, []):
        for part in split_claim_text(appendix_fact):
            if part not in facts:
                facts.append(part)
    facts = deduplicate_facts(facts)

    title = clean_text(str(metadata.get("title") or source_id))
    fetched_title = clean_text(str(fetch.get("title") or ""))
    if fetched_title and title_quality(fetched_title) > title_quality(title):
        title = fetched_title[:240]
    summary_for_abstract = "" if is_new_standard else old_summary if korean_ratio(old_summary) >= 0.15 else ""
    related_concepts = [str(item) for item in metadata.get("related_concepts") or []]
    concept_titles = [concept_title_map.get(item, item.replace("-", " ")) for item in related_concepts]
    abstract = make_abstract(summary_for_abstract, facts, publisher, title, concept_titles)

    claims = facts or [old_summary or f"{publisher} 자료가 관련 Entity의 근거로 연결되어 있다."]
    claim_rows = []
    number_rows = []
    relation_rows = []
    seen_relations = set()
    for index, fact in enumerate(claims, start=1):
        claim_id = f"{source_id}_c{index:02d}"
        evidence_type, certainty = claim_type(fact)
        numbers = extract_numbers(fact)
        numeric_text = "; ".join(f"{value} {unit}" for value, unit in numbers)
        display_fact = sentence(fact)
        if korean_ratio(fact) < 0.08:
            display_fact = f"[원문 언어 기록] {display_fact}"
        claim_rows.append(
            f"| `{claim_id}` | Source Notes / 원문 재확인 필요 | "
            f"{entities_in(fact)[0] if entities_in(fact) else publisher} | {display_fact} | "
            f"{numeric_text or '-'} | {evidence_type} | {certainty} |"
        )
        for value, unit in numbers:
            nature = "target" if re.search(r"목표|계획|예정|target", fact, re.I) else "reported"
            number_rows.append(f"| {sentence(fact)} | {value} | {unit} | {metadata.get('published', 'unknown')} | {nature} | `{claim_id}` |")
        found_entities = entities_in(fact)
        if len(found_entities) >= 2:
            relation = (found_entities[0], relation_predicate(fact), found_entities[1], claim_id)
            if relation not in seen_relations:
                relation_rows.append(
                    f"| {relation[0]} | `{relation[1]}` | {relation[2]} | `{claim_id}` | {metadata.get('published', 'unknown')} |"
                )
                seen_relations.add(relation)

    if not number_rows:
        number_rows = ["| 명시적 수치 없음 | - | - | - | not_applicable | - |"]
    if not relation_rows:
        relation_rows = ["| 명시적 관계 추출 없음 | - | - | 원문 구조화 재검토 필요 | - |"]

    headings = [clean_text(value) for value in fetch.get("headings", []) if clean_text(value)]

    terminology_rows = []
    for concept in metadata.get("related_concepts") or []:
        term = concept.replace("-", " ")
        concept_title = concept_title_map.get(concept, term)
        terminology_rows.append(
            f"| `{term}` | {concept_title} | 이 Source가 관련 근거로 사용되는 개념 | "
            f"[[concepts/{concept}|{concept_title}]] |"
        )
    if not terminology_rows:
        terminology_rows = ["| 추가 추출 필요 | - | 원문 용어와 Concept 연결 보강 필요 | - |"]

    matched_images = []
    normalized_url = url.rstrip("/")
    for item in image_inventory:
        source_url = str(item.get("source_url") or "").rstrip("/")
        used_by = item.get("used_by") or []
        if source_url == normalized_url or f"sources/{path.name}" in used_by:
            matched_images.append(item)
    image_rows = []
    for item in matched_images:
        description_text = clean_text(str(item.get("caption") or item.get("error") or ""))
        image_rows.append(
            f"| {item.get('image_id', '')} | image | 원문 또는 Source Notes | {description_text} | "
            f"{item.get('original_url', '')} | {item.get('local_path') or ''} | {item.get('status', '')} |"
        )
    if not image_rows and old_image_rows:
        image_rows = [
            "| 기존 이미지 기록 | image | 기존 Source Card | 상세 필드는 재검토 필요 | - | - | legacy_record |"
        ]
    if not image_rows:
        image_rows = ["| 없음 | - | - | 연결된 시각자료 없음 | - | - | not_linked |"]

    used_in_rows = []
    all_claim_ids = ", ".join(f"`{source_id}_c{i:02d}`" for i in range(1, len(claims) + 1))
    for entity, usage in used_rows:
        used_in_rows.append(f"| {entity} | {all_claim_ids} | {usage} |")
    if not used_in_rows:
        used_in_rows = ["| 연결 Entity 없음 | - | Source metadata 보강 필요 |"]

    directness = "high" if reliability_grade in {"A", "B"} else "medium"
    verifiability = "high" if len(facts) >= 4 else "medium" if facts else "low"
    capture_status = "complete" if fetch.get("status") == "fetched" and len(facts) >= 4 else "partial"
    if fetch.get("status") in {"missing_url"}:
        capture_status = "metadata_only"
    limitations = [
        "Source Card의 한국어 기록은 원문을 대체하지 않으며, 전략적 해석은 Docs와 Topics에서 관리한다.",
        "기존 Source Notes에서 승격한 claim은 원문 section·page 위치를 재확인해야 한다.",
    ]
    if content_policy == "claim_extraction_only":
        limitations.append("저작권 또는 접근 제한 가능성이 있는 2차 자료이므로 전체 번역 대신 claim 단위로 기록했다.")
    if fetch.get("status") != "fetched":
        limitations.append(f"원문 자동 수집 실패: {fetch.get('error', fetch.get('status', 'unknown'))}.")
    if old_reliability:
        limitations.append(sentence(old_reliability))

    updated = fetch.get("last_modified") or "unknown"
    metadata.update(
        {
            "id": source_id,
            "type": "source",
            "title": title,
            "publisher": publisher,
            "authors": metadata.get("authors") or [],
            "published": metadata.get("published", "unknown"),
            "updated": updated,
            "retrieved_at": RETRIEVED_AT,
            "url": url,
            "source_type": source_type,
            "language": metadata.get("language") or infer_language(url, publisher),
            "content_policy": content_policy,
            "capture_status": capture_status,
            "archive_url": metadata.get("archive_url"),
            "local_raw_path": metadata.get("local_raw_path"),
            "content_hash": fetch.get("content_hash") or metadata.get("content_hash"),
            "license": metadata.get("license") or "unknown",
            "reliability_grade": reliability_grade,
        }
    )

    impact_entities = ", ".join(entity for entity, _ in used_rows[:20]) or "연결 Entity 없음"
    markdown = f"""---
{yaml_text(metadata)}
---

# {title}

## 1. Source Identity

| 항목 | 내용 |
|---|---|
| 발행기관 | {publisher} |
| 저자·발표자 | {", ".join(metadata.get("authors") or []) or "unknown"} |
| 원문 유형 | `{source_type}` |
| 발행일·수정일 | {metadata.get("published", "unknown")} / {updated} |
| 수집일 | {RETRIEVED_AT} |
| 원문 언어 | `{metadata.get("language")}` |
| 원문 URL | {url} |
| 최종 도달 URL | {fetch.get("final_url") or url} |
| 수집 범위 | `{capture_status}` |
| 라이선스 | `{metadata.get("license")}` |

## 2. Evidence Abstract

{abstract}

## 3. Atomic Claims

| claim_id | 원문 위치 | 주체 | 주장·사실 | 수치·기간 | 근거 유형 | 확실성 |
|---|---|---|---|---|---|---|
{chr(10).join(claim_rows)}

## 4. Entities and Relationships

| 주체 | 관계 | 대상 | 원문 근거 | 유효시점 |
|---|---|---|---|---|
{chr(10).join(relation_rows)}

## 5. Numbers, Dates, and Commitments

| 항목 | 값 | 단위 | 기준시점 | 성격 | claim_id |
|---|---:|---|---|---|---|
{chr(10).join(number_rows)}

## 6. Definitions and Terminology

| 원문 용어 | 한국어 표기 | 원문에서의 의미 | Wiki Concept 후보 |
|---|---|---|---|
{chr(10).join(terminology_rows)}

## 7. Figures, Tables, and Images

| asset_id | 유형 | 원문 위치 | 설명·읽을 수 있는 사실 | original_url | local_path | status |
|---|---|---|---|---|---|---|
{chr(10).join(image_rows)}

## 8. Source Limitations

{chr(10).join(f"- {item}" for item in limitations)}

## 9. Reliability Assessment

| 평가 항목 | 판단 | 이유 |
|---|---|---|
| 출처 직접성 | `{directness}` | {publisher}의 자료 유형과 발행 주체를 기준으로 평가 |
| 사실 검증성 | `{verifiability}` | 기존 Source Notes에 {len(facts)}개 핵심 사실이 구조화되어 있음 |
| 최신성 | `{"current" if str(metadata.get("published", "")).startswith(("2025", "2026")) else "dated_or_unknown"}` | 발행일 {metadata.get("published", "unknown")} 기준 |
| 이해관계 | `{"high" if reliability_grade == "B" else "medium"}` | 공식 발표자료는 직접성이 높지만 발행 주체의 이해관계를 포함함 |
| 종합 등급 | `{reliability_grade}` | 원문 직접성, 접근성, 기존 facts의 구체성을 종합 평가 |

## 10. Used In

| Entity | 사용한 claim_id | 사용 방식 |
|---|---|---|
{chr(10).join(used_in_rows)}

## 11. Update Hooks

- **변경 감지 기준:** 원문 수정일, 핵심 수치, 제품 버전, 파트너, 투자·생산·구축 목표 변경
- **영향받는 Entity:** {impact_entities}
- **재검토 조건:** 후속 실적 발표, 목표 시점 도달, 계약·제품·정책의 새 버전 공개
- **마지막 검토일:** {RETRIEVED_AT}

## Appendix A. Permitted Evidence Excerpts

저작권과 검증 목적에 필요한 짧은 원문 발췌는 원문 위치 확인 후 추가한다. 현재 자동 마이그레이션에서는 전체 원문을 복제하지 않았다.

## Appendix B. Ingestion Notes

- **변환 방식:** 기존 Source Summary와 Key Facts를 atomic claim으로 승격
- **원문 수집 상태:** `{fetch.get("status", "unknown")}`
- **HTTP / 오류:** `{fetch.get("http_status", "-")}` / {fetch.get("error", "-")}
- **Content-Type:** `{fetch.get("content_type", "unknown")}`
- **Content Hash:** `{fetch.get("content_hash") or metadata.get("content_hash") or "unknown"}`
- **감지된 heading 수:** {len(headings)}
- **제외 범위:** navigation, footer, 광고, cookie 문구 및 전체 원문 복제
- **후속 작업:** claim별 원문 section·page 위치를 우선순위에 따라 수동 또는 정밀 파서로 보강
"""
    path.write_text(markdown, encoding="utf-8")
    return {
        "id": source_id,
        "path": path.relative_to(ROOT).as_posix(),
        "title": title,
        "publisher": publisher,
        "published": metadata.get("published", "unknown"),
        "url": url,
        "source_type": source_type,
        "content_policy": content_policy,
        "capture_status": capture_status,
        "fetch_status": fetch.get("status"),
        "http_status": fetch.get("http_status"),
        "error": fetch.get("error"),
        "claim_count": len(claims),
        "number_count": len(number_rows) if number_rows[0].find("명시적 수치 없음") == -1 else 0,
        "relation_count": len(relation_rows) if relation_rows[0].find("명시적 관계 추출 없음") == -1 else 0,
        "heading_count": len(headings),
        "image_count": len(matched_images),
        "reliability_grade": reliability_grade,
        "bytes_before": len(original.encode("utf-8")),
        "bytes_after": len(markdown.encode("utf-8")),
    }


def main() -> int:
    source_paths = sorted(path for path in SOURCES_DIR.glob("*.md") if not path.name.startswith("."))
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8")).get("images", [])
    appendix_facts = collect_appendix_facts()
    entity_usage = collect_entity_usage()
    concept_title_map = {}
    for concept_path in sorted((ROOT / "concepts").glob("*.md")):
        concept_metadata, _ = parse_frontmatter(concept_path.read_text(encoding="utf-8"))
        concept_title_map[concept_path.stem] = clean_text(
            str(concept_metadata.get("title") or concept_path.stem.replace("-", " "))
        )
    metadata_by_path = {}
    unique_urls = {}
    for path in source_paths:
        metadata, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        url = str(metadata.get("url") or "unknown")
        metadata_by_path[path] = metadata
        unique_urls.setdefault(url, None)

    print(f"Fetching {len(unique_urls)} unique URLs for {len(source_paths)} Source cards...")
    fetch_results: dict[str, dict[str, Any]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(fetch_url, url): url for url in unique_urls}
        for index, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            url = futures[future]
            fetch_results[url] = future.result()
            print(f"[{index}/{len(futures)}] {fetch_results[url].get('status')}: {url}")

    migrated = []
    for path in source_paths:
        url = str(metadata_by_path[path].get("url") or "unknown")
        migrated.append(
            migrate_one(
                path,
                fetch_results[url],
                inventory,
                appendix_facts,
                entity_usage,
                concept_title_map,
            )
        )

    summary = {
        "generated_at": f"{RETRIEVED_AT}T00:00:00+09:00",
        "sources": len(migrated),
        "unique_urls": len(unique_urls),
        "fetch_succeeded": sum(item["fetch_status"] == "fetched" for item in migrated),
        "fetch_failed": sum(item["fetch_status"] != "fetched" for item in migrated),
        "capture_complete": sum(item["capture_status"] == "complete" for item in migrated),
        "capture_partial": sum(item["capture_status"] == "partial" for item in migrated),
        "metadata_only": sum(item["capture_status"] == "metadata_only" for item in migrated),
        "total_claims": sum(item["claim_count"] for item in migrated),
        "total_numeric_records": sum(item["number_count"] for item in migrated),
        "total_relationships": sum(item["relation_count"] for item in migrated),
        "content_policy": dict(Counter(item["content_policy"] for item in migrated)),
        "reliability_grades": dict(Counter(item["reliability_grade"] for item in migrated)),
    }
    MANIFEST_PATH.write_text(
        json.dumps({"summary": summary, "sources": migrated}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    sources_index_path = ROOT / "data" / "sources.json"
    existing_index = (
        json.loads(sources_index_path.read_text(encoding="utf-8"))
        if sources_index_path.exists()
        else {"sources": []}
    )
    existing_by_id = {item["id"]: item for item in existing_index.get("sources", [])}
    indexed_sources = []
    for item in migrated:
        record = existing_by_id.get(item["id"], {"id": item["id"]})
        record.update(
            {
                "title": item["title"],
                "publisher": item["publisher"],
                "published": item["published"],
                "url": item["url"],
                "path": item["path"],
                "status": item["capture_status"],
                "capture_status": item["capture_status"],
                "fetch_status": item["fetch_status"],
                "content_policy": item["content_policy"],
                "reliability_grade": item["reliability_grade"],
                "claim_count": item["claim_count"],
                "number_count": item["number_count"],
                "relation_count": item["relation_count"],
            }
        )
        indexed_sources.append(record)
    existing_index["sources"] = indexed_sources
    existing_index["ingestion_summary"] = summary
    sources_index_path.write_text(
        json.dumps(existing_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    coverage = [
        "---",
        "id: source_coverage",
        "type: index",
        "title: Source Coverage",
        f"generated_at: {RETRIEVED_AT}",
        "---",
        "",
        "# Source Coverage",
        "",
        f"총 {len(migrated)}개 Source의 수집 상태와 LLM ingest 구조화 범위를 정리한다.",
        "",
        "| Source | Publisher | Published | Used By | Claims | Fetch | Capture |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for item in migrated:
        usage_count = len(entity_usage.get(item["id"], []))
        coverage.append(
            f"| [[sources/{item['id']}|{item['title']}]] | {item['publisher']} | "
            f"{item['published']} | {usage_count} | {item['claim_count']} | "
            f"`{item['fetch_status']}` | `{item['capture_status']}` |"
        )
    (ROOT / "docs" / "83_source_coverage.md").write_text(
        "\n".join(coverage) + "\n",
        encoding="utf-8",
    )

    failures = [item for item in migrated if item["fetch_status"] != "fetched"]
    low_claims = [item for item in migrated if item["claim_count"] < 3]
    report = [
        "---",
        "id: source_migration_report",
        "type: report",
        "title: Source Migration Report",
        f"generated_at: {RETRIEVED_AT}",
        "---",
        "",
        "# Source Migration Report",
        "",
        "## 1. Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    report.extend(f"| {key} | {value} |" for key, value in summary.items() if not isinstance(value, dict))
    report.extend(
        [
            "",
            "## 2. Fetch Failures",
            "",
            "| Source | URL | Error |",
            "|---|---|---|",
        ]
    )
    report.extend(
        f"| [[sources/{item['id']}]] | {item['url']} | {item.get('error') or item.get('http_status') or 'unknown'} |"
        for item in failures
    )
    if not failures:
        report.append("| 없음 | - | - |")
    report.extend(
        [
            "",
            "## 3. Low-Claim Sources",
            "",
            "3개 미만의 atomic claim만 확보된 Source다. 우선 재수집·수동 검토 대상이다.",
            "",
        ]
    )
    report.extend(f"- [[sources/{item['id']}]] — {item['claim_count']} claim(s)" for item in low_claims)
    report.extend(
        [
            "",
            "## 4. Next Review Priority",
            "",
            "1. 원문 수집 실패이면서 참조 횟수가 높은 Source",
            "2. 목표·수치가 있으나 원문 위치가 `재확인 필요`인 Source",
            "3. 3개 미만 claim Source",
            "4. 중복 URL에 서로 다른 source_id가 연결된 Source",
        ]
    )
    REPORT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
