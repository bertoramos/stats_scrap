
from bs4 import BeautifulSoup
from _scrapper import *

def scrape_data(raw_content: str, url_type: str) -> dict:
    # Lógica de scrapping aquí
    soup = BeautifulSoup(raw_content, 'html.parser')
    
    match url_type:
        case "ISTAC_SURVEY":
            return istac_survey_scrapper(soup)
        case _:
            return {"error": "Tipo de URL no soportado"}