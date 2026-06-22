#!/usr/bin/env python3
"""
Download original source images for:
topics/08_can_battery_software_become_lges_next_platform.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_08_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_can_battery_software_become_lges_next_platform",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lgensol_baround_core_values",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv02_img_03_mo_en.png",
      "filename": "topic_08_lgensol_baround_core_values.png",
      "caption": "B.around는 배터리 생애주기 전반을 진단·관리·서비스로 확장하는 BMTS 관점을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_bms_lifecycle",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop1_mo_en.png",
      "filename": "topic_08_lgensol_bms_lifecycle.png",
      "caption": "BMTS는 전통적 BMS를 넘어 배터리 전체 lifecycle을 관리하는 software·cloud·AI 기반 솔루션으로 설명된다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_sdv_bms",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop5_mo_en.png",
      "filename": "topic_08_lgensol_sdv_bms.png",
      "caption": "SDV BMS는 BMS 기능을 차량의 고성능 컴퓨팅 환경과 연결하는 방향을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_bms_to_hpc",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop3_mo_en.png",
      "filename": "topic_08_lgensol_bms_to_hpc.png",
      "caption": "Battery software가 SDV architecture와 연결되면 배터리는 차량 software layer의 일부가 된다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_sdverse_image_needed",
      "source": "LG Energy Solution",
      "source_url": "https://www.lgensol.com/mobile/en/company/newsroom-detail?seq=8753",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_08_lgensol_sdverse.jpg",
      "caption": "LG에너지솔루션은 배터리 기업 최초로 SDVerse에 참여하며 SDV 환경에 최적화된 5개 battery software solution을 제시했다. 원문 이미지 URL은 별도 확보 필요.",
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
            "used_by": ["topics/08_can_battery_software_become_lges_next_platform.md"],
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
            "used_by": ["topics/08_can_battery_software_become_lges_next_platform.md"],
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
            "used_by": ["topics/08_can_battery_software_become_lges_next_platform.md"],
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

    manifest_path = out_dir / "topic_08_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_08.json"

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
