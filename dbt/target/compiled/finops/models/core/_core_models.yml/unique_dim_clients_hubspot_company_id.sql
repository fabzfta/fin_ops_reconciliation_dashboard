
    
    

select
    hubspot_company_id as unique_field,
    count(*) as n_records

from "finops"."analytics_core"."dim_clients"
where hubspot_company_id is not null
group by hubspot_company_id
having count(*) > 1


