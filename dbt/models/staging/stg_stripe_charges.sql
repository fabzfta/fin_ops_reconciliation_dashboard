with source as (

    select *
    from {{ source('raw', 'api_records') }}
    where source_system = 'stripe'
      and entity_type = 'charges'

),

renamed as (

    select
        ingestion_id,
        source_record_id as stripe_charge_id,

        payload ->> 'customer'
            as stripe_customer_id,

        payload ->> 'payment_intent'
            as stripe_payment_intent_id,

        payload ->> 'balance_transaction'
            as stripe_balance_transaction_id,

        payload ->> 'payment_method'
            as stripe_payment_method_id,

        payload ->> 'status'
            as status,

        upper(payload ->> 'currency')
            as currency,

        (payload ->> 'amount')::numeric / 100.0
            as amount,

        (payload ->> 'amount_captured')::numeric / 100.0
            as amount_captured,

        (payload ->> 'amount_refunded')::numeric / 100.0
            as amount_refunded,

        (payload ->> 'paid')::boolean
            as is_paid,

        (payload ->> 'captured')::boolean
            as is_captured,

        (payload ->> 'refunded')::boolean
            as is_refunded,

        (payload ->> 'disputed')::boolean
            as is_disputed,

        payload -> 'payment_method_details'
            -> 'card'
            ->> 'brand'
            as card_brand,

        payload -> 'payment_method_details'
            -> 'card'
            ->> 'funding'
            as card_funding,

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