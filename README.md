# Cafe Calorie Per Dollar Analyzer

A tool to analyze menu items from Cafe Bon Appetit and calculate the calorie per dollar ratio to help identify the best value items.

## Features

- Web interface for easy browsing and analysis
- Scrapes menu data from sony.cafebonappetit.com
- Calculates calorie per dollar ratios
- Sorts items by best value
- Supports multiple data input formats (web scraping, CSV, JSON)
- Interactive filtering by price and calorie ranges
- Detailed statistics and visualizations
- Command-line interface for automation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Web Interface (Recommended)

Start the web server:
```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

The web interface provides:
- Interactive data visualization
- Menu data upload (JSON files)
- Web scraping interface
- Filtering and sorting options
- Beautiful, responsive design

### Option 2: Command Line Interface

#### Scrape and analyze the weekly menu:
```bash
python cafe_analyzer.py --url https://sony.cafebonappetit.com
```

#### Analyze from a JSON file:
```bash
python cafe_analyzer.py --json example_menu.json
```

#### Analyze from a CSV file:
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

## Quick Start with Example Data

To see the analyzer in action immediately:

**Web Interface:**
```bash
python app.py
```
The example menu is automatically loaded. Visit http://localhost:5000/analyze to see results.

**Command Line:**
```bash
python cafe_analyzer.py --json example_menu.json
```

## Notes

If the website has bot protection, you may need to:
1. Manually export the menu data to JSON or CSV
2. Use the `--browser` flag for browser-based scraping (requires Chrome)
3. Use the web interface's upload feature to load your data

## Project Structure

```
.
├── app.py                  # Flask web application
├── cafe_analyzer.py        # Command-line tool
├── analyzer.py             # Analysis logic
├── scraper.py              # Web scraping module
├── requirements.txt        # Python dependencies
├── example_menu.json       # Sample menu data
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── analyze.html
│   ├── upload.html
│   └── scrape.html
└── static/
    ├── css/
    │   └── style.css       # Styling
    └── example_menu.json   # Downloadable sample
```
