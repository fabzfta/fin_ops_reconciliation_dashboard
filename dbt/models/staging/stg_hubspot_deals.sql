with source as (

    select *
    from {{ source('raw', 'api_records') }}
    where source_system = 'hubspot'
      and entity_type = 'deals'

),

renamed as (

    select
        ingestion_id,
        source_record_id as hubspot_deal_id,

        payload -> 'properties' ->> 'dealname'
            as deal_name,

        (payload -> 'properties' ->> 'amount')::numeric(18, 2)
            as deal_amount,

        payload -> 'properties' ->> 'pipeline'
            as pipeline,

        payload -> 'properties' ->> 'dealstage'
            as deal_stage,

        (payload -> 'properties' ->> 'closedate')::timestamptz
            as closed_at,

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