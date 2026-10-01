
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select company_name
from "finops"."analytics_staging"."stg_hubspot_companies"
where company_name is null



  
  
      
    ) dbt_internal_test