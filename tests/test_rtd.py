from time import sleep

import pytest, re
from datetime import datetime, timedelta


def date_in_range(start_date: str, end_date: str, date: str) -> bool:
    """Helper function to check if a given date is within a specified range."""
    try:
        start = datetime.strptime(start_date, '%m-%d-%Y')
        end = datetime.strptime(end_date, '%m-%d-%Y')
        result = datetime.strptime(date, '%m-%d-%Y')
        return start <= result <= end
    except Exception as e:
        print(f"Error in 'date_in_range' function: {e}")
        raise


def get_last_7_days():
    """Calculate the start and end dates for the 'Last 7 Days' filter."""
    try:
        today = datetime.today()  # Get today's date
        start_date = today - timedelta(days=6)  # Subtract 6 days to get the start date (including today)
        return start_date.strftime('%d-%m-%Y'), today.strftime('%d-%m-%Y')  # Format as DD-MM-YYYY
    except Exception as e:
        print(f"Error in 'get_last_7_days' function: {e}")
        raise


def test_custom_date_API(login_page, dashboard_page, rtd_page):
    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Step 2: Apply a custom date range (e.g., from 01-01-2025 to today's date)
        print("Selecting a custom date range...")

        # Get today's date formatted as DD-MM-YYYY
        today = datetime.today().strftime('%d-%m-%Y')
        print(f"Today's date: {today}")

        # Set start day, month, and year manually (or dynamically)
        start_day = "01"
        month = "Jan"  # or dynamically set it as needed
        year = "2025"

        # Step 3: Call the select_custom_range method from the RTDPage
        api_date_val = rtd_page.select_api_custom_range(start_day, month, year)  # You will pass the date dynamically here

        # Step 4: Verify the displayed date range
        start_date, end_date = rtd_page.get_displayed_date_range()

        # Assert that the displayed date range matches the expected one (start date is the one set, and end date should be today)
        assert start_date == "01-01-2025", f"Expected start date 01-04-2025, but found {start_date}"
        assert end_date == today, f"Expected end date {today}, but found {end_date}"



        print(f"Custom date range from 01-04-2025 to {today} applied successfully!")

    except Exception as e:
        print(f"Error during 'Custom Date Range Filter' Test: {e}")
        raise


def test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page):
    """Test to log in, navigate to the dashboard, and validate the RTD page."""

    try:
        # Step 1: Navigate to the login page
        print("Navigating to login page...")
        login_page.navigate("https://my.ithinklogistics.com/login")

        # Ensure the page has loaded
        login_page.page.wait_for_load_state('load')  # Wait for the page to load
        print(f"Page loaded: {login_page.page.url}")

        # Step 2: Wait for the login form to appear and fill in the credentials
        login_page.wait_for_login_form()
        login_page.login("xylifedemo@gmail.com", "Admin@1234")

        # Step 3: Wait for the dashboard to load
        print("'Welcome' text not found, checking for 'Create Order' button instead...")
        dashboard_page.wait_for_dashboard_to_load()

        # Step 4: After login, navigate to the RTD page again
        print("Navigating back to RTD page...")
        login_page.page.goto("https://my.ithinklogistics.com/v4/order/rtd")

        # Step 5: Wait for the RTD page to load (check if the 'Ready To Dispatch' span is visible)
        rtd_page.wait_for_rtd_page_to_load()
        print("RTD page successfully loaded!")

        # Step 6: Validate the presence of the 'Ready To Dispatch' text
        assert rtd_page.is_ready_to_dispatch_visible(), "RTD page did not load successfully!"

        sleep(3)

        # Step 7: No need to manually close the browser; it's handled in conftest.py
        # Browser will be closed automatically after the test completes

    except Exception as e:
        print(f"Error during 'Login and Navigate to RTD Page' test: {e}")
        raise


