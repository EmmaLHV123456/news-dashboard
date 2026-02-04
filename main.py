#!/usr/bin/env python3
"""
Frontier Tech News Aggregator
Collects crypto/AI funding news and sends daily digests
"""
import os
import argparse
from dotenv import load_dotenv

from collectors import collect_all_feeds, fetch_recent_raises, collect_twitter_feed, format_tweet_for_digest
from outputs import push_articles_to_sheet, push_raises_to_sheet, send_digest_email, generate_dashboard

load_dotenv()


def run_aggregator(
    hours_back: int = 24,
    raises_days: int = 7,
    push_sheets: bool = True,
    send_email: bool = True,
    dry_run: bool = False,
    include_twitter: bool = True,
    build_dashboard: bool = True,
):
    """Main aggregator function"""
    print("=" * 50)
    print("Frontier Tech News Aggregator")
    print("=" * 50)

    # Collect RSS feeds
    print(f"\n[1/6] Collecting RSS feeds (last {hours_back}h)...")
    articles = collect_all_feeds(hours_back=hours_back)
    print(f"      Found {len(articles)} articles")

    funding_news = [a for a in articles if a["is_funding"]]
    regulatory_news = [a for a in articles if a["is_regulatory"]]
    print(f"      - Funding news: {len(funding_news)}")
    print(f"      - Regulatory news: {len(regulatory_news)}")

    # Collect DefiLlama raises
    print(f"\n[2/6] Fetching DefiLlama raises (last {raises_days} days)...")
    raises = fetch_recent_raises(days_back=raises_days)
    print(f"      Found {len(raises)} funding rounds")

    # Collect Twitter feed
    tweets = []
    if include_twitter:
        print(f"\n[3/6] Collecting Twitter feed (last {hours_back}h)...")
        raw_tweets = collect_twitter_feed(hours_back=hours_back)
        tweets = [format_tweet_for_digest(t) for t in raw_tweets]
        deal_tweets = [t for t in tweets if t["is_funding"]]
        print(f"      Found {len(tweets)} tweets ({len(deal_tweets)} deal-related)")
        # Merge tweets into articles
        articles.extend(tweets)
    else:
        print("\n[3/6] Skipping Twitter (disabled or not configured)")

    if dry_run:
        print("\n[DRY RUN] Skipping outputs")
        print("\n--- Top Funding News ---")
        for a in funding_news[:5]:
            print(f"  [{a['source']}] {a['title']}")
        print("\n--- Top Raises ---")
        for r in raises[:5]:
            print(f"  {r['project']} - {r['amount']} ({r['round']})")
        if tweets:
            print("\n--- Top Tweets ---")
            for t in tweets[:5]:
                print(f"  [{t['source']}] {t['title']}")
        return

    # Push to Google Sheets
    if push_sheets:
        spreadsheet_id = os.getenv("SPREADSHEET_ID")
        if spreadsheet_id:
            print("\n[4/6] Pushing to Google Sheets...")
            try:
                push_articles_to_sheet(articles, spreadsheet_id, "News")
                push_raises_to_sheet(raises, spreadsheet_id, "Funding Rounds")
            except Exception as e:
                print(f"      Error: {e}")
        else:
            print("\n[4/6] Skipping Sheets (SPREADSHEET_ID not set)")
    else:
        print("\n[4/6] Skipping Sheets (disabled)")

    # Send email digest
    if send_email:
        print("\n[5/6] Sending email digest...")
        try:
            send_digest_email(articles, raises)
        except Exception as e:
            print(f"      Error: {e}")
    else:
        print("\n[5/6] Skipping email (disabled)")

    # Generate dashboard
    if build_dashboard:
        print("\n[6/6] Generating dashboard...")
        try:
            generate_dashboard(articles, raises)
        except Exception as e:
            print(f"      Error: {e}")
    else:
        print("\n[6/6] Skipping dashboard (disabled)")

    print("\nDone!")


def main():
    parser = argparse.ArgumentParser(description="Frontier Tech News Aggregator")
    parser.add_argument("--hours", type=int, default=24, help="Hours back to fetch news")
    parser.add_argument("--raises-days", type=int, default=7, help="Days back for funding rounds")
    parser.add_argument("--no-sheets", action="store_true", help="Skip Google Sheets push")
    parser.add_argument("--no-email", action="store_true", help="Skip email digest")
    parser.add_argument("--dry-run", action="store_true", help="Collect only, no outputs")
    parser.add_argument("--no-twitter", action="store_true", help="Skip Twitter collection")
    parser.add_argument("--no-dashboard", action="store_true", help="Skip dashboard generation")

    args = parser.parse_args()

    run_aggregator(
        hours_back=args.hours,
        raises_days=args.raises_days,
        push_sheets=not args.no_sheets,
        send_email=not args.no_email,
        dry_run=args.dry_run,
        include_twitter=not args.no_twitter,
        build_dashboard=not args.no_dashboard,
    )


if __name__ == "__main__":
    main()
