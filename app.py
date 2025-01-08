from flask import Flask, request, jsonify, render_template
from crawler import crawl, search_index
import os

app = Flask(__name__)

# Default Whoosh index directory
INDEX_DIR = "index"

@app.route("/")
def home():
    """Render the homepage with a search form."""
    return render_template("home.html")

@app.route("/crawl", methods=["POST"])
def crawl_url():
    """Crawl a given URL."""
    url = request.form.get("url")
    seed = "https://vm009.rz.uos.de/crawl/index.html"
    if url:
        crawl(url, index_dir=INDEX_DIR)
        return f"Crawled URL: {url}", 200
    else:
        crawl(seed, index_dir=INDEX_DIR)
        return "No URL provided", 400


@app.route("/search", methods=["GET"])
def search():
    """API to search the indexed content."""
    query = request.args.get("query")
    if query:
        if not os.path.exists(os.path.join(INDEX_DIR, "segments")):  # Check if the index directory exists
            # Trigger crawl with the seed URL if the index doesn't exist yet
            crawl_url()
        # Get structured results from `search_index`
        results = search_index(query, index_dir=INDEX_DIR)
        return render_template("results.html", query=query, results=results)
    
    else:
        return jsonify({"error": "No query provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)
