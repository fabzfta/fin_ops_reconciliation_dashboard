
    
    



select settlement_net
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where settlement_net is null


