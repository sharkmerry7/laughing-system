# Troubleshooting the Browser Extension

If the extension says "No menu items found", follow these steps:

## Quick Fixes

### 1. Make Sure You're On The Right Page

The extension needs to be on a page that shows:
- Menu item names
- Prices (with $ signs)
- Calorie counts

**Common issues:**
- ❌ You're on the homepage (no menu shown)
- ❌ You're on a "welcome" or "location selection" page
- ❌ The menu items are collapsed/hidden
- ✅ You should be on the actual menu/food listing page

### 2. Expand Menu Items

Many Cafe Bon Appetit sites hide nutrition info until you click:

1. **Look for buttons like:**
   - "View Menu"
   - "See Nutrition"
   - "Details"
   - Individual menu item buttons/cards

2. **Click on menu items** to expand their details

3. **Try the extension again** after details are visible

### 3. Select Date/Location

Some sites require:
- Selecting today's date
- Choosing a specific meal (breakfast, lunch, dinner)
- Selecting a location/station

**Do this BEFORE running the extension**

## Understanding Debug Info

When no items are found, the extension now shows debug information:

```
• Found X potential elements     ← How many things it checked
• Price matches: X                ← Found prices in X elements
• Calorie matches: X              ← Found calories in X elements
• Complete items: 0               ← None had all 3 (name, price, calories)
```

**What this means:**

| Debug Output | Problem | Solution |
|--------------|---------|----------|
| 0 elements found | Page has no menu content | Navigate to menu page |
| Price matches: 0 | No prices visible | Make sure prices are showing |
| Calorie matches: 0 | No nutrition info visible | Click items to expand details |
| Complete items: 0 | Can't match name+price+calories | See manual extraction below |

## Manual Extraction (Fallback)

If the extension still can't find items, you can manually copy the data:

### Method 1: Simple Copy-Paste

1. Open the page HTML:
   - Right-click → Inspect
   - Or press F12

2. In the Console tab, paste this code:

```javascript
// Extract visible text that looks like menu items
Array.from(document.querySelectorAll('*')).forEach(el => {
  const text = el.textContent;
  if (text.includes('$') && text.match(/\d+\s*cal/i) && text.length < 200) {
    console.log(text);
  }
});
```

3. Copy the output and use the manual entry helper:
   ```bash
   python menu_entry_helper.py
   ```

### Method 2: Export Specific Elements

If you can see the menu items on screen:

1. Right-click on a menu item → Inspect
2. Note the HTML structure/class name
3. Email me the class name or add it to the extension (see below)

## Customizing the Extension for Your Site

If you're technical, you can add site-specific selectors:

1. Open `browser-extension/popup.js`

2. Find the `specificSelectors` array (around line 41):

```javascript
const specificSelectors = [
  'button[class*="menu"]',
  'div[class*="menu-item"]',
  // Add your custom selector here
  '.your-custom-class',
];
```

3. Add the selector you found from inspecting the page

4. Reload the extension:
   - Go to chrome://extensions/
   - Click the refresh icon on the Cafe Menu Scraper extension

## Still Not Working?

### Alternative: Use Enhanced Scraper

Try the automated scraper which might work better:

```bash
pip install undetected-chromedriver
python enhanced_scraper.py https://sony.cafebonappetit.com menu.json
```

### Alternative: Manual Entry Helper

Use the interactive helper (5-10 min for a full menu):

```bash
python menu_entry_helper.py
```

Choose option 2 (paste mode) and paste menu data in this format:
```
Item Name, Price, Calories
Breakfast Burrito, 6.99, 720
Caesar Salad, 7.99, 350
```

## Getting Help

If you want to report the issue, please provide:

1. The URL you're trying to scrape
2. The debug info shown by the extension
3. Screenshot of the menu page
4. Whether nutrition info is visible on the page

This helps me add support for your specific Cafe Bon Appetit site!

## Common Cafe Bon Appetit Site Patterns

Different locations have different layouts:

**Pattern A: Click to expand**
- Menu items are buttons
- Click them to see nutrition
- Run extension AFTER clicking

**Pattern B: Separate nutrition page**
- Click "Nutrition" link first
- Then run extension

**Pattern C: Hover to see details**
- Hover over items
- Some sites don't show calories until hover
- May need to use automated scraper instead

**Pattern D: PDF menu**
- Some locations only have PDF menus
- Extension won't work
- Download PDF and manually enter data
