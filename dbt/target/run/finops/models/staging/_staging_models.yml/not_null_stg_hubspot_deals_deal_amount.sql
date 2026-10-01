
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select deal_amount
from "finops"."analytics_staging"."stg_hubspot_deals"
where deal_amount is null



  
  
      
    ) dbt_internal_test