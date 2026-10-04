# Dicionario de dados - vendas_tratadas

| coluna | tipo | restricoes | descricao | origem |
|---|---|---|---|---|
| id_venda | VARCHAR(50) | PRIMARY KEY, NOT NULL | Identificador unico da venda (Invoice ID) | raw: invoice_id |
| Filial | VARCHAR(10) | NOT NULL | Codigo da filial | raw: branch |
| Cidade | VARCHAR(100) | NOT NULL | Cidade da filial | raw: city |
| tipo_cliente | VARCHAR(50) | - | Member ou Normal | raw: customer_type |
| Gênero | VARCHAR(20) | - | Genero do cliente | raw: gender |
| linha_produto | VARCHAR(150) | NOT NULL | Categoria do produto | raw: product_line |
| preco_unitario | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | Preco por unidade | raw: unit_price |
| Quantidade | INTEGER | NOT NULL, CHECK > 0 | Unidades vendidas | raw: quantity |
| Imposto | NUMERIC(10,2) | CHECK >= 0 | Imposto de 5 por cento sobre o custo | raw: tax_5pct |
| valor_total | NUMERIC(12,2) | NOT NULL, CHECK >= 0 | Valor total da venda (custo + imposto) | raw: sales |
| data_venda | DATE | NOT NULL | Data da venda (texto m/d/Y convertido para data) | raw: date |
| hora_venda | TIME | - | Horario da venda (texto convertido para hora) | raw: time |
| forma_pagamento | VARCHAR(50) | NOT NULL | Cash, Ewallet ou Credit card | raw: payment |
| custo_mercadoria | NUMERIC(12,2) | CHECK >= 0 | Custo da mercadoria vendida (cogs) | raw: cogs |
| margem_percentual | NUMERIC(10,2) | - | Margem bruta em percentual | raw: gross_margin_percentage |
| receita_bruta | NUMERIC(12,2) | CHECK >= 0 | Receita bruta (gross income) | raw: gross_income |
| Avaliação | NUMERIC(4,2) | CHECK entre 0 e 10 | Nota do cliente | raw: rating |
| dia_semana | VARCHAR(15) | NOT NULL | Dia da semana em portugues | derivada de data_venda |
| mes | INTEGER | CHECK entre 1 e 12 | Mes da venda | derivada de data_venda |
| periodo_dia | VARCHAR(15) | - | Manha (ate 11h), Tarde (12h-17h), Noite (18h+) | derivada de hora_venda |
| valor_conferido | BOOLEAN | - | True se Quantidade x preco_unitario + Imposto = valor_total (tolerancia 0,02) | derivada (conferencia) |
