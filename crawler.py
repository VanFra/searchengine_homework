import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser


def get_server_url(full_url):
    """Extract the base server URL."""
    if not full_url.startswith(('http://', 'https://')):
        full_url = 'http://' + full_url
    parsed_url = urlparse(full_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def initialize_index(index_dir="index"):
    """Initialize or open Whoosh index."""
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        # Define schema with stemming analyzer
        schema = Schema(
        url=ID(stored=True, unique=True),
        title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
        content=TEXT(stored=True, analyzer=StemmingAnalyzer())
        )
        return create_in(index_dir, schema)
    else:
        return open_dir(index_dir)


def crawl(url, index_dir="index", max_depth=3):
    visited = set()  # Track visited URLs
    to_visit = [(url, 0)]  # Queue of URLs to visit, with depth 0
    ix = initialize_index(index_dir)
    writer = ix.writer()

    while to_visit:
        current_url, current_depth = to_visit.pop(0)

        # Skip if already visited or depth exceeded
        if current_url in visited or current_depth > max_depth:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url)

            # Parse the current page
            if "text/html" in response.headers.get("Content-Type", ""):
                soup = BeautifulSoup(response.content, "html.parser")
                links = soup.find_all("a")

                # Extract content
                page_text = soup.get_text() if soup.get_text() else ""
                title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

                # Ensure content length doesn't exceed reasonable limits
                if len(page_text) > 1_000_000:  # Limit content size to 1MB
                    page_text = page_text[:1_000_000]

                # Check if the URL is already indexed
                with ix.searcher() as searcher:
                    query = QueryParser("url", ix.schema).parse(current_url)
                    existing_results = searcher.search(query)

                    if not existing_results:
                        writer.add_document(url=current_url, title=title, content=page_text)

                # Add new links to the queue
                for link in links:
                    href = link.get("href")
                    if href:
                        full_url = urljoin(response.url, href)
                        # only include links that werent visited and are on the same server
                        if full_url not in visited and full_url.startswith(get_server_url(url)):
                            to_visit.append((full_url, current_depth + 1))

        # if server issues occur (broken links, timeout etc.) the link is skipped
        except requests.exceptions.RequestException:
            continue

    writer.commit()


def search_index(query_str, index_dir="index"):
    """Search the Whoosh index."""
    index = open_dir(index_dir)
    results_list = []
        
    # Parse the user query string
    qp = QueryParser("content", index.schema)
    query = qp.parse(query_str)

    with index.searcher() as searcher:
        # correct any spelling mistakes
        corrected = searcher.correct_query(query, query_str)
        if corrected.query != query:
            query = corrected.query  
    
        # Perform the search with the (possibly corrected) query
        results = searcher.search(query)
        
        for result in results:
            results_list.append({
                "url": result["url"],  
                "title": result["title"],
                "content": result["content"][:150]  
            })
    
    return results_list


# Test the crawler and search functionality
# url = "https://vm009.rz.uos.de/crawl/index.html"
# crawl(url, index_dir="index")
# test with spelling mistake
# search_index("platapus", index_dir="index")

