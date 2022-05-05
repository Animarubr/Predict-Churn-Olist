SELECT '{date}' as dt_ref,
    t2.seller_city,
    t2.seller_state,
    t1.*
FROM (
        SELECT t2.seller_id,
            avg(t5.review_score) as avg_review_score,
            -- média do score de reviews
            t3.idade_base as idade_base_dias,
            -- dias desde a primeira venda
            1 + cast(t3.idade_base / 30 as INTEGER) as idade_base_mes,
            -- meses desde a primeira venda
            cast(
                '{date}' - max(t1.order_approved_at::date) - 1 as INTEGER
            ) as qtde_dias_ult_venda,
            count(
                DISTINCT DATE_PART('month', t1.order_approved_at::date)
            ) as qtde_mes_ativacao,
            cast(
                count(
                    DISTINCT DATE_PART('month', t1.order_approved_at::date)
                ) as FLOAT
            ) / GREATEST(1 + cast(t3.idade_base / 30 as INTEGER), 6) as prop_ativacao,
            -- proporção de meses em que o vendedor vendeu
            sum(
                case
                    when t1.order_estimated_delivery_date::date < t1.order_delivered_carrier_date::date then 1
                    else 0
                end
            ) / count(DISTINCT t2.order_id) as prop_atraso,
            -- proporção de pedidos em atraso
            cast(
                avg(
                    t1.order_estimated_delivery_date::date - t1.order_purchase_timestamp::date
                ) as INTEGER
            ) - 1 as avg_tempo_entrega_est,
            -- tempo médio de entrega prevista
            sum(t2.price) as receita_total,
            sum(t2.price) / count(DISTINCT t2.order_id) as avg_vl_venda,
            sum(t2.price) / GREATEST(1 + cast(t3.idade_base / 30 as INTEGER), 6) as avg_vl_venda_mes,
            -- receita média simples
            sum(t2.price) / count(
                DISTINCT DATE_PART('month', t1.order_approved_at::date)
            ) as avg_vl_venda_mes_ativado,
            -- receita média por mês em que vendedor é ativo
            count(DISTINCT t2.order_id) as qtde_vendas,
            count(t2.product_id) as qtde_produto,
            count(DISTINCT t2.product_id) as qtde_produto_dst,
            sum(t2.price) / count(t2.product_id) as avg_vl_produto,
            count(t2.product_id) / count(DISTINCT t2.order_id) as avg_qtde_produto_venda,
            -- média de produtos vendidos por venda
            -- Variáveis de volume de vendas por categoria de produto
            sum(
                case
                    when product_category_name = 'cama_mesa_banho' then 1
                    else 0
                end
            ) as qtde_cama_mesa_banho,
            sum(
                case
                    when product_category_name = 'beleza_saude' then 1
                    else 0
                end
            ) as qtde_beleza_saude,
            sum(
                case
                    when product_category_name = 'esporte_lazer' then 1
                    else 0
                end
            ) as qtde_esporte_lazer,
            sum(
                case
                    when product_category_name = 'moveis_decoracao' then 1
                    else 0
                end
            ) as qtde_moveis_decoracao,
            sum(
                case
                    when product_category_name = 'informatica_acessorios' then 1
                    else 0
                end
            ) as qtde_informatica_acessorios,
            sum(
                case
                    when product_category_name = 'utilidades_domesticas' then 1
                    else 0
                end
            ) as qtde_utilidades_domesticas,
            sum(
                case
                    when product_category_name = 'relogios_presentes' then 1
                    else 0
                end
            ) as qtde_relogios_presentes,
            sum(
                case
                    when product_category_name = 'telefonia' then 1
                    else 0
                end
            ) as qtde_telefonia,
            sum(
                case
                    when product_category_name = 'ferramentas_jardim' then 1
                    else 0
                end
            ) as qtde_ferramentas_jardim,
            sum(
                case
                    when product_category_name = 'automotivo' then 1
                    else 0
                end
            ) as qtde_automotivo,
            sum(
                case
                    when product_category_name = 'brinquedos' then 1
                    else 0
                end
            ) as qtde_brinquedos,
            sum(
                case
                    when product_category_name = 'cool_stuff' then 1
                    else 0
                end
            ) as qtde_cool_stuff,
            sum(
                case
                    when product_category_name = 'perfumaria' then 1
                    else 0
                end
            ) as qtde_perfumaria,
            sum(
                case
                    when product_category_name = 'bebes' then 1
                    else 0
                end
            ) as qtde_bebes,
            sum(
                case
                    when product_category_name = 'eletronicos' then 1
                    else 0
                end
            ) as qtde_eletronicos,
            sum(
                case
                    when product_category_name = 'papelaria' then 1
                    else 0
                end
            ) as qtde_papelaria,
            sum(
                case
                    when product_category_name = 'fashion_bolsas_e_acessorios' then 1
                    else 0
                end
            ) as qtde_fashion_bolsas_e_acessorios,
            sum(
                case
                    when product_category_name = 'pet_shop' then 1
                    else 0
                end
            ) as qtde_pet_shop,
            sum(
                case
                    when product_category_name = 'moveis_escritorio' then 1
                    else 0
                end
            ) as qtde_moveis_escritorio,
            sum(
                case
                    when product_category_name = 'consoles_games' then 1
                    else 0
                end
            ) as qtde_consoles_games,
            sum(
                case
                    when product_category_name = 'malas_acessorios' then 1
                    else 0
                end
            ) as qtde_malas_acessorios,
            sum(
                case
                    when product_category_name = 'construcao_ferramentas_construcao' then 1
                    else 0
                end
            ) as qtde_construcao_ferramentas_construcao,
            sum(
                case
                    when product_category_name = 'eletrodomesticos' then 1
                    else 0
                end
            ) as qtde_eletrodomesticos,
            sum(
                case
                    when product_category_name = 'instrumentos_musicais' then 1
                    else 0
                end
            ) as qtde_instrumentos_musicais,
            sum(
                case
                    when product_category_name = 'eletroportateis' then 1
                    else 0
                end
            ) as qtde_eletroportateis,
            sum(
                case
                    when product_category_name = 'casa_construcao' then 1
                    else 0
                end
            ) as qtde_casa_construcao,
            sum(
                case
                    when product_category_name = 'livros_interesse_geral' then 1
                    else 0
                end
            ) as qtde_livros_interesse_geral,
            sum(
                case
                    when product_category_name = 'alimentos' then 1
                    else 0
                end
            ) as qtde_alimentos,
            sum(
                case
                    when product_category_name = 'moveis_sala' then 1
                    else 0
                end
            ) as qtde_moveis_sala,
            sum(
                case
                    when product_category_name = 'casa_conforto' then 1
                    else 0
                end
            ) as qtde_casa_conforto,
            sum(
                case
                    when product_category_name = 'bebidas' then 1
                    else 0
                end
            ) as qtde_bebidas,
            sum(
                case
                    when product_category_name = 'audio' then 1
                    else 0
                end
            ) as qtde_audio,
            sum(
                case
                    when product_category_name = 'market_place' then 1
                    else 0
                end
            ) as qtde_market_place,
            sum(
                case
                    when product_category_name = 'construcao_ferramentas_iluminacao' then 1
                    else 0
                end
            ) as qtde_construcao_ferramentas_iluminacao,
            sum(
                case
                    when product_category_name = 'climatizacao' then 1
                    else 0
                end
            ) as qtde_climatizacao,
            sum(
                case
                    when product_category_name = 'moveis_cozinha_area_de_servico_jantar_e_jardim' then 1
                    else 0
                end
            ) as qtde_moveis_cozinha_area_de_servico_jantar_e_jardim,
            sum(
                case
                    when product_category_name = 'alimentos_bebidas' then 1
                    else 0
                end
            ) as qtde_alimentos_bebidas,
            sum(
                case
                    when product_category_name = 'industria_comercio_e_negocios' then 1
                    else 0
                end
            ) as qtde_industria_comercio_e_negocios,
            sum(
                case
                    when product_category_name = 'livros_tecnicos' then 1
                    else 0
                end
            ) as qtde_livros_tecnicos,
            sum(
                case
                    when product_category_name = 'telefonia_fixa' then 1
                    else 0
                end
            ) as qtde_telefonia_fixa,
            sum(
                case
                    when product_category_name = 'fashion_calcados' then 1
                    else 0
                end
            ) as qtde_fashion_calcados,
            sum(
                case
                    when product_category_name = 'construcao_ferramentas_jardim' then 1
                    else 0
                end
            ) as qtde_construcao_ferramentas_jardim,
            sum(
                case
                    when product_category_name = 'eletrodomesticos_2' then 1
                    else 0
                end
            ) as qtde_eletrodomesticos_2,
            sum(
                case
                    when product_category_name = 'agro_industria_e_comercio' then 1
                    else 0
                end
            ) as qtde_agro_industria_e_comercio,
            sum(
                case
                    when product_category_name = 'artes' then 1
                    else 0
                end
            ) as qtde_artes,
            sum(
                case
                    when product_category_name = 'pcs' then 1
                    else 0
                end
            ) as qtde_pcs,
            sum(
                case
                    when product_category_name = 'sinalizacao_e_seguranca' then 1
                    else 0
                end
            ) as qtde_sinalizacao_e_seguranca,
            sum(
                case
                    when product_category_name = 'construcao_ferramentas_seguranca' then 1
                    else 0
                end
            ) as qtde_construcao_ferramentas_seguranca,
            sum(
                case
                    when product_category_name = 'artigos_de_natal' then 1
                    else 0
                end
            ) as qtde_artigos_de_natal
        FROM olist.tb_orders as t1
            left join olist.tb_order_items as t2 on t1.order_id = t2.order_id
            left join (
                SELECT t2.seller_id,
                    max('{date}'::date - t1.order_approved_at::date) as idade_base
                FROM olist.tb_orders as t1
                    left join olist.tb_order_items as t2 on t1.order_id = t2.order_id
                where t1.order_approved_at < '{date}'
                    and t1.order_status = 'delivered'
                GROUP BY t2.seller_id
                order by t2.seller_id
            ) as t3 on t2.seller_id = t3.seller_id
            left join olist.tb_products as t4 on t2.product_id = t4.product_id
            left join olist.tb_order_reviews as t5 on t1.order_id = t5.order_id
        where t1.order_approved_at BETWEEN to_char(
                '{date}'::date - interval '6 months',
                'yyyy-mm-dd'
            )
            and '{date}'
            and t1.order_status = 'delivered'
        GROUP BY t2.seller_id,
            t3.idade_base
    ) as t1
    left join olist.tb_sellers as t2 on t1.seller_id = t2.seller_id
order by qtde_vendas DESC;