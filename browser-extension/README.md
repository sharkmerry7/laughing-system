# Cafe Menu Scraper Browser Extension

A Chrome extension to extract menu data from Cafe Bon Appetit websites with one click - **bypasses bot protection** since it runs in your actual browser!

## Installation

1. **Open Chrome** and navigate to `chrome://extensions/`

2. **Enable Developer Mode** (toggle in top right)

3. **Click "Load unpacked"**

4. **Select the `browser-extension` folder** from this project

5. **Pin the extension** for easy access (click the puzzle piece icon, then pin)

## Usage

### Step 1: Visit the Menu Page
Navigate to your cafe's menu page, for example:
- https://sony.cafebonappetit.com

### Step 2: Click the Extension
Click the Cafe Menu Scraper icon in your toolbar

### Step 3: Extract Data
Click "Extract Menu Data" button

The extension will:
- Scan the current page for menu items
- Extract names, prices, and calories
- Show you what it found

### Step 4: Download
Click "Download JSON" to save the menu data

### Step 5: Use the Data
Upload the downloaded JSON file to:
- The web analyzer at http://localhost:5000
- GitHub Pages version
- Or use: `python cafe_analyzer.py --json menu_data_2024-01-06.json`

## Why This Works Better Than Scraping

**Bot protection doesn't apply** because:
- Runs in your real browser (not automated)
- You manually navigate and click
- Uses your normal cookies and session
- No unusual request patterns

This is the **most reliable method** for sites with bot protection!

## Weekly Workflow

Every week when the menu changes:

1. Visit the cafe website
2. Click the extension icon
3. Click "Extract Menu Data"
4. Click "Download JSON"
5. Upload to your analyzer

**Takes less than 30 seconds!**

## Customization

If the extension doesn't find items on your specific site:

1. Right-click → Inspect Element on a menu item
2. Note the CSS class or structure
3. Edit `popup.js` and add the selector to the `selectors` array
4. Reload the extension

## Tips

- Make sure you're on the actual menu page (not homepage)
- Some sites show different menus for different days - navigate to the day you want
- If nutrition info isn't visible, click on items to expand details first
- The extension saves files as `menu_data_YYYY-MM-DD.json` with the date

## Troubleshooting

**No items found:**
- Make sure you're on the menu page showing prices and calories
- Try clicking on menu items to expand nutrition information
- Some sites load content dynamically - wait for the page to fully load

**Missing data (no price or calories):**
- Click on individual items to see full details
- Some sites require you to select a date or location first

**Extension not showing:**
- Make sure Developer Mode is enabled
- Check that you loaded the entire `browser-extension` folder
- Look for error messages in `chrome://extensions/`
