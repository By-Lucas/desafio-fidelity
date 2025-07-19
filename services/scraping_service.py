import glob
import os
import pandas as pd

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
            print(f"Executando filtro {pesquisa.filtro}...")

            # 🔁 Tenta recuperar de backup se existir
            backup_file = self._buscar_backup_mais_recente()
            if backup_file:
                print(f"Carregando backup: {backup_file}")
                df = pd.read_excel(backup_file)
                for _, row in df.iterrows():
                    self.repo.salvar_dados_completos(pesquisa, row.to_dict(), CONSTA01)
                os.remove(backup_file)
                print("Backup processado e removido.")
                continue

            for scraper in self.scrapers:
                if scraper.can_handle(pesquisa):
                    processos = scraper.executar(pesquisa)
                    resultado = CONSTA01 if processos else NADA_CONSTA

                    self.repo.salvar_resultado(pesquisa, resultado)
                    print(f"[OK] Resultado {resultado} salvo para {pesquisa}")

                    if processos:
                        for processo in processos:
                            self.repo.salvar_dados_completos(pesquisa, processo, resultado)
                            print(f"Processo salvo: {processo['codigo_processo']}")
                    break
            else:
                print(f"[ERRO] Nenhum scraper disponível para o filtro {pesquisa.filtro}")

    def _buscar_backup_mais_recente(self) -> str | None:
        arquivos = sorted(glob.glob("backup_*.xlsx"), reverse=True)
        return arquivos[0] if arquivos else None

    def _checar_resultado(self, html: str) -> int:
        if FRASE_NADA_CONSTA in html:
            return NADA_CONSTA
        elif (FRASE_CONSTA_PROCESSOS in html or FRASE_CONSTA_AUDIENCIAS in html) and ('Criminal' in html or 'criminal' in html):
            return CONSTA01
        elif FRASE_CONSTA_PROCESSOS in html or FRASE_CONSTA_AUDIENCIAS in html:
            return CONSTA02
        return RESULTADO_ERRO
