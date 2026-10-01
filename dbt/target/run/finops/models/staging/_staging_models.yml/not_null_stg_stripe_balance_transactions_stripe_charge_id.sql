
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select stripe_charge_id
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where stripe_charge_id is null



  
  
      
    ) dbt_internal_test