import sqlite3
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from enum import Enum
from pathlib import Path
from app.database.conetion import create_connection
from app.utils.handle_cover_image import handle_cover_image


class ReadingStatus(Enum):
    TO_READ = "To Read"
    READING = "Reading"
    PAUSED = "Paused"
    DROPPED = "Dropped"
    CONCLUDED = "Concluded"


class ReadingType(Enum):
    BOOK = "Book"
    MANGA = "Manga"
    HQ = "HQ"


class Reading:
    def __init__(
        self,
        title: str,
        authors: List[str],
        type: ReadingType,
        status: ReadingStatus,
        rating: Optional[int] = None,
        current_page: Optional[int] = None,
        total_pages: Optional[int] = None,
        published_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        description: Optional[str] = None,
        cover_image_path: Optional[Path] = None,
        genres: Optional[List[str]] = None,
    ):
        self.id: Optional[int] = None
        self.title: str = title
        self.authors: List[str] = authors
        self.type: ReadingType = type
        self.published_date: Optional[datetime] = published_date
        self.status: ReadingStatus = status
        self.current_page: Optional[int] = current_page
        self.total_pages: Optional[int] = total_pages
        self.rating: Optional[int] = rating
        self.notes: Optional[str] = notes
        self.description: Optional[str] = description
        self.cover_image_path: Optional[Path] = cover_image_path
        self.genres: List[str] = genres or []

    def create_table(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authors TEXT NOT NULL,
                type TEXT NOT NULL,
                published_date TEXT,
                status TEXT NOT NULL,
                current_page INTEGER,
                total_pages INTEGER,
                rating INTEGER,
                notes TEXT,
                description TEXT,
                cover_image_path TEXT,
                genres TEXT
            )
        """
        )
        conn.commit()

    def save(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO readings (title, authors, type, published_date, status, current_page, total_pages, rating, notes, description, cover_image_path, genres)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                self.title,
                ", ".join(self.authors),
                self.type.value,
                self.published_date,
                self.status.value,
                self.current_page,
                self.total_pages,
                self.rating,
                self.notes,
                self.description,
                handle_cover_image(self.cover_image_path),
                ", ".join(self.genres),
            ),
        )
        conn.commit()

    def update(self, id, conn: sqlite3.Connection):
        if self.id is None:
            raise ValueError("Reading must have an ID to be updated.")
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE readings
            SET title = ?, authors = ?, type = ?, published_date = ?, status = ?, current_page = ?, total_pages = ?, rating = ?, notes = ?, description = ?, cover_image_path = ?, genres = ?
            WHERE id = ?
        """,
            (
                self.title,
                ", ".join(self.authors),
                self.type.value,
                (
                    self.published_date.strftime("%Y%m%d")
                    if self.published_date
                    else None
                ),
                self.status.value,
                self.current_page,
                self.total_pages,
                self.rating,
                self.notes,
                self.description,
                handle_cover_image(self.cover_image_path),
                ", ".join(self.genres),
                self.id,
            ),
        )
        conn.commit()

    def delete(self, conn: sqlite3.Connection):
        if self.id is None:
            raise ValueError("Reading must have an ID to be deleted.")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM readings WHERE id = ?", (self.id,))
        conn.commit()

    @classmethod
    def listar_leitura(cls, conn: sqlite3.Connection) -> List["Reading"]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM readings")
        rows = cursor.fetchall()
        leituras = []
        for row in rows:
            leitura = Reading(
                title=row[1],
                authors=row[2].split(", "),
                type=ReadingType(row[3]),
                status=ReadingStatus(row[5]),
                rating=int(row[8]) if row[8] is not None else None,
            )
            leitura.id = row[0]
            leitura.published_date = (
                datetime.strptime(row[4], "%Y-%m-%d") if row[4] else None
            )
            leitura.current_page = row[6]
            leitura.total_pages = row[7]
            leitura.notes = row[9]
            leitura.description = row[10]
            leitura.cover_image_path = Path(row[11]) if row[11] else None
            leitura.genres = row[12].split(", ") if row[12] else []
            leituras.append(leitura)
        return leituras

    def buscar_leitura(cls, conn: sqlite3.Connection, id: int) -> Optional["Reading"]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM readings WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            leitura = Reading(
                title=row[1],
                authors=row[2].split(", "),
                type=ReadingType(row[3]),
                status=ReadingStatus(row[5]),
                rating=int(row[8]) if row[8] is not None else None,
            )
            leitura.id = row[0]
            leitura.published_date = (
                datetime.strptime(row[4], "%Y-%m-%d") if row[4] else None
            )
            leitura.current_page = row[6]
            leitura.total_pages = row[7]
            leitura.notes = row[9]
            leitura.description = row[10]
            leitura.cover_image_path = Path(row[11]) if row[11] else None
            leitura.genres = row[12].split(", ") if row[12] else []
            return leitura
        return None

    def __str__(self):
        return f"{self.title} by {', '.join(self.authors)} - {self.type.value} [{self.status.value} - {self.rating}/5 - {self.current_page}/{self.total_pages} pages] - Published on {self.published_date.strftime('%Y-%m-%d') if self.published_date else 'N/A'} - Genres: {', '.join(self.genres)}"


"""if __name__ == "__main__":
    conn = create_connection()
    leitura = Reading(
        title="The Great Gatsby",
        authors=["F. Scott Fitzgerald"],
        type=ReadingType.BOOK,
        status=ReadingStatus.TO_READ,
        rating=5,
        published_date=datetime(1925, 4, 10),
        notes="A classic novel set in the Jazz Age.",
        description="The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.",
        cover_image_path=Path("covers/great_gatsby.jpg"),
        genres=["Classic", "Fiction"],
    )
    leitura.create_table(conn)
    leitura.save(conn)
    leituras = leitura.listar_leitura(conn)
    for l in leituras:
        print(l)"""
