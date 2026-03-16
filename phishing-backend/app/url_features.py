"""
url_features.py
----------------
Extracts the 23 classical URL-based phishing detection features.
These match the Kaggle dataset used in your research.

Output: A list of numeric values in FIXED ORDER:
[
    NumDots, SubdomainLevel, PathLevel, UrlLength, NumDash,
    NumDashInHostname, AtSymbol, TildeSymbol, NumUnderscore,
    NumPercent, NumQueryComponents, NumAmpersand, NumHash,
    NumNumericChars, NoHttps, IpAddress, DomainInSubdomains,
    DomainInPaths, HttpsInHostname, HostnameLength, PathLength,
    QueryLength, DoubleSlashInPath
]
"""

import re
import tldextract
from urllib.parse import urlparse


def count_occurrences(s, char):
    return s.count(char)


def extract_features(url):

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    ext = tldextract.extract(url)
    subdomain = ext.subdomain
    domain = ext.domain
    registered_domain = ext.registered_domain

    # INDIVIDUAL FEATURE EXTRACTION

    # 1. Number of dots
    NumDots = hostname.count(".")

    # 2. Subdomain Level
    SubdomainLevel = 0 if subdomain == "" else len(subdomain.split("."))

    # 3. Path Level
    PathLevel = 0 if path == "" else len([p for p in path.split("/") if p])

    # 4. URL Length
    UrlLength = len(url)

    # 5. Number of dash in URL
    NumDash = url.count("-")

    # 6. Number of dash in hostname
    NumDashInHostname = hostname.count("-")

    # 7. Presence of '@'
    AtSymbol = 1 if "@" in url else 0

    # 8. Presence of '~'
    TildeSymbol = 1 if "~" in url else 0

    # 9. Number of '_'
    NumUnderscore = url.count("_")

    # 10. Number of '%'
    NumPercent = url.count("%")

    # 11. Number of query components (split by '&')
    NumQueryComponents = len(query.split("&")) if query else 0

    # 12. Number of '&'
    NumAmpersand = query.count("&")

    # 13. Number of '#'
    NumHash = url.count("#")

    # 14. Number of numeric characters
    NumNumericChars = sum(c.isdigit() for c in url)

    # 15. No HTTPS (1 if http, 0 if https)
    NoHttps = 1 if parsed.scheme != "https" else 0

    # 16. IP Address in URL
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    IpAddress = 1 if re.match(ip_pattern, hostname) else 0

    # 17. Domain found inside subdomain?
    DomainInSubdomains = 1 if domain in subdomain else 0

    # 18. Domain found inside path?
    DomainInPaths = 1 if domain in path else 0

    # 19. 'https' found inside hostname? (fake HTTPS)
    HttpsInHostname = 1 if "https" in hostname else 0

    # 20. Hostname length
    HostnameLength = len(hostname)

    # 21. Path length
    PathLength = len(path)

    # 22. Query length
    QueryLength = len(query)

    # 23. Double slash in path? ("//path")
    DoubleSlashInPath = 1 if "//" in path else 0

    # RETURN VALUES IN FIXED ORDER
    return [
        NumDots,
        SubdomainLevel,
        PathLevel,
        UrlLength,
        NumDash,
        NumDashInHostname,
        AtSymbol,
        TildeSymbol,
        NumUnderscore,
        NumPercent,
        NumQueryComponents,
        NumAmpersand,
        NumHash,
        NumNumericChars,
        NoHttps,
        IpAddress,
        DomainInSubdomains,
        DomainInPaths,
        HttpsInHostname,
        HostnameLength,
        PathLength,
        QueryLength,
        DoubleSlashInPath
    ]
