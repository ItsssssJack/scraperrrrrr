# 📜 Project Constitution: AI News Dashboard

**Project Name:** AI News Aggregator Dashboard  
**Created:** 2026-01-28  
**Status:** Protocol 0 - Initialization Phase

---

## 🎯 Project Mission

Build a beautiful, interactive dashboard that aggregates AI news from multiple sources (Ben's Bites, AI Rundown, Reddit), displays articles from the last 24 hours, and allows users to save articles with persistent storage.

---

## 📊 Data Schema

### Input Schema (Raw Scraped Data)
```json
{
  "source": "string (bens_bites | ai_rundown | reddit)",
  "scraped_at": "ISO 8601 timestamp",
  "articles": [
    {
      "title": "string",
      "url": "string",
      "published_date": "ISO 8601 timestamp",
      "summary": "string (optional)",
      "author": "string (optional)",
      "image_url": "string (optional)",
      "tags": ["string"] (optional)
    }
  ]
}
```

### Output Schema (Processed Payload for Dashboard)
```json
{
  "last_updated": "ISO 8601 timestamp",
  "articles": [
    {
      "id": "string (unique identifier)",
      "source": "string",
      "title": "string",
      "url": "string",
      "published_date": "ISO 8601 timestamp",
      "summary": "string",
      "author": "string",
      "image_url": "string",
      "tags": ["string"],
      "is_saved": "boolean",
      "saved_at": "ISO 8601 timestamp (if saved)"
    }
  ],
  "saved_articles": [
    {
      "id": "string",
      "saved_at": "ISO 8601 timestamp",
      "article_data": "object (same as article schema above)"
    }
  ]
}
```

### Database Schema (Supabase)
**Table: `articles`**
- `id` (uuid, primary key)
- `source` (text)
- `title` (text)
- `url` (text, unique)
- `published_date` (timestamp)
- `summary` (text, nullable)
- `author` (text, nullable)
- `image_url` (text, nullable)
- `tags` (text[], nullable)
- `created_at` (timestamp)

**Table: `saved_articles`**
- `id` (uuid, primary key)
- `article_id` (uuid, foreign key → articles.id)
- `saved_at` (timestamp)
- `user_id` (uuid, nullable - for future multi-user support)

---

## 🔧 Behavioral Rules

1. **24-Hour Window:** Only display articles published within the last 24 hours
2. **Deduplication:** If the same article appears from multiple sources, show only once
3. **Persistence:** Saved articles must persist across page refreshes
4. **Graceful Degradation:** If a source fails to scrape, continue with available sources
5. **Visual Excellence:** Dashboard must be gorgeous, interactive, with smooth animations
6. **Performance:** Initial load should be < 3 seconds
7. **Responsiveness:** Must work beautifully on desktop, tablet, and mobile

---

## 🏗️ Architecture Invariants

1. **Separation of Concerns:**
   - Scrapers (`tools/`) are independent, atomic Python scripts
   - Dashboard (frontend) never directly calls scrapers
   - Supabase acts as the single source of truth for the dashboard

2. **Error Handling:**
   - All scrapers must handle network failures gracefully
   - Log all errors to `progress.md`
   - Never crash the entire system if one source fails

3. **Data Flow:**
   ```
   Newsletter Sources → Scrapers (tools/) → .tmp/ → Supabase → Dashboard (UI)
   ```

4. **Execution Trigger:**
   - Manual execution initially
   - Future: Cron job every 24 hours (Phase 5: Trigger)

---

## 🔐 Environment Variables

```bash
# Supabase (to be configured in Phase 2: Link)
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=

# Future: Reddit API (if needed)
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
```

---

## 📝 Maintenance Log

### 2026-01-28 - Project Initialized
- Created project constitution
- Defined data schemas
- Established behavioral rules
- Awaiting Discovery Questions completion

---

## ⚠️ Known Constraints

- Ben's Bites and AI Rundown are newsletters (may require email scraping or web scraping)
- Reddit API has rate limits (60 requests/minute for unauthenticated)
- Supabase integration to be configured in Phase 2
