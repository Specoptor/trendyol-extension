from flask import Flask, request, jsonify, send_file
from api_responses import generate_api_response

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


@app_with_scraper.route('/scrape-and-generate-csv', methods=['POST'])
def scrape_and_generate_csv():
    """
    This endpoint will scrape the provided URLs and generate a CSV file containing the scraped data if
    scraper response is success or partial success.

    It will return the csv file as an attachment if the response is success or partial success.
    It will return a json response with if the response is failure.
    :return:
    """
    urls = request.get_json().get("urls", [])
    response = generate_api_response(urls)
    if response.status == "SUCCESS":
        return send_file(response.data.attachment.filename, as_attachment=True)
    elif response.status == "PARTIAL_SUCCESS":
        return send_file(response.data.attachment.filename, as_attachment=True)
    else:
        return response.json()


@app_with_scraper.route('/scrape-and-send-filename', methods=['POST'])
def scrape_and_send_filename():
    """
    This endpoint will scrape the provided URLs and generate a CSV file containing the scraped data if
    scraper response is success or partial success.

    :return: a json response with the filename of the csv file
    """
    urls = request.get_json().get("urls", [])
    response = generate_api_response(urls)
    return response.json()


@app_with_scraper.route('/get-file/<path:path_to_file>', methods=['GET'])
def get_file(path_to_file):
    return send_file(path_to_file, as_attachment=True)


# Run the Flask app instance
if __name__ == '__main__':
    app_with_scraper.run(debug=True)
