
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ingestion_id
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where ingestion_id is null



  
  
      
    ) dbt_internal_test