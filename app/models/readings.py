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
    def __init__(self, title: str, authors: List[str], type: ReadingType, status: ReadingStatus, rating: Optional[Rating] = None):
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
        cursor.execute('''
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
        ''')
        conn.commit()


    def save(self, conn: create_connection):
        pass    