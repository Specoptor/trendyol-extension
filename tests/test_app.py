# This is test_app.py

import json
import pytest
from app import app, imported_products  # import your app and your imported_products list


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_import_product(client):
    payload = {'url': 'https://www.trendyol.com/rise-and-shine/keratin-kolajen-sac-bakim-sutu-200-ml-p-174950884'}
    response = client.post('/import_product', json=payload)
    assert response.status_code == 200
    assert len(imported_products) == 1  # The list should contain one product now


def test_import_product_invalid_url(client):
    payload = {'url': 'https://invalid.com/some-product'}
    response = client.post('/import_product', json=payload)
    assert response.status_code == 400
    assert b'Invalid URL' in response.data


def test_delete_product(client):
    # First, add a product for testing deletion
    payload = {'url': 'https://www.trendyol.com/morfose/milk-therapy-fon-sutu-400-ml-p-4780060'}
    client.post('/import_product', json=payload)
    delete_payload = {'url': 'https://www.trendyol.com/morfose/milk-therapy-fon-sutu-400-ml-p-4780060'}
    response = client.post('/delete_product', json=delete_payload)
    assert response.status_code == 200
    # todo determine why the product is not deleted from the global list
    assert len(imported_products) == 0  # The list should be empty now


def test_reset_list(client):
    # First, add some products for testing reset
    payload1 = {'url': 'https://www.trendyol.com/rise-and-shine/keratin-kolajen-sac-bakim-sutu-200-ml-p-174950884'}
    payload2 = {'url': 'https://www.trendyol.com/morfose/milk-therapy-fon-sutu-400-ml-p-4780060'}
    client.post('/import_product', json=payload1)
    client.post('/import_product', json=payload2)

    response = client.get('/reset_list')
    assert response.status_code == 200
    assert len(imported_products) == 0  # The list should be empty now


def test_export_csv(client):
    # First, add some products for testing export
    payload1 = {'url': 'https://www.trendyol.com/morfose/milk-therapy-fon-sutu-400-ml-p-4780060'}
    payload2 = {'url': 'https://www.trendyol.com/rise-and-shine/keratin-kolajen-sac-bakim-sutu-200-ml-p-174950884'}
    client.post('/import_product', json=payload1)
    client.post('/import_product', json=payload2)

    response = client.get('/export_csv')
    assert response.status_code == 200
    assert b'CSV exported successfully' in response.data
