
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select is_synced_to_quickbooks
from "finops"."analytics_core"."fact_invoices"
where is_synced_to_quickbooks is null



  
  
      
    ) dbt_internal_test