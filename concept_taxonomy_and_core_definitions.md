# LG AI Strategy Wiki — Concept Taxonomy & Core Definitions

> 목적: `docs/01~06` 문서를 기반으로 Codex가 `concepts/` 폴더를 일관되게 생성할 수 있도록 개념 체계, 핵심 정의, frontmatter 규칙, 생성 지시문을 정리한다.  
> 기준: 6대 테마 v2 구조. Theme 1은 `AI Data Center / Infra`, `AI Factory`는 Theme 2의 하위 Concept으로 관리한다.

---

## 1. Concept 설계 원칙

### 1.1 Concept는 “반복적으로 등장하는 의미 단위”만 만든다

Concept 문서는 단순 키워드 사전이 아니다. 여러 테마, 회사, 출처에서 반복적으로 등장하고, 전략 해석에 영향을 주는 개념만 독립 문서로 만든다.

예를 들어 `AI Data Center`, `AI Factory`, `Physical AI`, `Enterprise Ontology`, `AI Co-Scientist`는 독립 Concept으로 관리한다. 반면 특정 제품명, 단일 행사명, 일회성 수치는 `sources/` 또는 해당 docs 본문에서 관리한다.

### 1.2 Theme와 Concept를 구분한다

Theme는 전략 영역이고, Concept는 그 전략을 설명하는 개념이다.

```text
Theme = 전략적 사업기회 영역
Concept = Theme를 구성하거나 설명하는 핵심 개념
Company = Theme와 Concept를 실행하는 주체
Source = Theme, Concept, Company를 뒷받침하는 근거
```

### 1.3 Primary Theme을 반드시 지정한다

하나의 Concept는 여러 Theme에 걸쳐 등장할 수 있지만, 중심이 되는 Theme는 하나로 둔다.

예:

```yaml
primary_theme: physical_ai_smart_manufacturing
related_themes:
  - ai_data_center_infra
  - physical_ai_smart_manufacturing
  - global_ai_alliance_open_innovation
```

`AI Factory`는 Theme 1의 이름이 아니라 Theme 2의 하위 운영 모델이므로, `primary_theme`은 반드시 `physical_ai_smart_manufacturing`으로 둔다.

### 1.4 개념 경계가 중요한 항목은 명확히 분리한다

특히 아래 개념들은 혼동되기 쉽기 때문에 분리해서 관리한다.

| 구분 | 정의상 중심 | 구분 기준 |
|---|---|---|
| AI Data Center | GPU·전력·냉각·클라우드 운영 기반 | AI가 돌아가는 물리적·연산 인프라 |
| AI Factory | 제조·로봇·디지털트윈을 학습·검증·배포하는 운영 모델 | AI Data Center 위에서 작동하는 Physical AI workflow |
| Physical AI | 물리 세계에서 인식·판단·실행하는 AI | 공장, 로봇, 물류, 설비, 안전으로 확장 |
| Smart Manufacturing | 제조공정을 데이터와 AI로 최적화하는 체계 | 공정·품질·설비·물류의 제조 운영 관점 |
| Enterprise Ontology | 기업 데이터를 의미·관계 기반 객체로 모델링 | 전사 의사결정과 Agentic Operating Model의 기반 |
| Agentic Operating Model | Agent가 분석·계획·실행·평가를 반복하는 운영체계 | 개별 챗봇이 아니라 기업 운영 방식의 변화 |

---

## 2. 전체 Concept Taxonomy

## 2.1 Theme 1 — AI Data Center / Infra

| Concept ID | Title | 역할 | Primary Theme |
|---|---|---|---|
| ai-data-center | AI Data Center | AI 연산을 위한 데이터센터 인프라 | ai_data_center_infra |
| gpu-cloud | GPU Cloud | GPU 기반 AI 학습·추론 서비스 | ai_data_center_infra |
| high-density-gpu-rack | High-Density GPU Rack | 고밀도 GPU 서버 집적 구조 | ai_data_center_infra |
| data-center-cooling | Data Center Cooling | AI 데이터센터 냉각·열관리 | ai_data_center_infra |
| direct-to-chip-cooling | Direct-to-Chip Cooling | GPU/CPU 칩 직접 냉각 방식 | ai_data_center_infra |
| cdu | Coolant Distribution Unit | 수랭식 데이터센터의 냉각수 분배 장치 | ai_data_center_infra |
| immersion-cooling | Immersion Cooling | 액침냉각 기반 고밀도 냉각 방식 | ai_data_center_infra |
| dc-grid | DC Grid | 데이터센터 전력 효율을 높이는 직류 전력망 | ai_data_center_infra |
| ess-ups-for-aidc | ESS / UPS for AIDC | AI 데이터센터 전력 안정화 장치 | ai_data_center_infra |
| workload-orchestration | Workload Orchestration | AI workload와 전력·냉각 운영 최적화 | ai_data_center_infra |
| pue | PUE | 데이터센터 전력효율 지표 | ai_data_center_infra |
| compute-per-megawatt | Compute per Megawatt | 전력당 AI 연산 생산성 지표 | ai_data_center_infra |

