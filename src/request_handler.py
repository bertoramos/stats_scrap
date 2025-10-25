import logging
import time
from tqdm import tqdm
from playwright.sync_api import sync_playwright
from config import get_settings

def fetch_page_content(url: str) -> str:
    """
    Descarga el HTML renderizado dinámicamente por JS usando Playwright,
    con reintentos y logging similares a requests.
    """
    settings = get_settings()
    retry_attempts = settings.retry_attempts
    timeout_seconds = settings.timeout_seconds

    for attempt in range(retry_attempts):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=timeout_seconds * 1000)  # timeout en ms
                
                # Estrategia genérica: esperar a que la página esté completamente cargada
                try:
                    # 1. Esperar a que no haya más requests de red activos (más confiable que sleep)
                    page.wait_for_load_state('networkidle', timeout=10000)
                except:
                    # 2. Fallback: esperar a que el DOM esté completo
                    page.wait_for_load_state('domcontentloaded', timeout=5000)
                
                html = page.content()
                browser.close()
                return html
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(0.25)  # evitar sobrecargar el servidor

    logging.error(f"Failed to fetch {url} after {retry_attempts} attempts")
    return ""
