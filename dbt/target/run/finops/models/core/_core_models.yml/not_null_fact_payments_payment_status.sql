
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select payment_status
from "finops"."analytics_core"."fact_payments"
where payment_status is null



  
  
      
    ) dbt_internal_test