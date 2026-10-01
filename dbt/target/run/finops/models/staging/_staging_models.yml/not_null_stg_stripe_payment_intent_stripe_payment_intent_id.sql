
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select stripe_payment_intent_id
from "finops"."analytics_staging"."stg_stripe_payment_intent"
where stripe_payment_intent_id is null



  
  
      
    ) dbt_internal_test