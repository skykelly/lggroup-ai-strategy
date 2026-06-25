---
id: doc_enterprise_ax_agentic_operating_model
type: doc
title: Enterprise AX / Agentic Operating Model
theme_id: enterprise_ax_agentic_operating_model
status: draft
updated: 2026-06-21
related_concepts:
  - enterprise-ontology
  - agentic-operating-model
  - ai-cockpit
  - decision-intelligence
  - what-if-simulation
  - data-foundation
  - knowledge-graph
  - agent-governance
  - llmops
  - ai-governance
related_companies:
  - lg-corp
  - lg-ai-research
  - lg-cns
  - lg-electronics
  - lg-energy-solution
  - lg-display
  - lg-chem
  - lg-innotek
  - lg-uplus
  - lg-household-health-care
  - palantir
source_ids:
  - src_lgcorp_silicon_valley_20260407
  - src_lge_strategy_ax_20260108
  - src_lgcns_palantir_20260312
  - src_lgcns_ax_platform
  - src_lgcns_ax_consulting
  - src_lgcns_ax_fair_20260527
  - src_lgdisplay_ai_productivity_20250805
  - src_lgensol_ax_productivity_20260413
  - src_lgchem_one_agent_20260528
tags:
  - enterprise-ax
  - agentic-ai
  - ontology
  - decision-intelligence
  - ai-operating-model
  - ai-governance
  - value-up
---

# Enterprise AX / Agentic Operating Model

## 1. Executive Summary

Enterprise AX / Agentic Operating Model은 LG그룹의 경영·운영 방식을 AI 중심의 전사 운영체계로 재설계하는 테마다. 핵심은 개별 직원의 생산성 도구를 넘어, 제품·고객·공장·공급망·재무·R&D·구매·물류 데이터를 하나의 의미 체계로 연결하고, [[concepts/agentic-operating-model]]이 예측·시뮬레이션·제안·실행·평가를 반복하도록 만드는 것이다.

이 테마는 외부 매출형 신사업보다 **그룹 밸류업**에 가깝다. 원가율, 재고일수, 납기, 품질, 생산성, R&D 리드타임, 현금전환주기, 의사결정 속도를 개선하는 것이 핵심 성과다. [[companies/lg-corp]]는 그룹 AX 방향과 포트폴리오 우선순위를 조정하고, [[companies/lg-ai-research]]는 EXAONE 계열 모델과 Advanced Agent 기술을 제공하며, [[companies/lg-cns]]는 ERP·MES·PLM·SCM·CRM과 AI 플랫폼을 연결하는 구현 계층을 맡는다.

이 문서에서 Palantir는 특정 벤더 도입 자체가 아니라 [[concepts/enterprise-ontology]]와 AI 기반 의사결정 체계의 벤치마크로 다룬다. 즉, 테마의 중심은 “Palantir 도입”이 아니라 **그룹 운영체계를 전사 데이터·온톨로지·Agentic AI 기반으로 바꾸는 것**이다.

## 2. AI Market Landscape & Why Now

### 2.1 기업 AI는 개인 업무도구에서 운영체계로 이동

생성형 AI 도입 초기에는 문서 작성, 번역, 요약, 코딩 지원 같은 개인 생산성 개선이 중심이었다. 하지만 대기업 관점에서 더 큰 가치는 개인 업무 효율보다 경영·운영 프로세스 전체를 바꾸는 데 있다. 수요예측, 생산계획, 공급망, 원가, 품질, 재무, R&D 의사결정은 여러 시스템과 데이터가 연결되어야 하므로, 단순 챗봇이나 RAG만으로는 전사 최적화를 만들기 어렵다.

LG CNS는 AX가 DX를 넘어 AI로 업무 방식, 의사결정, 조직 구조를 바꾸는 전사 변화라고 설명한다. 특히 Agentic AI는 단순 응답이나 보고서 생성을 넘어 목표를 달성하기 위해 스스로 계획하고 실행하며 결과를 평가하는 방향으로 발전하고 있다.

### 2.2 Agentic AI와 AX는 기업 운영의 핵심 경쟁력이 된다

