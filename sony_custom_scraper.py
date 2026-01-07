#!/usr/bin/env python3
"""
Custom scraper for sony.cafebonappetit.com format
Handles their specific format: name, reg.X.XX, XXX cal. nutrition information
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
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for price pattern: reg.X.XX
        price_match = re.search(r'reg\.?\s*(\d+\.\d{2})', line)

        if price_match:
            price = float(price_match.group(1))

            # Look backwards for name (usually previous line)
            name = None
            for j in range(max(0, i-3), i):
                potential_name = lines[j]
                # Skip descriptions and metadata
                if (len(potential_name) > 2 and len(potential_name) < 100 and
                    not re.search(r'reg\.|cal\.|with|contains|vegan|farm to fork|nutrition|absolutely', potential_name, re.I)):
                    name = potential_name
                    break

            # Look forwards for calories (usually next line or two)
            calories = 0
            for j in range(i+1, min(len(lines), i+5)):
                cal_match = re.search(r'(\d+)\s*cal', lines[j], re.I)
                if cal_match:
                    calories = int(cal_match.group(1))
                    break

            if name and price > 0 and calories > 0:
                # Check if already added
                if not any(item['name'] == name for item in items):
                    items.append({
                        'name': name,
                        'price': price,
                        'calories': calories
                    })

        i += 1

    # Remove duplicates and sort
    seen = set()
    unique_items = []
    for item in items:
        key = (item['name'], item['price'], item['calories'])
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    unique_items.sort(key=lambda x: x['name'])

    return unique_items


def main():
    print("Extracting from scraped_page.html...")
    print("Looking for Sony Cafe format: name, reg.X.XX, XXX cal...\n")

    items = extract_sony_menu()

    if items:
        print(f"✓ Found {len(items)} menu items:\n")
        for item in items:
            print(f"  • {item['name']}")
            print(f"    ${item['price']:.2f} - {item['calories']} cal - {item['calories']/item['price']:.1f} cal/$")

        # Save to JSON
        with open('menu.json', 'w') as f:
            json.dump(items, f, indent=2)

        print(f"\n{'='*60}")
        print(f"✓ SUCCESS! Saved {len(items)} items to menu.json")
        print(f"{'='*60}")
        print("\nNext steps:")
        print("  python cafe_analyzer.py --json menu.json")
        print("\nOr upload menu.json to the web interface:")
        print("  python app.py")

        return True
    else:
        print("✗ No items found with all three: name, price, and calories")
        print("\nTroubleshooting:")
        print("  1. Make sure scraped_page.html has the full menu")
        print("  2. Check that items show 'reg.X.XX' for price")
        print("  3. Check that items show 'XXX cal' for calories")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
