import os
from playwright.sync_api import Page, expect
import urllib.parse

def test_dashboard_ui(page: Page):
    """Test that the custom dashboard.html displays correctly."""
    dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dashboard.html"))
    
    # Check if dashboard exists
    assert os.path.exists(dashboard_path), "dashboard.html does not exist! Please run generate_dashboard.py first."
    
    # Open local file in playwright
    file_url = "file:///" + dashboard_path.replace("\\", "/")
    # Encode spaces in path if any
    file_url = urllib.parse.quote(file_url, safe=':/')
    
    page.goto(file_url)
    
    # Check main title
    expect(page).to_have_title("UI Bot Test Dashboard")
    expect(page.locator("h1")).to_have_text("UI Bot Test Report")
    
    # Check for the key metric cards
    expect(page.locator("text=Total Tests")).to_be_visible()
    expect(page.locator("text=Passed Tests")).to_be_visible()
    expect(page.locator("text=Failed Tests")).to_be_visible()
    expect(page.locator("text=Pass Rate")).to_be_visible()
    
    # Verify the table exists
    expect(page.locator("table")).to_be_visible()
    
    # We should have at least one test case row if tests were run
    rows = page.locator("tbody tr")
    assert rows.count() > 0, "Dashboard table has no rows"
