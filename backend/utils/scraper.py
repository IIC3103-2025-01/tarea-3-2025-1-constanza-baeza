
import requests
from bs4 import BeautifulSoup

def obtener_texto_articulo(url: str) -> str:
    """
    Descarga el HTML de la página de Wikipedia y extrae todos los párrafos
    del contenido principal, sin usar la API oficial.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    html = resp.text

    soup = BeautifulSoup(html, "lxml")

    cont_mw_id = soup.find("div", id="mw-content-text")
    if cont_mw_id:
        inner = cont_mw_id.find("div", class_="mw-parser-output")
        if inner:
            main_div = inner
        else:
            main_div = cont_mw_id
    else:
        main_div = soup.find("div", class_="mw-parser-output")

    if not main_div:
        main_div = soup.find("div", id="bodyContent")
    if not main_div:
        raise ValueError("No se encontró el contenedor principal de Wikipedia.")

    parrafos = []
    for p_tag in main_div.find_all("p"):
        texto = p_tag.get_text(strip=True)
        if len(texto) > 20:  
            parrafos.append(texto)

    if not parrafos:
        raise ValueError("El scraper no extrajo ningún párrafo válido del artículo.")

    return "\n\n".join(parrafos)
