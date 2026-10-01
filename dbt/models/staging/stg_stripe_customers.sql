with source as (

    select *
    from {{ source('raw', 'api_records') }}
    where source_system = 'stripe'
      and entity_type = 'customers'

),

renamed as (

    select
        ingestion_id,
        source_record_id as stripe_customer_id,

        payload ->> 'name'
            as customer_name,

        payload ->> 'email'
            as email,

        upper(payload ->> 'currency')
            as currency,

        payload -> 'metadata' ->> 'hubspot_company_id'
            as hubspot_company_id,

        (payload ->> 'delinquent')::boolean
            as is_delinquent,

        to_timestamp(
            (payload ->> 'created')::bigint
        ) as source_created_at,

        ingestion_date,
        run_id,
        loaded_at

    from source

)

select *
from renamed