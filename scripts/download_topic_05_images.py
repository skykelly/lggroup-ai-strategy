#!/usr/bin/env python3
"""
Download original source images for:
topics/05_what_did_palantir_ask_lg.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_05_images.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_what_did_palantir_ask_lg",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lgcorp_palantir_meeting_image_needed",
      "source": "LG Corp.",
      "source_url": "https://www.lgcorp.com/media/release/30066",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_05_lgcorp_palantir_meeting.jpg",
      "caption": "구광모 LG 회장은 2026년 4월 2일 Silicon Valley에서 Palantir의 Alex Karp와 만나 Ontology와 AI·data-driven decision-making framework를 논의했다. 원문 이미지 URL은 직접 확보 필요.",
      "status": "image_url_needed"
    },
    {
      "image_id": "lgcns_palantir_signing",
      "source": "Digital Today / LG CNS",
      "source_url": "https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion",
      "image_url": "https://cdn.digitaltoday.co.kr/news/photo/202603/640006_590746_75.jpg",
      "filename": "topic_05_lgcns_palantir_signing.jpg",
      "caption": "LG CNS와 Palantir의 전략적 파트너십 체결. Foundry와 AIP를 LG그룹 및 외부 고객 AX에 적용하는 방향이 제시됐다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgcns_ax_platform_1",
      "source": "LG CNS",
      "source_url": "https://www.lgcns.com/en/service/ai/ai-platform/",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_1.png",
      "filename": "topic_05_lgcns_ax_platform_1.png",
      "caption": "LG CNS AX Platform은 기업 데이터와 AI 활용을 연결하는 내부 기반으로 해석할 수 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgcns_ax_platform_2",
      "source": "LG CNS",
      "source_url": "https://www.lgcns.com/en/service/ai/ai-platform/",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_2.png",
      "filename": "topic_05_lgcns_ax_platform_2.png",
      "caption": "Palantir 협력은 외부 플랫폼 도입을 넘어, LG형 enterprise data operating model을 어떻게 만들 것인지의 문제와 연결된다.",
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
            "used_by": ["topics/05_what_did_palantir_ask_lg.md"],
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
            "used_by": ["topics/05_what_did_palantir_ask_lg.md"],
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
            "used_by": ["topics/05_what_did_palantir_ask_lg.md"],
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

    manifest_path = out_dir / "topic_05_image_download_manifest.json"
    inventory_path = data_dir / "image_inventory.topic_05.json"

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
