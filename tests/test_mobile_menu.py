import os
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage

BASE_URL = os.getenv("BASE_URL", "https://uat-frontend.constitutionalcourt.or.th")
if BASE_URL.endswith("/th/Home"):
    BASE_URL = BASE_URL[:-8]

def test_mobile_menu_toggle(page: Page):
    """
    Test that the hamburger menu works on mobile viewports.
    """
    # Resize viewport to a mobile resolution (e.g., iPhone X: 375x812)
    page.set_viewport_size({"width": 375, "height": 812})
    
    home_page = HomePage(page)
    home_page.navigate(f"{BASE_URL}/th/Home")
    
    # Locate the visible hamburger menu button
    hamburger_btn = page.locator("button.navbar-toggler:visible").first
    
    # Locate the collapsible menu container
    navbar_menu = page.locator("#navbarNav")
    
    # Click to expand
    hamburger_btn.click(force=True)
    
    # Wait for the menu to animate and become visible
    # On mobile, the Bootstrap collapse menu gets the 'show' class
    page.wait_for_function('document.querySelector("#navbarNav").classList.contains("show")', timeout=5000)
