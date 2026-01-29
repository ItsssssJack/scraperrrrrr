#!/usr/bin/env python3
"""
Quick script to load demo data into Supabase
"""
import json
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(url, key)

def load_demo_data():
    """Load demo data from JSON file into Supabase"""
    print("🚀 Loading demo data into Supabase...")

    # Read demo data
    with open('demo-data.json', 'r') as f:
        articles = json.load(f)

    success_count = 0
    error_count = 0

    for article in articles:
        try:
            # Remove 'id' from article as Supabase will auto-generate
            article_data = {k: v for k, v in article.items() if k != 'id'}

            # Check if article already exists by URL
            existing = supabase.table('articles').select('id').eq('url', article_data['url']).execute()

            if existing.data:
                print(f"⏭️  Skipping (exists): {article_data['title'][:50]}...")
            else:
                # Insert article
                result = supabase.table('articles').insert(article_data).execute()
                print(f"✅ Saved: {article_data['title'][:50]}...")
                success_count += 1

        except Exception as e:
            print(f"❌ Error: {article_data.get('title', 'Unknown')[:50]}... - {e}")
            error_count += 1

    print("\n" + "=" * 60)
    print("✅ DEMO DATA LOAD COMPLETE")
    print("=" * 60)
    print(f"💾 Successfully saved: {success_count}")
    print(f"⏭️  Skipped (duplicates): {len(articles) - success_count - error_count}")
    print(f"❌ Errors: {error_count}")

if __name__ == "__main__":
    load_demo_data()
