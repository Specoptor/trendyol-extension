from config import urls_10

from api_responses import generate_api_response


def test_generate_api_responses_success(urls_10):
    response = generate_api_response(urls_10)
    assert response.status == "SUCCESS"
    assert response.message == "All URLs scraped and CSV generated."
    assert response.data.attachment.filename == "scraped_data.csv"
    assert response.data.attachment.content_type == "text/csv"
    assert response.data.attachment.data is not None
    for data in response.data.processed_urls_dict.scraped:
        assert data['url'] in urls_10
    assert response.data.processed_urls_dict.invalid_urls == []
    assert response.data.processed_urls_dict.connection_errors == []
    assert response.data.processed_urls_dict.scraping_errors == []
    assert response.data.processed_urls_dict.url_not_found_errors == []