---

## 2.2 Theme 2 — Physical AI / Smart Manufacturing

| Concept ID | Title | 역할 | Primary Theme |
|---|---|---|---|
| physical-ai | Physical AI | 물리 세계에서 인식·판단·실행하는 AI | physical_ai_smart_manufacturing |
| smart-manufacturing | Smart Manufacturing | 데이터·AI 기반 제조 운영 고도화 | physical_ai_smart_manufacturing |
| ai-factory | AI Factory | Physical AI 학습·시뮬레이션·검증·배포 운영 모델 | physical_ai_smart_manufacturing |
| digital-twin | Digital Twin | 공장·설비·제품의 가상 모델 | physical_ai_smart_manufacturing |
| manufacturing-intelligence | Manufacturing Intelligence | 제조 데이터를 AI 판단 체계로 전환 | physical_ai_smart_manufacturing |
| predictive-maintenance | Predictive Maintenance | 설비 이상탐지·예지보전 | physical_ai_smart_manufacturing |
| robotic-foundation-model | Robotic Foundation Model | 범용 로봇 행동 모델 | physical_ai_smart_manufacturing |
| industrial-humanoid | Industrial Humanoid | 제조·물류 현장용 휴머노이드 | physical_ai_smart_manufacturing |
| synthetic-data | Synthetic Data | 시뮬레이션 기반 AI 학습 데이터 | physical_ai_smart_manufacturing |
| robot-simulation | Robot Simulation | 로봇 학습·검증용 시뮬레이션 | physical_ai_smart_manufacturing |
| factory-ontology | Factory Ontology | 공장 객체·설비·공정 관계 모델 | physical_ai_smart_manufacturing |

---

## 2.3 Theme 3 — AI Mobility / SDV·AIDV

| Concept ID | Title | 역할 | Primary Theme |
|---|---|---|---|
| sdv | Software-Defined Vehicle | 소프트웨어 중심 차량 아키텍처 | ai_mobility_sdv_aidv |
| aidv | AI-Defined Vehicle | AI가 차량 경험·판단을 고도화하는 차량 | ai_mobility_sdv_aidv |
| ai-cabin | AI Cabin | 차량 내부 AI 경험 공간 | ai_mobility_sdv_aidv |
| in-vehicle-ai | In-Vehicle AI | 차량 내 AI 모델·서비스 | ai_mobility_sdv_aidv |
| in-cabin-sensing | In-Cabin Sensing | 운전자·탑승자 상태 인식 | ai_mobility_sdv_aidv |
| automotive-display | Automotive Display | 차량용 디스플레이·HMI | ai_mobility_sdv_aidv |
| adas | ADAS | 첨단 운전자 보조 시스템 | ai_mobility_sdv_aidv |
| autonomous-driving | Autonomous Driving | 자율주행 인지·판단·제어 | ai_mobility_sdv_aidv |
| v2x | V2X | 차량과 인프라·차량·보행자 간 통신 | ai_mobility_sdv_aidv |
| bms-bmts | BMS / BMTS | 배터리 관리·서비스 체계 | ai_mobility_sdv_aidv |
| battery-software | Battery Software | 배터리 진단·예측·최적화 SW | ai_mobility_sdv_aidv |
| on-device-ai | On-Device AI | 차량 내 엣지 AI 실행 | ai_mobility_sdv_aidv |

---

## 2.4 Theme 4 — Enterprise AX / Agentic Operating Model

