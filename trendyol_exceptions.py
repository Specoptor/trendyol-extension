class BaseScrapingException(Exception):
    """Base class for all scraping related exceptions."""
    pass


class ConnectionError(BaseScrapingException):
    """Raised when there's a connection issue."""

    def __init__(self, message="Connection error occurred while trying to access the webpage."):
        self.message = message
        super().__init__(self.message)


class ScrapingError(BaseScrapingException):
    """Raised when an error occurs during scraping."""

    def __init__(self, data_point=None):
        if data_point:
            self.message = f"Failed to scrape the data point: {data_point}."
        else:
            self.message = "An unspecified scraping error occurred."
        super().__init__(self.message)


class InvalidURLError(BaseScrapingException):
    """Raised when a provided URL is invalid or doesn't match the expected pattern."""

    def __init__(self, message="Invalid URL or it doesn't match the expected pattern for a Turkish product webpage."):
        self.message = message
        super().__init__(self.message)


class InternalServerError(BaseScrapingException):
    """Raised when an unknown Exception Occurs."""

    def __init__(self, message="Internal server error."):
        self.message = message
        super().__init__(self.message)
