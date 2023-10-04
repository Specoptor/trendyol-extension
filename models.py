from typing import List, Optional

from pydantic import Field, BaseModel, HttpUrl


# Redefining the models with the necessary imports

# 1. AttachmentModel: Represents details of the generated CSV containing scraped product data.
class AttachmentModel(BaseModel):
    filename: str = Field(description="The name of the generated CSV file.")
    content_type: str = Field(enum=["text/csv"], description="The MIME type of the CSV file.")
    data: str = Field(description="The actual CSV data encoded in base64 format.")


# 2. ProcessedUrlsDictModel: Represents a breakdown of URLs based on their processing status.
class ProcessedUrlsDictModel(BaseModel):
    scraped: List[dict] = Field(description="List of successfully scraped product details.")
    invalid_urls: List[HttpUrl] = Field(description="List of URLs deemed invalid.")
    connection_errors: List[HttpUrl] = Field(
        description="List of URLs that encountered connection errors during scraping.")
    scraping_errors: List[HttpUrl] = Field(
        description="List of URLs where scraping failed due to issues like CAPTCHAs or changed site structures.")
    url_not_found_errors: List[HttpUrl] = Field(description="List of URLs that returned 404 errors.")


# 3. DataModel: Contains the attachment and URL processing details.
class DataModel(BaseModel):
    attachment: Optional[AttachmentModel] = Field(
        description="Details of the generated CSV containing scraped product data.")
    processed_urls_dict: ProcessedUrlsDictModel = Field(
        description="A breakdown of URLs based on their processing status.")


# 4. ScraperResponseModel: The main response model.
class ScraperResponseModel(BaseModel):
    status: str = Field(enum=["SUCCESS", "PARTIAL_SUCCESS", "FAILURE"],
                        description="The overall status of the request processing.")
    message: str = Field(description="A descriptive message providing additional details about the processing outcome.")
    data: DataModel = Field(description="Contains the CSV attachment and URL processing details if applicable.")
