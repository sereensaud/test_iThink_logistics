import os
import pytest
from playwright.sync_api import sync_playwright
from datetime import datetime
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.rtd_page import RTDPage


# Fixture to create a directory dynamically and enable video and tracing
@pytest.fixture(scope="session")
def browser():
    """Set up the Playwright browser instance, which is shared across all tests."""

    # Get the current timestamp to create unique directories for tracing and video
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create directories for storing trace and video data with the current timestamp
    trace_dir = f"trace/{current_time}"
    video_dir = f"videos/{current_time}"

    # Create the directories if they do not already exist
    os.makedirs(trace_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    # Start a Playwright session with a Chromium browser instance
    # Launch the browser in non-headless mode (you can change it to True for headless mode)
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)  # Set headless=True for non-UI mode (e.g., CI/CD environments)

        # # # Launch Firefox instead of Chromium
        # # browser = p.firefox.launch(headless=False)  # Set to True for headless mode
        #
        # # Launch Microsoft Edge (Chromium-based)
        # # Playwright uses the `chromium` API for Edge as it is Chromium-based
        # browser = p.chromium.launch(headless=False)  # Set to True for headless mode

        # Set up a new browser context that records video and tracing
        context = browser.new_context(
            record_video_dir=video_dir  # Specify the directory for saving recorded videos
        )

        # Start tracing for the context, capturing screenshots and snapshots
        context.tracing.start(screenshots=True, snapshots=True)

        # Yield the browser and context to the test functions
        yield browser, context

        # After tests complete, stop tracing and save it to a zip file
        context.tracing.stop(path=f"{trace_dir}/trace.zip")  # Trace file is saved as a .zip

        # Close the browser instance after the test session is done
        browser.close()


# Fixture to create a new page object for each test
@pytest.fixture
def page(browser):
    """Create a new page object with the browser context."""

    # Unpack the browser and context passed from the 'browser' fixture
    browser, context = browser

    # Create a new page in the browser context (essentially a new tab or window)
    page = context.new_page()

    # Yield the page object for the test function to use
    yield page

    # Close the page once the test completes
    page.close()


# Fixtures for interacting with different pages on the website

# Fixture to initialize and interact with the login page
@pytest.fixture
def login_page(page):
    """Provide LoginPage object for interacting with the login page."""

    # Return a LoginPage instance with the provided page object
    return LoginPage(page)


# Fixture to initialize and interact with the dashboard page
@pytest.fixture
def dashboard_page(page):
    """Provide DashboardPage object for interacting with the dashboard page."""

    # Return a DashboardPage instance with the provided page object
    return DashboardPage(page)


# Fixture to initialize and interact with the RTD (Ready To Dispatch) page
@pytest.fixture
def rtd_page(page):
    """Provide RTDPage object for interacting with the RTD page."""

    # Return an RTDPage instance with the provided page object
    return RTDPage(page)


# Define a fixture to handle the download directory
@pytest.fixture
def download_dir(tmp_path):
    """Fixture to create a temporary directory for downloads."""
    download_path = tmp_path / "downloads"
    os.makedirs(download_path, exist_ok=True)
    return download_path