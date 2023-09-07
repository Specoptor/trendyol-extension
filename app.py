from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import scraper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Temporary list to store imported products
imported_products = []


@app.route('/')
def index():
    return 'welcome to the chrome extension backend'


@app.route('/import_product', methods=['POST'])
def import_product():
    url = request.json['url']
    if "trendyol.com" not in url:
        return jsonify({'error': 'Invalid URL'}), 400

    # Initialize Selenium WebDriver
    scraper.get_url(url)

    # scrape the product page using selenium
    scraped_data = scraper.Scraper(scraper.d)
    product_details = scraper.scrape_data(scraped_data)

    # Add the imported product to the list
    imported_products.append(product_details)

    # Close the Selenium driver
    scraper.d.close()

    return jsonify(product_details), 200


@app.route('/delete_product', methods=['POST'])
def delete_product():
    product_name = request.json['url']
    global imported_products
    imported_products = [product for product in imported_products if product['url'] != product_name]
    return jsonify({'message': f'Product {product_name} deleted successfully'}), 200


@app.route('/reset_list', methods=['GET'])
def reset_list():
    global imported_products
    imported_products.clear()
    return jsonify({'message': 'List reset successfully'}), 200


@app.route('/export_csv', methods=['GET'])
def export_csv():
    # Export the imported products to a CSV file
    with open('products.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Price'])
        for product in imported_products:
            writer.writerow([product['name'], product['price']])

    return jsonify({'message': 'CSV exported successfully'}), 200