| Concept ID | Title | 역할 | Primary Theme |
|---|---|---|---|
| enterprise-ontology | Enterprise Ontology | 전사 데이터를 의미·관계 기반 객체로 모델링 | enterprise_ax_agentic_operating_model |
| agentic-operating-model | Agentic Operating Model | Agent 기반 기업 운영체계 | enterprise_ax_agentic_operating_model |
| ai-cockpit | AI Cockpit | 경영진·운영조직의 AI 의사결정 화면 | enterprise_ax_agentic_operating_model |
| decision-intelligence | Decision Intelligence | 데이터·AI 기반 의사결정 체계 | enterprise_ax_agentic_operating_model |
| what-if-simulation | What-if Simulation | 시나리오별 결과 예측 | enterprise_ax_agentic_operating_model |
| data-foundation | Data Foundation | AX를 위한 데이터 기반 | enterprise_ax_agentic_operating_model |
| knowledge-graph | Knowledge Graph | 객체와 관계 기반 지식 그래프 | enterprise_ax_agentic_operating_model |
| agent-governance | Agent Governance | Agent 승인권·책임·감사 체계 | enterprise_ax_agentic_operating_model |
| llmops | LLMOps | LLM 서비스 운영·평가·배포 관리 | enterprise_ax_agentic_operating_model |
| ai-governance | AI Governance | AI 위험·규제·정책 관리 | enterprise_ax_agentic_operating_model |

---

## 2.5 Theme 5 — AI for Science: Bio·Materials·Battery

| Concept ID | Title | 역할 | Primary Theme |
|---|---|---|---|
| ai-for-science | AI for Science | 과학 R&D를 AI로 가속하는 접근 | ai_for_science_bio_materials_battery |
| ai-co-scientist | AI Co-Scientist | 연구자와 협업하는 AI 연구 파트너 | ai_for_science_bio_materials_battery |
| exaone-discovery | EXAONE Discovery | 신약·소재 후보 탐색 AI 플랫폼 | ai_for_science_bio_materials_battery |
| bio-intelligence | Bio Intelligence | 바이오·신약 연구 AI | ai_for_science_bio_materials_battery |
| materials-intelligence | Materials Intelligence | 소재 구조·물성 예측 AI | ai_for_science_bio_materials_battery |
| chemical-agentic-ai | Chemical Agentic AI | 화학 R&D Agentic AI | ai_for_science_bio_materials_battery |
| closed-loop-rnd | Closed-loop R&D | AI 제안과 실험 피드백의 반복 루프 | ai_for_science_bio_materials_battery |
| peptide-drug-discovery | Peptide Drug Discovery | 펩타이드 신약 후보 설계·검증 | ai_for_science_bio_materials_battery |
| battery-materials | Battery Materials | 배터리 핵심 소재 | ai_for_science_bio_materials_battery |
| materials-informatics | Materials Informatics | 소재 데이터 기반 탐색·예측 | ai_for_science_bio_materials_battery |
| patent-intelligence | Patent Intelligence | 특허 검색·분석·전략 AI | ai_for_science_bio_materials_battery |

---

## 2.6 Theme 6 — Global AI Alliance / Open Innovation Network

| Concept ID | Title | 역할 | Primary Theme |
|---|---|---|---|
| global-ai-alliance | Global AI Alliance | 글로벌 AI 기업과의 전략적 협력 | global_ai_alliance_open_innovation |
| open-innovation | Open Innovation | 외부 기술·스타트업·연구기관 협력 | global_ai_alliance_open_innovation |
| cvc | Corporate Venture Capital | 전략적 투자 기반 기술 옵션 확보 | global_ai_alliance_open_innovation |
| hybrid-ai-strategy | Hybrid AI Strategy | 자체·오픈·파트너 모델 조합 전략 | global_ai_alliance_open_innovation |
| industrial-ai-ecosystem | Industrial AI Ecosystem | 산업 AI 생태계 내 포지셔닝 | global_ai_alliance_open_innovation |
| partner-technology-transfer | Partner Technology Transfer | 외부 기술의 내부 이식 | global_ai_alliance_open_innovation |
| strategic-alliance-governance | Strategic Alliance Governance | 파트너십 관리와 의존도 통제 | global_ai_alliance_open_innovation |

---

## 3. 핵심 Concept 10개 정의 초안

아래 10개는 Wiki 전체의 개념 경계를 결정하는 핵심 Concept이다.  
Codex는 이 정의를 우선 반영하고, 나머지 Concept는 docs에서 추출해 템플릿에 맞춰 초안을 생성한다.

---

# 3.1 AI Data Center

```yaml
---
id: concept_ai_data_center
type: concept
title: AI Data Center
aliases:
  - AIDC
  - AI 데이터센터
  - AI Infrastructure Data Center
primary_theme: ai_data_center_infra
related_themes:
  - ai_data_center_infra
  - physical_ai_smart_manufacturing
  - ai_for_science_bio_materials_battery
  - global_ai_alliance_open_innovation
related_companies:
  - lg-uplus
  - lg-cns
  - lg-electronics
  - lg-energy-solution
  - lg-ai-research
source_ids:
  - src_lguplus_paju_aidc_20260607
  - src_lge_dcw_20260421
  - src_lgcns_data_center
tags:
  - ai-data-center
  - gpu
  - cooling
  - power
  - aidc
---
```