LG CNS AX 자료는 Agentic AI가 기업 운영에 적용될 때 반복 업무 자동화, 운영 효율 개선, 고부가 업무 집중을 가능하게 하며, 단순 기술 전환이 아니라 일하는 방식 자체를 바꾸는 변화라고 설명한다. 또한 한국 기업들이 AX를 계획하거나 실행하고 있으나, AI 전문인력 부족, 높은 초기 비용, 생성형 AI 전환 전문성 부족을 주요 장애로 인식하고 있다고 정리한다.

이 흐름에서 중요한 것은 AI를 빠르게 도입하는 것이 아니라, **운영 데이터, 업무 프로세스, 승인권, 보안, 거버넌스, 비용 관리**를 함께 설계하는 것이다. LG그룹처럼 다양한 제조·소재·통신·서비스 계열사를 보유한 기업에서는 이 통합 운영체계의 가치가 더 크다.

### 2.3 전사 데이터와 온톨로지가 AI 의사결정의 기반이 된다

LG Corp. 공식 발표에 따르면 구광모 회장은 Palantir CEO Alex Karp와 만나 Ontology, 즉 AI·데이터 기반 의사결정 프레임워크와 제조·산업 환경의 혁신 사례를 논의했다. Digital Today의 LG CNS–Palantir 보도는 Palantir Foundry가 분산된 기업 데이터를 통합·정제해 데이터 기반 운영체계를 구축하고, AIP가 통합 데이터 환경과 생성형 AI를 결합해 실시간 의사결정을 지원한다고 설명한다.

이 관점에서 온톨로지는 단순 데이터 카탈로그가 아니다. 제품, 공장, 설비, 주문, 재고, 협력사, 원가, 고객, 프로젝트 같은 비즈니스 객체와 관계를 정의해 AI가 기업 운영을 이해하고 시뮬레이션할 수 있게 만드는 구조다.

<figure>
  <img src="assets/images/lgcns_knowledge_data_pipeline.png" alt="Knowledge Data pipeline: ingestion, processing, transformation, knowledge base. 전사 데이터·지식화·RAG 체계와 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Knowledge Data pipeline: ingestion, processing, transformation, knowledge base. 전사 데이터·지식화·RAG 체계와 연결된다. 출처: <a href="https://www.lgcns.com/en/service/ai/ax-platform">LG CNS AX Platform</a></small></figcaption>
</figure>

## 3. Business Opportunities

| 기회 | 설명 | 관련 계열사 | 보유 자산 |
|---|---|---|---|
| LG형 Enterprise Ontology | 제품·고객·공장·설비·원가·재고·협력사·R&D 과제를 연결하는 그룹 공통 의미 체계 | LG Corp., LG CNS, LG AI연구원, 전 계열사 | ERP/MES/PLM/SCM/CRM, 제조·판매·재무 데이터, EXAONE |
| 경영 Cockpit / Decision Intelligence | 경영진이 수익성, 재고, 공급망, 품질, 원가 변동을 실시간으로 보고 시뮬레이션하는 의사결정 환경 | LG Corp., LG CNS, LG전자, LG에너지솔루션, LG디스플레이 | 경영 KPI, 재무 데이터, 운영 데이터, AI dashboard |
| Agentic Workflow Automation | Planner, Analyst, Simulator, Executor, Evaluator Agent가 업무 프로세스를 분석·제안·실행·평가 | LG CNS, LG AI연구원, 전 계열사 | AX Platform, AgenticWorks, LLMOps, workflow data |
| 원가·수익성 시뮬레이션 | 환율, 원자재, 물류비, 판가, 생산량 변화에 따른 제품·사업별 손익 시뮬레이션 | LG전자, LG에너지솔루션, LG화학, LG디스플레이 | 원가 데이터, 구매 데이터, 재무 데이터, SCM |
| 수요·공급망·재고 최적화 | 지역·채널·고객별 수요예측과 생산·물류·재고 계획 자동 조정 | LG전자, LG생활건강, LG이노텍, LG디스플레이 | 판매 데이터, 채널 데이터, 물류 데이터, 고객 데이터 |
| R&D·제품개발 Agent | 특허·논문·품질·VOC·PLM 데이터를 연결해 과제 우선순위와 설계 변경 영향을 분석 | LG AI연구원, LG전자, LG화학, LG에너지솔루션 | EXAONE, PLM, R&D knowledge, 품질 데이터 |
| AI Governance / LLMOps | 모델, 데이터, 권한, 보안, 비용, 성능을 관리하는 운영 체계 | LG CNS, LG Corp., 각 계열사 IT/보안 조직 | AX Platform, LLMOps, governance policy |
| One-Agent-Per-Employee | 직원별 맞춤형 AI Agent로 문서, 보고, 데이터 분석, 구매, 일정, 정책 안내 등 업무 자동화 | LG화학, LG디스플레이, 전 계열사 | 사내 지식, 문서, 업무 프로세스, EXAONE 기반 Agent |

