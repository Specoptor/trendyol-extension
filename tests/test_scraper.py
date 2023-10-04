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


def test_scrape_payload():
    """ Test that the payload is scraped correctly for a sample of selective sample """

    # urls to test
    test_urls = ['https://www.trendyol.com/sail-lakers/beyaz-deri-bagcikli-erkek-gunluk-ayakkabi-p-366825717',
                 'https://www.trendyol.com/trendshopping/iphone-13-kose-korumali-antik-deri-telefon-kilifi-lacivert-p-348328113',
                 'https://www.trendyol.com/',
                 'https://www.trendyol.com/seher-yildizi/100-pamuk-gri-renk-5-adet-erkek-slip-kulot-yeni-sezon-p-73300907',
                 'https://www.trendyol.com/astra-market/protez-dis-saklama-kabi-p-732116228'
                 ]

    processed_urls_dict = scraper.scrape_payload(test_urls)

    # assert size of urls
    assert len(processed_urls_dict['scraped']) == 2
    assert len(processed_urls_dict['invalid_urls']) == 1
    assert len(processed_urls_dict['connection_errors']) == 0
    assert len(processed_urls_dict['url_not_found_errors']) == 1
    assert len(processed_urls_dict['scraping_errors']) == 1

    # assert scraped urls
    scraped_urls = [product['url'] for product in processed_urls_dict['scraped']]
    assert 'https://www.trendyol.com/sail-lakers/beyaz-deri-bagcikli-erkek-gunluk-ayakkabi-p-366825717' in scraped_urls
    assert 'https://www.trendyol.com/trendshopping/iphone-13-kose-korumali-antik-deri-telefon-kilifi-lacivert-p-348328113' in scraped_urls

    # assert non-scraped urls
    assert processed_urls_dict['invalid_urls'] == ['https://www.trendyol.com/']
    assert processed_urls_dict['url_not_found_errors'] == [
        'https://www.trendyol.com/seher-yildizi/100-pamuk-gri-renk-5-adet-erkek-slip-kulot-yeni-sezon-p-73300907']
    assert processed_urls_dict['scraping_errors'] == [
        'https://www.trendyol.com/astra-market/protez-dis-saklama-kabi-p-732116228']
