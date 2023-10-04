import re
from typing import Any

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import logging

from trendyol_exceptions import ScrapingError, InvalidURLError, URLNotFoundError

logger = logging.Logger('scraper_logger')


def is_valid_trendyol_url(url: str) -> bool:
    """
    Validate if the given URL matches the typical Trendyol product page pattern.

    The function uses a regex pattern to validate URLs, ensuring they conform to:
    https://www.trendyol.com/brand-name/product-name-p-productid
    https://www.trendyol.com/product-name-p-productid

    This function specifically invalidates URLs that:
    - Are not on the domain www.trendyol.com.
    - Have 'en' or 'de' (English or German) product page paths.
    - Do not lead directly to a product page after trendyol.com.

    :param url: url to validate
    :return: true or false
    """

    pattern = r'^https://www\.trendyol\.com/[\w\-]+/[\w\-]+-p-\d+$'
    return bool(re.match(pattern, url))


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("log-level=3")
        self.driver = webdriver.Chrome(options=options)


class Scraper:
    def __init__(self):
        self.driver = Driver().driver

    def get_title(self) -> str or None:
        """ Get the brand and title of the product by first finding the brand and title element using the class name.

        :return: a string containing the brand and title of the product.
        """
        try:
            brand_and_title_element = self.driver.find_element(By.CLASS_NAME, 'pr-new-br')
            brand_and_title = brand_and_title_element.text
            return brand_and_title
        except NoSuchElementException:
            raise ScrapingError(data_point='title')

    def get_price(self) -> str or None:
        """ Get the price of the product by first finding the price element using the class name
         and then getting the text of the element.

        :return: a string containing the price of the product.
        """
        try:
            price_element = self.driver.find_element(By.CLASS_NAME, 'prc-dsc')
            price = price_element.text
            return price
        except NoSuchElementException:
            raise ScrapingError(data_point='price')

    def get_attributes(self) -> dict[str]:
        """
        Get the attributes of the product by first finding the attributes list element
        and then splitting the text and then pairing adjacent tokens as key-value pairs.

        :return: a dictionary containing the attributes of the product.
        """
        attributes = {}
        try:
            attributes_list_element = self.driver.find_element(By.CLASS_NAME, 'detail-attr-container')
            attributes_list = attributes_list_element.text
            # Split the text by lines and filter out any empty lines
            lines = [line.strip() for line in attributes_list.split('\n') if line.strip()]
            # Create a dictionary by taking pairs of lines as key-value pairs
            attributes = {lines[i]: lines[i + 1] for i in range(0, len(lines) - 1, 2)}
        except NoSuchElementException:
            pass
        return attributes

    def get_images(self) -> list[str]:
        """ Get the images of the product by first finding the main image and then finding the other images.

        :return: a list containing the images of the product.
        """
        images = []
        try:
            main_image = self.driver.find_element(By.CLASS_NAME, 'base-product-image').find_element(By.TAG_NAME,
                                                                                                    'img').get_attribute(
                'src')
            images.append(main_image)
            for other_image in self.driver.find_element(By.CLASS_NAME, 'styles-module_slider__o0fqa').find_elements(
                    By.TAG_NAME,
                    'img'):
                images.append(other_image.get_attribute('src'))
        except NoSuchElementException:
            pass
        return images

    def get_description(self) -> str | None:
        """ Get the description of the product by first finding the description list element
        and then iterating over the list items. Initialize an empty string and append the text of each list item
        to the string using a new line seperator.

        :return: a string containing the description of the product.
        """
        try:
            description_list_element = self.driver.find_element(By.CLASS_NAME, 'detail-desc-list')
            description = description_list_element.text
            return description
        except NoSuchElementException:
            return None

    def get_barcode(self) -> str or None:
        """ Get the barcode from a script tag via a regex match.
            Since barcode is mentioned in a script tag, we first find all script tags. Then, do a regex pattern match by
            scanning the text inside the particular script tag.
        :return: a string containing the barcode of the product or None if not found.
        """
        try:
            # Find the script tag that contains the barcode information
            script_tag = self.driver.find_element(By.XPATH, '/html/body/script[1]')
            content = script_tag.get_attribute('innerHTML')
            if 'window.__PRODUCT_DETAIL_APP_INITIAL_STATE__' in content:
                # Use regular expressions to extract the barcode information
                match = re.search(r'"barcode":"([a-zA-Z0-9]+)"', content)
                if match:
                    barcode = match.group(1)
                    return barcode
        except NoSuchElementException:
            pass

    def scrape_details(self, url) -> dict[str]:
        """ Scrape the product details using the scraper object.

        1. Check if the url is valid.
        2. Check if connection established.
        3. Check if the page exists
        4. Get the title, price, attributes, images, description and barcode of the product.
        5. Return a dictionary containing the product details.

        :return: a dictionary containing the product details
        """

        if not is_valid_trendyol_url(url):
            raise InvalidURLError()

        self.driver.get(url)
        if self.driver.title == 'trendyol.com':
            raise URLNotFoundError('URL not found.')

        return {
            'url': self.driver.current_url,
            'title': self.get_title(),
            'description': self.get_description(),
            'price': self.get_price(),
            'attributes': self.get_attributes(),
            'barcode': self.get_barcode(),
            'images': self.get_images()
        }

    def close(self):
        self.driver.quit()


def scrape_payload(url_list: list[str]) -> dict[str, list[Any]]:
    """
    Scrape the payload using the scraper object and classify urls into different categories.
    """
    processed_urls_dict = {
        'scraped': [],
        'invalid_urls': [],
        'connection_errors': [],
        'url_not_found_errors': [],
        'scraping_errors': []
    }

    scraper_obj = Scraper()
    for url in url_list:
        try:
            product_details = scraper_obj.scrape_details(url)
        except InvalidURLError:
            processed_urls_dict['invalid_urls'].append(url)
        except ConnectionError:
            processed_urls_dict['connection_errors'].append(url)
        except URLNotFoundError:
            processed_urls_dict['url_not_found_errors'].append(url)
        except ScrapingError:
            processed_urls_dict['scraping_errors'].append(url)
        else:
            processed_urls_dict['scraped'].append(product_details)

    scraper_obj.close()
    return processed_urls_dict
