#!/usr/bin/env python3
"""
Ben's Bites Scraper
Scrapes latest AI news from Ben's Bites using RSS feed
"""

import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from pathlib import Path

def extract_image_from_article(url):
    """
    Extract featured image from Ben's Bites article page
    
    Args:
        url: Article URL
        
    Returns:
        str: Image URL or None
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple methods to find the image
        # Method 1: Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Method 2: Twitter card image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']
        
        # Method 3: First image in article content
        article_img = soup.find('article')
        if article_img:
            img = article_img.find('img')
            if img and img.get('src'):
                return img['src']
        
        # Method 4: Any image with specific class
        featured_img = soup.find('img', class_=['featured-image', 'post-image', 'hero-image'])
        if featured_img and featured_img.get('src'):
            return featured_img['src']
        
        return None
        
    except Exception as e:
        print(f"    ⚠️  Could not extract image: {e}")
        return None

def scrape_bensbites():
    """
    Scrape Ben's Bites RSS feed for articles from the last 24 hours
    
    Returns:
        list: Array of article dictionaries
    """
    print("🔍 Scraping Ben's Bites...")
    
    RSS_URL = "https://www.bensbites.com/feed"
    articles = []
    
    try:
        # Parse RSS feed
        feed = feedparser.parse(RSS_URL)
        
        if feed.bozo:
            print(f"⚠️  Warning: Feed parsing had issues: {feed.bozo_exception}")
        
        # Calculate 24-hour cutoff
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        
        # Process entries
        for entry in feed.entries:
            try:
                # Parse publication date
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                
                # Only include articles from last 24 hours
                if pub_date < cutoff_time:
                    continue
                
                # Extract article data
                article = {
                    "source": "bensbites",
                    "title": entry.title,
                    "url": entry.link,
                    "published_date": pub_date.isoformat(),
                    "summary": entry.get("summary", ""),
                    "author": entry.get("author", "Ben Tossell"),
                    "image_url": None,
                    "tags": [tag.term for tag in entry.get("tags", [])]
                }
                
                # Try to extract image from RSS first
                if hasattr(entry, "media_content") and entry.media_content:
                    article["image_url"] = entry.media_content[0].get("url")
                elif hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                    article["image_url"] = entry.media_thumbnail[0].get("url")
                
                # If no image in RSS, scrape from article page
                if not article["image_url"]:
                    print(f"    🖼️  Extracting image from article page...")
                    article["image_url"] = extract_image_from_article(entry.link)
                
                articles.append(article)
                print(f"  ✅ {article['title'][:60]}... {'📷' if article['image_url'] else '❌'}")
                
            except Exception as e:
                print(f"  ⚠️  Error processing entry: {e}")
                continue
        
        print(f"✅ Found {len(articles)} articles from Ben's Bites (last 24h)")
        
        # Save to .tmp for debugging
        tmp_dir = Path(__file__).parent.parent / ".tmp"
        tmp_dir.mkdir(exist_ok=True)
        
        with open(tmp_dir / "bensbites_articles.json", "w") as f:
            json.dump(articles, f, indent=2)
        
        return articles
        
    except Exception as e:
        print(f"❌ Error scraping Ben's Bites: {e}")
        return []

if __name__ == "__main__":
    articles = scrape_bensbites()
    print(f"\n📊 Total articles: {len(articles)}")
    
    if articles:
        print("\n📰 Sample article:")
        print(json.dumps(articles[0], indent=2))

