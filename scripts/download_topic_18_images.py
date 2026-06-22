#!/usr/bin/env python3
"""
Download original source images for:
topics/18_how_gpu_cloud_price_decline_changes_aidc_business.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_18_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_how_gpu_cloud_price_decline_changes_aidc_business",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lguplus_paju_aidc_site",
      "source": "Pulse by Maeil Business News Korea",
      "source_url": "https://pulse.mk.co.kr/news/english/12068307",
      "image_url": "https://pimg.mk.co.kr/news/cms/202606/08/news-p.v1.20260608.ae9589456ef3406ca639a3ef289bee8c_P1.png",
      "filename": "topic_18_lguplus_paju_aidc_site.png",
      "caption": "GPU Cloud 가격이 하락하면 AIDC는 단순 GPU 임대가 아니라 운영 효율과 안정성으로 차별화해야 한다.",
      "status": "confirmed"
    },
    {
      "image_id": "iea_datacenter_electricity_chart_needed",
      "source": "IEA",
      "source_url": "https://www.iea.org/data-and-statistics/charts/global-data-centre-electricity-consumption-by-equipment-base-case-2020-2030",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_18_iea_datacenter_electricity_chart.png",
      "caption": "IEA 데이터센터 전력 소비 전망 차트. 동적 렌더링으로 직접 이미지 URL은 별도 확보 필요.",
      "status": "image_url_needed"
    },
    {
      "image_id": "lge_dcw_cdu_press",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/press-setting-image-desktop-tablet-dcw-1440.png",
      "filename": "topic_18_lge_dcw_cdu_press.png",
      "caption": "가격 하락 환경에서 냉각과 전력 효율은 AIDC 수익성을 방어하는 핵심 요소다.",
      "status": "confirmed"
    },
    {
      "image_id": "nvidia_800v_architecture",
      "source": "NVIDIA Technical Blog",
      "source_url": "https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/",
      "image_url": "https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/800-V-tech-blog-fig-2.png",
      "filename": "topic_18_nvidia_800v_architecture.png",
      "caption": "GPU Cloud 가격이 내려갈수록 전력 구조와 compute per megawatt가 사업성을 좌우한다.",
      "status": "confirmed"
    },
    {
      "image_id": "lguplus_ace_on_trust",
      "source": "Seoul Economic Daily",
      "source_url": "https://en.sedaily.com/technology/2026/06/07/lg-uplus-targets-5-trillion-won-in-aidc-orders-by-2030",
      "image_url": "https://wimg.sedaily.com/news/cms/2026/06/07/news-p.v1.20260607.9bdb122ce9694d22b0bc1389e376a6a5_P1.png",
      "filename": "topic_18_lguplus_ace_on_trust.png",
      "caption": "AIDC의 차별화는 가격보다 Agility, Capacity, Efficiency, Trust를 함께 제공하는 능력에서 나온다.",
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
            "used_by": ["topics/18_how_gpu_cloud_price_decline_changes_aidc_business.md"],
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
            "used_by": ["topics/18_how_gpu_cloud_price_decline_changes_aidc_business.md"],
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
            "used_by": ["topics/18_how_gpu_cloud_price_decline_changes_aidc_business.md"],
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

    manifest_path = out_dir / "topic_18_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_18.json"

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
