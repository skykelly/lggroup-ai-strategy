---
id: doc_ai_mobility_sdv_aidv
type: doc
title: AI Mobility / SDV·AIDV
theme_id: ai_mobility_sdv_aidv
status: draft
updated: 2026-06-21
related_concepts:
  - sdv
  - aidv
  - ai-cabin
  - in-vehicle-ai
  - adas
  - autonomous-driving
  - v2x
  - bms-bmts
  - battery-software
  - automotive-display
  - in-cabin-sensing
  - on-device-ai
related_companies:
  - lg-electronics
  - lg-innotek
  - lg-display
  - lg-energy-solution
  - lg-uplus
  - lg-ai-research
  - lg-cns
  - nvidia
  - qualcomm
  - sdverse
source_ids:
  - src_lge_ai_in_vehicle_20251217
  - src_lginnotek_ces2026_aidv_20260106
  - src_lginnotek_ces2026_showcase
  - src_lgdisplay_ces2026_20260105
  - src_lgensol_sdverse_20260403
  - src_lgensol_baround
  - src_lgensol_qualcomm_bms_20241223
  - src_lguplus_autonomous_driving
  - src_lg_nvidia_map_20260608
tags:
  - ai-mobility
  - sdv
  - aidv
  - autonomous-driving
  - in-vehicle-ai
  - bms
  - automotive-display
  - v2x
---

# AI Mobility / SDV·AIDV

## 1. Executive Summary

AI Mobility / SDV·AIDV는 차량을 하드웨어 중심 이동수단에서 AI 기반 소프트웨어·센서·디스플레이·배터리 데이터 플랫폼으로 전환하는 테마다. [[concepts/sdv]]가 차량 기능을 소프트웨어 업데이트와 플랫폼 아키텍처 중심으로 재정의한다면, [[concepts/aidv]]는 여기에 AI 판단, 인캐빈 센싱, 온디바이스 AI, 자율주행 보조, 개인화 경험을 결합한다.

LG그룹은 완성차를 만들지는 않지만, SDV·AIDV 밸류체인의 핵심 구성요소를 다수 보유한다. [[companies/lg-electronics]] VS는 AI Cockpit, IVI, 인캐빈 AI 경험을, [[companies/lg-innotek]]은 카메라·LiDAR·Radar·통신·조명·전동화 부품을, [[companies/lg-display]]는 차량용 OLED·P2P·Slidable 디스플레이를, [[companies/lg-energy-solution]]은 BMS/BMTS와 배터리 SW를, [[companies/lg-uplus]]는 V2X·5G·정밀측위·자율주행 관제 인프라를 담당한다.

이 테마의 전략적 본질은 부품 단품 공급이 아니라 `AI Cabin + Sensing + Display + Battery Software + Connectivity`를 결합한 모빌리티 AI 경험과 소프트웨어 수익모델을 확보하는 것이다.

<figure>
  <img src="https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-2.png" alt="Mobility Display Solution. 투명 OLED 윈드실드와 AI 인터페이스를 결합한 차량 내 디스플레이 경험." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Mobility Display Solution. 투명 OLED 윈드실드와 AI 인터페이스를 결합한 차량 내 디스플레이 경험. 출처: <a href="https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/">LG Electronics Newsroom</a></small></figcaption>
</figure>

## 2. AI Market Landscape & Why Now

### 2.1 차량은 소프트웨어 정의 플랫폼으로 이동

자동차 산업의 경쟁축은 엔진·기계 성능에서 전장 아키텍처, 소프트웨어 업데이트, 데이터, AI 경험으로 이동하고 있다. SDV는 차량 기능을 물리 부품이 아니라 소프트웨어·클라우드·OTA·컴퓨팅 아키텍처를 통해 지속적으로 개선하는 방향이다. AIDV는 여기에서 한 단계 더 나아가 차량이 운전자·탑승자·주변 환경을 이해하고, 안전·콘텐츠·커머스·정비·에너지 관리를 AI로 수행하는 흐름이다.

