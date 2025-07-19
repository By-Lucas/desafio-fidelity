from datetime import date
from decouple import config
from config.db import DatabaseConnection


def insert_mock_data():
    db = DatabaseConnection(
        host=config("DB_HOST"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        database=config("DB_NAME")
    )

    with db.get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO estado (Cod_UF, UF)
            VALUES (1, 'SP')
            ON DUPLICATE KEY UPDATE UF='SP'
        """)

        cursor.execute("""
            INSERT INTO servico (Cod_Servico, nome)
            VALUES (1, 'Consulta TJSP')
            ON DUPLICATE KEY UPDATE nome='Consulta TJSP'
        """)

        cursor.execute("""
            INSERT INTO pesquisa (
                Cod_Pesquisa, Cod_Cliente, Cod_Servico, Cod_UF,
                Cod_UF_Nascimento, Cod_UF_RG, Data_Entrada,
                nome, CPF, rg, Nascimento, mae, tipo, Data_Conclusao
            ) VALUES (
                1, 1, 1, 1,
                1, 1, %s,
                %s, %s, %s, %s, %s, 0, NULL
            )
            ON DUPLICATE KEY UPDATE CPF=VALUES(CPF)
        """, (
            date.today(),
            "João da Silva",
            "12345678909",
            "1234567",
            date(1990, 1, 1),
            "Maria da Silva"
        ))

        cursor.execute("""
            INSERT IGNORE INTO pesquisa_spv (
                Cod_Pesquisa, Cod_SPV, filtro, Resultado, cod_spv_tipo
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            1, 1, 0, None, None
        ))

    print("Dados mockados inseridos com sucesso.")

if __name__ == "__main__":
    insert_mock_data()
