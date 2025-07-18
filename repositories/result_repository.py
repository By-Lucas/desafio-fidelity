# repositories/result_repository.py

from models.research import Research

class ResultRepository:
    def __init__(self, db):
        self.db = db

    def salvar_resultado(self, pesquisa: Research, resultado: int) -> None:
        sql = """
        INSERT INTO pesquisa_spv (Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id)
        VALUES (%s, 1, 36, NULL, %s, -1, %s, 1)
        """
        with self.db.get_cursor() as cursor:
            cursor.execute(sql, (pesquisa.cod_pesquisa, resultado, pesquisa.filtro))
