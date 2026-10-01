
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select quickbooks_invoice_id
from "finops"."analytics_staging"."stg_quickbooks_invoices"
where quickbooks_invoice_id is null



  
  
      
    ) dbt_internal_test