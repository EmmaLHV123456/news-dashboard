"""
News sources configuration for VC-focused crypto/AI aggregator
"""

# RSS Feeds - Funding & Industry News
RSS_FEEDS = {
    # Crypto Funding & News
    "the_block": "https://www.theblock.co/rss.xml",
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "cointelegraph": "https://cointelegraph.com/rss",
    "decrypt": "https://decrypt.co/feed",
    "blockworks": "https://blockworks.co/feed",
    "messari": "https://messari.io/rss",
    "unchained": "https://unchainedcrypto.com/feed/",

    # AI/Tech Funding
    "techcrunch_ai": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "techcrunch_crypto": "https://techcrunch.com/category/cryptocurrency/feed/",
    "venturebeat_ai": "https://venturebeat.com/category/ai/feed/",
    "mit_tech_review": "https://www.technologyreview.com/feed/",
    "wired_ai": "https://www.wired.com/feed/tag/ai/latest/rss",

    # VC & Founder Blogs
    "a16z_crypto": "https://a16zcrypto.com/feed/",
    "a16z_main": "https://a16z.com/feed/",
    "paradigm": "https://www.paradigm.xyz/feed.xml",
    "variant": "https://variant.fund/feed/",
    "polychain": "https://polychain.capital/feed/",

    # AI Labs & Research
    "openai_blog": "https://openai.com/blog/rss/",
    "anthropic_news": "https://www.anthropic.com/news/rss",
    "deepmind": "https://deepmind.google/blog/rss.xml",

    # Regulatory
    "sec_press": "https://www.sec.gov/news/pressreleases.rss",

    # Hacker News (top stories - will filter for relevance)
    "hn_front": "https://hnrss.org/frontpage",
}

# Keywords for filtering relevant news
FUNDING_KEYWORDS = [
    "raises", "raised", "funding", "seed", "series a", "series b",
    "investment", "venture", "backed", "million", "valuation",
    "pre-seed", "angel", "round", "investors", "led by"
]

REGULATORY_KEYWORDS = [
    "sec", "cftc", "regulation", "bill", "act", "congress", "senate",
    "enforcement", "lawsuit", "settlement", "clarity", "stablecoin",
    "etf", "approval", "framework", "compliance", "executive order"
]

CRYPTO_KEYWORDS = [
    "bitcoin", "ethereum", "crypto", "blockchain", "defi", "nft",
    "web3", "token", "protocol", "layer 2", "l2", "dao", "staking"
]

AI_KEYWORDS = [
    "ai", "artificial intelligence", "llm", "gpt", "machine learning",
    "neural", "openai", "anthropic", "model", "training", "inference"
]

# Categories for organizing news
CATEGORIES = {
    "funding": FUNDING_KEYWORDS,
    "regulatory": REGULATORY_KEYWORDS,
    "crypto": CRYPTO_KEYWORDS,
    "ai": AI_KEYWORDS,
}
