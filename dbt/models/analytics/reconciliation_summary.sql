with invoices as (

    select *
    from {{ ref('fact_invoices') }}

),

payments as (

    select *
    from {{ ref('fact_payments') }}

),

stripe_transactions as (

    select *
    from {{ ref('fact_stripe_transactions') }}

),

clients as (

    select *
    from {{ ref('dim_clients') }}

),

reconciliation as (

    select
        i.invoice_id,
        i.client_id,
        c.company_name,

        -- Business lineage
        i.hubspot_deal_id,
        i.stripe_invoice_id,
        i.quickbooks_invoice_id,

        p.payment_id,
        p.stripe_payment_intent_id,
        p.quickbooks_payment_id,

        st.stripe_charge_id,
        st.stripe_balance_transaction_id,

        -- Invoice
        i.currency as invoice_currency,
        i.total_amount as invoice_amount,
        i.quickbooks_total_amount,
        i.invoice_status,

        -- Payment
        p.payment_status,
        p.payment_amount,
        p.amount_received,
        p.quickbooks_payment_amount,

        -- Settlement
        st.charge_currency,
        st.charge_amount,

        st.settlement_currency,
        st.settlement_gross,
        st.settlement_fee,
        st.settlement_net,
        st.exchange_rate,

        -- Individual controls
        i.is_synced_to_quickbooks as invoice_synced,
        i.amount_reconciled as invoice_reconciled,

        p.is_recorded_in_quickbooks as payment_recorded,
        p.amount_reconciled as payment_reconciled,

        st.settlement_reconciled,
        st.has_currency_conversion,

        -- Differences
        i.total_amount
            - i.quickbooks_total_amount
            as invoice_difference,

        p.amount_received
            - p.quickbooks_payment_amount
            as payment_difference,

        st.settlement_gross
            - st.settlement_fee
            - st.settlement_net
            as settlement_difference,

        -- Overall reconciliation
        case
            when i.amount_reconciled = true
             and p.amount_reconciled = true
             and st.settlement_reconciled = true
                then 'RECONCILED'

            else 'EXCEPTION'
        end as reconciliation_status,

        -- Exception reason
        case
            when i.amount_reconciled is not true
                then 'INVOICE_MISMATCH'

            when p.amount_reconciled is not true
                then 'PAYMENT_MISMATCH'

            when st.settlement_reconciled is not true
                then 'SETTLEMENT_MISMATCH'

            else null
        end as exception_reason

    from invoices i

    left join clients c
        on c.client_id = i.client_id

    left join payments p
        on p.invoice_id = i.invoice_id

    left join stripe_transactions st
        on st.payment_id = p.payment_id

)

select *
from reconciliation