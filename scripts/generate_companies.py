#!/usr/bin/env python3
"""Generate Company entities from docs/topics metadata and curated Wiki roles."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
COMPANIES_DIR = ROOT / "companies"
PARTNERS_DIR = COMPANIES_DIR / "partners"
INVENTORY_PATH = ROOT / "data" / "image_inventory.json"

THEMES = {
    "ai_data_center_infra": ("AI Data Center / Infra", "docs/01_ai_data_center_infra"),
    "physical_ai_smart_manufacturing": ("Physical AI / Smart Manufacturing", "docs/02_physical_ai_smart_manufacturing"),
    "ai_mobility_sdv_aidv": ("AI Mobility / SDV·AIDV", "docs/03_ai_mobility_sdv_aidv"),
    "enterprise_ax_agentic_operating_model": ("Enterprise AX / Agentic Operating Model", "docs/04_enterprise_ax_agentic_operating_model"),
    "ai_for_science_bio_materials_battery": ("AI for Science / Bio / Materials / Battery", "docs/05_ai_for_science_bio_materials_battery"),
    "global_ai_alliance_open_innovation": ("Global AI Alliance / Open Innovation", "docs/06_global_ai_alliance_open_innovation"),
}

LG_AFFILIATES = {
    "lg-corp",
    "lg-ai-research",
    "lg-uplus",
    "lg-cns",
    "lg-electronics",
    "lg-energy-solution",
    "lg-display",
    "lg-innotek",
    "lg-chem",
    "lg-household-health-care",
    "lg-technology-ventures",
}

PROFILES = {
    "lg-corp": {
        "title": "LG Corp.",
        "summary": "그룹 차원의 AI 사업 포트폴리오, One LG 역할 조정, 글로벌 제휴와 기술 내부화 원칙을 설계하는 조정자다.",
        "image": "lg_nvidia_map_koo_huang_prn",
        "assets": ["그룹 포트폴리오 조정권", "NVIDIA·Palantir 등 전략 파트너 접점", "계열사 간 One LG 패키지 설계"],
        "roles": {
            "ai_data_center_infra": "AIDC·냉각·전력·DBO 자산을 One LG 인프라 제안으로 조정",
            "enterprise_ax_agentic_operating_model": "그룹 공통 ontology·AI governance·성과관리 원칙 설정",
            "global_ai_alliance_open_innovation": "글로벌 파트너십 의제와 기술 내부화 우선순위 조정",
        },
        "sources": ["src_lg_nvidia_map_20260608", "src_lgcorp_silicon_valley_20260407"],
    },
    "lg-ai-research": {
        "title": "LG AI Research",
        "summary": "EXAONE 계열 모델과 산업·과학 특화 AI를 개발하고, 그룹 데이터를 모델·Agent·Discovery 제품으로 전환하는 핵심 AI 연구 조직이다.",
        "image": "exaone_journey_timeline",
        "assets": ["EXAONE·K-EXAONE", "EXAONE Discovery", "Bio·Materials·Physical Intelligence 연구역량"],
        "roles": {
            "ai_data_center_infra": "대규모 학습·추론의 anchor workload와 모델 운영 요구 제공",
            "physical_ai_smart_manufacturing": "제조·로봇 데이터를 위한 Physical Intelligence 모델 개발",
            "enterprise_ax_agentic_operating_model": "EXAONE 기반 기업 Agent와 산업 특화 모델 제공",
            "ai_for_science_bio_materials_battery": "후보 탐색·실험 설계·소재 예측을 위한 AI Co-Scientist 기반 제공",
            "global_ai_alliance_open_innovation": "자체 모델과 외부 AI stack을 조합하는 hybrid AI 역량 담당",
        },
        "sources": ["src_lgai_exaone", "src_lgai_materials_intelligence", "src_lgai_exaone_discovery_patent_20260203", "src_lgai_dd_pharmatech_20260617"],
    },
    "lg-uplus": {
        "title": "LG U+",
        "summary": "AIDC 운영, 네트워크, GPU Cloud와 V2X·정밀지도·관제 역량을 통해 AI 인프라와 모빌리티의 운영 레이어를 담당한다.",
        "image": "img_lguplus_paju_pulse_01",
        "assets": ["파주 hyperscale AIDC", "데이터센터·네트워크 운영", "V2X·Dynamic Map·자율주행 관제"],
        "roles": {
            "ai_data_center_infra": "AIDC operator로서 고밀도 GPU·전력·냉각·SLA 운영",
            "ai_mobility_sdv_aidv": "5G/V2X, 정밀지도, 자율주행 관제와 edge connectivity 제공",
            "global_ai_alliance_open_innovation": "AI 인프라 파트너 stack을 국내 운영 서비스로 상품화",
        },
        "sources": ["src_lguplus_paju_aidc_20260607", "src_pulse_lguplus_paju_aidc_20260608", "src_lguplus_autonomous_driving"],
    },
    "lg-cns": {
        "title": "LG CNS",
        "summary": "데이터센터 DBO, Factova 제조 AX, AX Platform, LLMOps·governance를 통합해 그룹 내부 자산을 외부 고객용 AI 사업으로 전환하는 실행 사업자다.",
        "image": "lgcns_ax_platform_service_development",
        "assets": ["데이터센터 DBO와 AI Box", "Factova", "AX Platform·AgenticWorks·LLMOps"],
        "roles": {
            "ai_data_center_infra": "데이터센터 설계·구축·운영과 모듈러 AI Box 제공",
            "physical_ai_smart_manufacturing": "Factova 기반 제조 데이터·설비·로봇 통합과 외부 SI",
            "enterprise_ax_agentic_operating_model": "ontology, Agent workflow, LLMOps, governance 구현",
            "ai_for_science_bio_materials_battery": "ELN/LIMS·문서·실험 데이터 플랫폼과 workflow 운영",
            "global_ai_alliance_open_innovation": "파트너 기술을 고객별 산업 AX 제품으로 통합·전달",
        },
        "sources": ["src_lgcns_ai_box_20260304", "src_lgcns_factova_20260519", "src_lgcns_ax_platform", "src_lgcns_palantir_20260312"],
    },
    "lg-electronics": {
        "title": "LG Electronics",
        "summary": "AI 데이터센터 냉각, 글로벌 제조 현장, Smart Factory Solutions와 차량용 AI 경험을 보유한 Physical AI의 핵심 실행 계열사다.",
        "image": "img_koreatimes_cdu_01",
        "assets": ["CDU·DTC·Chiller·CRAH 냉각 stack", "LG Smart Park와 글로벌 제조 데이터", "VS 사업과 AI Cabin"],
        "roles": {
            "ai_data_center_infra": "고밀도 AI 데이터센터의 냉각·열관리와 운영 제어 제공",
            "physical_ai_smart_manufacturing": "제조 현장과 Smart Factory Solutions의 product owner 후보",
            "ai_mobility_sdv_aidv": "IVI·AI Cabin·차량용 experience layer 제공",
            "enterprise_ax_agentic_operating_model": "개발·제조·SCM·판매 workflow의 회사 단위 AX 적용",
        },
        "sources": ["src_lge_dcw_20260421", "src_lge_smart_factory_20260414", "src_lge_ai_in_vehicle_20251217", "src_lge_strategy_ax_20260108"],
    },
    "lg-energy-solution": {
        "title": "LG Energy Solution",
        "summary": "ESS·UPS 전력 안정화, BMS/BMTS와 배터리 SW, 배터리 소재·공정 R&D 데이터를 연결하는 에너지 지능 사업자다.",
        "image": "lgensol_baround_core_values",
        "assets": ["ESS·UPS와 배터리 생산 역량", "B.around·BMS/BMTS·SDV BMS", "배터리 소재·공정·수명 데이터"],
        "roles": {
            "ai_data_center_infra": "ESS·UPS·battery management를 통한 AIDC 전력 안정화",
            "ai_mobility_sdv_aidv": "배터리 진단·안전·수명 예측 SW와 SDV 유통",
            "enterprise_ax_agentic_operating_model": "생산성·품질·R&D workflow의 AX와 governance 적용",
            "ai_for_science_bio_materials_battery": "소재·공정·안전·수명 실험 데이터와 검증 field 제공",
        },
        "sources": ["src_lgensol_ess_expansion_20260415", "src_lgensol_baround", "src_lgensol_sdverse_20260403", "src_lgensol_genai_battery_20250613"],
    },
    "lg-display": {
        "title": "LG Display",
        "summary": "차량용 OLED/HMI와 제조·개발 AX를 통해 AIDV의 시각 인터페이스와 산업 AI 적용 사례를 제공한다.",
        "image": "lgdisplay_ces2026_automotive_display",
        "assets": ["차량용 OLED·P2P·Slidable Display", "Hi-D AI assistant", "디스플레이 제조·품질 데이터"],
        "roles": {
            "physical_ai_smart_manufacturing": "디스플레이 제조 데이터와 품질·공정 AI 적용 field",
            "ai_mobility_sdv_aidv": "차량의 HMI·AI interface와 공간 경험 제공",
            "enterprise_ax_agentic_operating_model": "개발·제조·사무 생산성 AX와 adoption 사례 제공",
        },
        "sources": ["src_lgdisplay_ces2026_20260105", "src_lgdisplay_ai_productivity_20250805"],
    },
    "lg-innotek": {
        "title": "LG Innotek",
        "summary": "카메라·LiDAR·Radar·통신·조명·전동화 부품으로 AIDV와 Physical AI의 외부 인지·연결 레이어를 담당한다.",
        "image": "lginnotek_autonomous_sensor_fusion",
        "assets": ["카메라·LiDAR·Radar sensing", "5G·UWB 통신 모듈", "차량 조명·전동화 부품"],
        "roles": {
            "physical_ai_smart_manufacturing": "센서와 제조 데이터를 Physical AI 학습·검증 field로 제공",
            "ai_mobility_sdv_aidv": "자율주행 sensing·communication·lighting layer 공급",
            "global_ai_alliance_open_innovation": "NVIDIA·Applied Intuition 등 mobility stack과 부품 역량 연결",
        },
        "sources": ["src_lginnotek_ces2026_aidv_20260106", "src_lginnotek_ces2026_showcase", "src_lginnotek_applied_intuition_20260329"],
    },
    "lg-chem": {
        "title": "LG Chem",
        "summary": "생명과학·첨단소재·배터리 소재의 실험·검증·상용화 field를 제공해 AI for Science를 실제 R&D 성과로 연결한다.",
        "image": "lgchem_open_innovation_energy_materials",
        "assets": ["생명과학 R&D", "양극재 등 배터리 소재", "소재·화학 실험과 상용화 역량"],
        "roles": {
            "physical_ai_smart_manufacturing": "화학·소재 공정 데이터와 품질·안전 AI 적용 field",
            "enterprise_ax_agentic_operating_model": "One Agent와 연구·생산·사무 workflow AX 적용",
            "ai_for_science_bio_materials_battery": "AI 후보의 합성·실험·물성·임상·상용화 검증",
        },
        "sources": ["src_lgchem_life_science", "src_lgchem_open_innovation", "src_lgchem_cathode_material", "src_lgchem_one_agent_20260528"],
    },
    "lg-household-health-care": {
        "title": "LG Household & Health Care",
        "summary": "화장품 효능 소재와 안전성 평가·제품화 field를 통해 AI가 제안한 후보를 소비재로 상용화하는 역할을 맡는다.",
        "image": "lghnh_bichup_nad_symposium",
        "assets": ["화장품 소재·효능 데이터", "안전성·사용성 평가", "브랜드와 소비자 제품화 역량"],
        "roles": {
            "enterprise_ax_agentic_operating_model": "R&D·마케팅·고객·제품 지식을 연결하는 AX 적용 field",
            "ai_for_science_bio_materials_battery": "AI 기반 화장품 소재의 검증과 상용화",
        },
        "sources": ["src_lghnh_ai_cosmetic_ingredients_20250323"],
    },
    "lg-technology-ventures": {
        "title": "LG Technology Ventures",
        "summary": "AI·로봇·바이오·소재 스타트업에 대한 전략적 투자로 기술 옵션을 확보하는 CVC 축이다. 구체적 건별 역할은 추가 검증이 필요하다.",
        "image": "lg_nvidia_map_koo_huang_prn",
        "assets": ["글로벌 스타트업 탐색", "전략적 투자와 option portfolio", "계열사 사업부와 기술 연결"],
        "roles": {
            "ai_for_science_bio_materials_battery": "바이오·소재 AI 스타트업 option 확보 — 검증 필요",
            "global_ai_alliance_open_innovation": "CVC를 통한 외부 기술 탐색·투자·내부 연결",
        },
        "sources": [],
    },
    "nvidia": {
        "title": "NVIDIA",
        "summary": "GPU·AI 인프라, 로봇 시뮬레이션, Physical AI와 mobility stack을 제공하는 enabling partner다. LG 자산을 대체하는 주체가 아니라 가속 플랫폼으로 본다.",
        "image": "nvidia_lg_ai_factory_robot",
        "assets": ["GPU·AI Factory stack", "Omniverse·Isaac·Cosmos·GR00T", "DRIVE와 800V DC ecosystem"],
        "roles": {
            "ai_data_center_infra": "GPU·AI infrastructure와 차세대 전력 architecture 제공",
            "physical_ai_smart_manufacturing": "시뮬레이션·합성데이터·robot learning stack 제공",
            "ai_mobility_sdv_aidv": "DRIVE 기반 sensing·compute ecosystem 연결",
            "global_ai_alliance_open_innovation": "M.A.P. 협력의 full-stack enabling partner",
        },
        "sources": ["src_lg_nvidia_map_20260608", "src_nvidia_lg_ai_factory_20260607", "src_nvidia_800v_architecture_20250520"],
    },
    "skild-ai": {
        "title": "Skild AI",
        "summary": "범용 로봇 행동 모델을 제공해 LG CNS와 LG 제조 현장의 industrial humanoid·robot intelligence 실험을 가속하는 파트너다.",
        "image": "doc_02_skild_ai_series_c",
        "assets": ["Robotic Foundation Model", "범용 로봇 행동 학습", "산업 로봇 적용 기술"],
        "roles": {
            "physical_ai_smart_manufacturing": "RFM과 industrial humanoid intelligence 제공",
            "global_ai_alliance_open_innovation": "LG CNS가 Physical AI 사업을 빠르게 외부화하도록 지원",
        },
        "sources": ["src_lgcns_skild_ai_20250616", "src_lgcns_skild_ai_20250605"],
    },
    "palantir": {
        "title": "Palantir",
        "summary": "Foundry·AIP와 FDE 방식을 통해 enterprise ontology와 decision intelligence의 벤치마크를 제공한다. Theme 4의 목적 자체가 아니라 파트너·참조 architecture다.",
        "image": "lgcorp_silicon_valley_palantir_signing",
        "assets": ["Foundry", "AIP", "FDE 기반 산업 적용 방식"],
        "roles": {
            "enterprise_ax_agentic_operating_model": "기업 객체·관계·action을 연결하는 ontology 기반 운영 벤치마크",
            "global_ai_alliance_open_innovation": "LG CNS와 산업별 AX 공동 사업·기술 이전 경로 제공",
        },
        "sources": ["src_lgcorp_silicon_valley_20260407", "src_lgcns_palantir_20260312"],
    },
    "qualcomm": {
        "title": "Qualcomm",
        "summary": "Snapdragon Digital Chassis와 SoC 기반 환경에서 LG에너지솔루션의 배터리 진단·제어 SW를 차량 compute layer에 연결하는 파트너다.",
        "image": "lgensol_sdv_bms",
        "assets": ["Snapdragon Digital Chassis", "차량용 SoC·edge AI", "SDV ecosystem"],
        "roles": {
            "ai_mobility_sdv_aidv": "배터리 SW와 차량용 HPC·SoC의 통합",
            "global_ai_alliance_open_innovation": "LGES battery intelligence의 글로벌 SDV 적용 경로 제공",
        },
        "sources": ["src_lgensol_qualcomm_bms_20241223", "src_lgensol_qualcomm_20240310"],
    },
    "sdverse": {
        "title": "SDVerse",
        "summary": "LG에너지솔루션의 배터리 SW를 OEM·Tier·개발자가 탐색하고 도입할 수 있게 하는 automotive software marketplace 파트너다.",
        "image": "lgensol_baround_core_values",
        "assets": ["Automotive software marketplace", "OEM·supplier software 유통 접점", "SDV 생태계 연결"],
        "roles": {
            "ai_mobility_sdv_aidv": "배터리 SW의 거래·통합·배포 채널 제공",
            "global_ai_alliance_open_innovation": "하드웨어 중심 배터리 사업을 software ecosystem으로 확장",
        },
        "sources": ["src_lgensol_sdverse_20260403"],
    },
    "dd-pharmatech": {
        "title": "D&D Pharmatech",
        "summary": "AI가 제안한 신약 후보를 실제 합성·평가·개발로 연결하고 결과를 다시 모델에 피드백하는 wet-lab validation 파트너다.",
        "image": "exaone_discovery_operation",
        "assets": ["신약 후보 합성·평가", "전임상·임상 개발 경험", "실험 피드백 데이터"],
        "roles": {
            "ai_for_science_bio_materials_battery": "EXAONE Discovery 후보의 wet-lab 검증과 closed-loop R&D",
            "global_ai_alliance_open_innovation": "AI 모델과 실제 신약개발 실행을 연결",
        },
        "sources": ["src_lgai_dd_pharmatech_20260617"],
    },
    "sinar-mas-group": {
        "title": "Sinar Mas Group",
        "summary": "인도네시아 AI 데이터센터 구축과 One LG 인프라 패키지의 해외 적용 후보로 계획 문서에 포함된 파트너다. docs/topics의 직접 근거와 구체적 계약 범위는 추가 검증이 필요하다.",
        "image": "img_lguplus_paju_pulse_01",
        "assets": ["인도네시아 사업 기반", "AI 데이터센터 수요·부지·고객 접점 가능성", "One LG Solution 해외 적용 후보"],
        "roles": {
            "ai_data_center_infra": "LG CNS·LG전자·LG에너지솔루션 인프라 package의 해외 적용 파트너 후보 — 검증 필요",
            "global_ai_alliance_open_innovation": "동남아 AI 인프라 사업 확장을 위한 현지 사업 접점 — 검증 필요",
        },
        "sources": ["src_sinar_mas_official"],
    },
    "applied-intuition": {
        "title": "Applied Intuition",
        "summary": "자율주행·차량 소프트웨어 시뮬레이션을 통해 LG이노텍 센서·부품의 가상 검증과 AIDV 개발 workflow를 지원하는 파트너로 다뤄진다.",
        "image": "lginnotek_autonomous_sensor_fusion",
        "assets": ["Autonomy simulation", "Vehicle software validation", "가상 센서·주행 검증"],
        "roles": {
            "physical_ai_smart_manufacturing": "센서·자율 시스템의 simulation·validation workflow 지원",
            "ai_mobility_sdv_aidv": "LG이노텍 mobility component의 가상 검증과 OEM 개발 연계",
        },
        "sources": ["src_lginnotek_applied_intuition_20260329"],
    },
    "microsoft": {
        "title": "Microsoft",
        "summary": "AI Cloud와 enterprise platform 관점에서 LG의 AI 인프라·AX 사업이 연동하거나 경쟁할 수 있는 글로벌 사업자다. 현재 docs의 구체적 협력 범위는 추가 검증이 필요하다.",
        "image": "img_lgcns_ai_box_campus_01",
        "assets": ["Azure AI·Cloud ecosystem", "Enterprise AI platform", "글로벌 데이터센터 운영 역량"],
        "roles": {
            "ai_data_center_infra": "GPU Cloud·enterprise workload 연계 또는 경쟁 benchmark — 검증 필요",
            "enterprise_ax_agentic_operating_model": "기업 AI·Cloud architecture의 글로벌 benchmark — 검증 필요",
        },
        "sources": ["src_microsoft_datacenter_sustainability"],
    },
    "ls-electric": {
        "title": "LS ELECTRIC",
        "summary": "AI 데이터센터의 수배전·전력변환·전력관리 stack과 연결 가능한 국내 전력 인프라 사업자로 문서에 포함돼 있다. LG와의 구체적 역할은 추가 검증이 필요하다.",
        "image": "nvidia_800v_architecture",
        "assets": ["수배전·전력기기", "전력변환·에너지 관리", "데이터센터 전력 infrastructure"],
        "roles": {
            "ai_data_center_infra": "AIDC 전력 공급·배전·변환 layer의 협력 또는 ecosystem 후보 — 검증 필요",
        },
        "sources": ["src_ls_electric_official"],
    },
    "ls-cable-system": {
        "title": "LS Cable & System",
        "summary": "고전력 AI 데이터센터의 케이블·전력망 연결 layer와 연관된 인프라 사업자로 문서에 포함돼 있다. 직접 협력 근거는 추가 검증이 필요하다.",
        "image": "nvidia_800v_architecture",
        "assets": ["전력 케이블", "고전압·직류 전력망 연결", "대규모 인프라 구축 역량"],
        "roles": {
            "ai_data_center_infra": "AIDC 전력망·배선 infrastructure 후보 — 검증 필요",
        },
        "sources": ["src_ls_cable_system_official"],
    },
    "grc": {
        "title": "GRC",
        "summary": "고밀도 AI 서버의 immersion cooling과 연결되는 냉각 전문 파트너 후보로 문서에 포함돼 있다. LG전자 냉각 portfolio와의 구체적 관계는 추가 검증이 필요하다.",
        "image": "img_koreatimes_cdu_01",
        "assets": ["Immersion cooling 기술", "고밀도 서버 열관리", "데이터센터 냉각 운영 경험"],
        "roles": {
            "ai_data_center_infra": "액침냉각 기술·운영 benchmark 또는 협력 후보 — 검증 필요",
        },
        "sources": ["src_grc_immersion_cooling"],
    },
    "sk-enmove": {
        "title": "SK Enmove",
        "summary": "데이터센터 액침냉각 유체와 열관리 ecosystem에 연결되는 국내 파트너·경쟁 사업자 후보로 문서에 포함돼 있다. 직접 협력 범위는 추가 검증이 필요하다.",
        "image": "img_koreatimes_cdu_01",
        "assets": ["열관리 유체", "Immersion cooling ecosystem", "에너지 효율 솔루션"],
        "roles": {
            "ai_data_center_infra": "액침냉각 fluid와 열관리 value chain의 협력·경쟁 후보 — 검증 필요",
        },
        "sources": ["src_sk_enmove_official"],
    },
    "vanderbilt-university-medical-center": {
        "title": "Vanderbilt University Medical Center",
        "summary": "바이오·의료 연구 데이터와 임상 검증 관점에서 AI for Science 협력 가능성을 제공하는 연구기관으로 문서에 포함돼 있다. 구체적 LG 협력 근거는 추가 검증이 필요하다.",
        "image": "lgchem_life_science_primary_care",
        "assets": ["의료·임상 연구 역량", "바이오 데이터와 validation field", "연구자·병원 network"],
        "roles": {
            "ai_for_science_bio_materials_battery": "AI 후보·바이오 연구의 임상·의료 validation 후보 — 검증 필요",
        },
        "sources": ["src_vumc_research"],
    },
}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    raw = text.split("---", 2)[1]
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        repaired = []
        for line in raw.splitlines():
            match = re.match(r"^(title):\s*(.+)$", line)
            if match and ":" in match.group(2) and not match.group(2).startswith(("'", '"')):
                line = f"{match.group(1)}: {json.dumps(match.group(2), ensure_ascii=False)}"
            repaired.append(line)
        return yaml.safe_load("\n".join(repaired)) or {}


def load_relations() -> dict[str, dict]:
    relations = defaultdict(lambda: {"themes": [], "concepts": [], "sources": [], "topics": []})
    for folder in ("docs", "topics"):
        for path in sorted((ROOT / folder).glob("*.md")):
            metadata = parse_frontmatter(path)
            companies = metadata.get("related_companies") or []
            themes = metadata.get("related_themes") or ([metadata.get("theme_id")] if metadata.get("theme_id") else [])
            for company in companies:
                for theme in themes:
                    if theme and theme not in relations[company]["themes"]:
                        relations[company]["themes"].append(theme)
                for concept in metadata.get("related_concepts") or []:
                    concept = "ai-data-center" if concept == "aidc" else "factory-ontology" if concept == "manufacturing-ontology" else concept
                    if concept not in relations[company]["concepts"]:
                        relations[company]["concepts"].append(concept)
                for source in metadata.get("source_ids") or []:
                    if source not in relations[company]["sources"]:
                        relations[company]["sources"].append(source)
                if folder == "topics":
                    relations[company]["topics"].append(
                        {
                            "id": metadata.get("id"),
                            "title": metadata.get("title") or metadata.get("question"),
                            "path": f"topics/{path.stem}",
                        }
                    )
    return relations


def yaml_frontmatter(data: dict) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000).strip()


def main() -> int:
    relations = load_relations()
    missing_profiles = sorted(set(relations) - set(PROFILES))
    if missing_profiles:
        raise RuntimeError(f"Missing profiles: {missing_profiles}")

    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    images = {item["image_id"]: item for item in inventory["images"] if item.get("status") == "downloaded"}
    COMPANIES_DIR.mkdir(parents=True, exist_ok=True)
    PARTNERS_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    image_usage = defaultdict(list)
    for company_id, profile in PROFILES.items():
        relation = relations.get(company_id, {"themes": [], "concepts": [], "sources": [], "topics": []})
        category = "lg_affiliate" if company_id in LG_AFFILIATES else "partner"
        themes = list(dict.fromkeys(list(profile["roles"]) + relation["themes"]))
        concepts = relation["concepts"][:12]
        sources = list(dict.fromkeys(profile["sources"] + relation["sources"]))[:12]
        topics = relation["topics"]
        image = images[profile["image"]]
        directory = COMPANIES_DIR if category == "lg_affiliate" else PARTNERS_DIR
        relative_path = (
            f"companies/{company_id}.md"
            if category == "lg_affiliate"
            else f"companies/partners/{company_id}.md"
        )
        image_usage[profile["image"]].append(relative_path)

        frontmatter = {
            "id": f"company_{company_id.replace('-', '_')}",
            "type": "company",
            "title": profile["title"],
            "category": category,
            "related_themes": themes,
            "related_topics": [topic["id"] for topic in topics if topic["id"]],
            "related_concepts": concepts,
            "source_ids": sources,
            "tags": [company_id, category.replace("_", "-")],
        }
        theme_rows = []
        for theme in themes:
            if theme not in THEMES:
                continue
            role = profile["roles"].get(theme, "관련 docs/topics에서 적용 가능성이 언급됨 — 역할 범위 검증 필요")
            evidence = ", ".join(f"`{source}`" for source in sources[:3]) if sources else "검증 필요"
            theme_rows.append(f"| [[{THEMES[theme][1]}|{THEMES[theme][0]}]] | {role} | {evidence} |")
        topic_rows = [
            f"| [[{topic['path']}|{topic['title']}]] | 이 회사의 역할·자산·파트너 의존도와 직접 연결 |"
            for topic in topics
        ] or ["| 직접 연결된 Topic 없음 | 추가 검증 필요 |"]
        concept_links = "\n".join(f"- [[concepts/{concept}]]" for concept in concepts) or "- 관련 Concept 보강 필요"
        source_links = "\n".join(f"- [[sources/{source}]]" for source in sources) or "- Source 보강 필요"
        assets = "\n".join(f"- {asset}" for asset in profile["assets"])
        source_note = "\n> Source 보강 필요: 직접 연결된 공개 source_id가 부족하다.\n" if not sources else ""
        markdown = f"""---
{yaml_frontmatter(frontmatter)}
---

