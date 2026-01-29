#!/usr/bin/env python3
"""
Orchestrator
Runs all scrapers and saves results to Supabase
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrape_bensbites import scrape_bensbites
from scrape_rundown import scrape_rundown
from save_to_supabase import save_articles

def main():
    """Run all scrapers and save to Supabase"""
    print("🚀 Starting AI News Aggregator Orchestrator\n")
    print("=" * 60)
    
    all_articles = []
    
    # Run Ben's Bites scraper
    print("\n1️⃣  BEN'S BITES")
    print("-" * 60)
    try:
        bensbites_articles = scrape_bensbites()
        all_articles.extend(bensbites_articles)
    except Exception as e:
        print(f"❌ Ben's Bites scraper failed: {e}")
    
    # Run The Rundown AI scraper
    print("\n2️⃣  THE RUNDOWN AI")
    print("-" * 60)
    try:
        rundown_articles = scrape_rundown()
        all_articles.extend(rundown_articles)
    except Exception as e:
        print(f"❌ The Rundown AI scraper failed: {e}")
    
    # Save to Supabase
    print("\n3️⃣  SAVING TO SUPABASE")
    print("-" * 60)
    if all_articles:
        try:
            stats = save_articles(all_articles)
            
            print("\n" + "=" * 60)
            print("✅ ORCHESTRATOR COMPLETE")
            print("=" * 60)
            print(f"📊 Total articles collected: {len(all_articles)}")
            print(f"💾 Successfully saved: {stats['success']}")
            print(f"⏭️  Skipped (duplicates): {stats['skipped']}")
            print(f"❌ Errors: {stats['errors']}")
            
        except Exception as e:
            print(f"❌ Failed to save to Supabase: {e}")
            print("💡 Make sure you've configured .env with Supabase credentials")
    else:
        print("⚠️  No articles collected from any source")
        print("=" * 60)

if __name__ == "__main__":
    main()
