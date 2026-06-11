import type { TopicNode } from './types'

// concept_type -> 위키 챕터(topics_config) 매칭 키워드.
// 챕터 번호는 재배치될 수 있으므로 title/label의 키워드로 매칭한다.
export const CONCEPT_TYPE_TOPIC_KEYWORDS: Record<string, string[]> = {
  style:      ['스타일', 'style'],
  lifestyle:  ['스타일', 'style'],
  material:   ['스타일', 'style', '공간', 'space'],
  spatial:    ['공간', 'space'],
  functional: ['카테고리', 'category'],
  market:     ['마케팅', 'marketing'],
}

export function topicsForConceptType(
  conceptType: string | null | undefined,
  topics: TopicNode[]
): TopicNode[] {
  if (!conceptType) return []
  const keywords = CONCEPT_TYPE_TOPIC_KEYWORDS[conceptType]
  if (!keywords) return []
  return topics.filter((t) =>
    keywords.some((k) =>
      t.title.toLowerCase().includes(k.toLowerCase()) ||
      t.label.toLowerCase().includes(k.toLowerCase())
    )
  )
}
