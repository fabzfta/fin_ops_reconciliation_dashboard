with reconciliation as (

    select *
    from "finops"."analytics_analytics"."reconciliation_summary"

),

scenarios as (

    select *
    from "finops"."analytics_test_data"."reconciliation_test_scenarios"

),

simulated as (

    select
        r.*,

        s.scenario_name,

        coalesce(
            s.quickbooks_invoice_override,
            r.quickbooks_total_amount
        ) as simulated_quickbooks_total_amount

    from reconciliation r

    left join scenarios s
        on s.stripe_invoice_id = r.stripe_invoice_id

)

select
    *,

    invoice_amount
        - simulated_quickbooks_total_amount
        as simulated_invoice_difference,

    case
        when invoice_amount
             = simulated_quickbooks_total_amount
         and payment_reconciled = true
         and settlement_reconciled = true
            then 'RECONCILED'

        else 'EXCEPTION'
    end as simulated_reconciliation_status,

    case
        when invoice_amount
             <> simulated_quickbooks_total_amount
            then 'INVOICE_MISMATCH'

        when payment_reconciled is not true
            then 'PAYMENT_MISMATCH'

        when settlement_reconciled is not true
            then 'SETTLEMENT_MISMATCH'

        else null
    end as simulated_exception_reason

from simulated