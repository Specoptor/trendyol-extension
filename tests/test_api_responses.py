from config import urls_10, all_kinds_of_urls

from api_responses import generate_api_response


def test_generate_api_responses_success(urls_10):
    response = generate_api_response(urls_10)
    assert response.status == "SUCCESS"
    assert response.message == "All URLs scraped and CSV generated."
    assert "scraped_data" in response.data.attachment.filename
    assert response.data.attachment.content_type == "text/csv"
    assert response.data.attachment.data is not None
    for data in response.data.processed_urls_dict.scraped:
        assert data['url'] in urls_10
    assert response.data.processed_urls_dict.invalid_urls == []
    assert response.data.processed_urls_dict.connection_errors == []
    assert response.data.processed_urls_dict.scraping_errors == []
    assert response.data.processed_urls_dict.url_not_found_errors == []


def test_generate_api_response_partial_success(all_kinds_of_urls):
    urls = all_kinds_of_urls['scraped'] + all_kinds_of_urls['invalid_urls'] + \
           all_kinds_of_urls['connection_errors'] + all_kinds_of_urls['scraping_errors'] + \
           all_kinds_of_urls['url_not_found_errors']

    response = generate_api_response(urls)
    assert response.status == "PARTIAL_SUCCESS"
    assert response.message == "Some URLs resulted in connection or scraping errors. CSV Generated containing the successfully scraped products."
    assert 'scraped_data' in response.data.attachment.filename
    assert response.data.attachment.content_type == "text/csv"
    assert response.data.attachment.data is not None
    for data in response.data.processed_urls_dict.scraped:
        assert data['url'] in all_kinds_of_urls['scraped']
    assert response.data.processed_urls_dict.invalid_urls == all_kinds_of_urls['invalid_urls']
    assert response.data.processed_urls_dict.connection_errors == all_kinds_of_urls['connection_errors']
    assert response.data.processed_urls_dict.scraping_errors == all_kinds_of_urls['scraping_errors']
    assert response.data.processed_urls_dict.url_not_found_errors == all_kinds_of_urls['url_not_found_errors']
