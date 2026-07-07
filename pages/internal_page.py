from playwright.sync_api import Page
from pages.base_page import BasePage

class USearchListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locator for the main heading or container of the search list page
        self.page_heading = page.locator("h2.text-red-new:has-text('U Search')")
        
    def get_heading_text(self):
        return self.page_heading.inner_text()


class ContentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locator for the main content container
        self.content_container = page.locator("div.blog-details")
        
    def get_content_title(self):
        # Some pages have title in h2, some have empty h2 and use h4.card-title
        h2_text = self.content_container.locator("h2").first.inner_text().strip()
        if h2_text:
            return h2_text
        
        # Fallback
        h4_locator = self.content_container.locator("h4")
        if h4_locator.count() > 0:
            return h4_locator.first.inner_text().strip()
            
        return ""
