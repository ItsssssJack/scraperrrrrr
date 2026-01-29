# 🚀 AI News Aggregator Dashboard

A beautiful, interactive dashboard that aggregates the latest AI news from **The Rundown AI** and **Ben's Bites**, with the ability to save articles that persist across refreshes.

## ✨ Features

- 📰 Aggregates AI news from multiple sources
- ⏰ Shows only articles from the last 24 hours
- 💾 Save articles with persistent storage (Supabase)
- 🎨 Gorgeous design using Glaido brand guidelines
- 🔄 Automatic refresh every 24 hours
- 📱 Responsive design (mobile, tablet, desktop)

## 🛠️ Tech Stack

- **Backend:** Python (scrapers)
- **Database:** Supabase (PostgreSQL)
- **Frontend:** HTML, CSS, JavaScript
- **Design:** Glassmorphism, neon green accents, Inter typography

## 📋 Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Supabase

1. Go to [supabase.com](https://supabase.com)
2. Create a new project (free tier)
3. Copy your project URL and API keys
4. Run the SQL migrations in `architecture/database-schema.sql`

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and add your Supabase credentials
```

### 4. Run Scrapers

```bash
# Test individual scrapers
python tools/scrape_bensbites.py
python tools/scrape_rundown.py

# Run all scrapers
python tools/orchestrator.py
```

### 5. Open Dashboard

```bash
# Serve locally
python -m http.server 8000

# Open in browser
open http://localhost:8000
```

## 📁 Project Structure

```
Scraperrrr/
├── tools/              # Python scrapers
├── architecture/       # SOPs and documentation
├── .tmp/              # Temporary scraping data
├── index.html         # Dashboard
├── styles.css         # Glaido-branded styling
├── app.js             # Dashboard interactivity
└── gemini.md          # Project constitution
```

## 🎨 Design Guidelines

- **Primary Color:** #BFF549 (neon green)
- **Background:** #000000 (black)
- **Accent:** #99A1AF (gray)
- **Typography:** Inter font family
- **Effects:** Glassmorphism, smooth animations

## 📝 License

MIT
