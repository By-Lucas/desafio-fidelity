from decouple import config
from datetime import datetime
from psycopg2.errors import UndefinedColumn

from models.research import Research


class ResultRepository:
    UPDATE_EXISTING = config("UPDATE_EXISTING_RECORDS", default="false").lower() == "true"

    def __init__(self, db):
        self.db = db
        

    def save_result(self, pesquisa: Research, resultado: int) -> None:
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

    def save_full_data(self, pesquisa: Research, dados: dict, resultado: int) -> None:
        try:
            with self.db.get_cursor() as cursor:
                # 1. Garantir estado (UF)
                uf = dados.get("foro", "").split("/")[0].strip() if dados.get("foro") else "SP"
                cod_uf = self._ensure_estado(cursor, uf)

                hoje = datetime.now().date()

                # 2. Verificar se a pesquisa já existe
                cursor.execute("""
                    SELECT cod_pesquisa FROM pesquisa
                    WHERE nome = %s AND data_entrada = %s
                """, (
                    dados.get("nome_completo"),
                    dados.get("data_distribuicao")
                ))
                existing = cursor.fetchone()

                if existing:
                    if not self.UPDATE_EXISTING:
                        print(f"Pulando processo já existente: {dados.get('codigo_processo')}")
                        return
                    else:
                        print(f"Atualizando processo existente: {dados.get('codigo_processo')}")
                        cod_pesquisa = existing[0]
                        # Aqui você pode fazer UPDATE dos campos, se quiser
                else:
                    # 3. Inserir novo registro de pesquisa
                    sql_pesquisa = """
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
                        ) RETURNING cod_pesquisa
                    """
                    values = (
                        pesquisa.cod_cliente,
                        cod_uf,
                        pesquisa.cod_servico,
                        1,
                        pesquisa.cpf,
                        None,
                        None,
                        dados.get("data_distribuicao"),
                        dados.get("data_distribuicao"),
                        dados.get("nome_completo"),
                        dados.get("nome_completo"),
                        pesquisa.rg,
                        pesquisa.rg,
                        None,
                        None,
                        None,
                        None
                    )
                    cursor.execute(sql_pesquisa, values)
                    cod_pesquisa = cursor.fetchone()[0]

                # 4. Criar lote se necessário
                cod_lote = self._ensure_lote(cursor)

                # 5. Relacionamento em lote_pesquisa (ignorar se já existe)
                cursor.execute("""
                    SELECT 1 FROM lote_pesquisa WHERE cod_pesquisa = %s AND cod_lote = %s
                """, (cod_pesquisa, cod_lote))
                exists_lote = cursor.fetchone()

                if not exists_lote:
                    sql_lote_pesquisa = """
                        INSERT INTO lote_pesquisa (
                            cod_lote, cod_pesquisa, cod_funcionario, cod_funcionario_conclusao,
                            cod_fornecedor, data_entrada, data_conclusao, cod_uf, obs
                        ) VALUES (%s, %s, -1, -1, -1, %s, %s, %s, NULL)
                    """
                    cursor.execute(sql_lote_pesquisa, (
                        cod_lote, cod_pesquisa, hoje, hoje, cod_uf
                    ))

                # 6. Salvar resultado da pesquisa_spv
                cursor.execute("""
                    INSERT INTO pesquisa_spv (
                        cod_pesquisa, cod_spv, cod_spv_computador, cod_spv_tipo,
                        resultado, cod_funcionario, filtro, website_id
                    ) VALUES (%s, 1, 36, NULL, %s, -1, %s, 1)
                    ON CONFLICT (cod_pesquisa, cod_spv, filtro)
                    DO UPDATE SET resultado = EXCLUDED.resultado
                """, (cod_pesquisa, resultado, pesquisa.filtro))
        except (UndefinedColumn, Exception) as e:
            print(f"[ERRO SALVAR DB]: {e}")
            self.salvar_backup_erro(dados)

    def _ensure_estado(self, cursor, uf: str) -> int:
        cursor.execute("SELECT cod_uf FROM estado WHERE uf = %s", (uf,))
        result = cursor.fetchone()
        if result:
            return result[0]

        cursor.execute("INSERT INTO estado (uf) VALUES (%s) RETURNING cod_uf", (uf,))
        return cursor.fetchone()[0]

    def _ensure_lote(self, cursor) -> int:
        cursor.execute("SELECT cod_lote FROM lote ORDER BY cod_lote DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            return result[0]

        cursor.execute("""
            INSERT INTO lote (descricao, cod_funcionario, tipo, prioridade)
            VALUES (%s, -1, 'automatica', 'normal') RETURNING cod_lote
        """, ("Lote Automático",))
        return cursor.fetchone()[0]

    def salvar_backup_erro(self, dados: dict):
        import pandas as pd

        try:
            df = pd.DataFrame([dados])
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = f"backup_{timestamp}.xlsx"
            df.to_excel(path, index=False)
            print(f"Backup salvo em {path}")
        except Exception as e:
            print(f"Falha ao salvar backup: {e}")