#!/usr/bin/env python3
"""
discover_sources.py — RSS 피드 자동 수집 → 스코어링 → ingest

표준 라이브러리 + openai만 사용.
수동 승인 없음. 점수 6점 이상이면 자동으로 /api/ingest 호출 →
runIngest() → synthesizeConcepts()까지 자동 실행됨.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import quote

from openai import OpenAI

FEEDS = [
    {"url": "https://blog.ohou.se/feed", "publisher": "오늘의집 블로그"},
    {"url": "https://www.kidp.or.kr/rss.do", "publisher": "한국디자인진흥원"},
    {"url": "https://www.seouldesign.or.kr/rss/news", "publisher": "서울디자인재단"},
    {"url": "https://rss.hankyung.com/economy/life.xml", "publisher": "한경 라이프"},
    {"url": "https://www.chosun.com/rss/life.xml", "publisher": "조선일보 라이프"},
]

ITEMS_PER_FEED = 10
SCORE_THRESHOLD = 6
RATE_LIMIT_SEC = 1
USER_AGENT = "Mozilla/5.0 (compatible; HomestyleWikiBot/1.0)"

INGEST_API_URL = os.environ["INGEST_API_URL"].rstrip("/")
INGEST_SECRET = os.environ["INGEST_SECRET"]

client = OpenAI()


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read()


def parse_feed(xml_bytes: bytes) -> list[dict]:
    """RSS 2.0 / Atom 피드를 파싱해 [{title, link}, ...] 반환."""
    root = ET.fromstring(xml_bytes)
    items = []

    # RSS 2.0: rss/channel/item
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title and link:
            items.append({"title": title, "link": link})

    if items:
        return items

    # Atom: feed/entry
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = (entry.findtext("atom:title", namespaces=ns) or "").strip()
        link_el = entry.find("atom:link", ns)
        link = link_el.get("href", "").strip() if link_el is not None else ""
        if title and link:
            items.append({"title": title, "link": link})

    return items


def source_exists(url: str) -> bool:
    api_url = f"{INGEST_API_URL}/api/sources/exists?url={quote(url, safe='')}"
    try:
        data = json.loads(fetch(api_url))
        return bool(data.get("exists"))
    except Exception as e:
        print(f"    [warn] 중복 확인 실패: {e}")
        return False


def score_item(title: str, url: str) -> int:
    """관련성(0-4) + 품질(0-3) + 독창성(0-2) + 최신성(0-1) = 0-10점."""
    prompt = f"""다음 글이 한국 리빙·인테리어·디자인 트렌드 위키에 적합한지 평가하세요.

제목: {title}
URL: {url}

아래 4개 기준으로 점수를 매기고 합계를 계산하세요:
- 관련성 (0-4): 리빙/인테리어/디자인/공간 트렌드와의 관련도
- 품질 (0-3): 정보의 깊이와 신뢰도
- 독창성 (0-2): 새로운 정보나 관점 포함 여부
- 최신성 (0-1): 최근 트렌드 반영 여부

JSON으로만 응답하세요: {{"relevance": N, "quality": N, "originality": N, "freshness": N, "total": N}}"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    data = json.loads(res.choices[0].message.content)
    return int(data.get("total", 0))


def fetch_content(url: str) -> str:
    """Jina Reader로 본문 텍스트 추출."""
    return fetch(f"https://r.jina.ai/{url}", timeout=60).decode("utf-8", errors="ignore")


def ingest(title: str, raw_content: str, url: str, publisher: str) -> dict:
    payload = json.dumps({
        "title": title,
        "raw_content": raw_content,
        "url": url,
        "publisher": publisher,
        "source_type": "external",
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{INGEST_API_URL}/api/ingest",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {INGEST_SECRET}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        return json.loads(res.read())


def main() -> None:
    for feed in FEEDS:
        print(f"\n=== {feed['publisher']} ({feed['url']}) ===")

        try:
            items = parse_feed(fetch(feed["url"]))[:ITEMS_PER_FEED]
        except Exception as e:
            print(f"  [error] 피드 가져오기 실패: {e}")
            continue

        print(f"  {len(items)}개 항목 발견")

        for item in items:
            title, url = item["title"], item["link"]
            print(f"  - {title}")

            if source_exists(url):
                print("    이미 존재함, 스킵")
                time.sleep(RATE_LIMIT_SEC)
                continue

            try:
                score = score_item(title, url)
            except Exception as e:
                print(f"    [error] 스코어링 실패: {e}")
                time.sleep(RATE_LIMIT_SEC)
                continue

            print(f"    점수: {score}")

            if score < SCORE_THRESHOLD:
                print("    점수 미달, 스킵")
                time.sleep(RATE_LIMIT_SEC)
                continue

            try:
                raw_content = fetch_content(url)
                result = ingest(title, raw_content, url, feed["publisher"])
                print(f"    ingest 완료: {result.get('source_id')}")
            except Exception as e:
                print(f"    [error] ingest 실패: {e}")

            time.sleep(RATE_LIMIT_SEC)


if __name__ == "__main__":
    sys.exit(main())
