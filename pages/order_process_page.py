from time import sleep

from pages.base_page import BasePage
import re, os
import csv
import time
from datetime import datetime

class RTDPage(BasePage):
    def __init__(self, page):
        """Initialize with the Playwright page and define selectors."""
        super().__init__(page)

        # ============================
        # **Locators for Pagination*
        # ============================
        self.pagination_text_locator = ".pagignationRow .p-paginator-left-content"  # Locator for pagination text


        # ============================
        # **Export Table Locators**
        # ============================
        self.export_button_locator = "div.export-btn-outer.export-btn-dataTable:has-text('Export')"

    def wait_for_od_page_to_load(self):
        """Wait for the 'Ready To Dispatch' text to appear, confirming that the RTD page has loaded."""
        self.wait_for_element("span.w-max:text('Ready To Dispatch')", timeout=10000)

    def is_order_processes_visible(self):
        """Check if the 'Ready To Dispatch' text is visible on the page."""
        return self.is_visible("span.w-max:text('Ready To Dispatch')")


    def get_total_pages(self):
        """Retrieve the total number of pages from the pagination display text."""
        try:
            # Find the pagination element that shows the total pages (e.g., "Showing 1 to 10 of 119 entries")
            pagination_text = self.page.locator(self.pagination_text_locator).text_content()  # Locator for the pagination text
            print(f"Pagination text: {pagination_text}")

            # Extract the total entries from the text, which is in the format "Showing 1 to 10 of 119 entries"
            total_entries = int(pagination_text.split('of')[1].split('entries')[0].strip())  # Extract total entries
            rows_per_page = 10  # Assuming there are 10 entries per page
            total_pages = (total_entries // rows_per_page) + (1 if total_entries % rows_per_page > 0 else 0)

            print(f"Total pages: {total_pages}")
            return total_pages

        except Exception as e:
            print(f"Error occurred while getting total pages: {e}")
            raise

    def click_export_button(self):
        """Click the Export button."""
        self.page.wait_for_selector(self.export_button_locator, timeout=10000)
        self.page.click(self.export_button_locator)
        print("Export button clicked.")

    def download_report(self, download_dir):
        """Trigger the export action and handle the download."""
        with self.page.expect_download() as download_info:
            # Click the export button to initiate the download
            self.click_export_button()

        # Get the download object
        download = download_info.value

        # Define the file path for the downloaded file
        downloaded_file_path = os.path.join(download_dir, download.suggested_filename)

        # Save the downloaded file
        download.save_as(downloaded_file_path)

        print(f"File downloaded to: {downloaded_file_path}")
        return downloaded_file_path

    def verify_csv_data(self, downloaded_file_path):
        """Verify the CSV data after downloading."""
        # Ensure the file exists
        assert os.path.exists(downloaded_file_path), f"File not found: {downloaded_file_path}"

        # Open and verify the CSV file
        with open(downloaded_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            print(f"CSV Headers: {headers}")

            # You can modify the expected headers based on the actual CSV structure
            expected_headers = ["Order ID", "Customer", "Amount", "Date"]  # Example headers
            assert headers == expected_headers, f"Headers do not match. Expected {expected_headers}, but got {headers}"

            # Additional data validation (optional)
            for row in csv_reader:
                print(f"CSV Row: {row}")
                try:
                    amount = float(row[2])  # Assuming 'Amount' is at index 2
                    assert amount > 0, f"Invalid amount {amount} found in row {row}"
                except ValueError:
                    assert False, f"Invalid data in 'Amount' column for row {row}"

        print("✅ CSV verification completed successfully!")
