
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select client_id
from "finops"."analytics_core"."fact_stripe_transactions"
where client_id is null



  
  
      
    ) dbt_internal_test