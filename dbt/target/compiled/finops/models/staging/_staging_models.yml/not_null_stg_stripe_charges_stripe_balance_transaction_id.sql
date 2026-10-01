
    
    



select stripe_balance_transaction_id
from "finops"."analytics_staging"."stg_stripe_charges"
where stripe_balance_transaction_id is null


