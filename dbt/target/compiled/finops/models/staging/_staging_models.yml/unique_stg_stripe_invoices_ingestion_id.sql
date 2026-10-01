
    
    

select
    ingestion_id as unique_field,
    count(*) as n_records

from "finops"."analytics_staging"."stg_stripe_invoices"
where ingestion_id is not null
group by ingestion_id
having count(*) > 1


