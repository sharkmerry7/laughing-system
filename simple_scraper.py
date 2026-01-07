#!/usr/bin/env python3
"""
Simple scraper using just Selenium
Works on Windows without extra setup
"""

import json
import time
import re
from typing import List, Dict

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Selenium not installed. Run: pip install selenium")
    exit(1)

from bs4 import BeautifulSoup


def simple_scrape(url: str, output_file: str = 'menu.json'):
    """
    Simple scraper using Selenium
    """
    print(f"Scraping: {url}")
    print("This will open a Chrome window briefly...\n")

    # Set up Chrome options
    options = Options()
    options.add_argument('--start-maximized')
    # Don't use headless - let user see what's happening
    # options.add_argument('--headless')

    try:
        # Create driver
        driver = webdriver.Chrome(options=options)

        print("Opening website...")
        driver.get(url)

        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(5)  # Give it time to load

        # Scroll to load dynamic content
        print("Scrolling to load content...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Get page source
        html = driver.page_source

        # Save for debugging
        with open('scraped_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Saved page HTML to scraped_page.html")

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract menu items
        items = []

        # Strategy: Find all elements with text containing both $ and cal
        all_elements = soup.find_all(True)  # Get all elements

        for element in all_elements:
            text = element.get_text()

            # Must have price and calories
            if '$' not in text or not re.search(r'\d+\s*cal', text, re.I):
                continue

            # Must be reasonable length
            if len(text) < 10 or len(text) > 500:
                continue

            # Extract data
            try:
                # Name: first line of text that doesn't have $ or cal
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                name = None
                for line in lines:
                    if '$' not in line and not re.search(r'\d+\s*cal', line, re.I):
                        if len(line) > 3 and len(line) < 100:
                            name = line
                            break

                # Price
                price_match = re.search(r'\$(\d+\.?\d*)', text)
                price = float(price_match.group(1)) if price_match else 0

                # Calories
                cal_match = re.search(r'(\d+)\s*cal', text, re.I)
                calories = int(cal_match.group(1)) if cal_match else 0

                if name and price > 0 and calories > 0:
                    # Check if not duplicate
                    if not any(item['name'] == name for item in items):
                        items.append({
                            'name': name,
                            'price': price,
                            'calories': calories
                        })
            except:
                continue

        driver.quit()

        if items:
            # Save to file
            with open(output_file, 'w') as f:
                json.dump(items, f, indent=2)

            print(f"\n✓ SUCCESS! Found {len(items)} menu items")
            print(f"✓ Saved to {output_file}")
            print("\nItems found:")
            for item in items[:5]:
                print(f"  • {item['name']} - ${item['price']} - {item['calories']} cal")
            if len(items) > 5:
                print(f"  ... and {len(items) - 5} more")

            return True
        else:
            print("\n✗ No menu items found")
            print("\nTroubleshooting:")
            print("1. Check scraped_page.html to see what was loaded")
            print("2. Make sure you navigated to the menu page")
            print("3. The site might need manual interaction (clicking buttons)")
            print("\nTry the browser extension instead - it's more reliable!")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure Chrome is installed!")
        return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python simple_scraper.py <url> [output_file]")
        print("Example: python simple_scraper.py https://sony.cafebonappetit.com menu.json")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'menu.json'

    success = simple_scrape(url, output)

    if success:
        print(f"\n✓ Next step: python cafe_analyzer.py --json {output}")
    else:
        print("\n✗ Scraping failed. Use the browser extension instead:")
        print("  1. Open Chrome → chrome://extensions/")
        print("  2. Load unpacked → Select browser-extension/")
        print("  3. Visit the menu page and click the extension")
