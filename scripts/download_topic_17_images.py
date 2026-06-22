#!/usr/bin/env python3
"""
Download original source images for:
topics/17_is_korean_ai_sovereignty_an_opportunity_or_burden_for_lg.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_17_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_is_korean_ai_sovereignty_an_opportunity_or_burden_for_lg",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lgai_exaone_journey",
      "source": "LG AI Research",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_journey_pc.png",
      "filename": "topic_17_lgai_exaone_journey.png",
      "caption": "Sovereign AI 논의에서 EXAONE은 한국어·산업 문맥을 가진 국내 모델 layer로 해석할 수 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "exaone45_github_symbol",
      "source": "LG-AI-EXAONE GitHub",
      "source_url": "https://github.com/LG-AI-EXAONE/EXAONE-4.5",
      "image_url": "https://raw.githubusercontent.com/LG-AI-EXAONE/EXAONE-4.5/main/assets/EXAONE_Symbol%2BBI_3d.png",
      "filename": "topic_17_exaone45_github_symbol.png",
      "caption": "EXAONE 4.5의 공개는 국내 AI 생태계와 기업 AI 통제력 측면에서 의미가 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "msit_sovereign_ai_image_needed",
      "source": "MSIT",
      "source_url": "https://www.msit.go.kr/eng/bbs/view.do?bbsSeqNo=42&mId=4&mPid=2&nttSeqNo=1212&sCode=eng",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_17_msit_sovereign_ai.png",
      "caption": "MSIT는 Sovereign AI Foundation Model 프로젝트를 AI G3 전략과 기술·문화·경제·안보 의존도 완화 관점에서 설명한다. 직접 이미지 URL은 별도 확보 필요.",
      "status": "image_url_needed"
    },
    {
      "image_id": "lg_nvidia_map_koo_huang",
      "source": "PRNewswire / LG",
      "source_url": "https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html",
      "image_url": "https://mma.prnewswire.com/media/2995864/1.jpg?w=500",
      "filename": "topic_17_lg_nvidia_map_koo_huang.jpg",
      "caption": "Sovereign AI는 폐쇄가 아니라 글로벌 stack과 국내 역량을 함께 쓰는 managed interdependence의 문제다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_dcw_cdu_press",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/press-setting-image-desktop-tablet-dcw-1440.png",
      "filename": "topic_17_lge_dcw_cdu_press.png",
      "caption": "AI sovereignty는 모델뿐 아니라 compute, 전력, 냉각, 데이터센터 운영 통제력과 연결된다.",
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
            "used_by": ["topics/17_is_korean_ai_sovereignty_an_opportunity_or_burden_for_lg.md"],
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
            "used_by": ["topics/17_is_korean_ai_sovereignty_an_opportunity_or_burden_for_lg.md"],
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
            "used_by": ["topics/17_is_korean_ai_sovereignty_an_opportunity_or_burden_for_lg.md"],
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

    manifest_path = out_dir / "topic_17_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_17.json"

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
