
from pathlib import Path
from datetime import datetime
import pandas as pd
import re
import logging

def save_dataframe(title, df, output_dir):
    # Crear carpeta si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Nombre de archivo seguro y corto (fecha + hash opcional)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    short_name = f"data_{date_str}.xlsx"
    file_path = output_dir / short_name

    # Guardar DataFrame en Excel
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        # Guardar el título en la primera celda
        df.to_excel(writer, index=False, startrow=1)
        worksheet = writer.sheets['Sheet1']
        worksheet.cell(row=1, column=1, value=title)  # fila 1, columna 1
    
    logging.info(f"Archivo guardado en: {file_path}")
