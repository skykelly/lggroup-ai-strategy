#!/usr/bin/env python3
"""
Download source images for docs/01_ai_data_center_infra.md.

Usage:
  python scripts/download_ai_data_center_infra_images.py
  python scripts/download_ai_data_center_infra_images.py --out assets/images/01_ai_data_center_infra
  python scripts/download_ai_data_center_infra_images.py --manifest image_download_manifest.json

Notes:
- This script downloads images from original source/CDN URLs referenced in the wiki doc.
- Some media CDN URLs may block hotlinking or time out. Failed items are logged and kept in the manifest for manual follow-up.
- No images are generated. This only downloads original source images.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse, unquote

try:
    import requests
except ImportError as exc:
    raise SystemExit("requests is required. Install with: pip install requests") from exc

IMAGE_ASSETS: List[Dict[str, str]] = [
    {
        "id": "img_lge_dcw_2026_cdu_01",
        "description": "LG DCW 2026 CDU exhibition image 1",
        "url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/DCW%202026%20Expo%20Image%201.jpg",
        "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
        "status": "confirmed",
    },
    {
        "id": "img_lge_dcw_2026_cdu_02",
        "description": "LG DCW 2026 CDU exhibition image 2",
        "url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/DCW%202026%20Expo%20Image%202.jpg",
        "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
        "status": "confirmed",
    },
    {
        "id": "img_lguplus_paju_pulse_01",
        "description": "LG Uplus Paju AIDC construction site",
        "url": "https://pimg.mk.co.kr/news/cms/202606/08/news-p.v1.20260608.ae9589456ef3406ca639a3ef289bee8c_P1.png",
        "source_url": "https://pulse.mk.co.kr/news/english/12068307",
        "status": "confirmed",
    },
    {
        "id": "img_lguplus_paju_digitaltoday_01",
        "description": "LG Uplus next-generation AI infrastructure strategy presentation",
        "url": "https://cdn.digitaltoday.co.kr/news/photo/202606/672472_621286_631.jpg",
        "source_url": "https://www.digitaltoday.co.kr/en/view/61108/lgu-to-step-up-ai-data-centre-business-targets-5-trillion-won-in-orders-by-2030",
        "status": "needs_download_check",
    },
    {
        "id": "img_lgcns_ai_box_01",
        "description": "LG CNS AI Box cutaway",
        "url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/uploads/2026/03/AI%EB%B0%95%EC%8A%A4.jpg",
        "source_url": "https://www.lgcns.com/kr/newsroom/press/detail.aidc-2603-2",
        "status": "confirmed",
    },
    {
        "id": "img_lgcns_ai_box_campus_01",
        "description": "LG CNS AI Box Campus concept",
        "url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/uploads/2026/03/AI%EB%B0%95%EC%8A%A4%EC%BA%A0%ED%8D%BC%EC%8A%A4.jpg",
        "source_url": "https://www.lgcns.com/kr/newsroom/press/detail.aidc-2603-2",
        "status": "confirmed",
    },
    {
        "id": "img_lgensol_ess_na_01",
        "description": "LG Energy Solution North America ESS manufacturing overview",
        "url": "https://news.lgensol.com/wp-content/uploads/2026/04/LGES_LG-Energy-Solutions-North-America-ESS-manufacturing-overview_600KB.png",
        "source_url": "https://news.lgensol.com/company-news/supplementary-stories/4880/",
        "status": "confirmed",
    },
    {
        "id": "img_koreatimes_ess_container_01",
        "description": "LG Energy Solution grid-scale ESS containers",
        "url": "https://newsimg.koreatimes.co.kr/2026/03/17/ffdebf62-4cdf-406b-b455-d98c36f3fecf.jpg?w=728",
        "source_url": "https://www.koreatimes.co.kr/business/tech-science/20260318/lg-bets-on-ai-data-center-ess-as-future-growth-driver",
        "status": "confirmed_media_cdn",
    },
    {
        "id": "img_koreatimes_ai_box_module_01",
        "description": "LG CNS AI Box module image",
        "url": "https://newsimg.koreatimes.co.kr/2026/03/17/46628003-deeb-4be1-a36e-4e3a182f2853.jpg?w=728",
        "source_url": "https://www.koreatimes.co.kr/business/tech-science/20260318/lg-bets-on-ai-data-center-ess-as-future-growth-driver",
        "status": "confirmed_media_cdn",
    },
    {
        "id": "img_koreatimes_cdu_01",
        "description": "LG Electronics CDU on display",
        "url": "https://newsimg.koreatimes.co.kr/2026/03/17/c4cc7129-49d9-4643-adb1-f9bbeb0de08e.jpg?w=728",
        "source_url": "https://www.koreatimes.co.kr/business/tech-science/20260318/lg-bets-on-ai-data-center-ess-as-future-growth-driver",
        "status": "needs_download_check",
    },
]


def guess_extension(url: str, content_type: str | None) -> str:
    parsed = urlparse(url)
    path = unquote(parsed.path)
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return suffix
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if ext:
            return ext
    return ".img"


def safe_filename(asset_id: str, url: str, content_type: str | None) -> str:
    ext = guess_extension(url, content_type)
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", asset_id).strip("_")
    return f"{base}{ext}"


def download_one(asset: Dict[str, str], out_dir: Path, timeout: int = 30, retries: int = 3) -> Dict[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LG-AI-Wiki-ImageDownloader/1.0)",
        "Referer": asset.get("source_url", ""),
    }
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(asset["url"], headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if content_type and not content_type.lower().startswith("image/"):
                raise ValueError(f"URL did not return image content-type: {content_type}")

            filename = safe_filename(asset["id"], asset["url"], content_type)
            out_path = out_dir / filename
            with out_path.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 128):
                    if chunk:
                        f.write(chunk)

            return {
                **asset,
                "download_status": "ok",
                "local_path": str(out_path.as_posix()),
                "content_type": content_type,
                "bytes": str(out_path.stat().st_size),
            }
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            if attempt < retries:
                time.sleep(1.5 * attempt)

    return {
        **asset,
        "download_status": "failed",
        "local_path": "",
        "error": last_error,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="assets/images/01_ai_data_center_infra", help="Output directory")
    parser.add_argument("--manifest", default="image_download_manifest.json", help="Manifest JSON output path")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout seconds")
    parser.add_argument("--retries", type=int, default=3, help="Retry count per image")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    results: List[Dict[str, str]] = []
    for asset in IMAGE_ASSETS:
        print(f"Downloading {asset['id']} ...", flush=True)
        result = download_one(asset, out_dir=out_dir, timeout=args.timeout, retries=args.retries)
        status = result.get("download_status")
        if status == "ok":
            print(f"  OK -> {result['local_path']} ({result['bytes']} bytes)")
        else:
            print(f"  FAILED -> {result.get('error', 'unknown error')}", file=sys.stderr)
        results.append(result)

    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps({"images": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Manifest written to {manifest_path}")

    failures = [r for r in results if r.get("download_status") != "ok"]
    if failures:
        print(f"Completed with {len(failures)} failed downloads.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
