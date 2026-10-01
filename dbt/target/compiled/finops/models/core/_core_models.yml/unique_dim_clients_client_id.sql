
    
    

select
    client_id as unique_field,
    count(*) as n_records

from "finops"."analytics_core"."dim_clients"
where client_id is not null
group by client_id
having count(*) > 1


