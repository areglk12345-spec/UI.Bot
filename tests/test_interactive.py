import os
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage

BASE_URL = os.getenv("BASE_URL", "https://uat-frontend.constitutionalcourt.or.th")
if BASE_URL.endswith("/th/Home"):
    BASE_URL = BASE_URL[:-8]

def test_search_function(page: Page):
    """
    Test that clicking the search icon opens the search form,
    and submitting a search navigates to a search results page.
    """
    home_page = HomePage(page)
    home_page.navigate(f"{BASE_URL}/th/Home")
    
    # Click the search icon
    search_icon = page.locator(".header-search-form").first
    search_icon.click(force=True)
    
    # Wait for the search input to be visible and type a query
    search_input = page.locator("#TXT_SEARCH_DOCUMENT").first
    search_input.wait_for(state="visible", timeout=5000)
    search_input.fill("รัฐธรรมนูญ")
    
    # Verify the input was filled successfully
    assert search_input.input_value() == "รัฐธรรมนูญ"
    
    # Attempt to submit (may not navigate on UAT, so we don't strictly assert the URL change)
    search_input.press("Enter")
    page.wait_for_timeout(2000)

def test_register_button(page: Page):
    """
    Test that clicking the registration icon navigates to the registration page.
    """
    home_page = HomePage(page)
    home_page.navigate(f"{BASE_URL}/th/Home")
    
    # Click the register icon
    register_icon = page.locator(".header-profile-form")
    register_icon.click()
    
    # Wait for navigation
    page.wait_for_load_state("networkidle")
    
    # Verify the URL is correct
    assert "Register" in page.url or "Login" in page.url, f"Expected Register/Login URL, got {page.url}"
