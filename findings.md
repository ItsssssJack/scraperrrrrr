# 🔍 Findings: AI News Aggregator Dashboard

**Project:** AI News Dashboard  
**Created:** 2026-01-28

---

## 📰 Source Research

### Ben's Bites
**Status:** ✅ Research Complete  
**Type:** Newsletter (Substack)  
**URL:** https://www.bensbites.com

**Key Findings:**
- **Platform:** Hosted on Substack (highly consistent structure)
- **RSS Feed:** ✅ Available at `https://www.bensbites.com/feed` (RECOMMENDED METHOD)
- **Archive Page:** `https://www.bensbites.com/archive`
- **Article Pattern:** `https://www.bensbites.com/p/[article-slug]`

**HTML Selectors:**
- **Archive Page:**
  - Article Container: `div[role="article"]` or `div.post-preview`
  - Title: `a.post-preview-title`
  - Summary: `a.post-preview-description`
  - Date: `time` element (has `datetime` attribute)
  - Link: `href` of title link
- **Individual Article:**
  - Title: `h1.post-title`
  - Subtitle: `h3.subtitle`
  - Date: `time` element
  - Content: `div.body.markup`

**Scraping Strategy:**
- [x] RSS feed found (PRIMARY METHOD)
- [x] HTML structure documented
- [x] Date filtering possible (chronological order)
- **Recommended Approach:** Use RSS feed with `feedparser` library
- **Frequency:** Check every 24 hours
- **Anti-Scraping:** Minimal (standard Substack protections)
- **Paywall:** Some articles may be paywalled (check for lock icon)

---

### The Rundown AI
**Status:** ✅ Research Complete  
**Type:** Newsletter (Custom Site)  
**URL:** https://www.therundown.ai

**Key Findings:**
- **Platform:** Modern Next.js/Vercel site
- **Archive Page:** `https://www.therundown.ai/archive`
- **Article Pattern:** `https://www.therundown.ai/p/[slug]`
- **⚠️ Critical:** Dates NOT shown on archive page (only on individual articles)
- **Pagination:** Infinite scroll (first 12-16 articles pre-rendered)

**HTML Selectors:**
- **Archive Page:**
  - Card Link: `a.embla__slide__number`
  - Title: `h3 strong`
  - Summary: `p span` (often starts with "PLUS: ")
  - Thumbnail: `img` inside `picture`
  - Author: `span` (e.g., "Zach Mink, +4")
  - ⚠️ Date: NOT AVAILABLE (must visit article)
- **Individual Article:**
  - Title: `h1`
  - Date: `span` containing date text (e.g., "Jan 28, 2026")
  - Summary: First `p` or sibling of title
  - Hero Image: `img`

**Scraping Strategy:**
- [x] HTML structure documented
- [x] Two-step approach required
- **Recommended Approach:**
  1. Fetch archive page HTML (first load has ~12-16 articles)
  2. Extract top 3-5 article URLs
  3. Visit each article to get publication date
  4. Filter by 24-hour window
- **Tools:** `requests` + `BeautifulSoup` (no Selenium needed)
- **Anti-Scraping:** Modern stack, use realistic User-Agent
- **Efficiency:** Only scrape top 3-5 articles (daily newsletter = 1 per day)

---

### Reddit
**Status:** ✅ Research Complete  
**Type:** Social Platform  
**URL:** reddit.com

**Key Findings:**
- **Official API:** Available (requires app registration)
- **Rate Limits:** 
  - Unauthenticated: 60 requests/min
  - Authenticated: 600 requests/min
- **Recommended Library:** PRAW (Python Reddit API Wrapper)
- **Target Subreddits:** r/artificial, r/MachineLearning, r/OpenAI, r/LocalLLaMA

**Scraping Strategy:**
- [x] PRAW library identified (best option)
- [x] API approach confirmed
- **Recommended Approach:**
  1. Register Reddit app (get client_id, client_secret)
  2. Use PRAW to fetch `subreddit.new(limit=10)`
  3. Filter posts by timestamp (last 24 hours)
  4. Extract: title, url, author, score, created_utc
- **Installation:** `pip install praw`
- **Rate Limiting:** Built into PRAW
- **Authentication:** Required for reliable access

---

## 🛠️ Technical Discoveries

### Scraping Tools (Python)
- **BeautifulSoup4:** HTML parsing
- **Requests:** HTTP requests
- **Selenium:** For JavaScript-heavy sites (if needed)
- **PRAW:** Reddit API wrapper
- **Feedparser:** For RSS feeds (if available)

### Anti-Scraping Considerations
- **Rate Limiting:** Implement delays between requests
- **User-Agent Rotation:** Mimic real browsers
- **Robots.txt Compliance:** Check each site's robots.txt
- **CAPTCHA:** May need to handle or avoid

---

## 🗄️ Database Considerations

### Supabase Setup
- **Free Tier Limits:**
  - 500 MB database space
  - 2 GB bandwidth
  - 50 MB file storage
  - Sufficient for this project

- **Required Tables:**
  - `articles` (main article storage)
  - `saved_articles` (user-saved articles)

- **Indexes Needed:**
  - `published_date` (for 24-hour filtering)
  - `url` (for deduplication)
  - `source` (for filtering by source)

---

## 🎨 Design Inspiration

### Dashboard Design Goals
- **Color Palette:** Dark mode with vibrant accents (purple, cyan, orange)
- **Typography:** Inter or Outfit (Google Fonts)
- **Layout:** Card-based grid layout
- **Animations:** Smooth hover effects, fade-ins, skeleton loaders
- **Components:**
  - Article cards with image, title, summary, source badge
  - Filter bar (by source, by date)
  - Save button with heart icon animation
  - Refresh indicator

---

## ⚠️ Constraints & Risks

### Identified Constraints
1. **Newsletter Access:** Ben's Bites and AI Rundown may not have public archives
2. **Rate Limits:** Need to respect each source's rate limits
3. **Data Freshness:** 24-hour window may miss articles if scraper runs at wrong time
4. **Supabase Free Tier:** Limited storage (500 MB)

### Mitigation Strategies
1. **Newsletter Access:** Start with web scraping, fall back to RSS if available
2. **Rate Limits:** Implement exponential backoff and delays
3. **Data Freshness:** Run scraper multiple times per day (e.g., every 6 hours)
4. **Storage:** Implement data retention policy (delete articles older than 7 days)

---

## 📝 Research Tasks (Next Steps)

- [ ] Visit Ben's Bites website and inspect structure
- [ ] Visit AI Rundown website and inspect structure
- [ ] Test Reddit API access
- [ ] Check for RSS feeds
- [ ] Test scraping a single article from each source
- [ ] Document HTML selectors for each source
- [ ] Update this file with findings
