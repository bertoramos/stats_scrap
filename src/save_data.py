
from pathlib import Path
from datetime import datetime

def save_dataframe(title, df):
    # Crea una carpeta con la fecha actual en data/output
    output_dir = Path("data/output") / datetime.now().strftime("%H-%M-%S_%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Guarda el DataFrame en un archivo Excel con el título como nombre de archivo
    safe_title = "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in title).strip()
    file_path = output_dir / f"{safe_title}.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")