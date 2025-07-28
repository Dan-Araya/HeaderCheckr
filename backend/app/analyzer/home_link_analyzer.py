from bs4 import BeautifulSoup
import requests

from app.controllers.web_analysis_controller import perform_web_analysis


def home_link_analizer(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')

    anchor_elements = soup.find_all("a")
    script_count = len(soup.find_all("script"))
    special_tags = soup.find_all(["app-root", "main-app", "router-outlet"])

    if (len(anchor_elements)< 4 and script_count < 4) or len(special_tags) > 0:
        print("""⚠️ Este sitio utiliza tecnología SPA (Single Page Application).
        "Por ahora, sólo analizamos la ruta ingresada. Pronto incluiremos soporte completo para este tipo de sitios.""")

    else:
        for element in anchor_elements:
            perform_web_analysis(url)

home_link_analizer("https://www.bancoestado.cl/")