LG전자는 CES 2026에서 AI-powered in-vehicle solutions를 공개하며, 디스플레이, 인캐빈 센싱, 온디바이스 AI를 결합한 AI-Defined Vehicle 아키텍처를 제시했다. 해당 솔루션은 Mobility Display Solution, Automotive Vision Solution, In-Vehicle Entertainment Solution으로 구성된다.

### 2.2 차량 내부는 새로운 AI 경험 공간이 된다

차량 실내는 향후 집, 사무실, 매장에 이은 또 하나의 AI 실행 공간이 된다. 주행 중에는 안전과 정보 제공이 중요하고, 자율주행 모드나 정차 중에는 콘텐츠, 커뮤니케이션, 쇼핑, 생산성 경험이 중요해진다.

LG전자의 Automotive Vision Solution은 운전자 움직임, 시선, 주의, 의복 색상, 제스처를 실시간 추적하고, Mobility Display Solution은 투명 OLED 윈드실드를 지능형 인터페이스로 활용한다. 이는 차량 실내가 단순 디스플레이 탑재 공간이 아니라 AI가 탑승자 상태와 외부 맥락을 이해해 반응하는 경험 플랫폼으로 바뀌고 있음을 보여준다.

### 2.3 센싱·디스플레이·배터리 SW·연결성이 통합된다

SDV·AIDV는 단일 기술로 구현되지 않는다. 차량 외부를 인지하는 센서, 차량 내부의 UX/HMI, 배터리 상태를 해석하는 BMS/BMTS, 차량과 인프라를 연결하는 V2X/5G, 그리고 이를 통합하는 소프트웨어 아키텍처가 함께 필요하다.

LG이노텍은 CES 2026에서 AIDV 시대를 겨냥해 카메라, LiDAR, Radar, UWB, 5G-NTN, AP Module, 조명, 800V Wireless BMS 등 하드웨어와 소프트웨어를 결합한 모빌리티 솔루션을 제시했다. LG디스플레이는 SDV에 최적화된 51인치 P2P OLED와 Slidable OLED 등 차량용 디스플레이를 제안했다. LG에너지솔루션은 SDVerse 참여와 B.around/BMTS를 통해 배터리를 제조 이후의 소프트웨어·서비스 영역으로 확장하고 있다.

## 3. Business Opportunities

| 기회 | 설명 | 관련 계열사 | 보유 자산 |
|---|---|---|---|
| AI Cabin Platform | 운전자·탑승자 상태 인식, 투명 OLED, 콘텐츠 추천, 실시간 번역, 제스처/시선 기반 인터랙션 | LG전자, LG디스플레이, LG AI연구원 | VS, OLED, 인캐빈 센싱, 온디바이스 AI, 멀티모달 AI |
| SDV/AIDV Sensing Package | 카메라, LiDAR, Radar, UWB Radar, 5G-NTN, AP Module, 조명 통합 패키지 | LG이노텍, LG전자 | 차량용 카메라, 센싱, 통신모듈, 조명, 전장 부품 |
| Automotive Display / HMI | P2P, Slidable OLED, 투명·스트레처블 디스플레이 기반 차량용 UX 플랫폼 | LG디스플레이, LG전자 | OLED, LTPS LCD, Oxide LCD, P-OLED, HMI 설계 |
| Battery Software / BMTS | 배터리 안전진단, 열화·수명 예측, SDV BMS, 클라우드·AI 기반 배터리 관리 | LG에너지솔루션, Qualcomm, SDVerse | 20년 이상 BMS 경험, BMS 특허, B.around, SDVerse 유통 채널 |
| V2X / Autonomous Driving Infrastructure | 정밀지도, 정밀측위, 5G-V2X, MEC, 자율주행 관제 플랫폼 | LG U+ | 5G, Dynamic 정밀지도, 자율주행 관제, C-ITS |
| Vehicle Data Service | 차량·배터리·운행·정비 데이터를 기반으로 보험, 리스, 중고차, 플릿 관리 서비스 확장 | LG에너지솔루션, LG U+, LG전자 | 배터리 lifecycle data, 차량 커넥티비티, 고객·운행 데이터 |
| OEM Package / One LG Mobility Solution | AI Cabin, Display, Sensing, Battery SW, Connectivity를 묶은 OEM 대상 통합 제안 | LG전자 VS, LG이노텍, LG디스플레이, LG에너지솔루션, LG U+ | 그룹 계열사별 모빌리티 부품·SW·인프라 자산 |