## Definition

AI Data Center는 대규모 AI 학습·추론을 위해 GPU, 고밀도 랙, 전력, 냉각, 네트워크, 클라우드 운영 소프트웨어를 통합한 데이터센터 인프라다. 기존 데이터센터가 범용 서버 공간과 네트워크를 제공하는 시설에 가까웠다면, AI Data Center는 고전력·고발열 AI workload를 안정적으로 처리하기 위한 특수 인프라에 가깝다.

## LG Relevance

LG그룹에서는 LG U+의 AIDC 운영, LG CNS의 데이터센터 설계·구축·운영, LG전자의 냉각·열관리, LG에너지솔루션의 ESS/UPS/DC Grid가 결합된다. AI Data Center는 Theme 1의 중심 개념이며, Theme 2의 AI Factory, Theme 5의 AI for Science, Theme 6의 NVIDIA 협력의 물리적 기반이 된다.

## Boundary

AI Data Center는 AI가 돌아가는 기반이다.  
AI Factory는 이 기반 위에서 제조·로봇·디지털트윈을 학습·검증·배포하는 운영 모델이다.

---

# 3.2 AI Factory

```yaml
---
id: concept_ai_factory
type: concept
title: AI Factory
aliases:
  - AI 팩토리
  - Physical AI Factory
  - Industrial AI Factory
primary_theme: physical_ai_smart_manufacturing
related_themes:
  - ai_data_center_infra
  - physical_ai_smart_manufacturing
  - global_ai_alliance_open_innovation
related_companies:
  - lg-electronics
  - lg-cns
  - lg-ai-research
  - lg-uplus
  - nvidia
  - skild-ai
source_ids:
  - src_nvidia_lg_ai_factory_20260607
  - src_lg_nvidia_map_20260608
  - src_lge_smart_factory_20260414
tags:
  - ai-factory
  - physical-ai
  - digital-twin
  - robot-simulation
---
```

## Definition

AI Factory는 제조 데이터, 로봇, 디지털트윈, 합성데이터, 시뮬레이션, AI 모델 학습·검증·배포를 하나의 workflow로 연결하는 Physical AI 운영 모델이다. 데이터센터 자체를 의미하는 것이 아니라, AI Data Center가 제공하는 GPU·전력·냉각·클라우드 기반 위에서 물리 세계 AI를 학습하고 실제 현장에 적용하는 실행 체계다.

## LG Relevance

LG그룹에서 AI Factory는 LG전자 Smart Factory, LG Smart Park, LG CNS Factova, NVIDIA Isaac/Omniverse/Cosmos/GR00T, Skild AI RFM과 연결된다. Theme 2의 핵심 하위 개념이며, Theme 1과 Theme 6을 연결하는 bridge concept이다.

## Boundary

AI Factory는 Theme 1의 테마명이 아니다.  
Primary Theme은 반드시 `physical_ai_smart_manufacturing`으로 둔다.

---

# 3.3 Physical AI

```yaml
---
id: concept_physical_ai
type: concept
title: Physical AI
aliases:
  - 물리 AI
  - Embodied AI
primary_theme: physical_ai_smart_manufacturing
related_themes:
  - physical_ai_smart_manufacturing
  - ai_mobility_sdv_aidv
  - global_ai_alliance_open_innovation
related_companies:
  - lg-electronics
  - lg-cns
  - lg-ai-research
  - lg-innotek
  - skild-ai
  - nvidia
source_ids:
  - src_lge_smart_factory_20260414
  - src_lgcns_skild_ai_20250616
  - src_lg_nvidia_map_20260608
tags:
  - physical-ai
  - robot
  - manufacturing
  - embodied-ai
---
```

## Definition

Physical AI는 AI가 디지털 정보만 처리하는 것을 넘어 공장, 설비, 로봇, 물류, 차량, 센서 등 물리 세계의 상태를 인식하고 판단하며 실행하는 AI를 의미한다. LLM이 언어와 문서를 이해하는 AI라면, Physical AI는 실제 환경에서 움직이고 조작하고 반응하는 AI에 가깝다.

## LG Relevance