def test_last_7_days_filter(login_page, dashboard_page, rtd_page):
    """Test to apply the 'Last 7 Days' filter on the RTD page and verify the displayed date range."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Step 2: Apply the 'Last 7 Days' filter
        print("Selecting 'Last 7 Days' filter...")
        sleep(3)
        rtd_page.select_last_7_days()  # Select the 'Last 7 Days' filter

        # Step 3: Calculate the expected date range (last 7 days)
        start_date, today = get_last_7_days()

        # Step 4: Get the displayed date range after applying the filter
        start_date_range_text, today_date_range_text = rtd_page.get_displayed_date_range()
        print(f"Expected date range: {start_date} - {today}")
        print(f"Displayed date range: {start_date_range_text} - {today_date_range_text}")

        # Step 5: Validate that the displayed date range is correct
        assert start_date in start_date_range_text and today in today_date_range_text, f"Date range is incorrect. Expected: {start_date} - {today}, but found: {start_date_range_text} - {today_date_range_text}"

        # Step 6: Validate the applied filter text above the table
        applied_filter_text = rtd_page.get_applied_filter_text()  # Get the filter text
        expected_filter_text = "Order Date : Last 7 Days"
        print(f"Expected filter text: {expected_filter_text}")
        print(f"Displayed filter text: {applied_filter_text}")

        # Step 7: Assert the filter text is correct
        assert expected_filter_text in applied_filter_text, f"Expected filter text: {expected_filter_text}, but found: {applied_filter_text}"

        print("✅ 'Last 7 Days' filter applied successfully and verified!")

    except Exception as e:
        print(f"Error during 'Last 7 Days' Filter Test: {e}")
        raise


def test_custom_date_range_filter(login_page, dashboard_page, rtd_page):
    """Test to apply a custom date range filter on the RTD page and verify the displayed date range."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Step 2: Apply a custom date range (e.g., from 01-01-2025 to today's date)
        print("Selecting a custom date range...")

        # Get today's date formatted as DD-MM-YYYY
        today = datetime.today().strftime('%d-%m-%Y')
        print(f"Today's date: {today}")

        # Set start day, month, and year manually (or dynamically)
        start_day = "01"
        month = "Jan"  # or dynamically set it as needed
        year = "2025"

        # Step 3: Call the select_custom_range method from the RTDPage
        rtd_page.select_custom_range(start_day, month, year)  # You will pass the date dynamically here

        # Step 4: Verify the displayed date range
        start_date, end_date = rtd_page.get_displayed_date_range()

        # Assert that the displayed date range matches the expected one (start date is the one set, and end date should be today)
        assert start_date == "01-01-2025", f"Expected start date 01-04-2025, but found {start_date}"
        assert end_date == today, f"Expected end date {today}, but found {end_date}"

        print(f"Custom date range from 01-04-2025 to {today} applied successfully!")

    except Exception as e:
        print(f"Error during 'Custom Date Range Filter' Test: {e}")
        raise


