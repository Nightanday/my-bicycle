
with 

final as (
    select
        *
    from {{source('paris_source', 'paris_all_tables')}}
)

select 
    * 
from 
    final