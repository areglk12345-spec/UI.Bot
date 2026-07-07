from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
