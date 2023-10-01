# Update the test configuration for the new Flask app instance
import pytest

from concurrent_app import concurrent_app
from test_app import urls_250

concurrent_app.config['TESTING'] = True


# Updating the tests to use the new Flask app instance
@pytest.fixture
def concurrent_client():
    with concurrent_app.test_client() as client:
        yield client


def test_scrape_concurrent_endpoint_updated(concurrent_client, urls_250):
    # Use a subset of the URLs for brevity in testing
    mock_urls = {"urls": urls_250}

    response = concurrent_client.post('/scrape-concurrent', json=mock_urls)
    assert response.status_code == 200
    assert len(response.get_json()) == len(urls_250)


def test_generate_csv_concurrent_endpoint_updated(concurrent_client, urls_250):
    # Use a subset of the URLs for brevity in testing
    mock_urls = {"urls": urls_250}

    response = concurrent_client.post('/generate-csv-concurrent', json=mock_urls)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=products.csv'
    assert "url,title,description,price,attributes,barcode,images" in response.data.decode()  # Checking for CSV headers


def test_scrape_parallel_endpoint(concurrent_client, urls_250):
    # Use a subset of the URLs for brevity in testing
    mock_urls = {"urls": urls_250}

    response = concurrent_client.post('/scrape-parallel', json=mock_urls)
    assert response.status_code == 200
    assert len(response.get_json()) == len(urls_250)


def test_generate_csv_parallel_endpoint(concurrent_client, urls_250):
    # Use a subset of the URLs for brevity in testing
    mock_urls = {"urls": urls_250}

    response = concurrent_client.post('/generate-csv-parallel', json=mock_urls)
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=products_parallel.csv'
    assert "url,title,description,price,attributes,barcode,images" in response.data.decode()  # Checking for CSV headers