LG그룹에서는 스마트팩토리, 로봇, 제조 물류, 품질 검사, 자율공장, 모빌리티 센싱 등과 연결된다. LG전자의 제조 경험, LG CNS의 제조 AX, LG AI연구원의 Physical Intelligence, Skild AI의 RFM, NVIDIA의 로봇 시뮬레이션 스택이 주요 연결점이다.

---

# 3.4 Smart Manufacturing

```yaml
---
id: concept_smart_manufacturing
type: concept
title: Smart Manufacturing
aliases:
  - 스마트 제조
  - Smart Factory
  - 스마트팩토리
primary_theme: physical_ai_smart_manufacturing
related_themes:
  - physical_ai_smart_manufacturing
  - enterprise_ax_agentic_operating_model
related_companies:
  - lg-electronics
  - lg-cns
  - lg-energy-solution
  - lg-display
  - lg-chem
source_ids:
  - src_lge_smart_factory_20260414
  - src_lg_smart_park_lighthouse_20220427
  - src_lgcns_factova_20260519
tags:
  - smart-manufacturing
  - smart-factory
  - manufacturing-ai
---
```

## Definition

Smart Manufacturing은 제조공정, 설비, 품질, 물류, 에너지, 작업자 데이터를 연결해 생산성과 품질을 높이는 데이터·AI 기반 제조 운영 체계다. 기존 자동화가 설비와 로봇 중심이었다면, Smart Manufacturing은 데이터와 AI가 공정 전체의 판단과 최적화에 참여한다.

## LG Relevance

LG전자는 글로벌 공장 운영 경험과 Smart Factory Solutions를 보유하고, LG CNS는 Factova 기반 제조 AX 플랫폼을 제공한다. LG Smart Park는 Lighthouse Factory 레퍼런스로, 디지털트윈·5G AGV·AI 검사·예지보전·물류 자동화의 실제 적용 사례다.

---

# 3.5 SDV

```yaml
---
id: concept_sdv
type: concept
title: Software-Defined Vehicle
aliases:
  - SDV
  - 소프트웨어 정의 차량
primary_theme: ai_mobility_sdv_aidv
related_themes:
  - ai_mobility_sdv_aidv
  - global_ai_alliance_open_innovation
related_companies:
  - lg-electronics
  - lg-innotek
  - lg-display
  - lg-energy-solution
  - lg-uplus
source_ids:
  - src_lge_ai_in_vehicle_20251217
  - src_lgdisplay_ces2026_20260105
  - src_lgensol_sdverse_20260403
tags:
  - sdv
  - mobility
  - vehicle-software
---
```

## Definition

SDV는 차량 기능과 사용자 경험이 하드웨어 고정 기능보다 소프트웨어, OTA 업데이트, 컴퓨팅 아키텍처, 클라우드 연결을 통해 지속적으로 개선되는 차량을 의미한다. 차량은 더 이상 일회성 제품이 아니라 업데이트 가능한 플랫폼이 된다.

## LG Relevance

LG그룹에서는 LG전자 VS의 IVI·AI Cockpit, LG디스플레이의 차량용 OLED·HMI, LG이노텍의 센싱·통신 부품, LG에너지솔루션의 배터리 SW, LG U+의 V2X·정밀측위가 SDV 전환과 연결된다.

---

# 3.6 AIDV

```yaml
---
id: concept_aidv
type: concept
title: AI-Defined Vehicle
aliases:
  - AIDV
  - AI 정의 차량
primary_theme: ai_mobility_sdv_aidv
related_themes:
  - ai_mobility_sdv_aidv
  - physical_ai_smart_manufacturing
  - global_ai_alliance_open_innovation
related_companies:
  - lg-electronics
  - lg-innotek
  - lg-display
  - lg-energy-solution
  - lg-uplus
  - lg-ai-research
source_ids:
  - src_lge_ai_in_vehicle_20251217
  - src_lginnotek_ces2026_aidv_20260106
  - src_lg_nvidia_map_20260608
tags:
  - aidv
  - ai-mobility
  - in-vehicle-ai
---
```

## Definition

AIDV는 SDV 위에 AI 판단, 인캐빈 센싱, 운전자·탑승자 이해, 자율주행 보조, 개인화 경험, 배터리·정비 예측을 결합한 차량 개념이다. SDV가 소프트웨어 중심 차량이라면, AIDV는 AI가 차량 경험과 운영을 지속적으로 고도화하는 차량이다.

## LG Relevance

LG전자는 AI-powered in-vehicle solutions를 통해 차량 내부 AI 경험을, LG이노텍은 카메라·LiDAR·Radar·통신·조명을 통해 외부 인지와 연결성을, LG디스플레이는 차량용 HMI를, LG에너지솔루션은 BMS/BMTS와 배터리 SW를 담당한다.

