#!/usr/bin/env python3
"""
Set default placeholder images for articles with broken/missing images
Uses Unsplash AI-themed images as placeholders
"""
import requests

SUPABASE_URL = "https://hqxxapqukrzawrvdlwmu.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhxeHhhcHF1a3J6YXdydmRsd211Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyNzU5MTMsImV4cCI6MjA4NDg1MTkxM30.eGrFJ7HgXdhjfiyq7G8rEb0gitp0pF2pq9ZLzbnGB_4"

# Unsplash AI-themed placeholder images
DEFAULT_IMAGES = [
    "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=600&fit=crop",  # AI circuit
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200&h=600&fit=crop",  # AI robot
    "https://images.unsplash.com/photo-1655635949384-f737c5133dfe?w=1200&h=600&fit=crop",  # AI abstract
]

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
            params={"select": "id,title,image_url"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
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

def main():
    print("🖼️  Setting default images for broken URLs...")
    print()

    articles = get_all_articles()
    print(f"   Found {len(articles)} articles")

    broken_articles = []
    for article in articles:
        if not test_image_url(article.get('image_url')):
            broken_articles.append(article)

    print(f"   ❌ Found {len(broken_articles)} articles with broken/missing images")
    print()

    fixed = 0
    for i, article in enumerate(broken_articles):
        # Rotate through default images
        default_image = DEFAULT_IMAGES[i % len(DEFAULT_IMAGES)]

        print(f"   Setting default image for: {article['title'][:50]}...")

        if update_article_image(article['id'], default_image):
            print(f"   ✅ Set to: {default_image}")
            fixed += 1
        else:
            print(f"   ❌ Failed to update")
        print()

    print(f"✅ Fixed {fixed}/{len(broken_articles)} articles with default images")

if __name__ == "__main__":
    main()
