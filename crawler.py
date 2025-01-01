# Crawler functionalities:
# Crawl (=get and parse) all HTML pages on a certain server 
# that can directly or indirectly be reached from a start URL 
# by following links on the pages. 
# Do not follow links to URLs on other servers and only process HTML responses. 
# Test the crawler with a simple website, e.g., https://vm009.rz.uos.de/crawl/index.html 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_server_url(full_url):
    """Extract the base server URL."""
    if not full_url.startswith(('http://', 'https://')):
        full_url = 'http://' + full_url 
    parsed_url = urlparse(full_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def crawl(url):
    visited = set()  # Track visited URLs
    to_visit = [url]  # Queue of URLs to visit

    # until there are no more URLs to visit
    while to_visit:
        current_url = to_visit.pop(0)
         # Skip already visited URLs
        if current_url in visited:
            continue 
        
        visited.add(current_url)

        #print(f"Crawling: {current_url}")

        try:
            response = requests.get(current_url)

            # Parse the current page
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a")

            for link in links:
                href = link.get("href")
                if href:
                    full_url = urljoin(response.url, href) 

                    if full_url not in visited:
                        if full_url.startswith(get_server_url(url)):
                        #only add html pages to the queue
                            if "text/html" in response.headers.get("Content-Type", ""):
                                to_visit.append(full_url)
                                
                                                        
        except:
            continue
            

# Test URL
url = "https://vm009.rz.uos.de/crawl/index.html"
crawl(url)

