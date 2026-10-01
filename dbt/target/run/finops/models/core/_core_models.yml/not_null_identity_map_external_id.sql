
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select external_id
from "finops"."analytics_core"."identity_map"
where external_id is null



  
  
      
    ) dbt_internal_test