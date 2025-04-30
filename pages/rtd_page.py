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
        # **Locators for Date Range Filters**
        # ============================

        # Date Picker and Related Elements
        self.date_picker_input = "input[name='from_date']"  # The input field for selecting date
        self.date_box = "div.datepicker-parent"  # Date picker box element
        self.date_picker_calendar = "//p[contains(text(), 'All')]"  # XPath for the 'All' option in date picker

        # 'Last 7 Days' Filter Option
        self.last_7_days_filter = "p.m-0.text-sm:has-text('Last 7 Days')"  # 'Last 7 Days' filter option

        # Custom Range Elements
        self.custom_range_locator = "p.m-0.text-sm:has-text('Custom Range')"  # Custom range option
        self.from_month_dropdown_locator = "span.p-dropdown-label.p-inputtext[aria-label='Jan, 2025']"  # "From" month dropdown
        self.to_month_dropdown_locator = "span.p-dropdown-label.p-inputtext[aria-label='Feb, 2025']"  # "To" month dropdown

        # Calendar Day Element with Dynamic 'date_id'
        self.calendar_day_locator = "//div[@id='{date_id}']"  # Calendar day element with a dynamic date_id

        # ============================
        # **Apply and Filter Button Locators**
        # ============================

        # Search ORDER ID on Filters
        self.search_order_id_locator = "input[placeholder='Search By Order Id']"  # Locator for search by order ID

        # 'Apply' Button to Apply Filters
        self.apply_button_locator = "button:has-text('Apply')"  # Locator for the apply button

        # ============================
        # **Locators for the Applied Filter and Date Range Display**
        # ============================

        # Applied Filter Text (e.g., "Order Date : Last 7 Days")
        self.applied_filter_text_locator = "div.cursor-pointer:has-text('Order Date : Last 7 Days')"  # Applied filter text

        # Displayed Date Range (e.g., "01-01-2025 to 08-04-2025")
        self.date_range_display = "div.showing-date-box"  # Displayed date range element

        # ============================
        # **Locators for 'No Records Found' Message**
        # ============================

        # 'No Records Found' Message (When No Records Match the Applied Filter)
        self.no_records_found_locator = "div.head:has-text('No Records Found')"  # Locator for the "No Records Found" message

        # ============================
        # **Locators for Amount Filters on Table**
        # ============================

        # Amount Filter Fields
        self.amount_section = "#order_amount:has-text('Amount')"  # Locator for the Amount section
        self.amount_range_dropdown = "#order_amount_list #baseDropdown"  # Locator for the amount range dropdown
        self.min_value_input_locator = "#order_amount_list input[placeholder='Min']"  # Min value input field
        self.max_value_input_locator = "#order_amount_list input[placeholder='Max']"  # Max value input field
        self.amount_value_input_locator = '#order_amount_list input[placeholder="Value"]'  # Amount value input field

        # Error Message for Invalid 'Min' Value
        self.min_value_error_message_locator = ".p-toast.notification-bar"  # Error message for invalid Min value

        # ============================
        # **Locators for Risk Filters on Table**
        # ============================

        # Risk Filter Fields
        self.risk_section = "#order_risk:has-text('Risk')"  # Locator for the Risk section
        self.risk_column_header_locator = 'th.order_risk:has-text("Risk")'  # Locator for the Risk column header

        # Risk Overlay Locator (e.g., overlay content when selecting risk)
        self.risk_overlay_locator = '.p-overlaypanel-content .header'  # Locator for the content in the risk overlay

        # Close Button for the Overlay
        self.overlay_close_button_locator = 'p-overlaypanel-close p-link'  # Close button for the overlay

        # ============================
        # **Dispatch Table Locators**
        # ============================

        # Locators for Amount Column and Pagination
        self.amount_column_header_locator = 'th.order_amount:has-text("Amount")'  # Locator for the Amount column header

        # Pagination Controls
        self.next_button_locator = 'button.p-paginator-next.p-paginator-element.p-link'  # Locator for the Next Page button
        self.last_button_locator = "button.p-paginator-last.p-paginator-element.p-link"  # Locator for the Last Page button
        self.first_button_locator = 'button.p-paginator-first.p-paginator-element.p-link'  # Locator for the First Page button
        self.pagination_text_locator = ".pagignationRow .p-paginator-left-content"  # Locator for pagination text

        # ============================
        # **Export Table Locators**
        # ============================
        self.export_button_locator = "div.export-btn-outer.export-btn-dataTable:has-text('Export')"

    def wait_for_rtd_page_to_load(self):
        """Wait for the 'Ready To Dispatch' text to appear, confirming that the RTD page has loaded."""
        self.wait_for_element("span.w-max:text('Ready To Dispatch')", timeout=10000)

    def is_ready_to_dispatch_visible(self):
        """Check if the 'Ready To Dispatch' text is visible on the page."""
        return self.is_visible("span.w-max:text('Ready To Dispatch')")

    def select_last_7_days(self):
        """Click on the date box, select 'Last 7 Days' filter, and apply it."""
        try:
            # Step 1: Click the date picker box to open the calendar
            print("Waiting for the date picker box to be visible...")
            self.page.wait_for_selector(self.date_box, timeout=30000)  # Wait for the element to appear
            print("Date picker box visible.")
            self.click(self.date_box)
            print("Date picker opened.")

            # Step 2: Wait for and select the 'Last 7 Days' filter
            print("Waiting for the 'Last 7 Days' filter to be visible...")
            self.page.wait_for_selector(self.last_7_days_filter, timeout=30000)  # Wait for the 'Last 7 Days' filter to be visible
            print("Last 7 Days filter visible.")
            self.click(self.last_7_days_filter)  # Select 'Last 7 Days' filter option
            print("✅ 'Last 7 Days' filter applied successfully.")

        except Exception as e:
            print(f"Error during 'select_last_7_days' action: {e}")
            raise

    def select_custom_range(self, start_day: str, month: str, year: str):
        """Select the custom range by clicking the Custom Range option,
        selecting the month, selecting start and end dates, and applying the filter."""

        try:
            # Step 1: Click the date picker box to open the calendar
            print("Opening the date picker...")
            self.click(self.date_box)
            print("Date picker opened.")

            # Step 2: Select the Custom Range option
            print("Waiting for 'Custom Range' option to appear...")
            self.wait_for_element(self.custom_range_locator, timeout=10000)
            sleep(10)  # You can adjust this based on the time it takes for the calendar to open
            self.click(self.custom_range_locator)
            print("Custom Range option selected.")

            # Step 3: Wait and click the "From" month dropdown
            print("Selecting the 'From' month dropdown...")
            self.wait_for_element(self.from_month_dropdown_locator, timeout=10000)
            self.click(self.from_month_dropdown_locator)
            print("'From' month dropdown clicked.")

            # Step 4: Select the "From" month dropdown (e.g., Jan, 2025)
            month_locator = f"//div[@id='baseDropdown']//li[@aria-label='{month}, {year}']"
            print(f"Locator for the 'From' month: {month_locator}")
            self.wait_for_element(month_locator, timeout=10000)
            self.click(month_locator)
            print(f"Start month {month}, {year} selected.")

            # Step 5: Select the start date (e.g., 1st Jan)
            start_month = datetime.strptime(month, "%b").strftime(
                "%m")  # Convert month to 2-digit format (01, 02, 03...)
            start_date_locator = f'div[id="{year}-{start_month.zfill(2)}-{start_day.zfill(2)}"]'
            print(f"Locator for start date: {start_date_locator}")

            # Wait for the specific start date element to appear
            self.wait_for_element(start_date_locator, timeout=10000)
            self.click(start_date_locator)  # Click on the start date
            print(f"Start date {start_day}-{month}-{year} selected.")

            # Step 6: Select the "To" month dropdown
            today = datetime.today()
            current_month = today.strftime('%b')
            current_year = today.strftime('%Y')

            print("Selecting the 'To' month dropdown...")
            self.wait_for_element(self.to_month_dropdown_locator, timeout=10000)
            self.click(self.to_month_dropdown_locator)
            print("'To' month dropdown clicked.")

            # Step 7: Select the "To" month (current month)
            month_locator = f"li#baseDropdown_2[aria-label='{current_month},  {current_year}']" # this has two spaces in between
            print(f"Locator for 'To' month: {month_locator}")
            self.wait_for_element(month_locator, timeout=10000)
            self.click(month_locator)
            print(f"End month {current_month}, {current_year} selected.")

            # Step 8: Select today's date as the end date
            current_day = today.strftime('%d')  # Get today's day as a 2-digit number
            end_date_locator = f'div[id="{current_year}-{today.month:02d}-{current_day.zfill(2)}"]'
            print(f"Locator for end date: {end_date_locator}")

            # Wait for the specific end date element (today's date) to appear
            self.wait_for_element(end_date_locator, timeout=10000)
            self.click(end_date_locator)  # Click on today's date
            print(f"End date {current_day}-{current_month}-{current_year} selected.")

            # Step 9: Click the 'Apply' button to apply the filter
            print("Clicking 'Apply' button to apply the custom date range filter...")
            self.click(self.apply_button_locator)
            print(
                f"✅ Custom date range from {start_day}-{month}-{year} to {current_day}-{current_month}-{current_year} applied successfully.")

        except Exception as e:
            print(f"❌ Error during selecting custom date range: {e}")
            raise

    def get_displayed_date_range(self):
        """Get the date range displayed on the RTD page after applying a filter."""
        self.wait_for_element(self.date_range_display, timeout=10000)
        date_range_text = self.page.locator(self.date_range_display).text_content()
        # Extract the start and end dates using a regular expression for DD-MM-YYYY format
        date_match = re.match(r"(\d{2}-\d{2}-\d{4}) - (\d{2}-\d{2}-\d{4})", date_range_text)
        if date_match:
            start_date = date_match.group(1)  # Start date from the displayed range
            end_date = date_match.group(2)  # End date from the displayed range
            return start_date, end_date
        else:
            raise ValueError("Date range format is incorrect or couldn't be parsed.")

    def get_applied_filter_text(self):
        """Get the applied filter text from above the table."""
        self.wait_for_element(self.applied_filter_text_locator, timeout=10000)
        return self.page.locator(self.applied_filter_text_locator).text_content().strip()

    def open_filter_menu(self):
        """Click on the Filters button to open the filter options."""
        self.click("span:has-text('Filters')")
        print("Filter menu opened.")

    def fill_order_id(self, order_id: str):
        """Apply the Order ID filter with the specified Order ID."""

        try:
            # Step 1: Wait for the Order ID input field to appear
            print("Waiting for the Order ID input field to appear...")
            self.wait_for_element(self.search_order_id_locator, timeout=10000)  # Wait for the element to appear
            print("Order ID input field found.")

            # Step 2: Fill in the input field with the provided Order ID
            print(f"Filling the Order ID input field with value: {order_id}")
            self.fill(self.search_order_id_locator, order_id)  # Fill the input with the Order ID
            print(f"Order ID '{order_id}' entered successfully.")

        except Exception as e:
            print(f"❌ Error occurred while applying filter for Order ID: {order_id}. Error: {e}")
            raise

    def verify_no_records_found(self):
        """Verify if the 'No Records Found' message is visible after applying an invalid filter."""
        self.wait_for_element(self.no_records_found_locator, timeout=10000)  # Wait for the 'No Records Found' message
        assert self.is_visible(self.no_records_found_locator), "No Records Found message not displayed!"
        print("✅ 'No Records Found' message is visible.")

    def select_risk_section(self):
        """Select the 'Risk' filter and set 'Select Range' condition."""
        try:
            # Wait for the Amount section to be visible
            self.wait_for_element(self.risk_section, timeout=10000)
            self.click(self.risk_section)
            print("Risk filter section is visible.")

        except Exception as e:
            print(f"Error during 'select_risk_section' method: {e}")
            raise  # Re-raise the exception for further debugging or logging

    def select_risk_option(self, risk_options: list):
        """Select multiple checkboxes based on the given risk options."""
        try:
            # Loop through each risk option and select the corresponding checkbox
            for risk_option in risk_options:
                # Generate the dynamic locator for the risk option
                risk_option_locator = f"input[name='{risk_option}']"

                # Wait for the checkbox element to be visible
                self.wait_for_element(risk_option_locator, timeout=10000)
                print(f"Risk option '{risk_option}' checkbox is visible.")

                # Locate the checkbox and check if it is already selected
                checkbox = self.page.locator(risk_option_locator)
                if not checkbox.is_checked():  # If the checkbox is not selected
                    checkbox.click()  # Click to select the checkbox
                    print(f"Selected risk option: {risk_option}")
                else:
                    print(f"Risk option '{risk_option}' is already selected.")

        except Exception as e:
            print(f"Error while selecting risk options: {e}")
            raise

    def extract_by_parent_key(self, obj, parent_key):
        """
        Recursively collect all dicts that match the parent_key.
        """
        matches = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == parent_key and isinstance(v, dict):
                    matches.append(v)
                elif isinstance(v, (dict, list)):
                    matches.extend(self.extract_by_parent_key(v, parent_key))
        elif isinstance(obj, list):
            for item in obj:
                matches.extend(self.extract_by_parent_key(item, parent_key))
        return matches

    def get_all_risk_column_values(self, first_page_response=None, parent_key=None ,target_ui_key=None):
        """Get all values from the 'Risk' column, handling pagination and overlays."""
        try:
            all_risk_values = []  # List to store all UI risk across pages
            all_api_risk = []  # List to store all API risk across pages
            current_page = 1
            total_pages = self.get_total_pages()  # Get the total number of pages
            print(f"Total pages to process: {total_pages}")

            while current_page <= total_pages:
                print(f"\n📄 Processing page {current_page}/{total_pages}...")

                # Wait for the Amount column header to be visible
                self.wait_for_element(self.amount_column_header_locator, timeout=10000)

                # --- API Interception ---
                if current_page == 1 and first_page_response:
                    response = first_page_response
                elif current_page > 1:
                    next_button = self.page.locator(self.next_button_locator)
                    if next_button.is_enabled():
                        trigger = lambda: next_button.click()
                        response = self.intercept_response("/api/v1/order/forward/get/data", trigger_action=trigger)
                        # Wait for table to load
                        time.sleep(5)
                    else:
                        print("❌ Next button not enabled despite expected more pages.")
                        break
                else:
                    raise Exception("Unexpected pagination state.")

                json_data = response.json()
                # Step 1: Filter to only order_risk sub-dicts
                order_risk_sections = self.extract_by_parent_key(json_data, parent_key)

                # Step 2: get all the values within that extracted json
                api_risk_strs = []
                for section in order_risk_sections:
                    api_risk_strs.extend(self.find_keys_recursively(section, target_ui_key))
                all_api_risk.extend(api_risk_strs)

                print(f"✅ API values (page {current_page}): {all_api_risk}")

                # --- UI Extraction ---
                # Extract rows from the table (excluding the header)
                rows = self.page.locator('table tbody tr')  # Select all rows in the table body
                number_of_rows = rows.count()

                # Iterate over all rows and extract the risk column values
                for i in range(number_of_rows):
                    risk_cell = rows.nth(i).locator('td.order_risk')  # Select the risk cell in the row

                    # Check if it is 'NA' (No overlay)
                    img_src = risk_cell.locator('img').get_attribute('src')
                    if 'shield-gray' in img_src:
                        # If image has shield-gray, it indicates "NA"
                        risk_value = "NA"
                    else:
                        # Click to open the overlay for other risk values (Low, Medium, High)
                        risk_cell.click()
                        # print("Risk cell clicked to open overlay.")

                        # Wait for the overlay to appear
                        self.wait_for_element(self.risk_overlay_locator)

                        # Extract the risk value from the overlay (e.g., Low Risk, Medium Risk, High Risk)
                        risk_value = self.page.locator(self.risk_overlay_locator).text_content().strip()
                        # print(f"Risk value from overlay: {risk_value}")

                        # Close the overlay after extracting the value
                        risk_cell.click()  # Click again to close the overlay
                        # print("Risk cell clicked to close overlay.")

                    # Add the risk value to the list
                    all_risk_values.append(risk_value.strip())

                print(f"✅ UI values (page {current_page}): {all_risk_values}")

                # Exit loop if it's the last page
                if current_page == total_pages:
                    print("🏁 Reached the last page.")
                    break

                current_page += 1

            print(f"\n📊 All API values: {all_api_risk}")
            print(f"📊 All UI values: {all_risk_values}")
            return all_api_risk, all_risk_values

        except Exception as e:
            print(f"Error occurred while retrieving all Risk column values: {e}")
            raise

    def select_amount_section(self):
        """Select the 'Amount' filter and set 'Select Range' condition."""
        try:
            # Wait for the Amount section to be visible
            self.wait_for_element(self.amount_section, timeout=10000)
            self.click(self.amount_section)
            print("Amount filter section is visible.")

            # Wait for the amount range dropdown and click it
            self.wait_for_element(self.amount_range_dropdown, timeout=10000)
            self.click(self.amount_range_dropdown)
            print("Amount filter dropdown selected.")

        except Exception as e:
            print(f"Error during 'select_amount_section' method: {e}")
            raise  # Re-raise the exception for further debugging or logging

    def select_amount_filter_condition(self, condition: str):
        """Select the 'Amount' filter and set the specified condition (e.g., 'Select Range', 'Greater than')."""
        try:
            # Mapping of conditions to their respective dropdown selectors
            condition_to_selector_map = {
                "Select Range": "#baseDropdown_0",  # Selector for 'Select Range'
                "Greater than": "#baseDropdown_1",  # Selector for 'Greater than'
                "Less than": "#baseDropdown_2",  # Selector for 'Less than'
                "Greater than and equal to": "#baseDropdown_3",  # Selector for 'Greater than and equal to'
                "Less than and equal to": "#baseDropdown_4",  # Selector for 'Less than and equal to'
                "Equal to": "#baseDropdown_5"  # Selector for 'Equal to'
            }

            # Check if the condition is valid
            if condition not in condition_to_selector_map:
                raise ValueError(
                    f"Invalid condition: {condition}. Valid conditions are: 'Select Range', 'Greater than', 'Less than', 'Greater than and equal to', 'Less than and equal to', 'Equal to'.")


            # Step 1: Get the appropriate dropdown selector for the condition
            condition_selector = condition_to_selector_map[condition]

            # Step 2: Wait for the condition to appear and click it
            self.wait_for_element(condition_selector, timeout=10000)
            self.click(condition_selector)
            print(f"Amount filter condition '{condition}' selected successfully.")

        except Exception as e:
            print(f"Error during 'select_amount_filter_condition' method: {e}")
            raise  # Re-raise the exception for further debugging or logging

    def fill_amount_min_value(self, min_value):
        """Fill the 'Min' value input field."""
        try:
            # Fill the Min input field with the given value
            self.fill(self.min_value_input_locator, str(min_value))
            print(f"Min value set to {min_value}.")

        except Exception as e:
            print(f"Error during 'fill_amount_min_value' method: {e}")
            raise  # Re-raise the exception for further debugging or logging

    def fill_amount_max_value(self, max_value):
        """Fill the 'Max' value input field."""
        try:
            # Fill the Max input field with the given value
            self.fill(self.max_value_input_locator, str(max_value))
            print(f"Max value set to {max_value}.")

        except Exception as e:
            print(f"Error during 'fill_amount_max_value' method: {e}")
            raise  # Re-raise the exception for further debugging or logging

    def fill_amount_value(self, input_value):
        """Fill the 'greater than' value input field."""
        try:
            # Fill the Min input field with the given value
            self.fill(self.amount_value_input_locator, str(input_value))
            print(f"Amount value set to {input_value}.")

        except Exception as e:
            print(f"Error during 'fill_amount_value' method: {e}")
            raise  # Re-raise the exception for further debugging or logging

    def apply_filter(self):
        """Click the 'Apply' button to apply the filter."""
        self.click(self.apply_button_locator)  # Click the 'Apply' button to apply the filter
        print("Apply button clicked.")
        sleep(1)

    def get_min_value_toast_error_message(self):
        """Get the error message for invalid 'Min' value (toast message)."""
        try:
            # Wait for the toast message to appear (adjust the timeout if necessary)
            self.wait_for_element(self.min_value_error_message_locator, timeout=10000)

            # # Optionally, wait a bit more to ensure the message is fully visible
            # time.sleep(1)  # Wait for 1 second to capture the message if needed

            # Get the error message text (this will be the toast message)
            error_message = self.page.locator(self.min_value_error_message_locator).text_content()

            # Print the error message for debugging
            print(f"Error message displayed: {error_message}")

            return error_message

        except Exception as e:
            # Log the error and re-raise it for further handling
            print(f"Error while retrieving the 'Min' value error message: {e}")
            raise  # Re-raise the exception to propagate it upwards

    def wait_for_loading_state(self):
        """Wait for the table to process the filter."""
        self.wait_for_element("div.loading-indicator", timeout=10000)  # Wait for the loading spinner to disappear
        print("Data loaded successfully.")

    def wait_for_loading_spinner_to_disappear(self):
        """Wait for the loading spinner to disappear (indicating the table has finished loading)."""
        try:
            # Wait for the loading spinner to appear
            spinner_locator = self.page.locator('.loading-spinner')  # Replace with the actual class or selector
            spinner_locator.wait_for(state='visible', timeout=10000)  # Wait for spinner to appear

            # Wait for the spinner to disappear (indicating the table has finished loading)
            spinner_locator.wait_for(state='hidden', timeout=30000)  # Wait for spinner to disappear

            print("Loading spinner has disappeared, table is loaded.")
        except Exception as e:
            print(f"Error while waiting for the loading spinner to disappear: {e}")
            raise

    def clean_amount(self, amount_string):
        """Helper function to clean amount string by removing the ₹ symbol and converting to float."""
        try:
            if amount_string.strip().lower() == 'amount':  # Check if it's the header text
                return None  # Skip the header text

            # Remove the ₹ symbol and any non-numeric characters
            amount = amount_string.replace('₹', '').strip()
            return float(amount)
        except Exception as e:
            print(f"Error cleaning amount string '{amount_string}': {e}")
            return None  # Return None for invalid amounts (e.g., empty or malformed data)

    def find_keys_recursively(self, obj, key_name):
        """
        Recursively search for all values of a given key in a nested dict/list structure.
        """
        found = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key_name:
                    found.append(v)
                elif isinstance(v, (dict, list)):
                    found.extend(self.find_keys_recursively(v, key_name))  # Correct usage of self
        elif isinstance(obj, list):
            for item in obj:
                found.extend(self.find_keys_recursively(item, key_name))  # Correct usage of self
        return found

    def get_all_amount_column_values(self, first_page_response=None, target_ui_key=None):
        """
        Retrieves all values from the 'Amount' column in a paginated table and from API interception.
        Handles first page response via provided argument and continues interception for subsequent pages.
        Returns two lists: API values and UI values.
        """
        try:
            all_amount_values = []  # List to store all UI amounts across pages
            all_api_prices = []  # List to store all API amounts across pages
            current_page = 1
            total_pages = self.get_total_pages()

            while current_page <= total_pages:
                print(f"\n📄 Processing page {current_page}/{total_pages}...")

                # Wait for the Amount column header to be visible
                self.wait_for_element(self.amount_column_header_locator, timeout=10000)

                # --- API Interception ---
                if current_page == 1 and first_page_response:
                    response = first_page_response
                elif current_page > 1:
                    next_button = self.page.locator(self.next_button_locator)
                    if next_button.is_enabled():
                        trigger = lambda: next_button.click()
                        response = self.intercept_response("/api/v1/order/forward/get/data", trigger_action=trigger)
                        # Wait for table to load
                        time.sleep(5)
                    else:
                        print("❌ Next button not enabled despite expected more pages.")
                        break
                else:
                    raise Exception("Unexpected pagination state.")

                json_data = response.json()
                api_price_strs = self.find_keys_recursively(json_data, target_ui_key)

                if not api_price_strs:
                    raise AssertionError(f"No key '{target_ui_key}' found in API response JSON.")

                for idx, price_str in enumerate(api_price_strs, 1):
                    price_clean = re.sub(r"[^\d.]+", "", price_str)
                    try:
                        price = float(price_clean)
                        all_api_prices.append(price)
                    except ValueError:
                        raise AssertionError(f"❌ Entry #{idx}: '{price_str}' is not a valid number.")

                print(f"✅ API values (page {current_page}): {api_price_strs}")

                # --- UI Extraction ---
                rows = self.page.locator('table tbody tr')
                number_of_rows = rows.count()

                for i in range(number_of_rows):
                    amount_cell = rows.nth(i).locator('td:nth-child(4)')
                    amount_value = amount_cell.text_content()
                    cleaned_value = self.clean_amount(amount_value)
                    if cleaned_value is not None:
                        all_amount_values.append(cleaned_value)

                print(f"✅ UI values (page {current_page}): {all_amount_values}")

                # Exit loop if it's the last page
                if current_page == total_pages:
                    print("🏁 Reached the last page.")
                    break

                current_page += 1

            print(f"\n📊 All API values: {all_api_prices}")
            print(f"📊 All UI values: {all_amount_values}")
            return all_api_prices, all_amount_values

        except Exception as e:
            print(f"❌ Error in get_all_amount_column_values: {e}")
            raise

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
