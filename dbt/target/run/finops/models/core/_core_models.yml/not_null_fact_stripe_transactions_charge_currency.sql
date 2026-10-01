
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select charge_currency
from "finops"."analytics_core"."fact_stripe_transactions"
where charge_currency is null



  
  
      
    ) dbt_internal_test