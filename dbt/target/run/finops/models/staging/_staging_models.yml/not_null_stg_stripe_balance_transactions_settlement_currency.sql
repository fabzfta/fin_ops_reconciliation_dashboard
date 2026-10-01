
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select settlement_currency
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where settlement_currency is null



  
  
      
    ) dbt_internal_test