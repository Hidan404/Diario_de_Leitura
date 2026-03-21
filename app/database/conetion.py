import sqlite3
from pathlib import Path


def caminho_banco_dados() -> Path:
    return Path(__file__).parent / "readings.db"

def create_connection(db_file: Path = caminho_banco_dados()) -> sqlite3.Connection:
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn