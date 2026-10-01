
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select currency
from "finops"."analytics_core"."fact_payments"
where currency is null



  
  
      
    ) dbt_internal_test