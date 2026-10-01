
    
    



select stripe_charge_id
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where stripe_charge_id is null


