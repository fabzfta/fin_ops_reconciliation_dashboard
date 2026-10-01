
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select payment_amount
from "finops"."analytics_core"."fact_payments"
where payment_amount is null



  
  
      
    ) dbt_internal_test