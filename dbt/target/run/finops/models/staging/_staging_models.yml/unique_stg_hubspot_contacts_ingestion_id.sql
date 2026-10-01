
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    ingestion_id as unique_field,
    count(*) as n_records

from "finops"."analytics_staging"."stg_hubspot_contacts"
where ingestion_id is not null
group by ingestion_id
having count(*) > 1



  
  
      
    ) dbt_internal_test