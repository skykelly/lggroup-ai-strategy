#!/usr/bin/env python3
"""Generate Concept entities from the Wiki taxonomy and docs/topics metadata."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONCEPTS_DIR = ROOT / "concepts"
TAXONOMY_PATH = ROOT / "concept_taxonomy_and_core_definitions.md"
INVENTORY_PATH = ROOT / "data" / "image_inventory.json"

THEME_INFO = {
    "ai_data_center_infra": ("AI Data Center / Infra", "docs/01_ai_data_center_infra"),
    "physical_ai_smart_manufacturing": (
        "Physical AI / Smart Manufacturing",
        "docs/02_physical_ai_smart_manufacturing",
    ),
    "ai_mobility_sdv_aidv": ("AI Mobility / SDV·AIDV", "docs/03_ai_mobility_sdv_aidv"),
    "enterprise_ax_agentic_operating_model": (
        "Enterprise AX / Agentic Operating Model",
        "docs/04_enterprise_ax_agentic_operating_model",
    ),
    "ai_for_science_bio_materials_battery": (
        "AI for Science / Bio / Materials / Battery",
        "docs/05_ai_for_science_bio_materials_battery",
    ),
    "global_ai_alliance_open_innovation": (
        "Global AI Alliance / Open Innovation",
        "docs/06_global_ai_alliance_open_innovation",
    ),
}

COMPANY_NAMES = {
    "lg-corp": "LG Corp.",
    "lg-ai-research": "LG AI Research",
    "lg-uplus": "LG U+",
    "lg-cns": "LG CNS",
    "lg-electronics": "LG Electronics",
    "lg-energy-solution": "LG Energy Solution",
    "lg-display": "LG Display",
    "lg-innotek": "LG Innotek",
    "lg-chem": "LG Chem",
    "lg-household-health-care": "LG Household & Health Care",
    "lg-technology-ventures": "LG Technology Ventures",
    "nvidia": "NVIDIA",
    "skild-ai": "Skild AI",
    "palantir": "Palantir",
    "qualcomm": "Qualcomm",
    "sdverse": "SDVerse",
    "dd-pharmatech": "D&D Pharmatech",
    "applied-intuition": "Applied Intuition",
}

EXTRA_CONCEPTS = {
    "adoption-metrics": ("Adoption Metrics", "AI가 현업 업무에 실제 정착하고 반복 사용되는 정도를 측정하는 지표", "enterprise_ax_agentic_operating_model"),
    "ai-infrastructure-sovereignty": ("AI Infrastructure Sovereignty", "AI 연산 인프라의 위치·운영·전력·보안에 대한 통제력", "ai_data_center_infra"),
    "ai-moat": ("AI Moat", "AI 경쟁우위를 장기간 방어하게 하는 데이터·운영·물리 자산의 결합", "global_ai_alliance_open_innovation"),
    "ai-sovereignty": ("AI Sovereignty", "모델·데이터·인프라·거버넌스의 핵심 통제력을 확보하는 전략", "global_ai_alliance_open_innovation"),
    "ax-kpi": ("AX KPI", "AI 전환이 업무와 경영 성과를 바꾼 정도를 측정하는 성과지표", "enterprise_ax_agentic_operating_model"),
    "data-flywheel": ("Data Flywheel", "사용과 운영 결과가 다시 학습 데이터와 성능 개선으로 이어지는 순환 구조", "enterprise_ax_agentic_operating_model"),
    "data-product": ("Data Product", "재사용 가능한 데이터·품질·인터페이스·책임체계를 갖춘 제품형 데이터 자산", "enterprise_ax_agentic_operating_model"),
    "enterprise-ax": ("Enterprise AX", "기업의 업무·의사결정·운영체계를 AI 중심으로 재설계하는 전사 전환", "enterprise_ax_agentic_operating_model"),
    "exaone": ("EXAONE", "LG AI Research가 개발하는 범용·산업 특화 기반 모델 계열", "enterprise_ax_agentic_operating_model"),
    "foundation-model": ("Foundation Model", "다양한 하위 업무와 산업 애플리케이션에 전이 가능한 대규모 기반 모델", "enterprise_ax_agentic_operating_model"),
    "industrial-ai-ecosystem": ("Industrial AI Ecosystem", "모델·데이터·인프라·현장 자산·파트너가 결합된 산업 AI 생태계", "global_ai_alliance_open_innovation"),
    "industry-specialized-ai": ("Industry-Specialized AI", "산업 데이터와 업무 규칙에 맞춰 최적화된 전문 AI", "enterprise_ax_agentic_operating_model"),
    "inference-economics": ("Inference Economics", "추론 비용·활용률·지연시간·서비스 가격이 만드는 AI 운영 경제성", "ai_data_center_infra"),
    "k-exaone": ("K-EXAONE", "한국어와 국내 산업·공공 맥락의 경쟁력을 지향하는 EXAONE 계열 모델", "enterprise_ax_agentic_operating_model"),
    "korean-ai": ("Korean AI", "한국어·국내 데이터·제도·산업 환경에 적합하도록 구축된 AI 역량", "global_ai_alliance_open_innovation"),
    "manufacturing-data-product": ("Manufacturing Data Product", "제조 데이터를 예측·최적화·실행 가능한 반복형 AI 제품으로 만든 자산", "physical_ai_smart_manufacturing"),
    "model-governance": ("Model Governance", "모델 선정·평가·배포·위험·수명주기를 관리하는 통제체계", "enterprise_ax_agentic_operating_model"),
    "partner-technology-transfer": ("Partner Technology Transfer", "파트너 기술과 운영 노하우를 LG 내부 역량으로 이전·축적하는 과정", "global_ai_alliance_open_innovation"),
    "physical-world-data": ("Physical-World Data", "제품·공장·설비·차량·배터리·서비스 현장에서 생성되는 물리 세계 데이터", "physical_ai_smart_manufacturing"),
    "power-bottleneck": ("Power Bottleneck", "AI 인프라 확장을 제한하는 전력 공급·계통 접속·배전 제약", "ai_data_center_infra"),
    "sovereign-ai-foundation-model": ("Sovereign AI Foundation Model", "국가·언어·산업의 통제 요구를 반영해 운영되는 기반 모델", "global_ai_alliance_open_innovation"),
    "strategic-alliance-governance": ("Strategic Alliance Governance", "파트너십의 역할·지식이전·의존도·성과를 관리하는 체계", "global_ai_alliance_open_innovation"),
    "workflow-automation": ("Workflow Automation", "AI와 시스템 연계를 통해 업무 흐름의 판단·실행 단계를 자동화하는 것", "enterprise_ax_agentic_operating_model"),
}

ALIASES = {
    "ai-data-center": ["AIDC", "AI 데이터센터"],
    "ai-factory": ["AI 팩토리", "Physical AI Factory"],
    "physical-ai": ["물리 AI", "Embodied AI"],
    "smart-manufacturing": ["스마트 제조", "Smart Factory", "스마트팩토리"],
    "sdv": ["Software-Defined Vehicle", "소프트웨어 정의 차량"],
    "aidv": ["AI-Defined Vehicle", "AI 정의 차량"],
    "enterprise-ontology": ["기업 온톨로지", "Business Ontology"],
    "agentic-operating-model": ["Agentic AI Operating Model", "Agentic Workflow"],
    "ai-co-scientist": ["AI 공동 과학자", "AI Research Partner"],
    "global-ai-alliance": ["글로벌 AI 제휴", "Strategic AI Partnership"],
    "bms-bmts": ["BMS", "BMTS", "Battery Management Total Solution"],
    "cdu": ["Coolant Distribution Unit", "냉각수 분배 장치"],
    "exaone": ["EXAONE Foundation Model"],
    "k-exaone": ["K-EXAONE Foundation Model"],
}

CORE_DETAILS = {
    "ai-data-center": (
        "AI Data Center는 대규모 AI 학습·추론을 위해 GPU, 고밀도 랙, 전력, 냉각, 네트워크, 클라우드 운영 소프트웨어를 통합한 데이터센터 인프라다. 기존 데이터센터보다 전력 밀도와 발열이 높아 전력·열관리·workload 운영을 하나의 시스템으로 설계해야 한다.",
        "LG U+의 AIDC 운영, LG CNS의 설계·구축·운영, LG전자의 냉각, LG에너지솔루션의 ESS·전력 자산을 One LG 제안으로 묶을 수 있는 기반 사업이다.",
        "AI Data Center는 AI가 실행되는 물리적·연산 기반이다. AI Factory는 이 기반 위에서 제조·로봇 AI를 학습·검증·배포하는 운영 모델이므로 동일 개념이 아니다.",
    ),
    "ai-factory": (
        "AI Factory는 제조 데이터, 로봇, 디지털트윈, 합성데이터, 시뮬레이션, AI 모델의 학습·검증·배포를 하나의 workflow로 연결하는 Physical AI 운영 모델이다. 데이터센터 자체가 아니라 물리 세계 AI를 지속적으로 개선하고 현장에 적용하는 실행 체계다.",
        "LG전자 Smart Factory와 LG Smart Park, LG CNS Factova, LG AI Research 모델, 글로벌 로봇·시뮬레이션 파트너를 연결하는 그룹 차원의 제조 AI 축이다.",
        "Primary Theme은 반드시 Physical AI / Smart Manufacturing이다. AI Data Center는 필요한 기반이지만 AI Factory의 분류 기준은 제조·로봇 운영 workflow다.",
    ),
    "physical-ai": (
        "Physical AI는 AI가 공장, 설비, 로봇, 물류, 차량, 센서 등 물리 세계의 상태를 인식하고 판단하며 행동하는 체계다. 언어·문서 처리에서 끝나지 않고 실제 환경의 제약과 안전 조건 아래 실행 결과를 만든다.",
        "LG가 보유한 제조 현장, 제품, 센서, 배터리, 서비스 데이터는 Physical AI를 학습하고 검증할 수 있는 차별화 자산이다.",
        "Smart Manufacturing은 제조 운영의 최적화 범주이고, Physical AI는 로봇과 설비가 환경을 이해하고 행동하는 지능의 범주다.",
    ),
    "smart-manufacturing": (
        "Smart Manufacturing은 제조공정, 설비, 품질, 물류, 에너지, 작업자 데이터를 연결해 생산성과 품질을 높이는 데이터·AI 기반 제조 운영체계다. 자동화 설비 도입을 넘어 공정 전체의 판단과 최적화에 AI가 참여한다.",
        "LG전자의 글로벌 공장 경험과 LG CNS Factova를 외부 고객이 구매 가능한 반복형 제조 AX 솔루션으로 전환하는 기반이다.",
        "AI Factory가 Physical AI 모델의 학습·검증·배포 loop를 강조한다면 Smart Manufacturing은 공정 운영성과와 현장 실행을 중심으로 본다.",
    ),
    "sdv": (
        "SDV는 차량 기능과 사용자 경험이 하드웨어 고정 기능보다 소프트웨어, OTA 업데이트, 중앙 컴퓨팅, 클라우드 연결을 통해 지속 개선되는 차량 아키텍처다.",
        "LG전자 VS, LG디스플레이, LG이노텍, LG에너지솔루션, LG U+의 자산을 차량의 소프트웨어·HMI·센싱·배터리·통신 레이어로 연결한다.",
        "SDV는 소프트웨어 중심 차량이라는 기반 구조이고, AIDV는 이 구조 위에 AI 판단과 개인화·자율성을 더한 개념이다.",
    ),
    "aidv": (
        "AIDV는 SDV 위에 AI 판단, 인캐빈 센싱, 운전자·탑승자 이해, 자율주행 보조, 개인화 경험, 배터리·정비 예측을 결합한 차량 개념이다.",
        "LG는 완성차를 직접 생산하지 않더라도 차량 안의 경험, 센싱, 디스플레이, 배터리 지능, 연결성 레이어에서 주도권을 확보할 수 있다.",
        "AIDV는 SDV를 대체하는 말이 아니라 SDV 아키텍처를 전제로 AI가 차량 경험과 운영을 고도화하는 상위 진화 방향이다.",
    ),
    "enterprise-ontology": (
        "Enterprise Ontology는 제품, 고객, 공장, 설비, 부품, 주문, 재고, 원가, 품질, R&D 과제 같은 기업 객체와 관계를 정의하는 의미 체계다. AI가 기업 운영을 이해하고 시뮬레이션하며 실행하려면 데이터 테이블보다 안정적인 업무 의미 구조가 필요하다.",
        "여러 LG 계열사의 ERP·MES·PLM·SCM·CRM 데이터를 Agent가 이해할 수 있는 공통 운영 언어로 연결하는 기반이다.",
        "Ontology는 단순 데이터 통합이나 검색 인덱스가 아니다. 권한·업무 규칙·상태 변화·실행 가능한 action까지 기업 객체에 연결해야 한다.",
    ),
    "agentic-operating-model": (
        "Agentic Operating Model은 AI Agent가 목표를 이해하고 계획, 분석, 시뮬레이션, 실행 제안, 평가를 반복하도록 기업 프로세스를 재설계한 운영체계다.",
        "원가, 수요, 재고, 생산, 품질, R&D, 경영 Cockpit을 개별 챗봇이 아닌 연결된 Agent workflow로 전환하는 기준을 제공한다.",
        "Agent 도구 도입만으로 성립하지 않는다. Enterprise Ontology, Data Foundation, 시스템 action, 승인권, LLMOps, Governance가 함께 필요하다.",
    ),
    "ai-co-scientist": (
        "AI Co-Scientist는 논문, 특허, 분자구조, 이미지, 실험 데이터를 바탕으로 후보물질, 실험 설계, 물성 예측, 다음 연구 방향을 제안하는 AI 연구 파트너다.",
        "LG AI Research의 모델·Discovery 역량과 LG화학·LG에너지솔루션·LG생활건강의 실험·상용화 필드를 closed-loop R&D로 연결한다.",
        "연구자를 대체하는 자동화가 아니라 탐색 공간을 넓히고 실험 우선순위를 개선하는 의사결정 보조 체계다.",
    ),
    "global-ai-alliance": (
        "Global AI Alliance는 LG가 글로벌 AI·로봇·데이터·모빌리티·바이오 파트너와 협력해 부족한 원천기술을 빠르게 확보하고 LG의 산업 자산에 적용하는 전략이다.",
        "NVIDIA, Skild AI, Palantir, Qualcomm, SDVerse, D&D Pharmatech 등과의 협력을 1~5번 테마를 가속하는 옵션 포트폴리오로 관리한다.",
        "제휴 수나 발표 자체가 성과가 아니다. 데이터, 운영 노하우, 모델 평가역량, 고객 관계가 LG 내부 자산으로 이전되는지가 핵심 경계다.",
    ),
}

CORE_RELATIONS = {
    "pue": {
        "companies": ["lg-uplus", "lg-cns", "lg-electronics", "lg-energy-solution"],
        "sources": ["src_uptime_institute_pue"],
    },
    "ai-data-center": {
        "companies": ["lg-uplus", "lg-cns", "lg-electronics", "lg-energy-solution", "lg-ai-research"],
        "sources": ["src_lguplus_paju_aidc_20260607", "src_lge_dcw_20260421", "src_lgcns_ai_box_20260304"],
    },
    "ai-factory": {
        "companies": ["lg-electronics", "lg-cns", "lg-ai-research", "lg-uplus", "nvidia", "skild-ai"],
        "sources": ["src_nvidia_lg_ai_factory_20260607", "src_lg_nvidia_map_20260608", "src_lge_smart_factory_20260414"],
    },
    "physical-ai": {
        "companies": ["lg-electronics", "lg-cns", "lg-ai-research", "lg-innotek", "skild-ai", "nvidia"],
        "sources": ["src_lge_smart_factory_20260414", "src_lgcns_skild_ai_20250616", "src_lg_nvidia_map_20260608"],
    },
    "smart-manufacturing": {
        "companies": ["lg-electronics", "lg-cns", "lg-energy-solution", "lg-display", "lg-chem"],
        "sources": ["src_lge_smart_factory_20260414", "src_lg_smart_park_lighthouse_20220427", "src_lgcns_factova_20260519"],
    },
    "sdv": {
        "companies": ["lg-electronics", "lg-innotek", "lg-display", "lg-energy-solution", "lg-uplus"],
        "sources": ["src_lge_ai_in_vehicle_20251217", "src_lgdisplay_ces2026_20260105", "src_lgensol_sdverse_20260403"],
    },
    "aidv": {
        "companies": ["lg-electronics", "lg-innotek", "lg-display", "lg-energy-solution", "lg-uplus", "lg-ai-research"],
        "sources": ["src_lge_ai_in_vehicle_20251217", "src_lginnotek_ces2026_aidv_20260106", "src_lg_nvidia_map_20260608"],
    },
    "enterprise-ontology": {
        "companies": ["lg-corp", "lg-cns", "lg-ai-research", "palantir"],
        "sources": ["src_lgcorp_silicon_valley_20260407", "src_lgcns_palantir_20260312", "src_lgcns_ax_platform"],
    },
    "agentic-operating-model": {
        "companies": ["lg-corp", "lg-cns", "lg-ai-research", "lg-electronics", "lg-energy-solution"],
        "sources": ["src_lge_strategy_ax_20260108", "src_lgcns_ax_platform", "src_lgcns_ax_consulting"],
    },
    "ai-co-scientist": {
        "companies": ["lg-ai-research", "lg-chem", "lg-energy-solution", "lg-household-health-care", "dd-pharmatech"],
        "sources": ["src_lgai_exaone_discovery_patent_20260203", "src_lgai_dd_pharmatech_20260617", "src_lgai_materials_intelligence"],
    },
    "global-ai-alliance": {
        "companies": ["lg-corp", "lg-technology-ventures", "lg-ai-research", "lg-cns", "lg-electronics", "lg-energy-solution", "nvidia", "skild-ai", "palantir", "qualcomm", "sdverse", "dd-pharmatech"],
        "sources": ["src_lg_nvidia_map_20260608", "src_lgcorp_silicon_valley_20260407", "src_lgcns_palantir_20260312", "src_lgcns_skild_ai_20250616"],
    },
}

PRIMARY_THEME_RELEVANCE = {
    "ai_data_center_infra": "AI 연산 용량보다 전력·냉각·가동률을 함께 최적화하는 AIDC 사업성의 설계 변수다.",
    "physical_ai_smart_manufacturing": "제조 데이터가 예측·시뮬레이션·현장 실행으로 이어지는 Physical AI 운영 loop를 구성한다.",
    "ai_mobility_sdv_aidv": "차량의 소프트웨어·센싱·디스플레이·배터리 계층을 지속 업데이트 가능한 AI 서비스로 전환한다.",
    "enterprise_ax_agentic_operating_model": "기업 데이터와 업무 규칙을 의사결정·실행 가능한 Agent workflow로 바꾸는 운영 기반이다.",
    "ai_for_science_bio_materials_battery": "후보 탐색과 실험 검증 사이의 반복 시간을 줄여 R&D throughput을 높이는 수단이다.",
    "global_ai_alliance_open_innovation": "외부 기술을 빠르게 확보하면서 데이터와 운영 노하우를 LG 내부 자산으로 남기는 협력 장치다.",
}

CROSS_THEME_RELEVANCE = {
    "ai_data_center_infra": "대규모 학습·추론에 필요한 GPU 용량, 전력 안정성, 냉각 효율과 운영 SLA를 요구한다.",
    "physical_ai_smart_manufacturing": "공장·로봇·설비에서 생성되는 데이터와 시뮬레이션 결과를 실제 제어와 품질 개선으로 연결한다.",
    "ai_mobility_sdv_aidv": "차량 내 컴퓨팅, 센싱, HMI, 배터리 데이터에 적용되어 이동 경험과 안전 기능을 고도화한다.",
    "enterprise_ax_agentic_operating_model": "전사 데이터 모델, 권한, KPI, 승인 workflow에 편입되어 반복 가능한 경영·업무 프로세스가 된다.",
    "ai_for_science_bio_materials_battery": "논문·특허·실험·분자 및 소재 데이터를 처리하는 연구 workload와 검증 loop를 지원한다.",
    "global_ai_alliance_open_innovation": "자체 역량만으로 확보하기 어려운 모델·플랫폼·하드웨어를 파트너와 결합하되 의존도를 관리하게 한다.",
}

COMPANY_THEME_ROLES = {
    "ai_data_center_infra": {
        "lg-uplus": "파주 AIDC와 통신망을 기반으로 고밀도 GPU 인프라의 전력·네트워크·가동률·SLA를 운영한다.",
        "lg-cns": "데이터센터 DBO, AI Box, 클라우드·보안 역량으로 기업용 AI 인프라를 설계하고 구축·이관한다.",
        "lg-electronics": "HVAC, Chiller, DTC, CDU, DCCM을 결합해 고발열 AI 랙의 열관리와 냉각 효율을 담당한다.",
        "lg-energy-solution": "UPS 배터리와 ESS를 통해 계통 변동, 순간 정전, 피크 부하에 대응하는 전력 안정화 계층을 제공한다.",
        "lg-ai-research": "EXAONE 학습·추론을 내부 anchor workload로 제공해 GPU 클러스터의 성능과 활용률 요구를 구체화한다.",
        "lg-corp": "One LG AIDC 패키지의 투자 우선순위와 계열사 간 상업적 책임을 조정한다.",
        "nvidia": "GPU, 네트워킹, AI 소프트웨어 스택과 전력 아키텍처 reference를 제공하는 enabling partner다.",
    },
    "physical_ai_smart_manufacturing": {
        "lg-electronics": "60개 이상 글로벌 공장 운영 경험과 LG Smart Park 데이터를 바탕으로 공정 설계부터 안정화까지 검증한다.",
        "lg-cns": "Factova, MES·Control, 안전관리와 로봇 통합 역량으로 제조 AI를 고객 시스템에 구현한다.",
        "lg-ai-research": "EXAONE, Physical Intelligence, Advanced Agent를 제조 문서·영상·공정 데이터 이해에 적용한다.",
        "lg-energy-solution": "배터리 공정의 품질·수율·안전 문제를 고난도 제조 AI의 검증 필드로 제공한다.",
        "lg-display": "OLED 공정의 결함·수율·검사 데이터를 활용해 정밀 제조 최적화 효과를 검증한다.",
        "lg-chem": "화학·첨단소재 공정의 에너지, 품질, 안전 데이터를 연속공정 AI 적용 대상으로 제공한다.",
        "lg-innotek": "카메라·센서·기판 생산과 로봇용 부품 역량으로 인지·검사·제어 계층을 보강한다.",
        "lg-uplus": "Private 5G와 edge network로 AMR·로봇·설비의 저지연 연결과 원격관제를 지원한다.",
        "lg-technology-ventures": "Skild AI 등 Physical AI 스타트업 투자를 통해 로봇 원천기술 옵션을 확보한다.",
        "nvidia": "Isaac, Omniverse, Cosmos, GR00T를 통해 로봇 시뮬레이션과 합성데이터 학습 환경을 제공한다.",
        "skild-ai": "범용 로봇 파운데이션 모델을 제조·물류 데이터에 맞게 조정하는 외부 기술 파트너다.",
        "applied-intuition": "가상환경 기반 자율 시스템 개발·검증 도구를 제공할 수 있는 시뮬레이션 파트너다.",
    },
    "ai_mobility_sdv_aidv": {
        "lg-electronics": "VS 사업의 IVI, AI Cockpit, vision, entertainment 역량으로 차량 내 AI 경험과 중앙 컴퓨팅을 통합한다.",
        "lg-innotek": "카메라·LiDAR·Radar·UWB·5G-NTN·조명 모듈로 차량의 외부 인지와 연결성 데이터를 만든다.",
        "lg-display": "P-OLED, P2P, Slidable OLED 등 차량용 화면을 AI 서비스의 HMI와 사용자 피드백 접점으로 제공한다.",
        "lg-energy-solution": "B.around, BMS/BMTS, SDV BMS로 배터리 안전·열화·잔존가치 데이터를 차량 소프트웨어에 연결한다.",
        "lg-uplus": "5G-V2X, 정밀지도, 정밀측위, MEC와 관제 플랫폼으로 차량-도로-클라우드 연결을 운영한다.",
        "lg-ai-research": "멀티모달 모델을 운전자·탑승자 이해, 차량 문맥 추론, 정비·배터리 예측에 적용할 수 있다.",
        "lg-cns": "차량 데이터 플랫폼, 클라우드·보안과 OTA 운영체계를 기업 시스템에 통합하는 역할이 예상된다.",
        "nvidia": "DRIVE Hyperion과 차량용 AI 컴퓨팅 reference로 센싱·추론·검증 생태계를 제공한다.",
        "qualcomm": "Snapdragon Digital Chassis에 배터리 진단 기능을 결합할 SoC·차량 컴퓨팅 기반을 제공한다.",
        "sdverse": "자동차 SW B2B marketplace를 통해 LG 배터리 소프트웨어의 OEM 유통 채널을 제공한다.",
    },
    "enterprise_ax_agentic_operating_model": {
        "lg-corp": "그룹 AX 우선순위, 공통 KPI, 데이터 공유 원칙과 계열사 간 의사결정 구조를 설계한다.",
        "lg-ai-research": "EXAONE·K-EXAONE과 Advanced Agent를 그룹 문서·업무 데이터에 맞게 고도화한다.",
        "lg-cns": "ERP·SCM·MES·PLM 연계, AX Platform, Knowledge Lake, LLMOps와 Governance를 구현한다.",
        "lg-electronics": "개발·판매·SCM·구매·마케팅 업무와 LGenie를 통해 전사 Agent의 실제 adoption을 검증한다.",
        "lg-energy-solution": "수요·원재료·공장 가동률·품질 변동이 큰 배터리 사업에서 의사결정 자동화 효과를 측정한다.",
        "lg-display": "결함 원인 분석과 Hi-D assistant 사례로 제조·사무 AX의 cycle-time 단축을 검증한다.",
        "lg-chem": "one-person-one-agent와 기술·특허 분석을 통해 지식업무 자동화의 확산 모델을 제공한다.",
        "lg-innotek": "OEM 프로젝트, 부품 수요, 품질·수율과 공급망 리스크를 연결하는 적용 후보 기업이다.",
        "lg-uplus": "통신망 운영과 고객센터 데이터를 활용해 실시간 운영 Agent와 고객 Agent를 검증할 수 있다.",
        "lg-household-health-care": "브랜드·유통·고객·프로모션 데이터를 수요예측과 재고 의사결정에 연결할 적용 후보 기업이다.",
        "palantir": "Foundry/AIP와 ontology 운영 경험을 제공하지만 LG의 공통 데이터 모델 자체를 대신하는 주체는 아니다.",
    },
    "ai_for_science_bio_materials_battery": {
        "lg-ai-research": "EXAONE Discovery, Bio·Materials Intelligence로 문헌 이해, 후보 생성, 물성 예측 모델을 개발한다.",
        "lg-chem": "신약·생명과학·첨단소재 연구소에서 AI가 제안한 후보의 합성·실험·사업성 검증을 수행한다.",
        "lg-energy-solution": "양극재·전해질·첨가제·건식전극의 소재·공정 데이터를 제공하고 배터리 성능으로 검증한다.",
        "lg-household-health-care": "화장품 효능 소재의 합성 가능성, 안전성, 소비자 가치까지 연결해 상용화를 검증한다.",
        "lg-cns": "ELN·LIMS·특허·논문 데이터 파이프라인과 모델 운영·권한 체계를 구현하는 역할이 예상된다.",
        "lg-display": "OLED 소재의 수명·효율·공정 적합성을 평가하는 추가 적용 필드가 될 수 있다.",
        "lg-innotek": "광학·기판·센서·방열 소재의 물성 개선을 위한 추가 적용 가능성이 있다.",
        "dd-pharmatech": "펩타이드 formulation, 합성, 평가와 임상 개발로 AI 후보의 wet-lab 검증을 담당한다.",
    },
    "global_ai_alliance_open_innovation": {
        "lg-corp": "그룹 차원의 파트너 선정, 협력 범위, 상업화 우선순위와 기술 의존도 관리 원칙을 정한다.",
        "lg-technology-ventures": "AI·로봇 스타트업 투자로 조기 기술 접근권과 후속 사업 협력 옵션을 확보한다.",
        "lg-ai-research": "자체 EXAONE 역량을 외부 GPU·모델·바이오 파트너와 결합하고 내부 기술 흡수 수준을 평가한다.",
        "lg-cns": "파트너 기술을 LG 및 외부 고객의 데이터·업무 시스템에 이식해 반복 가능한 사업으로 만든다.",
        "lg-electronics": "냉각·스마트팩토리·로봇·모빌리티 제품을 외부 AI 스택과 결합해 현장 reference를 만든다.",
        "lg-uplus": "글로벌 GPU 및 네트워크 파트너 기술을 AIDC와 GPU Cloud 서비스로 운영한다.",
        "lg-energy-solution": "NVIDIA·Qualcomm·SDVerse 협력을 전력 아키텍처와 배터리 SW 사업으로 전환한다.",
        "lg-innotek": "글로벌 자율주행·로봇 플랫폼에 센서·통신·조명 부품을 최적화해 공급 범위를 넓힌다.",
        "lg-display": "차량용 디스플레이를 글로벌 OEM·SDV UX 생태계의 인터페이스 계층으로 공급한다.",
        "lg-chem": "바이오·소재 파트너와 후보 탐색부터 실험 검증까지 연결하는 오픈이노베이션 필드를 제공한다.",
        "lg-household-health-care": "AI 발굴 소재를 뷰티 제품과 소비자 효능으로 상용화하는 downstream 검증 역할을 맡는다.",
        "nvidia": "AI Infra, Physical AI, Mobility의 공통 compute·simulation stack을 제공하는 핵심 enabling partner다.",
        "skild-ai": "로봇 파운데이션 모델을 제공하고 LG 제조·물류 데이터로 산업 적합성을 검증한다.",
        "palantir": "기업 ontology와 운영 의사결정 플랫폼의 benchmark 및 구현 파트너 역할을 한다.",
        "qualcomm": "차량 SoC와 배터리 진단 소프트웨어를 결합하는 공동 개발 파트너다.",
        "sdverse": "LG 배터리 SW가 글로벌 OEM에 도달할 수 있는 marketplace와 거래 접점을 제공한다.",
        "dd-pharmatech": "AI 설계 펩타이드 후보의 formulation·실험·임상 가능성을 검증하는 바이오 파트너다.",
    },
}

COMPANY_CONCEPT_LENS = {
    "lg-uplus": "{role}을 실제 인프라 운영 지표와 고객 SLA로 검증한다.",
    "lg-cns": "{role}을 데이터 파이프라인과 업무시스템에 구현하고 외부 고객용 구축 방법론으로 표준화한다.",
    "lg-electronics": "{role}을 장비·공장·차량 환경에 적용해 성능, 안정성, 유지보수성을 검증한다.",
    "lg-energy-solution": "{role}을 배터리·전력 데이터와 연결해 안전성, 수명, 경제성 개선 효과를 측정한다.",
    "lg-ai-research": "{role}에 필요한 모델 학습·평가 체계와 도메인 지능을 개발한다.",
    "lg-corp": "{role}의 계열사별 책임, 투자 기준, 그룹 공통 KPI를 조정한다.",
    "lg-display": "{role}을 OLED 제조와 차량 HMI 현장에 적용해 품질·사용성 효과를 확인한다.",
    "lg-innotek": "{role}을 센서·부품 데이터와 정밀 제조 환경에서 인지·검사 성능으로 검증한다.",
    "lg-chem": "{role}을 화학·소재·생명과학 실험으로 검증하고 후보의 사업성을 평가한다.",
    "lg-household-health-care": "{role}을 소비재 R&D와 시장 반응에 연결해 상용화 가치를 확인한다.",
    "lg-technology-ventures": "{role} 관련 스타트업 투자로 기술 접근권과 전략적 옵션을 확보한다.",
    "nvidia": "{role}에 필요한 compute·simulation reference stack을 제공하고 LG 자산과의 결합을 지원한다.",
    "skild-ai": "{role}에 활용할 로봇 모델을 제공하고 LG 산업 데이터에 대한 전이 가능성을 검증한다.",
    "palantir": "{role}을 ontology 기반 운영 모델로 구조화하고 초기 구현을 지원한다.",
    "qualcomm": "{role}을 차량 SoC에서 실행할 수 있도록 컴퓨팅·추론 환경을 제공한다.",
    "sdverse": "{role} 관련 자동차 소프트웨어의 OEM 유통과 채택을 marketplace로 지원한다.",
    "dd-pharmatech": "{role}이 만든 후보를 합성·평가·개발 단계로 넘겨 wet-lab 타당성을 검증한다.",
    "applied-intuition": "{role}을 가상환경에서 학습·회귀시험·안전 검증할 수 있는 도구를 제공한다.",
}

CONCEPT_COMPANIES: dict[str, list[str]] = {}
for concept_ids, company_ids in [
    (
        ["ai-data-center", "gpu-cloud", "high-density-gpu-rack", "workload-orchestration", "pue", "compute-per-megawatt", "inference-economics", "ai-infrastructure-sovereignty"],
        ["lg-uplus", "lg-cns", "lg-electronics", "lg-energy-solution", "lg-ai-research"],
    ),
    (
        ["data-center-cooling", "direct-to-chip-cooling", "cdu", "immersion-cooling"],
        ["lg-electronics", "lg-cns", "lg-uplus"],
    ),
    (
        ["dc-grid", "ess-ups-for-aidc", "power-bottleneck"],
        ["lg-energy-solution", "lg-electronics", "lg-cns", "lg-uplus"],
    ),
    (
        ["physical-ai", "ai-factory"],
        ["lg-electronics", "lg-cns", "lg-ai-research", "lg-uplus", "nvidia", "skild-ai"],
    ),
    (
        ["smart-manufacturing", "manufacturing-intelligence", "digital-twin", "predictive-maintenance", "factory-ontology", "manufacturing-data-product", "physical-world-data"],
        ["lg-electronics", "lg-cns", "lg-ai-research", "lg-energy-solution", "lg-display", "lg-chem"],
    ),
    (
        ["robotic-foundation-model", "industrial-humanoid", "synthetic-data", "robot-simulation"],
        ["lg-cns", "lg-electronics", "lg-ai-research", "lg-innotek", "nvidia", "skild-ai"],
    ),
    (
        ["sdv", "aidv"],
        ["lg-electronics", "lg-innotek", "lg-display", "lg-energy-solution", "lg-uplus", "lg-ai-research"],
    ),
    (
        ["ai-cabin", "in-vehicle-ai", "in-cabin-sensing", "automotive-display", "on-device-ai"],
        ["lg-electronics", "lg-display", "lg-innotek", "lg-ai-research"],
    ),
    (
        ["adas", "autonomous-driving", "v2x"],
        ["lg-innotek", "lg-uplus", "lg-electronics", "nvidia"],
    ),
    (
        ["bms-bmts", "battery-software"],
        ["lg-energy-solution", "lg-electronics", "qualcomm", "sdverse"],
    ),
    (
        ["enterprise-ontology", "data-foundation", "knowledge-graph"],
        ["lg-corp", "lg-cns", "lg-ai-research", "palantir"],
    ),
    (
        ["agentic-operating-model", "ai-cockpit", "decision-intelligence", "what-if-simulation", "workflow-automation"],
        ["lg-corp", "lg-cns", "lg-ai-research", "lg-electronics", "lg-energy-solution"],
    ),
    (
        ["agent-governance", "llmops", "ai-governance", "model-governance"],
        ["lg-corp", "lg-cns", "lg-ai-research"],
    ),
    (
        ["enterprise-ax", "ax-kpi", "adoption-metrics", "data-product", "data-flywheel"],
        ["lg-cns", "lg-ai-research", "lg-electronics", "lg-energy-solution", "lg-display", "lg-chem"],
    ),
    (
        ["foundation-model", "exaone", "k-exaone", "industry-specialized-ai"],
        ["lg-ai-research", "lg-cns", "lg-electronics", "lg-chem", "lg-energy-solution"],
    ),
    (
        ["ai-for-science", "ai-co-scientist", "exaone-discovery", "chemical-agentic-ai", "closed-loop-rnd"],
        ["lg-ai-research", "lg-chem", "lg-energy-solution", "lg-household-health-care", "lg-cns"],
    ),
    (
        ["bio-intelligence", "peptide-drug-discovery"],
        ["lg-ai-research", "lg-chem", "dd-pharmatech"],
    ),
    (
        ["materials-intelligence", "materials-informatics", "battery-materials"],
        ["lg-ai-research", "lg-chem", "lg-energy-solution"],
    ),
    (
        ["patent-intelligence"],
        ["lg-ai-research", "lg-chem", "lg-energy-solution", "lg-cns"],
    ),
    (
        ["global-ai-alliance", "open-innovation", "industrial-ai-ecosystem", "strategic-alliance-governance"],
        ["lg-corp", "lg-technology-ventures", "lg-ai-research", "lg-cns", "lg-electronics", "lg-energy-solution", "nvidia", "palantir"],
    ),
    (
        ["cvc"],
        ["lg-corp", "lg-technology-ventures"],
    ),
    (
        ["hybrid-ai-strategy", "ai-moat", "ai-sovereignty", "sovereign-ai-foundation-model", "korean-ai"],
        ["lg-corp", "lg-ai-research", "lg-cns", "lg-uplus", "nvidia", "palantir"],
    ),
    (
        ["partner-technology-transfer"],
        ["lg-corp", "lg-technology-ventures", "lg-cns", "lg-ai-research", "nvidia", "skild-ai", "palantir"],
    ),
]:
    for concept_key in concept_ids:
        CONCEPT_COMPANIES[concept_key] = company_ids

IMAGE_RULES = {
    "ai-data-center": "img_lguplus_paju_pulse_01",
    "gpu-cloud": "img_lgcns_ai_box_01",
    "high-density-gpu-rack": "img_lgcns_ai_box_01",
    "data-center-cooling": "img_koreatimes_cdu_01",
    "direct-to-chip-cooling": "img_koreatimes_cdu_01",
    "cdu": "img_koreatimes_cdu_01",
    "immersion-cooling": "img_koreatimes_cdu_01",
    "dc-grid": "nvidia_800v_architecture",
    "ess-ups-for-aidc": "img_lgensol_ess_na_01",
    "workload-orchestration": "lguplus_ace_on_trust",
    "pue": "img_lguplus_paju_digitaltoday_01",
    "compute-per-megawatt": "nvidia_800v_architecture",
    "power-bottleneck": "nvidia_800v_architecture",
    "inference-economics": "lguplus_ace_on_trust",
    "ai-infrastructure-sovereignty": "img_lguplus_paju_pulse_01",
    "physical-ai": "nvidia_lg_ai_factory_robot",
    "ai-factory": "nvidia_lg_ai_factory_robot",
    "smart-manufacturing": "lgcns_factova_iot_expo",
    "digital-twin": "nvidia_lg_ai_factory_robot",
    "manufacturing-intelligence": "lgcns_factova_iot_expo",
    "predictive-maintenance": "lgcns_factova_iot_expo",
    "robotic-foundation-model": "doc_02_skild_ai_series_c",
    "industrial-humanoid": "doc_02_skild_ai_series_c",
    "synthetic-data": "nvidia_lg_ai_factory_robot",
    "robot-simulation": "nvidia_lg_ai_factory_robot",
    "factory-ontology": "lgcns_factova_iot_expo",
    "manufacturing-data-product": "lgcns_factova_iot_expo",
    "physical-world-data": "nvidia_lg_ai_factory_robot",
    "sdv": "lgdisplay_ces2026_automotive_display",
    "aidv": "lginnotek_autonomous_sensor_fusion",
    "ai-cabin": "lgdisplay_ces2026_automotive_display",
    "in-vehicle-ai": "lgdisplay_ces2026_main",
    "in-cabin-sensing": "lginnotek_autonomous_sensor_fusion",
    "automotive-display": "lgdisplay_ces2026_automotive_display",
    "adas": "lginnotek_autonomous_sensor_fusion",
    "autonomous-driving": "lguplus_autonomous_driving_main",
    "v2x": "lguplus_dynamic_map_architecture",
    "bms-bmts": "lgensol_baround_core_values",
    "battery-software": "lgensol_sdv_bms",
    "on-device-ai": "lginnotek_ces2026_sketch_05",
    "enterprise-ontology": "lgcorp_silicon_valley_palantir_signing",
    "agentic-operating-model": "lgcns_ax_platform_service_development",
    "ai-cockpit": "lgcns_ax_strategy_consulting",
    "decision-intelligence": "lgcns_ax_discovery",
    "what-if-simulation": "lgcns_process_innovation",
    "data-foundation": "lgcns_knowledge_data_pipeline",
    "knowledge-graph": "lgcns_knowledge_data_pipeline",
    "agent-governance": "lgcns_monitoring_governance",
    "llmops": "lgcns_llmops_lifecycle",
    "ai-governance": "lgcns_ai_governance_consulting",
    "enterprise-ax": "lgcns_ax_fair_2026",
    "workflow-automation": "lgcns_service_innovation",
    "ax-kpi": "lgdisplay_ai_transformation_plan",
    "adoption-metrics": "lgdisplay_hi_d_assistant",
    "data-product": "lgcns_knowledge_data_pipeline",
    "data-flywheel": "lgcns_llmops_lifecycle",
    "model-governance": "lgcns_monitoring_governance",
    "foundation-model": "exaone_journey_timeline",
    "exaone": "exaone_journey_timeline",
    "k-exaone": "lgai_exaone45_performance",
    "industry-specialized-ai": "lgai_exaone45_performance",
    "ai-for-science": "exaone_discovery_operation",
    "ai-co-scientist": "exaone_discovery_operation",
    "exaone-discovery": "exaone_discovery_digitaltoday_gif",
    "bio-intelligence": "lgchem_life_science_primary_care",
    "materials-intelligence": "lgchem_cathode_material_main",
    "chemical-agentic-ai": "exaone_discovery_operation",
    "closed-loop-rnd": "lgensol_battery_technology_roadmap_mid_nickel",
    "peptide-drug-discovery": "exaone_discovery_operation",
    "battery-materials": "lgchem_cathode_material_main",
    "materials-informatics": "lgchem_cathode_production_plan",
    "patent-intelligence": "lgensol_genai_patent_chatbot",
    "global-ai-alliance": "lg_nvidia_map_koo_huang_prn",
    "open-innovation": "lg_nvidia_map_koo_huang_prn",
    "cvc": "lg_nvidia_map_koo_huang_prn",
    "hybrid-ai-strategy": "exaone_journey_timeline",
    "industrial-ai-ecosystem": "lg_nvidia_map_koo_huang_prn",
    "partner-technology-transfer": "lgcns_skild_ai_hq",
    "strategic-alliance-governance": "lg_nvidia_map_koo_huang_prn",
    "ai-moat": "nvidia_lg_ai_factory_robot",
    "ai-sovereignty": "exaone_journey_timeline",
    "sovereign-ai-foundation-model": "lgai_exaone45_performance",
    "korean-ai": "exaone_journey_timeline",
}

DEFAULT_IMAGE_BY_THEME = {
    "ai_data_center_infra": "img_lguplus_paju_pulse_01",
    "physical_ai_smart_manufacturing": "lgcns_factova_iot_expo",
    "ai_mobility_sdv_aidv": "lgdisplay_ces2026_automotive_display",
    "enterprise_ax_agentic_operating_model": "lgcns_ax_platform_service_development",
    "ai_for_science_bio_materials_battery": "exaone_discovery_operation",
    "global_ai_alliance_open_innovation": "lg_nvidia_map_koo_huang_prn",
}

CASE_IMAGE_USAGE = {
    "img_lgcns_ai_box_01": "concepts/lgcns_aibox.md",
    "img_koreatimes_cdu_01": "concepts/lge_cdu.md",
    "img_lgensol_ess_na_01": "concepts/lges_ess_us.md",
    "img_lguplus_paju_pulse_01": "concepts/lguplus_datacenter.md",
}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, frontmatter, body = text.split("---", 2)
    try:
        return yaml.safe_load(frontmatter) or {}, body
    except yaml.YAMLError:
        repaired_lines = []
        for line in frontmatter.splitlines():
            match = re.match(r"^(title):\s*(.+)$", line)
            if match and ":" in match.group(2) and not match.group(2).startswith(("'", '"')):
                line = f"{match.group(1)}: {json.dumps(match.group(2), ensure_ascii=False)}"
            repaired_lines.append(line)
        return yaml.safe_load("\n".join(repaired_lines)) or {}, body


def parse_taxonomy() -> dict[str, dict]:
    text = TAXONOMY_PATH.read_text(encoding="utf-8")
    concepts: dict[str, dict] = {}
    row_pattern = re.compile(
        r"^\| ([a-z0-9-]+) \| ([^|]+?) \| ([^|]+?) \| ([a-z0-9_]+) \|$",
        re.MULTILINE,
    )
    for concept_id, title, role, theme in row_pattern.findall(text):
        concepts[concept_id] = {
            "title": title.strip(),
            "role": role.strip(),
            "primary_theme": theme.strip(),
        }
    for concept_id, (title, role, theme) in EXTRA_CONCEPTS.items():
        concepts[concept_id] = {"title": title, "role": role, "primary_theme": theme}
    return concepts


def load_entities() -> list[dict]:
    entities = []
    for folder in ("docs", "topics"):
        for path in sorted((ROOT / folder).glob("*.md")):
            metadata, body = parse_frontmatter(path)
            concepts = metadata.get("related_concepts") or []
            concepts = [
                "ai-data-center" if value == "aidc" else "factory-ontology" if value == "manufacturing-ontology" else value
                for value in concepts
            ]
            entities.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "metadata": metadata,
                    "body": body,
                    "concepts": concepts,
                }
            )
    return entities


def select_image(concept_id: str, primary_theme: str, inventory_by_id: dict) -> dict:
    image_id = IMAGE_RULES.get(concept_id, DEFAULT_IMAGE_BY_THEME[primary_theme])
    image = inventory_by_id.get(image_id)
    if not image:
        raise KeyError(f"Missing downloaded image {image_id} for {concept_id}")
    return image


def generic_details(title: str, role: str, theme: str) -> tuple[str, str, str]:
    theme_title = THEME_INFO[theme][0]
    definition = (
        f"{title}은(는) {role}을(를) 의미하며, "
        f"{theme_title} 전략을 설계하고 평가하는 개념으로 사용한다."
    )
    why = (
        f"LG그룹이 보유한 계열사별 자산을 {theme_title} 사업기회로 연결할 때 역할, 데이터, "
        "운영 책임과 성과지표를 명확히 구분하게 해준다."
    )
    boundary = (
        "인접 개념과 기술 요소를 무조건 포함하는 포괄어로 사용하지 않는다. 실제 데이터 흐름, "
        "운영 workflow, 고객 가치 또는 통제 책임이 확인되는 범위에서 적용한다."
    )
    return definition, why, boundary


def select_relevant_companies(
    concept_id: str,
    primary_theme: str,
    candidates: list[str],
) -> list[str]:
    if concept_id in CONCEPT_COMPANIES:
        return CONCEPT_COMPANIES[concept_id]
    override = CORE_RELATIONS.get(concept_id)
    if override:
        return override["companies"]
    supported = COMPANY_THEME_ROLES[primary_theme]
    selected = [company for company in candidates if company in supported]
    if not selected:
        selected = list(supported)
    return selected[:6]


def theme_relevance_reason(
    title: str,
    role: str,
    primary_theme: str,
    related_theme: str,
) -> str:
    if related_theme == primary_theme:
        return (
            f"**{title}**: {role}. "
            f"{PRIMARY_THEME_RELEVANCE[primary_theme]}"
        )
    return (
        f"{title}의 핵심 기능 — {role} — 이 이 테마로 확장되면 "
        f"{CROSS_THEME_RELEVANCE[related_theme]}"
    )


def company_role_reason(
    company: str,
    title: str,
    role: str,
    primary_theme: str,
) -> str:
    base_role = COMPANY_THEME_ROLES[primary_theme].get(company)
    if base_role is None:
        for theme_roles in COMPANY_THEME_ROLES.values():
            if company in theme_roles:
                base_role = theme_roles[company]
                break
    if base_role is None:
        base_role = f"{title} 관련 데이터·기술·사업 적용 가능성을 가진 주체다."
    lens_template = COMPANY_CONCEPT_LENS.get(
        company,
        "{role} 기능을 실제 사업·운영 환경에서 검증하는 역할이 예상된다.",
    )
    lens = lens_template.format(role=f"‘{role}’ 기능")
    return f"{base_role} {title}에서는 {lens}"


def yaml_frontmatter(data: dict) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000).strip()


def main() -> int:
    concepts = parse_taxonomy()
    entities = load_entities()
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    inventory_by_id = {
        item["image_id"]: item
        for item in inventory["images"]
        if item.get("status") == "downloaded"
    }

    occurrences: dict[str, list[dict]] = defaultdict(list)
    cooccurrence: dict[str, Counter] = defaultdict(Counter)
    for entity in entities:
        valid = [concept_id for concept_id in entity["concepts"] if concept_id in concepts]
        for concept_id in valid:
            occurrences[concept_id].append(entity)
            cooccurrence[concept_id].update(other for other in valid if other != concept_id)

    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    image_usage: dict[str, list[str]] = defaultdict(list)
    for concept_id, info in sorted(concepts.items()):
        related_entities = occurrences.get(concept_id, [])
        themes = []
        companies = []
        sources = []
        topics = []
        for entity in related_entities:
            metadata = entity["metadata"]
            for theme in metadata.get("related_themes") or [metadata.get("theme_id")]:
                if theme and theme not in themes:
                    themes.append(theme)
            for company in metadata.get("related_companies") or []:
                if company not in companies:
                    companies.append(company)
            for source in metadata.get("source_ids") or []:
                if source not in sources:
                    sources.append(source)
            if entity["path"].startswith("topics/") and metadata.get("id"):
                topics.append((metadata["id"], metadata.get("title") or metadata.get("question")))

        primary_theme = info["primary_theme"]
        if primary_theme not in themes:
            themes.insert(0, primary_theme)
        if not companies:
            primary_doc = next(
                (entity for entity in entities if entity["metadata"].get("theme_id") == primary_theme),
                None,
            )
            if primary_doc:
                companies = list(primary_doc["metadata"].get("related_companies") or [])[:4]
        relation_override = CORE_RELATIONS.get(concept_id)
        if relation_override:
            sources = relation_override["sources"]
        else:
            sources = sources[:12]
        companies = select_relevant_companies(concept_id, primary_theme, companies)

        related_concepts = [item for item, _ in cooccurrence[concept_id].most_common(6)]
        if not related_concepts:
            related_concepts = [
                item
                for item, candidate in concepts.items()
                if candidate["primary_theme"] == primary_theme and item != concept_id
            ][:4]

        image = select_image(concept_id, primary_theme, inventory_by_id)
        local_path = image["local_path"]
        concept_path = f"concepts/{concept_id}.md"
        image_usage[image["image_id"]].append(concept_path)

        definition, why, boundary = CORE_DETAILS.get(
            concept_id,
            generic_details(info["title"], info["role"], primary_theme),
        )
        source_note = ""
        if not sources:
            source_note = "\n> Source 보강 필요: 현재 docs/topics metadata에 직접 연결된 source_id가 없다.\n"

        frontmatter = {
            "id": f"concept_{concept_id.replace('-', '_')}",
            "type": "concept",
            "title": info["title"],
            "aliases": ALIASES.get(concept_id, []),
            "primary_theme": primary_theme,
            "related_themes": themes,
            "related_companies": companies,
            "source_ids": sources,
            "tags": [concept_id, primary_theme.replace("_", "-")],
        }
        theme_rows = "\n".join(
            f"| [[{THEME_INFO[theme][1]}]] | "
            f"{theme_relevance_reason(info['title'], info['role'], primary_theme, theme)} |"
            for theme in themes
            if theme in THEME_INFO
        )
        company_rows = "\n".join(
            f"| {COMPANY_NAMES.get(company, company)} | "
            f"{company_role_reason(company, info['title'], info['role'], primary_theme)} |"
            for company in companies
        )
        concept_links = "\n".join(f"- [[concepts/{item}]]" for item in related_concepts)
        source_links = (
            "\n".join(f"- [[sources/{source}]]" for source in sources)
            if sources
            else "- Source 보강 필요"
        )
        topic_links = (
            "\n".join(
                f"- [[topics/{next(Path(e['path']).stem for e in related_entities if e['metadata'].get('id') == topic_id)}|{title}]]"
                for topic_id, title in topics
            )
            if topics
            else "- 직접 연결된 Topic 없음"
        )
        caption = image.get("caption") or f"{info['title']} 관련 원본 이미지"
        markdown = f"""---
{yaml_frontmatter(frontmatter)}
---

