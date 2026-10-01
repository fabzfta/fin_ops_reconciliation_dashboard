
    
    



select stripe_payment_intent_id
from "finops"."analytics_staging"."stg_quickbooks_payments"
where stripe_payment_intent_id is null