### 3.1 LG Electronics AI-powered In-Vehicle Solutions

* 내용 요약
  - LG전자 VS는 차량 내부를 AI 경험 공간으로 전환하는 `AI Cabin`의 중심 축이다.
  - 디스플레이, 인캐빈 센싱, 온디바이스 AI를 결합해 안전·개인화·콘텐츠 경험을 동시에 제공한다.
  - 단품 IVI 공급을 넘어 AI Cockpit, 실시간 번역, 제스처/시선 인식, 차량 내 엔터테인먼트 플랫폼으로 확장 가능하다.
  - Theme 3 관점에서는 `AI Cabin Platform`과 `OEM Package / One LG Mobility Solution`의 핵심 사업 후보로 볼 수 있다.

<figure>
  <img src="https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image-3.png" alt="Automotive Vision Solution. 운전자·탑승자 상태와 주변 맥락을 인식해 안전과 개인화 경험을 제공하는 콘셉트." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>Automotive Vision Solution. 운전자·탑승자 상태와 주변 맥락을 인식해 안전과 개인화 경험을 제공하는 콘셉트. 출처: <a href="https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/">LG Electronics Newsroom</a></small></figcaption>
</figure>

<figure>
  <img src="https://www.lg.com/content/dam/channel/wcms/global/newsroom/news/vehicle-component-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/LG-AI-Powered-In-Vehicle-Solutions_image_4.png" alt="In-Vehicle Entertainment Solution. 차량 창문·디스플레이를 AI 기반 인터랙티브 미디어 공간으로 확장하는 경험." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>In-Vehicle Entertainment Solution. 차량 창문·디스플레이를 AI 기반 인터랙티브 미디어 공간으로 확장하는 경험. 출처: <a href="https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/">LG Electronics Newsroom</a></small></figcaption>
</figure>

### 3.2 LG Innotek CES 2026 AIDV / Mobility Solutions

* 내용 요약
  - LG이노텍은 AIDV 구현에 필요한 외부 인지·통신·조명·전동화 부품을 통합 제공할 수 있는 핵심 계열사다.
  - 카메라, LiDAR, Radar, UWB, 5G-NTN, AP Module 등은 자율주행·ADAS·인캐빈/아웃캐빈 센싱의 기반이 된다.
  - 하드웨어 부품 공급에 머물지 않고 센싱 패키지, 융복합 모듈, OEM 맞춤형 AIDV 솔루션으로 확장 가능하다.
  - Theme 3 관점에서는 `SDV/AIDV Sensing Package`와 `One LG Mobility Solution`의 외부 인지 레이어를 담당한다.

<figure>
  <img src="assets/images/lginnotek_ces2026_sketch_05.avif" alt="LG이노텍 CES 2026 모빌리티 전시 현장 이미지 후보. AVIF 형식이며 렌더링/다운로드 환경 확인 필요." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG이노텍 CES 2026 모빌리티 전시 현장 이미지 후보. AVIF 형식이며 렌더링/다운로드 환경 확인 필요. 출처: <a href="https://www.lginnotek.com/showcase/ces2026.do">LG Innotek CES 2026 Showcase</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lginnotek_ces2026_sketch_06.avif" alt="LG이노텍 CES 2026 자율주행·전동화 솔루션 전시 현장 이미지 후보. AVIF 형식이며 렌더링/다운로드 환경 확인 필요." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG이노텍 CES 2026 자율주행·전동화 솔루션 전시 현장 이미지 후보. AVIF 형식이며 렌더링/다운로드 환경 확인 필요. 출처: <a href="https://www.lginnotek.com/showcase/ces2026.do">LG Innotek CES 2026 Showcase</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lginnotek_ces2026_sketch_small_02.avif" alt="LG이노텍 CES 2026 전시 하이라이트 썸네일 이미지 후보." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG이노텍 CES 2026 전시 하이라이트 썸네일 이미지 후보. 출처: <a href="https://www.lginnotek.com/showcase/ces2026.do">LG Innotek CES 2026 Showcase</a></small></figcaption>
