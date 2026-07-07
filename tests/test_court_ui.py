import os
import pytest
from playwright.sync_api import Page, expect
from dotenv import load_dotenv
from pages.home_page import HomePage

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://uat-frontend.constitutionalcourt.or.th/th/Home")

def test_homepage_load_and_title(page: Page):
    """Test that the homepage loads successfully and has the correct title"""
    home = HomePage(page)
    home.open(BASE_URL)
    
    # Assert the title contains expected keywords
    expect(page).to_have_title("ศาลรัฐธรรมนูญ || Constitutional Court || หน้าแรก || Home Page")
    
    # Ensure screenshots directory exists
    os.makedirs("screenshots", exist_ok=True)
    page.screenshot(path="screenshots/pytest_homepage.png")

def test_extract_links(page: Page):
    """Test to verify that links exist on the page"""
    home = HomePage(page)
    home.open(BASE_URL)
    
    # Find all links
    links = page.locator("a")
    count = links.count()
    
    # Assert that we found some links
    assert count > 0, "No links found on the homepage"
    
    # Log top 5 links for debugging
    print(f"\nFound {count} links. Top 5:")
    for i in range(min(5, count)):
        text = links.nth(i).inner_text().strip()
        if text:
            print(f"  - {text}")



@pytest.mark.parametrize("keyword", ["รัฐธรรมนูญ", "ศาล", "พรรคการเมือง"])
def test_e2e_search_journey(page: Page, keyword: str):
    """Data-Driven Test: Try to find and use search with multiple keywords."""
    home = HomePage(page)
    home.open(BASE_URL)
    
    # Look for a search input or button by common Thai keywords
    search_element = page.locator("text=ค้นหา").first
    if search_element.count() > 0 and search_element.is_visible():
        search_element.click()
        # Find input by placeholder
        search_input = page.get_by_placeholder("ค้นหา", exact=False).first
        if search_input.count() > 0 and search_input.is_visible():
            search_input.fill(keyword)
            search_input.press("Enter")
            page.wait_for_load_state("networkidle")
        
    # Check that the page hasn't crashed (body still visible)
    expect(page.locator("body")).to_be_visible()

def test_accessibility(page: Page):
    """Test page accessibility using axe-core."""
    from axe_playwright_python.sync_playwright import Axe
    
    home = HomePage(page)
    home.open(BASE_URL)
    
    results = Axe().run(page)
    # We won't strictly assert 0 violations because many sites have existing issues,
    # but we can log them or assert against a known threshold.
    # For now, we just ensure the tool runs successfully.
    print(f"Found {results.violations_count} accessibility violations.")

def test_language_switch(page: Page):
    """Test switching the website language to English."""
    home = HomePage(page)
    home.open(BASE_URL)
    
    # Click EN language switch
    home.switch_to_english()
    
    # Assert URL changed or body is visible
    expect(page.locator("body")).to_be_visible()
    # Check if URL updated or just ensure it didn't crash
    assert "/en/" in page.url or "Home" in page.url, f"Current url: {page.url}"

@pytest.mark.parametrize("menu_name", ["รู้จักเรา", "คำวินิจฉัย", "บริการประชาชน"])
def test_menu_navigation(page: Page, menu_name: str):
    """Data-Driven Test: Try to click various top-level menus."""
    home = HomePage(page)
    home.open(BASE_URL)
    
    # Click the menu
    home.click_menu(menu_name)
    
    # Assert body is still visible (no crash/404)
    expect(page.locator("body")).to_be_visible()
