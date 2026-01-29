#!/usr/bin/env python3
"""
Upload generated images to Supabase Storage and update articles
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# Image mappings
image_updates = {
    "OpenAI's new reasoning model breaks benchmarks": {
        "local_path": "/Users/jackroberts/.gemini/antigravity/brain/07677992-b143-44c9-90a6-7efc9b950e83/bensbites_openai_reasoning_1769628862641.png",
        "storage_path": "article-images/bensbites-openai-reasoning.png"
    },
    "Skills are taking over": {
        "local_path": "/Users/jackroberts/.gemini/antigravity/brain/07677992-b143-44c9-90a6-7efc9b950e83/bensbites_skills_ai_1769628891200.png",
        "storage_path": "article-images/bensbites-skills-ai.png"
    }
}

print("📤 Uploading images to Supabase Storage...")

for title, paths in image_updates.items():
    try:
        local_path = paths["local_path"]
        storage_path = paths["storage_path"]
        
        # Read the image file
        with open(local_path, 'rb') as f:
            image_data = f.read()
        
        # Upload to Supabase Storage
        print(f"  📤 Uploading {title}...")
        result = supabase.storage.from_('article-images').upload(
            storage_path,
            image_data,
            file_options={"content-type": "image/png", "upsert": "true"}
        )
        
        # Get public URL
        public_url = supabase.storage.from_('article-images').get_public_url(storage_path)
        
        # Update article with image URL
        update_result = supabase.table('articles').update({
            'image_url': public_url
        }).eq('title', title).eq('source', 'bensbites').execute()
        
        print(f"  ✅ Updated: {title}")
        print(f"     URL: {public_url}")
        
    except Exception as e:
        print(f"  ❌ Error with {title}: {e}")

print("\n✅ Upload complete!")
