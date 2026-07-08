import csv
import os
import pytest
from playwright.sync_api import Page, expect

def load_urls():
    """Load URLs from the CSV file."""
    urls = []
    csv_path = os.path.join(os.path.dirname(__file__), "..", "urls_to_test.csv")
    
    if not os.path.exists(csv_path):
        return []
        
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("url") and row["url"].strip():
                urls.append((row["url"].strip(), row.get("description", "").strip()))
                
    return urls

urls_data = load_urls()

@pytest.mark.parametrize("url,description", urls_data, ids=[f"{desc}-{url}" for url, desc in urls_data])
def test_custom_url_load(page: Page, url: str, description: str):
    """
    Test that a custom URL from the CSV file loads successfully
    and does not return an error status code.
    """
    if not url:
        pytest.skip("Empty URL")
        
    print(f"\nChecking URL: {url} ({description})")
    
    # Go to the URL
    response = page.goto(url, timeout=30000, wait_until="domcontentloaded")
    
    # Assert that response is not None
    assert response is not None, f"Failed to load {url}"
    
    # Assert that the status is ok (200-299)
    assert response.ok, f"Error loading {url}. HTTP Status: {response.status}"
    
    # Assert that the page has a title
    title = page.title()
    print(f"Success! Page Title: {title}")
    assert title, f"Page {url} loaded but has no title."
