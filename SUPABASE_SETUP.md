# 🚀 Supabase Setup Guide

Follow these steps to set up your Supabase database for the AI News Dashboard.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub (or create an account)
4. Click "New Project"
5. Fill in the details:
   - **Name:** AI News Dashboard
   - **Database Password:** (create a strong password - save it!)
   - **Region:** Choose closest to you
   - **Pricing Plan:** Free
6. Click "Create new project"
7. Wait 2-3 minutes for the project to initialize

## Step 2: Run the Database Migration

1. In your Supabase dashboard, click "SQL Editor" in the left sidebar
2. Click "New query"
3. Copy the entire contents of `architecture/database-schema.sql`
4. Paste into the SQL editor
5. Click "Run" (or press Cmd/Ctrl + Enter)
6. You should see "Success. No rows returned"

## Step 3: Get Your API Credentials

1. Click "Project Settings" (gear icon) in the left sidebar
2. Click "API" in the settings menu
3. You'll see two important values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon public** key (long string starting with `eyJ...`)
   - **service_role** key (another long string - keep this secret!)

## Step 4: Configure Your Environment

1. In your project folder, copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and fill in your credentials:
   ```bash
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_ANON_KEY=eyJhbGc...your_anon_key
   SUPABASE_SERVICE_KEY=eyJhbGc...your_service_key
   ```

3. Save the file

## Step 5: Verify the Setup

1. In Supabase dashboard, click "Table Editor"
2. You should see two tables:
   - `articles`
   - `saved_articles`
3. Both should be empty (0 rows)

## Step 6: Test the Scrapers

1. Activate your Python virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Test Ben's Bites scraper:
   ```bash
   python tools/scrape_bensbites.py
   ```

4. Test The Rundown scraper:
   ```bash
   python tools/scrape_rundown.py
   ```

5. Save articles to Supabase:
   ```bash
   python tools/save_to_supabase.py
   ```

6. Or run everything at once:
   ```bash
   python tools/orchestrator.py
   ```

## Step 7: Open the Dashboard

1. Start a local web server:
   ```bash
   python -m http.server 8000
   ```

2. Open your browser to: `http://localhost:8000`

3. When prompted, enter your Supabase credentials:
   - **URL:** Your project URL from Step 3
   - **Anon Key:** Your anon public key from Step 3

4. You should see your articles!

## Troubleshooting

### "No articles found"
- Make sure you ran the scrapers first
- Check that articles were saved to Supabase (check Table Editor)
- Verify your `.env` file has correct credentials

### "Failed to connect to database"
- Double-check your Supabase URL and anon key
- Make sure you're using the **anon public** key (not service_role) in the dashboard
- Clear localStorage and re-enter credentials

### Scrapers failing
- Check your internet connection
- Websites may have changed structure (check `findings.md`)
- Try running scrapers individually to isolate the issue

## Next Steps

Once everything is working:

1. **Set up automation:** Create a cron job to run `orchestrator.py` every 24 hours
2. **Deploy dashboard:** Host on Vercel, Netlify, or GitHub Pages
3. **Add Reddit:** Follow Phase 2 instructions to add Reddit integration

## Support

If you encounter issues:
1. Check the Supabase logs (Dashboard → Logs)
2. Check browser console for errors (F12 → Console)
3. Review `progress.md` for debugging info
