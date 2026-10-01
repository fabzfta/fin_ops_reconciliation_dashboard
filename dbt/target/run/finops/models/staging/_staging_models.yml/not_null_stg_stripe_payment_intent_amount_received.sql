
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select amount_received
from "finops"."analytics_staging"."stg_stripe_payment_intent"
where amount_received is null



  
  
      
    ) dbt_internal_test