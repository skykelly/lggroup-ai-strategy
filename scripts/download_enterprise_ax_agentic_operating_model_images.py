#!/usr/bin/env python3
"""
Download source images for docs/04_enterprise_ax_agentic_operating_model.md.

Usage:
  python scripts/download_enterprise_ax_agentic_operating_model_images.py

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
  "output_dir": "assets/images/04_enterprise_ax_agentic_operating_model",
  "images": [
    {
      "id": "lgcorp_silicon_valley_palantir_signing",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "Digital Today / LG CNS photo",
      "source_url": "https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion",
      "image_url": "https://cdn.digitaltoday.co.kr/news/photo/202603/640006_590746_75.jpg",
      "filename": "lgcns_palantir_signing.jpg",
      "caption": "LG CNS CEO Hyun Shin-gyun and Palantir CEO Alex Karp at the strategic partnership signing ceremony. LG그룹 AX의 온톨로지·의사결정 체계 벤치마킹과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lge_ceo_strategy_press_conference",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG Electronics Newsroom",
      "source_url": "https://www.lg.com/global/newsroom/news/corporate/lg-electronics-ceo-sets-strategic-direction-for-profit-driven-growth-prioritizing-speed-and-action/",
      "image_url": "https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/corporate/lg-electronics-ceo-sets-strategic-direction-for-profit-driven-growth-prioritizing-speed-and-action/press-setting-image-desktoptablet-koreapressconference-1440.png",
      "filename": "lge_ceo_strategy_press_conference.png",
      "caption": "LG Electronics CEO Lyu Jae-cheol speaks at a press briefing. AX를 통한 end-to-end AI-driven operations, speed, productivity, execution 방향과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_platform_service_development",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Platform",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-platform",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_1.png",
      "filename": "lgcns_ax_platform_service_development.png",
      "caption": "LG CNS AX Platform: faster, simpler AI service development. 기업 AI 서비스 개발·배포 기반을 설명하는 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_platform_operations",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Platform",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-platform",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_2.png",
      "filename": "lgcns_ax_platform_operations.png",
      "caption": "LG CNS AX Platform: AI service operations, monitoring, LLMOps. 운영·모니터링·거버넌스 레이어와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_platform_emerging_tech",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Platform",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-platform",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_3.png",
      "filename": "lgcns_ax_platform_emerging_tech.png",
      "caption": "LG CNS AX Platform: RAG, multimodal, vector DB, LLMOps 등 emerging technologies를 기업 AX에 적용하는 구조.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_knowledge_data_pipeline",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Platform",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-platform",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_4.png",
      "filename": "lgcns_knowledge_data_pipeline.png",
      "caption": "Knowledge Data pipeline: ingestion, processing, transformation, knowledge base. 전사 데이터·지식화·RAG 체계와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_monitoring_governance",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Platform",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-platform",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_5.png",
      "filename": "lgcns_monitoring_governance.png",
      "caption": "Monitoring & Governance. 보안, 권한, 거버넌스 정책 운영을 설명하는 이미지.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_llmops_lifecycle",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Platform",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-platform",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ai-platform/AXplatform_webimage_16.png",
      "filename": "lgcns_llmops_lifecycle.png",
      "caption": "Enterprise-fit AI lifecycle management: learning, monitoring, evaluation, retraining. 운영형 AI의 지속 개선 루프와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_consulting_master_plan",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/aicc/EN_027_AICC_AI%20%E1%84%89%E1%85%A1%E1%86%BC%E1%84%83%E1%85%A1%E1%86%B7%E1%84%87%E1%85%A9%E1%86%BA_AICC_%20cloud%E1%84%80%E1%85%B5%E1%84%87%E1%85%A1%E1%86%AB%20%E1%84%91%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A2%E1%86%BA%E1%84%91%E1%85%A9%E1%86%B7%20%E1%84%80%E1%85%AE%E1%84%89%E1%85%A5%E1%86%BC.png",
      "filename": "lgcns_ax_consulting_master_plan.png",
      "caption": "LG CNS AX Consulting의 세 축: AI Transformation Master Plan, AI PI & Service Design, AI Engineering Consulting.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_strategy_consulting",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ax-consulting/AXConsulting1_webimage_1.png",
      "filename": "lgcns_ax_strategy_consulting.png",
      "caption": "AX Strategy Consulting. C-level 의사결정과 AI adoption roadmap 수립을 지원하는 영역.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_discovery",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ax-consulting/AXConsulting1_webimage_3.png",
      "filename": "lgcns_ax_discovery.png",
      "caption": "AX Discovery. 업무 pain point와 AI use case를 발굴해 전사 AX roadmap으로 연결하는 영역.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_process_innovation",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ax-consulting/AXConsulting2_webimage_1.png",
      "filename": "lgcns_process_innovation.png",
      "caption": "AX PI: AI-Based Process Innovation. 업무 프로세스 전체를 데이터 기반으로 분석·재설계하는 접근.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_service_innovation",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ax-consulting/AXConsulting2_webimage_3.png",
      "filename": "lgcns_service_innovation.png",
      "caption": "AX SAI: AI-Based Service & Application Innovation. Agentic AI 기반 서비스·업무 앱 설계와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ai_governance_consulting",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ax-consulting/AXConsulting3_webimage_3.png",
      "filename": "lgcns_ai_governance_consulting.png",
      "caption": "AI Governance Consulting. AI regulation, risk, explainability, governance framework와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ai_platform_architecture",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "LG CNS AX Consulting",
      "source_url": "https://www.lgcns.com/en/service/ai/ax-consulting",
      "image_url": "https://www.lgcns.com/content/dam/lgcns/images/service/ai/ax-consulting/AXConsulting3_webimage_6.png",
      "filename": "lgcns_ai_platform_architecture.png",
      "caption": "AI Platform Planning / Design. Agentic AI 플랫폼과 legacy IT 연계를 위한 architecture planning.",
      "status": "confirmed"
    },
    {
      "id": "lgdisplay_ai_transformation_plan",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "The Korea Times / LG Display courtesy",
      "source_url": "https://www.koreatimes.co.kr/business/tech-science/20250805/lg-display-eyes-30-improvement-in-productivity-through-ai",
      "image_url": "https://newsimg.koreatimes.co.kr/2025/08/05/73cc09fa-0b33-45a3-8292-b97ef345bfc5.png?w=728",
      "filename": "lgdisplay_ai_transformation_plan.png",
      "caption": "LG Display AI Transformation plan infographic. 개발, 제조, 사무 업무에서 생산성 개선을 설명한다.",
      "status": "confirmed"
    },
    {
      "id": "lgdisplay_hi_d_assistant",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "The Korea Times / LG Display courtesy",
      "source_url": "https://www.koreatimes.co.kr/business/tech-science/20250805/lg-display-eyes-30-improvement-in-productivity-through-ai",
      "image_url": "https://newsimg.koreatimes.co.kr/2025/08/05/6a6f1122-9cb0-466e-a68b-2929fec8c039.jpg?w=728",
      "filename": "lgdisplay_hi_d_assistant.jpg",
      "caption": "LG Display Hi-D AI assistant demonstration. 지식검색, 실시간 통역, 회의록 생성 등 사무 AX와 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgenergy_ceo_ax_productivity",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "Maeil Business News",
      "source_url": "https://www.mk.co.kr/en/business/12015637",
      "image_url": "https://wimg.mk.co.kr/news/cms/202604/14/20260414_01160113000002_L00.jpg",
      "filename": "lgenergy_ceo_ax_productivity.jpg",
      "caption": "LG Energy Solution CEO Kim Dong-myung. AX 기반 생산성 개선과 AI Governance Committee 방향과 연결된다.",
      "status": "confirmed"
    },
    {
      "id": "lgcns_ax_fair_2026",
      "theme": "enterprise_ax_agentic_operating_model",
      "source": "전자신문",
      "source_url": "https://www.etnews.com/20260527000356",
      "image_url": "https://img.etnews.com/news/article/2026/05/27/news-p.v1.20260527.bc5ee2f056434e02acf50a51ee87dc39_P1.jpg",
      "filename": "lgcns_ax_fair_2026.jpg",
      "caption": "LG CNS AX Fair 2026 발표 장면. AgenticWorks, AXThink, enterprise AI 실행 전략과 연결된다.",
      "status": "confirmed"
    }
  ]
}


def get_referer(url: str) -> str:
    if "lgcns.com" in url:
        return "https://www.lgcns.com/"
    if "lg.com" in url:
        return "https://www.lg.com/"
    if "digitaltoday.co.kr" in url:
        return "https://www.digitaltoday.co.kr/"
    if "koreatimes.co.kr" in url:
        return "https://www.koreatimes.co.kr/"
    if "mk.co.kr" in url:
        return "https://www.mk.co.kr/"
    if "etnews.com" in url:
        return "https://www.etnews.com/"
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
