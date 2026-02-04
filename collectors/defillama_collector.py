"""
DefiLlama Raises API collector - free funding data for crypto projects
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict


DEFILLAMA_RAISES_URL = "https://api.llama.fi/raises"


def fetch_recent_raises(days_back: int = 7) -> List[Dict]:
    """Fetch recent funding rounds from DefiLlama"""
    raises = []
    cutoff = datetime.now() - timedelta(days=days_back)

    try:
        response = requests.get(DEFILLAMA_RAISES_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        for raise_data in data.get("raises", []):
            # DefiLlama uses Unix timestamp
            timestamp = raise_data.get("date", 0)
            raise_date = datetime.fromtimestamp(timestamp)

            if raise_date > cutoff:
                amount = raise_data.get("amount")
                amount_str = f"${amount}M" if amount else "Undisclosed"

                investors = raise_data.get("leadInvestors", [])
                other_investors = raise_data.get("otherInvestors", [])
                all_investors = investors + other_investors

                raises.append({
                    "project": raise_data.get("name", "Unknown"),
                    "amount": amount_str,
                    "amount_raw": amount or 0,
                    "round": raise_data.get("round", "Unknown"),
                    "category": raise_data.get("category", ""),
                    "lead_investors": investors,
                    "all_investors": all_investors[:10],  # Limit for display
                    "date": raise_date.isoformat(),
                    "source": "defillama",
                    "chains": raise_data.get("chains", []),
                })

    except Exception as e:
        print(f"Error fetching DefiLlama raises: {e}")

    # Sort by amount (largest first), then by date
    raises.sort(key=lambda x: (x["amount_raw"], x["date"]), reverse=True)
    return raises


def format_raise_for_display(raise_data: Dict) -> str:
    """Format a raise for text display"""
    investors_str = ", ".join(raise_data["lead_investors"][:3]) or "Undisclosed"
    return (
        f"{raise_data['project']} - {raise_data['amount']} "
        f"({raise_data['round']}) - Led by: {investors_str}"
    )


if __name__ == "__main__":
    # Test run
    raises = fetch_recent_raises(days_back=14)
    print(f"Found {len(raises)} raises in the last 14 days\n")

    print("--- Recent Crypto Funding Rounds ---")
    for r in raises[:15]:
        print(f"  {format_raise_for_display(r)}")
