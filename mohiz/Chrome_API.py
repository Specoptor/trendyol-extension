import csv
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
import re

app = Flask(__name__)

# Function to scrape image links using Selenium and BeautifulSoup
def get_barcode(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag that contains the barcode information
        script_tag = soup.find('script', string=re.compile('window.__PRODUCT_DETAIL_APP_INITIAL_STATE__'))

        if script_tag:
            # Use regular expressions to extract the barcode information
            match = re.search(r'"barcode":"(\d+)"', script_tag.string)

            if match:
                barcode = match.group(1)
                return barcode
    except Exception as e:
        print(f"Error retrieving barcode for {url}: {str(e)}")

    return None

def scrape_image_links(url):
    driver = None  # Initialize 'driver' to None
    try:
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('-headless')

        driver = webdriver.Firefox(options=firefox_options)

        driver.get(url)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all <img> tags within the <div> elements with class 'gallery-container'
        img_tags = soup.select('div.gallery-container img[src]')
        image_links = [img['src'] for img in img_tags]

        return image_links
    except Exception as e:
        return []
    finally:
        if driver is not None:
            driver.quit()

def get_brand_and_title(soup):
    # Implement the brand and title scraping logic here
    try:
        brand_and_title_element = soup.find(class_='pr-new-br')
        brand_and_title = brand_and_title_element.get_text()
        return brand_and_title
    except:
        return None

def get_price(soup):
    # Implement the price scraping logic here
    try:
        price_element = soup.find(class_='prc-dsc')
        price = price_element.get_text()
        return price
    except:
        return None

def get_attributes(soup):
    # Implement the attributes scraping logic here
    attr = soup.find_all('li', class_='detail-attr-item')
    attributes_dict = {}

    for element in attr:
        span_elements = element.find_all('span')

        if len(span_elements) == 2:
            text_values = [item.get_text(strip=True) for item in span_elements]

            if len(text_values) == 2:
                key, value = text_values
                attributes_dict[key] = value

    return attributes_dict

def get_description(soup):
    # Implement the description scraping logic here
    try:
        description_list_element = soup.find(class_='detail-desc-list')
        description = description_list_element.get_text()
        return description
    except:
        return None

@app.route('/scrape', methods=['POST'])
def scrape_product_details():
    try:
        data = request.json
        urls_to_scrape = data.get('urls')

        if not urls_to_scrape or not isinstance(urls_to_scrape, list):
            return jsonify({'ErrorCode': 400,
                            'ErrorMessage': 'Invalid request, Wrong Syntax and  Please provide a list of URLs in the JSON payload.'}), 400

        scraped_data = []

        for url_to_scrape in urls_to_scrape:
            try:
                response = requests.get(url_to_scrape)
                if response.status_code != 200:
                    return jsonify({'ErrorCode': 403,
                                    'ErrorMessage': f'Forbidden to scrap: {url_to_scrape}'}), 403

                soup = BeautifulSoup(response.text, 'html.parser')
                if soup.title.get_text() == 'trendyol.com':
                    return jsonify({'ErrorCode': 404, 'ErrorMessage': 'Request Not Found'}), 404

                image_links = scrape_image_links(url_to_scrape)

                product_details = {
                    'url': url_to_scrape,
                    'brand_and_title': get_brand_and_title(soup),
                    'price': get_price(soup),
                    'attributes': get_attributes(soup),
                    'images': image_links,
                    'description': get_description(soup),
                    'barcode': get_barcode(url_to_scrape)  # New line to get barcode
                }

                scraped_data.append(product_details)
            except Exception as e:
                return jsonify({'ErrorCode': 500, 'ErrorMessage': 'Internal server Error'}), 500

        payload_list_size = len(scraped_data)
        urls_found_count = len(urls_to_scrape)
        urls_scrapped_count = payload_list_size

        response_data = {
            'ErrorCode': 200,
            'ErrorMessage': 'CSV generated',
            'PayloadListSize': payload_list_size,
            'UrlsFoundCount': urls_found_count,
            'UrlsScrappedCount': urls_scrapped_count,
            'ScrappedProductsResponse': scraped_data
        }

        csv_filename = 'product_details.csv'
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['url', 'brand_and_title', 'price', 'attributes', 'images', 'description', 'barcode']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:
                writer.writeheader()
            for product_detail in scraped_data:
                writer.writerow(product_detail)

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)