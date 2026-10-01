
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select email
from "finops"."analytics_staging"."stg_hubspot_contacts"
where email is null



  
  
      
    ) dbt_internal_test