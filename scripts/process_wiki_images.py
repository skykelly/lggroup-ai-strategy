#!/usr/bin/env python3
"""Download declared Wiki images, update Markdown image references, and build inventory."""

from __future__ import annotations

import ast
import concurrent.futures
import hashlib
import json
import mimetypes
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
IMAGES_DIR = ROOT / "assets" / "images"
INVENTORY_PATH = ROOT / "data" / "image_inventory.json"

SCRIPT_TARGETS = OrderedDict(
    [
        ("download_ai_data_center_infra_images.py", "docs/01_ai_data_center_infra.md"),
        ("download_physical_ai_smart_manufacturing_images.py", "docs/02_physical_ai_smart_manufacturing.md"),
        ("download_ai_mobility_sdv_aidv_images.py", "docs/03_ai_mobility_sdv_aidv.md"),
        ("download_enterprise_ax_agentic_operating_model_images.py", "docs/04_enterprise_ax_agentic_operating_model.md"),
        ("download_ai_for_science_bio_materials_battery_images.py", "docs/05_ai_for_science_bio_materials_battery.md"),
        ("download_global_ai_alliance_open_innovation_images.py", "docs/06_global_ai_alliance_open_innovation.md"),
    ]
)

DISCOVERED_IMAGE_DECLARATIONS = [
    {
        "image_id": "doc_02_skild_ai_series_c",
        "original_url": "https://cdn.wowtale.net/wp-content/uploads/2026/01/skild-ai-series-c-800x329.jpg",
        "source_url": None,
        "source": "Markdown image reference",
        "caption": "Skild AI 소개.",
        "declared_status": "discovered_in_markdown",
        "filename": "doc_02_skild-ai-series-c-800x329.jpg",
        "used_by": "docs/02_physical_ai_smart_manufacturing.md",
        "script": "scripts/process_wiki_images.py",
    },
    {
        "image_id": "doc_04_asiae_enterprise_ax",
        "original_url": "https://www.asiae.co.kr/news/img_view.htm?img=2026040709445416262_1775522694.jpg",
        "source_url": None,
        "source": "Markdown image reference",
        "caption": None,
        "declared_status": "discovered_in_markdown",
        "filename": "doc_04_2026040709445416262_1775522694.jpg",
        "used_by": "docs/04_enterprise_ax_agentic_operating_model.md",
        "script": "scripts/process_wiki_images.py",
    },
]


