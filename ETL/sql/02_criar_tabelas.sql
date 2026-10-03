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

-- Tabela da camada Silver (Dados limpos e estruturados)
CREATE TABLE IF NOT EXISTS silver.supermarket_clean (
    invoice_id VARCHAR(50) PRIMARY KEY,
    branch VARCHAR(10) NOT NULL,
    city VARCHAR(50) NOT NULL,
    customer_type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    product_line VARCHAR(100) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    quantity INT NOT NULL,
    total NUMERIC(10, 2) NOT NULL,
    date DATE NOT NULL,
    payment VARCHAR(50) NOT NULL,
    gross_income NUMERIC(10, 2) NOT NULL,
    rating NUMERIC(3, 1)
);