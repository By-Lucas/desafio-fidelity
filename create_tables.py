import os
import sys
from decouple import config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import DatabaseConnection


def create_tables():
    db = DatabaseConnection(
        host=config("DB_HOST"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        database=config("DB_NAME"),
        port=int(config("DB_PORT", default=5432))
    )

    create_statements = [
        # Tabela de estados (UF)
        """
        CREATE TABLE IF NOT EXISTS estado (
            Cod_UF SERIAL PRIMARY KEY,
            UF VARCHAR(2) NOT NULL
        )
        """,

        # Tabela de serviços
        """
        CREATE TABLE IF NOT EXISTS servico (
            Cod_Servico SERIAL PRIMARY KEY,
            nome VARCHAR(100)
        )
        """,

        # Tabela de lotes
        """
        CREATE TABLE IF NOT EXISTS lote (
            cod_lote SERIAL PRIMARY KEY,
            descricao VARCHAR(100),
            cod_funcionario INT,
            tipo VARCHAR(50),
            prioridade VARCHAR(50),
            data_criacao DATE DEFAULT CURRENT_DATE
        )
        """,

        # Relacionamento entre pesquisa e lote
        """
        CREATE TABLE IF NOT EXISTS lote_pesquisa (
            cod_lote INT,
            Cod_Pesquisa INT,
            cod_funcionario INT,
            cod_funcionario_conclusao INT,
            cod_fornecedor INT,
            data_entrada DATE,
            data_conclusao DATE,
            cod_uf INT,
            obs TEXT,
            PRIMARY KEY (cod_lote, Cod_Pesquisa)
        )
        """,

        # Tabela principal de pesquisa
        """
        CREATE TABLE IF NOT EXISTS pesquisa (
            Cod_Pesquisa SERIAL PRIMARY KEY,
            Cod_Cliente INT,
            Cod_Servico INT,
            Cod_UF INT,
            Cod_UF_Nascimento INT,
            Cod_UF_RG INT,
            Data_Entrada DATE,
            nome VARCHAR(100),
            nome_corrigido VARCHAR(100),
            CPF VARCHAR(20),
            rg VARCHAR(20),
            rg_corrigido VARCHAR(20),
            Nascimento DATE,
            mae VARCHAR(100),
            mae_corrigido VARCHAR(100),
            tipo INT,
            anexo TEXT,
            Data_Conclusao DATE
        )
        """,

        # Resultado da pesquisa SPV
        """
        CREATE TABLE IF NOT EXISTS pesquisa_spv (
            Cod_Pesquisa INT,
            Cod_SPV INT,
            filtro INT,
            Resultado VARCHAR(255),
            cod_spv_tipo INT,
            Cod_spv_computador INT,
            Cod_Funcionario INT,
            website_id INT,
            PRIMARY KEY (Cod_Pesquisa, Cod_SPV, filtro)
        )
        """
    ]

    with db.get_cursor() as cursor:
        for sql in create_statements:
            print(f"Executando: {sql.split('(')[0].strip()}")
            cursor.execute(sql)

if __name__ == "__main__":
    create_tables()
