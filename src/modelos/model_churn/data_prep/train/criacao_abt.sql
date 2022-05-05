drop table if exists olist.tb_abt_churn;

create table olist.tb_abt_churn as 
    select  t2.*,
            t1.flag_churn
    from (
        select  t1.dt_ref,
                t1.seller_id,
                min(coalesce(t2.venda,1)) as flag_churn

        from olist.tb_book_sellers as t1

        left join (
            SELECT  to_char(t1.order_approved_at::date, 'YYYY-MM') || '-01' as dt_venda,
                    t2.seller_id,
                    max(0) as venda

                from olist.tb_orders as t1

                left join olist.tb_order_items as t2
                on t1.order_id = t2.order_id

                where t1.order_approved_at is not null
                and t2.seller_id is not null
                and t1.order_status = 'delivered'

            GROUP BY to_char(t1.order_approved_at::date, 'YYYY-MM') || '-01', t2.seller_id
            ORDER BY t2.seller_id, to_char(t1.order_approved_at::date, 'YYYY-MM') || '-01'
        ) as t2
        on t1.seller_id = t2.seller_id
        and t2.dt_venda between t1.dt_ref and to_char(t1.dt_ref::date + interval '2 months',
                        'yyyy-mm-dd')


        group by t1.dt_ref, t1.seller_id

        order by dt_ref
    ) as t1

    left join olist.tb_book_sellers as t2
    on t1.seller_id = t2.seller_id
    and t1.dt_ref = t2.dt_ref

    order by seller_id
;