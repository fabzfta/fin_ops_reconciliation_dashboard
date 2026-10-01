
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select entity_type
from "finops"."analytics_core"."identity_map"
where entity_type is null



  
  
      
    ) dbt_internal_test