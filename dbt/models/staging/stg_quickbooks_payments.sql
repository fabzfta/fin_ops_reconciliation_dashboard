with source as (

    select *
    from {{ source('raw', 'api_records') }}
    where source_system = 'quickbooks'
      and entity_type = 'payments'

),

renamed as (

    select
        ingestion_id,
        source_record_id as quickbooks_payment_id,

        payload -> 'CustomerRef' ->> 'value'
            as quickbooks_customer_id,

        payload -> 'CustomerRef' ->> 'name'
            as customer_name,

        payload -> 'Line'
            -> 0
            -> 'LinkedTxn'
            -> 0
            ->> 'TxnId'
            as quickbooks_invoice_id,

        (payload ->> 'TxnDate')::date
            as payment_date,

        (payload ->> 'TotalAmt')::numeric(18, 2)
            as amount,

        (payload ->> 'UnappliedAmt')::numeric(18, 2)
            as unapplied_amount,

        upper(payload -> 'CurrencyRef' ->> 'value')
            as currency,

        payload -> 'DepositToAccountRef' ->> 'value'
            as deposit_account_id,

        payload ->> 'PrivateNote'
            as private_note,

        nullif(
            replace(
                payload ->> 'PrivateNote',
                'Stripe PaymentIntent: ',
                ''
            ),
            ''
        ) as stripe_payment_intent_id,

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