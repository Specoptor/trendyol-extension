from types import NoneType

import pytest
import random

import scraper  # driver initialized at module level


@pytest.fixture
def url_list():
    with open('files/urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines()]
        random.shuffle(urls)  # shuffle the list to randomize the order of urls
        return urls


def test_title(url_list):
    """ Test that the title is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['title'], str)
    scraper_obj.close()


def test_price(url_list):
    """ Test that the price is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['price'], str)
    scraper_obj.close()


def test_attributes(url_list):
    """ Test that the attributes is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['attributes'], dict)
    scraper_obj.close()


def test_images(url_list):
    """ Test that the images is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['images'], list)
    scraper_obj.close()


def test_description(url_list):
    """ Test that the description is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['description'], str)
    scraper_obj.close()


def test_url(url_list):
    """ Test that the url is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['url'], str)
    scraper_obj.close()


def test_barcode(url_list):
    """ Test that the barcode is not null for a sample of 10 products """
    urls = url_list[:10]
    scraper_obj = scraper.Scraper()
    for url in urls:
        product_details = scraper_obj.scrape_details(url)
        assert isinstance(product_details['barcode'], (str, NoneType))
    scraper_obj.close()
