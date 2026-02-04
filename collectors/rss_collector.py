"""
RSS Feed collector for crypto/AI news
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import config


def fetch_rss_feed(url: str, source_name: str) -> List[Dict]:
    """Fetch and parse a single RSS feed"""
    articles = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # Last 20 items per feed
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            if published:
                pub_date = datetime(*published[:6])
            else:
                pub_date = datetime.now()

            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "source": source_name,
                "published": pub_date.isoformat(),
                "summary": entry.get("summary", "")[:500],
            })
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
    return articles


def categorize_article(article: Dict) -> List[str]:
    """Categorize article based on keywords"""
    text = (article["title"] + " " + article["summary"]).lower()
    categories = []
    for category, keywords in config.CATEGORIES.items():
        if any(kw in text for kw in keywords):
            categories.append(category)
    return categories if categories else ["general"]


def is_funding_news(article: Dict) -> bool:
    """Check if article is about funding/investment"""
    text = (article["title"] + " " + article["summary"]).lower()
    return any(kw in text for kw in config.FUNDING_KEYWORDS)


def is_regulatory_news(article: Dict) -> bool:
    """Check if article is about regulation/policy"""
    text = (article["title"] + " " + article["summary"]).lower()
    return any(kw in text for kw in config.REGULATORY_KEYWORDS)


def collect_all_feeds(hours_back: int = 24) -> List[Dict]:
    """Collect articles from all configured RSS feeds"""
    all_articles = []
    cutoff = datetime.now() - timedelta(hours=hours_back)

    for source_name, url in config.RSS_FEEDS.items():
        print(f"Fetching {source_name}...")
        articles = fetch_rss_feed(url, source_name)

        for article in articles:
            pub_date = datetime.fromisoformat(article["published"])
            if pub_date > cutoff:
                article["categories"] = categorize_article(article)
                article["is_funding"] = is_funding_news(article)
                article["is_regulatory"] = is_regulatory_news(article)
                all_articles.append(article)

    # Sort by date, newest first
    all_articles.sort(key=lambda x: x["published"], reverse=True)
    return all_articles


if __name__ == "__main__":
    # Test run
    articles = collect_all_feeds(hours_back=48)
    print(f"\nCollected {len(articles)} articles")

    funding = [a for a in articles if a["is_funding"]]
    regulatory = [a for a in articles if a["is_regulatory"]]

    print(f"Funding news: {len(funding)}")
    print(f"Regulatory news: {len(regulatory)}")

    print("\n--- Top Funding News ---")
    for a in funding[:5]:
        print(f"  [{a['source']}] {a['title']}")
