
    
    

select
    stripe_balance_transaction_id as unique_field,
    count(*) as n_records

from "finops"."analytics_core"."fact_stripe_transactions"
where stripe_balance_transaction_id is not null
group by stripe_balance_transaction_id
having count(*) > 1