---

# 3.7 Enterprise Ontology

```yaml
---
id: concept_enterprise_ontology
type: concept
title: Enterprise Ontology
aliases:
  - 기업 온톨로지
  - LG Ontology
  - Business Ontology
primary_theme: enterprise_ax_agentic_operating_model
related_themes:
  - enterprise_ax_agentic_operating_model
  - global_ai_alliance_open_innovation
related_companies:
  - lg-corp
  - lg-cns
  - lg-ai-research
  - palantir
source_ids:
  - src_lgcorp_silicon_valley_20260407
  - src_lgcns_palantir_20260312
  - src_lgcns_ax_platform
tags:
  - ontology
  - knowledge-graph
  - enterprise-ax
---
```

## Definition

Enterprise Ontology는 제품, 고객, 공장, 설비, 부품, 협력사, 주문, 재고, 원가, 품질, R&D 과제 같은 기업의 핵심 객체와 그 관계를 정의하는 의미 체계다. 단순 데이터 통합이나 RAG 인덱스가 아니라, AI가 기업 운영을 이해하고 시뮬레이션하며 의사결정할 수 있도록 비즈니스 세계를 구조화하는 모델이다.

## LG Relevance

LG그룹에서는 여러 계열사의 ERP, MES, PLM, SCM, CRM, 재무, R&D 데이터를 하나의 의미 체계로 연결하기 위한 기반이다. Palantir식 ontology와 LG CNS AX Platform, EXAONE 기반 Agent를 연결하는 핵심 개념이다.

---

# 3.8 Agentic Operating Model

```yaml
---
id: concept_agentic_operating_model
type: concept
title: Agentic Operating Model
aliases:
  - Agentic AI Operating Model
  - AI 운영체계
  - Agentic Workflow
primary_theme: enterprise_ax_agentic_operating_model
related_themes:
  - enterprise_ax_agentic_operating_model
  - physical_ai_smart_manufacturing
  - ai_for_science_bio_materials_battery
related_companies:
  - lg-corp
  - lg-cns
  - lg-ai-research
  - lg-electronics
  - lg-energy-solution
source_ids:
  - src_lge_strategy_ax_20260108
  - src_lgcns_ax_platform
  - src_lgcns_ax_consulting
tags:
  - agentic-ai
  - enterprise-ax
  - workflow
---
```

## Definition

Agentic Operating Model은 AI Agent가 단순 질의응답을 넘어 목표를 이해하고, 계획을 세우고, 데이터를 분석하고, 시뮬레이션을 수행하고, 실행을 제안하며, 결과를 평가하는 기업 운영 모델이다. 핵심은 개별 챗봇이 아니라 Planner, Analyst, Simulator, Executor, Evaluator 같은 역할을 가진 Agent들이 기업 프로세스에 연결되는 것이다.

## LG Relevance

LG그룹에서는 원가, 수요, 재고, 생산계획, 품질, R&D 포트폴리오, 경영 Cockpit을 연결하는 운영 방식으로 적용될 수 있다. 이 모델이 작동하려면 Enterprise Ontology, Data Foundation, LLMOps, AI Governance가 함께 설계되어야 한다.

---

# 3.9 AI Co-Scientist

```yaml
---
id: concept_ai_co_scientist
type: concept
title: AI Co-Scientist
aliases:
  - AI 공동 과학자
  - AI Research Partner
primary_theme: ai_for_science_bio_materials_battery
related_themes:
  - ai_for_science_bio_materials_battery
  - global_ai_alliance_open_innovation
related_companies:
  - lg-ai-research
  - lg-chem
  - lg-energy-solution
  - lg-household-health-care
  - dd-pharmatech
source_ids:
  - src_lgai_exaone_discovery_patent_20260203
  - src_lgai_dd_pharmatech_20260617
  - src_lgai_materials_intelligence
tags:
  - ai-for-science
  - ai-co-scientist
  - r-and-d
---
```

## Definition

AI Co-Scientist는 연구자의 질문을 이해하고, 논문·특허·분자구조·실험 데이터를 바탕으로 후보물질, 실험 설계, 물성 예측, 안전성 검토, 다음 실험 방향을 제안하는 AI 연구 파트너다. 연구자를 대체하는 도구가 아니라, 연구자의 탐색 범위를 넓히고 실험 우선순위를 정하는 역할을 한다.

## LG Relevance

