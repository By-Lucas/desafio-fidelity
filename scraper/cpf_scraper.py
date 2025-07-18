# scraper/cpf_scraper.py

from scraper.base_scraper import BaseScraper
from models.research import Research

class CPFScraper(BaseScraper):
    def can_handle(self, pesquisa: Research) -> bool:
        return pesquisa.filtro == 0 and pesquisa.cpf is not None

    def get_documento(self, pesquisa: Research) -> str:
        return pesquisa.cpf
