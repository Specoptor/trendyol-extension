from types import NoneType
from config import urls_10, urls_250
import scraper


def test_title(urls_10):
    """ Test that the title is not null for a sample of 10 products """
    scraper_obj = scraper.Scraper()
    for url in urls_10:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['title'], str)
    scraper_obj.close()


def test_price(urls_10):
    """ Test that the price is not null for a sample of 10 products """
    scraper_obj = scraper.Scraper()
    for url in urls_10:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['price'], str)
    scraper_obj.close()


def test_attributes(urls_10):
    """ Test that the attributes is not null for a sample of 10 products """
    scraper_obj = scraper.Scraper()
    for url in urls_10:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['attributes'], dict)
    scraper_obj.close()


def test_images(urls_10):
    """ Test that the images is not null for a sample of 10 products """
    urls = urls_10
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['images'], list)
    scraper_obj.close()


def test_description(urls_10):
    """ Test that the description is not null for a sample of 10 products """
    scraper_obj = scraper.Scraper()
    for url in urls_10:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['description'], str)
    scraper_obj.close()


def test_url(urls_10):
    """ Test that the url is not null for a sample of 10 products """
    scraper_obj = scraper.Scraper()
    for url in urls_10:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['url'], str)
    scraper_obj.close()


def test_barcode(urls_10):
    """ Test that the barcode is not null for a sample of 10 products """
    scraper_obj = scraper.Scraper()
    for url in urls_10:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['barcode'], (str, NoneType))
    scraper_obj.close()


def test_validate_actual_product_urls(urls_250):
    """ Test that the product urls are valid """
    for url in urls_250:
        assert scraper.is_valid_trendyol_url(url)


def test_invalidate_non_turkish_product_links():
    """
    Test that invalid urls, non-product page urls, and non-turkish product urls are invalidated.
    """
    invalid_url_list = [
        'https://www.trendyol.com/de/happiness-istanbul/dress-beige-shift-p-670197121?boutiqueId=48&merchantId=968&itemNumber=886692985',
        # german product
        'https://www.trendyol.com/en/olalook/blouse-pink-slim-fit-p-333500680',  # english product
        'https://www.google.com'  # not trendyol
        'https://www.trendyol.com'  # home page
    ]
    for url in invalid_url_list:
        assert not scraper.is_valid_trendyol_url(url)