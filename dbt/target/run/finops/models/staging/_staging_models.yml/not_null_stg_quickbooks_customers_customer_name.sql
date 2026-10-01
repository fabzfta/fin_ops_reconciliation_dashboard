
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_name
from "finops"."analytics_staging"."stg_quickbooks_customers"
where customer_name is null



  
  
      
    ) dbt_internal_test