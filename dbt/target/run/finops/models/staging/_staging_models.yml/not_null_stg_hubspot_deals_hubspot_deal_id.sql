
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hubspot_deal_id
from "finops"."analytics_staging"."stg_hubspot_deals"
where hubspot_deal_id is null



  
  
      
    ) dbt_internal_test