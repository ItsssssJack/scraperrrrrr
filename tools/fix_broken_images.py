#!/usr/bin/env python3
"""
Fix broken image URLs that return 404 or other errors
Tests all image URLs and re-scrapes broken ones from source pages
"""
import requests
from bs4 import BeautifulSoup
import time

SUPABASE_URL = "https://hqxxapqukrzawrvdlwmu.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhxeHhhcHF1a3J6YXdydmRsd211Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyNzU5MTMsImV4cCI6MjA4NDg1MTkxM30.eGrFJ7HgXdhjfiyq7G8rEb0gitp0pF2pq9ZLzbnGB_4"

def test_image_url(url):
    """Test if image URL is accessible"""
    if not url:
        return False

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def extract_image_from_url(url):
    """Extract featured image from article page"""
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
            img_url = og_image['content']
            if test_image_url(img_url):
                return img_url

        # Method 2: Twitter card image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            img_url = twitter_image['content']
            if test_image_url(img_url):
                return img_url

        # Method 3: First image in article content
        article_img = soup.find('article')
        if article_img:
            img = article_img.find('img')
            if img and img.get('src'):
                img_url = img['src']
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif not img_url.startswith('http'):
                    img_url = 'https://' + url.split('/')[2] + img_url
                if test_image_url(img_url):
                    return img_url

        return None

    except Exception as e:
        print(f"    ⚠️  Could not extract image: {e}")
        return None

def get_all_articles():
    """Fetch all articles"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/articles",
            headers=headers,
            params={"select": "id,title,url,source,image_url"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        return []

def get_all_enrichments():
    """Fetch all enrichments"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/article_enrichments",
            headers=headers,
            params={"select": "id,title,article_id,image_url"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching enrichments: {e}")
        return []

def get_parent_article_url(article_id):
    """Get parent article URL for an enrichment"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/articles",
            headers=headers,
            params={"select": "url", "id": f"eq.{article_id}"}
        )
        response.raise_for_status()
        data = response.json()
        return data[0]['url'] if data else None
    except Exception as e:
        return None

def update_article_image(article_id, image_url):
    """Update article with new image URL"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/articles",
            headers=headers,
            params={"id": f"eq.{article_id}"},
            json={"image_url": image_url}
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"    ❌ Error updating article: {e}")
        return False

def update_enrichment_image(enrichment_id, image_url):
    """Update enrichment with new image URL"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/article_enrichments",
            headers=headers,
            params={"id": f"eq.{enrichment_id}"},
            json={"image_url": image_url}
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"    ❌ Error updating enrichment: {e}")
        return False

def main():
    print("🔍 Checking all image URLs...")
    print()

    # Check articles
    print("📰 Checking articles...")
    articles = get_all_articles()
    print(f"   Found {len(articles)} articles")

    broken_articles = []
    for article in articles:
        if not test_image_url(article.get('image_url')):
            broken_articles.append(article)

    print(f"   ❌ Found {len(broken_articles)} articles with broken/missing images")

    fixed_articles = 0
    for article in broken_articles:
        print(f"\n   Fixing: {article['title'][:50]}...")
        print(f"   Old URL: {article.get('image_url', 'None')[:60]}...")

        new_image_url = extract_image_from_url(article['url'])

        if new_image_url:
            if update_article_image(article['id'], new_image_url):
                print(f"   ✅ Updated with: {new_image_url[:60]}...")
                fixed_articles += 1
            else:
                print(f"   ❌ Failed to update")
        else:
            print(f"   ⚠️  Could not find a working image")

        time.sleep(0.5)  # Be polite to servers

    print(f"\n✅ Fixed {fixed_articles}/{len(broken_articles)} articles")

    # Check enrichments
    print("\n🔍 Checking enrichments...")
    enrichments = get_all_enrichments()
    print(f"   Found {len(enrichments)} enrichments")

    broken_enrichments = []
    for enrichment in enrichments:
        if not test_image_url(enrichment.get('image_url')):
            broken_enrichments.append(enrichment)

    print(f"   ❌ Found {len(broken_enrichments)} enrichments with broken/missing images")

    fixed_enrichments = 0
    for enrichment in broken_enrichments:
        print(f"\n   Fixing: {enrichment['title'][:50]}...")
        print(f"   Old URL: {enrichment.get('image_url', 'None')[:60]}...")

        # Get parent article URL
        parent_url = get_parent_article_url(enrichment['article_id'])
        if not parent_url:
            print(f"   ⚠️  Could not find parent article")
            continue

        new_image_url = extract_image_from_url(parent_url)

        if new_image_url:
            if update_enrichment_image(enrichment['id'], new_image_url):
                print(f"   ✅ Updated with: {new_image_url[:60]}...")
                fixed_enrichments += 1
            else:
                print(f"   ❌ Failed to update")
        else:
            print(f"   ⚠️  Could not find a working image")

        time.sleep(0.5)  # Be polite to servers

    print(f"\n✅ Fixed {fixed_enrichments}/{len(broken_enrichments)} enrichments")
    print(f"\n📊 Total fixed: {fixed_articles + fixed_enrichments} images")

if __name__ == "__main__":
    main()
