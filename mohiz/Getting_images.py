# # import cProfile
# import pprint
# import pandas as pd
# from selenium.webdriver.common.by import By
# from selenium import webdriver
#
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# def get_brand_and_title(driver):
#     """
#     Get the brand and title of the product by first finding the brand and title element using the class name.
#     :param driver: driver with the product page loaded.
#     :return: a string containing the brand and title of the product.
#     """
#     try:
#         brand_and_title_element = driver.find_element(By.CLASS_NAME, 'pr-new-br')
#         brand_and_title = brand_and_title_element.text
#         return brand_and_title
#     except:
#         logger.critical(f'Error getting brand and title: {driver.current_url}')
#         return None
#
#
# # %%
# def get_price(driver):
#     """
#     Get the price of the product by first finding the price element using the class name
#      and then getting the text of the element.
#     :param driver: driver with the product page loaded.
#     :return: a string containing the price of the product.
#     """
#     try:
#         price_element = driver.find_element(By.CLASS_NAME, 'prc-dsc')
#         price = price_element.text
#         return price
#     except:
#         logger.debug(f'Price not found: {driver.current_url}')
#         return None
#
#
# # %%
# def get_attributes(driver):
#     """
#     Get the attributes of the product by first finding the attributes list element
#     and then splitting the text and then pairing adjacent tokens as key-value pairs.
#     :param driver: driver with the product page loaded.
#     :return: a dictionary containing the attributes of the product.
#     """
#     attributes = {}
#     try:
#         attributes_list_element = driver.find_element(By.CLASS_NAME, 'detail-attr-container')
#         for li in attributes_list_element.find_elements(By.TAG_NAME, 'li'):
#             key, value = li.text.split('\n')
#             attributes[key] = value
#     except:
#         logger.debug(f'Attributes not found: {driver.current_url}')
#         pass
#     finally:
#         return attributes
#
#
# def get_images(driver):
#     images = []
#     try:
#         main_image = driver.find_element(By.CLASS_NAME, 'base-product-image').find_element(By.TAG_NAME,
#                                                                                            'img').get_attribute('src')
#         images.append(main_image)
#         for other_image in driver.find_element(By.CLASS_NAME, 'styles-module_slider__o0fqa').find_elements(By.TAG_NAME,
#                                                                                                            'img'):
#             images.append(other_image.get_attribute('src'))
#     except:
#         if not images:
#             logger.debug(f'No images found: {driver.current_url}')
#         else:
#             logger.debug(f'Only main image found: {driver.current_url}')
#     finally:
#         return images
#
#
# def get_description(driver):
#     """
#     Get the description of the product by first finding the description list element and then iterating over the list items.
#     Initialize an empty string and append the text of each list item to the string using a new line seperator.
#     :param driver: driver with the product page loaded.
#     :return: a string containing the description of the product.
#     """
#     description = None
#     try:
#         description_list_element = driver.find_element(By.CLASS_NAME, 'detail-desc-list')
#         description = description_list_element.text
#     except:
#         logger.debug(f'Description not found: {driver.current_url}')
#     finally:
#         return description
#
#
# import os
#
#
# def get_unique_filename(base_filename):
#     """
#     Returns a unique filename based on the given base_filename by appending
#     a count before the file extension. If the base filename does not exist, it
#     will return the base_filename.
#     """
#     # Split the filename and its extension
#     name, ext = os.path.splitext(base_filename)
#     count = 1
#     while os.path.exists(base_filename):
#         base_filename = f"{name}_{count}{ext}"
#         count += 1
#     return base_filename
#
#
# if __name__ == '__main__':
#     print('This module will generate a csv file containing the product details')
#     print('if the url is not valid or the product is not available, an error message will be printed.')
#     print('The csv file will be saved in the same directory as this script.')
#     print('type in quit to exit the program.')
#
#     options = webdriver.FirefoxOptions()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--log-level=4')
#     driver = webdriver.Firefox(options=options)
#
#     while True:
#         url_to_scrape = input('Enter the url to scrape: ').strip()
#         try:
#             if url_to_scrape.lower().strip() == 'quit':
#                 driver.quit()
#                 exit()
#             else:
#                 try:
#                     driver.get(url_to_scrape)
#                     if driver.title == 'trendyol.com':
#                         print('product is not available')
#                         continue
#
#                     product_details = {
#                         'url': url_to_scrape,
#                         'brand_and_title': get_brand_and_title(driver),
#                         'price': get_price(driver),
#                         'attributes': get_attributes(driver),
#                         'images': get_images(driver),
#                         'description': get_description(driver)
#                     }
#
#                     print('product details: ')
#                     pprint.pprint(product_details)
#                     df = pd.DataFrame([product_details])
#
#                 except:
#                     print('error occurred while scraping the url')
#                 else:
#                     try:
#                         filename = get_unique_filename('product_details.csv')
#                         df.to_csv(filename)
#                         print(f'product details saved to {filename}')
#                     except:
#                         print('error occurred while saving the file')
#         except TypeError or ValueError:
#             print('please enter a valid url')
#