### 3.1 Group AX Direction / Ontology / Palantir

* 내용 요약
  - 그룹 AX의 출발점은 특정 솔루션 도입이 아니라, 제품·공장·설비·원가·고객 등 핵심 비즈니스 객체를 온톨로지로 연결하는 것이다.
  - Palantir는 벤더 자체보다 전사 데이터 통합, 의사결정 객체화, 실시간 운영체계의 벤치마크로 해석하는 것이 적절하다.
  - 목표는 경영진이 수익성·공급망·품질·원가 리스크를 실시간으로 보고, what-if 시뮬레이션 기반으로 빠르게 판단하는 체계를 만드는 것이다.


<figure>
  <img src="https://www.asiae.co.kr/news/img_view.htm?img=2026040709445416262_1775522694.jpg" alt="이미지 URL 확보 필요." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>구광모 LG Corp. 대표와 Palantir CEO Alex Karp의 기념 사진. LG그룹 AX의 온톨로지·의사결정 체계 벤치마킹과 연결된다. 출처: <a href="https://www.asiae.co.kr/en/article/2026040709471239793">Asia Business Daily / LG Corp photo</a></small></figcaption>
</figure>

### 3.2 LG Electronics AX Direction

* 내용 요약
  - LG전자 AX는 개별 업무 자동화가 아니라 개발·구매·생산·SCM·판매·서비스를 연결하는 end-to-end AI-driven operations 전환이다.
  - LGenie와 EXAONE 기반 Agent 플랫폼은 조직 전반의 업무 속도, 생산성, 실행력을 높이는 공통 AI 운영 계층으로 확장될 수 있다.
  - 핵심 사업기회는 QCD 개선, 의사결정 속도 향상, 반복 보고·분석의 자동화, 운영 데이터 기반 수익성 개선이다.


<figure>
  <img src="https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/corporate/lg-electronics-ceo-sets-strategic-direction-for-profit-driven-growth-prioritizing-speed-and-action/press-setting-image-desktoptablet-koreapressconference-1440.png" alt="LG Electronics CEO Lyu Jae-cheol speaks at a press briefing. AX를 통한 end-to-end AI-driven operations, speed, productivity, execution 방향과 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Electronics CEO Lyu Jae-cheol speaks at a press briefing. AX를 통한 end-to-end AI-driven operations, speed, productivity, execution 방향과 연결된다. 출처: <a href="https://www.lg.com/global/newsroom/news/corporate/lg-electronics-ceo-sets-strategic-direction-for-profit-driven-growth-prioritizing-speed-and-action/">LG Electronics Newsroom</a></small></figcaption>
</figure>

### 3.3 Affiliate AX Cases

* 내용 요약
  - LG디스플레이, LG에너지솔루션, LG화학 사례는 AX가 설계·제조·품질·사무·R&D·거버넌스까지 확산되고 있음을 보여준다.
  - 계열사별 AX 사례는 개별 성공사례로 끝내지 말고, 그룹 공통의 생산성 개선 패턴과 운영 모델로 추상화해야 한다.
  - 성과지표는 생산성, 품질 개선 리드타임, 제조 운영 효율, 사무 자동화, AI 거버넌스 체계로 관리하는 것이 적절하다.


