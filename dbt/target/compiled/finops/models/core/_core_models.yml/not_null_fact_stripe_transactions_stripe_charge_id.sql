
    
    



select stripe_charge_id
from "finops"."analytics_core"."fact_stripe_transactions"
where stripe_charge_id is null


