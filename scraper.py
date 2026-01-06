"""
Menu data scraper for Cafe Bon Appetit
Supports multiple scraping methods to handle bot protection
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict, Optional
import time

# Selenium imports are optional - only needed for browser-based scraping
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class MenuScraper:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def scrape_with_requests(self) -> Optional[List[Dict]]:
        """Try to scrape using requests library"""
        try:
            session = requests.Session()
            response = session.get(self.url, headers=self.headers, timeout=10)

            if response.status_code == 403:
                print("Access forbidden (403). Website has bot protection.")
                return None

            response.raise_for_status()
            return self._parse_html(response.text)
        except Exception as e:
            print(f"Error with requests scraping: {e}")
            return None

    def scrape_with_selenium(self) -> Optional[List[Dict]]:
        """Try to scrape using Selenium (browser automation)"""
        if not SELENIUM_AVAILABLE:
            print("Selenium is not installed. Install it with: pip install selenium")
            print("You also need Chrome and chromedriver installed.")
            return None

        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            driver = webdriver.Chrome(options=options)
            driver.get(self.url)

            # Wait for page to load
            time.sleep(3)

            html = driver.page_source
            driver.quit()

            return self._parse_html(html)
        except Exception as e:
            print(f"Error with Selenium scraping: {e}")
            print("Make sure Chrome and chromedriver are installed.")
            return None

    def _parse_html(self, html: str) -> List[Dict]:
        """Parse HTML to extract menu items"""
        soup = BeautifulSoup(html, 'lxml')
        menu_items = []

        # Look for common Cafe Bon Appetit menu item patterns
        # This is a generic parser - may need adjustment based on actual HTML structure

        # Try to find menu items
        items = soup.find_all(['div', 'article', 'li'], class_=re.compile(r'menu.*item|item.*card|food.*item', re.I))

        for item in items:
            try:
                # Extract name
                name_elem = item.find(['h2', 'h3', 'h4', 'span', 'div'], class_=re.compile(r'name|title', re.I))
                if not name_elem:
                    name_elem = item.find(['h2', 'h3', 'h4'])

                # Extract price
                price_elem = item.find(['span', 'div', 'p'], class_=re.compile(r'price|cost', re.I))
                if not price_elem:
                    price_elem = item.find(string=re.compile(r'\$\d+\.?\d*'))

                # Extract calories
                cal_elem = item.find(['span', 'div', 'p'], string=re.compile(r'\d+\s*(cal|kcal)', re.I))
                if not cal_elem:
                    cal_elem = item.find(['span', 'div', 'p'], class_=re.compile(r'calor|nutrition', re.I))

                if name_elem and price_elem and cal_elem:
                    name = name_elem.get_text(strip=True)

                    # Extract numeric price
                    price_text = price_elem.get_text(strip=True) if hasattr(price_elem, 'get_text') else str(price_elem)
                    price_match = re.search(r'\$?(\d+\.?\d*)', price_text)
                    price = float(price_match.group(1)) if price_match else 0.0

                    # Extract numeric calories
                    cal_text = cal_elem.get_text(strip=True)
                    cal_match = re.search(r'(\d+)', cal_text)
                    calories = int(cal_match.group(1)) if cal_match else 0

                    if price > 0 and calories > 0:
                        menu_items.append({
                            'name': name,
                            'price': price,
                            'calories': calories
                        })
            except Exception as e:
                continue

        return menu_items

    def scrape(self, use_selenium: bool = False) -> List[Dict]:
        """Main scraping method"""
        print(f"Scraping menu from {self.url}...")

        if use_selenium:
            result = self.scrape_with_selenium()
        else:
            result = self.scrape_with_requests()
            if result is None or len(result) == 0:
                print("Falling back to Selenium...")
                result = self.scrape_with_selenium()

        if result:
            print(f"Successfully scraped {len(result)} menu items")
        else:
            print("Failed to scrape menu items")
            result = []

        return result


def load_from_json(filepath: str) -> List[Dict]:
    """Load menu data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_from_csv(filepath: str) -> List[Dict]:
    """Load menu data from CSV file"""
    import csv
    items = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                'name': row['name'],
                'price': float(row['price']),
                'calories': int(row['calories'])
            })
    return items


def save_to_json(items: List[Dict], filepath: str):
    """Save menu data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(items, f, indent=2)
    print(f"Saved {len(items)} items to {filepath}")
