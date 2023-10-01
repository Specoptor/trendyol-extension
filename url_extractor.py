import os

import requests
from xml.etree import ElementTree as ET


def extract_turkish_product_urls_from_sitemap(max_sitemaps_count=243, max_urls_count=9000000):
    """ Get the Product links from the sitemap. Include only turkish products.

    Iterate over a list of turkish product sitemaps and extract the product links.
    The sitemaps are numbered from 1 to 243.
    Each sitemap is an xml file containing around 400,000 product links.
    The total number of product links is ~8.5M.

    :param max_urls_count: max urls to scrape: default is set to 9M
    :param max_sitemaps_count: max sitemaps to scrape. Maximum is 243

    :return: a dictionary containing a list of product links. key is 'urls'.
    """
    if max_sitemaps_count > 243:
        max_sitemaps_count = 243
    links = []
    for counter in range(1, max_sitemaps_count + 1):
        target_link = f'https://www.trendyol.com/sitemap_products{counter}.xml'
        response = requests.get(target_link)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for child in root:
                links.append(child[0].text)
                if len(links) >= max_urls_count:
                    break

    # Return links in the desired JSON format
    return {"urls": links}


def save_urls_to_file(urls_to_save):
    """
    Save the product links to a file by reading in a dictionary containing the links as value of key 'urls'
    :return: None
    """
    result = extract_turkish_product_urls_from_sitemap(max_urls_count=urls_to_save)
    with open('urls.txt', 'w') as f:
        for url in result['urls']:
            f.write(url + '\n')


def load_urls_from_file():
    """
    Load the product links from a file
    :return: a dictionary of product links with key 'urls'
    """
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines()]
    return {'urls': urls}


def get_urls(sample_size=250):
    """
    Get the product links from a file if it exists, otherwise save the links to a file and then return the links.
    :param sample_size: number of links to return. Max is 252 for now.
    :return: a dictionary of product links with key 'urls'
    """

    if not os.path.exists('urls.txt'):
        save_urls_to_file(urls_to_save=sample_size)
    return {'urls': load_urls_from_file()['urls'][:sample_size]}


if __name__ == '__main__':
    save_urls_to_file(urls_to_save=10)
