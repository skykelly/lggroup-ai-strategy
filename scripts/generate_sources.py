#!/usr/bin/env python3
"""Generate source cards from docs/topics Source Notes and entity frontmatter."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "sources"
INVENTORY_PATH = ROOT / "data" / "image_inventory.json"

PUBLISHERS = {
    "lg.com": "LG Electronics",
    "lgcorp.com": "LG Corp.",
    "lg.co.kr": "LG Corp.",
    "lgcns.com": "LG CNS",
    "lgresearch.ai": "LG AI Research",
    "lgensol.com": "LG Energy Solution",
    "inside.lgensol.com": "LG Energy Solution Battery Inside",
    "news.lgensol.com": "LG Energy Solution Newsroom",
    "lgchem.com": "LG Chem",
    "lgdisplay.com": "LG Display",
    "lginnotek.com": "LG Innotek",
    "lguplus.com": "LG U+",
    "nvidia.com": "NVIDIA",
    "blogs.nvidia.com": "NVIDIA Blog",
    "developer.nvidia.com": "NVIDIA Technical Blog",
    "prnewswire.com": "PRNewswire",
    "digitaltoday.co.kr": "Digital Today",
    "pulse.mk.co.kr": "Pulse by Maeil Business News Korea",
    "mk.co.kr": "Maeil Business Newspaper",
    "sedaily.com": "Seoul Economic Daily",
    "etnews.com": "Electronic Times",
    "koreatimes.co.kr": "The Korea Times",
    "yna.co.kr": "Yonhap News Agency",
    "asiae.co.kr": "The Asia Business Daily",
    "iea.org": "International Energy Agency",
    "goldmansachs.com": "Goldman Sachs",
    "arxiv.org": "arXiv",
    "github.com": "GitHub",
    "huggingface.co": "Hugging Face",
    "msit.go.kr": "Ministry of Science and ICT",
    "ces.tech": "Consumer Technology Association",
    "ifr.org": "International Federation of Robotics",
    "weforum.org": "World Economic Forum",
    "gpuperhour.com": "GPUperHour",
    "aimultiple.com": "AIMultiple",
    "semianalysis.com": "SemiAnalysis",
}

SOURCE_OVERRIDES = {
    "src_uptime_institute_pue": {
        "url": "https://uptimeinstitute.com/beyond-pue-tackling-it-efficiency",
        "publisher": "Uptime Institute",
        "title": "Beyond PUE: Tackling IT Efficiency",
        "used_for": "PUE의 적용 범위와 데이터센터 효율 평가 시 보완 지표가 필요한 이유",
    },
    "src_sinar_mas_official": {
        "url": "https://www.sinarmas.com/en/",
        "publisher": "Sinar Mas",
        "title": "Sinar Mas Official",
        "used_for": "Sinar Mas의 인도네시아 사업 기반 확인. LG와의 직접 AIDC 협력은 공개 근거 미확인.",
    },
    "src_microsoft_datacenter_sustainability": {
        "url": "https://datacenters.microsoft.com/",
        "publisher": "Microsoft",
        "title": "Microsoft Datacenters",
        "used_for": "글로벌 cloud·AI 데이터센터 운영과 지속가능성 benchmark",
    },
    "src_ls_electric_official": {
        "url": "https://www.ls-electric.com/",
        "publisher": "LS ELECTRIC",
        "title": "LS ELECTRIC Official",
        "used_for": "전력기기·배전·에너지 관리 역량 확인. LG AIDC 직접 협력은 공개 근거 미확인.",
    },
    "src_ls_cable_system_official": {
        "url": "https://www.lscns.com/",
        "publisher": "LS Cable & System",
        "title": "LS Cable & System Official",
        "used_for": "전력·통신 케이블과 인프라 구축 역량 확인. LG AIDC 직접 협력은 공개 근거 미확인.",
    },
    "src_grc_immersion_cooling": {
        "url": "https://www.grcooling.com/",
        "publisher": "GRC",
        "title": "GRC Immersion Cooling",
        "used_for": "데이터센터 액침냉각 기술과 운영 역량 확인. LG와의 직접 협력은 공개 근거 미확인.",
    },
    "src_sk_enmove_official": {
        "url": "https://www.skenmove.com/",
        "publisher": "SK Enmove",
        "title": "SK Enmove Official",
        "used_for": "열관리·윤활 기반 사업 역량 확인. LG AIDC 직접 협력은 공개 근거 미확인.",
    },
    "src_vumc_research": {
        "url": "https://www.vumc.org/research/",
        "publisher": "Vanderbilt University Medical Center",
        "title": "VUMC Research",
        "used_for": "의료·임상 연구 및 validation 역량 확인. LG AI Research와의 직접 협력은 공개 근거 미확인.",
    },
    "src_iea_energy_ai_2026": {
        "url": "https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai",
        "publisher": "International Energy Agency",
    },
    "src_ifr_world_robotics_20250925": {
        "url": "https://ifr.org/img/worldrobotics/Executive_Summary_WR_2025_Industrial_Robots.pdf",
        "publisher": "International Federation of Robotics",
        "title": "World Robotics 2025 — Industrial Robots Executive Summary",
        "published": "2025-09-25",
    },
    "src_lgcns_ai_box_20260304": {
        "url": "https://www.lgcns.com/kr/newsroom/press/detail.aidc-2603-2",
    },
    "src_lgcorp_smart_park_lighthouse_20220331": {
        "url": "https://www.lg.com/global/newsroom/news/home-appliance-solution/lg-smart-park-named-lighthouse-factory-for-futuristic-manufacturing-technology/",
        "publisher": "LG Electronics Newsroom",
        "title": "LG Smart Park Named Lighthouse Factory",
        "published": "2022-03-31",
    },
    "src_lgensol_ess_expansion_20260415": {
        "url": "https://news.lgensol.com/company-news/supplementary-stories/4880/",
    },
    "src_lginnotek_ces2026_showcase": {
        "url": "https://www.lginnotek.com/showcase/ces2026.do",
        "publisher": "LG Innotek",
    },
    "src_lguplus_paju_aidc_20260607": {
        "url": "https://www.digitaltoday.co.kr/en/view/61108/lgu-to-step-up-ai-data-centre-business-targets-5-trillion-won-in-orders-by-2030",
    },
    "src_pulse_lguplus_paju_aidc_20260608": {
        "url": "https://pulse.mk.co.kr/news/english/12068307",
    },
    "src_koreatimes_lg_ai_data_center_ess_20260318": {
        "url": "https://www.koreatimes.co.kr/business/tech-science/20260318/lg-bets-on-ai-data-center-ess-as-future-growth-driver",
        "publisher": "The Korea Times",
        "title": "LG bets on AI data center, ESS as future growth driver",
        "published": "2026-03-18",
        "used_for": "LG그룹의 AI 데이터센터·ESS·AI Box·CDU 사업 연결",
    },
    "src_lgcns_data_center": {
        "url": "https://www.lgcns.com/kr/newsroom/press/detail.aidc-2603-2",
        "publisher": "LG CNS",
        "title": "LG CNS AI Box and Data Center Business",
        "published": "2026-03-04",
        "used_for": "LG CNS의 AI 데이터센터 설계·구축·운영과 모듈러 AI Box 역량",
    },
    "src_goldman_data_center_power_20260520": {
        "url": "https://www.goldmansachs.com/insights/articles/AI-poised-to-drive-160-increase-in-power-demand",
        "publisher": "Goldman Sachs",
        "title": "AI is poised to drive 160% increase in data center power demand",
        "published": "2024-05-14",
        "used_for": "AI 확산에 따른 데이터센터 전력 수요와 전력망 투자 증가 전망",
    },
    "src_wef_global_lighthouse_20260115": {
        "url": "https://www.weforum.org/projects/global-lighthouse-network/",
        "publisher": "World Economic Forum",
        "title": "Global Lighthouse Network",
        "published": "unknown",
        "used_for": "제조 현장의 디지털 전환·AI 적용을 검증하는 Global Lighthouse Network benchmark",
    },
}

LEGACY_SOURCE_LINKS = {
    "2022-03-31_lg-corp_smart-park-lighthouse-factory": "src_lgcorp_smart_park_lighthouse_20220331",
    "2022-04-27_lg-smart-park_lighthouse-factory": "src_lg_smart_park_lighthouse_20220427",
    "2024-12-23_lg-energy-solution_qualcomm-bms": "src_lgensol_qualcomm_bms_20241223",
    "2025-03-23_lg-household-health-care_ai-cosmetic-ingredients": "src_lghnh_ai_cosmetic_ingredients_20250323",
    "2025-06-13_lg-energy-solution_genai-battery": "src_lgensol_genai_battery_20250613",
    "2025-06-16_lg-cns_skild-ai": "src_lgcns_skild_ai_20250616",
    "2025-06-20_lg-energy-solution_battery-technology-roadmap": "src_lgensol_battery_technology_roadmap_20250620",
    "2025-08-05_lg-display_ai-productivity": "src_lgdisplay_ai_productivity_20250805",
    "2025-09-25_ifr_world-robotics-industrial-robots": "src_ifr_world_robotics_20250925",
    "2025-12-17_lg-electronics_ai-in-vehicle-solutions": "src_lge_ai_in_vehicle_20251217",
    "2026-01-05_lg-display_ces2026-oled-automotive": "src_lgdisplay_ces2026_20260105",
    "2026-01-06_lg-innotek_ces2026-aidv": "src_lginnotek_ces2026_aidv_20260106",
    "2026-01-08_lg-electronics_profit-driven-growth-ax": "src_lge_strategy_ax_20260108",
    "2026-01-15_wef_global-lighthouse-network": "src_wef_global_lighthouse_20260115",
    "2026-02-03_lg-ai-research_exaone-discovery-patent": "src_lgai_exaone_discovery_patent_20260203",
    "2026-03-04_lg-cns_ai-box": "src_lgcns_ai_box_20260304",
    "2026-03-12_lg-cns_palantir-partnership": "src_lgcns_palantir_20260312",
    "2026-03-18_korea-times_lg-ai-data-center-ess": "src_koreatimes_lg_ai_data_center_ess_20260318",
    "2026-04-03_lg-energy-solution_sdverse": "src_lgensol_sdverse_20260403",
    "2026-04-07_lg-corp_silicon-valley-ai-transformation": "src_lgcorp_silicon_valley_20260407",
    "2026-04-09_exaone-4-5-technical-report": "src_exaone45_technical_report_20260409",
    "2026-04-13_lg-energy-solution_ax-productivity": "src_lgensol_ax_productivity_20260413",
    "2026-04-14_lg-electronics_smart-factory-success": "src_lge_smart_factory_20260414",
    "2026-04-15_lg-energy-solution_ess-expansion": "src_lgensol_ess_expansion_20260415",
    "2026-04-21_lg-electronics_data-center-world-2026": "src_lge_dcw_20260421",
    "2026-05-08_arxiv_ai-ml-smart-manufacturing-roadmap": "src_ai_ml_smart_manufacturing_roadmap_202605",
    "2026-05-19_lg-cns_factova-manufacturing-ax": "src_lgcns_factova_20260519",
    "2026-05-27_lg-cns_ax-fair": "src_lgcns_ax_fair_20260527",
    "2026-05-28_lg-chem_one-person-one-agent": "src_lgchem_one_agent_20260528",
    "2026-06-07_lguplus_paju-aidc": "src_lguplus_paju_aidc_20260607",
    "2026-06-07_nvidia-lg-ai-factory": "src_nvidia_lg_ai_factory_20260607",
    "2026-06-08_lg-nvidia-map": "src_lg_nvidia_map_20260608",
    "2026-06-08_lguplus_200mw-aidc": "src_pulse_lguplus_paju_aidc_20260608",
    "2026-06-17_lg-ai-research_dd-pharmatech": "src_lgai_dd_pharmatech_20260617",
    "exaone-4-5-technical-report": "src_exaone45_technical_report_20260409",
    "lg-ai-research_exaone": "src_lgai_exaone",
    "lg-ai-research_materials-intelligence": "src_lgai_materials_intelligence",
    "lg-chem_cathode-material": "src_lgchem_cathode_material",
    "lg-chem_life-science": "src_lgchem_life_science",
    "lg-chem_open-innovation": "src_lgchem_open_innovation",
    "lg-cns_ax-consulting": "src_lgcns_ax_consulting",
    "lg-cns_ax-platform": "src_lgcns_ax_platform",
    "lg-cns_data-center": "src_lgcns_data_center",
    "lg-energy-solution_baround": "src_lgensol_baround",
    "lg-innotek_ces2026-showcase": "src_lginnotek_ces2026_showcase",
    "lg-uplus_autonomous-driving": "src_lguplus_autonomous_driving",
}


def repair_yaml(raw: str) -> dict:
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


def parse_entity(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, raw, body = text.split("---", 2)
    return repair_yaml(raw), body


def normalize_url(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip().rstrip(".,")
    parsed = urlparse(url)
    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
    ]
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", urlencode(query), ""))


def domain_publisher(url: str | None) -> str:
    if not url:
        return "unknown"
    host = urlparse(url).netloc.lower().removeprefix("www.")
    for domain, publisher in PUBLISHERS.items():
        if host == domain or host.endswith("." + domain):
            return publisher
    return host or "unknown"


def title_from_url(url: str | None, source_id: str) -> str:
    if not url:
        return source_id.removeprefix("src_").replace("_", " ").replace("-", " ").title()
    path = Path(urlparse(url).path).name
    if path and path not in {"", "index.html"}:
        text = re.sub(r"\.(html?|php|aspx?)$", "", path, flags=re.I)
        text = re.sub(r"[-_]+", " ", text).strip()
        if text and not text.isdigit():
            return text[:1].upper() + text[1:]
    return source_id.removeprefix("src_").replace("_", " ").replace("-", " ").title()


def parse_source_notes() -> dict[str, dict]:
    records: dict[str, dict] = {}
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
                record = records.setdefault(source_id, {"notes_from": [], "images": []})
                record["notes_from"].append(path.relative_to(ROOT).as_posix())
                lines = block.splitlines()
                in_key_facts = False
                for line in lines:
                    field = field_pattern.match(line.strip())
                    if not field:
                        nested_fact = re.match(r"^\s{2,}-\s+(.+)$", line)
                        if in_key_facts and nested_fact:
                            record.setdefault("key_facts", []).append(nested_fact.group(1).strip())
                        continue
                    key = field.group(1).strip().lower().replace(" ", "_")
                    value = field.group(2).strip()
                    in_key_facts = key == "key_facts"
                    if key == "image":
                        record["images"].extend(re.findall(r"`([^`]+)`", value) or [value])
                    elif key == "key_facts":
                        if value:
                            record.setdefault("key_facts", []).append(value)
                    elif value and not record.get(key):
                        record[key] = value

    table_pattern = re.compile(
        r"^\|\s*(src_[a-zA-Z0-9_-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
        re.MULTILINE,
    )
    for path in sorted((ROOT / "docs").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for source_id, title, publisher, usage in table_pattern.findall(text):
            if title.strip().lower() in {"제목", "---"}:
                continue
            record = records.setdefault(source_id, {"notes_from": [], "images": []})
            record.setdefault("title", title.strip())
            record.setdefault("publisher", publisher.strip())
            record.setdefault("used_for", usage.strip())
            if path.relative_to(ROOT).as_posix() not in record["notes_from"]:
                record["notes_from"].append(path.relative_to(ROOT).as_posix())
    return records


def entity_source_usage() -> tuple[dict[str, list[dict]], set[str]]:
    usage = defaultdict(list)
    ids = set()
    for folder in ("docs", "topics", "concepts", "companies"):
        for path in sorted((ROOT / folder).rglob("*.md")):
            metadata, _ = parse_entity(path)
            text = path.read_text(encoding="utf-8")
            linked_source_ids = re.findall(r"\[\[sources/(src_[^\]|]+)", text)
            entity_source_ids = list(
                dict.fromkeys((metadata.get("source_ids") or []) + linked_source_ids)
            )
            for source_id in entity_source_ids:
                ids.add(source_id)
                entity = {
                    "path": path.relative_to(ROOT).as_posix(),
                    "type": metadata.get("type") or folder.rstrip("s"),
                    "title": metadata.get("title") or path.stem,
                    "entity_id": metadata.get("id"),
                    "themes": metadata.get("related_themes")
                    or ([metadata.get("theme_id")] if metadata.get("theme_id") else []),
                    "concepts": metadata.get("related_concepts") or [],
                    "companies": metadata.get("related_companies") or [],
                }
                if not any(item["path"] == entity["path"] for item in usage[source_id]):
                    usage[source_id].append(entity)
    return usage, ids


def url_registry_from_markdown() -> dict[str, list[str]]:
    registry = defaultdict(list)
    for folder in ("docs", "topics"):
        for path in sorted((ROOT / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for url in re.findall(r"https?://[^\s)>|]+", text):
                normalized = normalize_url(url)
                if normalized and path.relative_to(ROOT).as_posix() not in registry[normalized]:
                    registry[normalized].append(path.relative_to(ROOT).as_posix())
    return registry


def image_matches(record: dict, inventory: dict) -> list[dict]:
    images = []
    wanted_ids = set(record.get("images") or [])
    source_url = normalize_url(record.get("url"))
    for item in inventory["images"]:
        id_match = item.get("image_id") in wanted_ids or bool(wanted_ids.intersection(item.get("aliases") or []))
        url_match = source_url and normalize_url(item.get("source_url")) == source_url
        if id_match or url_match:
            images.append(item)
    return images


def unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def main() -> int:
    standard_sources = [
        path
        for path in SOURCES_DIR.glob("*.md")
        if "## 4. Atomic Claims" in path.read_text(encoding="utf-8")
    ]
    if standard_sources:
        print(
            f"Skipped legacy Source generation: {len(standard_sources)} ingestion-standard "
            "Source cards already exist. Use migrate_sources_to_ingestion_standard.py."
        )
        return 0

    notes = parse_source_notes()
    usage, source_ids = entity_source_usage()
    source_ids.update(notes)
    source_ids.update(SOURCE_OVERRIDES)
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    url_registry = url_registry_from_markdown()
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    url_to_ids = defaultdict(list)
    pending_used_by = defaultdict(list)
    for source_id in sorted(source_ids):
        existing_path = SOURCES_DIR / f"{source_id}.md"
        if existing_path.exists() and "## 4. Atomic Claims" in existing_path.read_text(encoding="utf-8"):
            continue
        record = notes.get(source_id, {"notes_from": [], "images": []})
        record = {**record, **SOURCE_OVERRIDES.get(source_id, {})}
        url = record.get("url")
        normalized_url = normalize_url(url)
        if normalized_url:
            url_to_ids[normalized_url].append(source_id)
        used = usage.get(source_id, [])
        themes = unique([theme for entity in used for theme in entity["themes"]])
        topics = unique(
            [
                entity.get("entity_id")
                for entity in used
                if entity["path"].startswith("topics/") and entity.get("entity_id")
            ]
        )
        concepts = unique([Path(entity["path"]).stem for entity in used if entity["path"].startswith("concepts/")])
        companies = unique(
            [
                Path(entity["path"]).stem
                for entity in used
                if entity["path"].startswith("companies/")
            ]
        )
        publisher = record.get("publisher") or domain_publisher(url)
        published = record.get("published") or "unknown"
        title = record.get("title") or title_from_url(url, source_id)
        key_facts = record.get("key_facts") or []
        used_for = record.get("used_for") or (
            " ".join(key_facts[:2])
            if key_facts
            else "Entity metadata에서 관련 근거로 연결됨. 원문 요약 보강 필요."
        )
        matched_images = image_matches(record, inventory)
        source_path = f"sources/{source_id}.md"
        for image in matched_images:
            pending_used_by[image["image_id"]].append(source_path)

        frontmatter = {
            "id": source_id,
            "type": "source",
            "title": title,
            "publisher": publisher,
            "published": published,
            "url": url or "unknown",
            "related_themes": themes,
            "related_topics": topics,
            "related_concepts": concepts,
            "related_companies": companies,
            "tags": ["source", re.sub(r"[^a-z0-9]+", "-", publisher.lower()).strip("-") or "unknown"],
        }
        used_rows = [
            f"| [[{entity['path'][:-3]}|{entity['title']}]] | {used_for} |"
            for entity in used
        ] or ["| 연결 Entity 없음 | Source Note 기반으로만 생성됨 |"]
        image_rows = []
        for image in matched_images:
            image_rows.append(
                "| {image_id} | {original_url} | {local_path} | {status} | {used_by} | {note} |".format(
                    image_id=image.get("image_id", ""),
                    original_url=image.get("original_url", ""),
                    local_path=image.get("local_path") or "",
                    status=image.get("status", ""),
                    used_by=", ".join(sorted(set((image.get("used_by") or []) + [source_path]))),
                    note=image.get("caption") or image.get("error") or "",
                )
            )
        if not image_rows:
            image_rows = ["| 없음 |  |  | not_linked |  | 원문 이미지 연결 정보 없음 |"]
        key_facts = key_facts or [
            item.strip() for item in re.split(r"[;,]", used_for) if item.strip()
        ]
        if not key_facts:
            key_facts = ["원문 사실관계 요약 보강 필요"]
        fact_lines = "\n".join(f"- {fact}" for fact in key_facts)
        duplicate_note = ""
        reliability = (
            "공식 기업·기관·연구 원문 또는 원문에 가까운 자료다. 전략적 해석은 Source Card가 아니라 docs/topics에서 관리한다."
            if publisher not in {"unknown"} and url
            else "URL 또는 publisher metadata가 부족하다. 원문 확인 및 Source 보강 필요."
        )
        if not url:
            reliability += " 현재 source_id는 Entity에서 사용되지만 URL을 Source Notes에서 찾지 못했다."
        markdown = f"""---
{yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False, width=1000).strip()}
---

