#!/usr/bin/env python3
"""
Download source images for docs/03_ai_mobility_sdv_aidv.md.

Usage:
  python scripts/download_ai_mobility_sdv_aidv_images.py

The script downloads only original source images referenced by URL.
It does not generate, transform, or create new images.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import urllib.request


MANIFEST = {
  "output_dir": "assets/images/03_ai_mobility_sdv_aidv",
  "images": [
    {
      "id": "lge_ai_in_vehicle_overview",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-1-D.png",
      "filename": "lge_ai_in_vehicle_overview.png",
      "caption": "LG AI-powered In-Vehicle Solutions. 디스플레이, 인캐빈 센싱, 온디바이스 AI를 결합한 AI-Defined Vehicle 경험.",
      "status": "confirmed"
    },
    {
      "id": "lge_mobility_display_solution",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-2.png",
      "filename": "lge_mobility_display_solution.png",
      "caption": "Mobility Display Solution. 투명 OLED 윈드실드와 AI 인터페이스를 결합한 차량 내 디스플레이 경험.",
      "status": "confirmed"
    },
    {
      "id": "lge_automotive_vision_solution",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-3.png",
      "filename": "lge_automotive_vision_solution.png",
      "caption": "Automotive Vision Solution. 운전자·탑승자 상태와 주변 맥락을 인식해 안전과 개인화 경험을 제공하는 콘셉트.",
      "status": "confirmed"
    },
    {
      "id": "lge_in_vehicle_entertainment_solution",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image_4.png",
      "filename": "lge_in_vehicle_entertainment_solution.png",
      "caption": "In-Vehicle Entertainment Solution. 차량 창문·디스플레이를 AI 기반 인터랙티브 미디어 공간으로 확장하는 경험.",
      "status": "confirmed"
    },
    {
      "id": "lginnotek_ces2026_sketch_05",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Innotek CES 2026 Showcase",
      "source_url": "https://www.lginnotek.com/showcase/ces2026.do",
      "image_url": "https://www.lginnotek.com/resources/img/ces/sketch-05.avif",
      "filename": "lginnotek_ces2026_sketch_05.avif",
      "caption": "LG이노텍 CES 2026 모빌리티 전시 현장 이미지 후보. AVIF 형식이며 렌더링/다운로드 환경 확인 필요.",
      "status": "confirmed_avif"
    },
    {
      "id": "lginnotek_ces2026_sketch_06",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Innotek CES 2026 Showcase",
      "source_url": "https://www.lginnotek.com/showcase/ces2026.do",
      "image_url": "https://www.lginnotek.com/resources/img/ces/sketch-06.avif",
      "filename": "lginnotek_ces2026_sketch_06.avif",
      "caption": "LG이노텍 CES 2026 자율주행·전동화 솔루션 전시 현장 이미지 후보. AVIF 형식이며 렌더링/다운로드 환경 확인 필요.",
      "status": "confirmed_avif"
    },
    {
      "id": "lginnotek_ces2026_sketch_small_02",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Innotek CES 2026 Showcase",
      "source_url": "https://www.lginnotek.com/showcase/ces2026.do",
      "image_url": "https://www.lginnotek.com/resources/img/ces/sketch-s-02.avif",
      "filename": "lginnotek_ces2026_sketch_small_02.avif",
      "caption": "LG이노텍 CES 2026 전시 하이라이트 썸네일 이미지 후보.",
      "status": "confirmed_avif"
    },
    {
      "id": "lgdisplay_ces2026_main",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Display Newsroom",
      "source_url": "https://www.lgdisplay.com/kor/company/media-center/latest-news?contentId=5495",
      "image_url": "https://www-cdn.lgdisplay.com/v1/c362c3ebb68e4dd98c62bfd9599e9d75/bucket-lgd-hp-contents/2026-01-05/dNSW6lY16t1Tvj10ajtLFebydHuNDHfZ.png",
      "filename": "lgdisplay_ces2026_main.png",
      "caption": "LG디스플레이 CES 2026 전시 대표 이미지. AI 시대 디스플레이 전략과 차량용 디스플레이 전시를 함께 소개.",
      "status": "confirmed_but_fetch_400_possible"
    },
    {
      "id": "lgdisplay_ces2026_automotive_display",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Display Newsroom",
      "source_url": "https://www.lgdisplay.com/kor/company/media-center/latest-news?contentId=5495",
      "image_url": "https://www-cdn.lgdisplay.com/v1/c362c3ebb68e4dd98c62bfd9599e9d75/bucket-lgd-hp-contents/2026-01-05/laNQS3RNREGPZm9c3NIZ1dKD24UKjSjM.jpg",
      "filename": "lgdisplay_ces2026_automotive_display.jpg",
      "caption": "LG디스플레이 CES 2026 차량용 디스플레이 이미지. P2P, Slidable OLED 등 SDV용 HMI 방향과 연결.",
      "status": "confirmed_but_fetch_400_possible"
    },
    {
      "id": "lgensol_baround_core_values",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv02_img_03_mo_en.png",
      "filename": "lgensol_baround_core_values.png",
      "caption": "B.around Core Values. 진단 전문성, 신뢰 기반 관리, 혁신 서비스, 직관적 경험을 강조.",
      "status": "confirmed"
    },
    {
      "id": "lgensol_bms_lifecycle",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop1_mo_en.png",
      "filename": "lgensol_bms_lifecycle.png",
      "caption": "BMS는 배터리 수명주기, 성능, 안전 관리를 담당하는 핵심 제어 시스템으로 설명된다.",
      "status": "confirmed"
    },
    {
      "id": "lgensol_sdv_bms",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop5_mo_en.png",
      "filename": "lgensol_sdv_bms.png",
      "caption": "SDV BMS. BMS 기능을 고성능 컴퓨팅과 AI 기반 진단·제어로 확장하는 개념.",
      "status": "confirmed"
    },
    {
      "id": "lgensol_bms_features_to_hpc",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG Energy Solution B.around",
      "source_url": "https://www.lgensol.com/mobile/en/business/baround",
      "image_url": "https://www.lgensol.com/inc/images/img/serv_bms_pop3_mo_en.png",
      "filename": "lgensol_bms_features_to_hpc.png",
      "caption": "BMS 기능이 HPC 환경으로 확장되는 개념 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lguplus_autonomous_driving_main",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG U+ Autonomous Driving",
      "source_url": "https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127",
      "image_url": "https://www.lguplus.com/static/pc-contents/images/uhdc/entp/pr/20230726-111732-657-zkOTPTlY.jpg",
      "filename": "lguplus_autonomous_driving_main.jpg",
      "caption": "LG U+ 자율주행 서비스 대표 이미지. 원본 페이지에서 직접 이미지 URL 확보.",
      "status": "url_confirmed_but_fetch_400_possible"
    },
    {
      "id": "lguplus_dynamic_map_features",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG U+ Autonomous Driving",
      "source_url": "https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127",
      "image_url": "https://image.lguplus.com/static/pc-contents/images/fcmm/cnts/imge/20230724-045046-845-7m6JNc0Y.png",
      "filename": "lguplus_dynamic_map_features.png",
      "caption": "U+ Dynamic 정밀지도 플랫폼. 정밀지도 융합, 정밀 전자지도 적용, 국제 표준 준수를 설명.",
      "status": "confirmed"
    },
    {
      "id": "lguplus_control_center",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG U+ Autonomous Driving",
      "source_url": "https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127",
      "image_url": "https://image.lguplus.com/static/pc-contents/images/fcmm/cnts/imge/20230724-045059-757-lKafcyHG.png",
      "filename": "lguplus_control_center.png",
      "caption": "자율주행 운영 관제센터 이미지. 실시간 위치·운행상태 모니터링과 운영관리 역할을 설명.",
      "status": "confirmed"
    },
    {
      "id": "lguplus_dynamic_map_architecture",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG U+ Autonomous Driving",
      "source_url": "https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127",
      "image_url": "https://image.lguplus.com/static/pc-contents/images/fcmm/cnts/imge/20230724-045723-227-BDbJxueg.png",
      "filename": "lguplus_dynamic_map_architecture.png",
      "caption": "U+ Dynamic 정밀지도 플랫폼 구성도. 객체인식센서, Static 정밀지도, 인프라 정보, V2X 정보를 연결.",
      "status": "confirmed"
    },
    {
      "id": "lguplus_autonomous_control_architecture",
      "theme": "ai_mobility_sdv_aidv",
      "source": "LG U+ Autonomous Driving",
      "source_url": "https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127",
      "image_url": "https://image.lguplus.com/static/pc-contents/images/fcmm/cnts/imge/20251231-111108-771-geJgzr8n.png",
      "filename": "lguplus_autonomous_control_architecture.png",
      "caption": "U+ 자율주행 관제 구성도. 5G, MEC V2X Gateway, 관제 서버, Dynamic Map 서버, 정밀측위 서버를 연결.",
      "status": "confirmed"
    }
  ]
}


def download_file(url: str, dest: Path, timeout: int = 30) -> dict:
    referer = "https://www.lg.com/"
    if "lginnotek.com" in url:
        referer = "https://www.lginnotek.com/showcase/ces2026.do"
    elif "lgdisplay.com" in url:
        referer = "https://www.lgdisplay.com/"
    elif "lgensol.com" in url:
        referer = "https://www.lgensol.com/"
    elif "lguplus.com" in url:
        referer = "https://www.lguplus.com/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Referer": referer,
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
