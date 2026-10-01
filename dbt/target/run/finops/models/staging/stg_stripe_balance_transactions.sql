
  create view "finops"."analytics_staging"."stg_stripe_balance_transactions__dbt_tmp"
    
    
  as (
    with source as (

    select *
    from "finops"."raw"."api_records"
    where source_system = 'stripe'
      and entity_type = 'balance_transactions'

),

renamed as (

    select
        ingestion_id,
        source_record_id as stripe_balance_transaction_id,

        payload ->> 'source'
            as stripe_charge_id,

        payload ->> 'type'
            as transaction_type,

        payload ->> 'status'
            as status,

        upper(payload ->> 'currency')
            as settlement_currency,

        (payload ->> 'amount')::numeric / 100.0
            as settlement_gross,

        (payload ->> 'fee')::numeric / 100.0
            as settlement_fee,

        (payload ->> 'net')::numeric / 100.0
            as settlement_net,

        (payload ->> 'exchange_rate')::numeric
            as exchange_rate,

        payload ->> 'reporting_category'
            as reporting_category,

        payload ->> 'description'
            as description,

        to_timestamp(
            (payload ->> 'created')::bigint
        ) as source_created_at,

        to_timestamp(
            (payload ->> 'available_on')::bigint
        ) as available_at,

        ingestion_date,
        run_id,
        loaded_at

    from source

)

select *
from renamed
  );