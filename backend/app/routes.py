from flask import Blueprint, request, jsonify
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import time
import random
from .controllers.web_analysis_controller import perform_web_analysis
from .security.url_guard import is_url_safe

bp = Blueprint('main', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze_route():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400
    url = data['url']
    if not is_url_safe(url):
        return jsonify({"error": "Invalid URL"}), 400
    try:
        results, status = perform_web_analysis(url)
        return jsonify(results), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/extended-analyze', methods=['POST'])
def extended_analyze_route():
    """
    A. Takes the original URL entered by the user (https://example.com/contact)
    B. Analyzes that path with perform_web_analysis()
    C. Extracts the base domain (https://example.com)
    D. Downloads the HTML of the main page
    E. Scrapes internal links
    F. Normalizes, validates, and analyzes each subpath found
    G. Returns a JSON with:
    - main: result of the original URL
    - related: results of the subpaths found
    """
    # A. Takes the original URL entered by the user (https://example.com/contact)
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400

    url = data['url']
    if not is_url_safe(url):
        return jsonify({"error": "Invalid URL"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        # B. Analyzes that path with perform_web_analysis()
        main_result, status = perform_web_analysis(url)

        # C. Extracts the base domain (https://example.com)
        parsed_url = urlparse(url)
        root_path = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # D. Downloads the HTML of the main page
        response = requests.get(root_path, headers=headers, timeout=10)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'lxml')

        # E. Scrapes internal links
        anchor_elements = soup.find_all("a")
        script_count = len(soup.find_all("script"))
        special_tags = soup.find_all(["app-root", "main-app", "router-outlet"])

        related_results = []

        # F. Normalizes, validates, and analyzes each subpath found
        if (len(anchor_elements) < 4 and script_count < 4) or len(special_tags) > 0:
            print("⚠️ Sitio SPA detectado. No se analizarán subrutas.")
        else:
            visited = set()
            for element in anchor_elements:
                href = element.get('href')
                if not href:
                    continue

                absolute_url = urljoin(root_path, href)

                if urlparse(absolute_url).netloc != parsed_url.netloc:
                    continue
                if absolute_url in visited:
                    continue
                if not is_url_safe(absolute_url):
                    continue

                visited.add(absolute_url)
                time.sleep(random.uniform(2, 6.0))

                try:
                    result, _ = perform_web_analysis(absolute_url)
                    print(
                        f"✅ Subruta analizada: {absolute_url} → {result['evaluation']['score']} ({result['evaluation']['level']})")
                    related_results.append({
                        "url": absolute_url,
                        **result
                    })
                except Exception as e:
                    related_results.append({
                        "url": absolute_url,
                        "error": str(e)
                    })

        return jsonify({
            "main": {"url": url, **main_result},
            "related": related_results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500