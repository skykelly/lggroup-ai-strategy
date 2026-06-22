#!/usr/bin/env python3
"""
Download source images for docs/06_global_ai_alliance_open_innovation.md.

Usage:
  python scripts/download_global_ai_alliance_open_innovation_images.py

The script downloads only original source images referenced by URL.
It does not generate, transform, or create new images.
Items marked as IMAGE_URL_NEEDED in the MD must be resolved manually.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request


MANIFEST = {
  "output_dir": "assets/images/06_global_ai_alliance_open_innovation",
  "images": [
    {
      "id": "lg_nvidia_map_koo_huang_prn",
      "theme": "global_ai_alliance_open_innovation",
      "source": "PRNewswire / LG",
      "source_url": "https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html",
      "image_url": "https://mma.prnewswire.com/media/2995864/1.jpg?w=500",
      "filename": "lg_nvidia_map_koo_huang_prn.jpg",
      "caption": "LG Corp. 구광모 회장과 NVIDIA Jensen Huang CEO. M.A.P. 협력은 Mobility, AI Infra, Physical AI를 연결하는 6번 테마의 핵심 축이다.",
      "status": "confirmed_but_timeout_possible"
    },
    {
      "id": "nvidia_lg_ai_factory_robot",
      "theme": "global_ai_alliance_open_innovation",
      "source": "NVIDIA Blog",
      "source_url": "https://blogs.nvidia.com/blog/nvidia-and-lg-group-ai-factory/",
      "image_url": "https://blogs.nvidia.com/wp-content/uploads/2026/06/kr-visit-lg-group-1920x1080-no-credit-1280x720.png",
      "filename": "nvidia_lg_ai_factory_robot.png",
      "caption": "NVIDIA Blog의 LG AI Factory 대표 이미지. 제조·로봇·디지털트윈·Physical AI 운영 모델과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_palantir_signing",
      "theme": "global_ai_alliance_open_innovation",
      "source": "Digital Today / LG CNS photo",
      "source_url": "https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion",
      "image_url": "https://cdn.digitaltoday.co.kr/news/photo/202603/640006_590746_75.jpg",
      "filename": "lgcns_palantir_signing.jpg",
      "caption": "LG CNS와 Palantir의 전략적 파트너십 체결. Enterprise AX와 온톨로지 기반 의사결정 체계의 외부 협력 축.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_skild_ai_hq",
      "theme": "global_ai_alliance_open_innovation",
      "source": "LG CNS Newsroom",
      "source_url": "https://www.lgcns.com/kr/newsroom/press/detail.66074",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/MAIN-scaled-e1749113375930-1920x1436.jpg",
      "filename": "lgcns_skild_ai_hq.jpg",
      "caption": "LG CNS와 Skild AI 협력 보도자료 이미지. 로봇 파운데이션 모델을 제조·물류 현장에 이식하는 협력 축.",
      "status": "confirmed_but_generic"
    },
    {
      "id": "lgai_exaone_journey",
      "theme": "global_ai_alliance_open_innovation",
      "source": "LG AI Research EXAONE",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_journey_pc.png",
      "filename": "lgai_exaone_journey.png",
      "caption": "EXAONE Journey. NVIDIA Blackwell, NeMo, Nemotron, TensorRT-LLM 등과 연결되는 LG AI Research의 모델 생태계 기반.",
      "status": "confirmed"
    },
    {
      "id": "lgenergy_baround_core_values",
      "theme": "global_ai_alliance_open_innovation",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv02_img_03_mo_en.png",
      "filename": "lgenergy_baround_core_values.png",
      "caption": "LG Energy Solution B.around Core Values. Qualcomm, SDVerse 협력과 연결되는 배터리 SW·BMTS 생태계 기반.",
      "status": "confirmed"
    },
    {
      "id": "lgenergy_bms_sdv",
      "theme": "global_ai_alliance_open_innovation",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop5_mo_en.png",
      "filename": "lgenergy_bms_sdv.png",
      "caption": "SDV BMS. Qualcomm Snapdragon Digital Chassis 및 SDVerse와 연결되는 배터리 소프트웨어 확장 방향.",
      "status": "confirmed"
    }
  ]
}


def get_referer(url: str) -> str:
    if "prnewswire.com" in url or "mma.prnewswire.com" in url:
        return "https://www.prnewswire.com/"
    if "blogs.nvidia.com" in url:
        return "https://blogs.nvidia.com/"
    if "digitaltoday.co.kr" in url:
        return "https://www.digitaltoday.co.kr/"
    if "lgcns.com" in url:
        return "https://www.lgcns.com/"
    if "lgresearch.ai" in url:
        return "https://www.lgresearch.ai/"
    if "lgensol.com" in url:
        return "https://www.lgensol.com/"
    return "https://www.google.com/"


def download_file(url: str, dest: Path, timeout: int = 30) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Referer": get_referer(url),
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read()

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

        return {
            "ok": True,
            "path": str(dest),
            "bytes": len(data),
            "content_type": content_type,
            "error": None,
        }

    except Exception as exc:
        return {
            "ok": False,
            "path": str(dest),
            "bytes": 0,
            "content_type": None,
            "error": repr(exc),
        }


def main() -> None:
    out_dir = Path(MANIFEST["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for item in MANIFEST["images"]:
        url = item["image_url"]
        dest = out_dir / item["filename"]
        print(f"Downloading {item['id']} -> {dest}")
        result = download_file(url, dest)
        result.update({
            "id": item["id"],
            "source": item["source"],
            "source_url": item["source_url"],
            "image_url": url,
            "filename": item["filename"],
            "caption": item["caption"],
            "status": item["status"],
        })
        results.append(result)
        time.sleep(0.5)

    manifest_path = out_dir / "image_download_manifest.json"
    manifest_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok_count = sum(1 for r in results if r["ok"])
    fail_count = len(results) - ok_count
    print(f"Done. ok={ok_count}, failed={fail_count}")
    print(f"Manifest: {manifest_path}")

    if fail_count:
        print("\nFailed downloads:")
        for r in results:
            if not r["ok"]:
                print(f"- {r['id']}: {r['error']}")


if __name__ == "__main__":
    main()
