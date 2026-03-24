from app.models.readings import Reading, ReadingStatus, ReadingType
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from app.database.conetion import create_connection


class ReadingService:
    def __init__(self):
        self.path_db = Path(__file__).parent.parent / "models/readings.db"

    def adicionar_leitura(
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
        nova_leitura = Reading(
            title,
            authors,
            type,
            status,
            rating,
            current_page,
            total_pages,
            published_date,
            notes,
            description,
            cover_image_path,
            genres,
        )

        try:
            with create_connection(self.path_db) as conn:
                nova_leitura.create_table(conn)
                nova_leitura.save(conn)

        except Exception as e:
            print(f"Erro: {e}")
        

    def listar_leitura(self):
        with create_connection(self.path_db) as conn:
            listar_leitura = Reading.listar_leitura(conn)
            for l in listar_leitura:
                print(l)  

    def atualizar_leitura(
        self,
        id: int,
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
        leituras_id = Reading(
            title,
            authors,
            type,
            status,
            rating,
            current_page,
            total_pages,
            published_date,
            notes,
            description,
            cover_image_path,
            genres
        )

        leituras_id.id = id

        with create_connection()
        

r = ReadingService()

r.adicionar_leitura(
    title="Kagurabachi Vol. 1",
    authors=["Takeru Hokazono"],
    type=ReadingType.MANGA,
    status=ReadingStatus.READING,
    rating=9,
    current_page=20,
    total_pages=192,
    notes="Comecei hoje, arte muito boa",
    genres=["Ação", "Sobrenatural"]
)  

r.listar_leitura()



