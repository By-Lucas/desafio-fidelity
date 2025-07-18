from typing import List
from models.research import Research
from config.db import DatabaseConnection


class ResearchRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_pending_researches(self, filter: int = 0, limit: int = 210) -> List[Research]:
        condition = ' AND rg <> "" ' if filter in (1, 3) else ''
        query = f"""
            SELECT DISTINCT p.Cod_Cliente, p.Cod_Pesquisa, e.UF, p.Data_Entrada,
                COALESCE(p.nome_corrigido, p.nome),
                p.CPF,
                COALESCE(p.rg_corrigido, p.rg),
                p.Nascimento,
                COALESCE(p.mae_corrigido, p.mae),
                p.anexo,
                ps.Resultado,
                ps.cod_spv_tipo
            FROM pesquisa p
            INNER JOIN servico s ON p.Cod_Servico = s.Cod_Servico
            LEFT JOIN lote_pesquisa lp ON p.Cod_Pesquisa = lp.Cod_Pesquisa
            LEFT JOIN lote l ON l.cod_lote = lp.cod_lote
            LEFT JOIN estado e ON e.Cod_UF = p.Cod_UF
            LEFT JOIN pesquisa_spv ps ON ps.Cod_Pesquisa = p.Cod_Pesquisa
                AND ps.Cod_SPV = 1
                AND ps.filtro = {filter}
            WHERE p.Data_Conclusao IS NULL
              AND ps.resultado IS NULL
              AND p.tipo = 0
              AND p.cpf <> ""
              {condition}
              AND (e.UF = "SP" OR p.Cod_UF_Nascimento = 26 OR p.Cod_UF_RG = 26)
            GROUP BY p.cod_pesquisa
            ORDER BY COALESCE(p.nome_corrigido, p.nome) ASC, ps.Resultado DESC
            LIMIT {limit}
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            return [Research(*row) for row in cursor.fetchall()]
