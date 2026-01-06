"""
Enhanced scraper with better bot detection evasion
Uses multiple strategies to bypass bot protection
"""

import time
import random
import json
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# Try to import undetected_chromedriver (best for bot evasion)
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False
    print("Note: undetected-chromedriver not available. Install with: pip install undetected-chromedriver")

# Try to import playwright (modern alternative)
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class EnhancedMenuScraper:
    """Enhanced scraper with multiple strategies for bot evasion"""

    def __init__(self, url: str):
        self.url = url

    def scrape_with_undetected_chrome(self) -> Optional[List[Dict]]:
        """Use undetected-chromedriver - best for bypassing bot protection"""
        if not UNDETECTED_AVAILABLE:
            print("undetected-chromedriver not installed")
            return None

        print("Using undetected-chromedriver (best bot evasion)...")

        try:
            options = uc.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = uc.Chrome(options=options, version_main=None)

            # Navigate to page
            driver.get(self.url)

            # Wait for page load with random human-like delay
            time.sleep(random.uniform(2, 4))

            # Scroll like a human
            self._human_scroll(driver)

            # Get page source
            html = driver.page_source
            driver.quit()

            return self._parse_html(html)

        except Exception as e:
            print(f"Error with undetected-chromedriver: {e}")
            return None

    def scrape_with_playwright(self) -> Optional[List[Dict]]:
        """Use Playwright - modern browser automation"""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright not installed")
            return None

        print("Using Playwright...")

        try:
            with sync_playwright() as p:
                # Launch browser with realistic settings
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                )

                # Create context with realistic viewport and user agent
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )

                page = context.new_page()

                # Navigate
                page.goto(self.url, wait_until='networkidle')

                # Human-like delay
                time.sleep(random.uniform(1.5, 3))

                # Scroll to load dynamic content
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)

                # Get content
                html = page.content()

                browser.close()

                return self._parse_html(html)

        except Exception as e:
            print(f"Error with Playwright: {e}")
            return None

    def _human_scroll(self, driver):
        """Simulate human-like scrolling behavior"""
        try:
            total_height = driver.execute_script("return document.body.scrollHeight")
            viewport_height = driver.execute_script("return window.innerHeight")

            current_position = 0
            while current_position < total_height:
                # Random scroll amount
                scroll_amount = random.randint(100, 300)
                current_position += scroll_amount

                driver.execute_script(f"window.scrollTo(0, {current_position})")

                # Random delay between scrolls
                time.sleep(random.uniform(0.1, 0.3))
        except:
            pass

    def _parse_html(self, html: str) -> List[Dict]:
        """Parse HTML to extract menu items - Cafe Bon Appetit specific"""
        soup = BeautifulSoup(html, 'lxml')
        menu_items = []

        # Save HTML for debugging
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved page HTML to debug_page.html for inspection")

        # Strategy 1: Look for common Cafe Bon Appetit patterns
        # They often use specific CSS classes or data attributes

        # Try finding menu items by common class patterns
        possible_selectors = [
            {'class': 'menu-item'},
            {'class': 'food-item'},
            {'class': 'item'},
            {'data-name': True},
            {'class': 'site-panel__daypart-item'},
            {'class': 'nutrition-item'},
        ]

        for selector in possible_selectors:
            items = soup.find_all(attrs=selector)
            if items:
                print(f"Found {len(items)} potential items with selector: {selector}")

                for item in items:
                    try:
                        parsed = self._extract_item_data(item)
                        if parsed and parsed['price'] > 0 and parsed['calories'] > 0:
                            menu_items.append(parsed)
                    except:
                        continue

        # Remove duplicates based on name
        seen = set()
        unique_items = []
        for item in menu_items:
            if item['name'] not in seen:
                seen.add(item['name'])
                unique_items.append(item)

        print(f"Extracted {len(unique_items)} unique menu items")

        return unique_items

    def _extract_item_data(self, element) -> Optional[Dict]:
        """Extract name, price, and calories from an element"""
        import re

        # Get all text from element
        text = element.get_text(separator=' ', strip=True)

        # Try to find name (usually the first significant text)
        name = None
        for tag in ['h2', 'h3', 'h4', 'span', 'div', 'a']:
            name_elem = element.find(tag, class_=re.compile(r'name|title|label', re.I))
            if name_elem:
                name = name_elem.get_text(strip=True)
                break

        if not name:
            # Try data attributes
            name = element.get('data-name') or element.get('aria-label')

        if not name:
            # Take first non-empty text
            for tag in element.find_all(['h2', 'h3', 'h4', 'span']):
                potential = tag.get_text(strip=True)
                if len(potential) > 3:
                    name = potential
                    break

        # Find price
        price = 0.0
        price_match = re.search(r'\$?\s*(\d+\.?\d*)', text)
        if price_match:
            price = float(price_match.group(1))

        # Find calories
        calories = 0
        cal_match = re.search(r'(\d+)\s*(cal|kcal|calories)', text, re.I)
        if cal_match:
            calories = int(cal_match.group(1))

        if name and price > 0 and calories > 0:
            return {
                'name': name,
                'price': price,
                'calories': calories
            }

        return None

    def scrape(self, method='auto') -> List[Dict]:
        """
        Main scraping method with fallback strategy

        Args:
            method: 'auto', 'undetected', 'playwright'
        """

        if method == 'undetected' or (method == 'auto' and UNDETECTED_AVAILABLE):
            result = self.scrape_with_undetected_chrome()
            if result and len(result) > 0:
                return result

        if method == 'playwright' or (method == 'auto' and PLAYWRIGHT_AVAILABLE):
            result = self.scrape_with_playwright()
            if result and len(result) > 0:
                return result

        print("\nAll scraping methods failed or returned no data.")
        print("\nTroubleshooting:")
        print("1. Check debug_page.html to see what was actually loaded")
        print("2. Visit the website manually to see the menu structure")
        print("3. The site may require JavaScript or have strong bot protection")
        print("4. Consider using the browser extension method (see docs)")

        return []


def auto_scrape_and_save(url: str, output_file: str = 'menu_data.json'):
    """
    Convenience function to scrape and save in one step
    """
    scraper = EnhancedMenuScraper(url)
    items = scraper.scrape()

    if items:
        with open(output_file, 'w') as f:
            json.dump(items, f, indent=2)
        print(f"\n✓ Successfully saved {len(items)} items to {output_file}")
        return True
    else:
        print("\n✗ No items found. See troubleshooting above.")
        return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python enhanced_scraper.py <url> [output_file]")
        print("Example: python enhanced_scraper.py https://sony.cafebonappetit.com menu.json")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'menu_data.json'

    auto_scrape_and_save(url, output)
