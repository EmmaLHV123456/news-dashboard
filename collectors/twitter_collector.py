"""
Twitter/X collector for VC and crypto/AI founder announcements
Requires Twitter API v2 Bearer Token ($100/mo for Basic tier)
"""
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

TWITTER_API_BASE = "https://api.twitter.com/2"

# Curated list of accounts to follow
# Format: username -> category
TWITTER_ACCOUNTS = {
    # Top Crypto VCs
    "a]6z_crypto": "vc",
    "paradigm": "vc",
    "polyabordan": "vc",  # Polychain
    "haaborun_sun": "vc",  # Dragonfly
    "cburniske": "vc",  # Placeholder
    "balaborji": "vc",  # Placeholder
    "FredEhrsam": "vc",  # Paradigm
    "cdixon": "vc",  # a16z

    # AI VCs & Founders
    "sama": "ai",  # Sam Altman
    "AnthropicAI": "ai",
    "OpenAI": "ai",
    "ylecun": "ai",  # Yann LeCun
    "kaborarpathy": "ai",  # Andrej Karpathy
    "emaborad": "ai",  # Emad (Stability)

    # Crypto Founders
    "VitalikButerin": "crypto",
    "caborz_brian": "crypto",  # Coinbase
    "SBF_FTX": "crypto",  # for historical context
    "staborni": "crypto",  # Stani (Aave)
    "haydaborams": "crypto",  # Uniswap

    # Crypto Journalists
    "laurashin": "journalist",
    "FraborSchabs": "journalist",
    "TheBlock__": "journalist",
}

# Keywords that indicate funding/deal announcements
DEAL_KEYWORDS = [
    "raised", "raising", "funding", "invested", "backing",
    "series a", "series b", "seed", "announcing", "launched",
    "partnering", "acquired", "acquisition", "ipo", "token launch"
]


def get_twitter_client() -> Optional[str]:
    """Get Twitter Bearer Token from environment"""
    token = os.getenv("TWITTER_BEARER_TOKEN")
    if not token:
        return None
    return token


def fetch_user_tweets(username: str, bearer_token: str, max_results: int = 10) -> List[Dict]:
    """Fetch recent tweets from a user"""
    tweets = []

    try:
        # First get user ID
        user_url = f"{TWITTER_API_BASE}/users/by/username/{username}"
        headers = {"Authorization": f"Bearer {bearer_token}"}
        user_resp = requests.get(user_url, headers=headers, timeout=10)

        if user_resp.status_code != 200:
            return tweets

        user_data = user_resp.json()
        user_id = user_data.get("data", {}).get("id")
        if not user_id:
            return tweets

        # Then get tweets
        tweets_url = f"{TWITTER_API_BASE}/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics",
            "exclude": "retweets,replies"
        }

        tweets_resp = requests.get(tweets_url, headers=headers, params=params, timeout=10)

        if tweets_resp.status_code == 200:
            data = tweets_resp.json()
            for tweet in data.get("data", []):
                tweets.append({
                    "username": username,
                    "text": tweet.get("text", ""),
                    "created_at": tweet.get("created_at", ""),
                    "metrics": tweet.get("public_metrics", {}),
                    "url": f"https://twitter.com/{username}/status/{tweet['id']}",
                })

    except Exception as e:
        print(f"Error fetching @{username}: {e}")

    return tweets


def is_deal_related(tweet_text: str) -> bool:
    """Check if tweet is about a deal/funding"""
    text_lower = tweet_text.lower()
    return any(kw in text_lower for kw in DEAL_KEYWORDS)


def collect_twitter_feed(hours_back: int = 24) -> List[Dict]:
    """Collect tweets from all tracked accounts"""
    bearer_token = get_twitter_client()
    if not bearer_token:
        print("Twitter API not configured (set TWITTER_BEARER_TOKEN)")
        return []

    all_tweets = []
    cutoff = datetime.now() - timedelta(hours=hours_back)

    for username, category in TWITTER_ACCOUNTS.items():
        print(f"  Fetching @{username}...")
        tweets = fetch_user_tweets(username, bearer_token)

        for tweet in tweets:
            try:
                created = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
                created = created.replace(tzinfo=None)
                if created > cutoff:
                    tweet["category"] = category
                    tweet["is_deal"] = is_deal_related(tweet["text"])
                    tweet["source"] = "twitter"
                    all_tweets.append(tweet)
            except Exception:
                continue

    # Sort by engagement (likes + retweets)
    all_tweets.sort(
        key=lambda x: x["metrics"].get("like_count", 0) + x["metrics"].get("retweet_count", 0),
        reverse=True
    )

    return all_tweets


def format_tweet_for_digest(tweet: Dict) -> Dict:
    """Convert tweet to standard article format for digest"""
    return {
        "title": tweet["text"][:100] + ("..." if len(tweet["text"]) > 100 else ""),
        "link": tweet["url"],
        "source": f"@{tweet['username']}",
        "published": tweet["created_at"],
        "summary": tweet["text"],
        "categories": ["twitter", tweet["category"]],
        "is_funding": tweet["is_deal"],
        "is_regulatory": False,
    }


if __name__ == "__main__":
    # Test run
    tweets = collect_twitter_feed(hours_back=48)
    print(f"\nCollected {len(tweets)} tweets")

    deal_tweets = [t for t in tweets if t["is_deal"]]
    print(f"Deal-related: {len(deal_tweets)}")

    print("\n--- Top Tweets ---")
    for t in tweets[:10]:
        likes = t["metrics"].get("like_count", 0)
        print(f"  @{t['username']} ({likes} likes): {t['text'][:80]}...")
