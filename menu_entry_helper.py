#!/usr/bin/env python3
"""
Quick Menu Data Entry Helper
Helps you quickly create a JSON file from menu data
"""

import json

def create_menu_data():
    """Interactive menu data entry"""
    print("=" * 60)
    print("Cafe Menu Data Entry Helper")
    print("=" * 60)
    print("\nEnter menu items one at a time.")
    print("Press Enter with empty name to finish.\n")

    menu_items = []

    while True:
        print(f"\n--- Item #{len(menu_items) + 1} ---")

        # Get item name
        name = input("Item name (or press Enter to finish): ").strip()
        if not name:
            break

        # Get price
        while True:
            try:
                price_str = input("Price (e.g., 6.99): $").strip().replace('$', '')
                price = float(price_str)
                break
            except ValueError:
                print("Invalid price. Please enter a number like 6.99")

        # Get calories
        while True:
            try:
                calories_str = input("Calories (e.g., 720): ").strip()
                calories = int(calories_str)
                break
            except ValueError:
                print("Invalid calories. Please enter a whole number like 720")

        menu_items.append({
            "name": name,
            "price": price,
            "calories": calories
        })

        print(f"✓ Added: {name} - ${price:.2f} - {calories} cal")

    if not menu_items:
        print("\nNo items entered. Exiting.")
        return

    # Save to file
    filename = input("\nSave as (default: menu_data.json): ").strip()
    if not filename:
        filename = "menu_data.json"
    if not filename.endswith('.json'):
        filename += '.json'

    with open(filename, 'w') as f:
        json.dump(menu_items, f, indent=2)

    print(f"\n✓ Saved {len(menu_items)} items to {filename}")
    print(f"\nNow you can use:")
    print(f"  python cafe_analyzer.py --json {filename}")
    print(f"  or upload {filename} to the web interface")


def create_from_text():
    """Create menu data from pasted text"""
    print("=" * 60)
    print("Cafe Menu Data Entry - Paste Mode")
    print("=" * 60)
    print("\nPaste your menu data in this format:")
    print("Item Name, Price, Calories")
    print("Example:")
    print("  Breakfast Burrito, 6.99, 720")
    print("  Caesar Salad, 7.99, 350")
    print("\nPaste your data below (press Ctrl+D or Ctrl+Z when done):\n")

    menu_items = []

    try:
        while True:
            line = input().strip()
            if not line or line.startswith('#'):
                continue

            parts = [p.strip() for p in line.split(',')]
            if len(parts) != 3:
                print(f"Skipping invalid line: {line}")
                continue

            try:
                name = parts[0]
                price = float(parts[1].replace('$', ''))
                calories = int(parts[2])

                menu_items.append({
                    "name": name,
                    "price": price,
                    "calories": calories
                })
                print(f"✓ {name}")
            except ValueError:
                print(f"Skipping invalid line: {line}")
    except EOFError:
        pass

    if not menu_items:
        print("\nNo valid items found. Exiting.")
        return

    # Save to file
    filename = "menu_data.json"
    with open(filename, 'w') as f:
        json.dump(menu_items, f, indent=2)

    print(f"\n✓ Saved {len(menu_items)} items to {filename}")
    print(f"\nNow you can use:")
    print(f"  python cafe_analyzer.py --json {filename}")


if __name__ == '__main__':
    import sys

    print("\nHow would you like to enter data?")
    print("1. Interactive (one item at a time)")
    print("2. Paste (comma-separated format)")

    choice = input("\nChoice (1 or 2): ").strip()

    if choice == '1':
        create_menu_data()
    elif choice == '2':
        create_from_text()
    else:
        print("Invalid choice. Exiting.")
