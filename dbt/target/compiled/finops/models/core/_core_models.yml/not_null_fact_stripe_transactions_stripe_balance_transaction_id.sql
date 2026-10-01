
    
    



select stripe_balance_transaction_id
from "finops"."analytics_core"."fact_stripe_transactions"
where stripe_balance_transaction_id is null


