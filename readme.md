# Platypus Search Engine

A basic web crawler and search engine built using Python, Flask, and Whoosh. This project demonstrates how to crawl a website, index its content, and search through the indexed data, within a given server.

## Features

- **Web Crawling**: Crawl a given website to fetch and index its content.
- **Text Indexing**: Store and index crawled content using the Whoosh library.
- **Search Functionality**: Search the indexed content with query correction for potential typos.
- **Web Interface**: Interact with the crawler and search functionality through a Flask-powered web interface.

## Prerequisites

- Python 3.8 or later
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start the Flask Server

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

### Crawling

- To crawl a website, provide a URL in the web interface or use the default seed URL (`https://vm009.rz.uos.de/crawl/index.html`).

### Searching

- Enter a search query in the web interface to search through the indexed content. The application supports query correction for typos.

## File Structure

```
.
├── app.py               # Flask application
├── crawler.py           # Crawling and search logic
├── templates/
│   ├── home.html        # Homepage template
│   ├── results.html     # Search results template
├── static/              # Static files (CSS, JS, etc.)
├── index/               # Whoosh index directory
└── requirements.txt     # Python dependencies
```

## Dependencies

- Flask: Web framework
- BeautifulSoup: HTML parsing
- Whoosh: Full-text search and indexing
- Requests: HTTP requests

## Limitations

- **Scalability**: Not designed for large-scale crawling or indexing.
- **Content Size**: Limits content size to 1MB per page.
- **Local Scope**: Only crawls pages on the same server as the seed URL.

## Future Improvements

- Enhance error handling during crawling.
- Add support for distributed crawling and indexing.
- Improve the UI for search results.

## Acknowledgments

- [Whoosh Documentation](https://whoosh.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
