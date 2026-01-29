# 🤖 Modal Deployment Guide

This guide will help you deploy the AI News Scraper to run automatically every 24 hours using Modal.

## 📋 Prerequisites

- Modal account (sign up at [modal.com](https://modal.com))
- Modal CLI installed and authenticated (already done! ✅)
- Supabase credentials

## 🚀 Setup Steps

### 1. Create Modal Secret for Supabase

You need to add your Supabase credentials as a Modal secret:

```bash
# Create the secret in Modal
modal secret create supabase-credentials \
  SUPABASE_URL=https://hqxxapqukrzawrvdlwmu.supabase.co \
  SUPABASE_ANON_KEY=your_anon_key_here \
  SUPABASE_SERVICE_KEY=your_service_key_here
```

**Important:** Replace the values with your actual Supabase credentials from your `.env` file.

### 2. Deploy the Scraper

Deploy the Modal app to run on a schedule:

```bash
# Deploy the app
modal deploy modal_scraper.py
```

This will:
- ✅ Deploy your scraper to Modal's cloud
- ✅ Set up a cron schedule to run daily at midnight UTC
- ✅ Make it available for manual triggers

### 3. Test the Deployment

Before relying on the schedule, test it manually:

```bash
# Run the scraper manually
modal run modal_scraper.py
```

This will execute the scraper immediately and show you the results.

## 📅 Schedule Details

The scraper is configured to run:
- **Frequency:** Every 24 hours
- **Time:** Midnight UTC (00:00)
- **Cron Expression:** `0 0 * * *`

To change the schedule, edit the `schedule` parameter in `modal_scraper.py`:

```python
schedule=modal.Cron("0 0 * * *"),  # Midnight UTC
# Examples:
# "0 */12 * * *"  # Every 12 hours
# "0 6 * * *"     # 6 AM UTC daily
# "0 0 * * 1"     # Every Monday at midnight
```

## 🔍 Monitoring

### View Logs

```bash
# View recent logs
modal app logs ai-news-scraper

# Follow logs in real-time
modal app logs ai-news-scraper --follow
```

### Check App Status

```bash
# List all your Modal apps
modal app list

# Get details about the scraper app
modal app show ai-news-scraper
```

### Manual Trigger

You can manually trigger the scraper anytime:

```bash
modal run modal_scraper.py::run_scrapers_manual
```

## 💰 Cost Estimate

Modal pricing (as of 2024):
- **Free tier:** 30 credits/month (plenty for this use case)
- **Estimated usage:** ~0.1 credits per run
- **Monthly cost:** FREE (well within free tier)

Each scraper run takes ~30-60 seconds, so you'll use minimal resources.

## 🛠️ Troubleshooting

### Secret Not Found Error

If you see `Secret "supabase-credentials" not found`:

```bash
# List your secrets
modal secret list

# Create the secret if missing
modal secret create supabase-credentials \
  SUPABASE_URL=your_url \
  SUPABASE_ANON_KEY=your_key \
  SUPABASE_SERVICE_KEY=your_service_key
```

### Import Errors

Make sure all dependencies are listed in the `image.pip_install()` section of `modal_scraper.py`.

### Scraper Failures

Check the logs to see which scraper failed:

```bash
modal app logs ai-news-scraper --follow
```

Common issues:
- Website structure changed (update scraper logic)
- Rate limiting (add delays or retry logic)
- Network timeouts (increase timeout in `@app.function`)

## 🔄 Updating the Scraper

When you make changes to your scraper code:

```bash
# Redeploy with latest changes
modal deploy modal_scraper.py
```

The schedule will continue running with the updated code.

## 🎯 Next Steps

1. ✅ Create Modal secret with Supabase credentials
2. ✅ Deploy the app: `modal deploy modal_scraper.py`
3. ✅ Test manually: `modal run modal_scraper.py`
4. ✅ Monitor logs: `modal app logs ai-news-scraper --follow`
5. ✅ Relax! Your scraper now runs automatically 🎉

## 📚 Resources

- [Modal Documentation](https://modal.com/docs)
- [Modal Cron Schedules](https://modal.com/docs/guide/cron)
- [Modal Secrets](https://modal.com/docs/guide/secrets)
