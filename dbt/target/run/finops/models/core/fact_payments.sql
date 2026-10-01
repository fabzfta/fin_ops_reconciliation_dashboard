
  
    

  create  table "finops"."analytics_core"."fact_payments__dbt_tmp"
  
  
    as
  
  (
    with stripe_payments as (

    select
        stripe_payment_intent_id,
        stripe_customer_id,
        stripe_charge_id,
        stripe_invoice_id,
        stripe_payment_method_id,
        status,
        currency,
        amount,
        amount_received,
        description,
        source_created_at
    from "finops"."analytics_staging"."stg_stripe_payment_intent"

),

quickbooks_payments as (

    select
        quickbooks_payment_id,
        quickbooks_customer_id,
        quickbooks_invoice_id,
        payment_date,
        amount,
        unapplied_amount,
        currency,
        deposit_account_id,
        stripe_payment_intent_id,
        source_created_at
    from "finops"."analytics_staging"."stg_quickbooks_payments"

),

stripe_identity as (

    select
        client_id,
        external_id as stripe_customer_id
    from "finops"."analytics_core"."identity_map"
    where source_system = 'stripe'
      and entity_type = 'client'

),

invoices as (

    select
        invoice_id,
        stripe_invoice_id,
        quickbooks_invoice_id
    from "finops"."analytics_core"."fact_invoices"

),

resolved_payments as (

    select
        md5(
            'payment|stripe|' || sp.stripe_payment_intent_id
        ) as payment_id,

        ident.client_id,
        i.invoice_id,

        -- Cross-system lineage
        sp.stripe_payment_intent_id,
        qp.quickbooks_payment_id,

        sp.stripe_invoice_id,
        qp.quickbooks_invoice_id,

        sp.stripe_charge_id,
        sp.stripe_payment_method_id,

        -- Payment state
        sp.status as payment_status,
        sp.currency,

        sp.amount as payment_amount,
        sp.amount_received,

        -- QuickBooks accounting representation
        qp.amount as quickbooks_payment_amount,
        qp.unapplied_amount as quickbooks_unapplied_amount,
        qp.deposit_account_id,

        -- Dates
        sp.source_created_at as payment_created_at,
        qp.payment_date as quickbooks_payment_date,

        -- Reconciliation controls
        case
            when qp.quickbooks_payment_id is not null
                then true
            else false
        end as is_recorded_in_quickbooks,

        case
            when qp.quickbooks_payment_id is null
                then null

            when sp.currency <> qp.currency
                then false

            when sp.amount_received = qp.amount
                then true

            else false
        end as amount_reconciled

    from stripe_payments sp

    left join stripe_identity ident
        on ident.stripe_customer_id = sp.stripe_customer_id

    left join invoices i
        on i.stripe_invoice_id = sp.stripe_invoice_id

    left join quickbooks_payments qp
        on qp.stripe_payment_intent_id = sp.stripe_payment_intent_id

)

select *
from resolved_payments
  );
  