
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    hubspot_company_id as unique_field,
    count(*) as n_records

from "finops"."analytics_core"."dim_clients"
where hubspot_company_id is not null
group by hubspot_company_id
having count(*) > 1



  
  
      
    ) dbt_internal_test