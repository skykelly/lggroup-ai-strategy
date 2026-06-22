#!/usr/bin/env python3
"""
Download source images for docs/05_ai_for_science_bio_materials_battery.md.

Usage:
  python scripts/download_ai_for_science_bio_materials_battery_images.py

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
  "output_dir": "assets/images/05_ai_for_science_bio_materials_battery",
  "images": [
    {
      "id": "exaone_journey_timeline",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG AI Research EXAONE",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_journey_pc.png",
      "filename": "exaone_journey_timeline.png",
      "caption": "EXAONE Journey timeline. EXAONE 4.5까지 이어진 LG AI Research의 모델 고도화 흐름.",
      "status": "confirmed"
    },
    {
      "id": "exaone_logo",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG AI Research EXAONE",
      "source_url": "https://www.lgresearch.ai/exaone/",
      "image_url": "https://www.lgresearch.ai/img/solution/exaone_logo.png",
      "filename": "exaone_logo.png",
      "caption": "EXAONE logo. AI for Science의 기반 모델·솔루션 계층을 대표하는 이미지.",
      "status": "confirmed"
    },
    {
      "id": "exaone_discovery_operation",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "Financial News / LG AI Research",
      "source_url": "https://en.fnnews.com/news/202602031623047760",
      "image_url": "https://image.fnnews.com/resource/media/image/2026/02/03/202602031018422799_l.jpg",
      "filename": "exaone_discovery_operation.jpg",
      "caption": "EXAONE Discovery in operation. 논문·특허·분자구조 등 비정형 데이터를 활용해 후보물질 탐색과 실험 설계를 지원하는 예시.",
      "status": "confirmed"
    },
    {
      "id": "exaone_discovery_digitaltoday_gif",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "Digital Today / LG AI Research",
      "source_url": "https://www.digitaltoday.co.kr/en/view/2921/lg-ai-research-registers-gateway-patent-for-ai-to-aid-new-materials-and-drug-development",
      "image_url": "https://cdn.digitaltoday.co.kr/news/photo/202602/626597_578710_2823.gif",
      "filename": "exaone_discovery_digitaltoday.gif",
      "caption": "EXAONE Discovery image from Digital Today. 일부 fetch 환경에서 400 응답 가능성이 있어 다운로드 확인 필요.",
      "status": "url_confirmed_but_fetch_400_possible"
    },
    {
      "id": "lgai_research_logo",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG AI Research",
      "source_url": "https://www.lgresearch.ai/ourwork/research?tab=PE",
      "image_url": "https://www.lgresearch.ai/img/common/logo_en.png",
      "filename": "lgai_research_logo.png",
      "caption": "LG AI Research logo. Bio Intelligence, Materials Intelligence, Advanced Agent 연구영역의 주체.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_life_science_sales_graph",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Life Science",
      "source_url": "https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US",
      "image_url": "https://www.lgchem.com/asset/images/common/company/img_life_science_graph.png",
      "filename": "lgchem_life_science_sales_graph.png",
      "caption": "LG Chem Life Science sales graph. 생명과학 사업의 중장기 성장축을 보여주는 공식 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_life_science_primary_care",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Life Science",
      "source_url": "https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US",
      "image_url": "https://www.lgchem.com/asset/images/common/company/thumb_business401.jpg",
      "filename": "lgchem_life_science_primary_care.jpg",
      "caption": "LG Chem Life Science Primary Care division image. AI 신약개발의 실험·검증 필드와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_life_science_specialty_care",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Life Science",
      "source_url": "https://www.lgchem.com/company/company-information/business-domain/biology?lang=en_US",
      "image_url": "https://www.lgchem.com/asset/images/common/company/thumb_business402.jpg",
      "filename": "lgchem_life_science_specialty_care.jpg",
      "caption": "LG Chem Life Science Specialty Care division image. 바이오·신약 R&D 자산과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_open_innovation_energy_materials",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Open Innovation",
      "source_url": "https://www.lgchem.com/company/research-and-development/open-innovation?lang=en_US",
      "image_url": "https://www.lgchem.com/asset/images/common/company/research/innovation-energy.jpg",
      "filename": "lgchem_open_innovation_energy_materials.jpg",
      "caption": "Energy Transition & Sustainable Materials. 배터리·재생에너지 소재 오픈이노베이션 방향과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_cathode_material_main",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Cathode Material",
      "source_url": "https://www.lgchem.com/product-detail/cathode-material?lang=en_US",
      "image_url": "https://www.lgchem.com/upload/file/product/66/global/0_anode_kor.png",
      "filename": "lgchem_cathode_material_main.png",
      "caption": "LG Chem Cathode Material page hero image. 배터리 소재 탐색·검증의 핵심 적용 영역.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_cathode_production_plan",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Cathode Material",
      "source_url": "https://www.lgchem.com/product-detail/cathode-material?lang=en_US",
      "image_url": "https://www.lgchem.com/upload/file/product/66/global/chart_pc_e.png",
      "filename": "lgchem_cathode_production_plan.png",
      "caption": "LG Chem Cathode Material Production Plan by 2030. 배터리 소재 포트폴리오와 생산능력 확대 방향.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_cathode_mobile_application",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Cathode Material",
      "source_url": "https://www.lgchem.com/product-detail/cathode-material?lang=en_US",
      "image_url": "https://www.lgchem.com/upload/file/product/66/global/1_Cathode_kor.png",
      "filename": "lgchem_cathode_mobile_application.png",
      "caption": "Cathode material application image: mobile batteries.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_cathode_auto_application",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Cathode Material",
      "source_url": "https://www.lgchem.com/product-detail/cathode-material?lang=en_US",
      "image_url": "https://www.lgchem.com/upload/file/product/66/global/2_Cathode_kor.png",
      "filename": "lgchem_cathode_auto_application.png",
      "caption": "Cathode material application image: automotive batteries.",
      "status": "confirmed"
    },
    {
      "id": "lgchem_cathode_ess_application",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Chem Cathode Material",
      "source_url": "https://www.lgchem.com/product-detail/cathode-material?lang=en_US",
      "image_url": "https://www.lgchem.com/upload/file/product/66/global/3_Cathode_kor.png",
      "filename": "lgchem_cathode_ess_application.png",
      "caption": "Cathode material application image: ESS batteries.",
      "status": "confirmed"
    },
    {
      "id": "lgensol_battery_technology_roadmap_mid_nickel",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Energy Solution Battery Inside",
      "source_url": "https://inside.lgensol.com/en/2025/06/lg-energy-solutions-battery-technology-roadmap-creating-customer-value-through-material-and-process-innovation/",
      "image_url": "https://inside.lgensol.com/wp-content/uploads/2025/06/6_%EC%86%8C%EC%9E%AC%EC%99%80-%EA%B3%B5%EC%A0%95-%ED%98%81%EC%8B%A0%EC%9D%84-%ED%86%B5%ED%95%B4-%EA%B3%A0%EA%B0%9D%EA%B0%80%EC%B9%98%EB%A5%BC-%EC%8B%A4%ED%98%84%ED%95%98%EB%8A%94-LG%EC%97%90%EB%84%88%EC%A7%80%EC%86%94%EB%A3%A8%EC%85%98-%EB%B0%B0%ED%84%B0%EB%A6%AC-%EA%B8%B0%EC%88%A0-%EB%A1%9C%EB%93%9C%EB%A7%B5.png",
      "filename": "lgensol_battery_technology_roadmap_mid_nickel.png",
      "caption": "LG Energy Solution battery technology roadmap presentation. 소재·공정 혁신과 AI-driven materials research 흐름.",
      "status": "confirmed"
    },
    {
      "id": "lgensol_dry_electrode_process",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Energy Solution Battery Inside",
      "source_url": "https://inside.lgensol.com/en/2025/06/lg-energy-solutions-battery-technology-roadmap-creating-customer-value-through-material-and-process-innovation/",
      "image_url": "https://inside.lgensol.com/wp-content/uploads/2025/06/8_%EC%86%8C%EC%9E%AC%EC%99%80-%EA%B3%B5%EC%A0%95-%ED%98%81%EC%8B%A0%EC%9D%84-%ED%86%B5%ED%95%B4-%EA%B3%A0%EA%B0%9D%EA%B0%80%EC%B9%98%EB%A5%BC-%EC%8B%A4%ED%98%84%ED%95%98%EB%8A%94-LG%EC%97%90%EB%84%88%EC%A7%80%EC%86%94%EB%A3%A8%EC%85%98-%EB%B0%B0%ED%84%B0%EB%A6%AC-%EA%B8%B0%EC%88%A0-%EB%A1%9C%EB%93%9C%EB%A7%B5.png",
      "filename": "lgensol_dry_electrode_process.png",
      "caption": "Wet electrode process vs dry electrode process. 배터리 소재·공정 혁신의 대표 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lgensol_genai_patent_chatbot",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "LG Energy Solution Battery Inside",
      "source_url": "https://inside.lgensol.com/en/2025/06/genai-transforming-the-present-and-future-of-the-battery-industry/",
      "image_url": "https://inside.lgensol.com/wp-content/uploads/2025/05/9_%EC%83%9D%EC%84%B1%ED%98%95-AI%EB%A1%9C-%EB%B0%94%EA%BE%B8%EB%8A%94-%EB%B0%B0%ED%84%B0%EB%A6%AC-%EC%82%B0%EC%97%85%EC%9D%98-%ED%98%84%EC%9E%AC%EC%99%80-%EB%AF%B8%EB%9E%98-1.png",
      "filename": "lgensol_genai_patent_chatbot.png",
      "caption": "LG Energy Solution GenAI in battery industry. 특허 검색·요약, 배터리 지식 AI 챗봇과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lghnh_bichup_nad_symposium",
      "theme": "ai_for_science_bio_materials_battery",
      "source": "Maeil Business News / LG Household & Health Care",
      "source_url": "https://www.mk.co.kr/en/special-edition/11271183",
      "image_url": "https://wimg.mk.co.kr/news/cms/202503/24/20250324_01110229000002_L01.jpg",
      "filename": "lghnh_bichup_nad_symposium.jpg",
      "caption": "LG Household & Health Care The Whoo Bichup NAD+ Symposium. AI 기반 화장품 효능 소재 개발 사례와 연결된다.",
      "status": "confirmed"
    }
  ]
}


def get_referer(url: str) -> str:
    if "lgresearch.ai" in url:
        return "https://www.lgresearch.ai/"
    if "fnnews.com" in url:
        return "https://en.fnnews.com/"
    if "digitaltoday.co.kr" in url:
        return "https://www.digitaltoday.co.kr/"
    if "lgchem.com" in url:
        return "https://www.lgchem.com/"
    if "lgensol.com" in url:
        return "https://inside.lgensol.com/"
    if "mk.co.kr" in url:
        return "https://www.mk.co.kr/"
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
