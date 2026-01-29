# 🎯 Article Enrichments Setup Guide

This guide will help you set up the new **Article Enrichments** feature, which extracts individual news items from within articles (especially useful for The Rundown, which contains multiple news stories per article).

## What's New?

The dashboard now shows:
- **Individual news items** within each article
- **Images** for each news item
- **Titles and summaries** for each piece of news
- **Full content** with expandable "Read More" sections
- **Expandable cards** to show/hide enrichments

## Step 1: Update Database Schema

Run the new enrichment schema in your Supabase SQL Editor:

1. Go to your Supabase dashboard
2. Click "SQL Editor" in the left sidebar
3. Click "New query"
4. Copy the contents of `architecture/enrichment-schema.sql`
5. Paste and click "Run"
6. You should see "Success. No rows returned"

This creates the `article_enrichments` table.

## Step 2: Test the Enhanced Scraper

The Rundown scraper has been enhanced to extract individual news items:

```bash
# Activate your virtual environment
source venv/bin/activate  # or: source .venv/bin/activate

# Run the enhanced scraper
python tools/scrape_rundown.py
```

You should see output like:
```
🔍 Scraping The Rundown AI (with enrichments)...
  📄 Fetching archive page...
  📋 Found 10 article links
  🔗 Fetching article 1/5: https://...
    🔍 Found 6 news items in article
      ✅ Enrichment 1: 🦞 Viral AI agent takes the internet by storm...
      ✅ Enrichment 2: 🔬 OpenAI releases free scientific writing workspace...
      ...
    ✅ Article title... (6 enrichments)
```

## Step 3: Save to Supabase

The save script has also been enhanced to save enrichments:

```bash
python tools/save_to_supabase.py
```

You should see:
```
💾 Saving X articles to Supabase...
  ✅ Saved: Article title...
    🔍 Saving 6 enrichments...
    ✅ Saved 6 enrichments
```

## Step 4: Verify in Supabase

1. Go to Supabase dashboard → Table Editor
2. Click on `article_enrichments` table
3. You should see rows with:
   - `article_id` (links to parent article)
   - `title` (news item title)
   - `summary` (brief description)
   - `image_url` (image for this news item)
   - `content` (full text)
   - `position` (order within article)

## Step 5: View in Dashboard

1. Refresh your dashboard at `http://localhost:8000`
2. Look for articles with a "📰 X News Items" badge
3. Click "Show Details" to expand enrichments
4. Each enrichment shows:
   - Image (if available)
   - Title
   - Summary
   - "Read More" button for full content

## Features

### Expandable Cards
- Articles with enrichments show a count badge
- Click "Show Details" to expand/collapse
- Toggle icon changes (▼/▲)

### Individual News Items
- Each enrichment is displayed in its own card
- Images are shown at full width
- Hover effects for better UX

### Read More
- Click "Read More" to see full content
- Content is formatted with paragraphs
- Click "Read Less" to collapse

## Troubleshooting

### No enrichments showing
- Check if the scraper found any: `cat .tmp/rundown_articles.json`
- Verify the database has enrichments: Check Supabase Table Editor
- Check browser console for errors (F12)

### Enrichments not saving
- Ensure you ran the enrichment schema SQL
- Check that `article_enrichments` table exists
- Verify RLS policies are set correctly

### Images not loading
- Some images may be blocked by CORS
- Images are lazy-loaded for performance
- Check the image URLs in the database

## Running Everything Together

Use the orchestrator to run everything at once:

```bash
python tools/orchestrator.py
```

This will:
1. Scrape Ben's Bites
2. Scrape The Rundown (with enrichments)
3. Save everything to Supabase

## Next Steps

- **Automate**: Set up a cron job to run the orchestrator daily
- **Expand**: Add enrichment extraction for Ben's Bites if needed
- **Enhance**: Add filtering by enrichment keywords
- **Deploy**: Push to production when ready

## Database Schema

The enrichments table structure:

```sql
CREATE TABLE article_enrichments (
  id UUID PRIMARY KEY,
  article_id UUID REFERENCES articles(id),
  title TEXT NOT NULL,
  summary TEXT,
  image_url TEXT,
  content TEXT,
  position INTEGER NOT NULL,
  created_at TIMESTAMPTZ
);
```

## API Changes

The dashboard now fetches:
- Articles (as before)
- Enrichments (new)
- Saved articles (as before)

Enrichments are automatically attached to their parent articles.
