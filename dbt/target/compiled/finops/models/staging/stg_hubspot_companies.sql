with source as (

    select *
    from "finops"."raw"."api_records"
    where source_system = 'hubspot'
      and entity_type = 'companies'

),
renamed as (
    select
        ingestion_id,
        source_record_id as hubspot_company_id,
        payload -> 'properties' ->> 'name'
            as company_name,
        payload -> 'properties' ->> 'domain'
            as domain,
        payload -> 'properties' ->> 'industry'
            as industry,
        payload -> 'properties' ->> 'city'
            as city,
        payload -> 'properties' ->> 'state'
            as state,
        payload -> 'properties' ->> 'country'
            as country,
        (payload ->> 'createdAt')::timestamptz
            as source_created_at,
        (payload ->> 'updatedAt')::timestamptz
            as source_updated_at,
        coalesce(
            (payload ->> 'archived')::boolean,
            false
        ) as is_archived,
        ingestion_date,
        run_id,
        loaded_at
    from source
)
select *
from renamed