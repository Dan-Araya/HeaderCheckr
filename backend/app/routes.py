from flask import Blueprint, request, jsonify
from .controllers.web_analysis_controller import perform_web_analysis

bp = Blueprint('main', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze_route():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400
    url = data['url']

    try:
        results = perform_web_analysis(url)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500