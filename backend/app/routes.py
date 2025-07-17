from flask import Blueprint, request, jsonify
from .analyzer.fetcher import get_headers

bp = Blueprint('main', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        headers = get_headers(url)
        return jsonify({"headers": headers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
