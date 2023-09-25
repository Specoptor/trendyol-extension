import csv
import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import logging

logger = logging.getLogger(__name__)

# Function to scrape image links using Selenium and BeautifulSoup
def scrape_image_links(url):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('-headless')

    driver = webdriver.Firefox(options=firefox_options)

    try:
        driver.get(url)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all <img> tags within the <div> elements with class 'gallery-container'
        img_tags = soup.select('div.gallery-container img[src]')
        image_links = [img['src'] for img in img_tags]

        return image_links
    finally:
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
        logger.critical(f'Error getting brand and title')
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

if __name__ == '__main__':
    print('This module will scrape and print product details including image links.')
    print('If the URL is not valid or the product is not available, an error message will be printed.')
    print('Type "quit" to exit the program.')

    while True:
        url_to_scrape = input('Enter the URL to scrape: ').strip()
        try:
            if url_to_scrape.lower().strip() == 'quit':
                exit()
            else:
                try:
                    response = requests.get(url_to_scrape)
                    if response.status_code != 200:
                        print('Error: Invalid URL or product not available')
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')
                    if soup.title.get_text() == 'trendyol.com':
                        print('Product is not available')
                        continue

                    # Call the function to get image links
                    image_links = scrape_image_links(url_to_scrape)

                    product_details = {
                        'url': url_to_scrape,
                        'brand_and_title': get_brand_and_title(soup),
                        'price': get_price(soup),
                        'attributes': get_attributes(soup),
                        'images': image_links,  # Use the fetched image links
                        'description': get_description(soup)
                    }

                    print('Product details: ')
                    pprint.pprint(product_details)

                    # Save product details to a CSV file
                    csv_filename = 'product_details.csv'
                    with open(csv_filename, 'a', newline='', encoding='utf-8') as csv_file:
                        fieldnames = ['url', 'brand_and_title', 'price', 'attributes', 'images', 'description']
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        # Write the header only once
                        if csv_file.tell() == 0:
                            writer.writeheader()
                        writer.writerow(product_details)

                    print(f'Product details saved to {csv_filename}')
                except:
                    print('Error occurred while scraping the URL')
        except TypeError or ValueError:
            print('Please enter a valid URL')