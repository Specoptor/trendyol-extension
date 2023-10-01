from flask import Flask, request, jsonify

from scraper import Scraper
import csv
from io import StringIO

# Create a new Flask app instance and define the /scrape endpoint with the integrated scraper functionality

app_with_scraper = Flask(__name__)


@app_with_scraper.route('/scrape', methods=['POST'])
def scrape_with_scraper():
    data = request.get_json()
    urls = data.get("urls", [])

    scraper = Scraper()
    results = []
    for url in urls:
        product_details = scraper.scrape_details(url)
        results.append(product_details)
    scraper.close()

    return jsonify(results), 200


@app_with_scraper.route('/generate-csv', methods=['POST'])
def generate_csv():
    # Retrieve data
    data = request.get_json()
    urls = data.get("urls", [])

    scraper = Scraper()
    scraped_data = []
    for url in urls:
        product_details = scraper.scrape_details(url)
        scraped_data.append(product_details)
    scraper.close()

    # Convert data to CSV format
    output = StringIO()
    fieldnames = ['url', 'title', 'description', 'price', 'attributes', 'barcode', 'images']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in scraped_data:
        writer.writerow(row)

    # Set the correct headers for CSV response
    response = app_with_scraper.response_class(
        response=output.getvalue(),
        mimetype='text/csv'
    )
    response.headers['Content-Disposition'] = 'attachment; filename=products.csv'
    return response


"Endpoint '/generate-csv' implemented for generating and sending CSV as a response."

# Run the Flask app instance
if __name__ == '__main__':
    app_with_scraper.run(debug=True)