def topic_target(number: int) -> str:
    matches = sorted((ROOT / "topics").glob(f"{number:02d}_*.md"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Topic {number:02d} document, found {len(matches)}")
    return matches[0].relative_to(ROOT).as_posix()


def literal_assignment(path: Path, names: tuple[str, ...]) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        target_name = None
        value = None
        if isinstance(node, ast.Assign):
            value = node.value
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    target_name = target.id
                    break
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id in names:
                target_name = node.target.id
                value = node.value
        if target_name and value is not None:
            return target_name, ast.literal_eval(value)
    raise RuntimeError(f"No {names} literal found in {path}")


def extension_from_url(url: str) -> str:
    suffix = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg"}:
        return suffix
    return ".img"


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._") or "image"


def load_declarations() -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    targets = OrderedDict(SCRIPT_TARGETS)
    for number in range(1, 19):
        targets[f"download_topic_{number:02d}_images.py"] = topic_target(number)

    for script_name, used_by in targets.items():
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            raise FileNotFoundError(script_path)
        variable, value = literal_assignment(script_path, ("IMAGE_ASSETS", "MANIFEST"))
        items = value if variable == "IMAGE_ASSETS" else value.get("images", [])
        for index, item in enumerate(items, start=1):
            original_url = item.get("image_url") or item.get("url")
            image_id = item.get("image_id") or item.get("id") or f"{script_path.stem}_{index}"
            filename = item.get("filename")
            if not filename:
                filename = f"{safe_name(image_id)}{extension_from_url(original_url)}"
            declarations.append(
                {
                    "image_id": image_id,
                    "original_url": original_url,
                    "source_url": item.get("source_url"),
                    "source": item.get("source"),
                    "caption": item.get("caption") or item.get("description"),
                    "declared_status": item.get("status"),
                    "filename": safe_name(filename),
                    "used_by": used_by,
                    "script": f"scripts/{script_name}",
                }
            )

    declarations.extend(dict(item) for item in DISCOVERED_IMAGE_DECLARATIONS)
    declared_urls = {
        item["original_url"]
        for item in declarations
        if item["original_url"] and item["original_url"] != "IMAGE_URL_NEEDED"
    }
    for folder in ("docs", "topics"):
        for markdown_path in sorted((ROOT / folder).glob("*.md")):
            text = markdown_path.read_text(encoding="utf-8")
            for match in re.finditer(r'<img\b[^>]*\bsrc=["\'](https?://[^"\']+)["\']', text):
                original_url = match.group(1)
                if original_url in declared_urls:
                    continue
                basename = Path(urllib.parse.unquote(urllib.parse.urlparse(original_url).path)).name
                if not basename:
                    basename = hashlib.sha256(original_url.encode("utf-8")).hexdigest()[:16] + ".img"
                prefix = markdown_path.stem.split("_", 1)[0]
                filename = safe_name(f"{folder.rstrip('s')}_{prefix}_{basename}")
                declarations.append(
                    {
                        "image_id": f"undeclared_{markdown_path.stem}_{len(declarations) + 1}",
                        "original_url": original_url,
                        "source_url": None,
                        "source": "Markdown image reference",
                        "caption": None,
                        "declared_status": "discovered_in_markdown",
                        "filename": filename,
                        "used_by": markdown_path.relative_to(ROOT).as_posix(),
                        "script": None,
                    }
                )
                declared_urls.add(original_url)
    return declarations


def unique_filename(preferred: str, url: str, claimed: dict[str, str]) -> str:
    candidate = preferred
    owner = claimed.get(candidate)
    if owner is None or owner == url:
        claimed[candidate] = url
        return candidate
    path = Path(candidate)
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]
    candidate = f"{path.stem}_{digest}{path.suffix}"
    claimed[candidate] = url
    return candidate


def looks_like_image(data: bytes, content_type: str) -> bool:
    lowered = content_type.lower()
    if lowered.startswith("image/"):
        return True
    if data.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"GIF87a", b"GIF89a", b"RIFF")):
        return True
    if len(data) > 12 and data[4:12] in {b"ftypavif", b"ftypavis"}:
        return True
    return data.lstrip().startswith(b"<svg")


def download(entry: dict[str, Any], retries: int = 2, timeout: int = 25) -> dict[str, Any]:
    url = entry["original_url"]
    destination = IMAGES_DIR / entry["filename"]
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    if entry.get("source_url"):
        headers["Referer"] = entry["source_url"]

    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "")
            if not data:
                raise ValueError("empty response")
            if not looks_like_image(data, content_type):
                raise ValueError(f"non-image response: {content_type or 'unknown content type'}")
            destination.write_bytes(data)
            return {
                **entry,
                "local_path": f"assets/images/{entry['filename']}",
                "status": "downloaded",
                "error": None,
                "content_type": content_type or mimetypes.guess_type(destination.name)[0],
                "bytes": len(data),
            }
        except Exception as exc:  # noqa: BLE001
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < retries:
                time.sleep(attempt)
    return {
        **entry,
        "local_path": None,
        "status": "failed",
        "error": last_error,
        "content_type": None,
        "bytes": 0,
    }


