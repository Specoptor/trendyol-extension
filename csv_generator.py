import csv
from io import StringIO


class CSVGenerator:
    @staticmethod
    def generate_csv_string_from_data(data: list[dict[str, str | dict | list[str]]]):
        """
        Generate a CSV file from the scraped data.

        :param data: List of dictionaries containing the scraped product data.
        :return: CSV formatted string.
        """

        headers = ['url', 'title', 'description', 'price', 'attributes', 'barcode', 'images']

        output = StringIO()

        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow({k: str(v) for k, v in item.items()})

        return output.getvalue()


    @staticmethod
    def generate_csv_from_data(data: list[dict[str, str | dict | list[str]]], filename: str = "scraped_data.csv"):
        """
        Generate a CSV file from the provided scraped data.

        :param data: List of dictionaries containing the scraped product data.
        :param filename: Name of the output CSV file.

        :return: Path to the generated CSV file.
        """

        headers = ['url', 'title', 'description', 'price', 'attributes', 'barcode', 'images']

        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            for item in data:
                writer.writerow({k: str(v) for k, v in item.items()})

        return filename
