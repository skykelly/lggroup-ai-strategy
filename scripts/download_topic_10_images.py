#!/usr/bin/env python3
"""
Download original source images for:
topics/10_can_ai_for_science_change_lg_rnd_productivity.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_10_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_can_ai_for_science_change_lg_rnd_productivity",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lgai_exaone_journey",
      "source": "LG AI Research",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_journey_pc.png",
      "filename": "topic_10_lgai_exaone_journey.png",
      "caption": "EXAONE은 범용 대화형 AI를 넘어 산업·과학 영역의 문제 해결로 확장되고 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgai_exaone_logo",
      "source": "LG AI Research",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_logo.png",
      "filename": "topic_10_lgai_exaone_logo.png",
      "caption": "LG AI Research의 EXAONE은 AI for Science의 기반 모델·솔루션 레이어로 해석할 수 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgai_dd_pharmatech_image_needed",
      "source": "PRNewswire / LG AI Research",
      "source_url": "https://www.prnewswire.com/news-releases/lg-ai-research-announces-collaboration-with-dd-pharmatech-to-accelerate-next-generation-oral-peptide-drug-discovery-302802738.html",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_10_lgai_dd_pharmatech.jpg",
      "caption": "LG AI Research와 D&D Pharmatech의 차세대 oral peptide drug discovery 협력. 원문 페이지의 직접 이미지 URL은 별도 확보 필요.",
      "status": "image_url_needed"
    },
    {
      "image_id": "lgensol_genai_battery_industry",
      "source": "LG Energy Solution Battery Inside",
      "source_url": "https://inside.lgensol.com/en/2025/06/genai-transforming-the-present-and-future-of-the-battery-industry/",
      "image_url": "https://inside.lgensol.com/wp-content/uploads/2025/05/9_%EC%83%9D%EC%84%B1%ED%98%95-AI%EB%A1%9C-%EB%B0%94%EA%BE%B8%EB%8A%94-%EB%B0%B0%ED%84%B0%EB%A6%AC-%EC%82%B0%EC%97%85%EC%9D%98-%ED%98%84%EC%9E%AC%EC%99%80-%EB%AF%B8%EB%9E%98-1.png",
      "filename": "topic_10_lgensol_genai_battery_industry.png",
      "caption": "LG에너지솔루션은 GenAI를 배터리 설계, 지식관리, 특허 검색에 적용하는 사례를 소개했다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgchem_life_science_graph",
      "source": "LG Chem",
      "source_url": "https://www.lgchem.com/company/information-center/business/life-sciences",
      "image_url": "https://www.lgchem.com/asset/images/common/company/img_life_science_graph.png",
      "filename": "topic_10_lgchem_life_science_graph.png",
      "caption": "LG Chem Life Sciences는 AI for Science가 신약·바이오 R&D 생산성과 연결될 수 있는 사업 영역이다.",
      "status": "confirmed"
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
            "used_by": ["topics/10_can_ai_for_science_change_lg_rnd_productivity.md"],
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
            "used_by": ["topics/10_can_ai_for_science_change_lg_rnd_productivity.md"],
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
            "used_by": ["topics/10_can_ai_for_science_change_lg_rnd_productivity.md"],
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

    manifest_path = out_dir / "topic_10_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_10.json"

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
