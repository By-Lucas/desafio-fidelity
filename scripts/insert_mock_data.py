# scripts/insert_mock_data.py

from datetime import date
from decouple import config
from config.db import DatabaseConnection


def insert_mock_data():
    db = DatabaseConnection(
        host=config("DB_HOST"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        database=config("DB_NAME"),
        port=int(config("DB_PORT", default=5432))
    )

    with db.get_cursor() as cursor:
        # Inserir estado (UF)
        cursor.execute("""
            INSERT INTO estado (Cod_UF, UF)
            VALUES (1, 'SP')
            ON CONFLICT (Cod_UF) DO UPDATE SET UF = EXCLUDED.UF
        """)

        # Inserir serviço
        cursor.execute("""
            INSERT INTO servico (Cod_Servico, nome)
            VALUES (1, 'Consulta TJSP')
            ON CONFLICT (Cod_Servico) DO UPDATE SET nome = EXCLUDED.nome
        """)

        # Inserir pesquisa
        cursor.execute("""
            INSERT INTO pesquisa (
                Cod_Pesquisa, Cod_Cliente, Cod_Servico, Cod_UF,
                Cod_UF_Nascimento, Cod_UF_RG, Data_Entrada,
                nome, nome_corrigido, CPF, rg, rg_corrigido,
                Nascimento, mae, mae_corrigido, tipo, Data_Conclusao
            ) VALUES (
                1, 1, 1, 1,
                1, 1, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, 0, %s
            )
            ON CONFLICT (Cod_Pesquisa) DO UPDATE SET nome = EXCLUDED.nome
        """, (
            date.today(),
            "João da Silva", "João da Silva",
            "12345678909", "1234567", "1234567",
            date(1990, 1, 1),
            "Maria da Silva", "Maria da Silva",
            date.today()
        ))

        # Inserir resultado da pesquisa
        cursor.execute("""
            INSERT INTO pesquisa_spv (
                Cod_Pesquisa, Cod_SPV, filtro, Resultado,
                cod_spv_tipo, Cod_spv_computador, Cod_Funcionario, website_id
            ) VALUES (
                1, 1, 0, %s,
                NULL, 36, -1, 1
            )
            ON CONFLICT (Cod_Pesquisa, Cod_SPV, filtro) DO NOTHING
        """, (None,))

    print("Dados mockados inseridos com sucesso.")


if __name__ == "__main__":
    insert_mock_data()
