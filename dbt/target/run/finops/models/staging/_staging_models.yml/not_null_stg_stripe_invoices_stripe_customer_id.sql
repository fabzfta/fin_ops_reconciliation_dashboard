
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select stripe_customer_id
from "finops"."analytics_staging"."stg_stripe_invoices"
where stripe_customer_id is null



  
  
      
    ) dbt_internal_test