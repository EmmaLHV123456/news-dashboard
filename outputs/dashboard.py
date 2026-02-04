"""
Generate static HTML dashboard for news aggregator
Outputs to docs/ folder for GitHub Pages deployment
"""
import os
from datetime import datetime
from typing import List, Dict


def generate_dashboard(articles: List[Dict], raises: List[Dict], output_dir: str = "docs") -> str:
    """Generate a static HTML dashboard"""

    os.makedirs(output_dir, exist_ok=True)

    funding_articles = [a for a in articles if a.get("is_funding")][:15]
    regulatory_articles = [a for a in articles if a.get("is_regulatory")][:15]
    crypto_articles = [a for a in articles if "crypto" in a.get("categories", [])][:15]
    ai_articles = [a for a in articles if "ai" in a.get("categories", [])][:15]
    top_raises = raises[:15]

    last_updated = datetime.now().strftime("%B %d, %Y at %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frontier Tech Dashboard</title>
    <meta http-equiv="refresh" content="1800"> <!-- Auto-refresh every 30 min -->
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #e4e4e4;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 30px;
        }}

        h1 {{
            font-size: 2.5rem;
            background: linear-gradient(90deg, #e94560, #0f4c75);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}

        .updated {{
            color: #888;
            font-size: 0.9rem;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin: 20px 0;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #e94560;
        }}

        .stat-label {{
            color: #888;
            font-size: 0.85rem;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .card h2 {{
            color: #e94560;
            font-size: 1.2rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #333;
        }}

        .card.funding h2 {{ color: #4ade80; }}
        .card.regulatory h2 {{ color: #f59e0b; }}
        .card.crypto h2 {{ color: #8b5cf6; }}
        .card.ai h2 {{ color: #06b6d4; }}

        .article {{
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .article:last-child {{
            border-bottom: none;
        }}

        .article a {{
            color: #fff;
            text-decoration: none;
            font-weight: 500;
            line-height: 1.4;
            display: block;
        }}

        .article a:hover {{
            color: #e94560;
        }}

        .article-meta {{
            font-size: 0.8rem;
            color: #666;
            margin-top: 5px;
        }}

        .source {{
            color: #888;
        }}

        .raise {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .raise:last-child {{
            border-bottom: none;
        }}

        .raise-project {{
            font-weight: 600;
        }}

        .raise-amount {{
            color: #4ade80;
            font-weight: bold;
        }}

        .raise-details {{
            font-size: 0.8rem;
            color: #888;
            margin-top: 3px;
        }}

        .tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            margin-right: 5px;
        }}

        .tag.funding {{ background: rgba(74, 222, 128, 0.2); color: #4ade80; }}
        .tag.regulatory {{ background: rgba(245, 158, 11, 0.2); color: #f59e0b; }}

        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            h1 {{
                font-size: 1.8rem;
            }}
            .stats {{
                flex-wrap: wrap;
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Frontier Tech Dashboard</h1>
            <p class="updated">Last updated: {last_updated}</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{len(articles)}</div>
                    <div class="stat-label">Articles</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(funding_articles)}</div>
                    <div class="stat-label">Funding News</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(top_raises)}</div>
                    <div class="stat-label">Raises (7d)</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(regulatory_articles)}</div>
                    <div class="stat-label">Regulatory</div>
                </div>
            </div>
        </header>

        <div class="grid">
            <!-- Funding Rounds -->
            <div class="card funding">
                <h2>💰 Crypto Funding Rounds</h2>
"""

    for r in top_raises:
        investors = ", ".join(r.get("lead_investors", [])[:2]) or "Undisclosed"
        html += f"""
                <div class="raise">
                    <div>
                        <div class="raise-project">{r['project']}</div>
                        <div class="raise-details">{r['round']} · {investors}</div>
                    </div>
                    <div class="raise-amount">{r['amount']}</div>
                </div>
"""

    html += """
            </div>

            <!-- Funding News -->
            <div class="card funding">
                <h2>📈 Funding News</h2>
"""

    for a in funding_articles:
        source = a.get('source', 'unknown')
        date = a.get('published', '')[:10]
        html += f"""
                <div class="article">
                    <a href="{a['link']}" target="_blank">{a['title']}</a>
                    <div class="article-meta">
                        <span class="source">{source}</span> · {date}
                    </div>
                </div>
"""

    html += """
            </div>

            <!-- Regulatory -->
            <div class="card regulatory">
                <h2>⚖️ Regulatory & Policy</h2>
"""

    for a in regulatory_articles:
        source = a.get('source', 'unknown')
        date = a.get('published', '')[:10]
        html += f"""
                <div class="article">
                    <a href="{a['link']}" target="_blank">{a['title']}</a>
                    <div class="article-meta">
                        <span class="source">{source}</span> · {date}
                    </div>
                </div>
"""

    html += """
            </div>

            <!-- Crypto -->
            <div class="card crypto">
                <h2>🔗 Crypto & Web3</h2>
"""

    for a in crypto_articles[:10]:
        source = a.get('source', 'unknown')
        date = a.get('published', '')[:10]
        html += f"""
                <div class="article">
                    <a href="{a['link']}" target="_blank">{a['title']}</a>
                    <div class="article-meta">
                        <span class="source">{source}</span> · {date}
                    </div>
                </div>
"""

    html += """
            </div>

            <!-- AI -->
            <div class="card ai">
                <h2>🤖 AI & Machine Learning</h2>
"""

    for a in ai_articles[:10]:
        source = a.get('source', 'unknown')
        date = a.get('published', '')[:10]
        html += f"""
                <div class="article">
                    <a href="{a['link']}" target="_blank">{a['title']}</a>
                    <div class="article-meta">
                        <span class="source">{source}</span> · {date}
                    </div>
                </div>
"""

    html += """
            </div>
        </div>
    </div>
</body>
</html>
"""

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Dashboard generated: {output_path}")
    return output_path


if __name__ == "__main__":
    # Test with sample data
    sample_articles = [
        {"title": "Test Article", "link": "#", "source": "test", "published": "2024-01-01",
         "is_funding": True, "is_regulatory": False, "categories": ["crypto", "funding"]}
    ]
    sample_raises = [
        {"project": "TestCo", "amount": "$10M", "round": "Seed", "lead_investors": ["a16z"], "date": "2024-01-01"}
    ]
    generate_dashboard(sample_articles, sample_raises)
