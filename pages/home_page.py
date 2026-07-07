from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators
        self.search_button = page.get_by_role("button", name="ค้นหา")
        self.search_input = page.get_by_placeholder("ค้นหา", exact=False)
        self.en_lang_button = page.locator("a.text-light-gray", has_text="EN").first
        
        # Elements to mask during visual regression
        self.image_mask = page.locator("img")
        self.video_mask = page.locator("video")
        
    def open(self, url: str):
        self.navigate(url)
        
    def perform_search(self, keyword: str):
        """Click the search button, fill in the keyword, and press enter."""
        self.search_button.click()
        # Ensure the input is visible before interacting
        self.search_input.wait_for(state="visible")
        self.search_input.fill(keyword)
        self.search_input.press("Enter")
        # Wait for potential navigation or network requests
        self.page.wait_for_load_state("networkidle")

    def switch_to_english(self):
        """Click the EN language switch button."""
        if self.en_lang_button.is_visible():
            self.en_lang_button.click()
            self.page.wait_for_load_state("networkidle")
        
    def click_menu(self, menu_name: str):
        """Click a menu item by its text."""
        menu = self.page.locator("a.nav-link", has_text=menu_name).first
        if menu.is_visible():
            menu.click()
            self.page.wait_for_load_state("networkidle")
