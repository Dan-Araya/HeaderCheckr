from flask import Blueprint, request, jsonify
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