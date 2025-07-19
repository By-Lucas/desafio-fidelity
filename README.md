# Projeto: Scraper Judicial com Backup Automático e Integração com PostgreSQL

## Visão Geral

Este projeto realiza **web scraping automatizado** no site do **Tribunal de Justiça de São Paulo (TJSP)** para extrair informações de processos judiciais vinculados a pessoas físicas (CPF, RG, nome).

Os dados extraídos são persistidos em um banco de dados **PostgreSQL**, com tratamento de erros e criação automática de backups em **Excel (xlsx)** caso o salvamento falhe.

---

## Funcionalidades

* Consulta de processos por **nome completo**, **CPF** ou **RG**;
* Paginação automática de resultados no TJSP;
* Raspagem de detalhes dos processos (classe, assunto, vara, distribuição etc.);
* Estrutura relacional com inserção em várias tabelas (pesquisa, resultado, lote etc.);
* Criação automática de backups se houver falha ao salvar no banco;
* Reprocessamento automático a partir de backups ao reiniciar.

---

## Estrutura de Pastas

```
├── config/
│   └── db.py                  # Conexão com PostgreSQL
├── models/
│   └── research.py            # Classe Research (entrada de dados)
├── repositories/
│   └── result_repository.py   # Salva resultados no banco, com backup
├── scrapers/
│   └── tjsp_scraper.py        # Scraper para o TJSP
├── services/
│   └── scraping_service.py    # Orquestra os scrapers e controle de fluxo
├── utils/
│   └── constants.py           # Frases padrões para checagem
├── main.py                    # Script principal
├── create_tables.py           # Script de criação de tabelas
├── .env                       # Variáveis de ambiente
├── backup_*.xlsx              # (auto gerado) backups em caso de falha
```

---

## Como Executar

### 1. Instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### 2. Configurar .env

Crie um arquivo `.env` na raiz com os dados do seu banco PostgreSQL:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meu_banco
DB_USER=meu_usuario
DB_PASSWORD=minha_senha

UPDATE_EXISTING_RECORDS=false
```

### 3. Gerar as tabelas do banco

```bash
python create_tables.py
```

### 4. Executar o scraping

```bash
python main.py
```

---

## Modo de Funcionamento

1. O sistema recebe uma lista de `Research` contendo os dados da pessoa (nome/CPF/RG);
2. Um dos scrapers (ex: TJSP) é escolhido com base no filtro;
3. O scraper executa o scraping, pagina os resultados, e retorna uma lista de dicionários;
4. Os dados são inseridos no banco (estado, pesquisa, lote, resultados);
5. Se houver falha no salvamento, os dados são salvos automaticamente em `backup_YYYY-MM-DD_HH-MM.xlsx`;
6. Na próxima execução, se houver backup, ele é processado antes de iniciar novo scraping.

---

## Dados Salvos no Banco

### Tabela `pesquisa`

* nome
* cpf
* rg
* data\_entrada / conclusao
* cod\_cliente / cod\_servico

### Tabela `pesquisa_spv`

* cod\_pesquisa
* resultado (0=nada consta, 1=criminal, 2=civil)
* filtro

### Tabela `lote` e `lote_pesquisa`

* agrupam pesquisas por lote automático

### Tabela `estado`

* salva os UF dos processos

---

## Backups

* Se ocorrer erro ao salvar no banco, os dados do processo são exportados para um arquivo `.xlsx` no mesmo diretório
* O nome segue o formato `backup_YYYY-MM-DD_HH-MM.xlsx`
* Ao iniciar o script, ele procura por esse backup e, se encontrar, importa os dados antes de qualquer raspagem
* Após o processamento bem-sucedido do backup, o arquivo é removido automaticamente

---
