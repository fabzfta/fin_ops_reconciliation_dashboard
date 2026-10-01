
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hubspot_contact_id
from "finops"."analytics_staging"."stg_hubspot_contacts"
where hubspot_contact_id is null



  
  
      
    ) dbt_internal_test