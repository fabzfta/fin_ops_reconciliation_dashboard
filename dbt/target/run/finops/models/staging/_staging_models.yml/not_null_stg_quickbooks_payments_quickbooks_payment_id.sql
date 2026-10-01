
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select quickbooks_payment_id
from "finops"."analytics_staging"."stg_quickbooks_payments"
where quickbooks_payment_id is null



  
  
      
    ) dbt_internal_test