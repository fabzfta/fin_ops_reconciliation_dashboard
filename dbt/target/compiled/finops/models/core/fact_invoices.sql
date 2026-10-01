with stripe_invoices as (

    select
        stripe_invoice_id,
        stripe_customer_id,
        invoice_number,
        status,
        currency,
        subtotal,
        total_amount,
        amount_due,
        amount_paid,
        amount_remaining,
        stripe_subscription_id,
        hubspot_deal_id
    from "finops"."analytics_staging"."stg_stripe_invoices"

),

quickbooks_invoices as (

    select
        quickbooks_invoice_id,
        invoice_number,
        quickbooks_customer_id,
        customer_name,
        invoice_date,
        due_date,
        total_amount,
        balance,
        currency,
        stripe_invoice_id,
        quickbooks_item_id
    from "finops"."analytics_staging"."stg_quickbooks_invoices"

),

stripe_identity as (

    select
        client_id,
        external_id as stripe_customer_id
    from "finops"."analytics_core"."identity_map"
    where source_system = 'stripe'
      and entity_type = 'client'

),

resolved_invoices as (

    select
        md5(
            'invoice|stripe|' || si.stripe_invoice_id
        ) as invoice_id,

        ident.client_id,

        -- Cross-system lineage
        si.hubspot_deal_id,
        si.stripe_invoice_id,
        qi.quickbooks_invoice_id,

        -- Customer lineage
        si.stripe_customer_id,
        qi.quickbooks_customer_id,

        -- Invoice references
        si.invoice_number as stripe_invoice_number,
        qi.invoice_number as quickbooks_invoice_number,

        -- Stripe billing state
        si.status as invoice_status,
        si.currency,

        si.subtotal,
        si.total_amount,
        si.amount_due,
        si.amount_paid,
        si.amount_remaining,

        -- QuickBooks accounting state
        qi.total_amount as quickbooks_total_amount,
        qi.balance as quickbooks_balance,

        -- Additional lineage
        si.stripe_subscription_id,
        qi.quickbooks_item_id,

        -- Accounting dates
        qi.invoice_date,
        qi.due_date,

        -- Reconciliation controls
        case
            when qi.quickbooks_invoice_id is not null
                then true
            else false
        end as is_synced_to_quickbooks,

        case
            when qi.quickbooks_invoice_id is null
                then null

            when si.currency <> qi.currency
                then false

            when si.total_amount = qi.total_amount
                then true

            else false
        end as amount_reconciled

    from stripe_invoices si

    left join stripe_identity ident
        on ident.stripe_customer_id = si.stripe_customer_id

    left join quickbooks_invoices qi
        on qi.stripe_invoice_id = si.stripe_invoice_id

)

select *
from resolved_invoices