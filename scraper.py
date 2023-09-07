from selenium.webdriver.common.by import By
from driver import Driver
import logging

d = Driver()

logger = logging.Logger('scraper_logger')


def get_url(url):
    d.driver.get(url)


class Scraper:
    def __init__(self, d: Driver):
        self.driver = d.driver

    def get_title(self):
        """
        Get the brand and title of the product by first finding the brand and title element using the class name.
        :param driver: driver with the product page loaded.
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
    def get_price(self):
        """
        Get the price of the product by first finding the price element using the class name
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
    def get_attributes(self):
        """
        Get the attributes of the product by first finding the attributes list element
        and then splitting the text and then pairing adjacent tokens as key-value pairs.
        :param driver: driver with the product page loaded.
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

    def get_images(self):
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

    def get_description(self):
        """
        Get the description of the product by first finding the description list element and then iterating over the list items.
        Initialize an empty string and append the text of each list item to the string using a new line seperator.
        :param driver: driver with the product page loaded.
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

    def get_barcode(self):
        pass


def scrape_data(scraper: Scraper) -> dict[str]:
    return {
        'url': scraper.driver.current_url,
        'title': scraper.get_title(),
        'description': scraper.get_description(),
        'price': scraper.get_price(),
        'attributes': scraper.get_attributes(),
        'barcode': scraper.get_barcode(),
        'images': scraper.get_images()
    }
