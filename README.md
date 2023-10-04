# Trendyol Extension 

## This branch is responsible for implementing and generating 5 possible kinds of API Responses.

### 1. SUCCESS: All URLs scraped and CSV generated

**Conditions**:
- All URLs provided in the request were accessible.
- The scraping operation successfully retrieved product data from each URL.
- CSV generation operation executed without any errors and compiled the scraped data.

**Description**:
The system successfully processed each URL provided in the request, scraped the relevant product data, and then compiled this data into a CSV format without encountering any issues.

**Specifics**:
- `status`: `SUCCESS`
- `message`: "All URLs scraped and CSV generated."

**Sample Response**:
```json
{
    "status": "SUCCESS",
    "message": "All URLs scraped and CSV generated.",
    "data": {
        "attachment": {
            "filename": "products_data.csv",
            "content_type": "text/csv",
            "data": "Base64 encoded CSV data..."
        },
        "processed_urls_dict": {
            "scraped": ["http://valid-url1.com", "http://valid-url2.com"],
            "invalid_urls": [],
            "connection_errors": [],
            "scraping_errors": []
        }
    }
}
```

---

### 2. PARTIAL SUCCESS: Some URLs resulted in connection or scraping errors. CSV Generated containing the successfully scraped products.

**Conditions**:
- Some of the provided URLs were either inaccessible or resulted in scraping issues.
- The URLs that were successfully scraped had their product data retrieved.
- A CSV was generated containing only the products that were successfully scraped.

**Description**:
The system was able to scrape product data from some of the URLs provided in the request. However, certain URLs were either inaccessible or presented scraping difficulties. Despite these challenges, a CSV was generated for the URLs that were successfully scraped.

**Specifics**:
- `status`: `PARTIAL_SUCCESS`
- `message`: "Some URLs resulted in connection or scraping errors. CSV Generated containing the successfully scraped products."

**Sample Response**:
```json
{
    "status": "PARTIAL_SUCCESS",
    "message": "Some URLs resulted in connection or scraping errors. CSV Generated containing the successfully scraped products.",
    "data": {
        "attachment": {
            "filename": "partial_products_data.csv",
            "content_type": "text/csv",
            "data": "Base64 encoded CSV data for successful URLs..."
        },
        "processed_urls_dict": {
            "scraped": ["http://valid-url1.com"],
            "invalid_urls": ["http://invalid-url.com"],
            "connection_errors": ["http://connection-error-url.com"],
            "scraping_errors": ["http://scraping-error-url1.com"]
        }
    }
}
```

---

### 3. FAILURE: No URLs provided

**Conditions**:
- The request either did not contain a list of URLs or the list was empty.

**Description**:
The system expected a list of URLs to process, but the request did not provide any. As a result, no scraping or CSV generation operations were initiated.

**Specifics**:
- `status`: `FAILURE`
- `message`: "No URLs provided."

**Sample Response**:
```json
{
    "status": "FAILURE",
    "message": "No URLs provided.",
    "data": {
        "processed_urls_dict": {
            "scraped": [],
            "invalid_urls": [],
            "connection_errors": [],
            "scraping_errors": []
        }
    }
}
```

---

### 4. FAILURE: More than allowable limit of 100 URLs provided

**Conditions**:
- The request provided a list of URLs that exceeded the maximum allowable limit of 100.

**Description**:
The system can process a maximum of 100 URLs in a single request. The request provided more than this limit, and as a result, the system did not initiate the scraping or CSV generation operations.

**Specifics**:
- `status`: `FAILURE`
- `message`: "More than allowable limit of 100 URLs provided."

**Sample Response**:
```json
{
    "status": "FAILURE",
    "message": "More than allowable limit of 100 URLs provided.",
    "data": {
        "processed_urls_dict": {
            "scraped": [],
            "invalid_urls": [],
            "connection_errors": [],
            "scraping_errors": []
        }
    }
}
```

---

### 5. FAILURE: Unable to generate the CSV file

**Conditions**:
- Some or all of the URLs were successfully scraped.
- The CSV generation operation encountered an unexpected error and could not compile the scraped data.

**Description**:
The system successfully scraped product data from the URLs provided in the request but encountered an unexpected error during the CSV generation phase. As a result, the data could not be compiled into a CSV format.

**Specifics**:
- `status`: `FAILURE`
- `message`: "Unable to generate the CSV file."

**Sample Response**:
```json
{
    "status": "FAILURE",
    "message": "Unable to generate the CSV file.",
    "data": {
        "processed_urls_dict": {
            "scraped": ["http://valid-url1.com"],
            "invalid_urls": [],
            "connection_errors": [],
            "scraping_errors": ["http://scraping-error-url1.com"]
        }
    }
}
```
