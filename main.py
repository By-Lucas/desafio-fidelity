from scraper.scraper_executor import ScraperExecutor
from scraper.cpf_scraper import CPFScraper
from scraper.rg_scraper import RGScraper
from scraper.nome_scraper import NomeScraper
from repositories.result_repository import ResultRepository
from services.scraping_service import ScrapingService
from config.db import DatabaseConnection
from decouple import config
from models.research import Research

def main():
    db = DatabaseConnection(
        host=config("DB_HOST"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        database=config("DB_NAME"),
    )

    executor = ScraperExecutor()
    scrapers = [
        CPFScraper(executor),
        RGScraper(executor),
        NomeScraper(executor)
    ]

    service = ScrapingService(ResultRepository(db), scrapers)

    pesquisas = [
        #Research(filtro=0, cpf="12345678901", cod_pesquisa=101),
       # Research(filtro=1, rg="4567890", cod_pesquisa=102),
        Research(filtro=2, nome="Lucas da Silva dos Santos"), #, cod_pesquisa=103
    ]

    service.processar(pesquisas)

if __name__ == "__main__":
    main()
