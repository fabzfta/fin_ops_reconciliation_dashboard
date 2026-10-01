with source as (

    select *
    from {{ source('raw', 'api_records') }}
    where source_system = 'stripe'
      and entity_type = 'invoices'

),

renamed as (

    select
        ingestion_id,
        source_record_id as stripe_invoice_id,

        payload ->> 'customer'
            as stripe_customer_id,

        payload ->> 'number'
            as invoice_number,

        payload ->> 'status'
            as status,

        upper(payload ->> 'currency')
            as currency,

        (payload ->> 'subtotal')::numeric / 100.0
            as subtotal,

        (payload ->> 'total')::numeric / 100.0
            as total_amount,

        (payload ->> 'amount_due')::numeric / 100.0
            as amount_due,

        (payload ->> 'amount_paid')::numeric / 100.0
            as amount_paid,

        (payload ->> 'amount_remaining')::numeric / 100.0
            as amount_remaining,

        payload -> 'parent'
            -> 'subscription_details'
            ->> 'subscription'
            as stripe_subscription_id,

        payload -> 'parent'
            -> 'subscription_details'
            -> 'metadata'
            ->> 'hubspot_deal_id'
            as hubspot_deal_id,

        payload -> 'lines'
            -> 'data'
            -> 0
            -> 'pricing'
            -> 'price_details'
            ->> 'product'
            as stripe_product_id,

        payload -> 'lines'
            -> 'data'
            -> 0
            -> 'pricing'
            -> 'price_details'
            ->> 'price'
            as stripe_price_id,

        payload ->> 'billing_reason'
            as billing_reason,

        to_timestamp(
            (payload ->> 'created')::bigint
        ) as source_created_at,

        to_timestamp(
            (payload ->> 'period_start')::bigint
        ) as period_start,

        to_timestamp(
            (payload ->> 'period_end')::bigint
        ) as period_end,

        ingestion_date,
        run_id,
        loaded_at

    from source

)

select *
from renamed