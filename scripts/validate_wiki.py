#!/usr/bin/env python3
"""Validate Wiki links, entity IDs, topic fields, and image inventory."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "reports" / "wiki-validation-report.md"
ENTITY_DIRS = ("docs", "topics", "concepts", "companies", "sources")
VALID_THEMES = {
    "ai_data_center_infra",
    "physical_ai_smart_manufacturing",
    "ai_mobility_sdv_aidv",
    "enterprise_ax_agentic_operating_model",
    "ai_for_science_bio_materials_battery",
    "global_ai_alliance_open_innovation",
}


def parse_frontmatter(path: Path) -> tuple[dict, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, "missing frontmatter"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, "unclosed frontmatter"
    raw = parts[1]
    try:
        return yaml.safe_load(raw) or {}, None
    except yaml.YAMLError as exc:
        repaired = []
        for line in raw.splitlines():
            match = re.match(r"^(title):\s*(.+)$", line)
            if match and ":" in match.group(2) and not match.group(2).startswith(("'", '"')):
                line = f"{match.group(1)}: {json.dumps(match.group(2), ensure_ascii=False)}"
            repaired.append(line)
        try:
            return yaml.safe_load("\n".join(repaired)) or {}, f"non-standard YAML repaired: {exc}"
        except yaml.YAMLError:
            return {}, f"invalid YAML: {exc}"


def resolve_wikilink(target: str) -> bool:
    target = target.strip().split("#", 1)[0]
    if not target:
        return True
    path = ROOT / target
    if path.suffix:
        return path.is_file()
    return path.with_suffix(".md").is_file()


def main() -> int:
    errors = []
    warnings = []
    stats = Counter()
    metadata_by_path = {}
    ids = defaultdict(list)

    markdown_files = []
    for folder in ENTITY_DIRS:
        markdown_files.extend(sorted((ROOT / folder).rglob("*.md")))
    markdown_files.extend(sorted((ROOT / "_templates").glob("*.md")))
    markdown_files.extend([ROOT / "README.md"])
    markdown_files = [path for path in markdown_files if path.is_file()]

    for path in markdown_files:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        stats["markdown_files"] += 1

        if path.name != "README.md" and "_templates" not in path.parts and not path.name.startswith("."):
            metadata, yaml_issue = parse_frontmatter(path)
            metadata_by_path[relative] = metadata
            if yaml_issue:
                if yaml_issue.startswith("non-standard"):
                    warnings.append((relative, yaml_issue))
                else:
                    errors.append((relative, yaml_issue))
            if metadata.get("id"):
                ids[str(metadata["id"])].append(relative)
            elif path.parent.name not in {"assets"}:
                errors.append((relative, "frontmatter id 누락"))

        for target in re.findall(r"\[\[([^\]|]+)", text):
            stats["wikilinks"] += 1
            if not resolve_wikilink(target):
                errors.append((relative, f"broken wikilink: [[{target}]]"))

        for src in re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', text):
            stats["image_references"] += 1
            if src.startswith("assets/images/"):
                stats["local_image_references"] += 1
                if not (ROOT / src).is_file():
                    errors.append((relative, f"broken local image: {src}"))
                if len(Path(src).parts) != 3:
                    errors.append((relative, f"image path is not flat: {src}"))
            elif src.startswith(("http://", "https://")):
                stats["remote_image_references"] += 1
                warnings.append((relative, f"remote image retained: {src}"))
            else:
                errors.append((relative, f"unsupported image path: {src}"))

        is_content_doc = bool(
            re.match(r"^docs/0[1-6]_", relative)
            or re.match(r"^topics/(?:0[1-9]|1[0-8])_", relative)
        )
        needed_count = text.count("IMAGE_URL_NEEDED") if is_content_doc else 0
        if needed_count:
            stats["image_url_needed_occurrences"] += needed_count
            warnings.append((relative, f"IMAGE_URL_NEEDED {needed_count}건"))

    for entity_id, paths in ids.items():
        if len(paths) > 1:
            errors.append((", ".join(paths), f"duplicate frontmatter id: {entity_id}"))

    concept_files = {path.stem for path in (ROOT / "concepts").glob("*.md")}
    company_files = {path.stem for path in (ROOT / "companies").glob("*.md")}
    partner_files = {path.stem for path in (ROOT / "companies" / "partners").glob("*.md")}
    source_files = {path.stem for path in (ROOT / "sources").glob("*.md")}
    topic_ids = {
        metadata.get("id")
        for path, metadata in metadata_by_path.items()
        if path.startswith("topics/") and Path(path).name != "00_topic_index.md"
    }

    for relative, metadata in metadata_by_path.items():
        for theme in metadata.get("related_themes") or []:
            if theme not in VALID_THEMES:
                errors.append((relative, f"unknown theme id: {theme}"))
        if metadata.get("theme_id") and metadata["theme_id"] not in VALID_THEMES:
            errors.append((relative, f"unknown theme_id: {metadata['theme_id']}"))
        for concept in metadata.get("related_concepts") or []:
            if concept not in concept_files:
                errors.append((relative, f"missing concept entity: {concept}"))
        for company in metadata.get("related_companies") or []:
            if company not in company_files and company not in partner_files:
                errors.append((relative, f"missing company entity: {company}"))
        for source_id in metadata.get("source_ids") or []:
            if source_id not in source_files:
                errors.append((relative, f"missing source entity: {source_id}"))
        if (
            metadata.get("type") in {"concept", "company"}
            and "source_ids" in metadata
            and not metadata.get("source_ids")
        ):
            warnings.append((relative, "source_ids 비어 있음 — Source 보강 필요"))
        for topic_id in metadata.get("related_topics") or []:
            if topic_id not in topic_ids:
                errors.append((relative, f"missing topic id: {topic_id}"))

    topic_paths = [
        path
        for path in sorted((ROOT / "topics").glob("[0-9][0-9]_*.md"))
        if 1 <= int(path.name[:2]) <= 18
    ]
    stats["topics"] = len(topic_paths)
    if len(topic_paths) != 18:
        errors.append(("topics/", f"expected 18 topic files, found {len(topic_paths)}"))
    if list((ROOT / "topics").glob("19_*.md")) or list((ROOT / "topics").glob("20_*.md")):
        errors.append(("topics/", "forbidden Topic 19 or 20 exists"))
    for path in topic_paths:
        metadata, _ = parse_frontmatter(path)
        for field in ("question", "short_answer", "image_policy"):
            if not metadata.get(field):
                errors.append((path.relative_to(ROOT).as_posix(), f"missing topic field: {field}"))
        if "Image Inventory" not in path.read_text(encoding="utf-8"):
            errors.append((path.relative_to(ROOT).as_posix(), "missing Image Inventory section"))

    ai_factory = metadata_by_path.get("concepts/ai-factory.md", {})
    if ai_factory.get("primary_theme") != "physical_ai_smart_manufacturing":
        errors.append(("concepts/ai-factory.md", "AI Factory primary_theme mismatch"))
    ai_dc = metadata_by_path.get("concepts/ai-data-center.md", {})
    if ai_dc.get("primary_theme") != "ai_data_center_infra":
        errors.append(("concepts/ai-data-center.md", "AI Data Center primary_theme mismatch"))

    for folder in ("docs", "topics", "concepts", "companies", "sources", "data"):
        for path in (ROOT / folder).rglob("*"):
            if not path.is_file():
                continue
            try:
                if "ai_infra_factory" in path.read_text(encoding="utf-8", errors="ignore"):
                    errors.append((path.relative_to(ROOT).as_posix(), "legacy id ai_infra_factory remains"))
            except OSError:
                pass

    inventory_path = ROOT / "data" / "image_inventory.json"
    if not inventory_path.is_file():
        errors.append(("data/image_inventory.json", "image inventory missing"))
        inventory = {"images": []}
    else:
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory_urls = {item.get("original_url") for item in inventory["images"]}
    inventory_local = {item.get("local_path") for item in inventory["images"] if item.get("local_path")}
    for item in inventory["images"]:
        if item.get("status") == "downloaded":
            if not item.get("local_path") or not (ROOT / item["local_path"]).is_file():
                errors.append(("data/image_inventory.json", f"missing downloaded image: {item.get('image_id')}"))
            if item.get("local_path") and len(Path(item["local_path"]).parts) != 3:
                errors.append(("data/image_inventory.json", f"non-flat local path: {item['local_path']}"))
        if not isinstance(item.get("used_by"), list):
            errors.append(("data/image_inventory.json", f"used_by is not array: {item.get('image_id')}"))

    if (ROOT / "assets" / "images").is_dir():
        subdirs = [path for path in (ROOT / "assets" / "images").iterdir() if path.is_dir()]
        for path in subdirs:
            errors.append((path.relative_to(ROOT).as_posix(), "assets/images must remain flat"))
        local_files = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "assets" / "images").iterdir()
            if path.is_file() and path.name != ".gitkeep"
        }
        untracked = sorted(local_files - inventory_local)
        for path in untracked:
            warnings.append((path, "local image not referenced by image_inventory.json"))

    required_files = [
        "README.md",
        "docs/00_overview.md",
        "docs/80_theme_company_matrix.md",
        "docs/81_concept_theme_map.md",
        "docs/82_partner_map.md",
        "docs/83_source_coverage.md",
        "docs/84_concept_index.md",
        "docs/85_topic_index.md",
        "docs/90_research_questions.md",
        "topics/00_topic_index.md",
        "data/concepts.json",
        "data/companies.json",
        "data/sources.json",
        "data/topics.json",
        "data/theme_company_matrix.json",
        "data/image_inventory.json",
    ]
    for required in required_files:
        if not (ROOT / required).is_file():
            errors.append((required, "required file missing"))

    sources_data_path = ROOT / "data" / "sources.json"
    if sources_data_path.is_file():
        sources_data = json.loads(sources_data_path.read_text(encoding="utf-8"))
        for source in sources_data.get("sources", []):
            if source.get("status") == "needs_metadata":
                warnings.append(
                    (
                        source.get("path", "data/sources.json"),
                        "Source URL 또는 publisher metadata 보강 필요",
                    )
                )

    errors = list(dict.fromkeys(errors))
    warnings = list(dict.fromkeys(warnings))
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Wiki Validation Report",
        "",
        f"- Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        f"- Markdown files scanned: {stats['markdown_files']}",
        f"- Wikilinks checked: {stats['wikilinks']}",
        f"- Image references checked: {stats['image_references']}",
        f"- Local image references: {stats['local_image_references']}",
        f"- Remote image references retained: {stats['remote_image_references']}",
        f"- IMAGE_URL_NEEDED occurrences: {stats['image_url_needed_occurrences']}",
        "",
        "## Errors",
        "",
    ]
    if errors:
        lines.extend(f"- `{path}` — {message}" for path, message in errors)
    else:
        lines.append("- 없음")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        lines.extend(f"- `{path}` — {message}" for path, message in warnings)
    else:
        lines.append("- 없음")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Error는 링크·ID·필수 구조·로컬 파일 정합성 문제다.",
            "- Warning은 다운로드 실패로 유지된 원격 이미지, IMAGE_URL_NEEDED, metadata 보강 필요처럼 원본 정책상 허용되는 항목이다.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"errors": len(errors), "warnings": len(warnings), "report": REPORT_PATH.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
