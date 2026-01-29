#!/usr/bin/env python3
"""
Update missing images for articles and enrichments
Fetches articles/enrichments without images and extracts them from source pages
"""
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

SUPABASE_URL = "https://hqxxapqukrzawrvdlwmu.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhxeHhhcHF1a3J6YXdydmRsd211Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyNzU5MTMsImV4cCI6MjA4NDg1MTkxM30.eGrFJ7HgXdhjfiyq7G8rEb0gitp0pF2pq9ZLzbnGB_4"

def extract_image_from_url(url):
    """
    Extract featured image from article page

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

def get_articles_without_images():
    """Fetch articles that don't have image_url"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/articles",
            headers=headers,
            params={
                "select": "id,title,url,source",
                "image_url": "is.null"
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        return []

def get_enrichments_without_images():
    """Fetch enrichments that don't have image_url"""
    try:
        headers = {
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}"
        }

        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/article_enrichments",
            headers=headers,
            params={
                "select": "id,title,article_id",
                "image_url": "is.null"
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching enrichments: {e}")
        return []

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
            params={
                "select": "url",
                "id": f"eq.{article_id}"
            }
        )
        response.raise_for_status()
        data = response.json()
        return data[0]['url'] if data else None
    except Exception as e:
        print(f"    ❌ Error fetching parent article: {e}")
        return None

def main():
    print("🖼️  Updating missing images...")
    print()

    # Update articles
    print("📰 Checking articles...")
    articles = get_articles_without_images()
    print(f"   Found {len(articles)} articles without images")

    updated_articles = 0
    for article in articles:
        print(f"\n   Processing: {article['title'][:60]}...")
        image_url = extract_image_from_url(article['url'])

        if image_url:
            if update_article_image(article['id'], image_url):
                print(f"   ✅ Updated with image: {image_url[:60]}...")
                updated_articles += 1
            else:
                print(f"   ❌ Failed to update")
        else:
            print(f"   ⚠️  No image found")

    print(f"\n✅ Updated {updated_articles} articles")

    # Update enrichments
    print("\n🔍 Checking enrichments...")
    enrichments = get_enrichments_without_images()
    print(f"   Found {len(enrichments)} enrichments without images")

    updated_enrichments = 0
    for enrichment in enrichments:
        print(f"\n   Processing: {enrichment['title'][:60]}...")

        # Get parent article URL
        parent_url = get_parent_article_url(enrichment['article_id'])
        if not parent_url:
            print(f"   ⚠️  Could not find parent article")
            continue

        # Try to extract image from parent article page
        # Note: Enrichments typically share images from the same article page
        image_url = extract_image_from_url(parent_url)

        if image_url:
            if update_enrichment_image(enrichment['id'], image_url):
                print(f"   ✅ Updated with image: {image_url[:60]}...")
                updated_enrichments += 1
            else:
                print(f"   ❌ Failed to update")
        else:
            print(f"   ⚠️  No image found")

    print(f"\n✅ Updated {updated_enrichments} enrichments")
    print(f"\n📊 Total: {updated_articles} articles + {updated_enrichments} enrichments = {updated_articles + updated_enrichments} images added")

if __name__ == "__main__":
    main()
