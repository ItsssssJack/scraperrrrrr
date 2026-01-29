"""
Modal App for AI News Scraper
Runs scrapers every 24 hours and saves to Supabase
"""

import modal

# Create Modal app
app = modal.App("ai-news-scraper")

# Define the image with all dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "requests==2.31.0",
    "beautifulsoup4==4.12.2",
    "feedparser==6.0.10",
    "python-dotenv==1.0.0",
    "supabase>=2.10.0",  # Updated to latest version
    "praw==7.7.1",
    "python-dateutil==2.8.2",
    "lxml==5.1.0",
)

# Define secrets for environment variables
@app.function(
    image=image,
    secrets=[modal.Secret.from_name("supabase-credentials")],
    schedule=modal.Cron("0 0 * * *"),  # Run daily at midnight UTC
    timeout=600,  # 10 minute timeout
)
def run_scrapers():
    """
    Main function that runs all scrapers and saves to Supabase.
    Scheduled to run every 24 hours.
    """
    import os
    import requests
    from bs4 import BeautifulSoup
    import feedparser
    from datetime import datetime, timezone
    from supabase import create_client
    
    print("🚀 Starting AI News Aggregator (Modal Scheduled Run)")
    print("=" * 60)
    
    # Initialize Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase = create_client(supabase_url, supabase_key)
    
    all_articles = []
    
    # ============================================
    # Ben's Bites Scraper
    # ============================================
    print("\n1️⃣  BEN'S BITES")
    print("-" * 60)
    try:
        feed_url = "https://www.bensbites.co/feed"
        feed = feedparser.parse(feed_url)
        
        bensbites_articles = []
        for entry in feed.entries[:10]:  # Get last 10 articles
            article = {
                'title': entry.get('title', 'No title'),
                'url': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'author': entry.get('author', 'Ben\'s Bites'),
                'published_date': datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat() if hasattr(entry, 'published_parsed') else datetime.now(timezone.utc).isoformat(),
                'source': 'bensbites',
                'image_url': None
            }
            
            # Try to extract image from content
            if 'content' in entry and len(entry.content) > 0:
                soup = BeautifulSoup(entry.content[0].value, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    article['image_url'] = img['src']
            
            bensbites_articles.append(article)
        
        all_articles.extend(bensbites_articles)
        print(f"✅ Collected {len(bensbites_articles)} articles from Ben's Bites")
    except Exception as e:
        print(f"❌ Ben's Bites scraper failed: {e}")
    
    # ============================================
    # The Rundown AI Scraper
    # ============================================
    print("\n2️⃣  THE RUNDOWN AI")
    print("-" * 60)
    try:
        feed_url = "https://www.therundown.ai/feed"
        feed = feedparser.parse(feed_url)
        
        rundown_articles = []
        for entry in feed.entries[:10]:  # Get last 10 articles
            article = {
                'title': entry.get('title', 'No title'),
                'url': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'author': entry.get('author', 'The Rundown AI'),
                'published_date': datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat() if hasattr(entry, 'published_parsed') else datetime.now(timezone.utc).isoformat(),
                'source': 'rundown',
                'image_url': None
            }
            
            # Try to extract image from content
            if 'content' in entry and len(entry.content) > 0:
                soup = BeautifulSoup(entry.content[0].value, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    article['image_url'] = img['src']
            
            rundown_articles.append(article)
        
        all_articles.extend(rundown_articles)
        print(f"✅ Collected {len(rundown_articles)} articles from The Rundown")
    except Exception as e:
        print(f"❌ The Rundown AI scraper failed: {e}")
    
    # ============================================
    # Save to Supabase
    # ============================================
    print("\n3️⃣  SAVING TO SUPABASE")
    print("-" * 60)
    
    if all_articles:
        try:
            stats = {'success': 0, 'skipped': 0, 'errors': 0}
            
            for article in all_articles:
                try:
                    # Check if article already exists
                    existing = supabase.table('articles').select('id').eq('url', article['url']).execute()
                    
                    if existing.data:
                        print(f"⏭️  Skipped (duplicate): {article['title'][:50]}...")
                        stats['skipped'] += 1
                    else:
                        # Insert new article
                        supabase.table('articles').insert(article).execute()
                        print(f"💾 Saved: {article['title'][:50]}...")
                        stats['success'] += 1
                        
                except Exception as e:
                    print(f"❌ Error saving article: {e}")
                    stats['errors'] += 1
            
            print("\n" + "=" * 60)
            print("✅ SCRAPER RUN COMPLETE")
            print("=" * 60)
            print(f"📊 Total articles collected: {len(all_articles)}")
            print(f"💾 Successfully saved: {stats['success']}")
            print(f"⏭️  Skipped (duplicates): {stats['skipped']}")
            print(f"❌ Errors: {stats['errors']}")
            
            return {
                "status": "success",
                "total_articles": len(all_articles),
                "saved": stats['success'],
                "skipped": stats['skipped'],
                "errors": stats['errors']
            }
            
        except Exception as e:
            print(f"❌ Failed to save to Supabase: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    else:
        print("⚠️  No articles collected from any source")
        print("=" * 60)
        return {
            "status": "warning",
            "message": "No articles collected"
        }


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("supabase-credentials")],
)
def run_scrapers_manual():
    """
    Manual trigger function for testing.
    Run with: modal run modal_scraper.py::run_scrapers_manual
    """
    return run_scrapers.remote()


@app.local_entrypoint()
def main():
    """
    Local entrypoint for testing.
    Run with: modal run modal_scraper.py
    """
    print("🧪 Running scrapers manually for testing...")
    result = run_scrapers_manual.remote()
    print(f"\n📋 Result: {result}")
