import json

from app import app_with_scraper
import pytest

app_with_scraper.config['TESTING'] = True


@pytest.fixture
def client():
    with app_with_scraper.test_client() as client:
        yield client


@pytest.fixture
def trendyol_urls():
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


@pytest.fixture
def urls_250():
    with open('files/urls_250.json', 'r') as f:
        urls = json.load(f)
        return urls


def test_scrape_endpoint(client, trendyol_urls):
    """
    Test that the scrape endpoint returns a list of products
    """
    # Mock data for testing
    mock_urls = {
        "urls": trendyol_urls
    }
    response = client.post('/scrape', json=mock_urls)
    assert response.status_code == 200
    assert len(response.get_json()) == len(trendyol_urls)


def test_generate_csv_endpoint(client, trendyol_urls):
    """ Test that the generate-csv endpoint returns a CSV file """
    mock_urls = {
        "urls": trendyol_urls
    }
    response = client.post('/generate-csv', json=mock_urls)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=products.csv'