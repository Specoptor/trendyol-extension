import re
from bs4 import BeautifulSoup
import requests

url = "https://www.trendyol.com/tchibo/profesional-espresso-cekirdek-kahve-1kg-p-3990495?boutiqueId=620856&merchantId=547106"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Find the script tag that contains the barcode information
script_tag = soup.find('script', string=re.compile('window.__PRODUCT_DETAIL_APP_INITIAL_STATE__'))

if script_tag:
    # Use regular expressions to extract the barcode information
    match = re.search(r'"barcode":"(\d+)"', script_tag.string)

    if match:
        barcode = match.group(1)
        print("Barcode:", barcode)
    else:
        print("Barcode not found")
else:
    print("Script tag not found")
