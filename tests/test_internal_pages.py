import os
import pytest
from playwright.sync_api import Page, expect
from pages.internal_page import USearchListPage, ContentPage

BASE_URL = os.getenv("BASE_URL", "https://uat-frontend.constitutionalcourt.or.th")
if BASE_URL.endswith("/th/Home"):
    BASE_URL = BASE_URL[:-8]

# List of Search List URLs to test
search_list_urls = [
    f"{BASE_URL}/th/USearchList?cat=7&subcat=33,",  # คำวินิจฉัยกลาง
    f"{BASE_URL}/th/USearchList?cat=7&subcat=11,",  # ข่าวประชาสัมพันธ์
]

# List of Content Details URLs to test
content_urls = [
    f"{BASE_URL}/th/Content/Detail/BackgroundoftheConstitutionalCourtOffice", # ความเป็นมา
    f"{BASE_URL}/th/Content/Detail/ConstitutionalCourtjudges", # คณะตุลาการ
]

@pytest.mark.parametrize("url", search_list_urls)
def test_search_list_page_loads(page: Page, url: str):
    """
    Test that USearchList pages load successfully and display the main heading.
    """
    search_page = USearchListPage(page)
    search_page.navigate(url)
    
    # Wait for the heading to be visible
    expect(search_page.page_heading).to_be_visible(timeout=10000)
    
    # Assert it contains 'U Search'
    heading_text = search_page.get_heading_text()
    assert "U Search" in heading_text, f"Expected 'U Search' in heading, got '{heading_text}'"

@pytest.mark.parametrize("url", content_urls)
def test_content_page_loads(page: Page, url: str):
    """
    Test that Content Detail pages load successfully and display a title.
    """
    content_page = ContentPage(page)
    content_page.navigate(url)
    
    # Wait for the content container to be visible
    expect(content_page.content_container).to_be_visible(timeout=10000)
    
    # Ensure there is a title present
    title_text = content_page.get_content_title()
    assert len(title_text) > 0, "Content title should not be empty"