</figure>

> LG이노텍 CES 2026 특집 사이트의 주요 전시 이미지는 AVIF 형식이다. 일부 환경에서는 Markdown 미리보기에서 렌더링되지 않을 수 있으므로 다운로드 후 변환 여부를 별도 검토한다. 단, 이 작업에서는 별도 이미지 생성·변환은 하지 않는다.

### 3.3 LG Display Automotive Display / SDV HMI

* 내용 요약
  - LG디스플레이는 SDV 시대 차량 내부 UX를 구현하는 화면 인프라를 제공한다.
  - P2P OLED, Slidable OLED, 투명·스트레처블 디스플레이는 차량을 이동수단에서 콘텐츠·업무·AI 인터페이스 공간으로 바꾸는 핵심 요소다.
  - 디스플레이는 단순 부품이 아니라 AI Cockpit, 개인화 HMI, 인비히클 엔터테인먼트와 결합되는 경험 플랫폼으로 확장된다.
  - Theme 3 관점에서는 `Automotive Display / HMI`와 `AI Cabin Platform`의 시각 인터페이스 레이어를 담당한다.

<figure>
  <img src="assets/images/lgdisplay_ces2026_main.png" alt="LG디스플레이 CES 2026 전시 대표 이미지. AI 시대 디스플레이 전략과 차량용 디스플레이 전시를 함께 소개." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG디스플레이 CES 2026 전시 대표 이미지. AI 시대 디스플레이 전략과 차량용 디스플레이 전시를 함께 소개. 출처: <a href="https://www.lgdisplay.com/kor/company/media-center/latest-news?contentId=5495">LG Display Newsroom</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgdisplay_ces2026_automotive_display.jpg" alt="LG디스플레이 CES 2026 차량용 디스플레이 이미지. P2P, Slidable OLED 등 SDV용 HMI 방향과 연결." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>LG디스플레이 CES 2026 차량용 디스플레이 이미지. P2P, Slidable OLED 등 SDV용 HMI 방향과 연결. 출처: <a href="https://www.lgdisplay.com/kor/company/media-center/latest-news?contentId=5495">LG Display Newsroom</a></small></figcaption>
</figure>

> LG디스플레이 CDN 이미지는 직접 이미지 URL을 확보했지만, 일부 fetch 환경에서 400 응답이 발생할 수 있다. 다운로드 실패 시 원문 페이지에서 재확인한다.

### 3.4 LG Energy Solution B.around / BMTS / SDV BMS

* 내용 요약
  - LG에너지솔루션은 배터리를 제조 이후의 소프트웨어·데이터 서비스 영역으로 확장하고 있다.
  - B.around/BMTS는 배터리 안전진단, 열화·수명 예측, 잔존가치 평가, 클라우드·AI 기반 관리 서비스를 제공하는 기반이다.
  - SDV BMS와 SDVerse 참여는 배터리 SW가 자동차 소프트웨어 생태계에서 별도 상품으로 유통될 수 있음을 보여준다.
  - Theme 3 관점에서는 `Battery Software / BMTS`와 `Vehicle Data Service`의 에너지·안전 데이터 레이어를 담당한다.

