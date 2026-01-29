#!/usr/bin/env python3
"""
Supabase Save Script
Saves scraped articles and enrichments to Supabase database
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Create and return Supabase client"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env file")
    
    return create_client(url, key)

def save_enrichments(supabase: Client, article_id: str, enrichments: list) -> dict:
    """
    Save article enrichments to Supabase
    
    Args:
        supabase: Supabase client
        article_id: UUID of the parent article
        enrichments: List of enrichment dictionaries
        
    Returns:
        dict: Statistics about the save operation
    """
    if not enrichments:
        return {"success": 0, "errors": 0}
    
    stats = {"success": 0, "errors": 0}
    
    # Delete existing enrichments for this article first
    try:
        supabase.table("article_enrichments").delete().eq("article_id", article_id).execute()
    except Exception as e:
        print(f"    ⚠️  Warning: Could not delete old enrichments: {e}")
    
    # Insert new enrichments
    for enrichment in enrichments:
        try:
            enrichment_data = {
                "article_id": article_id,
                "title": enrichment["title"],
                "summary": enrichment.get("summary", ""),
                "image_url": enrichment.get("image_url"),
                "content": enrichment.get("content", ""),
                "position": enrichment.get("position", 0)
            }
            
            supabase.table("article_enrichments").insert(enrichment_data).execute()
            stats["success"] += 1
            
        except Exception as e:
            stats["errors"] += 1
            print(f"    ❌ Error saving enrichment: {e}")
            continue
    
    return stats

def save_articles_with_enrichments(articles: list, enrichments_map: dict = None) -> dict:
    """
    Save articles and their enrichments to Supabase
    
    Args:
        articles: List of article dictionaries
        enrichments_map: Dict mapping article URLs to their enrichments
        
    Returns:
        dict: Statistics about the save operation
    """
    if not articles:
        print("⚠️  No articles to save")
        return {"articles": {"success": 0, "skipped": 0, "errors": 0}, "enrichments": {"success": 0, "errors": 0}}
    
    print(f"💾 Saving {len(articles)} articles to Supabase...")
    
    try:
        supabase = get_supabase_client()
        
        stats = {
            "articles": {"success": 0, "skipped": 0, "errors": 0},
            "enrichments": {"success": 0, "errors": 0}
        }
        
        for article in articles:
            try:
                # Remove enrichment_count from article data (not in schema)
                article_data = {k: v for k, v in article.items() if k != "enrichment_count"}
                
                # Upsert article (insert or update if URL exists)
                response = supabase.table("articles").upsert(
                    article_data,
                    on_conflict="url"
                ).execute()
                
                if response.data and len(response.data) > 0:
                    article_id = response.data[0]["id"]
                    stats["articles"]["success"] += 1
                    print(f"  ✅ Saved: {article['title'][:60]}...")
                    
                    # Save enrichments if available
                    if enrichments_map and article["url"] in enrichments_map:
                        enrichments = enrichments_map[article["url"]]
                        if enrichments:
                            print(f"    🔍 Saving {len(enrichments)} enrichments...")
                            enrich_stats = save_enrichments(supabase, article_id, enrichments)
                            stats["enrichments"]["success"] += enrich_stats["success"]
                            stats["enrichments"]["errors"] += enrich_stats["errors"]
                            print(f"    ✅ Saved {enrich_stats['success']} enrichments")
                else:
                    stats["articles"]["skipped"] += 1
                    print(f"  ⏭️  Skipped (duplicate): {article['title'][:60]}...")
                    
            except Exception as e:
                stats["articles"]["errors"] += 1
                print(f"  ❌ Error saving article: {e}")
                continue
        
        print(f"\n📊 Save Statistics:")
        print(f"  Articles:")
        print(f"    ✅ Success: {stats['articles']['success']}")
        print(f"    ⏭️  Skipped: {stats['articles']['skipped']}")
        print(f"    ❌ Errors: {stats['articles']['errors']}")
        print(f"  Enrichments:")
        print(f"    ✅ Success: {stats['enrichments']['success']}")
        print(f"    ❌ Errors: {stats['enrichments']['errors']}")
        
        return stats
        
    except Exception as e:
        print(f"❌ Fatal error connecting to Supabase: {e}")
        return {
            "articles": {"success": 0, "skipped": 0, "errors": len(articles)},
            "enrichments": {"success": 0, "errors": 0}
        }

def load_data_from_tmp() -> tuple:
    """Load articles and enrichments from .tmp directory for testing"""
    tmp_dir = Path(__file__).parent.parent / ".tmp"
    articles = []
    enrichments_map = {}
    
    # Load Ben's Bites articles
    bensbites_file = tmp_dir / "bensbites_articles.json"
    if bensbites_file.exists():
        with open(bensbites_file) as f:
            data = json.load(f)
            if isinstance(data, list):
                articles.extend(data)
            elif isinstance(data, dict):
                articles.extend(data.get("articles", []))
                enrichments_map.update(data.get("enrichments", {}))
    
    # Load Rundown articles (now with enrichments)
    rundown_file = tmp_dir / "rundown_articles.json"
    if rundown_file.exists():
        with open(rundown_file) as f:
            data = json.load(f)
            if isinstance(data, list):
                articles.extend(data)
            elif isinstance(data, dict):
                articles.extend(data.get("articles", []))
                enrichments_map.update(data.get("enrichments", {}))
    
    return articles, enrichments_map

if __name__ == "__main__":
    # Test mode: load from .tmp and save
    articles, enrichments_map = load_data_from_tmp()
    
    if not articles:
        print("⚠️  No articles found in .tmp directory")
        print("💡 Run scrapers first:")
        print("   python tools/scrape_bensbites.py")
        print("   python tools/scrape_rundown.py")
    else:
        stats = save_articles_with_enrichments(articles, enrichments_map)
