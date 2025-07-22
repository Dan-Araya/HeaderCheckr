from ..analyzer.fetcher import get_headers
from ..analyzer.evaluator import evaluate_headers

def perform_web_analysis (url: str) -> dict:
    try:
        #TODO SSRF LOGIC
        headers = get_headers(url)
        evaluation = evaluate_headers(headers)
        return {"headers": headers, "evaluation" : evaluation}, 200

    except Exception as e:
        print(f"Error interno en perform_web_analysis: {e}")
