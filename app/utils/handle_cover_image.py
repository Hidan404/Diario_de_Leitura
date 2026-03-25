from pathlib import Path
from app.utils.detectar_url import download_image

def handle_cover_image(value):
    if not value:
        return None

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, str) and value.startswith("http"):
        return download_image(value)

    return str(Path(value))