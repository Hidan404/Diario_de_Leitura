import sqlite3
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from enum import Enum
from pathlib import Path
from app.database.conetion import create_connection


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


class Rating(Enum):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5
    SIX_STARS = 6
    SEVEN_STARS = 7
    EIGHT_STARS = 8
    NINE_STARS = 9
    TEN_STARS = 10


class Reading:
    def __init__(
        self,
        title: str,
        authors: List[str],
        type: ReadingType,
        status: ReadingStatus,
        rating: Optional[Rating] = None,
    ):
        self.id: Optional[int] = None
        self.title: str = title
        self.authors: List[str] = authors
        self.type: ReadingType = type
        self.published_date: Optional[datetime] = None
        self.status: ReadingStatus = status
        self.current_page: Optional[int] = None
        self.total_pages: Optional[int] = None
        self.rating: Optional[Rating] = rating
        self.notes: Optional[str] = None
        self.description: Optional[str] = None
        self.cover_image_path: Optional[Path] = None
        self.genres: List[str] = []

    def create_table(self, conn: create_connection):
        cursor = create_connection().cursor()
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

    def save(self, conn: create_connection):
        cursor = create_connection().cursor()
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
                self.rating.value if self.rating else None,
                self.notes,
                self.description,
                str(self.cover_image_path) if self.cover_image_path else None,
                ", ".join(self.genres),
            ),
        )
        conn.commit()

    def update(self, conn: create_connection):
        if self.id is None:
            raise ValueError("Reading must have an ID to be updated.")
        cursor = create_connection().cursor()
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
                self.published_date,
                self.status.value,
                self.current_page,
                self.total_pages,
                self.rating.value if self.rating else None,
                self.notes,
                self.description,
                str(self.cover_image_path) if self.cover_image_path else None,
                ", ".join(self.genres),
                self.id,
            ),
        )
        conn.commit()    


    def delete(self, conn: create_connection):
        if self.id is None:
            raise ValueError("Reading must have an ID to be deleted.")
        cursor = create_connection().cursor()
        cursor.execute("DELETE FROM readings WHERE id = ?", (self.id,))
        conn.commit()    

    def listar_leitura(self, conn: create_connection) -> List['Reading']:
        cursor = create_connection().cursor()
        cursor.execute("SELECT * FROM readings")
        rows = cursor.fetchall()
        leituras = []
        for row in rows:
            leitura = Reading(
                title=row[1],
                authors=row[2].split(", "),
                type=ReadingType(row[3]),
                status=ReadingStatus(row[5]),
                rating=Rating(row[7]) if row[7] is not None else None,
            )
            leitura.id = row[0]
            leitura.published_date = datetime.strptime(row[4], "%Y-%m-%d") if row[4] else None
            leitura.current_page = row[6]
            leitura.total_pages = row[7]
            leitura.notes = row[8]
            leitura.description = row[9]
            leitura.cover_image_path = Path(row[10]) if row[10] else None
            leitura.genres = row[11].split(", ") if row[11] else []
            leituras.append(leitura)
        return leituras

    def __str__(self):
        return f"{self.title} by {', '.join(self.authors)} - {self.type.value} [{self.status.value}]"    