# {title}

## 1. Source Summary

{used_for}

## 2. Key Facts

{fact_lines}

## 3. Used In

| Entity | Usage |
|---|---|
{chr(10).join(used_rows)}

## 4. Image Notes

| image_id | original_url | local_path | status | used_by | note |
|---|---|---|---|---|---|
{chr(10).join(image_rows)}

## 5. Reliability Notes

{reliability}
{duplicate_note}
"""
        (SOURCES_DIR / f"{source_id}.md").write_text(markdown, encoding="utf-8")
        generated.append(
            {
                "id": source_id,
                "title": title,
                "publisher": publisher,
                "published": published,
                "url": url,
                "normalized_url": normalized_url,
                "related_themes": themes,
                "related_topics": topics,
                "related_concepts": concepts,
                "related_companies": companies,
                "used_by": [entity["path"] for entity in used],
                "image_ids": [image["image_id"] for image in matched_images],
                "path": source_path,
                "status": "complete_metadata" if url and publisher != "unknown" else "needs_metadata",
            }
        )

    duplicate_groups = {
        url: ids for url, ids in url_to_ids.items() if len(ids) > 1
    }
    for item in generated:
        if item["normalized_url"] in duplicate_groups:
            item["duplicate_source_ids"] = [
                source_id
                for source_id in duplicate_groups[item["normalized_url"]]
                if source_id != item["id"]
            ]
        else:
            item["duplicate_source_ids"] = []

    for item in inventory["images"]:
        additions = pending_used_by.get(item.get("image_id"), [])
        if additions:
            item["used_by"] = sorted(set((item.get("used_by") or []) + additions))
    INVENTORY_PATH.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "data" / "sources.json").write_text(
        json.dumps({"sources": generated, "duplicate_url_groups": duplicate_groups}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    coverage = [
        "---",
        "id: source_coverage",
        "type: index",
        "title: Source Coverage",
        "---",
        "",
        "# Source Coverage",
        "",
        f"총 {len(generated)}개 source_id의 metadata와 사용 범위를 정리한다.",
        "",
        "| Source | Publisher | Published | Used By | Images | Status |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in generated:
        coverage.append(
            f"| [[sources/{item['id']}|{item['title']}]] | {item['publisher']} | "
            f"{item['published']} | {len(item['used_by'])} | {len(item['image_ids'])} | "
            f"`{item['status']}` |"
        )
    coverage.extend(
        [
            "",
            "## Duplicate URL Groups",
            "",
            "동일 URL에 복수 source_id가 연결된 경우다. 기존 Entity ID 호환성을 위해 자동 병합하지 않았다.",
            "",
        ]
    )
    if duplicate_groups:
        for url, ids in duplicate_groups.items():
            coverage.append(f"- {url}: " + ", ".join(f"`{source_id}`" for source_id in ids))
    else:
        coverage.append("- 없음")
    (ROOT / "docs" / "83_source_coverage.md").write_text("\n".join(coverage) + "\n", encoding="utf-8")

    rewritten_links = 0
    for folder in ("docs", "topics", "concepts", "companies"):
        for path in sorted((ROOT / folder).rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            updated = text
            for legacy, canonical in LEGACY_SOURCE_LINKS.items():
                updated, count = re.subn(
                    rf"(\[\[sources/){re.escape(legacy)}(?=(?:\||\]\]))",
                    rf"\g<1>{canonical}",
                    updated,
                )
                rewritten_links += count
            if updated != text:
                path.write_text(updated, encoding="utf-8")

    print(
        json.dumps(
            {
                "sources": len(generated),
                "complete_metadata": sum(item["status"] == "complete_metadata" for item in generated),
                "needs_metadata": sum(item["status"] == "needs_metadata" for item in generated),
                "sources_with_images": sum(bool(item["image_ids"]) for item in generated),
                "duplicate_url_groups": len(duplicate_groups),
                "markdown_urls_indexed": len(url_registry),
                "legacy_links_rewritten": rewritten_links,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
