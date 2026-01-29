#!/usr/bin/env python3
"""
The Rundown AI Scraper - Enhanced with Article Enrichment
Scrapes latest AI news from The Rundown AI archive
Extracts individual news items from within each article
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
import re

def extract_enrichments(article_soup):
    """
    Extract individual news items from within a Rundown article
    
    Args:
        article_soup: BeautifulSoup object of the article page
        
    Returns:
        list: Array of enrichment dictionaries
    """
    enrichments = []
    
    # Find all h4 headers with the specific classes (news item titles)
    headers = article_soup.select("h4.hynlcx1.hynlcx5")
    
    print(f"    🔍 Found {len(headers)} news items in article")
    
    for idx, header in enumerate(headers):
        try:
            enrichment = {
                "title": header.get_text(strip=True),
                "summary": "",
                "image_url": None,
                "content": "",
                "position": idx
            }
            
            # Collect content following the header
            content_parts = []
            current = header.parent.next_sibling
            
            # Traverse siblings until we hit another h4 or run out of content
            while current and len(content_parts) < 20:  # Safety limit
                if isinstance(current, str):
                    current = current.next_sibling
                    continue
                    
                # Stop if we hit another news item header
                if current.name == 'h4' or (current.find('h4', class_='hynlcx1') if hasattr(current, 'find') else False):
                    break
                
                # Extract images
                if not enrichment["image_url"]:
                    img = current.find('img') if hasattr(current, 'find') else None
                    if img and img.get('src'):
                        enrichment["image_url"] = img.get('src')
                
                # Extract text content
                text = current.get_text(strip=True) if hasattr(current, 'get_text') else ""
                if text and len(text) > 10:
                    content_parts.append(text)
                
                current = current.next_sibling
            
            # Join content and extract summary
            full_content = "\n\n".join(content_parts)
            enrichment["content"] = full_content
            
            # Extract summary (usually the first "The Rundown:" section)
            rundown_match = re.search(r'The Rundown:\s*(.+?)(?:The details:|Why it matters:|$)', full_content, re.DOTALL | re.IGNORECASE)
            if rundown_match:
                enrichment["summary"] = rundown_match.group(1).strip()[:500]  # Limit to 500 chars
            elif content_parts:
                # Fallback to first paragraph
                enrichment["summary"] = content_parts[0][:500]
            
            enrichments.append(enrichment)
            print(f"      ✅ Enrichment {idx + 1}: {enrichment['title'][:50]}...")
            
        except Exception as e:
            print(f"      ⚠️  Error extracting enrichment {idx}: {e}")
            continue
    
    return enrichments


def scrape_rundown():
    """
    Scrape The Rundown AI for articles from the last 24 hours
    Now includes enrichments (individual news items within each article)
    
    Returns:
        dict: {
            "articles": Array of article dictionaries,
            "enrichments": Dict mapping article URLs to their enrichments
        }
    """
    print("🔍 Scraping The Rundown AI (with enrichments)...")
    
    ARCHIVE_URL = "https://www.therundown.ai/archive"
    BASE_URL = "https://www.therundown.ai"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    articles = []
    enrichments_map = {}
    
    try:
        # Step 1: Fetch archive page
        print("  📄 Fetching archive page...")
        response = requests.get(ARCHIVE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find article links
        article_links = soup.select("a.embla__slide__number")
        
        if not article_links:
            print("  ⚠️  No article links found. HTML structure may have changed.")
            return {"articles": [], "enrichments": {}}
        
        print(f"  📋 Found {len(article_links)} article links")
        
        # Calculate 24-hour cutoff
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        
        # Step 2: Fetch individual articles (limit to top 5 for efficiency)
        for i, link in enumerate(article_links[:5]):
            try:
                article_url = link.get("href")
                if not article_url.startswith("http"):
                    article_url = BASE_URL + article_url
                
                print(f"  🔗 Fetching article {i+1}/5: {article_url}")
                
                # Fetch article page
                time.sleep(0.5)  # Be polite, avoid rate limiting
                article_response = requests.get(article_url, headers=headers, timeout=10)
                article_response.raise_for_status()
                
                article_soup = BeautifulSoup(article_response.content, "html.parser")
                
                # Extract title
                title_elem = article_soup.select_one("h1")
                title = title_elem.get_text(strip=True) if title_elem else "No title"
                
                # Extract date (look for date patterns)
                date_text = None
                date_spans = article_soup.find_all("span")
                for span in date_spans:
                    text = span.get_text(strip=True)
                    # Look for date pattern like "Jan 28, 2026"
                    if re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}", text):
                        date_text = text
                        break
                
                if not date_text:
                    print(f"    ⚠️  No date found, skipping")
                    continue
                
                # Parse date
                try:
                    pub_date = datetime.strptime(date_text, "%b %d, %Y")
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                except ValueError:
                    print(f"    ⚠️  Could not parse date: {date_text}")
                    continue
                
                # Check if within 24 hours
                if pub_date < cutoff_time:
                    print(f"    ⏭️  Article too old ({date_text}), stopping")
                    break
                
                # Extract summary (first paragraph or subtitle)
                summary = ""
                summary_elem = article_soup.select_one("h3") or article_soup.select_one("p")
                if summary_elem:
                    summary = summary_elem.get_text(strip=True)
                
                # Extract image
                image_url = None
                img_elem = article_soup.select_one("img")
                if img_elem:
                    image_url = img_elem.get("src")
                    if image_url and not image_url.startswith("http"):
                        image_url = BASE_URL + image_url
                
                # Extract author
                author = "Rowan Cheung"  # Default author for The Rundown
                
                # Extract enrichments (individual news items)
                enrichments = extract_enrichments(article_soup)
                enrichments_map[article_url] = enrichments
                
                article = {
                    "source": "rundown",
                    "title": title,
                    "url": article_url,
                    "published_date": pub_date.isoformat(),
                    "summary": summary,
                    "author": author,
                    "image_url": image_url,
                    "tags": ["AI", "News"],
                    "enrichment_count": len(enrichments)
                }
                
                articles.append(article)
                print(f"    ✅ {title[:60]}... ({len(enrichments)} enrichments)")
                
            except Exception as e:
                print(f"    ⚠️  Error processing article: {e}")
                continue
        
        print(f"✅ Found {len(articles)} articles from The Rundown AI (last 24h)")
        
        # Save to .tmp for debugging
        tmp_dir = Path(__file__).parent.parent / ".tmp"
        tmp_dir.mkdir(exist_ok=True)
        
        output = {
            "articles": articles,
            "enrichments": enrichments_map
        }
        
        with open(tmp_dir / "rundown_articles.json", "w") as f:
            json.dump(output, f, indent=2)
        
        return output
        
    except Exception as e:
        print(f"❌ Error scraping The Rundown AI: {e}")
        return {"articles": [], "enrichments": {}}

if __name__ == "__main__":
    result = scrape_rundown()
    articles = result["articles"]
    enrichments = result["enrichments"]
    
    print(f"\n📊 Total articles: {len(articles)}")
    print(f"📊 Total enrichments: {sum(len(e) for e in enrichments.values())}")
    
    if articles:
        print("\n📰 Sample article:")
        print(json.dumps(articles[0], indent=2))
        
        if enrichments.get(articles[0]["url"]):
            print("\n🔍 Sample enrichments:")
            print(json.dumps(enrichments[articles[0]["url"]][:2], indent=2))
