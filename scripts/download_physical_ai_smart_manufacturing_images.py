#!/usr/bin/env python3
"""
Download source images for docs/02_physical_ai_smart_manufacturing.md.

Usage:
  python scripts/download_physical_ai_smart_manufacturing_images.py

The script downloads only original source images referenced by URL.
It does not generate or modify images.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import urlparse
import urllib.request
import urllib.error


MANIFEST = {
  "output_dir": "assets/images/02_physical_ai_smart_manufacturing",
  "images": [
    {
      "id": "lge_smart_factory_main",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/main-image-desktopmobile-ecsmart-464.png",
      "filename": "lge_smart_factory_main.png",
      "caption": "LG Smart Factory End-to-End Solutions를 설명하는 메인 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lge_smart_factory_end_to_end",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/Executive%20Corner%20Smart%20Factory%20Image%201.png",
      "filename": "lge_smart_factory_end_to_end.png",
      "caption": "Front Engineering, Intelligent Automation, AI-DX Operation, Lifecycle Services로 구성된 LG Smart Factory End-to-End Solutions.",
      "status": "confirmed"
    },
    {
      "id": "lge_tennessee_factory",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/Executive%20Corner%20Smart%20Factory%20Image%202.jpg",
      "filename": "lge_tennessee_factory.jpg",
      "caption": "LG Electronics Tennessee facility. 다운로드 시 timeout 가능성 확인 필요.",
      "status": "url_confirmed_but_timeout_possible"
    },
    {
      "id": "lge_tailored_to_industry",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/Executive%20Corner%20Smart%20Factory%20Image%203.png",
      "filename": "lge_tailored_to_industry.png",
      "caption": "Tailored to Your Industry 인포그래픽. 다운로드 시 timeout 가능성 확인 필요.",
      "status": "url_confirmed_but_timeout_possible"
    },
    {
      "id": "lge_smart_park_robot_arms",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/executive-corner-lg-electronics-on-smart-factory-success-end-to-end-solution-and-experience-across-the-full-manufacturing-lifecycle/Executive%20Corner%20Smart%20Factory%20Image%204.jpg",
      "filename": "lge_smart_park_robot_arms.jpg",
      "caption": "LG Smart Park 창원 생산 현장의 로봇 암.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_lighthouse",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_01.jpg",
      "filename": "lg_smart_park_lighthouse.jpg",
      "caption": "LG Smart Park가 WEF Lighthouse Factory로 선정되었음을 소개하는 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_digital_twin",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_02.jpg",
      "filename": "lg_smart_park_digital_twin.jpg",
      "caption": "Digital Twin 기술로 생산라인을 가상화하고 다양한 생산 시나리오를 시뮬레이션하는 개념 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_agv_conveyor",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_03.jpg",
      "filename": "lg_smart_park_agv_conveyor.jpg",
      "caption": "5G 기반 AGV와 overhead conveyor를 결합한 3차원 물류 자동화.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_pie_mavin_station",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_05.jpg",
      "filename": "lg_smart_park_pie_mavin_station.jpg",
      "caption": "PIE와 MAVIN 기반 검사·예지보전이 적용된 LG Smart Park 생산 셀.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_cloud_pie_mavin",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_06.jpg",
      "filename": "lg_smart_park_cloud_pie_mavin.jpg",
      "caption": "Cloud, IIoT, PIE, MAVIN, Edge Computing을 연결한 LG Smart Park의 AI 제조 플랫폼 개념.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_automation_line",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_08.jpg",
      "filename": "lg_smart_park_automation_line.jpg",
      "caption": "로봇과 자동화 설비가 결합된 LG Smart Park 자동 생산라인.",
      "status": "confirmed"
    },
    {
      "id": "lg_smart_park_exterior",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/lg-story/beyond-news/the-future-of-manufacturing-lighthouse-factory-lighting-the-way-ahead-lg-smart-park/LG-Smart-Park_10.jpg",
      "filename": "lg_smart_park_exterior.jpg",
      "caption": "LG Smart Park 창원 공장 전경.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_factova_iot_expo",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG CNS Newsroom",
      "source_url": "https://www.lgcns.com/en/newsroom/press/detail.manufacture-2605-1",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/uploads/2026/05/%EB%B6%81%EB%AF%B8%EC%97%91%EC%8A%A4%ED%8F%AC%EC%98%81%EB%AC%B8.jpg",
      "filename": "lgcns_factova_iot_expo.jpg",
      "caption": "IoT Tech Expo 2026에서 LG CNS가 Factova 기반 AI smart factory solution을 설명하는 모습.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_skild_ai_hq",
      "theme": "physical_ai_smart_manufacturing",
      "source": "LG CNS Newsroom",
      "source_url": "https://www.lgcns.com/kr/newsroom/press/detail.66074",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/newsroom/MAIN-scaled-e1749113375930-1920x1436.jpg",
      "filename": "lgcns_skild_ai_hq.jpg",
      "caption": "Skild AI 협력 보도자료에 포함된 LG CNS 본사 이미지. 로봇 솔루션 자체 이미지는 원문에 제공되지 않음.",
      "status": "confirmed_but_generic"
    }
  ]
}


def download_file(url: str, dest: Path, timeout: int = 30) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Referer": "https://www.lg.com/",
    }

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
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
        filename = item["filename"]
        dest = out_dir / filename

        print(f"Downloading {item['id']} -> {dest}")
        result = download_file(url, dest)
        result.update({
            "id": item["id"],
            "source": item["source"],
            "source_url": item["source_url"],
            "image_url": url,
            "filename": filename,
            "caption": item["caption"],
            "status": item["status"],
        })
        results.append(result)

        # Be polite to source servers.
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
