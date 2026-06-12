"""
교육·학습 목적이며, 사용 시 각 사이트의 robots.txt와 이용약관을 확인할 것
주의: 크롤링 시 대상 사이트의 robots.txt와 이용약관을 확인하고,
요청 간 간격(delay)을 두어 서버에 부담을 주지 않도록 한다.
"""

import time
import json
import csv
import xml.etree.ElementTree as ET
from urllib.parse import quote
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# 실제 브라우저처럼 보이게 하는 헤더 (차단 회피 기본)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}

# 요청 간 대기 시간(초) — 서버 부담을 줄이고 차단을 피하기 위함
REQUEST_DELAY = 1.5


def fetch_news_list(keyword: str, limit: int = 20) -> list[dict]:
    """
    구글 뉴스 RSS에서 키워드로 기사 목록을 가져온다.
    RSS는 구조가 단순하고 공개돼 있어 크롤링에 가장 안정적이다.
    """
    encoded = quote(keyword)
    url = (
        f"https://news.google.com/rss/search?"
        f"q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
    )

    print(f"[*] 뉴스 목록 요청: {keyword}")
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    # RSS(XML) 파싱
    root = ET.fromstring(resp.content)
    items = root.findall(".//item")

    articles = []
    for item in items[:limit]:
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        pub_date = item.findtext("pubDate", default="").strip()
        source_el = item.find("source")
        source = source_el.text.strip() if source_el is not None and source_el.text else ""

        articles.append({
            "title": title,
            "link": link,
            "source": source,
            "published": pub_date,
        })

    print(f"[+] 기사 {len(articles)}건 수집 완료")
    return articles


def fetch_article_body(url: str) -> str:
    """
    개별 기사 페이지에서 본문 텍스트를 추출한다.
    사이트마다 HTML 구조가 달라 완벽하진 않지만,
    일반적인 <article>, <p> 태그를 기준으로 텍스트를 모은다.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"    [!] 본문 요청 실패: {e}")
        return ""

    soup = BeautifulSoup(resp.text, "lxml")

    # 불필요한 태그 제거
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # 우선순위: <article> > 본문 후보 div > 전체 <p>
    container = soup.find("article")
    if container:
        paragraphs = container.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    text = "\n".join(
        p.get_text(strip=True)
        for p in paragraphs
        if len(p.get_text(strip=True)) > 20  # 짧은 잡텍스트 제외
    )
    return text.strip()


def crawl(keyword: str, max_articles: int = 10, with_body: bool = True) -> list[dict]:
    """전체 크롤링 파이프라인 실행."""
    articles = fetch_news_list(keyword, limit=max_articles)

    if with_body:
        for i, article in enumerate(articles, 1):
            print(f"[*] ({i}/{len(articles)}) 본문 수집: {article['title'][:40]}...")
            article["body"] = fetch_article_body(article["link"])
            time.sleep(REQUEST_DELAY)  # 예의 있는 크롤링: 간격 두기

    return articles


def save_results(articles: list[dict], basename: str = "korea_czech_news"):
    """결과를 JSON과 CSV 두 형식으로 저장."""
    # JSON 저장 (본문 포함, 전체 데이터 보존)
    json_path = f"{basename}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[+] 저장 완료: {json_path}")

    # CSV 저장 (엑셀에서 보기 좋게, 본문은 길어서 제외)
    csv_path = f"{basename}.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["title", "source", "published", "link"]
        )
        writer.writeheader()
        for a in articles:
            writer.writerow({k: a.get(k, "") for k in writer.fieldnames})
    print(f"[+] 저장 완료: {csv_path}")


if __name__ == "__main__":
    # 검색 키워드 — 경기를 특정할 수 있게 구체적으로
    KEYWORD = "월드컵 대한민국 체코"

    print("=" * 50)
    print("2026 월드컵 한국 vs 체코 뉴스 크롤링 시작")
    print(f"시작 시각: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 50)

    results = crawl(KEYWORD, max_articles=10, with_body=True)
    save_results(results)

    # 수집 결과 요약 출력
    print("\n" + "=" * 50)
    print("수집된 기사 제목 목록:")
    for i, a in enumerate(results, 1):
        print(f"  {i}. [{a['source']}] {a['title']}")
    print("=" * 50)