LG AI Research의 EXAONE Discovery, Bio Intelligence, Materials Intelligence와 연결된다. LG화학, LG에너지솔루션, LG생활건강은 AI가 제안한 후보를 실험·검증·상용화하는 필드를 제공한다. D&D Pharmatech 협력은 AI 후보 설계와 실험 검증을 연결하는 대표적 사례다.

---

# 3.10 Global AI Alliance

```yaml
---
id: concept_global_ai_alliance
type: concept
title: Global AI Alliance
aliases:
  - 글로벌 AI 제휴
  - AI Alliance
  - Strategic AI Partnership
primary_theme: global_ai_alliance_open_innovation
related_themes:
  - ai_data_center_infra
  - physical_ai_smart_manufacturing
  - ai_mobility_sdv_aidv
  - enterprise_ax_agentic_operating_model
  - ai_for_science_bio_materials_battery
  - global_ai_alliance_open_innovation
related_companies:
  - lg-corp
  - lg-technology-ventures
  - lg-ai-research
  - lg-cns
  - lg-electronics
  - lg-energy-solution
  - nvidia
  - skild-ai
  - palantir
  - qualcomm
  - sdverse
  - dd-pharmatech
source_ids:
  - src_lg_nvidia_map_20260608
  - src_lgcorp_silicon_valley_20260407
  - src_lgcns_palantir_20260312
  - src_lgcns_skild_ai_20250616
tags:
  - global-ai-alliance
  - open-innovation
  - partnership
  - cvc
---
```

## Definition

Global AI Alliance는 LG그룹이 NVIDIA, Skild AI, Palantir, Qualcomm, SDVerse, D&D Pharmatech 등 글로벌 AI·로봇·데이터·모빌리티·바이오 파트너와 협력해 내부에 부족한 원천기술을 빠르게 확보하고, 이를 LG의 산업 자산에 적용하는 전략이다.

## LG Relevance

이 개념은 1~5번 테마를 가속하는 횡단형 enabling concept이다. NVIDIA는 AI 인프라·Physical AI·Mobility, Skild AI는 로봇 파운데이션 모델, Palantir는 Enterprise Ontology, Qualcomm·SDVerse는 배터리 SW, D&D Pharmatech는 AI 신약 검증 루프와 연결된다.

---

## 4. Concept 문서 템플릿

Codex는 모든 Concept 파일을 아래 구조로 생성한다.

```markdown
---
id: concept_[kebab_case_without_hyphen_if_needed]
type: concept
title: [Concept Title]
aliases:
  - [Alias 1]
  - [Alias 2]
primary_theme: [theme_id]
related_themes:
  - [theme_id]
related_companies:
  - [company_id]
source_ids:
  - [source_id]
tags:
  - [tag]
---

# [Concept Title]

## 1. Definition

개념을 3~5문장으로 정의한다.

## 2. Why It Matters

LG그룹 AI 전략에서 이 개념이 왜 중요한지 설명한다.

## 3. How It Works

개념의 작동 방식, 구성요소, 적용 구조를 설명한다.

## 4. LG Relevance

| 관련 테마 | 연결 이유 |
|---|---|

## 5. Related Companies

| 회사 | 관련 역할 |
|---|---|

## 6. Related Concepts

- [[concepts/...]]
- [[concepts/...]]

## 7. Sources

- [[sources/...]]

## 8. Open Questions

- 아직 모호한 부분
- 추가 리서치 필요 사항
```

---

## 5. Codex 작업 지시문

아래 내용을 Codex에 그대로 전달한다.

