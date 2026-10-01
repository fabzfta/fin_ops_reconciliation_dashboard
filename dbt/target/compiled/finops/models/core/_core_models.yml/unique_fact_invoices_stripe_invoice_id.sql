
    
    

select
    stripe_invoice_id as unique_field,
    count(*) as n_records

from "finops"."analytics_core"."fact_invoices"
where stripe_invoice_id is not null
group by stripe_invoice_id
having count(*) > 1


