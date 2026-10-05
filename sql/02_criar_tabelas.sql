-- Criação dos schemas para as camadas do Data Warehouse
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Tabela da camada Bronze (Dados brutos)
CREATE TABLE IF NOT EXISTS bronze.supermarket_raw (
    invoice_id VARCHAR(50),
    branch VARCHAR(10),
    city VARCHAR(50),
    customer_type VARCHAR(20),
    gender VARCHAR(10),
    product_line VARCHAR(100),
    unit_price NUMERIC(10, 2),
    quantity INT,
    tax_5_percent NUMERIC(10, 2),
    total NUMERIC(10, 2),
    date DATE,
    time TIME,
    payment VARCHAR(50),
    cogs NUMERIC(10, 2),
    gross_margin_percentage NUMERIC(5, 4),
    gross_income NUMERIC(10, 2),
    rating NUMERIC(3, 1)
);

-- Fase 0 - Tabelas das camadas Raw e Tratada.
-- Executar conectado ao banco "supermercado":
--   psql -U postgres -d supermercado -f sql/02_criar_tabelas.sql

-- ---------------------------------------------------------------
-- RAW: copia fiel do CSV do Kaggle. Todos os campos sao TEXT para
-- nao alterar o conteudo original; a tipagem acontece na camada
-- tratada. "data_carga" garante rastreabilidade da ingestao.
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw_vendas (
    invoice_id               TEXT NOT NULL,
    branch                   TEXT NOT NULL,
    city                     TEXT NOT NULL,
    customer_type            TEXT,
    gender                   TEXT,
    product_line             TEXT NOT NULL,
    unit_price               TEXT,
    quantity                 TEXT,
    tax_5pct                 TEXT,
    sales                    TEXT,
    date                     TEXT,
    time                     TEXT,
    payment                  TEXT NOT NULL,
    cogs                     TEXT,
    gross_margin_percentage  TEXT,
    gross_income             TEXT,
    rating                   TEXT,
    data_carga               TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_raw_vendas PRIMARY KEY (invoice_id)
);

-- ---------------------------------------------------------------
-- TRATADA: dados limpos e tipados (dicionario de dados no README).
-- Ultimas quatro colunas = colunas derivadas criadas no Pandas.
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS vendas_tratadas (
    id_venda           VARCHAR(50)   NOT NULL,
    "Filial"           VARCHAR(10)   NOT NULL,
    "Cidade"           VARCHAR(100)  NOT NULL,
    tipo_cliente       VARCHAR(50),
    "Gênero"           VARCHAR(20),
    linha_produto      VARCHAR(150)  NOT NULL,
    preco_unitario     NUMERIC(10,2) NOT NULL
                       CONSTRAINT ck_preco_unitario CHECK (preco_unitario >= 0),
    "Quantidade"       INTEGER       NOT NULL
                       CONSTRAINT ck_quantidade CHECK ("Quantidade" > 0),
    "Imposto"          NUMERIC(10,2)
                       CONSTRAINT ck_imposto CHECK ("Imposto" >= 0),
    valor_total        NUMERIC(12,2) NOT NULL
                       CONSTRAINT ck_valor_total CHECK (valor_total >= 0),
    data_venda         DATE          NOT NULL,
    hora_venda         TIME,
    forma_pagamento    VARCHAR(50)   NOT NULL,
    custo_mercadoria   NUMERIC(12,2)
                       CONSTRAINT ck_custo CHECK (custo_mercadoria >= 0),
    margem_percentual  NUMERIC(10,2),
    receita_bruta      NUMERIC(12,2)
                       CONSTRAINT ck_receita CHECK (receita_bruta >= 0),
    "Avaliação"        NUMERIC(4,2)
                       CONSTRAINT ck_avaliacao
                       CHECK ("Avaliação" BETWEEN 0 AND 10),
    dia_semana         VARCHAR(15)   NOT NULL,
    mes                INTEGER
                       CONSTRAINT ck_mes CHECK (mes BETWEEN 1 AND 12),
    periodo_dia        VARCHAR(15),
    valor_conferido    BOOLEAN,
    CONSTRAINT pk_vendas_tratadas PRIMARY KEY (id_venda)
);
