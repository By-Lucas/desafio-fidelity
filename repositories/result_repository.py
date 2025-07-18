from models.research import Research


class ResultRepository:
    def __init__(self, db):
        self.db = db

    def salvar_resultado(self, pesquisa: Research, resultado: int) -> None:
        sql = """
        INSERT INTO pesquisa_spv (
            Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id
        )
        VALUES (%s, 1, 36, NULL, %s, -1, %s, 1)
        ON CONFLICT (Cod_Pesquisa, Cod_SPV, filtro)
        DO UPDATE SET Resultado = EXCLUDED.Resultado
        """
        with self.db.get_cursor() as cursor:
            cursor.execute(sql, (pesquisa.cod_pesquisa, resultado, pesquisa.filtro))

    def salvar_pesquisa(self, db, dados: dict, cod_cliente: int = 1, cod_servico: int = 1):
        sql = """
        INSERT INTO pesquisa (
            cod_cliente, cod_uf, cod_servico, tipo,
            cpf, cod_uf_nascimento, cod_uf_rg,
            data_entrada, data_conclusao,
            nome, nome_corrigido,
            rg, rg_corrigido, nascimento,
            mae, mae_corrigido, anexo
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s
        )
        """
        values = (
            cod_cliente,
            None,  # cod_uf (pode mapear a partir do foro)
            cod_servico,
            1,  # tipo
            None,
            None,
            None,
            dados.get("data_distribuicao"),
            dados.get("data_distribuicao"),
            dados.get("nome_completo"),
            dados.get("nome_completo"),
            None,
            None,
            None,
            None,
            None,
            None  # anexo
        )

        with db.get_cursor() as cursor:
            cursor.execute(sql, values)
