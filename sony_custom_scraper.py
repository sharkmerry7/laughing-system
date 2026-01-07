#!/usr/bin/env python3
"""
Custom scraper for sony.cafebonappetit.com format
Extracts items from scraped_page.html
"""

import re
import json
from bs4 import BeautifulSoup


def extract_sony_menu(html_file='scraped_page.html'):
    """Extract menu from Sony Cafe's specific format"""

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    items = []
    lines = text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Look for price pattern: reg.X.XX or reg. X.XX
        price_match = re.search(r'reg\.?\s*(\d+\.\d{2})', line)

        if price_match:
            price = float(price_match.group(1))

            # Look backwards for the item name (usually 1-3 lines before)
            name = None
            for j in range(max(0, i-5), i):
                potential_name = lines[j].strip()
                # Name should be short, no price pattern, not a description
                if (len(potential_name) > 3 and len(potential_name) < 100 and
                    not re.search(r'reg\.|with|contains|vegan|farm to fork', potential_name, re.I) and
                    not re.search(r'\d+\.\d{2}', potential_name)):
                    name = potential_name
                    break

            if name and price > 0:
                # Check if already added
                if not any(item['name'] == name for item in items):
                    items.append({
                        'name': name,
                        'price': price,
                        'calories': 0,  # Not available
                        'note': 'Calories not shown on this page'
                    })

        i += 1

    return items


def main():
    print("Extracting from scraped_page.html...")
    items = extract_sony_menu()

    if items:
        print(f"\n✓ Found {len(items)} items (WITHOUT calorie data):\n")
        for item in items:
            print(f"  • {item['name']} - ${item['price']}")

        print("\n" + "="*60)
        print("⚠️  WARNING: NO CALORIE DATA AVAILABLE")
        print("="*60)
        print("\nThe page you scraped doesn't show calories.")
        print("You need to:")
        print("  1. Click on menu items to see nutrition info")
        print("  2. Look for a 'Nutrition' tab or button")
        print("  3. Navigate to a page that shows calories")
        print("\nWithout calories, you can't calculate calorie per dollar!")
        print("="*60)

        # Ask user if they want to save anyway
        response = input("\nSave these items without calories? (y/n): ").lower()
        if response == 'y':
            with open('menu_no_calories.json', 'w') as f:
                json.dump(items, f, indent=2)
            print("✓ Saved to menu_no_calories.json")
            print("\nYou'll need to manually add calories to each item.")
    else:
        print("✗ No items found")


if __name__ == '__main__':
    main()
