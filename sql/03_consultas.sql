-- Fase 2 - Consultas SQL fundamentais e exportacao para CSV.
--
-- Cada consulta e precedida por um marcador "-- @export arquivo.csv".
-- O script src/exportacao.py executa as consultas e grava os
-- resultados em data/raw/. Equivalente manual no psql:
--   \copy (SELECT ...) TO 'data/raw/arquivo.csv' CSV HEADER
--
-- Obs.: a camada Raw guarda tudo como TEXT, por isso os calculos
-- usam CAST(... AS NUMERIC).

-- @export export_raw_vendas.csv
-- Todos os registros brutos (entrada da analise exploratoria em Pandas)
SELECT invoice_id, branch, city, customer_type, gender, product_line,
       unit_price, quantity, tax_5pct, sales, date, time, payment,
       cogs, gross_margin_percentage, gross_income, rating
FROM raw_vendas
ORDER BY invoice_id;

-- @export consulta_faturamento_por_filial.csv
-- Faturamento, quantidade de vendas e ticket medio por filial
SELECT branch AS filial,
       COUNT(*) AS qtd_vendas,
       ROUND(SUM(CAST(sales AS NUMERIC)), 2) AS faturamento,
       ROUND(AVG(CAST(sales AS NUMERIC)), 2) AS ticket_medio
FROM raw_vendas
GROUP BY branch
ORDER BY faturamento DESC;

-- @export consulta_faturamento_por_linha_produto.csv
-- Faturamento e quantidade de itens por linha de produto
SELECT product_line AS linha_produto,
       SUM(CAST(quantity AS INTEGER)) AS itens_vendidos,
       ROUND(SUM(CAST(sales AS NUMERIC)), 2) AS faturamento
FROM raw_vendas
GROUP BY product_line
ORDER BY faturamento DESC;

-- @export consulta_avaliacao_por_linha_produto.csv
-- Avaliacao media por linha de produto (somente notas validas)
SELECT product_line AS linha_produto,
       COUNT(*) AS qtd_avaliacoes,
       ROUND(AVG(CAST(rating AS NUMERIC)), 2) AS avaliacao_media
FROM raw_vendas
WHERE rating IS NOT NULL
GROUP BY product_line
ORDER BY avaliacao_media DESC;

-- @export consulta_formas_pagamento.csv
-- Quantidade de vendas por forma de pagamento
SELECT payment AS forma_pagamento,
       COUNT(*) AS qtd_vendas
FROM raw_vendas
GROUP BY payment
ORDER BY qtd_vendas DESC;

-- @export consulta_vendas_alto_valor.csv
-- Vendas acima de 1,5x o valor medio, da maior para a menor
SELECT invoice_id, branch AS filial, product_line AS linha_produto,
       CAST(sales AS NUMERIC) AS valor_total
FROM raw_vendas
WHERE CAST(sales AS NUMERIC) >
      1.5 * (SELECT AVG(CAST(sales AS NUMERIC)) FROM raw_vendas)
ORDER BY valor_total DESC;
