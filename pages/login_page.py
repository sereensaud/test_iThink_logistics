from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        """Initialize with the Playwright page and define selectors for login elements."""
        super().__init__(page)

        # ========================
        # Locators for Login Page
        # ========================

        # Input fields
        self.email_input = "input[type='email']"  # Locator for the email input field
        self.password_input = "input[type='password']"  # Locator for the password input field

        # Buttons
        self.login_button = "button:has-text('Log In')"  # Locator for the login button

        # Error messages
        self.login_error_message = "div.error-message:has-text('Invalid credentials')"  # Locator for error message when login fails

    def login(self, email: str, password: str):
        """Fill in the login form with email and password, then click the login button."""
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def wait_for_login_form(self):
        """Wait for the email input field to appear, confirming the login form is loaded."""
        self.wait_for_selector(self.email_input, timeout=10000)  # Wait for the email input to appear
        self.wait_for_selector(self.password_input, timeout=10000)  # Wait for the password input to appear

    def wait_for_error_message(self):
        """Wait for the error message to appear when login fails."""
        self.wait_for_selector(self.login_error_message, timeout=10000)  # Wait for error message if login fails
