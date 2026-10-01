
    
    

select
    stripe_payment_intent_id as unique_field,
    count(*) as n_records

from "finops"."analytics_core"."fact_payments"
where stripe_payment_intent_id is not null
group by stripe_payment_intent_id
having count(*) > 1


