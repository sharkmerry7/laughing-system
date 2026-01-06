# Cafe Calorie Per Dollar Analyzer

A tool to analyze menu items from Cafe Bon Appetit and calculate the calorie per dollar ratio to help identify the best value items.

## Features

- Scrapes menu data from sony.cafebonappetit.com
- Calculates calorie per dollar ratios
- Sorts items by best value
- Supports multiple data input formats (web scraping, CSV, JSON)
- Generates detailed reports

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Scrape and analyze the weekly menu:
```bash
python cafe_analyzer.py --url https://sony.cafebonappetit.com
```

### Analyze from a JSON file:
```bash
python cafe_analyzer.py --json menu_data.json
```

### Analyze from a CSV file:
```bash
python cafe_analyzer.py --csv menu_data.csv
```

## Output

The analyzer will display:
- Menu item name
- Price
- Calories
- Calorie per dollar ratio
- Items sorted by best value (highest calories per dollar)

## Data Format

### JSON Format:
```json
[
  {
    "name": "Item Name",
    "price": 8.99,
    "calories": 650
  }
]
```

### CSV Format:
```csv
name,price,calories
Item Name,8.99,650
```

## Notes

If the website has bot protection, you may need to:
1. Manually export the menu data to JSON or CSV
2. Use the `--browser` flag for browser-based scraping (requires Chrome)
