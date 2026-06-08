# Concept 후보 목록

총 **38개**의 Concept를 6개 유형으로 정규화했다. `canonical`은 현재 자료만으로 독립 Concept로 유지할 수 있고, `candidate`는 추가 문서·검색량·관계 검증이 필요하며, `supporting`은 상위 Concept의 속성으로 우선 관리한다.

## 1. Style Concept

| ID | 한국어명 | 영문명 | 상태 | Parent |
|---|---|---|---|---|
| [warm-minimalism](./warm-minimalism.md) | 웜 미니멀리즘 | Warm Minimalism | canonical | minimalism |
| [modern-natural](./modern-natural.md) | 모던 내추럴 | Modern Natural | canonical | contemporary-interior |
| [white-wood](./white-wood.md) | 화이트 우드 | White & Wood | canonical | modern-natural |
| [japandi](./japandi.md) | 재팬디 | Japandi | canonical | hybrid-style |
| [mid-century-modern](./mid-century-modern.md) | 미드센추리 모던 | Mid-century Modern | canonical | modernism |
| [nordic-style](./nordic-style.md) | 북유럽 스타일 | Nordic Style | canonical | scandinavian-design |
| [hotel-like-interior](./hotel-like-interior.md) | 호텔식 인테리어 | Hotel-like Interior | canonical | hospitality-inspired-interior |
| [natural-luxury](./natural-luxury.md) | 내추럴 럭셔리 | Natural Luxury | canonical | quiet-luxury |
| [plant-interior](./plant-interior.md) | 플랜테리어 | Plant Interior | canonical | biophilic-design |
| [storage-centered-interior](./storage-centered-interior.md) | 수납 중심 인테리어 | Storage-centered Interior | canonical | functional-interior |

## 2. Lifestyle Concept

| ID | 한국어명 | 영문명 | 상태 | Parent |
|---|---|---|---|---|
| [wellness-home](./wellness-home.md) | 웰니스 홈 | Wellness Home | canonical | home-wellbeing |
| [hotel-like-bedroom](./hotel-like-bedroom.md) | 호텔식 침실 | Hotel-like Bedroom | canonical | bedroom-experience |
| [storage-as-lifestyle](./storage-as-lifestyle.md) | 수납의 라이프스타일화 | Storage as Lifestyle | canonical | organized-living |
| [small-space-optimization](./small-space-optimization.md) | 작은 공간 최적화 | Small-space Optimization | canonical | compact-living |
| [ai-smart-living](./ai-smart-living.md) | AI 스마트 리빙 | AI & Smart Living | canonical | smart-home |

## 3. Spatial Concept

| ID | 한국어명 | 영문명 | 상태 | Parent |
|---|---|---|---|---|
| [living-room-lounge](./living-room-lounge.md) | 라운지형 거실 | Living-room Lounge | candidate | living-room |
| [sleep-wellness](./sleep-wellness.md) | 수면 웰니스 | Sleep Wellness | candidate | bedroom |
| [open-kitchen](./open-kitchen.md) | 대면형 주방 | Open-facing Kitchen | candidate | kitchen |
| [kitchen-island](./kitchen-island.md) | 아일랜드 주방 | Kitchen Island | candidate | kitchen |
| [home-office-zone](./home-office-zone.md) | 홈오피스 존 | Home Office Zone | candidate | home-office |
| [balcony-garden](./balcony-garden.md) | 베란다 가든 | Balcony Garden | candidate | balcony |
| [studio-officetel-living](./studio-officetel-living.md) | 원룸·오피스텔 리빙 | Studio & Officetel Living | candidate | compact-living |

## 4. Functional Concept

| ID | 한국어명 | 영문명 | 상태 | Parent |
|---|---|---|---|---|
| [hidden-storage](./hidden-storage.md) | 숨김 수납 | Hidden Storage | candidate | storage-system |
| [modular-storage](./modular-storage.md) | 모듈 수납 | Modular Storage | candidate | storage-system |
| [vertical-storage](./vertical-storage.md) | 수직 수납 | Vertical Storage | candidate | storage-system |
| [multifunctional-furniture](./multifunctional-furniture.md) | 멀티유즈 가구 | Multifunctional Furniture | candidate | compact-living-solution |
| [appliance-garage](./appliance-garage.md) | 어플라이언스 가라지 | Appliance Garage | candidate | kitchen-storage |
| [circadian-lighting](./circadian-lighting.md) | 서커디언 조명 | Circadian Lighting | candidate | wellness-lighting |
| [invisible-technology](./invisible-technology.md) | 보이지 않는 기술 | Invisible Technology | candidate | smart-home |

## 5. Material / CMF Concept

| ID | 한국어명 | 영문명 | 상태 | Parent |
|---|---|---|---|---|
| [warm-neutral-palette](./warm-neutral-palette.md) | 웜 뉴트럴 팔레트 | Warm Neutral Palette | candidate | color-palette |
| [natural-materiality](./natural-materiality.md) | 자연 소재성 | Natural Materiality | candidate | material-strategy |
| [tactile-materiality](./tactile-materiality.md) | 촉각적 소재감 | Tactile Materiality | candidate | material-strategy |
| [light-oak](./light-oak.md) | 밝은 우드 | Light Oak | supporting | wood-tone |
| [brushed-metal](./brushed-metal.md) | 브러시드 메탈 | Brushed Metal | supporting | metal-finish |

## 6. Market Concept

| ID | 한국어명 | 영문명 | 상태 | Parent |
|---|---|---|---|---|
| [premium-living](./premium-living.md) | 프리미엄 리빙 | Premium Living | canonical | market-positioning |
| [quiet-premium](./quiet-premium.md) | 조용한 프리미엄 | Quiet Premium | candidate | premium-positioning |
| [affordable-premium](./affordable-premium.md) | 합리적 프리미엄 | Affordable Premium | candidate | price-positioning |
| [material-storytelling](./material-storytelling.md) | 소재 스토리텔링 | Material Storytelling | candidate | brand-communication |

## Concept로 승격하지 않고 Entity/Attribute로 관리할 항목

다음은 중요하지만 현재 단계에서는 독립 Concept보다 속성 또는 상품 Entity로 관리하는 것이 적합하다.

- 컬러: 아이보리, 베이지, 오트밀, 샌드 베이지
- 소재: 린넨, 부클레, 울, 세라믹, 스톤
- 상품: 패브릭 소파, 러그, 우드 테이블, 협탁, 테이블 램프, 매트리스
- 수납 상품: 붙박이장, 수납형 침대, 리프트업 테이블, 수납 벤치
- 주방 상품: 인덕션, 식기세척기, 키큰장, 주방 타일

이 Entity들은 Concept 문서의 `핵심 구성요소`, `관계 Triple`, `검색어` 영역에서 연결한다.