def test_no_records_for_invalid_order_id(login_page, dashboard_page, rtd_page):
    """Test to verify that 'No Records Found' is displayed for an invalid Order ID."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Optional: Log outgoing API requests
        def log_request(request):
            if "/api/v1/order/forward/get/data" in request.url:
                print(f"\n➡️ [Request]")
                print(f"URL: {request.url}")
                print(f"Method: {request.method}")
                print(f"Headers: {request.headers}")
                print(f"Post Data: {request.post_data}\n")

        rtd_page.page.on("request", log_request)

        # Step 2: Open the filter menu and apply an invalid Order ID
        rtd_page.open_filter_menu()
        invalid_order_id = "INVALID_ORDER_ID"
        rtd_page.fill_order_id(invalid_order_id)  # Apply the invalid Order ID filter

        # Step 3: Intercept the API response and validate it
        response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter  # or whatever action triggers the request
        )

        # Step 4: API validation
        # Ensure the API returned status 200
        assert response.status == 200, f"Expected status code 200, got {response.status}"

        # Ensure the response JSON contains a success status
        response_json = response.json()
        assert response_json.get("status") == "success", f"Expected 'success' status, got {response_json.get('status')}"

        # Ensure the data array is empty
        assert response_json.get("data") == [], "Expected empty 'data' array, but got data."

        print("✅ API validation successful: Status 200, Success, and Empty Data.")

        # Step 5: Verify the 'No Records Found' message is displayed in the UI
        rtd_page.verify_no_records_found()  # Check if the "No Records Found" message appears
        print("✅ 'No Records Found' message displayed for invalid Order ID!")

    except Exception as e:
        print(f"Error during 'No Records Found' Test for Invalid Order ID: {e}")
        raise


def test_amount_min_value_zero(login_page, dashboard_page, rtd_page, min_value=0):
    """Test to verify that the 'Min' value cannot be zero in the 'Amount' filter.
       This includes checking that both the UI and API contain the expected error message.
    """

    expected_message_snippet = "The Min Amount field must be greater than or equal to 0.1."

    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Optional: Log outgoing API requests
        def log_request(request):
            if "/api/v1/order/forward/get/data" in request.url:
                print(f"\n➡️ [Request]")
                print(f"URL: {request.url}")
                print(f"Method: {request.method}")
                print(f"Headers: {request.headers}")
                print(f"Post Data: {request.post_data}\n")

        rtd_page.page.on("request", log_request)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the Amount filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Select the 'Select Range' filter condition
        rtd_page.select_amount_filter_condition("Select Range")
        print(f"Selected 'Select Range' condition with Min: {min_value}")

        # Step 5: Fill in Min/Max values
        rtd_page.fill_amount_min_value(min_value)
        rtd_page.fill_amount_max_value(100)

        # Step 6: Intercept API call and apply filter
        response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter  # or whatever action triggers the request
        )

        # Step 7: Immediately assert the UI error message (toast)
        toast_message = rtd_page.get_min_value_toast_error_message()
        assert expected_message_snippet in toast_message, \
            f"Expected toast to contain: '{expected_message_snippet}', but got: '{toast_message}'"
        print("UI toast validation passed.")

        # Step 8: Validate API response
        assert response.status == 422, f"Expected status code 422, but got {response.status}"
        try:
            json_data = response.json()
            print(f"Response JSON:\n{json_data}")
        except Exception as e:
            raise AssertionError(f"Could not parse JSON from response: {e}")

        assert json_data.get("status") == "error", f"Expected status 'error', got: {json_data.get('status')}"
        api_message = json_data.get("message", "")
        assert expected_message_snippet in api_message, \
            f"Expected API message to contain: '{expected_message_snippet}', but got: '{api_message}'"
        print("API response validation passed.")

        # Step 9: Ensure no records are shown
        rtd_page.verify_no_records_found()
        print("'No Records Found' message confirmed.")

    except Exception as e:
        print(f"Test failed: {e}")
        raise


def test_amount_min_value_negative(login_page, dashboard_page, rtd_page, min_neg_value=-1):
    """Test to verify that the 'Min' value cannot be negative in the 'Amount' filter."""

    expected_message_snippet = "The Min Amount field must be greater than or equal to 0.1."

    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'Select Range' condition
        print(f"Selecting 'Amount' filter and 'Select Range' condition with Min value: {min_neg_value}...")
        rtd_page.select_amount_filter_condition("Select Range")  # Method to select 'Select Range' in the Amount filter

        # Step 5: Set the 'Min' value dynamically and a valid 'Max' value
        print(f"Setting 'Min' value to {min_neg_value}...")
        rtd_page.fill_amount_min_value(min_neg_value)  # Set the dynamic 'Min' value
        rtd_page.fill_amount_max_value(100)  # Set a valid 'Max' value

        # Optional: Log outgoing API requests
        def log_request(request):
            if "/api/v1/order/forward/get/data" in request.url:
                print(f"\n➡️ [Request]")
                print(f"URL: {request.url}")
                print(f"Method: {request.method}")
                print(f"Headers: {request.headers}")
                print(f"Post Data: {request.post_data}\n")

        rtd_page.page.on("request", log_request)

        # Step 6: Intercept API call and apply filter
        response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter  # or whatever action triggers the request
        )

        # Step 7: Immediately assert the UI error message (toast)
        toast_message = rtd_page.get_min_value_toast_error_message()
        assert expected_message_snippet in toast_message, \
            f"Expected toast to contain: '{expected_message_snippet}', but got: '{toast_message}'"
        print("Min value cannot be negative, and error message is displayed.")

        # Step 8: Validate API response
        assert response.status == 422, f"Expected status code 422, but got {response.status}"
        try:
            json_data = response.json()
            print(f"Response JSON:\n{json_data}")
        except Exception as e:
            raise AssertionError(f"Could not parse JSON from response: {e}")

        assert json_data.get("status") == "error", f"Expected status 'error', got: {json_data.get('status')}"
        api_message = json_data.get("message", "")
        assert expected_message_snippet in api_message, \
            f"Expected API message to contain: '{expected_message_snippet}', but got: '{api_message}'"
        print("API response validation passed.")

        # Step 9: Ensure no records are shown
        rtd_page.verify_no_records_found()
        print("'No Records Found' message displayed for invalid filter.")

    except Exception as e:
        print(f"Error during 'Amount Filter Min Value' Test: {e}")
        raise


def test_amount_max_value_smaller_than_min_value(login_page, dashboard_page, rtd_page, min_value=100, max_value=10):
    """Test to verify that the 'Max' value cannot be smaller than the 'Min' value in the 'Amount' filter."""
    # mo request was seen for this on UI as after apply it remained on same page
    try:
        # Step 1: Log in and navigate to the RTD page
        test_login_and_navigate_to_rtd_page(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'Select Range' condition
        print(f"Selecting 'Amount' filter and 'Select Range' condition for Min: {min_value} and Max: {max_value}...")
        rtd_page.select_amount_filter_condition("Select Range")  # Method to select 'Select Range' in the Amount filter

        # Step 5: Set the 'Min' value and 'Max' value dynamically
        print(f"Setting 'Min' value to {min_value} and 'Max' value to {max_value}...")
        rtd_page.fill_amount_min_value(min_value)  # Set a dynamic 'Min' value
        rtd_page.fill_amount_max_value(max_value)  # Set a dynamic 'Max' value
        rtd_page.apply_filter()

        # Step 6: Check for error message when 'Min' value is greater than 'Max' value
        error_message = rtd_page.get_min_value_toast_error_message()  # Method to retrieve error message
        assert "Min Amount should not be greater than Max Amount!" in error_message, "Error message is not displayed as expected!"

        print("✅ Max value cannot be smaller than Min value, and error message is displayed.")

    except Exception as e:
        print(f"Error during 'Amount Filter Min Value' Test: {e}")
        raise


def test_amount_valid_select_range(login_page, dashboard_page, rtd_page, min_value=10, max_value=100):
    """Test to verify that selected range is displayed in UI and API across all pages in the 'Amount' filter."""
    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu and select Amount filter
        rtd_page.open_filter_menu()
        print("✅ Filter menu opened.")

        rtd_page.select_amount_section()
        print("✅ Amount section selected.")

        # Step 3: Choose 'Select Range' and enter values
        print(f"🔧 Setting 'Select Range' with min: {min_value}, max: {max_value}...")
        rtd_page.select_amount_filter_condition("Select Range")
        rtd_page.fill_amount_min_value(min_value)
        rtd_page.fill_amount_max_value(max_value)

        # Step 4: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 5: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_amount_values, ui_amount_values = rtd_page.get_all_amount_column_values(
            first_page_response=first_page_response,
            target_ui_key="final_total_price"
        )

        # Step 6: Validate that all amounts are within the selected range
        print("🔒 Validating UI and API values...")
        # Validate UI Amounts
        for amount in ui_amount_values:
            if not (min_value <= amount <= max_value):
                print(f"❌ UI Amount {amount} is outside the range {min_value} - {max_value}")
                assert False
            else:
                assert True

        # Validate API Amounts
        for amount in api_amount_values:
            if not (min_value <= amount <= max_value):
                print(f"❌ API Amount {amount} is outside the range {min_value} - {max_value}")
                assert False
            else:
                assert True

        print(f"🎉 Test Passed: All UI and API values fall within the selected range {min_value}–{max_value}")
        print(f"🧮 Total validated values: UI - {len(ui_amount_values)}, API - {len(api_amount_values)}")

    except AssertionError as ae:
        print(f"❌ Assertion Error: {ae}")
        raise

    except Exception as e:
        print(f"❌ Unexpected error during test: {e}")
        raise


def test_amount_greater_than_filter(login_page, dashboard_page, rtd_page, greater_than_value=100):
    """Test to verify that the 'Greater than' condition in the 'Amount' filter works correctly and only amounts greater than the specified value are shown."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'Greater than' condition for Amount filter
        print(f"Selecting 'Amount' filter and 'Greater than' condition for values greater than {greater_than_value}...")
        rtd_page.select_amount_filter_condition("Greater than")  # Method to select 'Greater than' condition in the Amount filter

        # Step 5: Set the 'Greater than' value dynamically
        print(f"Setting 'Greater than' condition for amount greater than {greater_than_value}...")
        rtd_page.fill_amount_value(greater_than_value)  # Set a dynamic 'Greater than' value

        # Step 6: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 7: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_amount_values, ui_amount_values = rtd_page.get_all_amount_column_values(
            first_page_response=first_page_response,
            target_ui_key="final_total_price"
        )
        # Step 8: Validate that all amounts are within the selected range
        print("🔒 Validating UI and API values...")
        # Validate UI Amounts
        for amount in ui_amount_values:
            assert amount > greater_than_value, f"Amount {amount} is not greater than {greater_than_value}!"

        # Validate API Amounts
        for amount in api_amount_values:
            assert amount > greater_than_value, f"Amount {amount} is not greater than {greater_than_value}!"

        print(f"🎉 Test Passed: All UI and API values are greater than selected amount: {greater_than_value}")
        print(f"🧮 Total validated values: UI - {len(ui_amount_values)}, API - {len(api_amount_values)}")


    except Exception as e:
        print(f"Error during 'Amount Greater Than Filter' Test: {e}")
        raise


