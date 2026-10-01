
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select has_currency_conversion
from "finops"."analytics_core"."fact_stripe_transactions"
where has_currency_conversion is null



  
  
      
    ) dbt_internal_test