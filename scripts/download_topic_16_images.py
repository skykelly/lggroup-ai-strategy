#!/usr/bin/env python3
"""
Download original source images for:
topics/16_how_does_manufacturing_data_become_an_ai_product.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_16_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_how_does_manufacturing_data_become_an_ai_product",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lge_smart_factory_main",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/business/insights/smart-factory/news/lg-acclerates-smart-factory-solutions-business-integrating-ai-with-66-year-manufacturing-expertise/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/main-image-desktopmobile-ecsmart-464.png",
      "filename": "topic_16_lge_smart_factory_main.png",
      "caption": "LG전자의 스마트팩토리 자산은 제조 데이터가 AI 제품으로 바뀔 수 있는 출발점이다.",
      "status": "confirmed"
    },
    {
      "image_id": "lg_smart_park_lighthouse",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/home-appliance-solution/lg-smart-park-named-lighthouse-factory-for-futuristic-manufacturing-technology/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/home-appliance-solution/lg-smart-park-named-lighthouse-factory-for-futuristic-manufacturing-technology/LG-Smart-Park_01.jpg",
      "filename": "topic_16_lg_smart_park_lighthouse.jpg",
      "caption": "LG Smart Park는 제조 데이터와 자동화 경험이 실제 운영 레퍼런스로 축적된 사례다.",
      "status": "confirmed"
    },
    {
      "image_id": "nvidia_lg_ai_factory_robot",
      "source": "NVIDIA Blog",
      "source_url": "https://blogs.nvidia.com/blog/nvidia-and-lg-group-ai-factory/",
      "image_url": "https://blogs.nvidia.com/wp-content/uploads/2026/06/kr-visit-lg-group-1920x1080-no-credit-1280x720.png",
      "filename": "topic_16_nvidia_lg_ai_factory_robot.png",
      "caption": "AI Factory는 제조 데이터를 simulation, validation, deployment workflow로 연결한다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgcns_factova_iot_expo",
      "source": "LG CNS",
      "source_url": "https://connect.lgcns.com/en/newsroom/press.html",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/uploads/2026/05/%EB%B6%81%EB%AF%B8%EC%97%91%EC%8A%A4%ED%8F%AC%EC%98%81%EB%AC%B8.jpg",
      "filename": "topic_16_lgcns_factova_iot_expo.jpg",
      "caption": "LG CNS의 Factova는 제조 데이터를 고객이 구매할 수 있는 플랫폼·솔루션으로 바꾸는 방향을 보여준다.",
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
            "used_by": ["topics/16_how_does_manufacturing_data_become_an_ai_product.md"],
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
            "used_by": ["topics/16_how_does_manufacturing_data_become_an_ai_product.md"],
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
            "used_by": ["topics/16_how_does_manufacturing_data_become_an_ai_product.md"],
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

    manifest_path = out_dir / "topic_16_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_16.json"

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
