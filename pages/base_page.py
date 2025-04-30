from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        """Initialize the page object with the Playwright page."""
        self.page = page
        # Maximize the window by setting a large viewport size
        self.page.set_viewport_size({"width": 1840, "height": 1080})  # Simulating a maximized window
        print("Browser window maximized to 1920x1080.")

    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)

    def fill(self, selector: str, value: str):
        """Fill an input field identified by the selector with the given value."""
        self.page.fill(selector, value)

    def click(self, selector: str):
        """Click an element identified by the selector."""
        self.page.click(selector)

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """Wait for an element to appear within the specified timeout."""
        self.page.wait_for_selector(selector, timeout=timeout)

    def is_visible(self, selector: str) -> bool:
        """Check if an element identified by the selector is visible."""
        return self.page.locator(selector).is_visible()

    def get_text(self, selector: str):
        """Get the text content of an element."""
        return self.page.inner_text(selector)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """
        Wait for an element to be visible before interacting with it.
        This ensures that the element is ready for interaction.
        """
        self.page.wait_for_selector(selector, timeout=timeout)

    def select_option(self, selector: str, value: str):
        """Select an option from a dropdown (select element) by its value."""
        self.page.select_option(selector, value=value)
        print(f"Selected option '{value}' in the dropdown identified by {selector}")

    def intercept_response(self, url_substring: str, method: str = "POST", trigger_action=None):
        """
        Intercept a network response matching the given URL substring and HTTP method.

        Args:
            url_substring (str): A substring that should be present in the intercepted request URL.
            method (str): HTTP method to match (default is POST).
            trigger_action (Callable): A function that triggers the network request (e.g., clicking a button).

        Returns:
            Response object: The intercepted response.
        """
        with self.page.expect_response(
                lambda response: url_substring in response.url and response.request.method == method
        ) as intercepted:
            if trigger_action:
                trigger_action()
        return intercepted.value