<figure>
  <img src="assets/images/lgensol_baround_core_values.png" alt="B.around Core Values. 진단 전문성, 신뢰 기반 관리, 혁신 서비스, 직관적 경험을 강조." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>B.around Core Values. 진단 전문성, 신뢰 기반 관리, 혁신 서비스, 직관적 경험을 강조. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgensol_bms_lifecycle.png" alt="BMS는 배터리 수명주기, 성능, 안전 관리를 담당하는 핵심 제어 시스템으로 설명된다." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>BMS는 배터리 수명주기, 성능, 안전 관리를 담당하는 핵심 제어 시스템으로 설명된다. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lgensol_bms_features_to_hpc.png" alt="BMS 기능이 HPC 환경으로 확장되는 개념 이미지." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>BMS 기능이 HPC 환경으로 확장되는 개념 이미지. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

### 3.5 LG U+ V2X / Autonomous Driving Infrastructure

* 내용 요약
  - LG U+는 차량과 도로 인프라를 연결하는 V2X·5G·정밀지도·자율주행 관제 레이어를 담당할 수 있다.
  - Dynamic 정밀지도, MEC, V2X Gateway, 정밀측위, 관제 서버는 자율주행·스마트시티·물류 모빌리티의 기반 인프라다.
  - 단기적으로는 민간 승용차보다 공공 셔틀, 물류, C-ITS, 특정 구역 자율주행에서 사업화 가능성이 높다.
  - Theme 3 관점에서는 `V2X / Autonomous Driving Infrastructure`와 `Vehicle Data Service`의 연결성 인프라 축을 담당한다.

<figure>
  <img src="assets/images/lguplus_dynamic_map_features.png" alt="U+ Dynamic 정밀지도 플랫폼. 정밀지도 융합, 정밀 전자지도 적용, 국제 표준 준수를 설명." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>U+ Dynamic 정밀지도 플랫폼. 정밀지도 융합, 정밀 전자지도 적용, 국제 표준 준수를 설명. 출처: <a href="https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127">LG U+ Autonomous Driving</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lguplus_control_center.png" alt="자율주행 운영 관제센터 이미지. 실시간 위치·운행상태 모니터링과 운영관리 역할을 설명." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>자율주행 운영 관제센터 이미지. 실시간 위치·운행상태 모니터링과 운영관리 역할을 설명. 출처: <a href="https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127">LG U+ Autonomous Driving</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lguplus_dynamic_map_architecture.png" alt="U+ Dynamic 정밀지도 플랫폼 구성도. 객체인식센서, Static 정밀지도, 인프라 정보, V2X 정보를 연결." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>U+ Dynamic 정밀지도 플랫폼 구성도. 객체인식센서, Static 정밀지도, 인프라 정보, V2X 정보를 연결. 출처: <a href="https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127">LG U+ Autonomous Driving</a></small></figcaption>
</figure>

<figure>
  <img src="assets/images/lguplus_autonomous_control_architecture.png" alt="U+ 자율주행 관제 구성도. 5G, MEC V2X Gateway, 관제 서버, Dynamic Map 서버, 정밀측위 서버를 연결." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>U+ 자율주행 관제 구성도. 5G, MEC V2X Gateway, 관제 서버, Dynamic Map 서버, 정밀측위 서버를 연결. 출처: <a href="https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127">LG U+ Autonomous Driving</a></small></figcaption>
</figure>

---

## 4. LG Group Strategic Meaning

### 4.1 완성차가 아니라 AIDV 핵심 레이어를 장악한다

LG그룹은 완성차 제조사가 아니지만, AIDV 구현에 필요한 핵심 레이어를 폭넓게 보유한다. 외부 인지 레이어는 [[companies/lg-innotek]], 내부 경험 레이어는 [[companies/lg-electronics]]와 [[companies/lg-display]], 에너지·안전 레이어는 [[companies/lg-energy-solution]], 연결성·인프라 레이어는 [[companies/lg-uplus]], AI 모델·Agent 레이어는 [[companies/lg-ai-research]]가 담당할 수 있다.

따라서 LG의 전략적 위치는 자동차 완제품 생산이 아니라, 완성차 OEM이 AIDV 전환을 추진할 때 필요한 부품·디스플레이·SW·배터리 데이터·통신 인프라를 묶어 제공하는 `Mobility AI Enabler`에 가깝다.

