
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select company_name
from "finops"."analytics_core"."dim_clients"
where company_name is null



  
  
      
    ) dbt_internal_test