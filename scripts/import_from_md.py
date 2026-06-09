#!/usr/bin/env python3
"""
import_from_md.py — kb/wiki/ → Neon Postgres 일괄 임포트
최초 1회만 실행한다.

pip install psycopg2-binary python-frontmatter
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import frontmatter
    import psycopg2
    from psycopg2.extras import Json
except ImportError as e:
    sys.exit(f"❌ 의존 패키지 없음: {e}\n   pip install psycopg2-binary python-frontmatter")


# ─────────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────────

def slugify(text: str, max_len: int = 80) -> str:
    """소문자 영숫자·한글·하이픈만 허용, 80자 제한."""
    text = text.lower().strip()
    text = re.sub(r'[\s_]+', '-', text)
    # 영숫자, 한글(AC00-D7A3, 1100-11FF, 3130-318F), 하이픈 유지
    text = re.sub(r'[^a-z0-9ᄀ-ᇿ㄰-㆏가-힣\-]', '', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:max_len]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def strip_md_inline(text: str) -> str:
    """볼드·이탤릭·링크 마크다운만 제거."""
    text = re.sub(r'\*{1,3}(.+?)\*{1,3}', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    return text.strip()


def upsert_setting(cur, key: str, value: str) -> None:
    cur.execute("""
        INSERT INTO settings (key, value, updated_at)
        VALUES (%s, %s, now())
        ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now()
    """, (key, value))


# ─────────────────────────────────────────────────
# 1. Concepts
# ─────────────────────────────────────────────────

def extract_brief(body: str) -> str | None:
    """'### 한 줄 정의' 다음 첫 단락 추출."""
    lines = body.splitlines()
    capture = False
    for line in lines:
        if re.match(r'^###\s+한 줄 정의', line.strip()):
            capture = True
            continue
        if capture:
            if line.startswith('#'):
                break
            stripped = strip_md_inline(line.strip())
            if stripped:
                return stripped
    return None


def import_concepts(cur, wiki_dir: Path, dry_run: bool) -> int:
    concepts_dir = wiki_dir / 'concepts'
    if not concepts_dir.exists():
        print('[concepts] 디렉터리 없음, skip')
        return 0

    # 직속 .md 파일만 (data/ 하위·_ 시작·README 제외)
    files = sorted(
        f for f in concepts_dir.glob('*.md')
        if not f.name.startswith('_') and f.name.lower() != 'readme.md'
    )

    count = 0
    for md_file in files:
        post = frontmatter.load(str(md_file))
        meta = post.metadata

        slug = slugify(md_file.stem)
        cid  = f'concept_{slug}'

        # 제목: korean_name → canonical_name → stem
        title = (meta.get('korean_name') or meta.get('canonical_name') or md_file.stem)

        aliases          = meta.get('aliases', []) or []
        related_concepts = meta.get('related_concepts', []) or []
        concept_type     = meta.get('concept_type') or None
        concept_status   = meta.get('concept_status') or 'candidate'

        conf_raw = meta.get('confidence')
        if isinstance(conf_raw, dict):
            confidence = int(conf_raw.get('score', 0))
        elif isinstance(conf_raw, (int, float)):
            confidence = int(conf_raw)
        else:
            confidence = 0

        brief   = extract_brief(post.content)
        content = post.content

        print(f'  [concept] {slug}  ({concept_status}, conf={confidence})')

        if not dry_run:
            cur.execute("""
                INSERT INTO concepts
                  (id, title, slug, brief, aliases, topics, related_concepts,
                   concept_type, concept_status, confidence,
                   content, source_count, updated_at)
                VALUES (%s,%s,%s,%s,%s,'{}',%s,%s,%s,%s,%s,0,now())
                ON CONFLICT (id) DO UPDATE SET
                  title            = EXCLUDED.title,
                  brief            = EXCLUDED.brief,
                  aliases          = EXCLUDED.aliases,
                  related_concepts = EXCLUDED.related_concepts,
                  concept_type     = EXCLUDED.concept_type,
                  concept_status   = EXCLUDED.concept_status,
                  confidence       = EXCLUDED.confidence,
                  content          = EXCLUDED.content,
                  updated_at       = now()
            """, (
                cid, title, slug, brief,
                aliases, related_concepts,
                concept_type, concept_status, confidence,
                content,
            ))
        count += 1

    return count


# ─────────────────────────────────────────────────
# 2. Pages
# ─────────────────────────────────────────────────

SKIP_FILENAMES = {'index.md', 'source-notes.md', 'README.md'}
SKIP_DIRS      = {'00-overview', 'data', 'templates'}

NUMBERED_H2 = re.compile(r'^##\s+(\d+)\.\s+(.+)$')


def extract_page_meta(meta: dict, body: str) -> tuple[str, str | None, list[dict]]:
    """title, summary, subsections 추출."""
    # title: 프론트매터 → # 헤딩 순
    title = meta.get('title', '')
    if not title:
        for line in body.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break

    # subsections: ## 헤딩 파싱
    subsections: list[dict] = []
    seq = 0
    first_section_lines: list[str] = []
    in_first_section = False
    summary: str | None = None

    for line in body.splitlines():
        if line.startswith('## '):
            heading = line[3:].strip()
            seq += 1
            m = NUMBERED_H2.match(line)
            if m:
                subsections.append({'number': m.group(1), 'title': m.group(2).strip()})
            else:
                subsections.append({'number': str(seq), 'title': heading})

            in_first_section = (seq == 1)
            continue

        if in_first_section and not summary:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                summary = strip_md_inline(stripped)
                in_first_section = False

    # fallback: frontmatter keywords → 첫 200자
    if not summary:
        plain = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
        plain = re.sub(r'\s+', ' ', plain).strip()
        summary = plain[:200] or None

    return title, summary, subsections


def import_pages(cur, wiki_dir: Path, dry_run: bool) -> int:
    pages_dir = wiki_dir / 'pages'
    if not pages_dir.exists():
        print('[pages] 디렉터리 없음, skip')
        return 0

    count = 0
    for chapter_dir in sorted(pages_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue
        if chapter_dir.name in SKIP_DIRS or not re.match(r'^\d{2}-', chapter_dir.name):
            continue

        chapter_number = chapter_dir.name[:2]

        for md_file in sorted(chapter_dir.glob('*.md')):
            if md_file.name in SKIP_FILENAMES:
                continue

            post = frontmatter.load(str(md_file))
            meta = post.metadata
            slug = md_file.stem
            pid  = f'page_{slug}'

            title, summary, subsections = extract_page_meta(meta, post.content)
            if not title:
                title = slug

            # topics: frontmatter keywords 우선
            topics = meta.get('keywords', []) or meta.get('topics', []) or []

            print(f'  [page]    {chapter_number}/{slug}')

            if not dry_run:
                cur.execute("""
                    INSERT INTO pages
                      (id, slug, title, chapter_number, subsections,
                       summary, topics, content, updated_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now())
                    ON CONFLICT (id) DO UPDATE SET
                      title          = EXCLUDED.title,
                      chapter_number = EXCLUDED.chapter_number,
                      subsections    = EXCLUDED.subsections,
                      summary        = EXCLUDED.summary,
                      topics         = EXCLUDED.topics,
                      content        = EXCLUDED.content,
                      updated_at     = now()
                """, (
                    pid, slug, title, chapter_number,
                    Json(subsections), summary, topics, post.content,
                ))
            count += 1

    return count


# ─────────────────────────────────────────────────
# 3. Editorial
# ─────────────────────────────────────────────────

def import_editorial(cur, wiki_dir: Path, dry_run: bool) -> None:
    editorial_file = wiki_dir / 'editorial' / 'main.md'
    if not editorial_file.exists():
        print('[editorial] main.md 없음 → 빈 값으로 초기화')
        if not dry_run:
            upsert_setting(cur, 'editorial_content', '')
            upsert_setting(cur, 'editorial_versions', '[]')
        return

    content  = editorial_file.read_text(encoding='utf-8')
    versions = json.dumps([{
        'label':    'Initial import',
        'content':  content,
        'saved_at': now_iso(),
        'is_draft': False,
    }], ensure_ascii=False)
    if not dry_run:
        upsert_setting(cur, 'editorial_content',  content)
        upsert_setting(cur, 'editorial_versions', versions)
    print('[editorial] 임포트 완료')


# ─────────────────────────────────────────────────
# 4. Topics (topic-map.md)
# ─────────────────────────────────────────────────

H2_CHAPTER = re.compile(r'^## (\d{2}) · (.+?) \((.+?)\)\s*$')


def import_topics(cur, wiki_dir: Path, dry_run: bool) -> None:
    topic_map_file = wiki_dir / 'topics' / 'topic-map.md'
    if not topic_map_file.exists():
        print('[topics] topic-map.md 없음, skip')
        return

    topics: list[dict] = []
    current: dict | None = None
    in_subtopics = False

    for line in topic_map_file.read_text(encoding='utf-8').splitlines():
        m = H2_CHAPTER.match(line)
        if m:
            if current:
                topics.append(current)
            current = {
                'number':    m.group(1),
                'title':     m.group(2).strip(),
                'label':     m.group(3).strip(),
                'subtopics': [],
            }
            in_subtopics = False
            continue

        if current and re.match(r'^###\s+서브토픽', line):
            in_subtopics = True
            continue

        if current and in_subtopics:
            if line.startswith('- '):
                current['subtopics'].append(line[2:].strip())
            elif line.startswith('#'):
                in_subtopics = False

    if current:
        topics.append(current)

    value = json.dumps(topics, ensure_ascii=False)
    if not dry_run:
        upsert_setting(cur, 'topics_config', value)
    print(f'[topics] {len(topics)}개 챕터 임포트')


# ─────────────────────────────────────────────────
# 5. Metrics
# ─────────────────────────────────────────────────

def import_metrics(cur, wiki_dir: Path, dry_run: bool) -> None:
    metrics_file = wiki_dir / 'metrics' / 'Homestyle-metrics.md'
    if not metrics_file.exists():
        print('[metrics] Homestyle-metrics.md 없음 → [] 초기화')
        if not dry_run:
            upsert_setting(cur, 'metrics_content', '[]')
        return

    # Card 섹션 파싱: ### card-01 아래 YAML-like 필드
    text  = metrics_file.read_text(encoding='utf-8')
    cards = []
    card_re = re.compile(
        r'###\s+(card-\d+)\s*\n(.*?)(?=###\s+card-|\Z)',
        re.DOTALL
    )
    field_re = re.compile(r'^-?\s*(\w+):\s*(.+)$', re.MULTILINE)

    for m in card_re.finditer(text):
        card: dict = {'id': m.group(1)}
        for fm in field_re.finditer(m.group(2)):
            card[fm.group(1)] = fm.group(2).strip()
        cards.append(card)

    value = json.dumps(cards, ensure_ascii=False)
    if not dry_run:
        upsert_setting(cur, 'metrics_content', value)
    print(f'[metrics] {len(cards)}개 카드 임포트')


# ─────────────────────────────────────────────────
# 6. Sources (선택)
# ─────────────────────────────────────────────────

def import_sources(cur, wiki_dir: Path, dry_run: bool) -> int:
    sources_dir = wiki_dir / 'sources'
    if not sources_dir.exists():
        print('[sources] 디렉터리 없음, skip')
        return 0

    count = 0
    for md_file in sorted(sources_dir.glob('*.md')):
        post = frontmatter.load(str(md_file))
        meta = post.metadata
        sid  = 'source_' + slugify(md_file.stem)

        print(f'  [source]  {md_file.stem}')

        if not dry_run:
            cur.execute("""
                INSERT INTO sources
                  (id, title, url, publisher, published_at,
                   raw_content, status, synthesis_result, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,'done','{}',now())
                ON CONFLICT (id) DO UPDATE SET
                  title       = EXCLUDED.title,
                  raw_content = EXCLUDED.raw_content,
                  updated_at  = now()
            """, (
                sid,
                meta.get('title', md_file.stem),
                meta.get('url'),
                meta.get('publisher'),
                str(meta.get('published_at', '')),
                post.content,
            ))
        count += 1

    return count


# ─────────────────────────────────────────────────
# 7. Summaries (선택)
# ─────────────────────────────────────────────────

def import_summaries(cur, wiki_dir: Path, dry_run: bool) -> int:
    summaries_dir = wiki_dir / 'summaries'
    if not summaries_dir.exists():
        print('[summaries] 디렉터리 없음, skip')
        return 0

    count = 0
    for md_file in sorted(summaries_dir.glob('*.md')):
        post  = frontmatter.load(str(md_file))
        meta  = post.metadata
        sid   = 'source_' + slugify(md_file.stem)
        ai_summary   = post.content
        one_line     = meta.get('one_line_summary', '')
        topics       = meta.get('topics', []) or []

        if not dry_run:
            cur.execute("SELECT id FROM sources WHERE id = %s", (sid,))
            if cur.fetchone():
                cur.execute("""
                    UPDATE sources
                    SET ai_summary = %s, one_line_summary = %s,
                        topics = %s, updated_at = now()
                    WHERE id = %s
                """, (ai_summary, one_line, topics, sid))
            else:
                cur.execute("""
                    INSERT INTO sources
                      (id, title, ai_summary, one_line_summary,
                       topics, status, synthesis_result, updated_at)
                    VALUES (%s,%s,%s,%s,%s,'done','{}',now())
                """, (sid, md_file.stem, ai_summary, one_line, topics))
        count += 1

    return count


# ─────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description='kb/wiki → Neon Postgres 일괄 임포트')
    parser.add_argument(
        '--database-url',
        default=os.environ.get('DATABASE_URL_UNPOOLED'),
        help='Neon direct connection URL (기본값: $DATABASE_URL_UNPOOLED)',
    )
    parser.add_argument('--wiki-dir', default='./kb/wiki', help='kb/wiki 경로')
    parser.add_argument('--dry-run', action='store_true', help='파싱 결과만 출력, DB 쓰기 없음')
    args = parser.parse_args()

    if not args.dry_run and not args.database_url:
        sys.exit('❌ --database-url 또는 $DATABASE_URL_UNPOOLED 를 설정하세요.')

    wiki_dir = Path(args.wiki_dir).resolve()
    if not wiki_dir.exists():
        sys.exit(f'❌ wiki-dir 없음: {wiki_dir}')

    if args.dry_run:
        print('🔍 DRY RUN — DB에 쓰지 않습니다.\n')

    conn = cur = None
    if not args.dry_run:
        conn = psycopg2.connect(args.database_url)
        conn.autocommit = False
        cur = conn.cursor()

    try:
        print('── concepts ─────────────────────────')
        n_concepts = import_concepts(cur, wiki_dir, args.dry_run)

        print('\n── pages ────────────────────────────')
        n_pages = import_pages(cur, wiki_dir, args.dry_run)

        print('\n── settings ─────────────────────────')
        import_editorial(cur, wiki_dir, args.dry_run)
        import_topics(cur, wiki_dir, args.dry_run)
        import_metrics(cur, wiki_dir, args.dry_run)

        print('\n── optional ─────────────────────────')
        n_sources = import_sources(cur, wiki_dir, args.dry_run)
        import_summaries(cur, wiki_dir, args.dry_run)

        if not args.dry_run and conn:
            conn.commit()

        print('\n' + '═' * 50)
        print(f'✅ concepts : {n_concepts}개')
        print(f'✅ pages    : {n_pages}개')
        print(f'✅ sources  : {n_sources}개')
        print('✅ settings : editorial_content, editorial_versions,')
        print('              topics_config, metrics_content')
        print()
        print('⚠️  knowledge_embeddings 는 비어 있습니다.')
        print('   배포 후 /admin → Health 탭 → "전체 Embeddings 재빌드" 실행 필요.')

    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