<figure>
  <img src="assets/images/lgdisplay_ai_transformation_plan.png" alt="LG Display AI Transformation plan infographic. 개발, 제조, 사무 업무에서 생산성 개선을 설명한다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Display AI Transformation plan infographic. 개발, 제조, 사무 업무에서 생산성 개선을 설명한다. 출처: <a href="https://www.koreatimes.co.kr/business/tech-science/20250805/lg-display-eyes-30-improvement-in-productivity-through-ai">The Korea Times / LG Display courtesy</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgdisplay_hi_d_assistant.jpg" alt="LG Display Hi-D AI assistant demonstration. 지식검색, 실시간 통역, 회의록 생성 등 사무 AX와 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Display Hi-D AI assistant demonstration. 지식검색, 실시간 통역, 회의록 생성 등 사무 AX와 연결된다. 출처: <a href="https://www.koreatimes.co.kr/business/tech-science/20250805/lg-display-eyes-30-improvement-in-productivity-through-ai">The Korea Times / LG Display courtesy</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgenergy_ceo_ax_productivity.jpg" alt="LG Energy Solution CEO Kim Dong-myung. AX 기반 생산성 개선과 AI Governance Committee 방향과 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG Energy Solution CEO Kim Dong-myung. AX 기반 생산성 개선과 AI Governance Committee 방향과 연결된다. 출처: <a href="https://www.mk.co.kr/en/business/12015637">Maeil Business News</a></small></figcaption>
</figure>

