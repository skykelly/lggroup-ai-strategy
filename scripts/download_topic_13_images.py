#!/usr/bin/env python3
"""
Download original source images for:
topics/13_are_power_and_cooling_bottlenecks_new_growth_engines.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_13_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_are_power_and_cooling_bottlenecks_new_growth_engines",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lge_dcw_cdu_press",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/press-setting-image-desktop-tablet-dcw-1440.png",
      "filename": "topic_13_lge_dcw_cdu_press.png",
      "caption": "LG전자의 1.4MW CDU는 AI 데이터센터의 고열·고밀도 문제를 겨냥한 cooling solution이다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_dcw_expo_cooling_1",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/DCW%202026%20Expo%20Image%201.jpg",
      "filename": "topic_13_lge_dcw_expo_cooling_1.jpg",
      "caption": "LG전자는 DTC, immersion cooling, CRAH, chiller, DCCM, DC Grid를 포함한 end-to-end AIDC cooling portfolio를 제시했다.",
      "status": "confirmed"
    },
    {
      "image_id": "nvidia_800v_architecture",
      "source": "NVIDIA Technical Blog",
      "source_url": "https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/",
      "image_url": "https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/800-V-tech-blog-fig-2.png",
      "filename": "topic_13_nvidia_800v_architecture.png",
      "caption": "NVIDIA의 800V DC architecture는 AI Factory의 병목이 전력 분배와 에너지 효율로 이동하고 있음을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lguplus_paju_aidc_site",
      "source": "Pulse by Maeil Business News Korea",
      "source_url": "https://pulse.mk.co.kr/news/english/12068307",
      "image_url": "https://pimg.mk.co.kr/news/cms/202606/08/news-p.v1.20260608.ae9589456ef3406ca639a3ef289bee8c_P1.png",
      "filename": "topic_13_lguplus_paju_aidc_site.png",
      "caption": "AIDC는 GPU 서버보다 전력·냉각·입지·운영 효율을 함께 요구하는 물리 인프라 사업이다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_baround_core_values",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv02_img_03_mo_en.png",
      "filename": "topic_13_lgensol_baround_core_values.png",
      "caption": "LG에너지솔루션의 battery management 역량은 AI Infra 전력 안정화와 ESS/UPS 영역으로 확장될 수 있다.",
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
            "used_by": ["topics/13_are_power_and_cooling_bottlenecks_new_growth_engines.md"],
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
            "used_by": ["topics/13_are_power_and_cooling_bottlenecks_new_growth_engines.md"],
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
            "used_by": ["topics/13_are_power_and_cooling_bottlenecks_new_growth_engines.md"],
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

    manifest_path = out_dir / "topic_13_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_13.json"

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
