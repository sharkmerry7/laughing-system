"""
Flask web application for Cafe Calorie Per Dollar Analyzer
Provides a web interface to view and analyze menu items
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from analyzer import CalorieAnalyzer
from scraper import MenuScraper, load_from_json, save_to_json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global storage for current menu data
current_menu = None
current_analyzer = None


def load_example_data():
    """Load the example menu data"""
    global current_menu, current_analyzer
    try:
        if os.path.exists('example_menu.json'):
            current_menu = load_from_json('example_menu.json')
            current_analyzer = CalorieAnalyzer(current_menu)
            current_analyzer.analyze()
            return True
    except Exception as e:
        print(f"Error loading example data: {e}")
    return False


# Load example data on startup
load_example_data()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/analyze')
def analyze():
    """Display analysis results"""
    if current_analyzer is None or not current_analyzer.analyzed_items:
        return redirect(url_for('index'))

    stats = current_analyzer.get_statistics()
    best_items = current_analyzer.get_best_value_items(10)
    worst_items = current_analyzer.get_worst_value_items(5)
    all_items = current_analyzer.analyzed_items

    return render_template('analyze.html',
                         stats=stats,
                         best_items=best_items,
                         worst_items=worst_items,
                         all_items=all_items)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload menu data"""
    if request.method == 'POST':
        global current_menu, current_analyzer

        # Check if JSON data was posted
        if request.is_json:
            try:
                menu_data = request.get_json()
                current_menu = menu_data
                current_analyzer = CalorieAnalyzer(current_menu)
                current_analyzer.analyze()
                return jsonify({'success': True, 'items': len(current_menu)})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400

        # Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400

            try:
                content = file.read().decode('utf-8')
                menu_data = json.loads(content)
                current_menu = menu_data
                current_analyzer = CalorieAnalyzer(current_menu)
                current_analyzer.analyze()
                return redirect(url_for('analyze'))
            except Exception as e:
                return jsonify({'success': False, 'error': f'Error processing file: {str(e)}'}), 400

    return render_template('upload.html')


@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    """Scrape menu from URL"""
    if request.method == 'POST':
        global current_menu, current_analyzer

        url = request.form.get('url')
        use_selenium = request.form.get('use_selenium') == 'on'

        if not url:
            return render_template('scrape.html', error='Please provide a URL')

        try:
            scraper = MenuScraper(url)
            menu_data = scraper.scrape(use_selenium=use_selenium)

            if menu_data and len(menu_data) > 0:
                current_menu = menu_data
                current_analyzer = CalorieAnalyzer(current_menu)
                current_analyzer.analyze()
                return redirect(url_for('analyze'))
            else:
                return render_template('scrape.html',
                                     error='Failed to scrape menu items. The site may have bot protection.')
        except Exception as e:
            return render_template('scrape.html', error=f'Error: {str(e)}')

    return render_template('scrape.html')


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    if current_analyzer is None:
        return jsonify({'error': 'No data loaded'}), 404

    return jsonify(current_analyzer.get_statistics())


@app.route('/api/items')
def api_items():
    """API endpoint for all analyzed items"""
    if current_analyzer is None:
        return jsonify({'error': 'No data loaded'}), 404

    return jsonify(current_analyzer.analyzed_items)


@app.route('/api/best/<int:count>')
def api_best(count):
    """API endpoint for best value items"""
    if current_analyzer is None:
        return jsonify({'error': 'No data loaded'}), 404

    return jsonify(current_analyzer.get_best_value_items(count))


@app.route('/filter')
def filter_items():
    """Filter items by criteria"""
    if current_analyzer is None:
        return redirect(url_for('index'))

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_calories = request.args.get('min_calories', type=int)
    max_calories = request.args.get('max_calories', type=int)

    filtered = current_analyzer.get_items_by_category(
        min_price=min_price,
        max_price=max_price,
        min_calories=min_calories,
        max_calories=max_calories
    )

    # Calculate stats for filtered items
    if filtered:
        prices = [item['price'] for item in filtered]
        calories = [item['calories'] for item in filtered]
        cal_per_dollar = [item['cal_per_dollar'] for item in filtered]

        stats = {
            'total_items': len(filtered),
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
    else:
        stats = {}

    return render_template('analyze.html',
                         stats=stats,
                         best_items=filtered[:10] if filtered else [],
                         worst_items=filtered[-5:] if filtered and len(filtered) > 5 else [],
                         all_items=filtered,
                         filters={
                             'min_price': min_price,
                             'max_price': max_price,
                             'min_calories': min_calories,
                             'max_calories': max_calories
                         })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Cafe Calorie Per Dollar Analyzer - Web Interface")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
