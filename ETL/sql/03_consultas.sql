-- 1. Consulta para verificar o total de vendas por linha de produto (camada Gold analítica)
SELECT 
    product_line,
    SUM(total) AS total_vendas,
    AVG(total) AS media_vendas,
    SUM(quantity) AS quantidade_total_itens
FROM silver.supermarket_clean
GROUP BY product_line
ORDER BY total_vendas DESC;

-- 2. Consulta para analisar vendas por género e tipo de cliente
SELECT 
    customer_type,
    gender,
    COUNT(invoice_id) AS total_transacoes,
    SUM(total) AS receita_total
FROM silver.supermarket_clean
GROUP BY customer_type, gender
ORDER BY receita_total DESC;