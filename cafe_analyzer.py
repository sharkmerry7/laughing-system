#!/usr/bin/env python3
"""
Cafe Calorie Per Dollar Analyzer
Main CLI application
"""

import argparse
import sys
from scraper import MenuScraper, load_from_json, load_from_csv, save_to_json
from analyzer import CalorieAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description='Analyze cafe menu items for calorie per dollar value'
    )

    # Input sources (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--url', type=str,
                            help='URL to scrape menu data from (e.g., https://sony.cafebonappetit.com)')
    input_group.add_argument('--json', type=str,
                            help='Path to JSON file with menu data')
    input_group.add_argument('--csv', type=str,
                            help='Path to CSV file with menu data')

    # Options
    parser.add_argument('--browser', action='store_true',
                       help='Use browser-based scraping (Selenium) instead of requests')
    parser.add_argument('--top', type=int, default=10,
                       help='Number of top items to show (default: 10)')
    parser.add_argument('--save-data', type=str,
                       help='Save scraped menu data to JSON file')
    parser.add_argument('--save-csv', type=str,
                       help='Export analysis results to CSV file')
    parser.add_argument('--save-json', type=str,
                       help='Export analysis results to JSON file')

    # Filters
    parser.add_argument('--min-price', type=float,
                       help='Filter items with minimum price')
    parser.add_argument('--max-price', type=float,
                       help='Filter items with maximum price')
    parser.add_argument('--min-calories', type=int,
                       help='Filter items with minimum calories')
    parser.add_argument('--max-calories', type=int,
                       help='Filter items with maximum calories')

    args = parser.parse_args()

    # Load menu data
    menu_items = []

    try:
        if args.url:
            print(f"Fetching menu from: {args.url}")
            scraper = MenuScraper(args.url)
            menu_items = scraper.scrape(use_selenium=args.browser)

            if not menu_items:
                print("\nFailed to scrape menu items from the website.")
                print("This could be due to:")
                print("  1. Bot protection (403 Forbidden)")
                print("  2. Website structure changed")
                print("  3. Network issues")
                print("\nTry these alternatives:")
                print("  - Use --browser flag for Selenium-based scraping")
                print("  - Manually save menu data and use --json or --csv")
                print("  - Check if the URL is correct")
                sys.exit(1)

            # Save scraped data if requested
            if args.save_data:
                save_to_json(menu_items, args.save_data)

        elif args.json:
            print(f"Loading menu from JSON: {args.json}")
            menu_items = load_from_json(args.json)

        elif args.csv:
            print(f"Loading menu from CSV: {args.csv}")
            menu_items = load_from_csv(args.csv)

        if not menu_items:
            print("No menu items found!")
            sys.exit(1)

        print(f"Loaded {len(menu_items)} menu items\n")

        # Analyze
        analyzer = CalorieAnalyzer(menu_items)
        analyzer.analyze()

        # Apply filters if specified
        if any([args.min_price, args.max_price, args.min_calories, args.max_calories]):
            filtered_items = analyzer.get_items_by_category(
                min_price=args.min_price,
                max_price=args.max_price,
                min_calories=args.min_calories,
                max_calories=args.max_calories
            )
            print(f"Applied filters: {len(filtered_items)} items match criteria\n")
            analyzer.analyzed_items = filtered_items

        # Print report
        analyzer.print_report(top_n=args.top)

        # Export if requested
        if args.save_csv:
            analyzer.export_to_csv(args.save_csv)

        if args.save_json:
            analyzer.export_to_json(args.save_json)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
