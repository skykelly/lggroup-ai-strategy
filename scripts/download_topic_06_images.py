#!/usr/bin/env python3
"""
Download original source images for:
topics/06_can_lg_win_ai_mobility_without_making_cars.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_06_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_can_lg_win_ai_mobility_without_making_cars",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lge_ai_in_vehicle_overview",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-1-D.png",
      "filename": "topic_06_lge_ai_in_vehicle_overview.png",
      "caption": "LG의 AI-powered in-vehicle solutions는 display, sensing, on-device AI를 하나의 in-vehicle experience로 묶는다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_mobility_display_solution",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-2.png",
      "filename": "topic_06_lge_mobility_display_solution.png",
      "caption": "Mobility Display Solution은 차량 유리와 디스플레이를 AI interface로 확장하는 방향을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lginnotek_ces2026_sketch_05",
      "source": "LG Innotek",
      "source_url": "https://www.lginnotek.com/showcase/ces2026.do?locale=en",
      "image_url": "https://www.lginnotek.com/resources/img/ces/sketch-05.avif",
      "filename": "topic_06_lginnotek_ces2026_sketch_05.avif",
      "caption": "LG이노텍은 CES 2026에서 camera, LiDAR, radar, 5G module, UWB digital key, wireless BMS 등 future car components를 제시했다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_baround_sdv_bms",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop5_mo_en.png",
      "filename": "topic_06_lgensol_baround_sdv_bms.png",
      "caption": "LG에너지솔루션은 B.around와 SDV BMS를 통해 배터리 데이터를 차량 software layer와 연결한다.",
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
            "used_by": ["topics/06_can_lg_win_ai_mobility_without_making_cars.md"],
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
            "used_by": ["topics/06_can_lg_win_ai_mobility_without_making_cars.md"],
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
            "used_by": ["topics/06_can_lg_win_ai_mobility_without_making_cars.md"],
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

    manifest_path = out_dir / "topic_06_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_06.json"

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
