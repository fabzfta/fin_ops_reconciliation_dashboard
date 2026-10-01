
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select source_system
from "finops"."analytics_core"."identity_map"
where source_system is null



  
  
      
    ) dbt_internal_test