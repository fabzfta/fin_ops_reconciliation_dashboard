
    
    

with all_values as (

    select
        entity_type as value_field,
        count(*) as n_records

    from "finops"."analytics_core"."identity_map"
    group by entity_type

)

select *
from all_values
where value_field not in (
    'client'
)


