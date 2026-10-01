
    
    



select stripe_invoice_id
from "finops"."analytics_staging"."stg_stripe_payment_intent"
where stripe_invoice_id is null


