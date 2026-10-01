with identity as (

    select *
    from {{ ref('identity_map') }}

),

hubspot_companies as (

    select
        hubspot_company_id,
        company_name,
        domain,
        industry,
        city,
        state,
        country
    from {{ ref('stg_hubspot_companies') }}

),

stripe_customers as (

    select
        stripe_customer_id,
        email,
        currency,
        is_delinquent
    from {{ ref('stg_stripe_customers') }}

),

resolved_clients as (

    select
        h.client_id,

        h.external_id as hubspot_company_id,
        s.external_id as stripe_customer_id,
        q.external_id as quickbooks_customer_id,

        hc.company_name,
        hc.domain,
        hc.industry,
        hc.city,
        hc.state,
        hc.country,

        sc.email as billing_email,
        sc.currency as billing_currency,
        sc.is_delinquent

    from identity h

    left join identity s
        on s.client_id = h.client_id
        and s.source_system = 'stripe'

    left join identity q
        on q.client_id = h.client_id
        and q.source_system = 'quickbooks'

    left join hubspot_companies hc
        on hc.hubspot_company_id = h.external_id

    left join stripe_customers sc
        on sc.stripe_customer_id = s.external_id

    where h.source_system = 'hubspot'

)

select *
from resolved_clients