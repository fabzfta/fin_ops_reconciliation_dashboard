
    
    



select stripe_payment_intent_id
from "finops"."analytics_staging"."stg_stripe_payment_intent"
where stripe_payment_intent_id is null


