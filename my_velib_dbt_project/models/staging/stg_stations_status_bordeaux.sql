
with 

final as (
    select
        *
    from {{source('bordeaux_source', 'bordeaux_all_tables')}}
)

select 
    * 
from 
    final