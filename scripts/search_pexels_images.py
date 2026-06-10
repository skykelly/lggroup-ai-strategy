#!/usr/bin/env python3
"""
kb/wiki/**/*.md 의 image_references[0].search_query 로 Pexels에서 이미지를 검색해
후보 목록을 data/image_candidates.json 에 저장한다. (1회성 스크립트)

사용법: PEXELS_API_KEY=... python3 scripts/search_pexels_images.py
       (.env 의 PEXELS_API_KEY 를 자동으로 읽음)
"""
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
KB_WIKI = ROOT / 'kb' / 'wiki'
OUT_PATH = ROOT / 'data' / 'image_candidates.json'

PER_PAGE = 6
RATE_LIMIT_SEC = 0.3
TIMEOUT = 15

SKIP_FILENAMES = {'index.md', 'source-notes.md', 'README.md'}
SKIP_DIRS = {'00-overview', 'data', 'templates'}


def load_api_key() -> str:
    key = os.environ.get('PEXELS_API_KEY')
    if key:
        return key.strip()
    env_text = (ROOT / '.env').read_text(encoding='utf-8')
    m = re.search(r'^PEXELS_API_KEY=(.*)$', env_text, re.MULTILINE)
    if not m:
        sys.exit('PEXELS_API_KEY가 .env에 없습니다.')
    return m.group(1).strip()


def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^a-z0-9가-힣ᄀ-ᇿ㄰-㆏\-]', '', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:max_len]


def find_md_files():
    files = []
    for f in sorted((KB_WIKI / 'concepts').glob('*.md')):
        files.append(('concept', f))
    for chapter_dir in sorted((KB_WIKI / 'pages').iterdir()):
        if not chapter_dir.is_dir():
            continue
        if chapter_dir.name in SKIP_DIRS or not re.match(r'^\d{2}-', chapter_dir.name):
            continue
        for f in sorted(chapter_dir.glob('*.md')):
            if f.name in SKIP_FILENAMES:
                continue
            files.append(('page', f))
    return files


def load_frontmatter(md_file: Path):
    text = md_file.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def search_pexels(query: str, api_key: str) -> list:
    resp = requests.get(
        'https://api.pexels.com/v1/search',
        params={'query': query, 'per_page': PER_PAGE, 'orientation': 'landscape'},
        headers={'Authorization': api_key},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    photos = resp.json().get('photos', [])

    candidates = []
    for i, p in enumerate(photos, start=1):
        candidates.append({
            'priority': i,
            'source_title': f'Photo by {p["photographer"]} on Pexels',
            'source_page_url': p['url'],
            'image_use': query,
            'image_url': p['src']['large'],
            'fetch_status': 'ok',
            'fetch_detail': None,
        })
    return candidates


def main():
    api_key = load_api_key()
    files = find_md_files()
    print(f'대상 파일: {len(files)}개')

    output = {}
    for kind, md_file in files:
        meta = load_frontmatter(md_file)

        if kind == 'concept':
            slug = slugify(md_file.stem)
            title = meta.get('korean_name') or meta.get('canonical_name') or md_file.stem
        else:
            slug = md_file.stem
            title = meta.get('title') or md_file.stem

        refs = meta.get('image_references') or []
        query = refs[0].get('search_query') if refs else title

        try:
            candidates = search_pexels(query, api_key)
        except requests.RequestException as e:
            print(f'  [오류] {slug}: {e}')
            candidates = []

        output[f'{kind}:{slug}'] = {
            'type': kind,
            'slug': slug,
            'title': title,
            'query': query,
            'candidates': candidates,
        }
        print(f'[{kind}] {slug}: "{query}" -> {len(candidates)}개')
        time.sleep(RATE_LIMIT_SEC)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')

    total = sum(len(e['candidates']) for e in output.values())
    print(f'\n완료: {len(output)}개 문서, 후보 {total}개')
    print(f'저장 위치: {OUT_PATH}')


if __name__ == '__main__':
    sys.exit(main())