```text
작업 목표:
docs/01~06 문서를 기준으로 concepts/ 폴더를 생성하고, 각 Concept MD 파일을 작성한다.

입력 문서:
- docs/01_ai_data_center_infra.md
- docs/02_physical_ai_smart_manufacturing.md
- docs/03_ai_mobility_sdv_aidv.md
- docs/04_enterprise_ax_agentic_operating_model.md
- docs/05_ai_for_science_bio_materials_battery.md
- docs/06_global_ai_alliance_open_innovation.md
- concept_taxonomy_and_core_definitions.md

작업 규칙:
1. 각 docs 문서의 frontmatter에 있는 related_concepts를 기준으로 concept 파일을 생성한다.
2. 파일명은 kebab-case로 한다. 예: concepts/ai-factory.md
3. 모든 concept 문서는 _templates/template_concept.md 구조를 따른다.
4. 각 concept의 frontmatter에는 id, type, title, aliases, primary_theme, related_themes, related_companies, source_ids, tags를 넣는다.
5. `concept_taxonomy_and_core_definitions.md`의 taxonomy를 우선 기준으로 삼는다.
6. 핵심 10개 Concept는 `concept_taxonomy_and_core_definitions.md`의 정의를 우선 반영한다.
7. 나머지 Concept는 docs/01~06의 관련 본문과 Source Notes를 참고해 초안을 작성한다.
8. source_ids는 docs의 frontmatter, Source Notes, Appendix C를 참고해 연결한다.
9. docs 본문에서 해당 개념이 등장하는 부분은 [[concepts/개념명]] 형태로 링크한다.
10. concept 문서 본문에는 원격 이미지 URL을 새로 추가하지 않는다. 이미지는 docs에서 관리한다.
11. 개념 정의가 불확실하거나 직접 출처가 약한 경우 `검증 필요`라고 표시한다.
12. AI Factory는 Theme 1이 아니라 Theme 2의 하위 Concept으로 둔다.
13. AI Data Center는 Theme 1의 primary Concept으로 둔다.
14. Palantir는 Theme 4의 Enterprise Ontology와 Theme 6의 Global AI Alliance에 연결하되, Theme 4의 중심을 특정 벤더 도입으로 쓰지 않는다.
15. NVIDIA는 Theme 1·2·3·6에 연결하되, Theme 1과 2에서는 보조 근거로 사용하고 LG 계열사 자산을 우선 설명한다.
16. 중복 정의를 피하고, 개념 간 경계가 명확하도록 작성한다.

검증:
1. concepts/*.md 전체에 primary_theme이 누락된 문서가 없는지 확인한다.
2. `AI Factory`가 docs/01의 Theme로 쓰이지 않았는지 확인한다.
3. `ai_infra_factory`라는 구 ID가 남아 있지 않은지 검색한다.
4. docs/01~06의 related_concepts와 concepts/ 파일명이 일치하는지 확인한다.
5. 각 concept에 최소 1개 이상의 related_theme과 related_company가 있는지 확인한다.
6. 각 concept에 source_ids가 없으면 `source_ids: []`로 두고 본문에 `Source 보강 필요`라고 표시한다.
```

---

## 6. 권장 생성 순서

Codex는 아래 순서로 concept 파일을 만든다.

```text
1. 핵심 10개 Concept 먼저 생성
   - ai-data-center
   - ai-factory
   - physical-ai
   - smart-manufacturing
   - sdv
   - aidv
   - enterprise-ontology
   - agentic-operating-model
   - ai-co-scientist
   - global-ai-alliance

2. Theme 1 Concepts 생성
3. Theme 2 Concepts 생성
4. Theme 3 Concepts 생성
5. Theme 4 Concepts 생성
6. Theme 5 Concepts 생성
7. Theme 6 Concepts 생성
8. 중복 파일·동의어 정리
9. docs/01~06 본문 링크 보강
10. concept_theme_map 자동 생성
```

---

## 7. 자동 생성 산출물

Concept 생성 후 Codex가 다음 파일도 자동 생성한다.

```text
docs/81_concept_theme_map.md
docs/84_concept_index.md
data/concepts.json
```

### data/concepts.json 예시

```json
{
  "concepts": [
    {
      "id": "ai-data-center",
      "title": "AI Data Center",
      "primary_theme": "ai_data_center_infra",
      "related_themes": [
        "ai_data_center_infra",
        "physical_ai_smart_manufacturing"
      ],
      "related_companies": [
        "lg-uplus",
        "lg-cns",
        "lg-electronics",
        "lg-energy-solution"
      ],
      "source_ids": [
        "src_lguplus_paju_aidc_20260607",
        "src_lge_dcw_20260421"
      ]
    }
  ]
}
```

---

## 8. 최종 검증 체크리스트

- [ ] `concepts/` 폴더가 생성되었는가?
- [ ] 핵심 10개 Concept가 작성되었는가?
- [ ] 모든 Concept에 frontmatter가 있는가?
- [ ] 모든 Concept에 `primary_theme`이 있는가?
- [ ] `AI Factory`의 primary_theme이 `physical_ai_smart_manufacturing`인가?
- [ ] `AI Data Center`의 primary_theme이 `ai_data_center_infra`인가?
- [ ] `ai_infra_factory` 구 ID가 제거되었는가?
- [ ] docs/01~06의 related_concepts와 concepts 파일명이 일치하는가?
- [ ] docs 본문에 `[[concepts/...]]` 링크가 추가되었는가?
- [ ] 중복 개념이 없는가?
- [ ] Source가 약한 개념은 `Source 보강 필요`로 표시되었는가?
