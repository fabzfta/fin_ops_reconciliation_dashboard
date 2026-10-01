with source as (

    select *
    from {{ source('raw', 'api_records') }}
    where source_system = 'stripe'
      and entity_type = 'payment_intents'

),

renamed as (

    select
        ingestion_id,
        source_record_id as stripe_payment_intent_id,

        payload ->> 'customer'
            as stripe_customer_id,

        payload ->> 'latest_charge'
            as stripe_charge_id,

        payload -> 'payment_details' ->> 'order_reference'
            as stripe_invoice_id,

        payload ->> 'payment_method'
            as stripe_payment_method_id,

        payload ->> 'status'
            as status,

        upper(payload ->> 'currency')
            as currency,

        (payload ->> 'amount')::numeric / 100.0
            as amount,

        (payload ->> 'amount_received')::numeric / 100.0
            as amount_received,

        payload ->> 'description'
            as description,

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