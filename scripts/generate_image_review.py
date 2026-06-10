#!/usr/bin/env python3
"""
data/image_candidates.json 을 읽어 image_review.html 을 생성한다.
브라우저에서 열어 각 문서별로 적용할 이미지를 라디오 버튼으로 선택하고,
"다운로드" 버튼으로 image_decisions.json을 받는다. (1회성 스크립트)

사용법: python3 scripts/generate_image_review.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_PATH = ROOT / 'data' / 'image_candidates.json'
OUT_PATH = ROOT / 'image_review.html'


def main():
    data = json.loads(CANDIDATES_PATH.read_text(encoding='utf-8'))

    sections = []
    for key, entry in sorted(data.items(), key=lambda kv: (kv[1]['type'], kv[1]['slug'])):
        candidates = sorted(
            entry['candidates'],
            key=lambda c: (c['priority'] is None, c['priority'])
        )

        cards = []
        for i, c in enumerate(candidates):
            checked = 'checked' if i == 0 else ''
            if c['fetch_status'] == 'ok':
                img_html = f'<img src="{c["image_url"]}" loading="lazy" onerror="this.closest(\'.card\').classList.add(\'broken\')">'
            else:
                img_html = f'<div class="placeholder">이미지 없음<br><small>{c["fetch_status"]}</small></div>'

            cards.append(f'''
            <label class="card">
              <div class="thumb">{img_html}</div>
              <div class="meta">
                <input type="radio" name="{key}" value="{i}" {checked}>
                <span class="src">#{c['priority']} {c['source_title'] or ''}</span>
                <a class="link" href="{c['source_page_url']}" target="_blank" rel="noopener">출처 페이지 ↗</a>
              </div>
            </label>''')

        cards.append(f'''
            <label class="card none">
              <div class="thumb"><div class="placeholder">사용 안 함</div></div>
              <div class="meta">
                <input type="radio" name="{key}" value="none">
                <span class="src">이 문서에 이미지를 적용하지 않음</span>
              </div>
            </label>''')

        sections.append(f'''
      <section class="doc" data-key="{key}">
        <h2>{entry['title']} <span class="badge">{entry['type']}</span> <span class="slug">{entry['slug']}</span></h2>
        <p class="query">검색어: {entry['query']}</p>
        <div class="grid">{''.join(cards)}</div>
      </section>''')

    candidates_json = json.dumps(data, ensure_ascii=False)

    html_doc = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>이미지 검토</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background: #111; color: #eee; margin: 0; padding: 1.5rem; }}
  h1 {{ font-size: 1.4rem; }}
  .toolbar {{ position: sticky; top: 0; background: #111; padding: 0.75rem 0; z-index: 10; border-bottom: 1px solid #333; margin-bottom: 1rem; }}
  .toolbar button {{ font-size: 1rem; padding: 0.5rem 1.2rem; border-radius: 8px; border: none; background: #4f8cff; color: #fff; cursor: pointer; }}
  .toolbar span {{ margin-left: 1rem; color: #999; font-size: 0.85rem; }}
  section.doc {{ margin-bottom: 2rem; border-bottom: 1px solid #333; padding-bottom: 1rem; }}
  h2 {{ font-size: 1rem; font-weight: 600; }}
  .badge {{ font-size: 0.7rem; background: #333; padding: 0.1rem 0.5rem; border-radius: 4px; color: #aaa; }}
  .slug {{ font-size: 0.75rem; color: #666; }}
  .query {{ font-size: 0.75rem; color: #888; margin: 0.2rem 0 0; }}
  .grid {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.5rem; }}
  .card {{ width: 220px; border: 2px solid #333; border-radius: 8px; padding: 0.5rem; cursor: pointer; display: flex; flex-direction: column; gap: 0.4rem; }}
  .card:has(input:checked) {{ border-color: #4f8cff; background: #1a2740; }}
  .card.broken .thumb img {{ display: none; }}
  .card.broken .thumb::after {{ content: "이미지 로드 실패"; color: #f55; font-size: 0.8rem; }}
  .thumb {{ width: 100%; height: 130px; background: #000; border-radius: 4px; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
  .thumb img {{ width: 100%; height: 100%; object-fit: cover; }}
  .placeholder {{ color: #777; font-size: 0.8rem; text-align: center; }}
  .meta {{ font-size: 0.75rem; display: flex; flex-direction: column; gap: 0.2rem; }}
  .meta .src {{ color: #ddd; font-weight: 600; }}
  .meta .use {{ color: #999; }}
  .meta .link {{ color: #4f8cff; text-decoration: none; }}
  .card.none {{ width: 120px; }}
  .card.none .thumb {{ height: 130px; }}
</style>
</head>
<body>
  <h1>이미지 후보 검토 ({len(data)}개 문서)</h1>
  <div class="toolbar">
    <button onclick="downloadDecisions()">선택 결과 다운로드 (image_decisions.json)</button>
    <span>각 문서마다 적용할 이미지를 하나 선택하거나 "사용 안 함"을 선택한 뒤 다운로드하세요.</span>
  </div>
  {''.join(sections)}

<script>
const CANDIDATES = {candidates_json};

function downloadDecisions() {{
  const decisions = {{}};
  document.querySelectorAll('section.doc').forEach(section => {{
    const key = section.dataset.key;
    const checked = section.querySelector(`input[name="${{key}}"]:checked`);
    if (!checked || checked.value === 'none') return;
    const idx = parseInt(checked.value, 10);
    const entry = CANDIDATES[key];
    const sorted = [...entry.candidates].sort((a, b) => {{
      const pa = a.priority ?? Infinity, pb = b.priority ?? Infinity;
      return pa - pb;
    }});
    const c = sorted[idx];
    decisions[key] = {{
      type: entry.type,
      slug: entry.slug,
      image_url: c.image_url,
      image_source_url: c.source_page_url,
    }};
  }});
  const blob = new Blob([JSON.stringify(decisions, null, 2)], {{ type: 'application/json' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'image_decisions.json';
  a.click();
}}
</script>
</body>
</html>'''

    OUT_PATH.write_text(html_doc, encoding='utf-8')
    print(f'생성 완료: {OUT_PATH} ({len(data)}개 문서)')


if __name__ == '__main__':
    main()
