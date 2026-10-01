
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select amount_reconciled
from "finops"."analytics_core"."fact_invoices"
where amount_reconciled is null



  
  
      
    ) dbt_internal_test