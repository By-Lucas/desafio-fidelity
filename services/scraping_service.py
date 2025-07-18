# services/scraping_service.py

from models.research import Research
from repositories.result_repository import ResultRepository
from utils.constants import (
    FRASE_NADA_CONSTA,
    FRASE_CONSTA_PROCESSOS,
    FRASE_CONSTA_AUDIENCIAS,
    NADA_CONSTA,
    CONSTA01,
    CONSTA02,
    RESULTADO_ERRO,
)

class ScrapingService:
    def __init__(self, repository: ResultRepository, scrapers: list):
        self.repo = repository
        self.scrapers = scrapers

    def processar(self, pesquisas: list[Research]) -> None:
        for pesquisa in pesquisas:
            print(f"🔎 Executando filtro {pesquisa.filtro}...")

            for scraper in self.scrapers:
                if scraper.can_handle(pesquisa):
                    processos = scraper.executar(pesquisa)  # ← agora retorna uma lista de dicts com dados estruturados
                    resultado = CONSTA01 if processos else NADA_CONSTA

                    self.repo.salvar_resultado(pesquisa, resultado)
                    print(f"[OK] Resultado {resultado} salvo para {pesquisa}")

                    if processos:
                        for processo in processos:
                            self.repo.salvar_pesquisa(
                                self.repo.db,
                                processo,
                                cod_cliente=pesquisa.cod_cliente,
                                cod_servico=pesquisa.cod_servico
                            )
                            print(f"📥 Processo salvo: {processo['codigo_processo']}")
                    break
            else:
                print(f"[ERRO] Nenhum scraper disponível para o filtro {pesquisa.filtro}")


    def _checar_resultado(self, html: str) -> int:
        if FRASE_NADA_CONSTA in html:
            return NADA_CONSTA
        elif (FRASE_CONSTA_PROCESSOS in html or FRASE_CONSTA_AUDIENCIAS in html) and ('Criminal' in html or 'criminal' in html):
            return CONSTA01
        elif FRASE_CONSTA_PROCESSOS in html or FRASE_CONSTA_AUDIENCIAS in html:
            return CONSTA02
        return RESULTADO_ERRO