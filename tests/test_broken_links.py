import os
import urllib.request
import urllib.error
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest
from playwright.sync_api import Page

BASE_URL = os.getenv("BASE_URL", "https://uat-frontend.constitutionalcourt.or.th")
if BASE_URL.endswith("/th/Home"):
    BASE_URL = BASE_URL[:-8]

def check_url(url: str):
    """
    Helper function to send a HEAD or GET request and return the URL and error if any.
    """
    # Fix spaces in URL
    url = urllib.parse.quote(url, safe=":/?&=")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    req.get_method = lambda: 'HEAD'
    
    try:
        urllib.request.urlopen(req, timeout=10, context=ctx)
        return None
    except urllib.error.HTTPError as e:
        # If HEAD is not allowed (405) or forbidden (403), fallback to GET
        if e.code in (405, 403):
            req.get_method = lambda: 'GET'
            try:
                urllib.request.urlopen(req, timeout=10, context=ctx)
                return None
            except urllib.error.HTTPError as e_get:
                return f"{url} (Status: {e_get.code})"
            except Exception as e_get2:
                return f"{url} (Error: {str(e_get2)})"
        return f"{url} (Status: {e.code})"
    except Exception as e:
         return f"{url} (Error: {str(e)})"

def test_no_broken_links_on_home_page(page: Page):
    """
    Test that navigates to the home page, extracts all links, 
    and verifies that none of them return a 4xx or 5xx status code.
    """
    page.goto(f"{BASE_URL}/th/Home", wait_until="domcontentloaded")
    
    # Extract all links
    links = page.locator("a").all()
    urls_to_check = set()
    
    # Known external links that block bots (403) or internal IP links that timeout
    IGNORED_URLS = [
        "https://workd.go.th/",
        "http://172.16.10.52",
        "https://ihub.constitutionalcourt.or.th/landing/main"
    ]
    
    for link in links:
        href = link.get_attribute("href")
        if not href:
            continue
        href = href.strip()
        
        # Filter out javascript, anchors, email, tel, and placeholders
        if href.startswith(("javascript:", "mailto:", "tel:", "#")) or href == "":
            continue
            
        # Convert relative URLs to absolute URLs
        if href.startswith("/"):
            href = f"{BASE_URL}{href}"
            
        # Strip URL fragments before checking
        href = href.split('#')[0]
            
        # Only check http/https links and not in ignored list
        if href.startswith("http"):
            if not any(href.startswith(ignored) for ignored in IGNORED_URLS):
                urls_to_check.add(href)
            
    broken_links = []
    
    # Use ThreadPoolExecutor to check URLs in parallel and speed up the test
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls_to_check}
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                broken_links.append(result)
                
    # Assert that no broken links were found
    assert not broken_links, f"Found {len(broken_links)} broken links:\n" + "\n".join(broken_links)
