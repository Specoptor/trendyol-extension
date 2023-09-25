import csv
# import pprint
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
# import logging

from Getting_images import logger

app = Flask(__name__)

# Function to scrape image links using Selenium and BeautifulSoup
def scrape_image_links(url):
    '''This function scrap imges links from the products.
        It uses Selenium to navigate to the slidebar and Beautiful soup to extract all the images link from
        src attribute of image element in a div. '''
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
        logger.error(f"Error while scraping image links: {str(e)}")
        raise e
    finally:
        if driver is not None:
            driver.quit()
def get_brand_and_title(soup):
    """
       Get the brand and title of the product from the BeautifulSoup object.
       :param soup: BeautifulSoup object representing the product page.
       :return: a string containing the brand and title of the product.
       """
    try:
        brand_and_title_element = soup.find(class_='pr-new-br')
        brand_and_title = brand_and_title_element.get_text()
        return brand_and_title
    except:
        logger.error(f'Error getting brand and title')
        return None


def get_price(soup):

    """
       Get the price of the product from the BeautifulSoup object.
       :param soup: BeautifulSoup object representing the product page.
       :return: a string containing the price of the product.
       """
    try:
        price_element = soup.find(class_='prc-dsc')
        price = price_element.get_text()
        return price
    except:
        logger.debug(f'Price not found')
        return None


def get_attributes(soup):
    """
       Get the attributes of the product from the BeautifulSoup object.
       :param soup: BeautifulSoup object representing the product page.
       :return: a dictionary containing the attributes of the product.
       """
    attr = soup.find_all('li', class_='detail-attr-item')


    attributes_dict = {}

    for element in attr:
        # Find all the text within the <span> elements and remove leading/trailing whitespace
        span_elements = element.find_all('span')

        if len(span_elements) == 2:
            text_values = [item.get_text(strip=True) for item in span_elements]

            # Check if there are exactly two text values (key and value)
            if len(text_values) == 2:
                key, value = text_values
                attributes_dict[key] = value

    return attributes_dict  # Return the attributes dictionary

def get_description(soup):

    """
       Get the description of the product from the BeautifulSoup object.
       :param soup: BeautifulSoup object representing the product page.
       :return: a string containing the description of the product.
       """
    description = None
    try:
        description_list_element = soup.find(class_='detail-desc-list')
        description = description_list_element.get_text()
    except:
        logger.debug(f'Description not found')
    return description

@app.route('/scrape', methods=['POST'])
def scrape_product_details():
    try:
        data = request.json
        urls_to_scrape = data.get('urls')

        if not urls_to_scrape or not isinstance(urls_to_scrape, list):
            return jsonify({'ErrorCode': 400,
                            'ErrorMessage': 'Invalid request, Wrong Syntax and  Please provide a list of URLs in the JSON payload.'}), 400

        scraped_data = []  # Initialize a list to store scraped data

        for url_to_scrape in urls_to_scrape:
            try:
                response = requests.get(url_to_scrape)
                if response.status_code != 200:
                    return jsonify({'ErrorCode': 403,
                                    'ErrorMessage': f'Forbidden to scrap: {url_to_scrape}'}), 403

                soup = BeautifulSoup(response.text, 'html.parser')
                if soup.title.get_text() == 'trendyol.com':
                    return jsonify({'ErrorCode': 404, 'ErrorMessage': 'Request Not Found'}), 404

                # Call the function to get image links
                image_links = scrape_image_links(url_to_scrape)

                product_details = {
                    'url': url_to_scrape,
                    'brand_and_title': get_brand_and_title(soup),
                    'price': get_price(soup),
                    'attributes': get_attributes(soup),
                    'images': image_links,
                    'description': get_description(soup)
                }

                scraped_data.append(product_details)  # Add scraped data to the list
            except Exception as e:
                return jsonify({'ErrorCode': 500, 'ErrorMessage': 'Internal server Error'}), 500

        # Calculate additional parameters
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

        # Save product details to a CSV file for all URLs
        csv_filename = 'product_details.csv'
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['url', 'brand_and_title', 'price', 'attributes', 'images', 'description']
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
