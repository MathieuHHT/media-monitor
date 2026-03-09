#!/usr/bin/env python3
"""
Media monitoring scraper.
Searches Google News RSS for configured keywords, uses Claude API to
translate and summarize Thai articles, and writes results to docs/data.json.
"""

import json
import os
import re
import sys
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus, urljoin
from xml.etree import ElementTree

import requests

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_FILE = PROJECT_ROOT / "docs" / "data.json"

# ── import local config ────────────────────────────────────────────────
sys.path.insert(0, str(SCRIPT_DIR))
from config import PEOPLE, COMPANIES, SEARCH_QUERIES, PRIORITY_OUTLETS


# ── helpers ────────────────────────────────────────────────────────────
def article_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]


def load_existing() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"articles": [], "last_updated": None, "scan_history": []}


def save_data(data: dict):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def search_google_news_rss(query: str, max_results: int = 20) -> list[dict]:
    """Fetch articles from Google News RSS feed for a query."""
    encoded = quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded}+when:7d&hl=th&gl=TH&ceid=TH:th"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MediaMonitor/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"  [WARN] RSS fetch failed for '{query}': {e}")
        return []

    articles = []
    try:
        root = ElementTree.fromstring(r.content)
        for item in root.findall(".//item")[:max_results]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pub_date = item.findtext("pubDate", "")
            source = item.findtext("source", "")
            description = item.findtext("description", "")
            # Strip HTML from description
            description = re.sub(r"<[^>]+>", "", description).strip()
            if link:
                articles.append({
                    "title_original": title,
                    "url": link,
                    "pub_date": pub_date,
                    "source": source,
                    "description_original": description,
                })
    except ElementTree.ParseError as e:
        print(f"  [WARN] XML parse failed: {e}")

    return articles


def detect_people_mentions(text: str) -> list[dict]:
    """Check which tracked people are mentioned in a text."""
    mentions = []
    text_lower = text.lower()
    for key, person in PEOPLE.items():
        for term in person["search_terms"]:
            if term.lower() in text_lower or term in text:
                mentions.append({
                    "key": key,
                    "name_en": person["name_en"],
                    "role": person["role"],
                    "priority": person["priority"],
                })
                break
    for key, company in COMPANIES.items():
        for term in company["search_terms"]:
            if term.lower() in text_lower or term in text:
                mentions.append({
                    "key": key,
                    "name_en": company["name"],
                    "role": "Company",
                    "priority": company["priority"],
                })
                break
    return mentions


def is_priority_outlet(source: str, url: str) -> bool:
    combined = (source + " " + url).lower()
    return any(outlet in combined for outlet in PRIORITY_OUTLETS)


def translate_and_summarize(articles: list[dict], api_key: str) -> list[dict]:
    """Use Claude API to translate titles and create English summaries."""
    if not articles:
        return articles

    # Process in batches of 10
    batch_size = 10
    for i in range(0, len(articles), batch_size):
        batch = articles[i : i + batch_size]
        items_text = ""
        for idx, a in enumerate(batch):
            items_text += (
                f"\n--- Article {idx + 1} ---\n"
                f"Title: {a.get('title_original', '')}\n"
                f"Source: {a.get('source', '')}\n"
                f"Description: {a.get('description_original', '')}\n"
            )

        prompt = f"""You are a media monitoring assistant. Below are {len(batch)} Thai news articles about the aromatic coconut (มะพร้าวน้ำหอม) industry, the Department of Business Development (กรมพัฒนาธุรกิจการค้า), nominees (นอมินี), and related topics.

For each article, provide:
1. "title_en": English translation of the title
2. "summary_en": A 1-2 sentence English summary of the article's content
3. "sentiment": one of "positive", "negative", "neutral"

Respond ONLY with a JSON array (no markdown, no backticks). Each element should have keys: title_en, summary_en, sentiment.

{items_text}"""

        try:
            r = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 4000,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=60,
            )
            r.raise_for_status()
            resp = r.json()
            text = "".join(
                block.get("text", "") for block in resp.get("content", [])
            )
            text = text.strip().removeprefix("```json").removesuffix("```").strip()
            translations = json.loads(text)

            for idx, t in enumerate(translations):
                if i + idx < len(articles):
                    articles[i + idx]["title_en"] = t.get("title_en", "")
                    articles[i + idx]["summary_en"] = t.get("summary_en", "")
                    articles[i + idx]["sentiment"] = t.get("sentiment", "neutral")

        except Exception as e:
            print(f"  [WARN] Claude API translation failed for batch {i}: {e}")
            for idx in range(len(batch)):
                if i + idx < len(articles):
                    articles[i + idx]["title_en"] = articles[i + idx].get("title_original", "")
                    articles[i + idx]["summary_en"] = "Translation unavailable"
                    articles[i + idx]["sentiment"] = "neutral"

        time.sleep(1)  # rate limiting

    return articles


# ── main ───────────────────────────────────────────────────────────────
def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not set. Skipping translation.")

    print("=== Media Monitor Scan ===")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")

    data = load_existing()
    existing_urls = {a["url"] for a in data["articles"]}

    # Collect articles from all search queries
    all_raw = []
    seen_urls = set()
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")
        results = search_google_news_rss(query)
        print(f"  Found {len(results)} results")
        for art in results:
            if art["url"] not in seen_urls and art["url"] not in existing_urls:
                seen_urls.add(art["url"])
                all_raw.append(art)

    print(f"\nNew articles found: {len(all_raw)}")

    if not all_raw:
        print("No new articles. Updating timestamp only.")
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        data["scan_history"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "new_articles": 0,
        })
        save_data(data)
        return

    # Detect people mentions
    for art in all_raw:
        combined_text = " ".join([
            art.get("title_original", ""),
            art.get("description_original", ""),
            art.get("source", ""),
        ])
        art["people_mentioned"] = detect_people_mentions(combined_text)
        art["is_priority_outlet"] = is_priority_outlet(
            art.get("source", ""), art.get("url", "")
        )
        art["id"] = article_id(art["url"])

    # Translate and summarize
    if api_key:
        print("Translating and summarizing with Claude API...")
        all_raw = translate_and_summarize(all_raw, api_key)
    else:
        for art in all_raw:
            art["title_en"] = art.get("title_original", "")
            art["summary_en"] = "Translation unavailable — no API key"
            art["sentiment"] = "neutral"

    # Add scan metadata
    scan_time = datetime.now(timezone.utc).isoformat()
    for art in all_raw:
        art["first_seen"] = scan_time

    # Merge with existing
    data["articles"] = all_raw + data["articles"]
    # Keep last 500 articles
    data["articles"] = data["articles"][:500]
    data["last_updated"] = scan_time
    data["scan_history"].append({
        "timestamp": scan_time,
        "new_articles": len(all_raw),
    })
    # Keep last 60 scan records
    data["scan_history"] = data["scan_history"][-60:]

    save_data(data)
    print(f"Saved {len(all_raw)} new articles. Total: {len(data['articles'])}")
    print("Done.")


if __name__ == "__main__":
    main()
