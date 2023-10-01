import re

from selenium.webdriver.common.by import By
from driver import Driver
import logging

d = Driver()

logger = logging.Logger('scraper_logger')


def get_url(url):
    """ Get the URL using the driver object initialized at module level. This is to avoid initializing the driver
    everytime we want to scrape a URL.

    :param url: url to scrape
    """
    d.driver.get(url)


class Scraper:
    def __init__(self, d: Driver):
        self.driver = d.driver

    def get_title(self) -> str or None:
        """ Get the brand and title of the product by first finding the brand and title element using the class name.

        :return: a string containing the brand and title of the product.
        """
        try:
            brand_and_title_element = self.driver.find_element(By.CLASS_NAME, 'pr-new-br')
            brand_and_title = brand_and_title_element.text
            return brand_and_title
        except:
            logger.critical(f'Error getting brand and title: {self.driver.current_url}')
            return None

    # %%
    def get_price(self) -> str or None:
        """ Get the price of the product by first finding the price element using the class name
         and then getting the text of the element.

        :return: a string containing the price of the product.
        """
        try:
            price_element = self.driver.find_element(By.CLASS_NAME, 'prc-dsc')
            price = price_element.text
            return price
        except:
            logger.debug(f'Price not found: {self.driver.current_url}')
            return None

    # %%
    def get_attributes(self) -> dict[str]:
        """
        Get the attributes of the product by first finding the attributes list element
        and then splitting the text and then pairing adjacent tokens as key-value pairs.

        :return: a dictionary containing the attributes of the product.
        """
        attributes = {}
        try:
            attributes_list_element = self.driver.find_element(By.CLASS_NAME, 'detail-attr-container')
            for li in attributes_list_element.find_elements(By.TAG_NAME, 'li'):
                key, value = li.text.split('\n')
                attributes[key] = value
        except:
            logger.debug(f'Attributes not found: {self.driver.current_url}')
            pass
        finally:
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
        except:
            if not images:
                logger.debug(f'No images found: {self.driver.current_url}')
            else:
                logger.debug(f'Only main image found: {self.driver.current_url}')
        finally:
            return images

    def get_description(self) -> str:
        """ Get the description of the product by first finding the description list element
        and then iterating over the list items. Initialize an empty string and append the text of each list item
        to the string using a new line seperator.

        :return: a string containing the description of the product.
        """
        description = None
        try:
            description_list_element = self.driver.find_element(By.CLASS_NAME, 'detail-desc-list')
            description = description_list_element.text
        except:
            logger.debug(f'Description not found: {self.driver.current_url}')
        finally:
            return description

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
        except Exception as e:
            pass
        return None


def scrape_data(scraper: Scraper) -> dict[str]:
    """ Scrape the product details using the scraper object.

    :param scraper: a scraper object
    :return: a dictionary containing the product details
    """
    return {
        'url': scraper.driver.current_url,
        'title': scraper.get_title(),
        'description': scraper.get_description(),
        'price': scraper.get_price(),
        'attributes': scraper.get_attributes(),
        'barcode': scraper.get_barcode(),
        'images': scraper.get_images()
    }
