
with 

final as (
    select
        *
    from {{source('lyon_source', 'lyon_all_tables')}}
)

select 
    * 
from 
    final