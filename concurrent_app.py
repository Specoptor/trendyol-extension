# Redefine the Flask app instance and integrate the updated concurrent logic
import csv
import threading
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from multiprocessing import Pool, cpu_count

from flask import Flask, request, jsonify

from scraper import Scraper

concurrent_app = Flask(__name__)


# Thread-safe list to store results from multiple threads
class ThreadSafeList:
    def __init__(self):
        self.lock = threading.Lock()
        self.list = []

    def append(self, item):
        with self.lock:
            self.list.append(item)

    def get_list(self):
        with self.lock:
            return self.list.copy()


def threaded_scrape_with_executor(urls, scraper, results):
    """
    Scrape product details from multiple URLs concurrently using threads.

    :param urls: List of URLs to be scraped.
    :param scraper: (Scraper): Instance of the Scraper class.
    :param results: (ThreadSafeList) Thread-safe list to store the scraping results.
    :return: None: Results are stored in the provided results list.
    """

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scraper.scrape_details, url) for url in urls]
        for future in futures:
            results.append(future.result())


@concurrent_app.route('/scrape-concurrent', methods=['POST'])
def concurrent_scrape():
    """
    Endpoint to scrape product details from multiple URLs concurrently using threads.

    Request Payload:
    - JSON object containing a list of URLs under the key "urls".

    Returns:
    - JSON response containing the scraped product details for each provided URL.
    """
    data = request.get_json()
    urls = data.get("urls", [])

    scraper = Scraper()
    results = ThreadSafeList()

    # Use ThreadPoolExecutor for concurrent scraping
    threaded_scrape_with_executor(urls, scraper, results)

    scraper.close()

    return jsonify(results.get_list()), 200


@concurrent_app.route('/generate-csv-concurrent', methods=['POST'])
def concurrent_generate_csv():
    """
    Endpoint to scrape product details from multiple URLs concurrently using threads and return the results as a CSV.

    Request Payload:
    - JSON object containing a list of URLs under the key "urls".

    Returns:
    - CSV response containing the scraped product details for each provided URL.
    """
    data = request.get_json()
    urls = data.get("urls", [])

    scraper = Scraper()
    results = ThreadSafeList()

    # Use ThreadPoolExecutor for concurrent scraping
    threaded_scrape_with_executor(urls, scraper, results)

    # Convert data to CSV format
    output = StringIO()
    fieldnames = ['url', 'title', 'description', 'price', 'attributes', 'barcode', 'images']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in results.get_list():
        writer.writerow(row)

    scraper.close()

    # Set the correct headers for CSV response
    response = concurrent_app.response_class(
        response=output.getvalue(),
        mimetype='text/csv'
    )
    response.headers['Content-Disposition'] = 'attachment; filename=products.csv'
    return response


def parallel_scrape(url):
    """
    Function to scrape a single URL.
    This function will be executed in a separate process when using multiprocessing.

    Args:
    - url (str): URL to be scraped.

    Returns:
    - dict: Product details scraped from the URL.
    """
    scraper = Scraper()
    product_details = scraper.scrape_details(url)
    scraper.close()
    return product_details


@concurrent_app.route('/scrape-parallel', methods=['POST'])
def scrape_parallel():
    """
    Endpoint to scrape product details from multiple URLs using parallel processing.

    Request Payload:
    - JSON object containing a list of URLs under the key "urls".

    Returns:
    - JSON response containing the scraped product details for each provided URL.
    """
    data = request.get_json()
    urls = data.get("urls", [])

    # Use Pool for parallel processing
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(parallel_scrape, urls)

    return jsonify(results), 200


@concurrent_app.route('/generate-csv-parallel', methods=['POST'])
def generate_csv_parallel():
    """
    Endpoint to scrape product details from multiple URLs using parallel processing and return the results as a CSV.

    Request Payload:
    - JSON object containing a list of URLs under the key "urls".

    Returns:
    - CSV response containing the scraped product details for each provided URL.
    """
    data = request.get_json()
    urls = data.get("urls", [])

    # Use Pool for parallel processing
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(parallel_scrape, urls)

    # Convert data to CSV format
    output = StringIO()
    fieldnames = ['url', 'title', 'description', 'price', 'attributes', 'barcode', 'images']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

    # Set the correct headers for CSV response
    response = concurrent_app.response_class(
        response=output.getvalue(),
        mimetype='text/csv'
    )
    response.headers['Content-Disposition'] = 'attachment; filename=products_parallel.csv'
    return response


"Endpoints have been updated to use parallel processing for enhanced performance."
