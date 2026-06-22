#!/usr/bin/env python3
"""
Download original source images for:
topics/07_is_physical_ai_more_than_smart_factory_rebranding.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_07_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_is_physical_ai_more_than_smart_factory_rebranding",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "nvidia_lg_ai_factory_robot",
      "source": "NVIDIA Blog",
      "source_url": "https://blogs.nvidia.com/blog/nvidia-and-lg-group-ai-factory/",
      "image_url": "https://blogs.nvidia.com/wp-content/uploads/2026/06/kr-visit-lg-group-1920x1080-no-credit-1280x720.png",
      "filename": "topic_07_nvidia_lg_ai_factory_robot.png",
      "caption": "Physical AI는 AI를 실제 로봇·공장·차량 환경에 적용하기 위한 데이터, 시뮬레이션, 검증 workflow를 필요로 한다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_smart_factory_main",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/main-image-desktopmobile-ecsmart-464.png",
      "filename": "topic_07_lge_smart_factory_main.png",
      "caption": "LG전자는 제조 전 과정의 end-to-end smart factory solution을 강조한다.",
      "status": "confirmed"
    },
    {
      "image_id": "lg_smart_park_lighthouse",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/home-appliance-solution/lg-smart-park-named-lighthouse-factory-for-futuristic-manufacturing-technology/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/home-appliance-solution/lg-smart-park-named-lighthouse-factory-for-futuristic-manufacturing-technology/LG-Smart-Park_01.jpg",
      "filename": "topic_07_lg_smart_park_lighthouse.jpg",
      "caption": "LG Smart Park는 자동화·AI·디지털트윈이 실제 제조 현장에 적용된 Lighthouse Factory 레퍼런스다.",
      "status": "confirmed"
    },
    {
      "image_id": "lginnotek_applied_intuition_image_needed",
      "source": "LG Innotek",
      "source_url": "https://www.lginnotek.com/news/pressView.do?idx=6582&locale=en",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_07_lginnotek_applied_intuition.jpg",
      "caption": "LG이노텍과 Applied Intuition의 협력은 sensing hardware, simulation, validation이 Physical AI로 연결되는 사례다. 원문 이미지 URL은 별도 확보 필요.",
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
            "used_by": ["topics/07_is_physical_ai_more_than_smart_factory_rebranding.md"],
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
            "used_by": ["topics/07_is_physical_ai_more_than_smart_factory_rebranding.md"],
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
            "used_by": ["topics/07_is_physical_ai_more_than_smart_factory_rebranding.md"],
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

    manifest_path = out_dir / "topic_07_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_07.json"

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