def test_amount_less_than_filter(login_page, dashboard_page, rtd_page, less_than_value=100):
    """Test to verify that the 'Less than' condition in the 'Amount' filter works correctly and only amounts lesser than the specified value are shown."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'less than' condition for Amount filter
        print(f"Selecting 'Amount' filter and 'Less than' condition for values greater than {less_than_value}...")
        rtd_page.select_amount_filter_condition("Less than")  # Method to select 'Greater than' condition in the Amount filter

        # Step 5: Set the 'Greater than' value dynamically
        print(f"Setting 'Less than' condition for amount greater than {less_than_value}...")
        rtd_page.fill_amount_value(less_than_value)  # Set a dynamic 'Greater than' value

        # Step 6: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 7: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_amount_values, ui_amount_values = rtd_page.get_all_amount_column_values(
            first_page_response=first_page_response,
            target_ui_key="final_total_price"
        )
        # Step 8: Validate that all amounts are less than selected value
        print("🔒 Validating UI and API values...")
        # Validate UI Amounts
        for amount in ui_amount_values:
            assert amount < less_than_value, f"UI Amount {amount} is not less than {less_than_value}!"

        # Validate API Amounts
        for amount in api_amount_values:
            assert amount < less_than_value, f"API Amount {amount} is not less than {less_than_value}!"

        print(f"🎉 Test Passed: All UI and API values are less than selected amount: {less_than_value}")
        print(f"🧮 Total validated values: UI - {len(ui_amount_values)}, API - {len(api_amount_values)}")

    except Exception as e:
        print(f"Error during 'Amount Less Than Filter' Test: {e}")
        raise


def test_amount_equal_to_filter(login_page, dashboard_page, rtd_page, equal_to_value=10):
    """Test to verify that the 'Equal to' condition in the 'Amount' filter works correctly and only amounts equal to the specified value are shown."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'Equal to' condition for Amount filter
        print(f"Selecting 'Amount' filter and 'Equal to' condition for values equal to {equal_to_value}...")
        rtd_page.select_amount_filter_condition("Equal to")  # Method to select 'Equal to' condition in the Amount filter

        # Step 5: Set the 'Equal to' value dynamically
        print(f"Setting 'Equal to' condition for amount equal to {equal_to_value}...")
        rtd_page.fill_amount_value(equal_to_value)  # Set a dynamic 'Equal to' value

        # Step 6: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 7: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_amount_values, ui_amount_values = rtd_page.get_all_amount_column_values(
            first_page_response=first_page_response,
            target_ui_key="final_total_price"
        )
        # Step 8: Validate that all amounts are equal to the selected value
        print("🔒 Validating UI and API values...")
        # Validate UI Amounts
        for amount in ui_amount_values:
            assert amount == equal_to_value, f"UI Amount {amount} is not equal to {equal_to_value}!"

        # Validate API Amounts
        for amount in api_amount_values:
            assert amount == equal_to_value, f"API Amount {amount} is not equal to {equal_to_value}!"

        print(f"🎉 Test Passed: All UI and API values are equal to the selected amount: {equal_to_value}")
        print(f"🧮 Total validated values: UI - {len(ui_amount_values)}, API - {len(api_amount_values)}")

    except Exception as e:
        print(f"Error during 'Amount Equal To Filter' Test: {e}")
        raise


