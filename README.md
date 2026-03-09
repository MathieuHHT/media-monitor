# 📰 Media Monitor — Coconut Industry Coverage Tracker

Automated media monitoring dashboard that tracks Thai news coverage of the coconut industry, Harmless Harvest Thailand, the Department of Business Development, and key people involved.

**Features:**
- 🔄 Automated twice-daily scanning (6 AM and 6 PM Bangkok time)
- 🌐 Translates Thai articles to English using Claude API
- 👥 Tracks mentions of specific people and companies
- 📊 Filterable dashboard with search, priority outlet highlighting
- 🆓 Free hosting via GitHub Pages + GitHub Actions

---

## 🚀 Setup Guide (Step by Step)

### Step 1: Create a GitHub Account
1. Go to [github.com](https://github.com) and click **Sign up**
2. Follow the registration steps
3. Verify your email address

### Step 2: Create the Repository
1. After logging in, click the **+** icon (top-right) → **New repository**
2. Settings:
   - **Repository name**: `media-monitor` (or whatever you like)
   - **Visibility**: Set to **Public** (required for free GitHub Pages)
   - Check ✅ **Add a README file**
3. Click **Create repository**

### Step 3: Upload the Project Files
1. In your new repo, click **Add file** → **Upload files**
2. Drag and drop ALL the files from this project:
   ```
   .github/workflows/scan.yml
   scripts/config.py
   scripts/scraper.py
   docs/index.html
   docs/data.json
   requirements.txt
   ```
   **Important**: You need to preserve the folder structure. The easiest way:
   - First upload files in the root: `requirements.txt`
   - Then create the folders by clicking **Add file** → **Create new file**
   - Type the full path like `scripts/config.py` and paste the content
   - Repeat for each file

   **Alternative (faster)**: Use the GitHub CLI or git from your terminal:
   ```bash
   git clone https://github.com/YOUR_USERNAME/media-monitor.git
   # Copy all project files into the cloned folder
   cd media-monitor
   git add -A
   git commit -m "Initial setup"
   git push
   ```

### Step 4: Add Your Anthropic API Key
1. Go to your repo → **Settings** tab → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))
5. Click **Add secret**

> 💡 The API cost is very low — each scan uses about $0.02-0.05 of Claude Sonnet credits for translation.

### Step 5: Enable GitHub Pages
1. Go to your repo → **Settings** tab → **Pages** (in the left sidebar)
2. Under **Source**, select:
   - **Branch**: `main`
   - **Folder**: `/docs`
3. Click **Save**
4. Wait 1-2 minutes, then your dashboard will be live at:
   ```
   https://YOUR_USERNAME.github.io/media-monitor/
   ```

### Step 6: Run the First Scan
1. Go to your repo → **Actions** tab
2. Click **Media Monitor Scan** in the left sidebar
3. Click **Run workflow** → **Run workflow**
4. Wait 1-2 minutes for it to complete
5. Refresh your dashboard page — articles should now appear!

### Step 7: Share the Link
Share the GitHub Pages URL with your team:
```
https://YOUR_USERNAME.github.io/media-monitor/
```
Anyone with the link can view the dashboard. No login required.

---

## 🔧 Customization

### Add/Remove Search Keywords
Edit `scripts/config.py` → `SEARCH_QUERIES` list to change what the scraper looks for.

### Add/Remove People
Edit `scripts/config.py` → `PEOPLE` dictionary. Make sure to include both Thai and English name variants in `search_terms`.

Also update the `PEOPLE_MAP` in `docs/index.html` so the dashboard shows the new people as filter pills.

### Change Scan Schedule
Edit `.github/workflows/scan.yml` → `cron` lines. Uses UTC time (Bangkok = UTC+7).

### Manual Scan
You can trigger a scan anytime from the **Actions** tab → **Run workflow**.

---

## 📂 Project Structure

```
media-monitor/
├── .github/workflows/
│   └── scan.yml              # GitHub Actions cron job
├── scripts/
│   ├── config.py             # Keywords, people, outlets config
│   └── scraper.py            # Google News RSS scraper + Claude translator
├── docs/
│   ├── index.html            # Dashboard (GitHub Pages)
│   └── data.json             # Article data (auto-updated by scraper)
├── requirements.txt
└── README.md
```

---

## ⚠️ Notes

- **Google News RSS** is the data source — it covers most major Thai outlets but may miss some smaller ones
- **Translation quality** depends on the Claude API; articles are summarized in 1-2 sentences
- **GitHub Actions free tier** gives you 2,000 minutes/month — this project uses about 2-3 min/day, well within limits
- The dashboard **auto-refreshes** every 5 minutes when open in a browser
- Data is stored in `docs/data.json` and keeps the last 500 articles
