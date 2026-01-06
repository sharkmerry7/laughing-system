# How to Populate Menu Data

This guide shows you different ways to get menu data into the analyzer.

## Quick Start: Use the Example Data

The easiest way to test the analyzer is to use the built-in example data:

**Web Interface:**
```bash
python app.py
# Visit http://localhost:5000
# Click "Load Example Data"
```

**GitHub Pages:**
- Just visit the site and click "Load Example Data"

**Command Line:**
```bash
python cafe_analyzer.py --json example_menu.json
```

---

## Method 1: Manual Entry Helper (Easiest) ⭐

Use the interactive helper script I created:

```bash
python menu_entry_helper.py
```

**Option 1 - Interactive Mode:**
- Enter items one at a time
- Script prompts for name, price, and calories
- Saves to JSON automatically

**Option 2 - Paste Mode:**
- Copy menu data from spreadsheet or website
- Paste in format: `Item Name, Price, Calories`
- Example:
  ```
  Breakfast Burrito, 6.99, 720
  Caesar Salad, 7.99, 350
  Pizza Slice, 3.99, 285
  ```

---

## Method 2: Create JSON File Manually

Create a file named `sony_menu.json`:

```json
[
  {
    "name": "Breakfast Burrito",
    "price": 6.99,
    "calories": 720
  },
  {
    "name": "Grilled Chicken Sandwich",
    "price": 8.49,
    "calories": 520
  },
  {
    "name": "Caesar Salad",
    "price": 7.99,
    "calories": 350
  }
]
```

**Required fields for each item:**
- `name` - String (item name)
- `price` - Number (price in dollars)
- `calories` - Number (calorie count)

**Then use it:**
```bash
# Web interface: Click "Upload Data" and select the file
# OR
python cafe_analyzer.py --json sony_menu.json
```

---

## Method 3: Create CSV File

Create `menu_data.csv`:

```csv
name,price,calories
Breakfast Burrito,6.99,720
Grilled Chicken Sandwich,8.49,520
Caesar Salad,7.99,350
Pepperoni Pizza Slice,3.99,285
French Fries,2.99,365
```

**Use it:**
```bash
python cafe_analyzer.py --csv menu_data.csv
```

Note: CSV upload is only available via command line, not web interface.

---

## Method 4: Copy from Sony Cafe Website

### Step-by-step:

1. **Visit the website** (https://sony.cafebonappetit.com)

2. **Find menu items** - Look for today's or this week's menu

3. **Collect the data** - For each item, note:
   - Item name
   - Price (usually shown with $)
   - Calories (usually shown in nutrition info)

4. **Use one of the methods above** to enter the data:
   - Use the helper script for quick entry
   - Create a JSON file manually
   - Create a spreadsheet and export as CSV

### Tips for Finding Nutrition Info:

Most Cafe Bon Appetit sites show calories when you:
- Click on the menu item
- Look for "Nutrition" or "Nutrition Info" link
- Check the item details panel

---

## Method 5: Spreadsheet to JSON

If you have menu data in Excel or Google Sheets:

### In Excel/Google Sheets:

1. Create columns: `name`, `price`, `calories`
2. Fill in your data
3. Save/Export as CSV
4. Use Method 3 above

### Or convert to JSON:

1. Create your spreadsheet
2. Use this Python script to convert CSV to JSON:

```bash
python -c "
import csv, json, sys

with open('menu_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    items = []
    for row in reader:
        items.append({
            'name': row['name'],
            'price': float(row['price']),
            'calories': int(row['calories'])
        })

with open('menu_data.json', 'w') as f:
    json.dump(items, f, indent=2)

print(f'Converted {len(items)} items to menu_data.json')
"
```

---

## Method 6: Try Web Scraping (May Not Work)

The built-in scraper can attempt to extract data from the website, but it often fails due to bot protection.

**Web Interface:**
1. Go to "Scrape Menu"
2. Enter: `https://sony.cafebonappetit.com`
3. Check "Use browser-based scraping" (needs Chrome installed)
4. Click "Scrape Menu"

**Command Line:**
```bash
# Try basic scraping
python cafe_analyzer.py --url https://sony.cafebonappetit.com

# Try with Selenium (requires Chrome + chromedriver)
python cafe_analyzer.py --url https://sony.cafebonappetit.com --browser
```

**If scraping fails:**
- Use one of the manual methods above
- The website has bot protection (403 errors)
- Manual entry is more reliable

---

## Example Workflow for Sony Cafe

Here's a practical workflow to get your cafe's menu data:

1. **Visit** https://sony.cafebonappetit.com

2. **Use the helper script:**
   ```bash
   python menu_entry_helper.py
   ```

3. **For each menu item on the website:**
   - Enter the name when prompted
   - Enter the price (just the number, like `6.99`)
   - Enter the calories (check nutrition info on the site)

4. **Save and analyze:**
   ```bash
   # File is automatically saved as menu_data.json
   python cafe_analyzer.py --json menu_data.json
   ```

5. **View in web interface:**
   ```bash
   python app.py
   # Visit http://localhost:5000
   # Upload your menu_data.json file
   ```

---

## Updating Your Data

To update the menu (e.g., weekly menu changes):

1. Create a new JSON file with the new menu items
2. Upload it to the analyzer (overwrites previous data)
3. The analysis updates automatically

You can keep different files for different weeks:
- `menu_week1.json`
- `menu_week2.json`
- `menu_week3.json`

---

## Need Help?

If you're having trouble:
1. Check that your JSON is valid at https://jsonlint.com
2. Make sure each item has `name`, `price`, and `calories`
3. Use the example file as a template (`example_menu.json`)
4. Try the helper script (`menu_entry_helper.py`) for easier data entry
