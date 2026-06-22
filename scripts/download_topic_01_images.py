#!/usr/bin/env python3
"""
Download original source images for:
topics/01_what_did_jensen_huang_leave_lg.md

Policy:
- Store every downloaded image in a single flat folder: assets/images/
- Do not create docs/topics/concepts/companies subfolders under assets/images/
- If a download fails, keep the original remote URL in Markdown and record the error.
- Skip IMAGE_URL_NEEDED entries.
- Do not generate or transform images.

Usage:
  python scripts/download_topic_01_images.py

Expected repo layout:
  assets/images/
  data/
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request
import urllib.parse


MANIFEST = {
  "topic_id": "topic_what_did_jensen_huang_leave_lg",
  "output_dir": "assets/images",
  "images": [
    {
      "image_id": "lg_nvidia_map_koo_huang",
      "source": "PRNewswire / LG",
      "source_url": "https://www.prnewswire.com/news-releases/lg-teams-with-nvidia-to-shape-the-future-with-map-mobility--ai-infra--physical-ai-302793797.html",
      "image_url": "https://mma.prnewswire.com/media/2995864/1.jpg?w=500",
      "filename": "topic_01_lg_nvidia_map_koo_huang.jpg",
      "caption": "구광모 LG 회장과 젠슨 황 NVIDIA CEO가 서울 여의도 LG트윈타워에서 전략 협력 논의 후 기념 촬영을 하고 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "nvidia_lg_ai_factory_robot",
      "source": "NVIDIA Blog",
      "source_url": "https://blogs.nvidia.com/blog/nvidia-and-lg-group-ai-factory/",
      "image_url": "https://blogs.nvidia.com/wp-content/uploads/2026/06/kr-visit-lg-group-1920x1080-no-credit-1280x720.png",
      "filename": "topic_01_nvidia_lg_ai_factory_robot.png",
      "caption": "NVIDIA가 설명한 LG AI Factory의 상징 이미지. 로봇, 자율주행, 데이터센터, GPU 클라우드가 하나의 Physical AI workflow로 연결된다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_dcw_cdu_press",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/press-setting-image-desktop-tablet-dcw-1440.png",
      "filename": "topic_01_lge_dcw_cdu_press.png",
      "caption": "DCW 2026의 LG 부스에서 관람객이 1.4MW Coolant Distribution Unit을 살펴보고 있다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_dcw_expo_cooling_1",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/DCW%202026%20Expo%20Image%201.jpg",
      "filename": "topic_01_lge_dcw_expo_cooling_1.jpg",
      "caption": "LG전자의 AI 데이터센터 냉각 솔루션 전시. DTC, CDU, CRAH, Chiller, immersion cooling, DCCM으로 확장되는 cooling stack을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lge_dcw_expo_cooling_2",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/DCW%202026%20Expo%20Image%202.jpg",
      "filename": "topic_01_lge_dcw_expo_cooling_2.jpg",
      "caption": "LG전자는 AI 데이터센터의 열관리 병목을 chip cooling에서 facility infrastructure까지 확장해 다룬다.",
      "status": "confirmed"
    },
    {
      "image_id": "lguplus_paju_aidc_site",
      "source": "Pulse by Maeil Business News Korea",
      "source_url": "https://pulse.mk.co.kr/news/english/12068307",
      "image_url": "https://pimg.mk.co.kr/news/cms/202606/08/news-p.v1.20260608.ae9589456ef3406ca639a3ef289bee8c_P1.png",
      "filename": "topic_01_lguplus_paju_aidc_site.png",
      "caption": "LG U+가 건설 중인 파주 200MW급 hyperscale AIDC 현장. AI Infra 사업의 물리적 거점을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lguplus_ace_on_trust",
      "source": "Seoul Economic Daily",
      "source_url": "https://en.sedaily.com/technology/2026/06/07/lg-uplus-targets-5-trillion-won-in-aidc-orders-by-2030",
      "image_url": "https://wimg.sedaily.com/news/cms/2026/06/07/news-p.v1.20260607.9bdb122ce9694d22b0bc1389e376a6a5_P1.png",
      "filename": "topic_01_lguplus_ace_on_trust.png",
      "caption": "LG U+의 차세대 AIDC 전략 ‘The ACE on Trust’. Agility, Capacity, Efficiency를 Trust 위에 결합한다.",
      "status": "confirmed"
    },
    {
      "image_id": "nvidia_800v_architecture",
      "source": "NVIDIA Technical Blog",
      "source_url": "https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/",
      "image_url": "https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/800-V-tech-blog-fig-2.png",
      "filename": "topic_01_nvidia_800v_architecture.png",
      "caption": "NVIDIA 800V DC architecture 개념도. AI Factory의 병목이 GPU에서 전력·냉각·운영 효율로 이동하고 있음을 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgensol_baround_core_values",
      "source": "LG Energy Solution",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv02_img_03_mo_en.png",
      "filename": "topic_01_lgensol_baround_core_values.png",
      "caption": "LG에너지솔루션 B.around의 핵심 가치. 배터리는 셀을 넘어 진단·관리·서비스 플랫폼으로 확장된다.",
      "status": "confirmed"
    },
    {
      "image_id": "lginnotek_autonomous_sensor_fusion",
      "source": "LG Innotek",
      "source_url": "https://www.lginnotek.com/solution/autoDrive.do?locale=en",
      "image_url": "https://www.lginnotek.com/resources/img/img-solution-autonomous-04en.png",
      "filename": "topic_01_lginnotek_autonomous_sensor_fusion.png",
      "caption": "LG이노텍의 자율주행 센서 포트폴리오. NVIDIA DRIVE Hyperion 협력에서 sensing, communication, lighting layer의 의미를 보여준다.",
      "status": "confirmed"
    },
    {
      "image_id": "lgcns_ai_box_image_needed",
      "source": "The Korea Times / LG CNS",
      "source_url": "https://www.koreatimes.co.kr/business/tech-science/20260305/lg-cns-unveils-container-based-ai-box-for-rapid-ai-data-center-expansion",
      "image_url": "IMAGE_URL_NEEDED",
      "filename": "topic_01_lgcns_ai_box_image_needed.jpg",
      "caption": "LG CNS AI Box는 AI servers, power, cooling, operations를 하나로 묶은 container-based AI data center package다. 원문 이미지 URL은 직접 확보 필요.",
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
            "original_url": url,
            "local_path": None,
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
            "intended_filename": item["filename"],
            "bytes": len(data),
            "content_type": content_type,
            "status": item["status"],
            "caption": item["caption"],
            "used_by": [
                "topics/01_what_did_jensen_huang_leave_lg.md"
            ],
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
            "used_by": [
                "topics/01_what_did_jensen_huang_leave_lg.md"
            ],
            "error": repr(exc),
        }


def main() -> None:
    out_dir = Path(MANIFEST["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for item in MANIFEST["images"]:
        print(f"Processing {item['image_id']}")
        result = download_file(item, out_dir)
        results.append(result)
        if not result.get("skipped"):
            time.sleep(0.5)

    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    topic_manifest_path = out_dir / "topic_01_image_download_manifest.json"
    topic_manifest_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    inventory_path = data_dir / "image_inventory.topic_01.json"
    inventory_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok_count = sum(1 for r in results if r.get("ok"))
    skipped_count = sum(1 for r in results if r.get("skipped"))
    fail_count = len(results) - ok_count - skipped_count

    print(f"Done. ok={ok_count}, failed={fail_count}, skipped={skipped_count}")
    print(f"Manifest: {topic_manifest_path}")
    print(f"Inventory fragment: {inventory_path}")

    if fail_count:
        print("\nFailed downloads; keep remote URLs in Markdown:")
        for r in results:
            if not r.get("ok") and not r.get("skipped"):
                print(f"- {r['image_id']}: {r['error']}")


if __name__ == "__main__":
    main()
