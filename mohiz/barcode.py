# from bs4 import BeautifulSoup
# import re
import requests
import xml.etree.ElementTree as ET
# import logging
import json

# url = "https://www.trendyol.com/tchibo/profesional-espresso-cekirdek-kahve-1kg-p-3990495?boutiqueId=620856&merchantId=547106"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
#
# # Find the script tag that contains the barcode information
# script_tag = soup.find('script', string=re.compile('window.__PRODUCT_DETAIL_APP_INITIAL_STATE__'))
#
# if script_tag:
#     # Use regular expressions to extract the barcode information
#     match = re.search(r'"barcode":"(\d+)"', script_tag.string)
#
#     if match:
#         barcode = match.group(1)
#         print("Barcode:", barcode)
#     else:
#         print("Barcode not found")
# else:
#     print("Script tag not found")

def get_links():
    """
    Get the Product links from the sitemap.
    Include only English-based urls.
    :return: a list containing product links.
    """
    links = []
    for counter in range(1, 7):
        target_link = f'https://www.trendyol.com/sitemap_products{counter}.xml'
        response = requests.get(target_link)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for child in root:
                links.append(child[0].text)
                if len(links) >= 100:
                    break
            if len(links) >= 100:
                break

    # Return links in the desired JSON format
    return {"urls": links}

# Call the function and print the links in JSON format
result = get_links()
print(json.dumps(result, indent=2))

