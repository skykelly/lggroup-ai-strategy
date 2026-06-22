#!/usr/bin/env python3
"""
Download original source images for:
topics/09_is_lg_ai_alliance_an_option_strategy_or_dependency_risk.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_09_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_is_lg_ai_alliance_an_option_strategy_or_dependency_risk",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lg_nvidia_map_koo_huang",
      "source": "PRNewswire / LG",
      "source_url": "https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html",
      "image_url": "https://mma.prnewswire.com/media/2995864/1.jpg?w=500",
      "filename": "topic_09_lg_nvidia_map_koo_huang.jpg",
      "caption": "NVIDIA와의 M.A.P. 협력은 LG의 글로벌 AI Alliance를 상징하는 대표 사례다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgcns_palantir_signing",
      "source": "Digital Today / LG CNS",
      "source_url": "https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion",
      "image_url": "https://cdn.digitaltoday.co.kr/news/photo/202603/640006_590746_75.jpg",
      "filename": "topic_09_lgcns_palantir_signing.jpg",
      "caption": "LG CNS–Palantir 파트너십은 enterprise AI와 ontology 기반 AX 확장의 사례다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgcns_skild_ai_hq",
      "source": "LG CNS Newsroom",
      "source_url": "https://www.lgcns.com/kr/newsroom/press/detail.66074",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/MAIN-scaled-e1749113375930-1920x1436.jpg",
      "filename": "topic_09_lgcns_skild_ai_hq.jpg",
      "caption": "LG CNS와 Skild AI의 협력은 Physical AI와 industrial humanoid robot solution 확장의 사례다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgai_exaone_journey",
      "source": "LG AI Research",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_journey_pc.png",
      "filename": "topic_09_lgai_exaone_journey.png",
      "caption": "EXAONE은 외부 모델·플랫폼과 병행해 LG가 내부적으로 통제할 수 있는 AI layer다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_sdverse_image_needed",
      "source": "LG Energy Solution",
      "source_url": "https://www.lgensol.com/mobile/en/company/newsroom-detail?seq=8753",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_09_lgensol_sdverse.jpg",
      "caption": "LG에너지솔루션의 SDVerse 참여는 외부 software marketplace를 활용해 배터리 SW를 확장하는 사례다. 원문 이미지 URL은 별도 확보 필요.",
      "status": "image_url_needed"
    }
  ]
}


def get_referer(url: str, source_url: str | None = None) -> str:
    if source_url:
        return source_url
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}/"
    return "https://www.google.com/"


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    idx = 2

    while True:
        candidate = parent / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def download_file(item: dict, out_dir: Path, timeout: int = 30) -> dict:
    url = item["image_url"]

    if url == "IMAGE_URL_NEEDED":
        return {
            "ok": False,
            "skipped": True,
            "image_id": item["image_id"],
            "source": item["source"],
            "source_url": item["source_url"],
            "original_url": url,
            "local_path": None,
            "filename": item["filename"],
            "bytes": 0,
            "content_type": None,
            "status": "image_url_needed",
            "caption": item["caption"],
            "used_by": ["topics/09_is_lg_ai_alliance_an_option_strategy_or_dependency_risk.md"],
            "error": "IMAGE_URL_NEEDED",
        }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Referer": get_referer(url, item.get("source_url")),
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    req = urllib.request.Request(url, headers=headers)
    intended_path = out_dir / item["filename"]
    dest = ensure_unique_path(intended_path)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read()

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

        return {
            "ok": True,
            "skipped": False,
            "image_id": item["image_id"],
            "source": item["source"],
            "source_url": item["source_url"],
            "original_url": url,
            "local_path": str(dest),
            "filename": dest.name,
            "bytes": len(data),
            "content_type": content_type,
            "status": item["status"],
            "caption": item["caption"],
            "used_by": ["topics/09_is_lg_ai_alliance_an_option_strategy_or_dependency_risk.md"],
            "error": None,
        }

    except Exception as exc:
        return {
            "ok": False,
            "skipped": False,
            "image_id": item["image_id"],
            "source": item["source"],
            "source_url": item["source_url"],
            "original_url": url,
            "local_path": None,
            "filename": item["filename"],
            "bytes": 0,
            "content_type": None,
            "status": "download_failed_keep_remote_url",
            "caption": item["caption"],
            "used_by": ["topics/09_is_lg_ai_alliance_an_option_strategy_or_dependency_risk.md"],
            "error": repr(exc),
        }


def main() -> None:
    out_dir = Path(MANIFEST["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for item in MANIFEST["images"]:
        print(f"Processing {item['image_id']}")
        results.append(download_file(item, out_dir))
        if item["image_url"] != "IMAGE_URL_NEEDED":
            time.sleep(0.5)

    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "topic_09_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_09.json"

    manifest_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    inventory_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok_count = sum(1 for r in results if r["ok"])
    skipped_count = sum(1 for r in results if r.get("skipped"))
    fail_count = len(results) - ok_count - skipped_count

    print(f"Done. ok={ok_count}, failed={fail_count}, skipped={skipped_count}")
    print(f"Manifest: {manifest_path}")
    print(f"Inventory fragment: {inventory_path}")

    if fail_count:
        print("\nFailed downloads; keep remote URLs in Markdown:")
        for r in results:
            if not r["ok"] and not r.get("skipped"):
                print(f"- {r['image_id']}: {r['error']}")


if __name__ == "__main__":
    main()
