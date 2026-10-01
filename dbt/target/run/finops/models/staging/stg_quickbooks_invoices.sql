
  create view "finops"."analytics_staging"."stg_quickbooks_invoices__dbt_tmp"
    
    
  as (
    with source as (

    select *
    from "finops"."raw"."api_records"
    where source_system = 'quickbooks'
      and entity_type = 'invoices'

),

renamed as (

    select
        ingestion_id,
        source_record_id as quickbooks_invoice_id,

        payload ->> 'DocNumber'
            as invoice_number,

        payload -> 'CustomerRef' ->> 'value'
            as quickbooks_customer_id,

        payload -> 'CustomerRef' ->> 'name'
            as customer_name,

        (payload ->> 'TxnDate')::date
            as invoice_date,

        (payload ->> 'DueDate')::date
            as due_date,

        (payload ->> 'TotalAmt')::numeric(18, 2)
            as total_amount,

        (payload ->> 'Balance')::numeric(18, 2)
            as balance,

        upper(payload -> 'CurrencyRef' ->> 'value')
            as currency,

        payload ->> 'PrivateNote'
            as private_note,

        nullif(
            replace(
                payload ->> 'PrivateNote',
                'Stripe Invoice: ',
                ''
            ),
            ''
        ) as stripe_invoice_id,

        payload -> 'Line'
            -> 0
            -> 'SalesItemLineDetail'
            -> 'ItemRef'
            ->> 'value'
            as quickbooks_item_id,

        payload -> 'Line'
            -> 0
            -> 'SalesItemLineDetail'
            -> 'ItemAccountRef'
            ->> 'value'
            as quickbooks_revenue_account_id,

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
  );