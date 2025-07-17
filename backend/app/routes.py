from flask import Blueprint, request, jsonify
from .analyzer.fetcher import get_headers
from .analyzer.evaluator import evaluate_headers  # ✅ Agregado

bp = Blueprint('main', __name__)

@bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        headers = get_headers(url)
        evaluation = evaluate_headers(headers)  # ✅ Evaluamos seguridad
        return jsonify({"headers": headers, **evaluation}), 200  # ✅ Combinamos headers y análisis
    except Exception as e:
        return jsonify({"error": str(e)}), 500
