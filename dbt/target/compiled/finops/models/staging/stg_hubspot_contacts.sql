with source as (

    select *
    from "finops"."raw"."api_records"
    where source_system = 'hubspot'
      and entity_type = 'contacts'

),

renamed as (

    select
        ingestion_id,
        source_record_id as hubspot_contact_id,

        payload -> 'properties' ->> 'firstname'
            as first_name,

        payload -> 'properties' ->> 'lastname'
            as last_name,

        payload -> 'properties' ->> 'email'
            as email,

        payload -> 'properties' ->> 'phone'
            as phone,

        payload -> 'properties' ->> 'jobtitle'
            as job_title,

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