### 4.2 단품 부품에서 소프트웨어·서비스로 확장한다

기존 전장 사업은 카메라, 디스플레이, 배터리, 통신모듈 같은 하드웨어 공급이 중심이었다. 그러나 SDV 시대에는 하드웨어가 소프트웨어 업데이트, 데이터 분석, cloud/HPC, marketplace와 연결될 때 지속 수익 모델이 가능해진다.

LG에너지솔루션의 SDVerse 참여는 배터리 SW가 차량 SW marketplace를 통해 유통될 수 있음을 보여준다. B.around/BMTS는 배터리 상태 진단, 수명 예측, 안전 관리, 잔존가치 평가를 서비스화할 수 있는 기반이다.

<figure>
  <img src="assets/images/lgensol_sdv_bms.png" alt="SDV BMS. BMS 기능을 고성능 컴퓨팅과 AI 기반 진단·제어로 확장하는 개념." style="max-width:100%; border-radius:8px;" />
  <figcaption><small>SDV BMS. BMS 기능을 고성능 컴퓨팅과 AI 기반 진단·제어로 확장하는 개념. 출처: <a href="https://www.lgensol.com/mobile/en/business/baround">LG Energy Solution B.around</a></small></figcaption>
</figure>

### 4.3 차량 내부는 AI Commerce와 고객 경험의 다음 공간이 될 수 있다

LG전자의 인비히클 AI 솔루션은 시선·제스처·외부 풍경·장소 기억·실시간 번역·콘텐츠 추천을 통해 차량 내부를 AI 경험 공간으로 전환한다. 장기적으로 이는 차량 내 콘텐츠, 커머스, 구독, 정비, 보험, 충전, 에너지 관리와 연결될 수 있다.

즉, AI Mobility는 전장부품 사업을 넘어 고객 경험과 데이터 기반 서비스 사업으로 확장될 수 있다.

## 5. 계열사별 역할

| 계열사 | 역할 | 관련 Source |
|---|---|---|
| LG전자 VS | AI Cockpit, IVI, Mobility Display Solution, Automotive Vision Solution, In-Vehicle Entertainment, 온디바이스 AI 기반 차량 내 경험 | [[sources/src_lge_ai_in_vehicle_20251217]] |
| LG이노텍 | 차량용 카메라, LiDAR, Radar, UWB, 5G-NTN, AP Module, 조명, 800V Wireless BMS 등 AIDV 핵심 부품과 통합 솔루션 | [[sources/src_lginnotek_ces2026_aidv_20260106]], [[sources/src_lginnotek_ces2026_showcase]] |
| LG디스플레이 | 51인치 P2P OLED, Slidable OLED, 투명·스트레처블 디스플레이 등 SDV용 HMI·UX 화면 인프라 | [[sources/src_lgdisplay_ces2026_20260105]] |
| LG에너지솔루션 | BMS/BMTS, B.around, SDVerse 기반 배터리 SW 유통, 안전진단·열화·수명 예측, SDV BMS | [[sources/src_lgensol_sdverse_20260403]], [[sources/src_lgensol_baround]], [[sources/src_lgensol_qualcomm_bms_20241223]] |
| LG U+ | 5G-V2X, Dynamic 정밀지도, 정밀측위, MEC 기반 자율주행 관제, C-ITS | [[sources/src_lguplus_autonomous_driving]] |
| LG AI연구원 | 차량 내 멀티모달 Agent, 시각·음성·문서 기반 운전자/탑승자 경험, 배터리·정비 데이터 해석 모델 | 검증 필요. EXAONE/Advanced Agent 역량 기반의 연계 가능성 |
| LG CNS | 차량 데이터 플랫폼, 클라우드·보안·OTA 운영, SDV SW 개발·운영 체계 | 검증 필요. 그룹 IT/SW 통합 역량 기반의 연계 가능성 |
| LG Corp. | 모빌리티 포트폴리오 조정, NVIDIA·SDVerse·Qualcomm 등 외부 파트너십 연결 | [[sources/src_lg_nvidia_map_20260608]] |

