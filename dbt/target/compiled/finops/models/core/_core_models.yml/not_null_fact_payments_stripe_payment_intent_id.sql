
    
    



select stripe_payment_intent_id
from "finops"."analytics_core"."fact_payments"
where stripe_payment_intent_id is null


