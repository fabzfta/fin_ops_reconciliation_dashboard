
    
    



select settlement_currency
from "finops"."analytics_core"."fact_stripe_transactions"
where settlement_currency is null


