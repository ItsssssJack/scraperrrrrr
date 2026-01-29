# 📋 Task Plan: AI News Aggregator Dashboard

**Project:** AI News Dashboard  
**Created:** 2026-01-28  
**Current Phase:** Protocol 0 - Initialization

---

## 🎯 Project Phases

### ✅ Phase 0: Protocol Initialization
- [x] Create `gemini.md` (Project Constitution)
- [x] Create `task_plan.md` (This file)
- [x] Create `findings.md` (Research log)
- [x] Create `progress.md` (Execution log)
- [ ] Complete Discovery Questions
- [ ] Research scraping methods for each source
- [ ] Define final Data Schema
- [ ] Get Blueprint approval

---

### 📦 Phase 1: B - Blueprint (Vision & Logic)

#### 1.1 Discovery Questions
- [ ] **North Star:** Confirmed - Beautiful dashboard showing latest AI news with save functionality
- [ ] **Integrations:** 
  - Ben's Bites (web scraping)
  - AI Rundown (web scraping)
  - Reddit (API or web scraping)
  - Supabase (database - keys needed)
- [ ] **Source of Truth:** Supabase database
- [ ] **Delivery Payload:** Web dashboard (HTML/CSS/JS), refreshes every 24 hours
- [ ] **Behavioral Rules:** Defined in `gemini.md`

#### 1.2 Research & Validation
- [ ] Research Ben's Bites scraping method (website structure)
- [ ] Research AI Rundown scraping method (website structure)
- [ ] Research Reddit scraping method (API vs web scraping)
- [ ] Identify anti-scraping measures (rate limits, CAPTCHAs, etc.)
- [ ] Document findings in `findings.md`

#### 1.3 Data Schema Finalization
- [ ] Validate Input Schema with actual scraped data
- [ ] Validate Output Schema with dashboard requirements
- [ ] Validate Database Schema with Supabase best practices
- [ ] Update `gemini.md` with final schemas

---

### ⚡ Phase 2: L - Link (Connectivity)

#### 2.1 Environment Setup
- [ ] Create `.env` file with placeholder keys
- [ ] Set up Supabase project
- [ ] Get Supabase URL and keys
- [ ] Test Supabase connection

#### 2.2 API/Service Verification
- [ ] Test Ben's Bites website accessibility
- [ ] Test AI Rundown website accessibility
- [ ] Test Reddit accessibility (API or web)
- [ ] Build minimal handshake scripts in `tools/`
- [ ] Verify all connections work

---

### ⚙️ Phase 3: A - Architect (3-Layer Build)

#### 3.1 Layer 1: Architecture (SOPs)
- [ ] Create `architecture/scraping-sop.md` (How to scrape each source)
- [ ] Create `architecture/database-sop.md` (How to interact with Supabase)
- [ ] Create `architecture/dashboard-sop.md` (How the UI should behave)

#### 3.2 Layer 3: Tools (Python Scripts)
- [ ] Build `tools/scrape_bens_bites.py`
- [ ] Build `tools/scrape_ai_rundown.py`
- [ ] Build `tools/scrape_reddit.py`
- [ ] Build `tools/save_to_supabase.py`
- [ ] Build `tools/orchestrator.py` (runs all scrapers)
- [ ] Test each tool independently

#### 3.3 Layer 2: Navigation (Dashboard)
- [ ] Design dashboard wireframe
- [ ] Build HTML structure
- [ ] Build CSS with gorgeous, interactive design
- [ ] Build JavaScript for:
  - Fetching data from Supabase
  - Displaying articles
  - Saving articles
  - Filtering by source/date
  - Smooth animations and interactions

---

### ✨ Phase 4: S - Stylize (Refinement & UI)

#### 4.1 Visual Excellence
- [ ] Implement modern color palette (vibrant, dark mode support)
- [ ] Add smooth animations (hover effects, transitions)
- [ ] Use premium typography (Google Fonts)
- [ ] Add glassmorphism/gradient effects
- [ ] Ensure responsive design (mobile, tablet, desktop)

#### 4.2 UX Refinement
- [ ] Add loading states
- [ ] Add error states (if scraping fails)
- [ ] Add empty states (no new articles)
- [ ] Add success feedback (article saved)
- [ ] Test user flow end-to-end

#### 4.3 User Feedback
- [ ] Present dashboard to user
- [ ] Gather feedback
- [ ] Implement requested changes

---

### 🛰️ Phase 5: T - Trigger (Deployment)

#### 5.1 Automation Setup
- [ ] Set up cron job for 24-hour scraping
- [ ] OR set up webhook trigger
- [ ] OR set up Supabase Edge Function

#### 5.2 Cloud Deployment
- [ ] Deploy dashboard to hosting (Vercel/Netlify)
- [ ] Deploy scrapers to cloud (AWS Lambda/Google Cloud Functions)
- [ ] Test end-to-end in production

#### 5.3 Documentation
- [ ] Finalize `gemini.md` maintenance log
- [ ] Create user guide (how to use dashboard)
- [ ] Create developer guide (how to maintain/extend)

---

## 🚨 Current Blockers

1. **Supabase Credentials:** Need to set up Supabase project and get keys
2. **Scraping Research:** Need to research actual website structures for Ben's Bites and AI Rundown
3. **Blueprint Approval:** Need user confirmation on Discovery Questions

---

## 📊 Success Criteria

- [ ] Dashboard loads in < 3 seconds
- [ ] Articles from all 3 sources are displayed
- [ ] Only articles from last 24 hours are shown
- [ ] Saved articles persist across refreshes
- [ ] Design is gorgeous and interactive
- [ ] System runs automatically every 24 hours
- [ ] No crashes if one source fails
