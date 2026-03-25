from app.services.reading_services import ReadingService, ReadingType, ReadingStatus
from app.utils.handle_cover_image import handle_cover_image
from typing import List, Optional
from datetime import datetime
from pathlib import Path




class LeituraController:
    def __init__(self):
        self.reading_service = ReadingService()

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
        cover_image_path = handle_cover_image(cover_image_path)
        self.reading_service.adicionar_leitura(
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

    def listar_leitura(self):
        return self.reading_service.listar_leitura()
    
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
        cover_image_path = handle_cover_image(cover_image_path)
        self.reading_service.atualizar_leitura(
            id,
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

    def excluir_leitura(self, id: int):
        self.reading_service.excluir_leitura(id)

    def buscar_leitura(self, id: int):
        return self.reading_service.buscar_leitura(id)        