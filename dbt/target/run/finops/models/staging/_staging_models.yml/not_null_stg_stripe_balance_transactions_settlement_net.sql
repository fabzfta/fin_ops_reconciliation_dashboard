
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select settlement_net
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where settlement_net is null



  
  
      
    ) dbt_internal_test