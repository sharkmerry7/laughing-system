"""
Calorie Per Dollar Analyzer
Analyzes menu items to find the best value based on calories per dollar
"""

from typing import List, Dict
from tabulate import tabulate


class CalorieAnalyzer:
    def __init__(self, menu_items: List[Dict]):
        self.menu_items = menu_items
        self.analyzed_items = []

    def analyze(self):
        """Calculate calorie per dollar for all menu items"""
        self.analyzed_items = []

        for item in self.menu_items:
            name = item['name']
            price = item['price']
            calories = item['calories']

            if price > 0:
                cal_per_dollar = calories / price
            else:
                cal_per_dollar = 0

            self.analyzed_items.append({
                'name': name,
                'price': price,
                'calories': calories,
                'cal_per_dollar': cal_per_dollar
            })

        # Sort by calorie per dollar (descending)
        self.analyzed_items.sort(key=lambda x: x['cal_per_dollar'], reverse=True)

    def get_best_value_items(self, top_n: int = 10) -> List[Dict]:
        """Get the top N items with best calorie per dollar ratio"""
        return self.analyzed_items[:top_n]

    def get_worst_value_items(self, bottom_n: int = 5) -> List[Dict]:
        """Get the bottom N items with worst calorie per dollar ratio"""
        return self.analyzed_items[-bottom_n:]

    def get_items_by_category(self, min_price: float = None, max_price: float = None,
                              min_calories: int = None, max_calories: int = None) -> List[Dict]:
        """Filter items by price and calorie ranges"""
        filtered = self.analyzed_items

        if min_price is not None:
            filtered = [item for item in filtered if item['price'] >= min_price]
        if max_price is not None:
            filtered = [item for item in filtered if item['price'] <= max_price]
        if min_calories is not None:
            filtered = [item for item in filtered if item['calories'] >= min_calories]
        if max_calories is not None:
            filtered = [item for item in filtered if item['calories'] <= max_calories]

        return filtered

    def get_statistics(self) -> Dict:
        """Calculate statistics about the menu"""
        if not self.analyzed_items:
            return {}

        prices = [item['price'] for item in self.analyzed_items]
        calories = [item['calories'] for item in self.analyzed_items]
        cal_per_dollar = [item['cal_per_dollar'] for item in self.analyzed_items]

        return {
            'total_items': len(self.analyzed_items),
            'avg_price': sum(prices) / len(prices),
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_calories': sum(calories) / len(calories),
            'min_calories': min(calories),
            'max_calories': max(calories),
            'avg_cal_per_dollar': sum(cal_per_dollar) / len(cal_per_dollar),
            'best_value': max(cal_per_dollar),
            'worst_value': min(cal_per_dollar)
        }

    def print_report(self, top_n: int = 10):
        """Print a formatted report of the analysis"""
        if not self.analyzed_items:
            print("No items to analyze!")
            return

        print("\n" + "=" * 80)
        print("CAFE CALORIE PER DOLLAR ANALYSIS REPORT")
        print("=" * 80)

        # Statistics
        stats = self.get_statistics()
        print("\nMENU STATISTICS:")
        print(f"  Total Items: {stats['total_items']}")
        print(f"  Price Range: ${stats['min_price']:.2f} - ${stats['max_price']:.2f} (avg: ${stats['avg_price']:.2f})")
        print(f"  Calorie Range: {stats['min_calories']} - {stats['max_calories']} (avg: {stats['avg_calories']:.0f})")
        print(f"  Cal/$ Range: {stats['worst_value']:.1f} - {stats['best_value']:.1f} (avg: {stats['avg_cal_per_dollar']:.1f})")

        # Best value items
        print(f"\n{'-' * 80}")
        print(f"TOP {top_n} BEST VALUE ITEMS (Most Calories Per Dollar)")
        print('-' * 80)

        best_items = self.get_best_value_items(top_n)
        table_data = []
        for i, item in enumerate(best_items, 1):
            table_data.append([
                i,
                item['name'][:40],  # Truncate long names
                f"${item['price']:.2f}",
                item['calories'],
                f"{item['cal_per_dollar']:.1f}"
            ])

        headers = ["Rank", "Item Name", "Price", "Calories", "Cal/$"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # Worst value items
        print(f"\n{'-' * 80}")
        print("5 WORST VALUE ITEMS (Least Calories Per Dollar)")
        print('-' * 80)

        worst_items = self.get_worst_value_items(5)
        table_data = []
        for item in worst_items:
            table_data.append([
                item['name'][:40],
                f"${item['price']:.2f}",
                item['calories'],
                f"{item['cal_per_dollar']:.1f}"
            ])

        headers = ["Item Name", "Price", "Calories", "Cal/$"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        print("\n" + "=" * 80)

    def export_to_csv(self, filepath: str):
        """Export analysis results to CSV"""
        import csv
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'price', 'calories', 'cal_per_dollar'])
            writer.writeheader()
            writer.writerows(self.analyzed_items)
        print(f"Analysis exported to {filepath}")

    def export_to_json(self, filepath: str):
        """Export analysis results to JSON"""
        import json
        with open(filepath, 'w') as f:
            json.dump({
                'statistics': self.get_statistics(),
                'items': self.analyzed_items
            }, f, indent=2)
        print(f"Analysis exported to {filepath}")