## 6. Related Concepts

- [[concepts/sdv]]
- [[concepts/aidv]]
- [[concepts/ai-cabin]]
- [[concepts/in-vehicle-ai]]
- [[concepts/in-cabin-sensing]]
- [[concepts/automotive-display]]
- [[concepts/adas]]
- [[concepts/autonomous-driving]]
- [[concepts/v2x]]
- [[concepts/bms-bmts]]
- [[concepts/battery-software]]
- [[concepts/on-device-ai]]

## 7. Related Companies

- [[companies/lg-electronics]]
- [[companies/lg-innotek]]
- [[companies/lg-display]]
- [[companies/lg-energy-solution]]
- [[companies/lg-uplus]]
- [[companies/lg-ai-research]]
- [[companies/lg-cns]]
- [[companies/partners/nvidia]]
- [[companies/partners/qualcomm]]
- [[companies/partners/sdverse]]

## 8. Sources

- [[sources/src_lge_ai_in_vehicle_20251217]]
- [[sources/src_lginnotek_ces2026_aidv_20260106]]
- [[sources/src_lginnotek_ces2026_showcase]]
- [[sources/src_lgdisplay_ces2026_20260105]]
- [[sources/src_lgensol_sdverse_20260403]]
- [[sources/src_lgensol_baround]]
- [[sources/src_lgensol_qualcomm_bms_20241223]]
- [[sources/src_lguplus_autonomous_driving]]
- [[sources/src_lg_nvidia_map_20260608]]

## 9. Open Questions

- SDV와 AIDV를 구분하는 기준은 무엇인가? AIDV는 단순 AI 기능 탑재인지, 차량 아키텍처 전환인지 명확히 정의해야 한다.
- LG전자 VS, LG이노텍, LG디스플레이, LG에너지솔루션의 OEM 대상 통합 제안 구조는 가능한가?
- 차량 내 AI 경험에서 개인정보·생체정보·시선 데이터 처리는 어떤 규제와 보안 요구를 받는가?
- 배터리 SW와 BMS 데이터는 OEM, 배터리 기업, 차량 SW marketplace 간에 어떻게 수익 배분되는가?
- V2X/정밀지도/관제 인프라는 민간 승용차보다 공공·셔틀·물류·스마트시티 영역에서 먼저 확산되는가?
- 차량용 AI Agent는 온디바이스, 클라우드, 하이브리드 중 어떤 구조가 적합한가?
- 완성차 OEM이 자체 OS·AI 플랫폼을 강화할수록 LG의 역할은 Tier 1, Tier 2, SW Provider 중 어디로 이동하는가?
- SDV/AIDV 경쟁사 대비 LG그룹의 차별점은 `디스플레이+센싱+배터리SW+연결성` 패키지화가 될 수 있는가?

---

# Appendix A. Source Notes

## src_lge_ai_in_vehicle_20251217

- URL: https://www.lg.com/global/newsroom/news/vehicle-solutions/lg-showcases-future-of-mobility-with-ai-powered-in-vehicle-solutions-at-ces-2026/
- Publisher: LG Electronics Newsroom
- Published: 2025-12-17
- Key facts:
  - CES 2026 Best of Innovation Award in In-Vehicle Entertainment 수상.
  - 디스플레이, 인캐빈 센싱, 온디바이스 AI를 결합한 AI-Defined Vehicle 아키텍처.
  - Mobility Display Solution, Automotive Vision Solution, In-Vehicle Entertainment Solution으로 구성.
  - 투명 OLED 윈드실드, Vision AI, 시선·제스처 인식, 개인화 콘텐츠 추천, 실시간 번역 등 제시.

## src_lginnotek_ces2026_aidv_20260106

