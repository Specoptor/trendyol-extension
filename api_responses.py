import base64

from csv_generator import CSVGenerator
from models import ScraperResponseModel, DataModel, ProcessedUrlsDictModel, AttachmentModel
from scraper import scrape_payload


# Update the generate_api_response function to handle this change
def generate_api_response(url_list: list[str]) -> ScraperResponseModel:
    processed_data = scrape_payload(url_list)

    csv_generated = False
    attachment_data = None

    if not url_list:
        return ScraperResponseModel(
            status="FAILURE",
            message="No URLs provided.",
            data=DataModel(processed_urls_dict=ProcessedUrlsDictModel(**processed_data))
        )

    if len(url_list) > 100:
        return ScraperResponseModel(
            status="FAILURE",
            message="More than allowable limit of 100 URLs provided.",
            data=DataModel(processed_urls_dict=ProcessedUrlsDictModel(**processed_data))
        )

    # If we have successfully scraped data, generate the CSV
    if processed_data['scraped']:
        csv_string = CSVGenerator.generate_csv_string_from_data(processed_data['scraped'])
        encoded_content = base64.b64encode(csv_string.encode()).decode('utf-8')
        attachment_data = AttachmentModel(filename="scraped_data.csv", content_type="text/csv", data=encoded_content)
        csv_generated = True

    if csv_generated and not any([processed_data['invalid_urls'], processed_data['connection_errors'], processed_data['scraping_errors'], processed_data['url_not_found_errors']]):
        return ScraperResponseModel(
            status="SUCCESS",
            message="All URLs scraped and CSV generated.",
            data=DataModel(attachment=attachment_data, processed_urls_dict=ProcessedUrlsDictModel(**processed_data))
        )

    if csv_generated:
        return ScraperResponseModel(
            status="PARTIAL_SUCCESS",
            message="Some URLs resulted in connection or scraping errors. CSV Generated containing the successfully scraped products.",
            data=DataModel(attachment=attachment_data, processed_urls_dict=ProcessedUrlsDictModel(**processed_data))
        )

    return ScraperResponseModel(
        status="FAILURE",
        message="Unable to generate the CSV file.",
        data=DataModel(processed_urls_dict=ProcessedUrlsDictModel(**processed_data))
    )