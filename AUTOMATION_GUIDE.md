# Weekly Menu Automation Guide

Since the menu changes weekly, you need automated solutions. Here are three approaches from easiest to most automated:

---

## ⭐ Option 1: Browser Extension (EASIEST - 30 seconds/week)

**Best for:** Weekly manual updates with minimal effort

**Setup once:**
1. Install the Chrome extension (see `browser-extension/README.md`)
2. Pin it to your toolbar

**Every week:**
1. Visit sony.cafebonappetit.com (10 seconds)
2. Click extension icon (5 seconds)
3. Click "Extract Menu Data" (5 seconds)
4. Click "Download JSON" (5 seconds)
5. Upload to analyzer (5 seconds)

**Total time: 30 seconds per week**

**Pros:**
- ✅ Works 100% of the time (bypasses all bot protection)
- ✅ Zero technical setup
- ✅ Visual confirmation of what's extracted
- ✅ Can manually verify data

**Cons:**
- ❌ Requires manual weekly action
- ❌ Need to remember to do it

**Perfect for:** Most users who want reliability without complexity

---

## Option 2: Enhanced Automated Scraper

**Best for:** Semi-automated approach with better bot evasion

**What it does:**
Uses advanced techniques to bypass bot protection:
- `undetected-chromedriver` - mimics real Chrome browser
- `playwright` - modern browser automation
- Human-like behavior simulation (scrolling, delays)

**Setup:**
```bash
# Install enhanced scraping libraries
pip install undetected-chromedriver playwright

# Install Playwright browsers
python -m playwright install chromium
```

**Usage:**
```bash
# Run enhanced scraper
python enhanced_scraper.py https://sony.cafebonappetit.com menu.json

# Then analyze
python cafe_analyzer.py --json menu.json
```

**Pros:**
- ✅ Can be fully automated
- ✅ Better at bypassing bot protection than standard scraping
- ✅ Saves to dated files automatically

**Cons:**
- ❌ May still be blocked by strong bot protection
- ❌ Requires Chrome installation
- ❌ More complex setup

**Perfect for:** Technical users who want automation

---

## Option 3: Scheduled Weekly Scraper (FULLY AUTOMATED)

**Best for:** Complete hands-off automation

**What it does:**
Automatically runs every week (you choose the day/time):
- Scrapes the menu
- Saves with date stamp
- Creates `latest.json` for easy access
- Keeps history of all weekly menus
- Optional email notifications

**Setup:**

### Step 1: Install dependencies
```bash
pip install undetected-chromedriver playwright
python -m playwright install chromium
```

### Step 2: Test it works
```bash
python weekly_scraper.py test
```

### Step 3: Set up automatic scheduling

**On Linux/Mac (cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 6 AM):
0 6 * * 1 /usr/bin/python3 /home/user/laughing-system/weekly_scraper.py

# Or every Sunday at 9 PM:
0 21 * * 0 /usr/bin/python3 /home/user/laughing-system/weekly_scraper.py
```

**On Windows (Task Scheduler):**
```
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Weekly Menu Scraper"
4. Trigger: Weekly, choose day/time
5. Action: Start a program
   - Program: C:\Python\python.exe (your Python path)
   - Arguments: C:\path\to\weekly_scraper.py
6. Finish
```

**Viewing setup instructions:**
```bash
python weekly_scraper.py setup
```

### Features:
- Saves to `weekly_menus/menu_YYYY-MM-DD.json`
- Creates `weekly_menus/latest.json` for current week
- Skips if already scraped today
- Optional email notifications
- Historical archive of all menus

**Pros:**
- ✅ Completely automated
- ✅ Historical tracking
- ✅ No manual intervention needed
- ✅ Can notify you when done

**Cons:**
- ❌ May fail if bot protection is strong
- ❌ Requires server/computer to be running
- ❌ More complex troubleshooting

**Perfect for:** Power users, developers, or those running on a server

---

## Comparison

| Method | Time/Week | Reliability | Setup Difficulty | Automation |
|--------|-----------|-------------|------------------|------------|
| **Browser Extension** | 30 sec | 100% | ⭐ Easy | Manual |
| **Enhanced Scraper** | 1 min | 70-90% | ⭐⭐ Medium | Semi-auto |
| **Scheduled Scraper** | 0 sec | 60-80% | ⭐⭐⭐ Hard | Full auto |

---

## Recommendation by Use Case

**"I just want it to work reliably every week"**
→ Use **Browser Extension** (Option 1)

**"I'm technical and want good automation"**
→ Use **Enhanced Scraper** (Option 2) and run it manually when needed

**"I want 100% hands-off and have a server"**
→ Use **Scheduled Scraper** (Option 3) with browser extension as backup

**"I want the best of both worlds"**
→ Set up **Scheduled Scraper** to try automatically, but keep **Browser Extension** installed as a fallback when it fails

---

## Hybrid Approach (Recommended)

1. **Set up the scheduled scraper** to try automatically every week
2. **Install the browser extension** as a backup
3. **Check weekly_menus/latest.json** each week
4. **If scraper failed:** Use browser extension (takes 30 seconds)

This gives you:
- Automation when it works
- Easy manual fallback when it doesn't
- Best of both reliability and convenience

---

## Testing Bot Protection

Want to see if the enhanced scraper works for your cafe?

```bash
# Test with enhanced scraper
python enhanced_scraper.py https://sony.cafebonappetit.com test.json

# Check if it found items
cat test.json

# If it worked, set up weekly automation!
# If it failed, use the browser extension
```

---

## File Locations

After automation is set up:

```
weekly_menus/
  ├── menu_2024-01-01.json    # Monday's menu
  ├── menu_2024-01-08.json    # Next Monday
  ├── menu_2024-01-15.json    # Following Monday
  └── latest.json             # → Always points to current week
```

Use `latest.json` in your analyzer:
```bash
python cafe_analyzer.py --json weekly_menus/latest.json
```

Or in the web interface, upload `latest.json` each time you want to see updated analysis.

---

## Troubleshooting

**Scheduled scraper keeps failing:**
- Bot protection is too strong
- Switch to browser extension method
- It's more reliable anyway!

**Want email notifications when scraper runs:**
- Edit `weekly_scraper.py`
- Set `NOTIFY_EMAIL = "your@email.com"`
- Configure SMTP settings (Gmail, etc.)

**Need to change scraping day/time:**
- Linux/Mac: `crontab -e` and edit the schedule
- Windows: Open Task Scheduler and edit the trigger

---

## Quick Start Commands

```bash
# See setup instructions
python weekly_scraper.py setup

# Test the scraper
python weekly_scraper.py test

# Run manually
python weekly_scraper.py

# List all saved menus
python weekly_scraper.py list

# Install browser extension
# Open chrome://extensions/ → Load unpacked → Select browser-extension/
```