def test_amount_greater_than_or_equal_to_filter(login_page, dashboard_page, rtd_page, greater_than_or_equal_to_value=100):
    """Test to verify that the 'Greater than or Equal to' condition in the 'Amount' filter works correctly and only amounts greater than or equal to the specified value are shown."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'Greater than or Equal to' condition for Amount filter
        print(f"Selecting 'Amount' filter and 'Greater than and equal to' condition for values greater than or equal to {greater_than_or_equal_to_value}...")
        rtd_page.select_amount_filter_condition("Greater than and equal to")  # Method to select 'Greater than or Equal to' condition in the Amount filter

        # Step 5: Set the 'Greater than or Equal to' value dynamically
        print(f"Setting 'Greater than or Equal to' condition for amount greater than or equal to {greater_than_or_equal_to_value}...")
        rtd_page.fill_amount_value(greater_than_or_equal_to_value)  # Set a dynamic 'Greater than or Equal to' value

        # Step 6: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 7: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_amount_values, ui_amount_values = rtd_page.get_all_amount_column_values(
            first_page_response=first_page_response,
            target_ui_key="final_total_price"
        )
        # Step 8: Validate that all amounts are within the selected range
        print("🔒 Validating UI and API values...")
        # Validate UI Amounts
        for amount in ui_amount_values:
            assert amount >= greater_than_or_equal_to_value, f"Amount {amount} is not greater than {greater_than_or_equal_to_value}!"

        # Validate API Amounts
        for amount in api_amount_values:
            assert amount >= greater_than_or_equal_to_value, f"Amount {amount} is not greater than {greater_than_or_equal_to_value}!"

        print(f"🎉 Test Passed: All UI and API values are greater than selected amount: {greater_than_or_equal_to_value}")
        print(f"🧮 Total validated values: UI - {len(ui_amount_values)}, API - {len(api_amount_values)}")


    except Exception as e:
        print(f"Error during 'Amount Greater Than or Equal To Filter' Test: {e}")
        raise


def test_amount_less_than_or_equal_to_filter(login_page, dashboard_page, rtd_page, less_than_and_equal_to_value=10):
    """Test to verify that the 'Less than or Equal to' condition in the 'Amount' filter works correctly and only amounts less than or equal to the specified value are shown."""

    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Amount' filter section
        rtd_page.select_amount_section()
        print("Amount section opened.")

        # Step 4: Choose 'Less than or Equal to' condition for Amount filter
        print(f"Selecting 'Amount' filter and 'Less than and equal to' condition for values less than or equal to {less_than_and_equal_to_value}...")
        rtd_page.select_amount_filter_condition("Less than and equal to")  # Method to select 'Less than or Equal to' condition in the Amount filter

        # Step 5: Set the 'Less than or Equal to' value dynamically
        print(f"Setting 'Less than or Equal to' condition for amount less than or equal to {less_than_and_equal_to_value}...")
        rtd_page.fill_amount_value(less_than_and_equal_to_value)  # Set a dynamic 'Less than or Equal to' value

        # Step 6: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 7: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_amount_values, ui_amount_values = rtd_page.get_all_amount_column_values(
            first_page_response=first_page_response,
            target_ui_key="final_total_price"
        )
        # Step 8: Validate that all amounts are less than selected value
        print("🔒 Validating UI and API values...")
        # Validate UI Amounts
        for amount in ui_amount_values:
            assert amount <= less_than_and_equal_to_value, f"UI Amount {amount} is not less than {less_than_and_equal_to_value}!"

        # Validate API Amounts
        for amount in api_amount_values:
            assert amount <= less_than_and_equal_to_value, f"API Amount {amount} is not less than {less_than_and_equal_to_value}!"

        print(f"🎉 Test Passed: All UI and API values are less than selected amount: {less_than_and_equal_to_value}")
        print(f"🧮 Total validated values: UI - {len(ui_amount_values)}, API - {len(api_amount_values)}")


    except Exception as e:
        print(f"Error during 'Amount Less Than or Equal To Filter' Test: {e}")
        raise


def test_risk_filter_selection_multiple_options(login_page, dashboard_page, rtd_page, risk_options=None):
    """Test to verify that the 'Risk' filter works correctly and only the selected risk options are shown."""
    if risk_options is None:
        risk_options = ["Low Risk", "Medium Risk"]
    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Risk' filter section
        rtd_page.select_risk_section()
        print("Risk section opened.")

        # Step 4: Select the risk options dynamically from the list of available options
        print(f"Selecting the following risk options: {risk_options}...")
        rtd_page.select_risk_option(risk_options)  # Select each risk option from the list

        # Step 6: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 7: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_risk_values, ui_risk_values = rtd_page.get_all_risk_column_values(
            first_page_response=first_page_response,
            parent_key="order_risk",
            target_ui_key="title"
        )

        # Step 8: Validate that all risk values are the range
        print("🔒 Validating UI and API values...")

        # Validate UI Amounts
        for risk_value in ui_risk_values:
            assert any(option in risk_value for option in risk_options), f"UI Risk value '{risk_value}' does not match any selected option!"

        # Validate API Amounts
        for risk_value in api_risk_values:
            assert any(option in risk_value for option in risk_options), f"API Risk value '{risk_value}' does not match any selected option!"

        print(f"🎉 Test Passed: All UI and API values are in the range: {risk_options}")
        print(f"🧮 Total validated values: UI - {len(ui_risk_values)}, API - {len(api_risk_values)}")

    except Exception as e:
        print(f"Error during 'Risk Filter Selection' Test: {e}")
        raise


def test_risk_filter_selection_NA(login_page, dashboard_page, rtd_page, risk_options=None):
    """Test to verify that the 'Risk' filter works correctly with risk options "NA" """

    if risk_options is None:
        risk_options = ["NA"]
    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Risk' filter section
        rtd_page.select_risk_section()
        print("Risk section opened.")

        # Step 4: Select the risk options NA
        print(f"Selecting the following risk options: {risk_options}...")
        rtd_page.select_risk_option(risk_options)  # Select each risk option from the list

        # Step 5: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 6: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_risk_values, ui_risk_values = rtd_page.get_all_risk_column_values(
            first_page_response=first_page_response,
            parent_key="order_risk",
            target_ui_key="title"
        )

        # Step 7: Validate that all risk values are the range
        print("🔒 Validating UI and API values...")

        # Validate UI Amounts
        for risk_value in ui_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"UI Risk value '{risk_value}' does not match any selected option!"

        # Validate API Amounts
        for risk_value in api_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"API Risk value '{risk_value}' does not match any selected option!"

        print(f"🎉 Test Passed: All UI and API values are in the range: {risk_options}")
        print(f"🧮 Total validated values: UI - {len(ui_risk_values)}, API - {len(api_risk_values)}")

    except Exception as e:
        print(f"Error during 'Risk Filter Selection' Test: {e}")
        raise


def test_risk_filter_selection_low(login_page, dashboard_page, rtd_page, risk_options=None):
    """Test to verify that the 'Risk' filter works correctly with risk options "Low Risk" """

    if risk_options is None:
        risk_options = ["Low Risk"]
    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Risk' filter section
        rtd_page.select_risk_section()
        print("Risk section opened.")

        # Step 4: Select the risk options Low Risks
        print(f"Selecting the following risk options: {risk_options}...")
        rtd_page.select_risk_option(risk_options)  # Select each risk option from the list

        # Step 5: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 6: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_risk_values, ui_risk_values = rtd_page.get_all_risk_column_values(
            first_page_response=first_page_response,
            parent_key="order_risk",
            target_ui_key="title"
        )

        # Step 7: Validate that all risk values are the range
        print("🔒 Validating UI and API values...")

        # Validate UI Amounts
        for risk_value in ui_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"UI Risk value '{risk_value}' does not match any selected option!"

        # Validate API Amounts
        for risk_value in api_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"API Risk value '{risk_value}' does not match any selected option!"

        print(f"🎉 Test Passed: All UI and API values are in the range: {risk_options}")
        print(f"🧮 Total validated values: UI - {len(ui_risk_values)}, API - {len(api_risk_values)}")

    except Exception as e:
        print(f"Error during 'Risk Filter Selection' Test: {e}")
        raise


def test_risk_filter_selection_high(login_page, dashboard_page, rtd_page, risk_options=None):
    """Test to verify that the 'Risk' filter works correctly with risk options "High Risk" """

    if risk_options is None:
        risk_options = ["High Risk"]
    try:
        # Step 1: Log in and navigate to the RTD page
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Risk' filter section
        rtd_page.select_risk_section()
        print("Risk section opened.")

        # Step 4: Select the risk options High Risk
        print(f"Selecting the following risk options: {risk_options}...")
        rtd_page.select_risk_option(risk_options)  # Select each risk option from the list

        # Step 5: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 6: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_risk_values, ui_risk_values = rtd_page.get_all_risk_column_values(
            first_page_response=first_page_response,
            parent_key="order_risk",
            target_ui_key="title"
        )

        # Step 7: Validate that all risk values are the range
        print("🔒 Validating UI and API values...")

        # Validate UI Amounts
        for risk_value in ui_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"UI Risk value '{risk_value}' does not match any selected option!"

        # Validate API Amounts
        for risk_value in api_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"API Risk value '{risk_value}' does not match any selected option!"

        print(f"🎉 Test Passed: All UI and API values are in the range: {risk_options}")
        print(f"🧮 Total validated values: UI - {len(ui_risk_values)}, API - {len(api_risk_values)}")

    except Exception as e:
        print(f"Error during 'Risk Filter Selection' Test: {e}")
        raise


def test_risk_filter_selection_medium(login_page, dashboard_page, rtd_page, risk_options=None):
    """Test to verify that the 'Risk' filter works correctly with risk options "Medium Risk" """

    if risk_options is None:
        risk_options = ["Medium Risk"]
    try:
        # Step 1: Log in and navigate to the RTD page and seelect a custom date
        test_custom_date_range_filter(login_page, dashboard_page, rtd_page)

        # Step 2: Open the filter menu
        rtd_page.open_filter_menu()
        print("Filter menu opened.")

        # Step 3: Select the 'Risk' filter section
        rtd_page.select_risk_section()
        print("Risk section opened.")

        # Step 4: Select the risk options Medium Risk
        print(f"Selecting the following risk options: {risk_options}...")
        rtd_page.select_risk_option(risk_options)  # Select each risk option from the list

        # Step 5: Apply the filter and intercept API for first page
        print("🎯 Applying filter and intercepting API...")
        first_page_response = rtd_page.intercept_response(
            "/api/v1/order/forward/get/data",
            trigger_action=rtd_page.apply_filter
        )

        # Step 6: Extract UI and API values
        print("🔍 Extracting values from UI and API...")
        api_risk_values, ui_risk_values = rtd_page.get_all_risk_column_values(
            first_page_response=first_page_response,
            parent_key="order_risk",
            target_ui_key="title"
        )

        # Step 7: Validate that all risk values are the range
        print("🔒 Validating UI and API values...")

        # Validate UI Amounts
        for risk_value in ui_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"UI Risk value '{risk_value}' does not match any selected option!"

        # Validate API Amounts
        for risk_value in api_risk_values:
            assert any(option in risk_value for option in
                       risk_options), f"API Risk value '{risk_value}' does not match any selected option!"

        print(f"🎉 Test Passed: All UI and API values are in the range: {risk_options}")
        print(f"🧮 Total validated values: UI - {len(ui_risk_values)}, API - {len(api_risk_values)}")

    except Exception as e:
        print(f"Error during 'Risk Filter Selection' Test: {e}")
        raise


# def test_export_table_and_verify_csv(login_page, dashboard_page, rtd_page):
#     """Test to export the table, download the report, and verify the CSV data."""
#
#     try:
#         # Step 1: Log in and navigate to the RTD page and select custom date
#         test_custom_date_range_filter(login_page, dashboard_page, rtd_page)
#
#         # Step 2: Trigger the export
#         #
#         # Step 3 and download the report
#         print("Exporting the report and downloading...")
#         download_dir = "path/to/your/download/directory"  # Set your download directory path here
#         downloaded_file_path = rtd_page.download_report(download_dir)  # Trigger export and get the file path
#
#         # Step 3: Verify the downloaded CSV file
#         rtd_page.verify_csv_data(downloaded_file_path)  # Verify the contents of the downloaded CSV file
#
#         print("✅ Export and CSV verification completed successfully!")
#
#     except Exception as e:
#         print(f"Error during Export and CSV Verification Test: {e}")
#         raise

# Run the test manually in pytest
if __name__ == "__main__":
    pytest.main()
