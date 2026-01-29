#!/usr/bin/env python3
"""
Update article dates to current time
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

print("🔄 Updating article dates to current time...\n")

# Get all articles
response = supabase.table('articles').select('*').execute()
articles = response.data

now = datetime.now()

for i, article in enumerate(articles):
    # Set each article to a time within the last few hours
    new_date = now - timedelta(hours=i)

    supabase.table('articles').update({
        'published_date': new_date.isoformat()
    }).eq('id', article['id']).execute()

    print(f"✅ Updated: {article['title'][:50]}... -> {new_date.isoformat()}")

print("\n✅ All article dates updated!")
