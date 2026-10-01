
  
    

  create  table "finops"."analytics_core"."identity_map__dbt_tmp"
  
  
    as
  
  (
    with hubspot_companies as (

    select
        hubspot_company_id,
        company_name
    from "finops"."analytics_staging"."stg_hubspot_companies"

),

stripe_customers as (

    select
        stripe_customer_id,
        hubspot_company_id,
        customer_name,
        email
    from "finops"."analytics_staging"."stg_stripe_customers"

),

stripe_invoices as (

    select
        stripe_invoice_id,
        stripe_customer_id
    from "finops"."analytics_staging"."stg_stripe_invoices"

),

quickbooks_invoices as (

    select
        quickbooks_invoice_id,
        quickbooks_customer_id,
        stripe_invoice_id
    from "finops"."analytics_staging"."stg_quickbooks_invoices"

),

resolved_entities as (

    select distinct
        h.hubspot_company_id,
        s.stripe_customer_id,
        q.quickbooks_customer_id,
        h.company_name

    from hubspot_companies h

    left join stripe_customers s
        on s.hubspot_company_id = h.hubspot_company_id

    left join stripe_invoices si
        on si.stripe_customer_id = s.stripe_customer_id

    left join quickbooks_invoices q
        on q.stripe_invoice_id = si.stripe_invoice_id

),

with_internal_id as (

    select
        md5(
            'client|hubspot|'
            || hubspot_company_id
        ) as client_id,

        hubspot_company_id,
        stripe_customer_id,
        quickbooks_customer_id,
        company_name

    from resolved_entities

),

identity_records as (

    select
        client_id,
        'client' as entity_type,
        'hubspot' as source_system,
        hubspot_company_id as external_id,
        company_name

    from with_internal_id
    where hubspot_company_id is not null

    union all

    select
        client_id,
        'client' as entity_type,
        'stripe' as source_system,
        stripe_customer_id as external_id,
        company_name

    from with_internal_id
    where stripe_customer_id is not null

    union all

    select
        client_id,
        'client' as entity_type,
        'quickbooks' as source_system,
        quickbooks_customer_id as external_id,
        company_name

    from with_internal_id
    where quickbooks_customer_id is not null

)

select
    client_id,
    entity_type,
    source_system,
    external_id,
    company_name

from identity_records
  );
  