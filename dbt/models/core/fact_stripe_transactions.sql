with stripe_charges as (

    select
        stripe_charge_id,
        stripe_customer_id,
        stripe_payment_intent_id,
        stripe_balance_transaction_id,
        stripe_payment_method_id,
        status,
        currency,
        amount,
        amount_captured,
        amount_refunded,
        is_paid,
        is_captured
    from {{ ref('stg_stripe_charges') }}

),

balance_transactions as (

    select
        stripe_balance_transaction_id,
        stripe_charge_id,
        transaction_type,
        status,
        settlement_currency,
        settlement_gross,
        settlement_fee,
        settlement_net,
        exchange_rate,
        reporting_category,
        description,
        source_created_at
    from {{ ref('stg_stripe_balance_transactions') }}

),

payments as (

    select
        payment_id,
        invoice_id,
        client_id,
        stripe_payment_intent_id
    from {{ ref('fact_payments') }}

),

resolved_transactions as (

    select
        md5(
            'stripe_transaction|'
            || bt.stripe_balance_transaction_id
        ) as stripe_transaction_id,

        p.client_id,
        p.invoice_id,
        p.payment_id,

        -- Stripe lineage
        c.stripe_customer_id,
        c.stripe_payment_intent_id,
        c.stripe_charge_id,
        bt.stripe_balance_transaction_id,
        c.stripe_payment_method_id,

        -- Original charge
        c.status as charge_status,
        c.currency as charge_currency,
        c.amount as charge_amount,
        c.amount_captured,
        c.amount_refunded,
        c.is_paid,
        c.is_captured,

        -- Settlement
        bt.transaction_type,
        bt.status as settlement_status,
        bt.settlement_currency,
        bt.settlement_gross,
        bt.settlement_fee,
        bt.settlement_net,
        bt.exchange_rate,
        bt.reporting_category,
        bt.description,
        bt.source_created_at as settlement_created_at,

        -- Financial controls
        case
            when bt.settlement_gross
                 = bt.settlement_fee + bt.settlement_net
                then true
            else false
        end as settlement_reconciled,

        case
            when c.currency <> bt.settlement_currency
                then true
            else false
        end as has_currency_conversion

    from balance_transactions bt

    left join stripe_charges c
        on c.stripe_balance_transaction_id
         = bt.stripe_balance_transaction_id

    left join payments p
        on p.stripe_payment_intent_id
         = c.stripe_payment_intent_id

)

select *
from resolved_transactions