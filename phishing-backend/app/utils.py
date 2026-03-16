"""
utils.py
--------
Common utilities for safe fetching + HTML parsing + domain parsing.

This is the backbone for all other feature extraction modules.
Handles:
 - Safe HTTP GET requests
 - Timeouts
 - Redirect limiting
 - Proper headers
 - HTML parsing helper
 - Domain extraction helper
"""

import requests
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urlparse


# Configuration

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

MAX_REDIRECTS = 5
REQUEST_TIMEOUT = 6


# Safe Fetch Function

def safe_get(url, timeout=REQUEST_TIMEOUT, max_redirects=MAX_REDIRECTS):
    """
    Safely fetch a webpage with:
      - timeout
      - redirect limit
      - custom headers
      - safe failure handling

    RETURNS:
        (status_code, final_url, html_text, response_headers)

    Raises exceptions only if absolutely necessary.
    All higher modules should handle failures gracefully.

    NOTE:
      - Never let malicious pages load resources
      - Never execute JS
    """
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        resp = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=timeout,
            allow_redirects=True
        )

        if len(resp.history) > max_redirects:
            return (
                resp.status_code,
                resp.url,          
                resp.text,
                resp.headers
            )

        return (
            resp.status_code,
            resp.url,
            resp.text,
            resp.headers
        )

    except requests.exceptions.Timeout:
        return (408, url, "", {})  

    except requests.exceptions.TooManyRedirects:
        return (310, url, "", {}) 

    except Exception as e:
        return (500, url, "", {})



def make_soup(html_text):
    """
    Converts HTML text into a BeautifulSoup object.
    If HTML is empty, returns an empty soup.
    """
    if not html_text:
        return BeautifulSoup("", "lxml")
    return BeautifulSoup(html_text, "lxml")


def extract_domain(url):
    """
    Extracts the registered domain (example.com).
    Returns empty string if extraction fails.
    """
    try:
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    except:
        return ""

def extract_hostname(url):
    """
    Extracts hostname from URL using urlparse.
    """
    try:
        return urlparse(url).hostname or ""
    except:
        return ""
