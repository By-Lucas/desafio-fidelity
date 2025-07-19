from models.research import Research
from scraper.base_scraper import BaseScraper


class RGScraper(BaseScraper):
    def can_handle(self, pesquisa: Research) -> bool:
        return pesquisa.filtro in [1, 3] and pesquisa.rg is not None

    def get_documento(self, pesquisa: Research) -> str:
        return pesquisa.rg
