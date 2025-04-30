# This page object represents the dashboard page that appears after logging in.
# It waits for elements that indicate the login was successful.
from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        """Initialize with the Playwright page and define selectors for dashboard elements."""
        super().__init__(page)
        self.create_order_button = "button:has-text('Create Order')"
        self.welcome_text = "h1:text('Welcome iThink Logistics!')"

    def wait_for_dashboard_to_load(self):
        """Wait for either the 'Welcome' text or the 'Create Order' button to appear, confirming the dashboard is loaded."""
        try:
            self.wait_for_selector(self.welcome_text, timeout=10000)
        except:
            # If 'Welcome' text is not found, check for the 'Create Order' button
            self.wait_for_selector(self.create_order_button, timeout=10000)
