with source as (

    select *
    from "finops"."raw"."api_records"
    where source_system = 'quickbooks'
      and entity_type = 'customers'

),

renamed as (

    select
        ingestion_id,
        source_record_id as quickbooks_customer_id,

        payload ->> 'DisplayName'
            as customer_name,

        payload ->> 'CompanyName'
            as company_name,

        payload -> 'PrimaryEmailAddr' ->> 'Address'
            as email,

        upper(payload -> 'CurrencyRef' ->> 'value')
            as currency,

        (payload ->> 'Balance')::numeric(18, 2)
            as balance,

        (payload ->> 'Active')::boolean
            as is_active,

        (payload -> 'MetaData' ->> 'CreateTime')::timestamptz
            as source_created_at,

        (payload -> 'MetaData' ->> 'LastUpdatedTime')::timestamptz
            as source_updated_at,

        ingestion_date,
        run_id,
        loaded_at

    from source

)

select *
from renamed