# {info['title']}

<figure>
  <img src="{local_path}" alt="{info['title']} 관련 이미지" style="max-width:100%; border-radius:8px;" />
  <figcaption>{caption}</figcaption>
</figure>

## 1. Definition

{definition}

## 2. Why It Matters

{why}

## 3. How It Works

{info['role']}이라는 목적을 달성하려면 데이터 입력, 모델 또는 분석 계층, 업무·현장 시스템 연계, 실행 결과의 측정과 피드백이 연결되어야 한다. LG 전략에서는 기술 도입 여부보다 이 전체 loop가 반복 운영되고 내부 역량으로 축적되는지를 기준으로 본다.

## 4. LG Relevance

| 관련 테마 | 연결 이유 |
|---|---|
{theme_rows}

## 5. Related Companies

| 회사 | 관련 역할 |
|---|---|
{company_rows}

## 6. Related Concepts

{concept_links}

## 7. Related Topics

{topic_links}

## 8. Sources

{source_links}
{source_note}
## 9. Open Questions

- 이 개념이 고객이 구매할 수 있는 제품·서비스 또는 내부 운영성과로 전환되는 조건은 무엇인가?
- 데이터, 모델, workflow와 실행 책임 중 LG가 직접 통제해야 할 핵심 계층은 무엇인가?
- 성과를 검증할 대표 KPI와 추가 공개 근거는 무엇인가?
"""
        (CONCEPTS_DIR / f"{concept_id}.md").write_text(markdown, encoding="utf-8")
        generated.append(
            {
                "id": concept_id,
                "entity_id": frontmatter["id"],
                "title": info["title"],
                "primary_theme": primary_theme,
                "related_themes": themes,
                "related_companies": companies,
                "source_ids": sources,
                "related_concepts": related_concepts,
                "image_id": image["image_id"],
                "image_path": local_path,
                "path": concept_path,
            }
        )

    for item in inventory["images"]:
        additions = image_usage.get(item.get("image_id"), [])
        case_path = CASE_IMAGE_USAGE.get(item.get("image_id"))
        if case_path:
            additions.append(case_path)
        if additions:
            item["used_by"] = sorted(set((item.get("used_by") or []) + additions))
    INVENTORY_PATH.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")

    (ROOT / "data" / "concepts.json").write_text(
        json.dumps({"concepts": generated}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    by_theme: dict[str, list[dict]] = defaultdict(list)
    for item in generated:
        by_theme[item["primary_theme"]].append(item)
    index_lines = [
        "---",
        "id: concept_index",
        "type: index",
        "title: Concept Index",
        "---",
        "",
        "# Concept Index",
        "",
        f"총 {len(generated)}개 Concept를 primary theme 기준으로 정리한다.",
        "",
    ]
    map_lines = [
        "---",
        "id: concept_theme_map",
        "type: matrix",
        "title: Concept-Theme Map",
        "---",
        "",
        "# Concept-Theme Map",
        "",
        "| Concept | Primary Theme | Related Themes |",
        "|---|---|---|",
    ]
    for theme, (theme_title, _) in THEME_INFO.items():
        index_lines.extend([f"## {theme_title}", ""])
        for item in sorted(by_theme[theme], key=lambda value: value["title"].lower()):
            index_lines.append(f"- [[concepts/{item['id']}|{item['title']}]]")
            map_lines.append(
                f"| [[concepts/{item['id']}|{item['title']}]] | `{theme}` | "
                + ", ".join(f"`{value}`" for value in item["related_themes"])
                + " |"
            )
        index_lines.append("")
    (ROOT / "docs" / "84_concept_index.md").write_text("\n".join(index_lines), encoding="utf-8")
    (ROOT / "docs" / "81_concept_theme_map.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "generated_concepts": len(generated),
                "concepts_with_sources": sum(bool(item["source_ids"]) for item in generated),
                "concepts_needing_source": sum(not item["source_ids"] for item in generated),
                "images_reused": len(image_usage),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