def consolidate(declarations: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_url: OrderedDict[str, dict[str, Any]] = OrderedDict()
    needed: list[dict[str, Any]] = []
    claimed: dict[str, str] = {}
    for item in declarations:
        if item["original_url"] == "IMAGE_URL_NEEDED":
            needed.append(
                {
                    **item,
                    "local_path": None,
                    "status": "image_url_needed",
                    "error": "IMAGE_URL_NEEDED",
                    "used_by": [item["used_by"]],
                }
            )
            continue
        existing = by_url.get(item["original_url"])
        if existing:
            existing["used_by"].append(item["used_by"])
            existing["aliases"].append(item["image_id"])
            if item["script"]:
                existing["scripts"].append(item["script"])
            continue
        filename = unique_filename(item["filename"], item["original_url"], claimed)
        by_url[item["original_url"]] = {
            **item,
            "filename": filename,
            "used_by": [item["used_by"]],
            "aliases": [],
            "scripts": [item["script"]] if item["script"] else [],
        }
    for entry in by_url.values():
        entry["used_by"] = sorted(set(entry["used_by"]))
        entry["aliases"] = sorted(set(entry["aliases"]))
        entry["scripts"] = sorted(set(entry["scripts"]))
    return list(by_url.values()), needed


def replace_markdown_images(results: list[dict[str, Any]]) -> dict[str, int]:
    replacements = {
        item["original_url"]: item["local_path"]
        for item in results
        if item["status"] == "downloaded" and item["local_path"]
    }
    changed: dict[str, int] = {}
    for folder in ("docs", "topics"):
        for path in sorted((ROOT / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            updated = text
            count = 0
            for original_url, local_path in replacements.items():
                escaped = re.escape(original_url)
                patterns = (
                    (rf'(<img\b[^>]*\bsrc=["\']){escaped}(["\'])', rf"\g<1>{local_path}\g<2>"),
                    (rf"(!\[[^\]]*\]\(){escaped}(\))", rf"\g<1>{local_path}\g<2>"),
                )
                for pattern, replacement in patterns:
                    updated, matches = re.subn(pattern, replacement, updated)
                    count += matches
            if updated != text:
                path.write_text(updated, encoding="utf-8")
                changed[path.relative_to(ROOT).as_posix()] = count
    return changed


def markdown_image_state() -> dict[str, int]:
    local_references = 0
    remote_references = 0
    image_url_needed = 0
    for folder in ("docs", "topics"):
        for path in sorted((ROOT / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            local_references += len(
                re.findall(r'<img\b[^>]*\bsrc=["\']assets/images/[^"\']+["\']', text)
            )
            remote_references += len(
                re.findall(r'<img\b[^>]*\bsrc=["\']https?://[^"\']+["\']', text)
            )
            image_url_needed += text.count("IMAGE_URL_NEEDED")
    return {
        "local_image_references": local_references,
        "remote_image_references": remote_references,
        "image_url_needed_occurrences": image_url_needed,
    }


def main() -> int:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    declarations = load_declarations()
    download_entries, needed = consolidate(declarations)
    print(
        f"Loaded {len(declarations)} declarations: "
        f"{len(download_entries)} unique URLs, {len(needed)} IMAGE_URL_NEEDED"
    )

    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download, entry): entry for entry in download_entries}
        for completed, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(f"[{completed}/{len(futures)}] {result['status']}: {result['image_id']}")

    order = {entry["original_url"]: index for index, entry in enumerate(download_entries)}
    results.sort(key=lambda item: order[item["original_url"]])
    changed = replace_markdown_images(results)
    markdown_state = markdown_image_state()
    inventory = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "summary": {
            "declarations": len(declarations),
            "unique_remote_urls": len(download_entries),
            "downloaded": sum(item["status"] == "downloaded" for item in results),
            "failed": sum(item["status"] == "failed" for item in results),
            "image_url_needed": len(needed),
            "markdown_files_updated": len(changed),
            "markdown_references_updated": sum(changed.values()),
            **markdown_state,
        },
        "markdown_updates": changed,
        "images": results + needed,
    }
    INVENTORY_PATH.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(inventory["summary"], ensure_ascii=False, indent=2))
    print(f"Inventory: {INVENTORY_PATH.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
