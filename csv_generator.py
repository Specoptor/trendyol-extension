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
            writer.writerow(item)

        return output.getvalue()
