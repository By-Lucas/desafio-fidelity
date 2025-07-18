# scraper/base_scraper.py

from abc import ABC, abstractmethod
from models.research import Research

class BaseScraper(ABC):
    def __init__(self, executor):
        self.executor = executor

    @abstractmethod
    def can_handle(self, pesquisa: Research) -> bool:
        ...

    @abstractmethod
    def get_documento(self, pesquisa: Research) -> str:
        ...

    def executar(self, pesquisa: Research) -> str:
        documento = self.get_documento(pesquisa)
        return self.executor.carregar_pagina(pesquisa.filtro, documento)
