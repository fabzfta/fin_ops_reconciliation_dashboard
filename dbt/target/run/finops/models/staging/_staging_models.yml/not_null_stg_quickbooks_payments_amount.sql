
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select amount
from "finops"."analytics_staging"."stg_quickbooks_payments"
where amount is null



  
  
      
    ) dbt_internal_test