
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select amount_received
from "finops"."analytics_core"."fact_payments"
where amount_received is null



  
  
      
    ) dbt_internal_test