#!/usr/bin/env python3
"""
Check what's in Supabase
"""
import os
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(url, key)

print("🔍 Checking Supabase database...\n")

# Get all articles
response = supabase.table('articles').select('*').execute()
articles = response.data

print(f"📊 Total articles in database: {len(articles)}\n")

if articles:
    print("Articles found:")
    for article in articles:
        print(f"  - {article['title'][:60]}")
        print(f"    Published: {article['published_date']}")
        print(f"    Source: {article['source']}")
        print()

    # Check 24 hour filter
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    print(f"\n⏰ 24 hours ago: {twenty_four_hours_ago.isoformat()}")

    response_24h = supabase.table('articles').select('*').gte('published_date', twenty_four_hours_ago.isoformat()).execute()
    print(f"📊 Articles from last 24 hours: {len(response_24h.data)}")
else:
    print("❌ No articles found in database!")
