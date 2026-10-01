
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select payment_id
from "finops"."analytics_core"."fact_stripe_transactions"
where payment_id is null



  
  
      
    ) dbt_internal_test