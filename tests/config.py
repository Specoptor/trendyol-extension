import json

import pytest

from app import app_with_scraper


@pytest.fixture
def client():
    with app_with_scraper.test_client() as client:
        yield client


@pytest.fixture
def urls_250():
    with open('files/urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines()]
        return urls[:250]


@pytest.fixture
def all_kinds_of_urls():
    with open('files/all_kinds_of_urls.json', 'r') as f:
        urls = json.load(f)
        return urls


@pytest.fixture
def urls_10():
    urls = [
        "https://www.trendyol.com/sail-lakers/beyaz-deri-bagcikli-erkek-gunluk-ayakkabi-p-366825717",
        "https://www.trendyol.com/gelincik/kahvaltilik-surulebilir-dogal-katkisiz-10kg-ozel-uretim-sekersiz-fistik-ezmesi-krem-p-234064644",
        "https://www.trendyol.com/zeyder-kids/kiz-bebek-baskili-t-shirt-p-731763902",
        "https://www.trendyol.com/nuclear/bubba-juice-10-ml-mix-aroma-kapruz-sakiz-p-731515507",
        "https://www.trendyol.com/midday/2-adet-evinize-somine-havasini-yasatacak-olan-dekoratif-5-watt-alev-gorunumlu-led-alevli-ampul-lamba-p-474594130",
        "https://www.trendyol.com/dk-tuning/tesla-model-3-s-x-orjinal-jant-gobek-kapagi-seti-57mm-gumus-renk-p-732527982",
        "https://www.trendyol.com/trendshopping/iphone-13-kose-korumali-antik-deri-telefon-kilifi-lacivert-p-348328113",
        "https://www.trendyol.com/opinel/inox-trekking-8-no-paslanmaz-celik-caki-p-378505993",
        "https://www.trendyol.com/victoria-s-secret/bej-rengi-kadin-kulot-victoria-s-secret-brazilian-kesim-bej-kadin-kulot-hediyelik-hediye-kulot-p-466727358",
        "https://www.trendyol.com/lema-store/3-yas-rakam-ve-20-adet-makaron-balon-sari-beyaz-p-656012721",
        "https://www.trendyol.com/bambi/vizon-suet-kadin-cizme-k03828030102-p-163949261"
    ]
    return urls