# {profile['title']}

<figure>
  <img src="{image['local_path']}" alt="{profile['title']} 관련 이미지" style="max-width:100%; border-radius:8px;" />
  <figcaption>{image.get('caption') or profile['title'] + ' 관련 원본 이미지'}</figcaption>
</figure>

## 1. Role Summary

{profile['summary']}

## 2. Theme Participation

| Theme | Role | Evidence |
|---|---|---|
{chr(10).join(theme_rows)}

## 3. Topic Participation

| Topic | Why It Matters |
|---|---|
{chr(10).join(topic_rows)}

## 4. Key Assets

{assets}

## 5. Related Concepts

{concept_links}

## 6. Related Sources

{source_links}
{source_note}
## 7. Open Questions

- 이 회사가 lead해야 할 제품·서비스 단위와 다른 계열사 또는 파트너의 역할 경계는 무엇인가?
- PoC나 제휴 발표를 반복 가능한 매출·생산성·R&D 성과로 전환할 KPI는 무엇인가?
- 데이터, 모델, workflow와 고객 관계 중 반드시 내부에 축적해야 할 자산은 무엇인가?
"""
        (directory / f"{company_id}.md").write_text(markdown, encoding="utf-8")
        generated.append(
            {
                "id": company_id,
                "entity_id": frontmatter["id"],
                "title": profile["title"],
                "category": category,
                "related_themes": themes,
                "related_topics": frontmatter["related_topics"],
                "related_concepts": concepts,
                "source_ids": sources,
                "image_id": profile["image"],
                "image_path": image["local_path"],
                "path": relative_path,
            }
        )

    for item in inventory["images"]:
        additions = image_usage.get(item.get("image_id"), [])
        if additions:
            item["used_by"] = sorted(set((item.get("used_by") or []) + additions))
    INVENTORY_PATH.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "data" / "companies.json").write_text(
        json.dumps({"companies": generated}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    matrix = [
        "---",
        "id: theme_company_matrix",
        "type: matrix",
        "title: Theme-Company Matrix",
        "---",
        "",
        "# Theme-Company Matrix",
        "",
        "| Company | Category | Themes |",
        "|---|---|---|",
    ]
    partners = [
        "---",
        "id: partner_map",
        "type: index",
        "title: Partner Map",
        "---",
        "",
        "# Partner Map",
        "",
        "| Partner | Primary Role | Related Themes |",
        "|---|---|---|",
    ]
    for item in generated:
        link = (
            f"[[companies/{item['id']}|{item['title']}]]"
            if item["category"] == "lg_affiliate"
            else f"[[companies/partners/{item['id']}|{item['title']}]]"
        )
        matrix.append(
            f"| {link} | `{item['category']}` | "
            + ", ".join(f"`{theme}`" for theme in item["related_themes"])
            + " |"
        )
        if item["category"] == "partner":
            partners.append(
                f"| {link} | {PROFILES[item['id']]['summary']} | "
                + ", ".join(f"`{theme}`" for theme in item["related_themes"])
                + " |"
            )
    (ROOT / "docs" / "80_theme_company_matrix.md").write_text("\n".join(matrix) + "\n", encoding="utf-8")
    (ROOT / "docs" / "82_partner_map.md").write_text("\n".join(partners) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "companies": len(generated),
                "lg_affiliates": sum(item["category"] == "lg_affiliate" for item in generated),
                "partners": sum(item["category"] == "partner" for item in generated),
                "companies_needing_source": sum(not item["source_ids"] for item in generated),
                "images_reused": len(image_usage),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
