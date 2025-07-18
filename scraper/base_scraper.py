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

    # def executar(self, pesquisa: Research) -> str:
    #     documento = self.get_documento(pesquisa)
    #     html =  self.executor.load_search_page(pesquisa.filtro, documento)
    #     participants = self.executor.extract_processes_data(html)
    #     print(participants)
    #     return participants

    def executar(self, pesquisa: Research) -> list[dict]:
        documento = self.get_documento(pesquisa)
        dados = self.executor.extract_all_pages_data(pesquisa.filtro, documento)
        print(dados)
        return dados