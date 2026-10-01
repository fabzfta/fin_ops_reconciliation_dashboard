
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select settlement_gross
from "finops"."analytics_core"."fact_stripe_transactions"
where settlement_gross is null



  
  
      
    ) dbt_internal_test