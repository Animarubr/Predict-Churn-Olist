SELECT *,
    case when order_estimated_delivery_date::date < order_delivered_carrier_date::date then 1 else 0 end as atraso 
FROM olist.tb_orders