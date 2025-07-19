from models.research import Research
from scraper.base_scraper import BaseScraper


class NomeScraper(BaseScraper):
    def can_handle(self, pesquisa: Research) -> bool:
        return pesquisa.filtro == 2 and pesquisa.nome is not None

    def get_documento(self, pesquisa: Research) -> str:
        return pesquisa.nome
