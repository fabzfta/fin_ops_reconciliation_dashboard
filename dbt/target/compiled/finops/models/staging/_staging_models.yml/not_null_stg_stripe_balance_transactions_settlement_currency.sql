
    
    



select settlement_currency
from "finops"."analytics_staging"."stg_stripe_balance_transactions"
where settlement_currency is null


