-- select * 
-- from olist.tb_book_sellers

-- where seller_id = 'cca3071e3e9bb7d12640c9fbe2301306'
-- order by dt_ref


SELECT  to_char(t1.order_approved_at::date, 'YYYY-MM') || '-01' as dt_venda,
        t2.seller_id,
        max(1) as venda

    from olist.tb_orders as t1

    left join olist.tb_order_items as t2
    on t1.order_id = t2.order_id

    where t1.order_approved_at is not null
    and t2.seller_id is not null
    and t1.order_status = 'delivered'

GROUP BY to_char(t1.order_approved_at::date, 'YYYY-MM') || '-01', t2.seller_id
ORDER BY t2.seller_id, to_char(t1.order_approved_at::date, 'YYYY-MM') || '-01'
