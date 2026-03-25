from urllib.parse import urlparse
from pathlib import Path
import requests


def download_image(url: str, save_dir="covers"):
    Path(save_dir).mkdir(exist_ok=True)

    filename = Path(urlparse(url).path).name
    file_path = Path(save_dir) / filename

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        return str(file_path)

    return None