- URL: https://www.lg.co.kr/media/release/29755
- Publisher: LG Corp. / LG Innotek
- Published: 2026-01-06
- Key facts:
  - CES 2026에서 AIDV 시대를 겨냥한 모빌리티 혁신 솔루션 공개.
  - 자율주행 컨셉카 목업에 AD/ADAS 제품 16종 탑재.
  - 카메라 모듈, LiDAR, Radar를 결합한 자율주행 융·복합 센싱 솔루션 강조.
  - 언더 디스플레이 카메라, UWB Radar, 초슬림 픽셀 라이팅, 5G-NTN 모듈, AP Module, UWB Digital Key 등 공개.
  - EV 목업에는 800V Wireless BMS, B-Link 등 전동화 솔루션 15종 탑재.

## src_lgdisplay_ces2026_20260105

- URL: https://www.lgdisplay.com/kor/company/media-center/latest-news?contentId=5495
- Publisher: LG Display
- Published: 2026-01-05
- Key facts:
  - CES 2026 주제는 “Display for AI, Technology for All”.
  - SDV에 최적화된 프리미엄 차량용 디스플레이 솔루션을 전시.
  - 차량용 P2P는 운전석부터 조수석까지 이어지는 초대형 화면으로 개인화 인포테인먼트 제공 가능.
  - 51인치 초대형 OLED P2P, 33인치 Slidable OLED, 투명·스트레처블 디스플레이 등을 제시.

## src_lgensol_sdverse_20260403

- URL: https://inside.lgensol.com/en/2026/04/lg-energy-solution-becomes-first-battery-company-to-join-sdverseglobal-b2b-marketplace-for-automotive-software/
- Publisher: LG Energy Solution Battery Inside
- Published: 2026-04-03
- Key facts:
  - LG에너지솔루션은 배터리 기업 최초로 SDVerse에 참여.
  - SDVerse는 GM, Magna, Wipro가 공동 설립한 automotive software B2B marketplace.
  - LG에너지솔루션은 Battery Platform SW, Safety Diagnostic Calibration Tool, Onboard FRISM, Onboard BLiS, Onboard DASH 등 5개 배터리 SW를 제공.
  - SDV 환경에서 배터리 소프트웨어와 서비스로 확장하는 전략.

## src_lgensol_qualcomm_bms_20241223

- URL: https://inside.lgensol.com/en/2024/12/lg-energy-solution-announces-availability-of-advanced-battery-management-system-solutions-for-automotive/
- Publisher: LG Energy Solution Battery Inside
- Published: 2024-12-23
- Key facts:
  - Qualcomm Snapdragon Digital Chassis 기반 SoC-based BMS 진단 솔루션.
  - 기존 BMS 대비 80배 증가한 연산 성능으로 안전진단, 열화진단, 이상감지 고도화.
  - 차량 데이터 분석을 별도 서버 없이 차량 내에서 실시간 수행 가능.
  - B.around는 cloud, AI, SDV platform-optimized services를 통합한 BMTS 브랜드로 설명됨.

## src_lgensol_baround

- URL: https://www.lgensol.com/mobile/en/business/baround
- Publisher: LG Energy Solution
- Key facts:
  - B.around는 BMTS 기반 통합 서비스 플랫폼.
  - 제조, 사용, 회수, 재사용까지 배터리 lifecycle 데이터를 수집·분석.
  - AI & Cloud-based Diagnostics and Forecasting을 통해 안전, 성능 저하, 수명을 예측.
  - SDV BMS는 BMS 기능을 HPC와 AI 기반 진단·제어로 확장한다.

## src_lguplus_autonomous_driving

- URL: https://www.lguplus.com/biz/all/5g/smart-mobility/autonomous-driving/B000000127
- Publisher: LG U+
- Key facts:
  - 5G와 V2X 기반의 자율주행 모빌리티 서비스.
  - U+ Dynamic 정밀지도 플랫폼은 센서 사각지대 보행자·차량 정보, 교통 정체, 사고, 기상 정보, 신호현시 정보를 제공.
  - 자율주행 관제는 실시간 위치·운행상태 모니터링, V2X, MEC, 정밀측위, Dynamic Map 서버를 연결한다.
