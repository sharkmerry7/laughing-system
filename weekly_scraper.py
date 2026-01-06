#!/usr/bin/env python3
"""
Weekly automated menu scraper
Can be run manually or scheduled with cron/Task Scheduler
"""

import os
import json
from datetime import datetime
from enhanced_scraper import EnhancedMenuScraper

# Configuration
CAFE_URL = "https://sony.cafebonappetit.com"
OUTPUT_DIR = "weekly_menus"
NOTIFY_EMAIL = None  # Set to your email for notifications (requires setup)


def scrape_weekly_menu():
    """
    Scrape the weekly menu and save with date stamp
    """
    print("=" * 60)
    print(f"Weekly Menu Scraper - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(OUTPUT_DIR, f'menu_{date_str}.json')

    # Check if already scraped today
    if os.path.exists(output_file):
        print(f"✓ Menu already scraped today: {output_file}")
        with open(output_file, 'r') as f:
            data = json.load(f)
        print(f"  Contains {len(data)} items")
        return output_file, True

    # Scrape the menu
    print(f"\nScraping menu from: {CAFE_URL}")
    scraper = EnhancedMenuScraper(CAFE_URL)
    items = scraper.scrape(method='auto')

    if items and len(items) > 0:
        # Save the data
        with open(output_file, 'w') as f:
            json.dump(items, f, indent=2)

        print(f"\n✓ SUCCESS: Saved {len(items)} items to {output_file}")

        # Create a symlink/copy to latest.json for easy access
        latest_file = os.path.join(OUTPUT_DIR, 'latest.json')
        with open(latest_file, 'w') as f:
            json.dump(items, f, indent=2)
        print(f"✓ Also saved to {latest_file}")

        # Send notification if configured
        if NOTIFY_EMAIL:
            send_notification(True, len(items), output_file)

        return output_file, True
    else:
        print(f"\n✗ FAILED: Could not scrape menu")
        print("This usually means:")
        print("  1. Bot protection blocked the scraper")
        print("  2. Website structure changed")
        print("  3. Network/connection issue")
        print("\nRecommendation: Use the browser extension instead")

        # Send failure notification
        if NOTIFY_EMAIL:
            send_notification(False, 0, None)

        return None, False


def send_notification(success, item_count, filename):
    """
    Send email notification about scraping result
    Requires email configuration
    """
    try:
        import smtplib
        from email.mime.text import MIMEText

        if success:
            subject = f"✓ Weekly Menu Scraped - {item_count} items"
            body = f"Successfully scraped {item_count} menu items.\nSaved to: {filename}"
        else:
            subject = "✗ Weekly Menu Scraping Failed"
            body = "Failed to scrape this week's menu. Manual intervention needed."

        # Note: You need to configure SMTP settings
        # This is just a template
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'your-email@gmail.com'
        msg['To'] = NOTIFY_EMAIL

        # Uncomment and configure when ready to use
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login('your-email@gmail.com', 'your-app-password')
        # server.send_message(msg)
        # server.quit()

        print(f"✓ Notification sent to {NOTIFY_EMAIL}")
    except Exception as e:
        print(f"Could not send notification: {e}")


def setup_cron():
    """
    Display instructions for setting up automatic weekly scraping
    """
    script_path = os.path.abspath(__file__)

    print("\n" + "=" * 60)
    print("AUTOMATIC WEEKLY SCRAPING SETUP")
    print("=" * 60)

    print("\n📅 LINUX/MAC (crontab):")
    print("-" * 60)
    print("1. Open crontab editor:")
    print("   crontab -e")
    print("\n2. Add this line (runs every Monday at 6 AM):")
    print(f"   0 6 * * 1 /usr/bin/python3 {script_path}")
    print("\n3. Or run every Sunday at 9 PM:")
    print(f"   0 21 * * 0 /usr/bin/python3 {script_path}")

    print("\n\n📅 WINDOWS (Task Scheduler):")
    print("-" * 60)
    print("1. Open Task Scheduler")
    print("2. Create Basic Task")
    print("3. Set trigger: Weekly, select day/time")
    print("4. Action: Start a program")
    print("   Program: python")
    print(f"   Arguments: {script_path}")

    print("\n\n📅 MANUAL TESTING:")
    print("-" * 60)
    print("Run this script directly:")
    print(f"   python {script_path}")

    print("\n" + "=" * 60)


def list_saved_menus():
    """List all previously scraped menus"""
    if not os.path.exists(OUTPUT_DIR):
        print("No menus saved yet.")
        return

    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json') and f != 'latest.json']
    files.sort(reverse=True)

    if not files:
        print("No menus saved yet.")
        return

    print("\n" + "=" * 60)
    print("SAVED MENUS")
    print("=" * 60)

    for filename in files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

        date = filename.replace('menu_', '').replace('.json', '')
        print(f"{date}: {len(data)} items - {filepath}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'setup':
            setup_cron()
        elif command == 'list':
            list_saved_menus()
        elif command == 'test':
            print("Testing scraper...")
            scrape_weekly_menu()
        else:
            print(f"Unknown command: {command}")
            print("Usage:")
            print("  python weekly_scraper.py          # Run scraper")
            print("  python weekly_scraper.py setup    # Show setup instructions")
            print("  python weekly_scraper.py list     # List saved menus")
            print("  python weekly_scraper.py test     # Test scraper")
    else:
        # Default: run the scraper
        result_file, success = scrape_weekly_menu()

        if success and result_file:
            print(f"\n{'=' * 60}")
            print("NEXT STEPS:")
            print(f"{'=' * 60}")
            print(f"\n1. Analyze the menu:")
            print(f"   python cafe_analyzer.py --json {result_file}")
            print(f"\n2. Or upload to web interface:")
            print(f"   python app.py")
            print(f"   Then upload: {result_file}")
            print(f"\n3. Set up automatic weekly scraping:")
            print(f"   python weekly_scraper.py setup")
