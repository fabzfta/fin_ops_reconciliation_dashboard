
    
    



select stripe_payment_intent_id
from "finops"."analytics_staging"."stg_stripe_charges"
where stripe_payment_intent_id is null


