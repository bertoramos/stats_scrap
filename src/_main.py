import logging
from datetime import datetime
import os
from tqdm import tqdm

from config import get_settings

from request_handler import fetch_page_content
from scrapper import scrape_data
from save_data import save_dataframe

def setup_logging():
    """Configura el logging con timestamp en el nombre del archivo"""
    # Crear directorio de logs si no existe
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
    os.makedirs(log_dir, exist_ok=True)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'stats_scrap_{timestamp}.log'
    log_path = os.path.join(log_dir, log_filename)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8')
        ]
    )
    
    logging.info(f"Logging configurado. Archivo de log: {log_path}")
    return log_path

def main():
    # Configurar logging al inicio
    log_path = setup_logging()
    
    settings = get_settings()
    logging.info("Iniciando aplicación stats_scrap")
    logging.info(f"URLs configuradas: {settings.urls}")
    logging.info(f"Intentos de reintento: {settings.retry_attempts}")
    logging.info(f"Timeout: {settings.timeout_seconds} segundos")
    
    
    # Procesar URLs con barra de progreso
    for url in tqdm(settings.urls, desc="Procesando URLs", unit="url"):
        url_str = str(url.url)  # Convertir HttpUrl a string
        
        # Actualizar descripción de la barra de progreso
        tqdm.write(f"Procesando: {url_str}")
        
        content = fetch_page_content(url_str)
        if content:
            title, df = scrape_data(content, url.type)
            save_dataframe(title, df)
            tqdm.write(f"✅ Datos scrappeados para {url_str}")
        
        else:
            logging.error(f"No se pudo obtener contenido para la URL: {url_str}")
            tqdm.write(f"❌ Error procesando: {url_str}")
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