> **이미지 URL 확보 필요**  
> LG Chem one-person-one-agent 교육/AX 문화 확산 관련 이미지. 원문 이미지 URL 직접 확보 필요.  
> 원문: [Seoul Economic Daily / LG Chem AX article](https://en.sedaily.com/news/2026/05/28/lg-chem-completes-ai-training-for-half-of-office-workforce)

---

### 3.4 LG CNS Claude Enterprise 도입 / KBIZ 중소기업 AI 상생

* 내용 요약
  - LG CNS는 2026년 6월 앤트로픽의 Claude Enterprise를 도입 계약 체결하고 LG그룹 전 계열사에 확산할 계획을 발표했다([[sources/src_lgcns_anthropic_claude_enterprise_20260609]]). 사내 전 직원에게 Claude 접속을 개방하고 개발·문서 작성·분석·협업 분야의 생성형 AI 기반 업무 혁신을 추진한다.
  - 이는 EXAONE 계열 자체 모델과 외부 파운데이션 모델(Claude)을 병용하는 Hybrid AI Strategy를 실행하는 사례이며, 외부 모델을 그룹 공통 Agentic 인프라에 연결하는 방향을 보여준다.
  - LG CNS는 2026년 6월 중소기업중앙회(KBIZ)와 '중소기업 AI 확산을 위한 대·중소 상생협력 모델 발굴' 업무협약을 체결했다([[sources/src_lgcns_kbiz_ax_20260617]]). 최대 30억 원 사업 규모로 선정 기업에 최대 12개월 AX 구축을 지원하며, AGV·AMR·로봇·클라우드를 포괄하는 하드웨어·소프트웨어 통합 지원을 제공한다.
  - LG CNS의 연간 약 20억 원 지원은 교육·기술·유통·마케팅 분야 중소기업 AI 역량 강화로 이어지며, 이는 Enterprise AX 역량을 외부 생태계로 확장하는 사업 모델이다.

### 3.5 LG CNS AX Platform

* 내용 요약
  - LG CNS AX Platform은 기업 AI 서비스를 개발·배포·운영·모니터링·관리하기 위한 전사 AI 운영 인프라다.
  - Knowledge Lake, LLMOps, 보안·권한·거버넌스, 운영 모니터링을 묶어 Agentic AI가 실제 업무 시스템과 연결될 수 있는 기반을 제공한다.
  - 그룹 내부 표준 플랫폼으로 활용하면서, 외부 고객 대상 AX 컨설팅·구축·운영 사업으로 확장할 수 있다.


<figure>
  <img src="assets/images/lgcns_ax_platform_operations.png" alt="LG CNS AX Platform: AI service operations, monitoring, LLMOps. 운영·모니터링·거버넌스 레이어와 연결된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG CNS AX Platform: AI service operations, monitoring, LLMOps. 운영·모니터링·거버넌스 레이어와 연결된다. 출처: <a href="https://www.lgcns.com/en/service/ai/ax-platform">LG CNS AX Platform</a></small></figcaption>
</figure>

## 4. LG Group Strategic Meaning

### 4.1 그룹 운영체계를 AI 중심으로 바꾼다

Theme 4의 본질은 “AI 도구를 많이 도입한다”가 아니다. LG그룹의 R&D, 구매, 생산, 공급망, 판매, 재무, 고객 데이터를 하나의 의미 체계로 연결하고, AI가 전사 최적화를 제안·실행·검증하는 운영체계를 만드는 것이다.

```text
기존: 부서별 데이터 → 사람이 취합 → 보고서 작성 → 회의 → 의사결정 → 실행 → 사후 분석
전환: 전사 데이터/온톨로지 → AI 예측·시뮬레이션 → Agent 제안 → 인간 승인/조정 → 실행 자동화 → 결과 학습
```

### 4.2 제조·소재·전장·통신 계열사의 운영 데이터를 공통 자산화한다

LG그룹은 전자, 배터리, 디스플레이, 화학, 부품, 통신, 생활소비재 등 서로 다른 산업 데이터를 보유하고 있다. 지금까지 이 데이터는 각 계열사의 ERP, MES, PLM, SCM, CRM, 재무 시스템에 분산되어 있었다. Enterprise AX는 이 데이터를 단순 통합하는 것이 아니라, 의미와 관계를 부여해 의사결정 가능한 객체로 바꾸는 작업이다.

예를 들어 `제품-부품-공장-협력사-원가-품질-고객-재고`가 연결되면, 특정 부품 가격 상승이 어느 제품군의 수익성에 영향을 주는지, 어느 공장의 생산계획을 조정해야 하는지, 어떤 대체 소싱 시나리오가 유리한지 AI가 시뮬레이션할 수 있다.

### 4.3 AX는 생산성 개선을 넘어 주주가치·수익성 개선의 수단이다

LG전자는 AX를 통해 end-to-end AI-driven operations를 강화하고, 2~3년 내 전체 생산성을 30% 높이는 목표를 제시했다. LG디스플레이는 AI를 개발·제조·사무 전반에 적용해 3년 내 생산성 30% 개선을 목표로 하고, AI 기반 제조 시스템이 연간 약 2,000억 원의 가치를 창출할 것으로 설명했다. LG에너지솔루션은 AX 기반 생산성 목표를 2028년까지 50%로 상향하고, AI Governance Committee를 운영하겠다고 밝혔다.

즉 Enterprise AX는 비용절감 프로젝트가 아니라, 그룹의 수익성·속도·현금흐름·운영회복력을 개선하는 밸류업 테마로 봐야 한다.


## 5. 계열사별 역할

| 계열사 | 역할 | 관련 Source |
|---|---|---|
| LG Corp. | 그룹 AX 방향 설정, 데이터 기반 경영 체질 개선, Palantir Ontology 벤치마킹, 경영진 Cockpit·AI 의사결정 체계 추진 | [[sources/src_lgcorp_silicon_valley_20260407]] |
| LG AI연구원 | EXAONE/K-EXAONE 기반 그룹 공통 AI 모델, 장문 문서 이해, 멀티모달, Advanced Agent, 산업별 모델 튜닝 | [[sources/src_exaone45_technical_report_20260409]], [[sources/src_lgai_exaone]] |
| LG CNS | ERP/SCM/MES/PLM/CRM 등 전사 시스템 통합, AX Platform, Knowledge Lake, LLMOps, AI Governance, AgenticWorks, Palantir Foundry/AIP 연계 | [[sources/src_lgcns_ax_platform]], [[sources/src_lgcns_ax_consulting]], [[sources/src_lgcns_palantir_20260312]], [[sources/src_lgcns_ax_fair_20260527]] |
| LG전자 | 개발·판매·제조·SCM·구매·마케팅에 AI 적용, LGenie의 회사 단위 AI Agent 플랫폼화, QCD·생산성·실행력 개선 | [[sources/src_lge_strategy_ax_20260108]] |
| LG에너지솔루션 | 배터리 수요 변동, 원자재 가격, 공장 가동률, 제품·소재·제조 운영 AX, AI Governance Committee | [[sources/src_lgensol_ax_productivity_20260413]] |
| LG디스플레이 | AI 설계, OLED 결함 원인 분석, 품질 개선 리드타임 단축, Hi-D assistant 기반 사무 생산성 개선 | [[sources/src_lgdisplay_ai_productivity_20250805]] |
| LG화학 | one-person-one-agent 기반 사무직 AI 활용 교육, 문서·데이터 분석·보고서·구매·일정·정책 안내·기술/특허 분석 자동화 | [[sources/src_lgchem_one_agent_20260528]] |
| LG이노텍 | 부품 수요예측, 고객사/OEM 프로젝트 관리, 품질·수율·공급망 리스크 관리 | 검증 필요. 전장·부품 공급망 기반의 연계 가능성 |
| LG U+ | 통신망 운영 데이터, 고객센터/고객경험 데이터, 네트워크 AI 운영, 고객 Agent 적용 필드 | 검증 필요. 통신 운영 데이터 기반의 연계 가능성 |
| LG생활건강 | 브랜드·유통·고객 수요예측, 원료/재고/프로모션 최적화, R&D-마케팅 연결 | 검증 필요. 소비재 사업 특성 기반의 연계 가능성 |

## 6. Related Concepts

- [[concepts/enterprise-ontology]]
- [[concepts/agentic-operating-model]]
- [[concepts/ai-cockpit]]
- [[concepts/decision-intelligence]]
- [[concepts/what-if-simulation]]
- [[concepts/data-foundation]]
- [[concepts/knowledge-graph]]
- [[concepts/agent-governance]]
- [[concepts/llmops]]
- [[concepts/ai-governance]]

## 7. Related Companies

- [[companies/lg-corp]]
- [[companies/lg-ai-research]]
- [[companies/lg-cns]]
- [[companies/lg-electronics]]
- [[companies/lg-energy-solution]]
- [[companies/lg-display]]
- [[companies/lg-chem]]
- [[companies/lg-innotek]]
- [[companies/lg-uplus]]
- [[companies/lg-household-health-care]]
- [[companies/partners/palantir]]

## 8. Sources

- [[sources/src_lgcorp_silicon_valley_20260407]]
- [[sources/src_lge_strategy_ax_20260108]]
- [[sources/src_lgcns_palantir_20260312]]
- [[sources/src_lgcns_ax_platform]]
- [[sources/src_lgcns_ax_consulting]]
- [[sources/src_lgcns_ax_fair_20260527]]
- [[sources/src_lgdisplay_ai_productivity_20250805]]
- [[sources/src_lgensol_ax_productivity_20260413]]
- [[sources/src_lgchem_one_agent_20260528]]
- [[sources/src_exaone45_technical_report_20260409]]
- [[sources/src_lgcns_anthropic_claude_enterprise_20260609]]
- [[sources/src_lgcns_kbiz_ax_20260617]]

## 9. Open Questions

- LG그룹 공통 ontology는 어떤 객체 체계로 시작해야 하는가? 예: 제품, 고객, 공장, 설비, 부품, 협력사, 주문, 재고, 원가, R&D 과제.
- 그룹 공통 ontology와 계열사별 domain ontology는 어디까지 표준화하고 어디부터 자율화해야 하는가?
- Palantir Foundry/AIP와 LG CNS AX Platform, EXAONE 기반 Agent는 어떤 역할 분담이 적절한가?
- Agent가 직접 실행할 수 있는 업무와 인간 승인이 필요한 업무의 경계는 무엇인가?
- 원가·재고·납기·품질·R&D 리드타임 등 밸류업 KPI를 어떤 방식으로 AI 성과와 연결할 것인가?
- 계열사별 데이터 접근권, 보안, 감사 로그, 내부통제 기준은 어떻게 설계해야 하는가?
- AX가 개별 업무 자동화에 머물지 않고 조직 생산성·수익성 개선으로 이어지도록 운영 모델을 어떻게 설계해야 하는가?
- LG전자, LG에너지솔루션, LG디스플레이, LG화학의 AX 사례를 그룹 공통 패턴으로 추상화할 수 있는가?

---

# Appendix A. Source Notes

## src_lgcorp_silicon_valley_20260407

- URL: https://www.lgcorp.com/media/release/30066
- Publisher: LG Corp.
- Published: 2026-04-07
- Key facts:
  - 구광모 회장이 Silicon Valley에서 Palantir CEO Alex Karp 및 Skild AI 창업진과 만났다.
  - Palantir와 Ontology, AI·data-driven decision-making framework, 제조·산업 환경의 혁신 사례를 논의했다.
  - Palantir는 제조, 금융, 물류 등에서 대규모 데이터 통합과 AI 기반 빠른 의사결정을 결합해 AX 성과를 냈다고 설명된다.

## src_lge_strategy_ax_20260108

- URL: https://www.lg.com/global/newsroom/news/corporate/lg-electronics-ceo-sets-strategic-direction-for-profit-driven-growth-prioritizing-speed-and-action/
- Publisher: LG Electronics Newsroom
- Published: 2026-01-08
- Key facts:
  - LG전자는 AX를 통해 speed, productivity, execution across the organization을 개선하겠다고 밝혔다.
  - AX는 DX가 개별 업무·프로세스를 최적화한 것에서 나아가 end-to-end 통합과 더 자율적이고 데이터 기반의 빠른 의사결정을 가능하게 하는 방향으로 설명된다.
  - 2~3년 내 전체 생산성 30% 향상 목표를 제시했다.
  - LGenie는 EXAONE 기반 회사 단위 AI agent platform으로 진화 중이라고 설명된다.

## src_lgcns_palantir_20260312

- URL: https://www.digitaltoday.co.kr/en/view/35307/lg-cns-partners-with-palantir-to-target-enterprise-ai-starting-with-lg-group-expansion
- Publisher: Digital Today
- Published: 2026-03-12
- Key facts:
  - LG CNS와 Palantir는 전략적 파트너십을 체결했다.
  - Foundry는 기업 내 분산 데이터를 통합·정제해 데이터 기반 운영체계를 구축한다.
  - AIP는 통합 데이터 환경과 생성형 AI를 결합해 실시간 의사결정을 지원한다.
  - LG CNS는 FDE 조직을 만들고 제조, 에너지, 전자, 물류 등 산업별 고부가 AX 프로젝트를 추진한다.
  - LG그룹 내 적용을 시작점으로 외부 AX 사업 확장을 계획한다.

## src_lgcns_ax_platform

- URL: https://www.lgcns.com/en/service/ai/ax-platform
- Publisher: LG CNS
- Key facts:
  - AX platform은 AI adoption을 accelerating across the business하는 integrated infrastructure로 설명된다.
  - 개발, 배포, 운영, 관리까지 full AI service lifecycle을 지원한다.
  - Knowledge Lake는 fragmented enterprise information을 structured, meaning-based knowledge로 전환한다.
  - Monitoring, LLMOps, governance, security, access control, standards를 통합한다.

## src_lgcns_ax_consulting

- URL: https://www.lgcns.com/en/service/ai/ax-consulting
- Publisher: LG CNS
- Key facts:
  - AX Consulting은 AX Master Plan, AI Process Innovation, Service Design, AI Engineering Consulting을 포함한다.
  - Agentic AI 기반의 intelligent automation, data-driven decision-making, process-wide AI integration을 강조한다.
  - ERP, MES, CRM 등 legacy systems에 분산된 데이터를 통합하고 workflow 가시성을 높이는 것이 핵심 조건으로 설명된다.
  - QCD framework를 활용해 AI 성과를 측정할 수 있다고 설명한다.

## src_lgcns_ax_fair_20260527

- URL: https://www.etnews.com/20260527000356
- Publisher: 전자신문
- Published: 2026-05-27
- Key facts:
  - LG CNS AX Fair 2026은 “Now in Action”을 주제로 진행됐다.
  - AgenticWorks와 PhysicalWorks가 AX 실행 플랫폼 전략으로 제시됐다.
  - AgenticWorks는 데이터 지식화, 모델 학습, 에이전트 개발, 운영 통제, 비용 최적화 전 과정을 지원한다고 설명된다.

## src_lgdisplay_ai_productivity_20250805

- URL: https://www.koreatimes.co.kr/business/tech-science/20250805/lg-display-eyes-30-improvement-in-productivity-through-ai
- Publisher: The Korea Times
- Published: 2025-08-05
- Key facts:
  - LG디스플레이는 AI를 전체 업무 프로세스에 적용해 3년 내 생산성을 30% 개선하겠다고 밝혔다.
  - AI 설계 시스템은 flexible panel edge 설계 시간을 4주에서 8시간으로 줄였다.
  - OLED 생산 결함 원인 분석·해결 제안을 통해 품질 개선 시간을 3주에서 2일로 줄였다.
  - Hi-D assistant는 지식검색, 실시간 통역, 회의록 생성 등을 지원한다.

## src_lgensol_ax_productivity_20260413

- URL: https://www.mk.co.kr/en/business/12015637
- Publisher: Maeil Business News
- Published: 2026-04-13
- Key facts:
  - LG에너지솔루션 CEO는 AX 기반 생산성 목표를 2028년까지 50%로 상향했다.
  - 특허, 30년 운영 이력, 인재를 AX와 결합하면 경쟁 구도를 바꿀 기회가 될 수 있다고 설명했다.
  - CEO 주재 월간 AI Governance Committee를 운영해 AI solution adoption, security, change management 이슈를 점검할 계획이다.

## src_lgchem_one_agent_20260528

- URL: https://en.sedaily.com/news/2026/05/28/lg-chem-completes-ai-training-for-half-of-office-workforce
- Publisher: Seoul Economic Daily
- Published: 2026-05-28
- Key facts:
  - LG화학은 사무직 절반 이상인 3,000명 이상이 AI 활용 교육을 완료했다고 보도됐다.
  - one-agent-per-employee 모델을 중심으로 직원이 업무에 맞춘 AI를 설계·활용한다.
  - 문서 작성, 데이터 분석, 보고서 생성, 구매, 일정, 사내 정책 안내, 기술·특허 정보 분석에 적용된다.

## src_lgcns_anthropic_claude_enterprise_20260609

- URL: https://www.thelec.kr/news/articleView.html?idxno=57787
- Publisher: 디일렉(THE ELEC)
- Published: 2026-06-09
- Key facts:
  - LG CNS가 앤트로픽의 Claude Enterprise를 도입 계약 체결하고 LG그룹 전 계열사에 적용 예정.
  - LG CNS는 사내 전 직원에게 Claude 접속을 개방하고 개발·문서 작성·분석·협업 분야의 생성형 AI 기반 업무 혁신을 추진.
  - LG테크놀로지벤처스는 2023년 앤트로픽에 지분 투자를 통해 협력 관계를 유지해왔음.

## src_lgcns_kbiz_ax_20260617

- URL: https://www.etnews.com/20260617000336
- Publisher: 전자신문
- Published: 2026-06-17
- Key facts:
  - 중소기업중앙회(KBIZ)와 LG CNS가 2026년 6월 17일 '중소기업 AI 확산을 위한 대·중소 상생협력 모델 발굴' 업무협약 체결.
  - 사업 규모 최대 30억 원, 정부 50%·대기업 10% 지원, 기업 자부담 40%.
  - 선정 기업은 최대 12개월 AX 구축 지원, AGV·AMR·로봇·클라우드 등 포괄 지원.
  - LG CNS 연간 약 20억 원 규모 지원으로 교육·기술·유통·마케팅 분야 중소기업 AI 역량 강화.
