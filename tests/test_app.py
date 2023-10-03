from config import client, urls_10
from app import app_with_scraper

app_with_scraper.config['TESTING'] = True


def test_scrape_endpoint(client, urls_10):
    """
    Test that the scrape endpoint returns a list of products
    """
    # Mock data for testing
    mock_urls = {
        "urls": urls_10
    }
    response = client.post('/scrape', json=mock_urls)
    assert response.status_code == 200
    assert len(response.get_json()) == len(urls_10)


def test_generate_csv_endpoint(client, urls_10):
    """ Test that the generate-csv endpoint returns a CSV file """
    mock_urls = {
        "urls": urls_10
    }
    response = client.post('/generate-csv', json=mock_urls)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=products.csv'